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
from src.core.models import EvidenceRecord, EvidenceStatus, SourceRecord
from src.core.storage import (
    EvidenceRegistry,
    SourceRegistry,
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


CORE_IMPLEMENTATION_VERSION = "1.0.0"


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def _contradiction_counts(audit: dict[str, Any]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for item in audit["contradictions"]:
        for evidence_id in item["trigger_evidence_ids"]:
            counts[evidence_id] = counts.get(evidence_id, 0) + 1
    return counts


def _write_run_log(root: Path, run_id: str, evidence_records: list[dict[str, Any]]) -> None:
    path = root / "logs" / f"{run_id}.jsonl"
    if path.exists():
        path.unlink()
    for evidence in sorted(evidence_records, key=lambda item: item["evidence_id"]):
        for transition in evidence["transitions"]:
            put_jsonl(
                path,
                {
                    "log_id": f"{evidence['evidence_id']}::{transition['to_status']}",
                    "evidence_id": evidence["evidence_id"],
                    **transition,
                },
                "log_id",
                immutable=True,
            )


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

    harness = DeterministicHarness()
    evidence_objects: list[EvidenceRecord] = []
    for spec in payload["evidence"]:
        evidence = EvidenceRecord.from_spec(
            spec,
            source,
            run_id,
            payload["run_at"],
            actor="manual-scenario-adapter",
        )
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
        evidence_registry.put(evidence.to_dict())
        evidence_objects.append(evidence)

    source_map = source_registry.as_map()
    classified_records = [item.to_dict() for item in evidence_objects]
    initial_retrieval = retrieve(payload["retrieval_query"], classified_records, source_map)

    provisional_confidence = {item.evidence_id: 0.0 for item in evidence_objects}
    provisional_evidence_map = {item.evidence_id: item.to_dict() for item in evidence_objects}
    graph = FileGraph(root / "data" / "graph" / "nodes.json", root / "data" / "graph" / "edges.json")
    graph_diff = graph.update(
        payload["nodes"],
        payload["edges"],
        provisional_evidence_map,
        provisional_confidence,
    )
    for evidence in evidence_objects:
        harness.transition(
            evidence,
            EvidenceStatus.LINKED.value,
            "Evidence linked to file-backed graph edges",
            run_id,
            payload["run_at"],
        )

    auditor = DeterministicAuditor()
    audit = auditor.audit([item.to_dict() for item in evidence_objects], source_map)
    contradiction_path = root / "data" / "audit" / "contradictions.jsonl"
    for item in audit["contradictions"]:
        put_jsonl(contradiction_path, item, "contradiction_id", immutable=True)
    write_json(run_dir / "audit_result.json", audit)
    for evidence in evidence_objects:
        harness.transition(
            evidence,
            EvidenceStatus.CONTRADICTION_CHECKED.value,
            "Semantic-boundary contradictions preserved; no automatic resolution",
            run_id,
            payload["run_at"],
        )

    counts = _contradiction_counts(audit)
    unique_source_count = len({item.source_id for item in evidence_objects})
    confidence_by_id: dict[str, float] = {}
    score_records: list[dict[str, Any]] = []
    for evidence in evidence_objects:
        confidence = score_evidence(
            evidence.to_dict(),
            payload["as_of"],
            unique_source_count,
            counts.get(evidence.evidence_id, 0),
        )
        evidence.confidence = confidence
        confidence_by_id[evidence.evidence_id] = confidence["score"]
        score_records.append({"evidence_id": evidence.evidence_id, **confidence})
        harness.transition(
            evidence,
            EvidenceStatus.DECISION_RELEVANT.value,
            "Decision-variable impact exists and confidence rubric was calculated",
            run_id,
            payload["run_at"],
        )
        harness.transition(
            evidence,
            EvidenceStatus.HUMAN_REVIEW.value,
            "Evidence reached the explicit review gate",
            run_id,
            payload["run_at"],
        )
        if payload.get("human_approved", False):
            harness.transition(
                evidence,
                EvidenceStatus.PROMOTED.value,
                "Human reviewer approved promotion at the declared evidence level",
                run_id,
                payload["run_at"],
                human_approved=True,
            )
        evidence_registry.put(evidence.to_dict())

    graph.set_edge_confidence(confidence_by_id)
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
    memo = build_memo(final_evidence_map, source_map, graph_context, audit, signal_summary, run_id)
    write_json(run_dir / "decision_memo.json", memo)
    (run_dir / "decision_memo.md").write_text(render_markdown(memo), encoding="utf-8")
    write_json(run_dir / "graph_diff.json", graph_diff)
    write_json(run_dir / "retrieval_trace.json", {"initial": initial_retrieval, "graph_aware": graph_rag})

    final_records = [final_evidence_map[key] for key in sorted(final_evidence_map)]
    _write_run_log(root, run_id, final_records)
    trace_basis = {
        "state_by_evidence": {
            evidence_id: final_evidence_map[evidence_id]["status"] for evidence_id in sorted(final_evidence_map)
        },
        "graph_diff": graph_diff,
        "source_trace": memo["source_evidence_trace"],
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
        "signal_summary": signal_summary,
        "memo": memo,
        "artifacts": {
            "decision_memo_json": f"data/runs/{run_id}/decision_memo.json",
            "decision_memo_markdown": f"data/runs/{run_id}/decision_memo.md",
            "graph_diff": f"data/runs/{run_id}/graph_diff.json",
            "retrieval_trace": f"data/runs/{run_id}/retrieval_trace.json",
        },
    }
    write_json(existing_result_path, result)
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the deterministic HBM4 vertical slice")
    parser.add_argument("--workspace", default=".")
    parser.add_argument("--scenario", default="data/raw/scenarios/hbm4_vertical_slice.json")
    args = parser.parse_args()
    root = Path(args.workspace)
    scenario = Path(args.scenario)
    if not scenario.is_absolute():
        scenario = root / scenario
    result = run_vertical_slice(root, scenario)
    print(json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
