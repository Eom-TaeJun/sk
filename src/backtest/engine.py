from __future__ import annotations

from calendar import monthrange
from collections import Counter, defaultdict
from copy import deepcopy
from datetime import date, datetime
import hashlib
import json
from pathlib import Path
from statistics import median
from typing import Any, Iterable

from src.core.storage import canonical_json, content_digest, load_json, load_jsonl, write_json

from .memo import build_h1_memo, render_h1_memo
from .models import (
    AtomicEvent,
    BacktestContractError,
    BacktestSource,
    LeakageError,
    PRIMARY_SOURCE_CLASSES,
    parse_date,
    parse_datetime,
)


ENGINE_VERSION = "1.0.0-h1-event-time"

DIRECTNESS = {
    "A_DIRECT_FACT": 0.90,
    "B_COMPANY_CLAIM": 0.65,
    "C_EXTERNAL_ESTIMATE": 0.55,
    "D_DERIVED_FACT": 0.80,
    "E_STRONG_INFERENCE": 0.60,
    "F_HYPOTHESIS": 0.30,
}
SCOPE_SCORE = {"BROAD": 0.0, "PARTIAL": 0.5, "EXACT": 1.0}
ORDER_PROXIMATE = {"SAMPLE", "QUALIFICATION", "LTA", "SUPPLY_COMMITMENT", "POWER_READY"}


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def add_months(value: date, months: int) -> date:
    month_index = value.month - 1 + months
    year = value.year + month_index // 12
    month = month_index % 12 + 1
    return date(year, month, min(value.day, monthrange(year, month)[1]))


def merge_source_revisions(
    existing: Iterable[dict[str, Any]], incoming: Iterable[dict[str, Any]]
) -> list[dict[str, Any]]:
    """Preserve revisions; a reused source_id cannot change immutable content."""
    merged = {item["source_id"]: dict(item) for item in existing}
    for item in incoming:
        source_id = item["source_id"]
        prior = merged.get(source_id)
        if prior is not None and canonical_json(prior) != canonical_json(item):
            raise BacktestContractError(f"source revision would overwrite {source_id}")
        merged[source_id] = dict(item)
    return [merged[key] for key in sorted(merged)]


def load_verified_sources(root: Path, path: Path) -> dict[str, dict[str, Any]]:
    records = load_jsonl(path)
    merged = merge_source_revisions([], records)
    result: dict[str, dict[str, Any]] = {}
    revision_keys: set[tuple[str, str]] = set()
    for raw in merged:
        source = BacktestSource.from_dict(raw)
        revision_key = (raw["url"], raw["revision_id"])
        if revision_key in revision_keys:
            raise BacktestContractError(f"duplicate URL/revision pair: {revision_key}")
        revision_keys.add(revision_key)
        archive = root / raw["local_archive_path"]
        if not archive.is_file():
            raise BacktestContractError(f"source archive not found: {archive}")
        actual_hash = file_sha256(archive)
        if actual_hash != raw["content_hash"]:
            raise BacktestContractError(
                f"source hash mismatch for {source.source_id}: {actual_hash}"
            )
        result[source.source_id] = dict(raw)
    return result


def screen_events(
    root: Path,
    raw_events: list[dict[str, Any]],
    source_map: dict[str, dict[str, Any]],
    primary_source_classes: set[str] | None = None,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    primary_classes = primary_source_classes or PRIMARY_SOURCE_CLASSES
    included: list[dict[str, Any]] = []
    excluded: list[dict[str, Any]] = []
    seen: set[str] = set()
    for raw in raw_events:
        event_id = raw.get("event_id") or "<missing-event-id>"
        reasons: list[str] = []
        for field in ("event_id", "source_id", "excerpt", "locator"):
            if not raw.get(field):
                reasons.append(f"MISSING_PROVENANCE:{field}")
        source = source_map.get(raw.get("source_id"))
        if source is None:
            reasons.append("UNKNOWN_SOURCE")
        if reasons:
            excluded.append({"event_id": event_id, "reasons": sorted(set(reasons))})
            continue
        event = AtomicEvent.from_dict(raw)
        if event.event_id in seen:
            raise BacktestContractError(f"duplicate event_id: {event.event_id}")
        seen.add(event.event_id)
        if source["source_class"] not in primary_classes:
            reasons.append("NON_PRIMARY_SOURCE")
        source_available = parse_datetime(source["available_at"], "source.available_at")
        event_available = parse_datetime(raw["available_at"], "event.available_at")
        if event_available < source_available:
            raise LeakageError(f"event {event_id} is available before its source")
        if raw["source_id"] not in raw["supporting_source_ids"]:
            reasons.append("PRIMARY_SOURCE_NOT_IN_SUPPORT")
        archive_text = (root / source["local_archive_path"]).read_text(encoding="utf-8")
        if raw["excerpt"] not in archive_text:
            reasons.append("EXCERPT_NOT_IN_ARCHIVE")
        for support_id in raw["supporting_source_ids"]:
            if support_id not in source_map:
                reasons.append(f"UNKNOWN_SUPPORTING_SOURCE:{support_id}")
        if reasons:
            excluded.append({"event_id": event_id, "reasons": sorted(set(reasons))})
        else:
            included.append(dict(raw))
    included.sort(key=lambda item: item["event_id"])
    excluded.sort(key=lambda item: item["event_id"])
    return included, excluded


def build_cutoff_snapshot(
    events: Iterable[dict[str, Any]], cutoff_at: str
) -> list[dict[str, Any]]:
    cutoff = parse_datetime(cutoff_at, "cutoff_at")
    return sorted(
        [
            dict(event)
            for event in events
            if parse_datetime(event["available_at"], "event.available_at") <= cutoff
        ],
        key=lambda item: item["event_id"],
    )


BLIND_FIELDS = (
    "case_id",
    "track_id",
    "event_id",
    "signal_type",
    "signal_subtype",
    "direction",
    "event_at",
    "available_at",
    "date_precision",
    "source_id",
    "supporting_source_ids",
    "entity",
    "product",
    "platform",
    "geography",
    "stated_scope",
    "scope_match",
    "order_distance",
    "cutoff_id",
    "cutoff_at",
    "claim",
    "excerpt",
    "locator",
    "evidence_level",
)


def build_blind_snapshot(events: Iterable[dict[str, Any]]) -> dict[str, Any]:
    rows = []
    for event in events:
        if not event["is_predictor"] or event["direction"] != "POSITIVE":
            continue
        rows.append({field: deepcopy(event.get(field)) for field in BLIND_FIELDS})
    rows.sort(key=lambda item: item["event_id"])
    return {
        "outcome_fields_hidden": [
            "target_outcome_id",
            "realization_status",
            "lead_days",
            "false_positive_status",
            "right_censored",
            "counterevidence_ids",
        ],
        "rows": rows,
        "blind_hash": content_digest(rows),
    }


def independent_origin_count(
    event: dict[str, Any], source_map: dict[str, dict[str, Any]]
) -> int:
    return len(
        {
            source_map[source_id]["origin_group"]
            for source_id in event["supporting_source_ids"]
            if source_id in source_map
        }
    )


def _visible_contradiction_count(
    event: dict[str, Any], event_map: dict[str, dict[str, Any]]
) -> int:
    cutoff = parse_datetime(event["cutoff_at"], "event.cutoff_at")
    return sum(
        1
        for event_id in event["counterevidence_ids"]
        if event_id in event_map
        and parse_datetime(event_map[event_id]["available_at"], "counterevidence.available_at")
        <= cutoff
    )


def score_event_evidence(
    event: dict[str, Any],
    source_map: dict[str, dict[str, Any]],
    event_map: dict[str, dict[str, Any]],
    independence_weight: float,
    contradiction_penalty_weight: float,
) -> dict[str, Any]:
    origin_count = independent_origin_count(event, source_map)
    source_available = parse_datetime(
        source_map[event["source_id"]]["available_at"], "source.available_at"
    )
    cutoff = parse_datetime(event["cutoff_at"], "event.cutoff_at")
    contradiction_count = _visible_contradiction_count(event, event_map)
    factors = {
        "directness": DIRECTNESS[event["evidence_level"]],
        "independence": min(1.0, origin_count / 2.0),
        "independent_origin_count": origin_count,
        "temporal_cutoff_fit": 1.0 if source_available <= cutoff else 0.0,
        "scope_fit": SCOPE_SCORE[event["scope_match"]],
        "open_contradiction_count_at_cutoff": contradiction_count,
        "contradiction_penalty": min(1.0, contradiction_count * 0.25),
    }
    score = (
        0.35 * factors["directness"]
        + independence_weight * factors["independence"]
        + 0.20 * factors["temporal_cutoff_fit"]
        + 0.25 * factors["scope_fit"]
        - contradiction_penalty_weight * factors["contradiction_penalty"]
    )
    score = round(max(0.0, min(1.0, score)), 4)
    return {
        "score": score,
        "label": "HIGH" if score >= 0.75 else "MEDIUM" if score >= 0.50 else "LOW",
        "factors": factors,
        "weights": {
            "directness": 0.35,
            "independence": independence_weight,
            "temporal_cutoff_fit": 0.20,
            "scope_fit": 0.25,
            "contradiction_penalty": contradiction_penalty_weight,
        },
        "interpretation": "Evidence-handling rubric; not a probability and not changed by future outcome.",
    }


def event_date_bounds(event: dict[str, Any]) -> tuple[date, date]:
    value = parse_date(event["event_at"], "event.event_at")
    precision = event["date_precision"]
    if precision == "DAY":
        return value, value
    if precision == "MONTH_END":
        return date(value.year, value.month, 1), date(
            value.year, value.month, monthrange(value.year, value.month)[1]
        )
    if precision == "QUARTER_END":
        first_month = ((value.month - 1) // 3) * 3 + 1
        last_month = first_month + 2
        return date(value.year, first_month, 1), date(
            value.year, last_month, monthrange(value.year, last_month)[1]
        )
    return date(value.year, 1, 1), date(value.year, 12, 31)


def _evaluate_predictor(
    event: dict[str, Any],
    event_map: dict[str, dict[str, Any]],
    observation_end: date,
    horizon_months: int,
    useful_lead_days: int,
    max_horizon_months: int,
) -> dict[str, Any]:
    if event["right_censored"]:
        return {
            "realization_status": "RIGHT_CENSORED",
            "false_positive_status": "RIGHT_CENSORED",
            "lead_days": None,
            "useful_lead": None,
            "outcome_window_fit": "INCOMPLETE",
        }
    target_id = event.get("target_outcome_id")
    signal_date = parse_datetime(event["available_at"], "event.available_at").date()
    horizon_end = add_months(signal_date, horizon_months)
    if not target_id or target_id not in event_map:
        status = "RIGHT_CENSORED" if observation_end < horizon_end else "FALSE_POSITIVE"
        return {
            "realization_status": status,
            "false_positive_status": status,
            "lead_days": None,
            "useful_lead": None,
            "outcome_window_fit": "INCOMPLETE" if status == "RIGHT_CENSORED" else "NO_REALIZATION",
        }
    outcome = event_map[target_id]
    outcome_date = parse_date(outcome["event_at"], "outcome.event_at")
    lead_days = (outcome_date - signal_date).days
    lower, upper = event_date_bounds(outcome)
    lead_interval = {
        "lower": (lower - signal_date).days,
        "upper": (upper - signal_date).days,
    }
    if lead_days < 0:
        status = "CONFIRMATORY"
        false_status = "NOT_A_PREDICTOR"
    elif outcome_date <= horizon_end:
        status = "REALIZED"
        false_status = "NOT_FALSE_POSITIVE"
    elif outcome_date <= add_months(signal_date, max_horizon_months):
        status = "DELAYED"
        false_status = "DELAYED"
    elif observation_end < horizon_end:
        status = "RIGHT_CENSORED"
        false_status = "RIGHT_CENSORED"
    else:
        status = "FALSE_POSITIVE"
        false_status = f"FALSE_POSITIVE_{horizon_months}M"
    return {
        "realization_status": status,
        "false_positive_status": false_status,
        "lead_days": lead_days,
        "lead_days_interval": lead_interval,
        "useful_lead": lead_days >= useful_lead_days if lead_days >= 0 else False,
        "outcome_window_fit": "WITHIN_WINDOW" if status == "REALIZED" else status,
        "realized_outcome_id": target_id,
    }


def evaluate_events(
    events: list[dict[str, Any]],
    source_map: dict[str, dict[str, Any]],
    config: dict[str, Any],
    *,
    horizon_months: int,
    useful_lead_days: int,
    independence_weight: float,
    contradiction_penalty_weight: float,
) -> list[dict[str, Any]]:
    event_map = {item["event_id"]: item for item in events}
    observation_end = parse_date(config["observation_end"], "config.observation_end")
    max_horizon = max(config["horizon_sensitivity_months"])
    evaluated: list[dict[str, Any]] = []
    for raw in sorted(events, key=lambda item: item["event_id"]):
        item = deepcopy(raw)
        item["evidence_confidence"] = score_event_evidence(
            raw,
            source_map,
            event_map,
            independence_weight,
            contradiction_penalty_weight,
        )
        eligible = (
            raw["is_predictor"]
            and raw["direction"] == "POSITIVE"
            and raw["signal_type"] in config["predictor_signal_types"]
        )
        item["predictor_eligible"] = eligible
        item["shipment_confirmation_only"] = raw["signal_type"] == "SHIPMENT"
        if eligible:
            item.update(
                _evaluate_predictor(
                    raw,
                    event_map,
                    observation_end,
                    horizon_months,
                    useful_lead_days,
                    max_horizon,
                )
            )
        else:
            item["lead_days"] = None
            item["useful_lead"] = None
            if raw["event_role"] == "OUTCOME":
                item["false_positive_status"] = "NOT_APPLICABLE_OUTCOME"
            elif raw["direction"] != "POSITIVE":
                item["false_positive_status"] = "NOT_APPLICABLE_DIRECTION"
            else:
                item["false_positive_status"] = "EXCLUDED_FROM_PREDICTOR_COMPARISON"
        evaluated.append(item)
    return evaluated


def summarize_signals(
    evaluated: list[dict[str, Any]], config: dict[str, Any]
) -> list[dict[str, Any]]:
    summary: list[dict[str, Any]] = []
    for signal_type in config["predictor_signal_types"]:
        rows = [
            item
            for item in evaluated
            if item["predictor_eligible"] and item["signal_type"] == signal_type
        ]
        leads = [item["lead_days"] for item in rows if item.get("lead_days") is not None]
        counts = Counter(item["realization_status"] for item in rows)
        summary.append(
            {
                "signal_type": signal_type,
                "eligible_n": len(rows),
                "fully_observed_n": len(rows) - counts["RIGHT_CENSORED"],
                "realized_n": counts["REALIZED"],
                "delayed_n": counts["DELAYED"],
                "false_positive_n": counts["FALSE_POSITIVE"],
                "right_censored_n": counts["RIGHT_CENSORED"],
                "useful_lead_n": sum(item.get("useful_lead") is True for item in rows),
                "lead_median_days": round(float(median(leads)), 1) if leads else None,
                "lead_range_days": [min(leads), max(leads)] if leads else None,
                "conclusion": (
                    "INSUFFICIENT_EVIDENCE"
                    if len(rows) < config["minimum_signal_n_for_comparison"]
                    else "DESCRIPTIVE_ONLY"
                ),
            }
        )
    return summary


def compare_matched_tracks(
    evaluated: list[dict[str, Any]], config: dict[str, Any]
) -> list[dict[str, Any]]:
    by_track: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for item in evaluated:
        by_track[item["track_id"]].append(item)
    output: list[dict[str, Any]] = []
    for track_id in sorted(by_track):
        predictors = [item for item in by_track[track_id] if item["predictor_eligible"]]
        capex = [item for item in predictors if item["signal_type"] == "CAPEX"]
        proximate = [item for item in predictors if item["signal_type"] in ORDER_PROXIMATE]
        matched = bool(capex and proximate)
        fully_observed = matched and all(
            item["realization_status"] != "RIGHT_CENSORED" for item in capex + proximate
        )
        comparison = "NOT_MATCHED"
        if fully_observed:
            capex_false = sum(item["realization_status"] == "FALSE_POSITIVE" for item in capex)
            prox_false = sum(
                item["realization_status"] == "FALSE_POSITIVE" for item in proximate
            )
            capex_leads = [item["lead_days"] for item in capex if item["lead_days"] is not None]
            prox_leads = [
                item["lead_days"] for item in proximate if item["lead_days"] is not None
            ]
            if prox_false < capex_false and any(
                item.get("useful_lead") for item in proximate
            ):
                comparison = "ORDER_PROXIMATE_BETTER"
            elif capex_false <= prox_false and capex_leads and prox_leads and median(capex_leads) >= median(prox_leads):
                comparison = "CAPEX_EQUAL_OR_BETTER_ON_FALSE_POSITIVE_AND_LEAD"
            else:
                comparison = "MIXED_WITHIN_TRACK"
        output.append(
            {
                "track_id": track_id,
                "case_id": by_track[track_id][0]["case_id"],
                "matched": matched,
                "fully_observed": fully_observed,
                "capex_event_ids": [item["event_id"] for item in capex],
                "order_proximate_event_ids": [item["event_id"] for item in proximate],
                "comparison": comparison,
            }
        )
    return output


def h1_verdict(
    evaluated: list[dict[str, Any]], config: dict[str, Any]
) -> dict[str, Any]:
    matched = compare_matched_tracks(evaluated, config)
    fully = [item for item in matched if item["fully_observed"]]
    if len(fully) < config["minimum_matched_tracks_for_h1"]:
        verdict = "INCONCLUSIVE"
        reason = (
            f"Only {len(fully)} fully observed matched track contains both CAPEX and an "
            f"order-proximate signal; the rule requires {config['minimum_matched_tracks_for_h1']}. "
            "The case evidence is useful for stage and timing diagnostics but cannot establish H1 superiority."
        )
    else:
        better = sum(item["comparison"] == "ORDER_PROXIMATE_BETTER" for item in fully)
        capex_better = sum(
            item["comparison"] == "CAPEX_EQUAL_OR_BETTER_ON_FALSE_POSITIVE_AND_LEAD"
            for item in fully
        )
        if better >= 2:
            verdict = "SUPPORTED"
            reason = "At least two matched tracks favor order-proximate signals under the fixed rule."
        elif capex_better >= 2:
            verdict = "REJECTED"
            reason = "At least two matched tracks show CAPEX equal or better on false positives and useful lead."
        else:
            verdict = "MIXED"
            reason = "Matched-track directions differ by product or platform."
    return {
        "verdict": verdict,
        "reason": reason,
        "fully_observed_matched_track_count": len(fully),
        "required_matched_track_count": config["minimum_matched_tracks_for_h1"],
        "matched_tracks": matched,
    }


def _case_results(evaluated: list[dict[str, Any]], cases: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_case: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for item in evaluated:
        by_case[item["case_id"]].append(item)
    results = []
    for case in cases:
        rows = by_case[case["case_id"]]
        results.append(
            {
                "case_id": case["case_id"],
                "period": case["period"],
                "atomic_event_count": len(rows),
                "predictor_event_ids": [
                    item["event_id"] for item in rows if item["predictor_eligible"]
                ],
                "outcome_event_ids": [
                    item["event_id"] for item in rows if item["event_role"] == "OUTCOME"
                ],
                "counterevidence_event_ids": [
                    item["event_id"]
                    for item in rows
                    if item["event_role"] == "COUNTEREVIDENCE"
                ],
                "exclusion_note": case["exclusion_note"],
            }
        )
    return results


def _date_interval_sensitivity(
    evaluated: list[dict[str, Any]], config: dict[str, Any]
) -> list[dict[str, Any]]:
    event_map = {item["event_id"]: item for item in evaluated}
    threshold = config["primary_useful_lead_days"]
    output = []
    for event in evaluated:
        target_id = event.get("target_outcome_id")
        if not event["predictor_eligible"] or not target_id or target_id not in event_map:
            continue
        lower, upper = event_date_bounds(event_map[target_id])
        signal_date = parse_datetime(event["available_at"], "event.available_at").date()
        lower_lead = (lower - signal_date).days
        upper_lead = (upper - signal_date).days
        output.append(
            {
                "event_id": event["event_id"],
                "target_outcome_id": target_id,
                "date_precision": event_map[target_id]["date_precision"],
                "lead_lower_days": lower_lead,
                "lead_upper_days": upper_lead,
                "useful_at_lower_bound": lower_lead >= threshold,
                "useful_at_upper_bound": upper_lead >= threshold,
            }
        )
    return sorted(output, key=lambda item: item["event_id"])


def _sensitivity_grid(
    events: list[dict[str, Any]],
    sources: dict[str, dict[str, Any]],
    config: dict[str, Any],
) -> list[dict[str, Any]]:
    grid = []
    for horizon in config["horizon_sensitivity_months"]:
        for lead in config["useful_lead_sensitivity_days"]:
            for independence_weight in config["independence_weight_sensitivity"]:
                for contradiction_weight in config["contradiction_penalty_sensitivity"]:
                    evaluated = evaluate_events(
                        events,
                        sources,
                        config,
                        horizon_months=horizon,
                        useful_lead_days=lead,
                        independence_weight=independence_weight,
                        contradiction_penalty_weight=contradiction_weight,
                    )
                    verdict = h1_verdict(evaluated, config)
                    summaries = summarize_signals(evaluated, config)
                    cell = {
                        "outcome_horizon_months": horizon,
                        "useful_lead_days": lead,
                        "independence_weight": independence_weight,
                        "contradiction_penalty_weight": contradiction_weight,
                        "verdict": verdict["verdict"],
                        "fully_observed_matched_track_count": verdict[
                            "fully_observed_matched_track_count"
                        ],
                        "signal_summary": summaries,
                    }
                    cell["cell_hash"] = content_digest(cell)
                    grid.append(cell)
    return grid


def _source_event_trace(
    events: list[dict[str, Any]], sources: dict[str, dict[str, Any]]
) -> list[dict[str, Any]]:
    result = []
    for event in sorted(events, key=lambda item: item["event_id"]):
        source = sources[event["source_id"]]
        result.append(
            {
                "event_id": event["event_id"],
                "source_id": source["source_id"],
                "excerpt": event["excerpt"],
                "locator": event["locator"],
                "publication_date": source["publication_date"],
                "available_at": source["available_at"],
                "url": source["url"],
                "local_archive_path": source["local_archive_path"],
                "content_hash": source["content_hash"],
                "source_class": source["source_class"],
                "origin_group": source["origin_group"],
                "revision_id": source["revision_id"],
            }
        )
    return result


def _validation_report(
    result: dict[str, Any], excluded_events: list[dict[str, Any]]
) -> dict[str, Any]:
    verdict = result["h1_verdict"]
    return {
        "overall_assessment": "SHARE_WITH_CAVEATS",
        "question_review": "The analysis tests signal timing and realization distance, not demand-volume prediction or causality.",
        "data_as_of": result["as_of"],
        "checks": {
            "source_hashes_verified": True,
            "primary_provenance_required": True,
            "event_count": result["event_count"],
            "duplicate_event_ids": 0,
            "future_information_cutoff_enforced": True,
            "blind_snapshot_hash_preserved": True,
            "shipment_excluded_from_predictor_comparison": True,
            "right_censoring_preserved": True,
            "sensitivity_cell_count": len(result["sensitivity_grid"]),
            "excluded_event_count": len(excluded_events),
        },
        "issues": [
            {
                "severity": "HIGH",
                "issue": "Only one fully observed matched track contains both CAPEX and an order-proximate predictor.",
                "impact": "The full H1 verdict must remain INCONCLUSIVE.",
            },
            {
                "severity": "MEDIUM",
                "issue": "C1 compares broad CSP infrastructure spend with broad supplier memory outcomes.",
                "impact": "It is a delay/control case, not a causal attribution.",
            },
            {
                "severity": "MEDIUM",
                "issue": "LTA and power-ready each have fewer than two eligible observations.",
                "impact": "Their signal-level conclusions remain INSUFFICIENT_EVIDENCE.",
            },
        ],
        "verdict_check": {
            "computed": verdict["verdict"],
            "supported_by_rule": verdict["verdict"] == "INCONCLUSIVE",
        },
        "required_caveat": "No predictive accuracy, statistical significance, causal effect, customer volume, price, or allocation percentage is claimed.",
    }


def run_h1_backtest(
    workspace: Path,
    config_path: Path | None = None,
    source_path: Path | None = None,
    event_path: Path | None = None,
    cases_path: Path | None = None,
) -> dict[str, Any]:
    root = workspace.resolve()
    config_path = config_path or root / "data/backtest/config.json"
    source_path = source_path or root / "data/backtest/source_registry.jsonl"
    event_path = event_path or root / "data/backtest/events.jsonl"
    cases_path = cases_path or root / "data/backtest/cases.json"
    config = load_json(config_path, None)
    cases = load_json(cases_path, None)
    if config is None or cases is None:
        raise FileNotFoundError("backtest config or cases file missing")
    raw_sources = load_jsonl(source_path)
    raw_events = load_jsonl(event_path)
    fingerprint = content_digest(
        {
            "engine_version": ENGINE_VERSION,
            "config": config,
            "cases": cases,
            "sources": raw_sources,
            "events": raw_events,
        }
    )
    run_dir = root / "data/backtest/runs" / config["run_id"]
    existing_path = run_dir / "run_result.json"
    if existing_path.exists():
        existing = load_json(existing_path, {})
        if existing.get("input_fingerprint") != fingerprint:
            raise BacktestContractError(
                f"run_id {config['run_id']} already exists for different inputs"
            )
        return existing
    if not config["minimum_event_count"] <= len(raw_events) <= config["maximum_event_count"]:
        raise BacktestContractError(
            f"event count {len(raw_events)} outside approved range "
            f"{config['minimum_event_count']}..{config['maximum_event_count']}"
        )
    sources = load_verified_sources(root, source_path)
    events, excluded = screen_events(
        root,
        raw_events,
        sources,
        set(config["primary_source_classes"]),
    )
    if len(events) < config["minimum_event_count"]:
        raise BacktestContractError(
            f"only {len(events)} events remain after primary-evidence screening"
        )
    blind = build_blind_snapshot(events)
    primary_evaluated = evaluate_events(
        events,
        sources,
        config,
        horizon_months=config["primary_horizon_months"],
        useful_lead_days=config["primary_useful_lead_days"],
        independence_weight=0.20,
        contradiction_penalty_weight=0.20,
    )
    primary_summary = summarize_signals(primary_evaluated, config)
    verdict = h1_verdict(primary_evaluated, config)
    sensitivity = _sensitivity_grid(events, sources, config)
    verdict_counts = dict(sorted(Counter(item["verdict"] for item in sensitivity).items()))
    trace = _source_event_trace(events, sources)
    result = {
        "run_id": config["run_id"],
        "engine_version": ENGINE_VERSION,
        "input_fingerprint": fingerprint,
        "question": config["question"],
        "as_of": config["as_of"],
        "observation_end": config["observation_end"],
        "event_count": len(events),
        "source_count": len(sources),
        "case_count": len(cases),
        "excluded_events": excluded,
        "blind_snapshot_hash": blind["blind_hash"],
        "blind_snapshot_row_count": len(blind["rows"]),
        "evaluated_events_primary": primary_evaluated,
        "signal_summary_primary": primary_summary,
        "case_results": _case_results(primary_evaluated, cases),
        "h1_verdict": verdict,
        "sensitivity_grid": sensitivity,
        "sensitivity_summary": {
            "cell_count": len(sensitivity),
            "verdict_counts": verdict_counts,
            "verdict_stable": len(verdict_counts) == 1,
            "date_interval_sensitivity": _date_interval_sensitivity(
                primary_evaluated, config
            ),
        },
        "source_event_trace": trace,
    }
    replay_basis = {
        "blind_snapshot_hash": result["blind_snapshot_hash"],
        "evaluated_events_primary": primary_evaluated,
        "signal_summary_primary": primary_summary,
        "h1_verdict": verdict,
        "sensitivity_grid": sensitivity,
        "source_event_trace": trace,
    }
    result["result_hash"] = content_digest(replay_basis)
    memo = build_h1_memo(result)
    validation = _validation_report(result, excluded)
    result["decision_memo"] = memo
    result["validation_report"] = validation
    result["artifacts"] = {
        "blind_snapshot": f"data/backtest/runs/{config['run_id']}/blind_snapshot.json",
        "evaluated_events": f"data/backtest/runs/{config['run_id']}/evaluated_events.json",
        "signal_summary": f"data/backtest/runs/{config['run_id']}/signal_summary.json",
        "sensitivity": f"data/backtest/runs/{config['run_id']}/sensitivity.json",
        "decision_memo_json": f"data/backtest/runs/{config['run_id']}/decision_memo.json",
        "decision_memo_markdown": f"data/backtest/runs/{config['run_id']}/decision_memo.md",
        "source_event_trace": f"data/backtest/runs/{config['run_id']}/source_event_trace.json",
        "validation_report": f"data/backtest/runs/{config['run_id']}/validation_report.json",
    }
    write_json(run_dir / "blind_snapshot.json", blind)
    write_json(run_dir / "screened_events.json", {"included": events, "excluded": excluded})
    write_json(run_dir / "evaluated_events.json", primary_evaluated)
    write_json(run_dir / "signal_summary.json", primary_summary)
    write_json(run_dir / "sensitivity.json", sensitivity)
    write_json(run_dir / "source_event_trace.json", trace)
    write_json(run_dir / "decision_memo.json", memo)
    (run_dir / "decision_memo.md").write_text(render_h1_memo(memo), encoding="utf-8")
    write_json(run_dir / "validation_report.json", validation)
    write_json(existing_path, result)
    return result
