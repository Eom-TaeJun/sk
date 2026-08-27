from __future__ import annotations

from typing import Any


class MemoTraceError(ValueError):
    pass


def build_source_trace(
    evidence_ids: list[str],
    evidence_map: dict[str, dict[str, Any]],
    source_map: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    trace: list[dict[str, Any]] = []
    for evidence_id in sorted(set(evidence_ids)):
        if evidence_id not in evidence_map:
            raise MemoTraceError(f"missing Evidence ID: {evidence_id}")
        evidence = evidence_map[evidence_id]
        source_id = evidence["source_id"]
        if source_id not in source_map:
            raise MemoTraceError(f"missing Source ID: {source_id}")
        source = source_map[source_id]
        for field in ("excerpt", "locator"):
            if not evidence.get(field):
                raise MemoTraceError(f"{evidence_id} lacks {field}")
        trace.append(
            {
                "evidence_id": evidence_id,
                "source_id": source_id,
                "original_excerpt": evidence["excerpt"],
                "locator": evidence["locator"],
                "publication_date": source["publication_date"],
                "url": source.get("url"),
                "local_archive_path": source.get("local_archive_path"),
                "content_hash": source["content_hash"],
            }
        )
    return trace


def validate_fact_trace(memo: dict[str, Any], evidence_map: dict[str, dict[str, Any]]) -> None:
    trace_ids = {item["evidence_id"] for item in memo.get("source_evidence_trace", [])}
    if not memo.get("fact_statements"):
        raise MemoTraceError("memo must include fact_statements")
    for statement in memo["fact_statements"]:
        if not statement.get("evidence_ids"):
            raise MemoTraceError("every fact statement must include Evidence IDs")
        for evidence_id in statement["evidence_ids"]:
            if evidence_id not in evidence_map:
                raise MemoTraceError(f"fact statement references unknown Evidence ID {evidence_id}")
            if evidence_id not in trace_ids:
                raise MemoTraceError(f"fact statement Evidence ID {evidence_id} is absent from source trace")


def build_memo(
    evidence_map: dict[str, dict[str, Any]],
    source_map: dict[str, dict[str, Any]],
    graph_context: dict[str, Any],
    audit: dict[str, Any],
    signal_summary: dict[str, Any],
    run_id: str,
    memo_spec: dict[str, Any],
) -> dict[str, Any]:
    fact_statements = memo_spec["fact_statements"]
    all_evidence_ids = [
        evidence_id
        for statement in fact_statements
        for evidence_id in statement["evidence_ids"]
    ]
    trace = build_source_trace(all_evidence_ids, evidence_map, source_map)
    statuses = {evidence_map[evidence_id]["status"] for evidence_id in all_evidence_ids}
    if statuses == {"PROMOTED"}:
        review_status = "HUMAN_APPROVED"
    elif "REJECTED" in statuses:
        review_status = "CONTAINS_REJECTED_EVIDENCE"
    else:
        review_status = "PENDING_HUMAN_REVIEW"
    memo = {
        "memo_id": memo_spec["memo_id"],
        "title": memo_spec["title"],
        "run_id": run_id,
        "review_status": review_status,
        "what_changed": memo_spec["what_changed"],
        "evidence_level": memo_spec["evidence_level"],
        "why_it_matters": memo_spec["why_it_matters"],
        "demand_or_supply": memo_spec["demand_or_supply"],
        "transmission_path": graph_context["edge_ids"],
        "current_bottleneck_candidate": memo_spec["current_bottleneck_candidate"],
        "assumption_updated": memo_spec["assumption_updated"],
        "decision_variables_affected": memo_spec["decision_variables_affected"],
        "confidence": {
            **signal_summary,
            "reason": memo_spec["confidence_reason"],
        },
        "counterevidence": [item["contradiction_id"] for item in audit["contradictions"]],
        "invalidate_if": memo_spec["invalidate_if"],
        "monitor_next": memo_spec["monitor_next"],
        "still_unknown": memo_spec.get("still_unknown", []),
        "fact_statements": fact_statements,
        "source_evidence_trace": trace,
    }
    validate_fact_trace(memo, evidence_map)
    return memo


def render_markdown(memo: dict[str, Any]) -> str:
    lines = [
        f"# {memo['title']}",
        "",
        f"Run ID: `{memo['run_id']}`",
        f"Review status: `{memo['review_status']}`",
        "",
        "## 1. WHAT CHANGED?",
        memo["what_changed"],
        "",
        "## 2. EVIDENCE LEVEL",
        ", ".join(memo["evidence_level"]),
        "",
        "## 3. WHY DOES IT MATTER?",
        memo["why_it_matters"],
        "",
        "## 4. DEMAND OR SUPPLY?",
        memo["demand_or_supply"],
        "",
        "## 5. WHICH TRANSMISSION PATH CHANGED?",
        "The retrieved 2-hop transmission subgraph contains:",
        "## 6. CURRENT BOTTLENECK CANDIDATE",
        memo["current_bottleneck_candidate"],
        "",
        "## 7. WHICH ASSUMPTION CHANGED?",
        memo["assumption_updated"],
        "",
        "## 8. WHICH MARKETING DECISION VARIABLE IS AFFECTED?",
        ", ".join(memo["decision_variables_affected"]),
        "",
        "## 9. CONFIDENCE",
        f"{memo['confidence']['label']} — {memo['confidence']['reason']} This is not a probability.",
        "",
        "## 10. COUNTEREVIDENCE / OPEN CONTRADICTIONS",
    ]
    insertion_index = lines.index("## 6. CURRENT BOTTLENECK CANDIDATE")
    transmission_lines = [f"- `{item}`" for item in memo["transmission_path"]] + [""]
    lines[insertion_index:insertion_index] = transmission_lines
    lines.extend(f"- `{item}`" for item in memo["counterevidence"])
    lines.extend(["", "## 11. WHAT WOULD INVALIDATE THIS?"])
    lines.extend(f"- {item}" for item in memo["invalidate_if"])
    lines.extend(["", "## 12. WHAT TO MONITOR NEXT?"])
    lines.extend(f"- {item}" for item in memo["monitor_next"])
    lines.extend(["", "## 13. SOURCE / EVIDENCE TRACE"])
    for item in memo["source_evidence_trace"]:
        lines.append(
            f"- `{item['evidence_id']}` → `{item['source_id']}` → excerpt stored → {item['locator']} → {item['url']}"
        )
    lines.extend(["", "### Fact statements"])
    for item in memo["fact_statements"]:
        evidence = ", ".join(f"`{value}`" for value in item["evidence_ids"])
        lines.append(f"- {item['text']} [{evidence}]")
    return "\n".join(lines) + "\n"
