from __future__ import annotations

import argparse
import csv
import hashlib
import json
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any, Iterable

from src.core.models import ContractError
from src.core.storage import content_digest, write_json
from src.measurement.corpus import FORBIDDEN_EMPIRICAL_KEYS


PACKAGE_VERSION = "H1-GATE6-REVIEW-1.0.0"
CREATED_AT = "2026-08-28T19:00:00+09:00"
WINDOWS = (6, 12, 18)

PRODUCT_SIGNAL_CLASSES = {
    "HBM_SAMPLE",
    "QUALIFICATION_STAGE",
    "DESIGN_IN",
    "ORDER_ADJACENT_SUPPLY_COMMITMENT",
}
PLATFORM_SIGNAL_CLASSES = {
    "CSP_CAPEX",
    "AI_INFRA_COMMITMENT",
    "PLATFORM_LAUNCH",
    "PLATFORM_DEPLOYMENT_STAGE",
}

# Accepted records that require a human policy or timing decision despite passing the
# deterministic shape/stage contract.
ACCEPTED_HOLD_RECOMMENDATIONS = {
    "EVT-C04-20241231-H200-GA-RETROSPECTIVE": (
        "The later source confirms year-end GA only retrospectively; exact occurrence timing "
        "should not be made more precise than the source.",
        "RETROSPECTIVE_TIMING_AND_ARTIFICIAL_PRECISION",
        "Choose retrospective corroboration, bounded timing, or exclusion from exact-date use.",
    ),
    "EVT-P05-20260630-O1": (
        "The source says mass shipments began in Q2 but does not state the first shipment day.",
        "O1_FIRST_DATE_NOT_DIRECTLY_OBSERVED",
        "Apply the human-selected O1 timing policy before admitting this as a timed O1.",
    ),
    "EVT-P06-20260212-O1": (
        "The source confirms current commercial shipment but does not establish the first "
        "shipment date.",
        "O1_CONFIRMATION_TIME_NOT_FIRST_OPERATIONAL_DATE",
        "Apply the human-selected O1 timing policy and preserve confirmation versus occurrence.",
    ),
    "EVT-P07-20260316-O1": (
        "The source bounds volume shipment to Q1; a filing timestamp is not the operational "
        "shipment-start timestamp.",
        "O1_INTERVAL_COLLAPSED_TO_TIMESTAMP",
        "Apply the human-selected O1 timing policy before any timed use.",
    ),
}

# These broad CAPEX observations are real context, but their historical availability is after
# the named Track's operational state. Keeping them as a Track-level empirical signal would
# invert the intended information sequence. The Source remains in the corpus and CAPEX audit.
ACCEPTED_EXCLUDE_RECOMMENDATIONS = {
    "EVT-C01-20240730-CAPEX": (
        "The company-level CAPEX disclosure became public after this Track's H100 GA event.",
        "POST_OUTCOME_CONTEXT_AND_SCOPE_MISMATCH",
        "Confirm exclusion from this Track's empirical sequence while retaining the Source as "
        "company context.",
    ),
    "EVT-C03-20250204-CAPEX": (
        "The company-level CAPEX disclosure post-dates the retrospective H100 GA period and "
        "cannot be a pre-P1 signal for this Track.",
        "POST_OUTCOME_CONTEXT_AND_SCOPE_MISMATCH",
        "Confirm exclusion from this Track's empirical sequence; do not delete the Source.",
    ),
    "EVT-C04-20250204-CAPEX": (
        "The company-level CAPEX disclosure became public after the retrospective year-end "
        "H200 GA state.",
        "POST_OUTCOME_CONTEXT_AND_SCOPE_MISMATCH",
        "Confirm exclusion from this Track's empirical sequence; retain as broad context only.",
    ),
}

HOLD_EXCLUDE_RECOMMENDATIONS = {
    "EVT-C14-20250929-GB200-INSTALLED-HOLD",
    "EVT-P01-20220608-QUAL-EVAL-HOLD",
    "EVT-P02-20230821-PRODUCTION-PLAN",
    "EVT-P04-20240226-PRODUCTION",
    "EVT-P05-20250319-PRODUCTION-PREP-HOLD",
    "EVT-P10-20260624-DEVELOPMENT-AS-SAMPLE-HOLD",
    "EVT-P10-20260624-PRODUCTION-PLAN-HOLD",
}

HOLD_RESOLUTION_DETAILS: dict[str, dict[str, Any]] = {
    "EVT-C03-20240410-H100-RETRO-GA-HOLD": {
        "semantic_issue": "A later retrospective GA month conflicts with the contemporaneous forward-looking statement.",
        "historical_time_issue": "The 2024 publication cannot be backdated into the 2023 analyst information set.",
        "resolving_primary_source": "A contemporaneous Google Cloud GA release, dated service changelog, or immutable official availability record.",
        "permanent_hold_for_this_gate": True,
        "exclusion_effect": "Removes an exact H100 GA outcome date; the earlier planned state and later retrospective corroboration remain visible.",
        "human_options": ["EXCLUDE_EXACT_DATE", "RETAIN_RETROSPECTIVE_CORROBORATION", "RETAIN_BOUNDED_INTERVAL_IF_APPROVED"],
    },
    "EVT-C14-20250929-GB200-INSTALLED-HOLD": {
        "semantic_issue": "A rack image caption establishes configuration, not an operating workload or customer-available service.",
        "historical_time_issue": "No timing leakage was found; the unsupported operational promotion is the issue.",
        "resolving_primary_source": "A Meta primary source explicitly stating current operational use of the Catalina GB200 rack.",
        "permanent_hold_for_this_gate": True,
        "exclusion_effect": "Prevents installed hardware from being counted as operational realization; broad Meta CAPEX context remains.",
        "human_options": ["EXCLUDE", "RETAIN_AS_NON_OPERATIONAL_CONTEXT"],
    },
    "EVT-P01-20220608-QUAL-EVAL-HOLD": {
        "semantic_issue": "Performance evaluation is not explicit qualification or certification completion.",
        "historical_time_issue": "No timing leakage was found.",
        "resolving_primary_source": "A supplier or counterparty primary source explicitly confirming qualification completion.",
        "permanent_hold_for_this_gate": True,
        "exclusion_effect": "Prevents qualification-stage inflation; the production-context fact remains.",
        "human_options": ["EXCLUDE", "RETAIN_AS_EVALUATION_CONTEXT"],
    },
    "EVT-P02-20230821-PRODUCTION-PLAN": {
        "semantic_issue": "A production plan is not a customer order or supply commitment.",
        "historical_time_issue": "The future plan was not mislabeled as an occurred shipment, but its proposed class is invalid.",
        "resolving_primary_source": "A signed commitment, explicit allocation, or direct supply-plan source at compatible product scope.",
        "permanent_hold_for_this_gate": True,
        "exclusion_effect": "Does not remove the production-plan information because the additive R2 context Event preserves it correctly.",
        "human_options": ["EXCLUDE_SUPERSEDED_CLASSIFICATION"],
    },
    "EVT-P02-20240319-FUTURE-CUSTOMER-SUPPLY": {
        "semantic_issue": "Future customer supply cannot establish current O1 realization.",
        "historical_time_issue": "The source was public before the planned supply date and cannot be used as proof that supply occurred.",
        "resolving_primary_source": "A later official source confirming that customer supply actually began and, if possible, its timing.",
        "permanent_hold_for_this_gate": True,
        "exclusion_effect": "Removes an unsupported O1; sample and production-context history remain.",
        "human_options": ["EXCLUDE", "RETAIN_AS_FUTURE_PLAN_CONTEXT"],
    },
    "EVT-P03-20241231-O1-START-HOLD": {
        "semantic_issue": "Expanded current supply does not identify the first customer-supply start date.",
        "historical_time_issue": "Quarter-level activity was collapsed to a month-end candidate date.",
        "resolving_primary_source": "A contemporaneous Samsung primary source stating when customer supply first began.",
        "permanent_hold_for_this_gate": True,
        "exclusion_effect": "Prevents a fabricated O1 start date; accepted current-supply corroboration remains.",
        "human_options": ["EXCLUDE_EXACT_DATE", "APPLY_SELECTED_O1_POLICY"],
    },
    "EVT-P04-20240226-H200-DESIGN-IN": {
        "semantic_issue": "The disclosure describes planned H200 integration, not a completed platform shipment or named-CSP supply relationship.",
        "historical_time_issue": "The planned future integration must remain a plan at the historical cutoff.",
        "resolving_primary_source": "A Micron or NVIDIA primary source confirming actual selection/integration at H200 scope; a CSP-specific bridge needs separate direct evidence.",
        "permanent_hold_for_this_gate": True,
        "exclusion_effect": "Removes the only design-in candidate but prevents planned integration from becoming completed commercial selection.",
        "human_options": ["EXCLUDE", "RETAIN_AS_PLANNED_INTEGRATION_CONTEXT"],
    },
    "EVT-P04-20240226-PRODUCTION": {
        "semantic_issue": "Production start is supply readiness, not a contractual commitment.",
        "historical_time_issue": "No timing leakage was found; classification inflation is the issue.",
        "resolving_primary_source": "A separate direct commercial-commitment source.",
        "permanent_hold_for_this_gate": True,
        "exclusion_effect": "Does not remove the production fact because the additive R2 context Event preserves it.",
        "human_options": ["EXCLUDE_SUPERSEDED_CLASSIFICATION"],
    },
    "EVT-P04-20250318-O1-START-HOLD": {
        "semantic_issue": "Current shipping confirms a current state but not the first commercial-shipment date or named customer scope.",
        "historical_time_issue": "Publication time is an information-confirmation time, not necessarily shipment occurrence time.",
        "resolving_primary_source": "An earlier official shipment-start source or a human-approved O1 timing policy.",
        "permanent_hold_for_this_gate": True,
        "exclusion_effect": "Prevents a fabricated first date; accepted current-shipping corroboration remains.",
        "human_options": ["EXCLUDE_EXACT_DATE", "APPLY_SELECTED_O1_POLICY"],
    },
    "EVT-P05-20250319-PRODUCTION-PREP-HOLD": {
        "semantic_issue": "A target to complete production preparation is not observed production readiness.",
        "historical_time_issue": "The target is forward-looking and cannot be promoted at publication.",
        "resolving_primary_source": "A later official source confirming that preparation or production actually occurred.",
        "permanent_hold_for_this_gate": True,
        "exclusion_effect": "Prevents a plan from becoming supply-readiness fact; sample and qualification-plan Events remain.",
        "human_options": ["EXCLUDE", "RETAIN_AS_FORWARD_PLAN_CONTEXT"],
    },
    "EVT-P10-20260624-DEVELOPMENT-AS-SAMPLE-HOLD": {
        "semantic_issue": "Development activity does not establish delivery of samples or sampling.",
        "historical_time_issue": "No future sample event may be backfilled from the development statement.",
        "resolving_primary_source": "A Micron primary source explicitly reporting sample delivery or sampling.",
        "permanent_hold_for_this_gate": True,
        "exclusion_effect": "Leaves P10 without an admissible H1-P signal, accurately making the Track descriptive/unavailable for comparison.",
        "human_options": ["EXCLUDE", "RETAIN_AS_DEVELOPMENT_CONTEXT_OUTSIDE_H1_SIGNAL_SET"],
    },
    "EVT-P10-20260624-PRODUCTION-PLAN-HOLD": {
        "semantic_issue": "An expected calendar year does not establish a current production stage or occurred production plan under the frozen lexical contract.",
        "historical_time_issue": "The future year cannot be treated as current readiness or O1.",
        "resolving_primary_source": "A primary source with explicit production-planned wording and bounded timing, or a later occurred production disclosure.",
        "permanent_hold_for_this_gate": True,
        "exclusion_effect": "Removes no occurred stage and prevents future timing from becoming current production.",
        "human_options": ["EXCLUDE", "RETAIN_AS_FORWARD_DEVELOPMENT_CONTEXT_OUTSIDE_EMPIRICAL_SET"],
    },
}


def _load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _walk_keys(value: Any) -> Iterable[str]:
    if isinstance(value, dict):
        for key, nested in value.items():
            yield key
            yield from _walk_keys(nested)
    elif isinstance(value, list):
        for nested in value:
            yield from _walk_keys(nested)


def _with_hash(payload: dict[str, Any]) -> dict[str, Any]:
    output = dict(payload)
    output["content_hash"] = content_digest(payload)
    return output


def _file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def _add_months(value: datetime, months: int) -> datetime:
    month_index = value.month - 1 + months
    year = value.year + month_index // 12
    month = month_index % 12 + 1
    month_lengths = (31, 29 if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0) else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)
    day = min(value.day, month_lengths[month - 1])
    return value.replace(year=year, month=month, day=day)


def _csv_value(value: Any) -> Any:
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    if value is None:
        return ""
    return value


def _write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({name: _csv_value(row.get(name)) for name in fieldnames})


def _default_event_risk(event: dict[str, Any]) -> tuple[str, str, str]:
    signal_class = event["signal_class"]
    if signal_class == "CSP_CAPEX":
        return (
            "Directly supports broad company-period investment context only; it does not allocate spending to the named platform.",
            "BROAD_SCOPE_AND_REPEATED_CONTEXT",
            "Confirm broad-context use, origin grouping, event precision, and prohibition on repeated denominator counting.",
        )
    if signal_class == "PRODUCTION_STAGE_CONTEXT":
        return (
            "Directly supports the stated supply-readiness stage as context only.",
            "PRODUCTION_COULD_BE_MISREAD_AS_CUSTOMER_ACCEPTANCE",
            "Confirm context-only admission and prohibit use as qualification, commitment, O1, or demand volume.",
        )
    if signal_class == "O2_OPERATIONAL_CORROBORATION":
        return (
            "Directly supports a current broader-scope supply/shipping statement as corroboration, not first O1 timing.",
            "CORROBORATION_COULD_BE_PROMOTED_TO_O1",
            "Confirm corroboration-only role and compatible product scope.",
        )
    if signal_class == "P1_PLATFORM_OPERATIONAL_REALIZATION":
        return (
            "Directly supports the named platform state at the stated availability subtype.",
            "AVAILABILITY_DOES_NOT_ESTABLISH_UTILIZATION_OR_HBM_SUPPLIER",
            "Confirm subtype, scope, and event precision without inferring utilization or memory demand.",
        )
    if signal_class == "PLATFORM_DEPLOYMENT_STAGE":
        return (
            "Directly supports the stated planned, preview, or deployment stage.",
            "PLANNED_PREVIEW_AND_GA_COULD_BE_COLLAPSED",
            "Confirm exact stage and named-platform scope.",
        )
    if signal_class == "PLATFORM_LAUNCH":
        return (
            "Directly supports a named-platform plan/announcement, not operational availability.",
            "PLAN_COULD_BE_MISREAD_AS_REALIZATION",
            "Confirm plan-only role and later-state separation.",
        )
    if signal_class == "HBM_SAMPLE":
        return (
            "Directly supports sample delivery or sampling at product scope.",
            "SAMPLE_COULD_BE_MISREAD_AS_QUALIFICATION_OR_ORDER",
            "Confirm sample wording and prohibit qualification, volume, price, or share inference.",
        )
    if signal_class == "QUALIFICATION_STAGE":
        return (
            "Directly supports only the stated planned, underway, or final-stage qualification state.",
            "QUALIFICATION_SUBSTAGE_COULD_BE_PROMOTED_TO_COMPLETE",
            "Confirm the literal substage and prohibit order/volume inference.",
        )
    if signal_class == "AI_INFRA_COMMITMENT":
        return (
            "Directly supports a broad infrastructure-capacity commitment, not named-platform deployment.",
            "COMPANY_CAPACITY_SCOPE_COULD_BE_ALLOCATED_TO_ONE_PLATFORM",
            "Confirm context scope and same-origin treatment with the paired CAPEX event.",
        )
    return (
        "The official excerpt directly supports the proposed atomic state at its stated scope.",
        "DISCLOSURE_SCOPE_OR_STAGE_MAY_BE_OVERGENERALIZED",
        "Confirm stage, scope, origin group, and event precision.",
    )


def _event_recommendation(record: dict[str, Any]) -> tuple[str, str, str, str]:
    event = record["event"]
    event_id = event["event_id"]
    if record["ingestion_status"] == "HOLD":
        detail = HOLD_RESOLUTION_DETAILS[event_id]
        if event_id in HOLD_EXCLUDE_RECOMMENDATIONS:
            return (
                "RECOMMEND_EXCLUDE",
                detail["semantic_issue"],
                "DETERMINISTIC_OR_SEMANTIC_STAGE_INFLATION",
                "Choose exclusion or a strictly contextual retention; do not promote the proposed empirical class.",
            )
        return (
            "RECOMMEND_HOLD",
            detail["semantic_issue"],
            "UNRESOLVED_SEMANTIC_OR_TIMING_POLICY",
            "Select a documented human option or retain HOLD for this Gate 6.",
        )
    if event_id in ACCEPTED_HOLD_RECOMMENDATIONS:
        reason, risk, judgment = ACCEPTED_HOLD_RECOMMENDATIONS[event_id]
        return "RECOMMEND_HOLD", reason, risk, judgment
    if event_id in ACCEPTED_EXCLUDE_RECOMMENDATIONS:
        reason, risk, judgment = ACCEPTED_EXCLUDE_RECOMMENDATIONS[event_id]
        return "RECOMMEND_EXCLUDE", reason, risk, judgment
    reason, risk, judgment = _default_event_risk(event)
    return "RECOMMEND_INCLUDE", reason, risk, judgment


class Gate6ReviewBuilder:
    def __init__(self, workspace: Path):
        self.workspace = workspace
        self.corpus_dir = workspace / "data/h1/corpus"
        self.output_dir = workspace / "data/h1/gate6_review"
        self.review_doc = workspace / "docs/reviews/h1_gate6_corpus_readiness.md"

    def build(self) -> dict[str, Any]:
        corpus_manifest = _load(self.corpus_dir / "build_manifest.json")
        if corpus_manifest["content_hash"] != "F4A6817C2D6BD76C723E3D03DA5A24EABCA854A0CBD42902503F9B6ECFD38037":
            raise ContractError("Gate 6 review must start from the approved 467c5f8 corpus manifest")
        if corpus_manifest["gate6_frozen"] or corpus_manifest["empirical_h1_calculated"]:
            raise ContractError("review package cannot be built from a frozen or analyzed H1 corpus")

        events_payload = _load(self.corpus_dir / "events.json")
        sources_payload = _load(self.corpus_dir / "source_registry.json")
        tracks_payload = _load(self.workspace / "data/h1/registry/candidate_tracks.json")
        collection_payload = _load(self.corpus_dir / "track_collection_status.json")
        coverage_payload = _load(self.corpus_dir / "coverage_report.json")
        validation_payload = _load(self.corpus_dir / "validation_results.json")
        adversarial_payload = _load(self.corpus_dir / "adversarial_verification.json")

        events = events_payload["records"]
        if len(events) != 75:
            raise ContractError("Gate 6 review contract requires exactly 75 corpus Events")
        sources = {row["source_id"]: row for row in sources_payload["sources"]}
        tracks = {row["track_id"]: row for row in tracks_payload["tracks"]}
        collection = {row["track_id"]: row for row in collection_payload["records"]}
        coverage = {row["track_id"]: row for row in coverage_payload["tracks"]}
        validation = {row["event_id"]: row for row in validation_payload["results"]}
        adversarial = {row["track_id"]: row for row in adversarial_payload["records"]}

        event_matrix = self._build_event_matrix(
            events, sources, tracks, collection, validation, adversarial
        )
        hold_sheet = self._build_hold_sheet(event_matrix, validation)
        censoring = self._build_censoring(event_matrix, tracks, corpus_manifest["created_at"])
        track_readiness = self._build_track_readiness(
            event_matrix, tracks, collection, coverage, censoring
        )
        h1_p_observability = self._build_h1_p_observability(event_matrix)
        h1_c_observability = self._build_h1_c_observability(event_matrix)
        negative_audit = self._build_negative_audit(collection, sources)
        bias_register = self._build_bias_register()
        capex_audit = self._build_capex_audit(event_matrix, tracks)
        o1_options = self._build_o1_options(event_matrix)
        authorization = self._build_authorization(
            h1_p_observability, h1_c_observability, negative_audit
        )
        checklist = self._build_human_checklist(event_matrix, hold_sheet, sources)
        candidate_facts = self._build_candidate_capability_facts()

        artifacts: list[tuple[str, dict[str, Any], list[str] | None]] = [
            ("event_review_matrix", event_matrix, list(event_matrix["records"][0])),
            ("hold_resolution_sheet", hold_sheet, list(hold_sheet["records"][0])),
            ("track_readiness_matrix", track_readiness, list(track_readiness["records"][0])),
            ("h1_p_observability_matrix", h1_p_observability, None),
            ("h1_c_observability_matrix", h1_c_observability, None),
            ("negative_evidence_sufficiency", negative_audit, None),
            ("disclosure_bias_register", bias_register, list(bias_register["records"][0])),
            ("censoring_readiness_matrix", censoring, list(censoring["records"][0])),
            ("capex_independence_reuse_audit", capex_audit, list(capex_audit["records"][0])),
            ("o1_timing_policy_options", o1_options, None),
            ("analysis_authorization_proposal", authorization, None),
            ("human_decision_checklist", checklist, None),
            ("candidate_capability_facts", candidate_facts, None),
        ]

        self.output_dir.mkdir(parents=True, exist_ok=True)
        artifact_paths: list[Path] = []
        for name, payload, csv_fields in artifacts:
            self._assert_no_empirical_output(payload)
            json_path = self.output_dir / f"{name}.json"
            write_json(json_path, payload)
            artifact_paths.append(json_path)
            if csv_fields:
                csv_path = self.output_dir / f"{name}.csv"
                _write_csv(csv_path, payload["records"], csv_fields)
                artifact_paths.append(csv_path)

        markdown = self._render_markdown(
            event_matrix,
            hold_sheet,
            h1_p_observability,
            h1_c_observability,
            negative_audit,
            censoring,
            capex_audit,
            o1_options,
            authorization,
        )
        self.review_doc.parent.mkdir(parents=True, exist_ok=True)
        self.review_doc.write_text(markdown, encoding="utf-8")
        artifact_paths.append(self.review_doc)

        manifest_basis = {
            "manifest_version": PACKAGE_VERSION,
            "created_at": CREATED_AT,
            "baseline_commit": "467c5f8",
            "baseline_corpus_manifest_hash": corpus_manifest["content_hash"],
            "baseline_dataset_hash": corpus_manifest["dataset_content_hash"],
            "baseline_source_registry_hash": corpus_manifest["source_registry_content_hash"],
            "corpus_cutoff_at": corpus_manifest["created_at"],
            "file_hashes": {
                path.relative_to(self.workspace).as_posix(): _file_hash(path)
                for path in sorted(artifact_paths)
            },
            "counts": {
                "events_reviewed": len(event_matrix["records"]),
                "raw_holds_reviewed": len(hold_sheet["records"]),
                "tracks_reviewed": len(track_readiness["records"]),
                "recommendations": event_matrix["recommendation_counts"],
                "capex_source_origins": len(capex_audit["records"]),
                "censoring_track_window_rows": len(censoring["records"]),
            },
            "human_decisions_selected": False,
            "gate6_frozen": False,
            "empirical_h1_calculated": False,
        }
        self._assert_no_empirical_output(manifest_basis)
        manifest = _with_hash(manifest_basis)
        write_json(self.output_dir / "build_manifest.json", manifest)
        return manifest

    @staticmethod
    def _assert_no_empirical_output(payload: dict[str, Any]) -> None:
        forbidden = set(_walk_keys(payload)) & FORBIDDEN_EMPIRICAL_KEYS
        if forbidden:
            raise ContractError(
                "Gate 6 review cannot contain empirical H1 result fields: "
                + ", ".join(sorted(forbidden))
            )

    def _build_event_matrix(
        self,
        records: list[dict[str, Any]],
        sources: dict[str, dict[str, Any]],
        tracks: dict[str, dict[str, Any]],
        collection: dict[str, dict[str, Any]],
        validation: dict[str, dict[str, Any]],
        adversarial: dict[str, dict[str, Any]],
    ) -> dict[str, Any]:
        rows: list[dict[str, Any]] = []
        for record in sorted(records, key=lambda item: item["event"]["event_id"]):
            event = record["event"]
            source = sources[event["source_id"]]
            track = tracks[event["track_id"]]
            result = validation[event["event_id"]]
            verifier = adversarial[event["track_id"]]
            linked_hold = event["event_id"] in verifier["hold_event_ids"]
            recommendation, reason, risk, judgment = _event_recommendation(record)
            if event["excerpt"] != source["excerpt"] or event["locator"] != source["locator"]:
                raise ContractError(f"Event-to-Source trace mismatch: {event['event_id']}")
            rows.append(
                {
                    "event_id": event["event_id"],
                    "track_id": event["track_id"],
                    "track_type": track["track_type"],
                    "source_id": event["source_id"],
                    "source_title": source["title"],
                    "publisher": source["publisher"],
                    "source_url": source["url"],
                    "source_content_hash": source["content_hash"],
                    "direct_excerpt": event["excerpt"],
                    "locator": event["locator"],
                    "data_role": event["data_role"],
                    "signal_class": event["signal_class"],
                    "signal_subtype": event["signal_subtype"],
                    "transmission_layer": event["transmission_layer"],
                    "event_at": event["event_at"],
                    "published_at": event["published_at"],
                    "available_at": event["available_at"],
                    "event_date_precision": event.get("event_date_precision") or event["date_precision"],
                    "scope_type": event["scope_type"],
                    "scope_value": event["scope_value"],
                    "origin_group": event["origin_group"],
                    "evidence_level": event["evidence_level"],
                    "ingestion_status": record["ingestion_status"],
                    "current_review_status": event["review_status"],
                    "deterministic_validation_result": result["deterministic_result"],
                    "deterministic_validation_reason": result["deterministic_reason"],
                    "adversarial_verifier_result": (
                        "EVENT_HOLD_LINKED" if linked_hold else (
                            "PASS_EVENT_TRACK_HAS_OTHER_HOLD"
                            if verifier["verdict"] == "PASS_WITH_HOLD"
                            else "PASS"
                        )
                    ),
                    "ambiguity": record["ambiguity"],
                    "missingness_relevant_to_interpretation": collection[event["track_id"]]["missingness"],
                    "codex_recommendation": recommendation,
                    "recommendation_reason": reason,
                    "main_risk": risk,
                    "required_human_judgment": judgment,
                }
            )
        counts = dict(sorted(Counter(row["codex_recommendation"] for row in rows).items()))
        accepted_noninclude = Counter(
            row["codex_recommendation"]
            for row in rows
            if row["ingestion_status"] == "ACCEPTED"
            and row["codex_recommendation"] != "RECOMMEND_INCLUDE"
        )
        return _with_hash(
            {
                "review_matrix_version": PACKAGE_VERSION,
                "created_at": CREATED_AT,
                "advisory_only": True,
                "review_status_mutated": False,
                "recommendation_counts": counts,
                "accepted_candidates_not_defaulted_to_include": dict(sorted(accepted_noninclude.items())),
                "records": rows,
            }
        )

    def _build_hold_sheet(
        self,
        event_matrix: dict[str, Any],
        validation: dict[str, dict[str, Any]],
    ) -> dict[str, Any]:
        by_id = {row["event_id"]: row for row in event_matrix["records"]}
        rows: list[dict[str, Any]] = []
        for event_id in sorted(HOLD_RESOLUTION_DETAILS):
            matrix = by_id[event_id]
            detail = HOLD_RESOLUTION_DETAILS[event_id]
            rows.append(
                {
                    "event_id": event_id,
                    "track_id": matrix["track_id"],
                    "source_id": matrix["source_id"],
                    "direct_excerpt": matrix["direct_excerpt"],
                    "locator": matrix["locator"],
                    "exact_ambiguity": matrix["ambiguity"],
                    "deterministic_result": validation[event_id]["deterministic_result"],
                    "deterministic_reason": validation[event_id]["deterministic_reason"],
                    "semantic_issue": detail["semantic_issue"],
                    "historical_time_issue": detail["historical_time_issue"],
                    "resolving_primary_source": detail["resolving_primary_source"],
                    "permanent_hold_for_this_gate": detail["permanent_hold_for_this_gate"],
                    "exclusion_effect": detail["exclusion_effect"],
                    "human_options": detail["human_options"],
                    "codex_recommendation": matrix["codex_recommendation"],
                    "human_resolution": None,
                }
            )
        if len(rows) != 12:
            raise ContractError("HOLD Resolution Sheet must contain exactly 12 current HOLD Events")
        return _with_hash(
            {
                "hold_sheet_version": PACKAGE_VERSION,
                "created_at": CREATED_AT,
                "unresolved_raw_hold_count": 12,
                "human_resolutions_selected": 0,
                "records": rows,
            }
        )

    def _build_censoring(
        self,
        event_matrix: dict[str, Any],
        tracks: dict[str, dict[str, Any]],
        corpus_cutoff_at: str,
    ) -> dict[str, Any]:
        cutoff = datetime.fromisoformat(corpus_cutoff_at)
        included_signals: dict[str, list[dict[str, Any]]] = defaultdict(list)
        for row in event_matrix["records"]:
            allowed = PRODUCT_SIGNAL_CLASSES if row["track_type"] == "PRODUCT_COMMERCIALIZATION_TRACK" else PLATFORM_SIGNAL_CLASSES
            if (
                row["codex_recommendation"] == "RECOMMEND_INCLUDE"
                and row["data_role"] == "SIGNAL"
                and row["signal_class"] in allowed
            ):
                included_signals[row["track_id"]].append(row)

        rows: list[dict[str, Any]] = []
        for track_id in sorted(tracks):
            track = tracks[track_id]
            anchors = sorted(included_signals.get(track_id, []), key=lambda item: item["event_id"])
            for months in WINDOWS:
                mature: list[str] = []
                censored: list[str] = []
                window_ends: dict[str, str] = {}
                for event in anchors:
                    available = datetime.fromisoformat(event["available_at"])
                    end = _add_months(available, months)
                    window_ends[event["event_id"]] = end.isoformat()
                    (censored if cutoff < end else mature).append(event["event_id"])
                rows.append(
                    {
                        "track_id": track_id,
                        "track_type": track["track_type"],
                        "observation_window_months": months,
                        "corpus_cutoff_at": corpus_cutoff_at,
                        "analysis_anchor_event_ids": [row["event_id"] for row in anchors],
                        "window_end_by_event_id": window_ends,
                        "fully_observed_event_ids": mature,
                        "right_censored_event_ids": censored,
                        "fully_observed": bool(anchors) and not censored,
                        "right_censored": bool(censored),
                        "left_truncated": bool(track["left_truncated"]),
                        "usable_for_failure_no_realization_denominator": bool(mature),
                        "denominator_eligible_event_ids": mature,
                        "usable_only_descriptively": not bool(mature),
                        "readiness_note": (
                            "Readiness is calculated from advisory-INCLUDE Signal availability only; it does not inspect or label outcomes."
                        ),
                    }
                )
        summary: dict[str, dict[str, int]] = {}
        for track_type in ("PRODUCT_COMMERCIALIZATION_TRACK", "CUSTOMER_PLATFORM_REALIZATION_TRACK"):
            for months in WINDOWS:
                subset = [row for row in rows if row["track_type"] == track_type and row["observation_window_months"] == months]
                summary[f"{track_type}:{months}M"] = {
                    "tracks": len(subset),
                    "tracks_all_anchor_events_fully_observed": sum(row["fully_observed"] for row in subset),
                    "tracks_with_any_right_censoring": sum(row["right_censored"] for row in subset),
                    "tracks_with_any_denominator_eligible_signal": sum(row["usable_for_failure_no_realization_denominator"] for row in subset),
                    "tracks_descriptive_only": sum(row["usable_only_descriptively"] for row in subset),
                }
        return _with_hash(
            {
                "censoring_readiness_version": PACKAGE_VERSION,
                "created_at": CREATED_AT,
                "not_an_h1_result": True,
                "calculation_basis": "corpus cutoff versus advisory-INCLUDE Signal available_at plus frozen 6/12/18-month windows",
                "summary": summary,
                "records": rows,
            }
        )

    def _build_track_readiness(
        self,
        event_matrix: dict[str, Any],
        tracks: dict[str, dict[str, Any]],
        collection: dict[str, dict[str, Any]],
        coverage: dict[str, dict[str, Any]],
        censoring: dict[str, Any],
    ) -> dict[str, Any]:
        by_track: dict[str, list[dict[str, Any]]] = defaultdict(list)
        for row in event_matrix["records"]:
            by_track[row["track_id"]].append(row)
        censor_by_track: dict[str, dict[str, dict[str, Any]]] = defaultdict(dict)
        for row in censoring["records"]:
            censor_by_track[row["track_id"]][f"{row['observation_window_months']}M"] = {
                "fully_observed": row["fully_observed"],
                "right_censored": row["right_censored"],
                "usable_for_failure_no_realization_denominator": row["usable_for_failure_no_realization_denominator"],
                "usable_only_descriptively": row["usable_only_descriptively"],
            }

        rows: list[dict[str, Any]] = []
        for track_id in sorted(tracks):
            track = tracks[track_id]
            events = by_track[track_id]
            rec_counts = Counter(row["codex_recommendation"] for row in events)
            include_signals = [row for row in events if row["codex_recommendation"] == "RECOMMEND_INCLUDE" and row["data_role"] == "SIGNAL"]
            include_outcomes = [row for row in events if row["codex_recommendation"] == "RECOMMEND_INCLUDE" and row["data_role"] == "OUTCOME"]
            if not include_signals:
                proposed_use = "DESCRIPTIVE_ONLY_NO_ADMISSIBLE_SIGNAL"
            elif not include_outcomes:
                proposed_use = "SIGNAL_TIMELINE_ONLY_NO_ADMITTED_OUTCOME"
            elif rec_counts["RECOMMEND_HOLD"] or rec_counts["RECOMMEND_EXCLUDE"]:
                proposed_use = "PARTIAL_PENDING_HUMAN_EVENT_DECISIONS"
            else:
                proposed_use = "EVENT_ADMISSION_REVIEW_READY"
            rows.append(
                {
                    "track_id": track_id,
                    "track_type": track["track_type"],
                    "entity": track["entity"],
                    "product": track["product"],
                    "platform": track["platform"],
                    "generation": track["generation"],
                    "left_truncated": track["left_truncated"],
                    "registry_right_censoring_risk": track["right_censoring_risk"],
                    "collection_status": collection[track_id]["collection_status"],
                    "negative_search_result": collection[track_id]["negative_search_result"],
                    "event_count": len(events),
                    "ingestion_counts": dict(sorted(Counter(row["ingestion_status"] for row in events).items())),
                    "recommendation_counts": dict(sorted(rec_counts.items())),
                    "recommended_include_signal_classes": sorted({row["signal_class"] for row in include_signals}),
                    "recommended_include_outcome_classes": sorted({row["signal_class"] for row in include_outcomes}),
                    "independent_origin_groups_in_corpus": sorted({row["origin_group"] for row in events}),
                    "missingness": collection[track_id]["missingness"],
                    "coverage_before_human_admission": coverage[track_id]["coverage"],
                    "window_readiness": censor_by_track[track_id],
                    "codex_proposed_use": proposed_use,
                    "main_limitation": track["known_scope_limitation"],
                    "human_track_admission_decision": None,
                }
            )
        return _with_hash(
            {
                "track_readiness_version": PACKAGE_VERSION,
                "created_at": CREATED_AT,
                "human_track_decisions_selected": 0,
                "records": rows,
            }
        )

    @staticmethod
    def _tracks_for(
        rows: list[dict[str, Any]],
        signal_class: str,
        recommendation: str = "RECOMMEND_INCLUDE",
        subtype: str | None = None,
    ) -> set[str]:
        return {
            row["track_id"]
            for row in rows
            if row["signal_class"] == signal_class
            and row["codex_recommendation"] == recommendation
            and (subtype is None or row["signal_subtype"] == subtype)
        }

    def _build_h1_p_observability(self, event_matrix: dict[str, Any]) -> dict[str, Any]:
        rows = [row for row in event_matrix["records"] if row["track_type"] == "PRODUCT_COMMERCIALIZATION_TRACK"]
        stage_specs = [
            ("SAMPLE", "HBM_SAMPLE", "EMPIRICALLY_OBSERVABLE", "Product existence and customer sampling/evaluation entry are directly visible across most Tracks."),
            ("QUALIFICATION", "QUALIFICATION_STAGE", "SPARSE_BUT_USABLE", "Three Tracks expose planned, underway, or final-stage qualification, but no complete cross-Track ladder exists."),
            ("DESIGN_IN", "DESIGN_IN", "NOT_IDENTIFIABLE_WITH_PUBLIC_CORPUS", "No advisory-INCLUDE Event exists; the sole candidate is planned H200 integration on HOLD."),
            ("COMMERCIAL_COMMITMENT", "ORDER_ADJACENT_SUPPLY_COMMITMENT", "NOT_IDENTIFIABLE_WITH_PUBLIC_CORPUS", "No advisory-INCLUDE commitment Event exists; production statements cannot substitute."),
            ("SUPPLY_READINESS_CONTEXT", "PRODUCTION_STAGE_CONTEXT", "EMPIRICALLY_OBSERVABLE", "Production stages are visible in seven Tracks but remain context and cannot enter the acceptance ladder."),
            ("O1_CUSTOMER_SUPPLY_OR_COMMERCIAL_SHIPMENT", "O1_COMMERCIAL_REALIZATION", "DESCRIPTIVE_ONLY", "All timed O1 candidates require the unresolved human timing policy or additional primary evidence."),
        ]
        records = []
        for stage, signal_class, assessment, rationale in stage_specs:
            records.append(
                {
                    "stage": stage,
                    "signal_class": signal_class,
                    "recommended_include_track_count": len(self._tracks_for(rows, signal_class)),
                    "recommended_hold_track_count": len(self._tracks_for(rows, signal_class, "RECOMMEND_HOLD")),
                    "recommended_exclude_track_count": len(self._tracks_for(rows, signal_class, "RECOMMEND_EXCLUDE")),
                    "observability_assessment": assessment,
                    "observable_uncertainty_dimension": {
                        "SAMPLE": "product existence and customer evaluation entry",
                        "QUALIFICATION": "partial technical-acceptance stage",
                        "DESIGN_IN": "commercial/platform selection",
                        "COMMERCIAL_COMMITMENT": "binding or allocation-adjacent commercial commitment",
                        "SUPPLY_READINESS_CONTEXT": "manufacturing readiness only",
                        "O1_CUSTOMER_SUPPLY_OR_COMMERCIAL_SHIPMENT": "public supplier-side commercial confirmation",
                    }[stage],
                    "rationale": rationale,
                    "maximum_business_interpretation": (
                        "Monitoring, qualification/TTM prioritization, and an internal confirmation request only."
                    ),
                    "prohibited_interpretation": "No fab decision, customer allocation quantity, price, volume, supplier share, or demand probability.",
                }
            )
        return _with_hash(
            {
                "observability_version": PACKAGE_VERSION,
                "created_at": CREATED_AT,
                "stratum": "H1-P",
                "complete_sequential_ladder_assessment": "NOT_IDENTIFIABLE_WITH_PUBLIC_CORPUS",
                "complete_sequential_ladder_reason": "Sample is broadly visible, qualification is sparse, design-in and commitment are absent after advisory review, and O1 timing is unresolved. The ladder must not be forced.",
                "production_context_boundary": "Supply readiness is observable separately and is never an acceptance signal or O1.",
                "records": records,
            }
        )

    def _build_h1_c_observability(self, event_matrix: dict[str, Any]) -> dict[str, Any]:
        rows = [row for row in event_matrix["records"] if row["track_type"] == "CUSTOMER_PLATFORM_REALIZATION_TRACK"]
        specs = [
            ("CAPEX", "CSP_CAPEX", None, "EMPIRICALLY_OBSERVABLE", "Company-period CAPEX context is available for all raw Tracks, but advisory review excludes three post-P1 uses and five origins cannot become fourteen independent observations."),
            ("AI_INFRASTRUCTURE_COMMITMENT", "AI_INFRA_COMMITMENT", None, "DESCRIPTIVE_ONLY", "Only one Track has an advisory-INCLUDE commitment Event."),
            ("PLATFORM_ANNOUNCEMENT", "PLATFORM_LAUNCH", None, "SPARSE_BUT_USABLE", "Three named-platform planned/launch Events are directly visible."),
            ("PREVIEW", "PLATFORM_DEPLOYMENT_STAGE", "PREVIEW", "SPARSE_BUT_USABLE", "Four Tracks expose preview, which must remain distinct from GA."),
            ("LIMITED_AVAILABILITY", "P1_PLATFORM_OPERATIONAL_REALIZATION", "LIMITED_AVAILABILITY", "DESCRIPTIVE_ONLY", "Two Tracks expose limited availability; this is not unrestricted GA."),
            ("GENERAL_AVAILABILITY", "P1_PLATFORM_OPERATIONAL_REALIZATION", "GENERAL_AVAILABILITY", "EMPIRICALLY_OBSERVABLE", "Named-platform GA is systematically visible, subject to one accepted retrospective timing HOLD and one raw retrospective HOLD."),
            ("INSTALLED_OR_OPERATIONAL", "P1_PLATFORM_OPERATIONAL_REALIZATION", "INSTALLED_OPERATIONAL", "SPARSE_BUT_USABLE", "One Meta H100 operating-cluster Event is advisory-INCLUDE; the GB200 rack caption is excluded because installed configuration is not operational use."),
            ("EXPLICIT_NAMED_TRACK_DELAY_OR_CONSTRAINT", "__NEGATIVE__", None, "NOT_IDENTIFIABLE_WITH_PUBLIC_CORPUS", "No named Platform Track has an accepted explicit delay/constraint Event."),
        ]
        records = []
        for stage, signal_class, subtype, assessment, rationale in specs:
            if signal_class == "__NEGATIVE__":
                included = held = excluded = set()
            else:
                included = self._tracks_for(rows, signal_class, "RECOMMEND_INCLUDE", subtype)
                held = self._tracks_for(rows, signal_class, "RECOMMEND_HOLD", subtype)
                excluded = self._tracks_for(rows, signal_class, "RECOMMEND_EXCLUDE", subtype)
            records.append(
                {
                    "state": stage,
                    "signal_class": signal_class,
                    "signal_subtype_filter": subtype,
                    "recommended_include_track_count": len(included),
                    "recommended_hold_track_count": len(held),
                    "recommended_exclude_track_count": len(excluded),
                    "observability_assessment": assessment,
                    "rationale": rationale,
                    "maximum_business_interpretation": "Platform/customer monitoring and TTM/customer-timing review only.",
                    "prohibited_interpretation": "No utilization, exact HBM volume, platform-specific CAPEX allocation, or named supplier inference.",
                }
            )
        return _with_hash(
            {
                "observability_version": PACKAGE_VERSION,
                "created_at": CREATED_AT,
                "stratum": "H1-C",
                "complete_state_ladder_assessment": "SPARSE_AND_HETEROGENEOUS_NOT_A_UNIVERSAL_SEQUENCE",
                "complete_state_ladder_reason": "Announcement, preview, limited availability, GA, and internal operational states are observable in different Tracks; they cannot be collapsed or assumed to occur in every Track.",
                "capex_boundary": "Repeated Track references remain one independent company-period origin and broad context only.",
                "records": records,
            }
        )

    @staticmethod
    def _build_negative_audit(
        collection: dict[str, dict[str, Any]],
        sources: dict[str, dict[str, Any]],
    ) -> dict[str, Any]:
        product_tracks = [row for row in collection.values() if row["track_id"].startswith("P") and row["negative_search_result"] == "EXPLICIT_NEGATIVE_OR_DELAY"]
        platform_tracks = [row for row in collection.values() if row["track_id"].startswith("C") and row["negative_search_result"] == "EXPLICIT_NEGATIVE_OR_DELAY"]

        def origin_groups(track_rows: list[dict[str, Any]]) -> list[str]:
            return sorted({sources[source_id]["origin_group"] for row in track_rows for source_id in row["negative_source_ids"]})

        def source_traces(track_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
            source_ids = sorted(
                {source_id for row in track_rows for source_id in row["negative_source_ids"]}
            )
            return [
                {
                    "source_id": source_id,
                    "title": sources[source_id]["title"],
                    "publisher": sources[source_id]["publisher"],
                    "url": sources[source_id]["url"],
                    "direct_excerpt": sources[source_id]["excerpt"],
                    "locator": sources[source_id]["locator"],
                    "content_hash": sources[source_id]["content_hash"],
                    "origin_group": sources[source_id]["origin_group"],
                }
                for source_id in source_ids
            ]

        records = [
            {
                "stratum": "H1-P",
                "required_explicit_negative_or_delayed_tracks": 2,
                "required_independent_origin_groups": 2,
                "additional_product_scope_negative_required": 1,
                "observed_track_count": len(product_tracks),
                "observed_track_ids": sorted(row["track_id"] for row in product_tracks),
                "observed_source_ids": sorted({source_id for row in product_tracks for source_id in row["negative_source_ids"]}),
                "observed_source_traces": source_traces(product_tracks),
                "observed_origin_groups": origin_groups(product_tracks),
                "atomic_event_representation": "TRACK_LEVEL_NEGATIVE_SOURCE_TRACE_ONLY",
                "representation_gap": "The current SIGNAL/OUTCOME/CONTEXT Event model has no separately admitted COUNTEREVIDENCE Event for this source. Human approval is required before any later negative-case empirical use.",
                "gap": "One additional explicit negative/delayed Product Track from a second independent origin is required.",
                "consequence": "Frozen comparative-verdict sufficiency is not met; silence cannot fill the gap.",
            },
            {
                "stratum": "H1-C",
                "required_explicit_negative_or_delayed_tracks": 2,
                "required_independent_origin_groups": 2,
                "additional_product_scope_negative_required": 0,
                "observed_track_count": len(platform_tracks),
                "observed_track_ids": sorted(row["track_id"] for row in platform_tracks),
                "observed_source_ids": sorted({source_id for row in platform_tracks for source_id in row["negative_source_ids"]}),
                "observed_source_traces": source_traces(platform_tracks),
                "observed_origin_groups": origin_groups(platform_tracks),
                "atomic_event_representation": "NONE",
                "representation_gap": "No named-Platform negative source or Event is present.",
                "gap": "Two explicit named-Platform delay/negative Tracks from two independent origins are required.",
                "consequence": "Frozen comparative-verdict sufficiency is not met; public non-observation is not failure.",
            },
        ]
        return _with_hash(
            {
                "audit_version": PACKAGE_VERSION,
                "created_at": CREATED_AT,
                "thresholds_unchanged": True,
                "records": records,
            }
        )

    @staticmethod
    def _build_bias_register() -> dict[str, Any]:
        rows = [
            {
                "bias_id": "SUCCESS_ANNOUNCEMENT_BIAS",
                "mechanism": "Successful samples, qualifications, shipments, and launches are more likely to receive official announcements than failed or abandoned efforts.",
                "affected_stratum": "H1-P,H1-C",
                "affected_metric": "Any future observed milestone or no-realization summary",
                "likely_direction_of_bias": "Observed corpus can overrepresent successful progression and undercount adverse paths.",
                "mitigation": "Outcome-neutral Track registry, completed adverse search, explicit negative threshold, and no inference from silence.",
                "residual_limitation": "Disclosure remains Missing Not At Random; unannounced failures are not recoverable.",
            },
            {
                "bias_id": "QUALIFICATION_FAILURE_NONDISCLOSURE",
                "mechanism": "Named qualification completion, failure criteria, and rejected samples are usually confidential.",
                "affected_stratum": "H1-P",
                "affected_metric": "Future stage-transition and negative-case descriptions",
                "likely_direction_of_bias": "Technical acceptance can appear more complete and failures less frequent than reality.",
                "mitigation": "Keep substages literal and require explicit product-scope negative evidence.",
                "residual_limitation": "The corpus cannot identify a full qualification denominator.",
            },
            {
                "bias_id": "CUSTOMER_COMMERCIAL_CONFIDENTIALITY",
                "mechanism": "Customer identity, contract, allocation, price, volume, and supplier share are often private.",
                "affected_stratum": "H1-P",
                "affected_metric": "Commitment, O1 scope, and decision translation",
                "likely_direction_of_bias": "Commercial selection is missing and broad supplier claims can be overgeneralized.",
                "mitigation": "Preserve KNOWN_UNKNOWN fields and prohibit inferred customer/supplier bridges.",
                "residual_limitation": "Public O1 is only a supplier-side commercialization proxy.",
            },
            {
                "bias_id": "SUPPLIER_DISCLOSURE_HETEROGENEITY",
                "mechanism": "Suppliers use different milestone verbs, cadence, and product/customer scope.",
                "affected_stratum": "H1-P",
                "affected_metric": "Future cross-supplier stage comparisons",
                "likely_direction_of_bias": "Disclosure-heavy suppliers can appear to progress through more observable stages.",
                "mitigation": "Literal stage taxonomy, leave-one-supplier sensitivity if later authorized, and no imputation.",
                "residual_limitation": "Comparability remains limited even after deterministic normalization.",
            },
            {
                "bias_id": "CLOUD_AVAILABILITY_DISCLOSURE_ASYMMETRY",
                "mechanism": "Cloud providers publish named service availability more systematically than memory suppliers publish commercial selection.",
                "affected_stratum": "H1-C versus H1-P",
                "affected_metric": "Cross-strata observability",
                "likely_direction_of_bias": "H1-C can look more complete for disclosure-structure reasons, not superior signal quality.",
                "mitigation": "Never pool strata or compare raw coverage as performance.",
                "residual_limitation": "Cross-strata data completeness remains structurally different.",
            },
            {
                "bias_id": "CAPEX_CONTEXT_REUSE",
                "mechanism": "One company-period CAPEX disclosure is referenced by several named Platform Tracks.",
                "affected_stratum": "H1-C",
                "affected_metric": "Any future count or comparison using CAPEX",
                "likely_direction_of_bias": "Repeated references can create pseudo-replication and false independence.",
                "mitigation": "Count independence by origin group and permit Track reuse as context only.",
                "residual_limitation": "CAPEX remains broad and cannot be allocated to a named SKU.",
            },
            {
                "bias_id": "RECENT_GENERATION_RIGHT_CENSORING",
                "mechanism": "HBM4/HBM4E and Blackwell Tracks have less elapsed follow-up than older generations.",
                "affected_stratum": "H1-P,H1-C",
                "affected_metric": "Any future no-realization or timing description",
                "likely_direction_of_bias": "Recent Tracks can be incorrectly treated as failures or omitted in a way that favors older successes.",
                "mitigation": "Frozen 6/12/18-month readiness flags and denominator exclusion for right-censored Events.",
                "residual_limitation": "Longer follow-up is not available at this Gate 6 cutoff.",
            },
            {
                "bias_id": "AVAILABILITY_UTILIZATION_GAP",
                "mechanism": "GA or installed infrastructure is publicly visible while utilization and memory consumption are usually not.",
                "affected_stratum": "H1-C",
                "affected_metric": "Platform operational interpretation",
                "likely_direction_of_bias": "Availability can be mistaken for high use or realized memory volume.",
                "mitigation": "Keep GA, limited availability, installed, and operational subtypes separate.",
                "residual_limitation": "Public sources do not establish actual utilization or exact HBM demand.",
            },
        ]
        return _with_hash(
            {
                "bias_register_version": PACKAGE_VERSION,
                "created_at": CREATED_AT,
                "missingness_mechanism": "POTENTIALLY_MISSING_NOT_AT_RANDOM",
                "records": rows,
            }
        )

    @staticmethod
    def _build_capex_audit(
        event_matrix: dict[str, Any], tracks: dict[str, dict[str, Any]]
    ) -> dict[str, Any]:
        grouped: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
        for row in event_matrix["records"]:
            if row["signal_class"] == "CSP_CAPEX":
                grouped[(row["source_id"], row["origin_group"])].append(row)
        rows = []
        for (source_id, origin_group), events in sorted(grouped.items()):
            rows.append(
                {
                    "csp": sorted({tracks[row["track_id"]]["entity"] for row in events}),
                    "capex_source_id": source_id,
                    "source_title": events[0]["source_title"],
                    "origin_group": origin_group,
                    "track_ids_referencing_source": sorted(row["track_id"] for row in events),
                    "event_ids_referencing_source": sorted(row["event_id"] for row in events),
                    "track_reference_count": len(events),
                    "recommendation_by_event": {row["event_id"]: row["codex_recommendation"] for row in sorted(events, key=lambda item: item["event_id"])},
                    "one_independent_company_period_observation": True,
                    "may_be_reused_as_context": True,
                    "may_be_counted_repeatedly_in_empirical_denominator": False,
                    "scope_boundary": "Company-period investment context; no named-platform funding allocation.",
                }
            )
        return _with_hash(
            {
                "capex_audit_version": PACKAGE_VERSION,
                "created_at": CREATED_AT,
                "raw_track_references": sum(row["track_reference_count"] for row in rows),
                "independent_company_period_origins": len(rows),
                "default_analytical_principle": "Repeated Track references do not create independent CAPEX observations.",
                "records": rows,
            }
        )

    @staticmethod
    def _build_o1_options(event_matrix: dict[str, Any]) -> dict[str, Any]:
        o1_rows = [row for row in event_matrix["records"] if row["signal_class"] == "O1_COMMERCIAL_REALIZATION"]
        return _with_hash(
            {
                "policy_options_version": PACKAGE_VERSION,
                "created_at": CREATED_AT,
                "candidate_event_ids": sorted(row["event_id"] for row in o1_rows),
                "human_selected_policy": None,
                "options": [
                    {
                        "policy_id": "POLICY_A_EXACT_DATE_ONLY",
                        "definition": "Admit timed O1 only when a primary source explicitly states the first customer-supply or shipment date.",
                        "effect_on_h1_p_sample": "None of the six current O1 candidates states an exact first date; timed O1 coverage would fall to zero unless a new exact primary source is admitted.",
                        "compatibility_with_gates_1_to_5": "COMPATIBLE_AND_MOST_RESTRICTIVE",
                        "required_contract_change": "NONE",
                        "human_approval_alone_sufficient": True,
                        "main_tradeoff": "Highest temporal purity with severe loss of observable O1 timing.",
                    },
                    {
                        "policy_id": "POLICY_B_PUBLIC_CONFIRMATION_PROXY",
                        "definition": "Use the first public current-shipping confirmation available_at as an information-confirmation proxy, never as the actual first shipment date.",
                        "effect_on_h1_p_sample": "Could retain up to five current-shipping/current-supply candidates; the future-only P02 statement remains ineligible. Final admission still requires human Event review.",
                        "compatibility_with_gates_1_to_5": "CONDITIONALLY_COMPATIBLE_IF_ESTIMAND_IS_RELABELED_AS_PUBLIC_CONFIRMATION_TIMING",
                        "required_contract_change": "Gate 6 timing specification plus derived-field implementation; O1 occurrence wording remains unchanged.",
                        "human_approval_alone_sufficient": False,
                        "main_tradeoff": "Preserves historical information logic but measures public confirmation, not operational start.",
                    },
                    {
                        "policy_id": "POLICY_C_INTERVAL_CENSORED_REALIZATION",
                        "definition": "Represent realization inside a defensible interval bounded by prior future/non-current evidence and later current-shipping evidence.",
                        "effect_on_h1_p_sample": "Could preserve a bounded subset only where both interval bounds are directly supported; no final count is authorized before human review.",
                        "compatibility_with_gates_1_to_5": "CONCEPTUALLY_ALIGNED_WITH_FROZEN_INTERVAL_RULES_BUT_NOT_IMPLEMENTED_IN_CURRENT_EVENT_SCHEMA",
                        "required_contract_change": "Add lower/upper outcome-time fields, validation, replay, and tests before Gate 6 freeze.",
                        "human_approval_alone_sufficient": False,
                        "main_tradeoff": "Closer to the available evidence but requires an explicit measurement-contract implementation change.",
                    },
                ],
            }
        )

    @staticmethod
    def _build_authorization(
        h1_p: dict[str, Any], h1_c: dict[str, Any], negative: dict[str, Any]
    ) -> dict[str, Any]:
        levels = [
            {
                "level": "LEVEL_0_NO_EMPIRICAL_ANALYSIS",
                "allowed": ["corpus description", "coverage and missingness"],
                "prohibited": ["timing comparison", "signal superiority", "realization probability", "verdict"],
            },
            {
                "level": "LEVEL_1_DESCRIPTIVE_TIMELINE",
                "allowed": ["observed Event ordering", "historical information-state reconstruction", "coverage/missingness", "public milestones"],
                "prohibited": ["signal superiority", "realization probability", "comparative success claims"],
            },
            {
                "level": "LEVEL_2_BOUNDED_LEAD_TIME_DESCRIPTION",
                "allowed": ["observed public-information timing intervals where Signal and Outcome timing are defensible"],
                "prohibited": ["causal predictive effect", "population probability", "cross-strata pooling"],
            },
            {
                "level": "LEVEL_3_DESCRIPTIVE_CONDITIONAL_COMPARISON",
                "allowed": ["conditioned comparison of observed public cases with disclosure limits"],
                "prohibited": ["population probability", "universal ranking", "causal claim"],
            },
            {
                "level": "LEVEL_4_COMPARATIVE_H1_VERDICT",
                "allowed": ["separate human-approved H1-P or H1-C verdict after every frozen sufficiency criterion is met"],
                "prohibited": ["pooled verdict", "threshold relaxation", "automated business decision"],
            },
        ]
        strata = [
            {
                "stratum": "H1-P",
                "codex_proposed_maximum_level": "LEVEL_1_DESCRIPTIVE_TIMELINE",
                "reasons": [
                    "The complete acceptance ladder is not publicly identifiable.",
                    "Timed O1 admission is unresolved under the current policy.",
                    "Only one explicit product negative/delay origin is observed.",
                ],
                "unmet_requirements": ["O1 timing policy", "second independent explicit negative/delayed Product Track", "human-approved negative-evidence representation", "human Event admission"],
                "conditionally_possible_after_human_action": "LEVEL_2 may become possible for a bounded subset after an approved O1 timing policy and replay; this package does not authorize it.",
                "maximum_business_interpretation": "Monitor product stages, prioritize qualification/TTM questions, and request internal customer confirmation.",
                "must_remain_prohibited": ["fab/CAPA decision", "customer allocation quantity", "price/volume/share forecast", "comparative H1 verdict"],
            },
            {
                "stratum": "H1-C",
                "codex_proposed_maximum_level": "LEVEL_2_BOUNDED_LEAD_TIME_DESCRIPTION",
                "reasons": [
                    "Named-platform announcement/preview/limited/GA/operational timestamps are observable for an older subset.",
                    "Company CAPEX is repeated broad context and cannot be counted as fourteen independent observations.",
                    "No named-Platform explicit negative/delay Track is observed.",
                ],
                "unmet_requirements": ["two independent named-Platform negative/delayed Tracks", "human Event admission", "state-specific scope conditioning"],
                "conditionally_possible_after_human_action": "Only state-specific bounded timing description is proposed; LEVEL 3/4 remain unsupported by this corpus.",
                "maximum_business_interpretation": "Monitor platform/customer timing and review TTM or internal demand-confirmation needs.",
                "must_remain_prohibited": ["utilization inference", "exact HBM demand", "named supplier inference", "repeated CAPEX denominator", "comparative H1 verdict"],
            },
        ]
        return _with_hash(
            {
                "authorization_version": PACKAGE_VERSION,
                "created_at": CREATED_AT,
                "advisory_only": True,
                "human_authorization_selected": False,
                "levels": levels,
                "strata": strata,
                "sequential_information_boundary": "Later stages are selected information states. Future analysis may ask what uncertainty each state reduces; it must not declare the stage with the highest observed realization the best predictor.",
            }
        )

    @staticmethod
    def _build_human_checklist(
        event_matrix: dict[str, Any],
        hold_sheet: dict[str, Any],
        sources: dict[str, dict[str, Any]],
    ) -> dict[str, Any]:
        origin_map: dict[str, set[str]] = defaultdict(set)
        for row in event_matrix["records"]:
            origin_map[row["origin_group"]].add(row["source_id"])
        return _with_hash(
            {
                "checklist_version": PACKAGE_VERSION,
                "created_at": CREATED_AT,
                "checklist_complete": False,
                "event_admission": [
                    {
                        "event_id": row["event_id"],
                        "current_review_status": row["current_review_status"],
                        "codex_recommendation": row["codex_recommendation"],
                        "human_decision": None,
                        "allowed_values": ["APPROVE", "EXCLUDE", "HOLD"],
                        "human_reason": None,
                    }
                    for row in event_matrix["records"]
                ],
                "hold_resolution": [
                    {
                        "event_id": row["event_id"],
                        "human_resolution": None,
                        "allowed_values": row["human_options"] + ["RETAIN_HOLD"],
                        "human_reason": None,
                    }
                    for row in hold_sheet["records"]
                ],
                "o1_timing_policy": {
                    "human_selected_policy": None,
                    "allowed_values": ["POLICY_A_EXACT_DATE_ONLY", "POLICY_B_PUBLIC_CONFIRMATION_PROXY", "POLICY_C_INTERVAL_CENSORED_REALIZATION", "REJECT_ALL"],
                    "human_reason": None,
                },
                "origin_grouping": [
                    {
                        "origin_group": origin,
                        "source_ids": sorted(source_ids),
                        "human_decision": None,
                        "allowed_values": ["APPROVE", "REVISE"],
                        "human_reason": None,
                    }
                    for origin, source_ids in sorted(origin_map.items())
                ],
                "event_precision": [
                    {
                        "event_id": row["event_id"],
                        "current_event_date_precision": row["event_date_precision"],
                        "human_decision": None,
                        "allowed_values": ["APPROVE", "REVISE"],
                        "human_reason": None,
                    }
                    for row in event_matrix["records"]
                ],
                "contract_change_flags": [
                    {
                        "issue_id": "NEGATIVE_EVIDENCE_ATOMIC_REPRESENTATION",
                        "issue": "The sole product negative is source-traced at Track level but the current Event model has no COUNTEREVIDENCE role.",
                        "human_decision": None,
                        "allowed_values": ["KEEP_TRACK_LEVEL_DESCRIPTIVE_ONLY", "AUTHORIZE_FUTURE_SCHEMA_EXTENSION", "DO_NOT_FREEZE"],
                        "human_reason": None,
                    },
                    {
                        "issue_id": "O1_INTERVAL_TIME_FIELDS",
                        "issue": "Policy C would require lower/upper outcome-time fields not implemented in the current Event schema.",
                        "human_decision": None,
                        "allowed_values": ["DO_NOT_USE_POLICY_C", "AUTHORIZE_CONTRACT_IMPLEMENTATION_BEFORE_FREEZE", "DO_NOT_FREEZE"],
                        "human_reason": None,
                    },
                ],
                "h1_p_readiness": {
                    "human_decision": None,
                    "allowed_values": ["NOT_READY", "DESCRIPTIVE_ONLY", "BOUNDED_EMPIRICAL_ANALYSIS", "FULL_COMPARATIVE_ANALYSIS"],
                    "human_reason": None,
                },
                "h1_c_readiness": {
                    "human_decision": None,
                    "allowed_values": ["NOT_READY", "DESCRIPTIVE_ONLY", "BOUNDED_EMPIRICAL_ANALYSIS", "FULL_COMPARATIVE_ANALYSIS"],
                    "human_reason": None,
                },
                "gate6": {
                    "human_decision": None,
                    "allowed_values": ["FREEZE", "FREEZE_WITH_EXCLUSIONS", "DO_NOT_FREEZE"],
                    "human_reason": None,
                },
            }
        )

    @staticmethod
    def _build_candidate_capability_facts() -> dict[str, Any]:
        return _with_hash(
            {
                "candidate_fact_version": PACKAGE_VERSION,
                "created_at": CREATED_AT,
                "ledger_mutated": False,
                "records": [
                    {
                        "candidate_fact_id": "CAP-G06-CANDIDATE-001",
                        "claim_status": "CANDIDATE_PENDING_HUMAN_GATE6_DECISION",
                        "performed_action_candidate": "Reviewed all 75 corpus Events and separated deterministic acceptance from semantic admission advice.",
                        "why_material": "It demonstrates that rule-passing evidence was not defaulted into the empirical dataset.",
                        "artifact_references": ["data/h1/gate6_review/event_review_matrix.json"],
                        "verification_condition": "Human completes Event admission and Gate 6 decision.",
                    },
                    {
                        "candidate_fact_id": "CAP-G06-CANDIDATE-002",
                        "claim_status": "CANDIDATE_PENDING_HUMAN_GATE6_DECISION",
                        "performed_action_candidate": "Kept public non-observation separate from explicit failure and documented that frozen negative thresholds are unmet.",
                        "why_material": "It prevents a resume-friendly comparative conclusion from overriding research truth.",
                        "artifact_references": ["data/h1/gate6_review/negative_evidence_sufficiency.json"],
                        "verification_condition": "Human confirms the readiness level and Gate 6 disposition.",
                    },
                    {
                        "candidate_fact_id": "CAP-G06-CANDIDATE-003",
                        "claim_status": "CANDIDATE_PENDING_HUMAN_GATE6_DECISION",
                        "performed_action_candidate": "Reduced fourteen Track-level CAPEX references to five independent company-period origins for independence review.",
                        "why_material": "It prevents pseudo-replication while retaining broad investment context.",
                        "artifact_references": ["data/h1/gate6_review/capex_independence_reuse_audit.json"],
                        "verification_condition": "Human approves or revises origin grouping at Gate 6.",
                    },
                ],
            }
        )

    @staticmethod
    def _render_markdown(
        event_matrix: dict[str, Any],
        hold_sheet: dict[str, Any],
        h1_p: dict[str, Any],
        h1_c: dict[str, Any],
        negative: dict[str, Any],
        censoring: dict[str, Any],
        capex: dict[str, Any],
        o1: dict[str, Any],
        authorization: dict[str, Any],
    ) -> str:
        rec = event_matrix["recommendation_counts"]
        hold_recs = Counter(row["codex_recommendation"] for row in hold_sheet["records"])
        censor_lines = []
        for key, value in censoring["summary"].items():
            censor_lines.append(
                f"| {key} | {value['tracks_all_anchor_events_fully_observed']} | {value['tracks_with_any_right_censoring']} | {value['tracks_with_any_denominator_eligible_signal']} | {value['tracks_descriptive_only']} |"
            )
        p_rows = "\n".join(
            f"| {row['stage']} | {row['recommended_include_track_count']} | {row['recommended_hold_track_count']} | {row['observability_assessment']} |"
            for row in h1_p["records"]
        )
        c_rows = "\n".join(
            f"| {row['state']} | {row['recommended_include_track_count']} | {row['recommended_hold_track_count']} | {row['observability_assessment']} |"
            for row in h1_c["records"]
        )
        neg_rows = "\n".join(
            f"| {row['stratum']} | {row['required_explicit_negative_or_delayed_tracks']} / {row['required_independent_origin_groups']} origins | {row['observed_track_count']} / {len(row['observed_origin_groups'])} origins | {row['consequence']} |"
            for row in negative["records"]
        )
        policy_rows = "\n".join(
            f"| {row['policy_id']} | {row['effect_on_h1_p_sample']} | {row['compatibility_with_gates_1_to_5']} | {row['human_approval_alone_sufficient']} |"
            for row in o1["options"]
        )
        auth_rows = "\n".join(
            f"| {row['stratum']} | {row['codex_proposed_maximum_level']} | {'; '.join(row['unmet_requirements'])} |"
            for row in authorization["strata"]
        )
        return f"""# Human Gate 6 Corpus-Readiness Review Package

## Status and boundary

This package reviews the `467c5f8` corpus for human Gate 6. It does **not** freeze Gate 6, calculate H1 outcomes, rank signals, or select a human decision. H1-P and H1-C sufficiency remain separate.

## Review artifacts

- `data/h1/gate6_review/event_review_matrix.json` / `.csv`: all 75 Events and advisory admission recommendations
- `data/h1/gate6_review/hold_resolution_sheet.json` / `.csv`: all 12 raw HOLDs
- `data/h1/gate6_review/track_readiness_matrix.json` / `.csv`: all 24 Tracks
- `data/h1/gate6_review/h1_p_observability_matrix.json`
- `data/h1/gate6_review/h1_c_observability_matrix.json`
- `data/h1/gate6_review/negative_evidence_sufficiency.json`
- `data/h1/gate6_review/disclosure_bias_register.json` / `.csv`
- `data/h1/gate6_review/censoring_readiness_matrix.json` / `.csv`
- `data/h1/gate6_review/capex_independence_reuse_audit.json` / `.csv`
- `data/h1/gate6_review/o1_timing_policy_options.json`
- `data/h1/gate6_review/analysis_authorization_proposal.json`
- `data/h1/gate6_review/human_decision_checklist.json`
- `data/h1/gate6_review/candidate_capability_facts.json`

## Event review result

| Advisory recommendation | Count |
|---|---:|
| RECOMMEND_INCLUDE | {rec.get('RECOMMEND_INCLUDE', 0)} |
| RECOMMEND_HOLD | {rec.get('RECOMMEND_HOLD', 0)} |
| RECOMMEND_EXCLUDE | {rec.get('RECOMMEND_EXCLUDE', 0)} |

The 12 raw HOLDs remain unresolved: {hold_recs.get('RECOMMEND_HOLD', 0)} retain-HOLD recommendations and {hold_recs.get('RECOMMEND_EXCLUDE', 0)} exclusion recommendations. Four deterministically accepted Events are additionally recommended HOLD, and three accepted post-outcome CAPEX uses are recommended EXCLUDE. No source record or `review_status` was changed.

## H1-P observability

| Stage | Advisory-INCLUDE Tracks | Advisory-HOLD Tracks | Assessment |
|---|---:|---:|---|
{p_rows}

Complete `Sample → Qualification → Design-in → Commitment → O1` sequencing is `NOT_IDENTIFIABLE_WITH_PUBLIC_CORPUS`. Production is separately observable supply-readiness context, not a substitute stage.

## H1-C observability

| State | Advisory-INCLUDE Tracks | Advisory-HOLD Tracks | Assessment |
|---|---:|---:|---|
{c_rows}

Platform states are visible but heterogeneous. GA does not prove utilization, and installed infrastructure does not automatically prove operation. Raw CAPEX coverage is fourteen Track references to five independent company-period origins.

## Negative-evidence sufficiency

| Stratum | Frozen requirement | Observed | Consequence |
|---|---|---|---|
{neg_rows}

The frozen negative-case threshold is unmet in both strata and is not relaxed.

The sole H1-P negative is fully Source-traced at Track level, but the current three-role Event model has no separately admitted Atomic counterevidence Event. This is routed to human contract review rather than silently repaired.

## Censoring readiness

Readiness uses advisory-INCLUDE Signal `available_at` plus the frozen windows at the corpus cutoff. It does not inspect outcomes.

| Stratum:window | All anchors fully observed | Any right censoring | Any denominator-eligible Signal | Descriptive only |
|---|---:|---:|---:|---:|
{chr(10).join(censor_lines)}

Right-censored Events are never treated as failure. P01 is left-truncated; recent HBM4/HBM4E and Blackwell Events remain partially or wholly descriptive depending on the window.

## CAPEX independence

- Raw Track references: {capex['raw_track_references']}
- Independent company-period origins: {capex['independent_company_period_origins']}
- Rule: repeated Track references may be context but may not be counted repeatedly in an empirical denominator.

## O1 timing policy options

| Option | Sample effect | Gate compatibility | Human approval alone sufficient? |
|---|---|---|---|
{policy_rows}

No option is selected. Policy C needs schema/validator/replay work before a later freeze; this task does not implement it.

## Non-binding analysis authorization

| Stratum | Proposed maximum | Unmet requirements |
|---|---|---|
{auth_rows}

H1-P can currently support product-stage timeline and missingness description. H1-C can support state-specific bounded timing description for defensible dated subsets. Neither supports a comparative verdict.

## Human decisions required

Use `human_decision_checklist.json` to decide every Event, resolve/retain every HOLD, select or reject an O1 policy, approve/revise origin groups and precision, select H1-P and H1-C readiness independently, and finally select `FREEZE`, `FREEZE_WITH_EXCLUSIONS`, or `DO_NOT_FREEZE`. Every final human field is currently null.

## Stop

The next task is human Gate 6 decision and empirical dataset freeze. No freeze or empirical H1 calculation is performed here.
"""


def main() -> None:
    parser = argparse.ArgumentParser(description="Build the non-binding Human Gate 6 corpus-readiness review package")
    parser.add_argument("--workspace", type=Path, default=Path("."))
    args = parser.parse_args()
    builder = Gate6ReviewBuilder(args.workspace.resolve())
    manifest = builder.build()
    print(json.dumps(manifest, ensure_ascii=False, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
