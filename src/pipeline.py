from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

from src.adapters.contracts import ManualScenarioAdapter
from src.audit.auditor import DeterministicAuditor
from src.audit.scoring import score_evidence, summarize_scores
from src.core.harness import DeterministicHarness
from src.core.models import EvidenceRecord, EvidenceStatus, ReviewRecord, SourceRecord
from src.core.storage import (
    DuplicateConflict,
    EvidenceRegistry,
    ReviewRegistry,
    SourceRegistry,
    canonical_json,
    content_digest,
    load_json,
    put_jsonl,
    write_json,
)
from src.graph.store import FileGraph
from src.memo.builder import build_memo, render_markdown
from src.retrieval.lightweight import retrieve


class SourceHashMismatch(ValueError):
    pass


class ReviewManifestError(ValueError):
    pass


CORE_IMPLEMENTATION_VERSION = "1.1.0-evidence-review-temporal"


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def _contradiction_counts(audit: dict[str, Any]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for item in audit["contradictions"]:
        for evidence_id in item["trigger_evidence_ids"] + item.get("counterevidence_ids", []):
            counts[evidence_id] = counts.get(evidence_id, 0) + 1
    return counts


def _unresolved_contradictions(evidence_id: str, audit: dict[str, Any]) -> list[str]:
    return sorted(
        item["contradiction_id"]
        for item in audit["contradictions"]
        if item.get("status") == "OPEN"
        and evidence_id in item["trigger_evidence_ids"] + item.get("counterevidence_ids", [])
    )


def _independent_source_count(
    evidence: dict[str, Any], records: list[dict[str, Any]]
) -> int:
    return len(
        {
            item["source_id"]
            for item in records
            if item.get("claim") == evidence.get("claim") and item.get("source_id")
        }
    )


def _write_run_log(root: Path, run_id: str, evidence_records: list[dict[str, Any]]) -> None:
    path = root / "logs" / f"{run_id}.jsonl"
    if path.exists():
        path.unlink()
    for evidence in sorted(evidence_records, key=lambda item: item["evidence_id"]):
        for ordinal, transition in enumerate(evidence["transitions"]):
            if transition["run_id"] != run_id:
                continue
            put_jsonl(
                path,
                {
                    "log_id": f"{evidence['evidence_id']}::{ordinal}::{transition['to_status']}",
                    "evidence_id": evidence["evidence_id"],
                    **transition,
                },
                "log_id",
                immutable=True,
            )


IMMUTABLE_EVIDENCE_FIELDS = (
    "evidence_id",
    "source_id",
    "publication_date",
    "excerpt",
    "locator",
    "claim",
    "event_type",
    "evidence_level",
    "demand_or_supply",
    "entities",
    "relationship",
    "decision_variables",
    "verification_status",
)


def _load_or_create_evidence(
    spec: dict[str, Any],
    source: SourceRecord,
    existing_map: dict[str, dict[str, Any]],
    run_id: str,
    run_at: str,
) -> EvidenceRecord:
    fresh = EvidenceRecord.from_spec(
        spec, source, run_id, run_at, actor="manual-scenario-adapter"
    )
    existing = existing_map.get(fresh.evidence_id)
    if existing is None:
        return fresh
    fresh_dict = fresh.to_dict()
    for field in IMMUTABLE_EVIDENCE_FIELDS:
        if canonical_json(existing.get(field)) != canonical_json(fresh_dict.get(field)):
            raise DuplicateConflict(
                f"newer scenario cannot overwrite {fresh.evidence_id}.{field}"
            )
    return EvidenceRecord.from_dict(existing)


def _load_reviews(root: Path, payload: dict[str, Any], evidence_ids: set[str]) -> dict[str, ReviewRecord]:
    relative = payload.get("review_manifest_path", "data/reviews/review_manifest.jsonl")
    registry = ReviewRegistry(root / relative)
    reviews = [ReviewRecord.from_dict(item) for item in registry.for_run(payload["run_id"])]
    by_evidence: dict[str, ReviewRecord] = {}
    for review in reviews:
        if review.evidence_id not in evidence_ids:
            raise ReviewManifestError(
                f"review {review.review_id} references Evidence outside run {payload['run_id']}"
            )
        if review.evidence_id in by_evidence:
            raise ReviewManifestError(
                f"multiple review records for {review.evidence_id} in {payload['run_id']}"
            )
        by_evidence[review.evidence_id] = review
    return by_evidence


def _edge_snapshot(graph: FileGraph) -> list[dict[str, Any]]:
    return sorted(graph.edges, key=lambda item: item["edge_id"])


def _temporal_state_diff(
    root: Path,
    payload: dict[str, Any],
    final_evidence: dict[str, dict[str, Any]],
    final_edges: list[dict[str, Any]],
) -> dict[str, Any] | None:
    baseline_run_id = payload.get("baseline_run_id")
    if not baseline_run_id:
        return None
    baseline_dir = root / "data" / "runs" / baseline_run_id
    before_result = load_json(baseline_dir / "run_result.json", None)
    before_evidence = load_json(baseline_dir / "evidence_snapshot.json", None)
    before_edges = load_json(baseline_dir / "graph_snapshot.json", None)
    if before_result is None or before_evidence is None or before_edges is None:
        raise FileNotFoundError(f"baseline snapshots missing for {baseline_run_id}")
    before_evidence_map = {item["evidence_id"]: item for item in before_evidence}
    before_edge_map = {item["edge_id"]: item for item in before_edges}
    after_edge_map = {item["edge_id"]: item for item in final_edges}

    new_evidence_ids = sorted(set(final_evidence) - set(before_evidence_map))
    confidence_changes = []
    for evidence_id in sorted(set(final_evidence) & set(before_evidence_map)):
        before = before_evidence_map[evidence_id].get("confidence", {})
        after = final_evidence[evidence_id].get("confidence", {})
        if canonical_json(before) != canonical_json(after):
            confidence_changes.append(
                {
                    "evidence_id": evidence_id,
                    "before": {"score": before.get("score"), "label": before.get("label")},
                    "after": {"score": after.get("score"), "label": after.get("label")},
                    "reason": "Deterministic rubric recomputed at the newer as-of date.",
                }
            )

    changed_edges = []
    for edge_id in sorted(set(after_edge_map) - set(before_edge_map)):
        changed_edges.append({"edge_id": edge_id, "change": "ADDED", "after": after_edge_map[edge_id]})
    for edge_id in sorted(set(after_edge_map) & set(before_edge_map)):
        if canonical_json(before_edge_map[edge_id]) != canonical_json(after_edge_map[edge_id]):
            changed_edges.append(
                {
                    "edge_id": edge_id,
                    "change": "UPDATED",
                    "before": before_edge_map[edge_id],
                    "after": after_edge_map[edge_id],
                }
            )

    temporal_spec = payload["temporal_update"]
    diff = {
        "baseline_run_id": baseline_run_id,
        "update_run_id": payload["run_id"],
        "before_state": {
            "what_changed": before_result["memo"]["what_changed"],
            "assumption": before_result["memo"]["assumption_updated"],
            "decision_variables": before_result["memo"]["decision_variables_affected"],
        },
        "new_evidence": [
            {
                "evidence_id": evidence_id,
                "source_id": final_evidence[evidence_id]["source_id"],
                "claim": final_evidence[evidence_id]["claim"],
                "evidence_level": final_evidence[evidence_id]["evidence_level"],
                "status": final_evidence[evidence_id]["status"],
            }
            for evidence_id in new_evidence_ids
        ],
        "changed_evidence_confidence": confidence_changes,
        "changed_graph_edges": changed_edges,
        "changed_decision_variables": temporal_spec["decision_variable_changes"],
        "still_unknown": temporal_spec["still_unknown"],
        "invalidation_conditions": temporal_spec["invalidation_conditions"],
    }
    diff["diff_hash"] = content_digest(diff)
    return diff


def _render_temporal_diff(diff: dict[str, Any]) -> str:
    lines = [
        "# HBM4 Temporal State Diff — 2025 Sample to 2026 Mass Shipment",
        "",
        f"Baseline: `{diff['baseline_run_id']}`",
        f"Update: `{diff['update_run_id']}`",
        f"Reproducibility hash: `{diff['diff_hash']}`",
        "",
        "## Before State",
        diff["before_state"]["what_changed"],
        "",
        "## New Evidence",
    ]
    lines.extend(f"- `{item['evidence_id']}`: {item['claim']}" for item in diff["new_evidence"])
    lines.extend(["", "## Changed Evidence Confidence"])
    if diff["changed_evidence_confidence"]:
        lines.extend(
            f"- `{item['evidence_id']}`: {item['before']} → {item['after']}"
            for item in diff["changed_evidence_confidence"]
        )
    else:
        lines.append("- None")
    lines.extend(["", "## Changed Graph Edge"])
    lines.extend(f"- `{item['edge_id']}`: {item['change']}" for item in diff["changed_graph_edges"])
    lines.extend(["", "## Changed Decision Variable"])
    lines.extend(
        f"- `{name}`: {change}"
        for name, change in sorted(diff["changed_decision_variables"].items())
    )
    lines.extend(["", "## Still Unknown"])
    lines.extend(f"- {item}" for item in diff["still_unknown"])
    lines.extend(["", "## Invalidation Condition"])
    lines.extend(f"- {item}" for item in diff["invalidation_conditions"])
    return "\n".join(lines) + "\n"


def run_vertical_slice(workspace: Path, scenario_path: Path) -> dict[str, Any]:
    root = workspace.resolve()
    payload = load_json(scenario_path, None)
    if payload is None:
        raise FileNotFoundError(scenario_path)
    payload = ManualScenarioAdapter(payload).normalized_payload()
    run_id = payload["run_id"]
    run_dir = root / "data" / "runs" / run_id
    scenario_fingerprint = content_digest(
        {"core_implementation_version": CORE_IMPLEMENTATION_VERSION, "payload": payload}
    )
    existing_result_path = run_dir / "run_result.json"
    if existing_result_path.exists():
        existing = load_json(existing_result_path, {})
        if existing.get("scenario_fingerprint") != scenario_fingerprint:
            raise ValueError(f"run_id {run_id} already exists for a different scenario")
        return existing

    source = SourceRecord.from_dict(payload["source"])
    archive_path = root / source.local_archive_path if source.local_archive_path else None
    if archive_path is not None:
        actual_hash = file_sha256(archive_path)
        if actual_hash != source.content_hash.upper():
            raise SourceHashMismatch(
                f"source content hash mismatch: expected {source.content_hash}, got {actual_hash}"
            )

    source_registry = SourceRegistry(root / "data" / "sources" / "source_registry.jsonl")
    evidence_registry = EvidenceRegistry(root / "data" / "evidence" / "atomic_evidence.jsonl")
    source_registry.register(source.to_dict())
    existing_evidence = evidence_registry.as_map()

    harness = DeterministicHarness()
    current_objects: list[EvidenceRecord] = []
    for spec in payload["evidence"]:
        evidence = _load_or_create_evidence(
            spec, source, existing_evidence, run_id, payload["run_at"]
        )
        if evidence.status == EvidenceStatus.NEW.value:
            harness.transition(
                evidence,
                EvidenceStatus.VERIFIED.value,
                "Source provenance and local archive hash verified",
                run_id,
                payload["run_at"],
            )
            harness.transition(
                evidence,
                EvidenceStatus.CLASSIFIED.value,
                "Evidence level, event type, demand/supply class, and decision variables validated",
                run_id,
                payload["run_at"],
            )
        current_objects.append(evidence)

    current_ids = {item.evidence_id for item in current_objects}
    reviews = _load_reviews(root, payload, current_ids)
    object_map = {
        evidence_id: EvidenceRecord.from_dict(record)
        for evidence_id, record in existing_evidence.items()
    }
    object_map.update({item.evidence_id: item for item in current_objects})
    source_map = source_registry.as_map()
    combined_records = [object_map[key].to_dict() for key in sorted(object_map)]
    initial_retrieval = retrieve(
        payload["retrieval_query"],
        [item.to_dict() for item in current_objects],
        source_map,
    )

    auditor = DeterministicAuditor()
    audit = auditor.audit(combined_records, source_map)
    contradiction_path = root / "data" / "audit" / "contradictions.jsonl"
    for item in audit["contradictions"]:
        put_jsonl(contradiction_path, item, "contradiction_id", immutable=False)

    counts = _contradiction_counts(audit)
    confidence_by_id: dict[str, float] = {}
    score_records: list[dict[str, Any]] = []
    for evidence_id in sorted(object_map):
        evidence = object_map[evidence_id]
        record = evidence.to_dict()
        confidence = score_evidence(
            record,
            payload["as_of"],
            _independent_source_count(record, combined_records),
            counts.get(evidence_id, 0),
        )
        evidence.confidence = confidence
        confidence_by_id[evidence_id] = confidence["score"]
        score_records.append({"evidence_id": evidence_id, **confidence})

    graph = FileGraph(root / "data" / "graph" / "nodes.json", root / "data" / "graph" / "edges.json")
    confidence_changes = graph.set_edge_confidence(confidence_by_id) if graph.edges else []
    graph_diff = graph.update(
        payload["nodes"],
        payload["edges"],
        {key: value.to_dict() for key, value in object_map.items()},
        confidence_by_id,
    )
    graph_diff["updated_edges"] = confidence_changes

    review_outcomes: list[dict[str, Any]] = []
    for evidence in current_objects:
        if evidence.status == EvidenceStatus.CLASSIFIED.value:
            harness.transition(
                evidence,
                EvidenceStatus.LINKED.value,
                "Evidence linked to file-backed graph edges",
                run_id,
                payload["run_at"],
            )
        if evidence.status == EvidenceStatus.LINKED.value:
            harness.transition(
                evidence,
                EvidenceStatus.CONTRADICTION_CHECKED.value,
                "Semantic-boundary contradictions preserved; no automatic resolution",
                run_id,
                payload["run_at"],
            )
        if evidence.status == EvidenceStatus.CONTRADICTION_CHECKED.value:
            harness.transition(
                evidence,
                EvidenceStatus.DECISION_RELEVANT.value,
                "Decision-variable impact exists and confidence rubric was calculated",
                run_id,
                payload["run_at"],
            )
        if evidence.status == EvidenceStatus.DECISION_RELEVANT.value:
            harness.transition(
                evidence,
                EvidenceStatus.HUMAN_REVIEW.value,
                "Evidence reached the explicit per-Evidence review gate",
                run_id,
                payload["run_at"],
            )
        review = reviews.get(evidence.evidence_id)
        if review and evidence.status == EvidenceStatus.HUMAN_REVIEW.value:
            try:
                harness.apply_review(
                    evidence,
                    review,
                    blocking_findings=audit["blocking_findings"],
                    independent_source_count=_independent_source_count(
                        evidence.to_dict(), combined_records
                    ),
                    unresolved_contradiction_ids=_unresolved_contradictions(
                        evidence.evidence_id, audit
                    ),
                )
                review_outcomes.append(
                    {
                        "review_id": review.review_id,
                        "evidence_id": evidence.evidence_id,
                        "decision": review.decision,
                        "resulting_status": evidence.status,
                        "promotion_blocked": False,
                    }
                )
            except PermissionError as exc:
                review_outcomes.append(
                    {
                        "review_id": review.review_id,
                        "evidence_id": evidence.evidence_id,
                        "decision": review.decision,
                        "resulting_status": evidence.status,
                        "promotion_blocked": True,
                        "reason": str(exc),
                    }
                )
        object_map[evidence.evidence_id] = evidence

    for evidence_id in sorted(object_map):
        evidence_registry.put(object_map[evidence_id].to_dict())

    audit["review_outcomes"] = review_outcomes
    write_json(run_dir / "audit_result.json", audit)
    write_json(
        root / "data" / "signals" / "signal_update.json",
        {
            "run_id": run_id,
            "rubric": {
                "directness_weight": 0.35,
                "independence_weight": 0.20,
                "temporal_fit_weight": 0.20,
                "scope_fit_weight": 0.25,
                "contradiction_penalty_max": 0.20,
            },
            "evidence_scores": sorted(score_records, key=lambda item: item["evidence_id"]),
            "summary": summarize_scores(score_records),
        },
    )

    final_evidence_map = evidence_registry.as_map()
    graph_context = graph.neighborhood(payload["graph_seed_entity"], max_hops=2)
    graph_rag = retrieve(
        payload["retrieval_query"],
        final_evidence_map.values(),
        source_map,
        allowed_evidence_ids=set(graph_context["evidence_ids"]),
    )
    signal_summary = summarize_scores(score_records)
    memo = build_memo(
        final_evidence_map,
        source_map,
        graph_context,
        audit,
        signal_summary,
        run_id,
        payload["decision_memo"],
    )
    write_json(run_dir / "decision_memo.json", memo)
    (run_dir / "decision_memo.md").write_text(render_markdown(memo), encoding="utf-8")
    write_json(run_dir / "graph_diff.json", graph_diff)
    write_json(run_dir / "retrieval_trace.json", {"initial": initial_retrieval, "graph_aware": graph_rag})

    final_records = [final_evidence_map[key] for key in sorted(final_evidence_map)]
    write_json(run_dir / "evidence_snapshot.json", final_records)
    write_json(run_dir / "graph_snapshot.json", _edge_snapshot(graph))
    temporal_diff = _temporal_state_diff(
        root, payload, final_evidence_map, _edge_snapshot(graph)
    )
    if temporal_diff is not None:
        write_json(run_dir / "temporal_state_diff.json", temporal_diff)
        (run_dir / "temporal_state_diff.md").write_text(
            _render_temporal_diff(temporal_diff), encoding="utf-8"
        )

    _write_run_log(root, run_id, final_records)
    trace_basis = {
        "state_by_evidence": {
            evidence_id: final_evidence_map[evidence_id]["status"]
            for evidence_id in sorted(final_evidence_map)
        },
        "graph_diff": graph_diff,
        "source_trace": memo["source_evidence_trace"],
        "temporal_state_diff": temporal_diff,
    }
    result = {
        "run_id": run_id,
        "scenario_id": payload["scenario_id"],
        "core_implementation_version": CORE_IMPLEMENTATION_VERSION,
        "scenario_fingerprint": scenario_fingerprint,
        **trace_basis,
        "trace_hash": content_digest(trace_basis),
        "retrieval": {"initial": initial_retrieval, "graph_aware": graph_rag},
        "graph_context": graph_context,
        "contradiction_ids": [item["contradiction_id"] for item in audit["contradictions"]],
        "blocking_findings": audit["blocking_findings"],
        "review_outcomes": review_outcomes,
        "signal_summary": signal_summary,
        "memo": memo,
        "artifacts": {
            "decision_memo_json": f"data/runs/{run_id}/decision_memo.json",
            "decision_memo_markdown": f"data/runs/{run_id}/decision_memo.md",
            "graph_diff": f"data/runs/{run_id}/graph_diff.json",
            "retrieval_trace": f"data/runs/{run_id}/retrieval_trace.json",
            "evidence_snapshot": f"data/runs/{run_id}/evidence_snapshot.json",
            "graph_snapshot": f"data/runs/{run_id}/graph_snapshot.json",
            "temporal_state_diff": (
                f"data/runs/{run_id}/temporal_state_diff.json" if temporal_diff else None
            ),
        },
    }
    write_json(existing_result_path, result)
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the deterministic HBM4 evidence scenario")
    parser.add_argument("--workspace", default=".")
    parser.add_argument("--scenario", default="data/raw/scenarios/hbm4_vertical_slice.json")
    args = parser.parse_args()
    root = Path(args.workspace)
    scenario = Path(args.scenario)
    if not scenario.is_absolute():
        scenario = root / scenario
    result = run_vertical_slice(root, scenario)
    # Keep persisted artifacts UTF-8, but make CLI replay portable across Windows cp949 consoles.
    print(json.dumps(result, ensure_ascii=True, sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
