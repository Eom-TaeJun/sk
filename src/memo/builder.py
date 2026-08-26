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
) -> dict[str, Any]:
    fact_statements = [
        {
            "text": "SK hynix reported delivery of 12-layer HBM4 samples to major customers.",
            "evidence_ids": ["EVD-HBM4-SAMPLE-SHIPMENT"],
        },
        {
            "text": "The announcement described customer certification as a next process rather than completed qualification.",
            "evidence_ids": ["EVD-HBM4-CERTIFICATION-PENDING"],
        },
        {
            "text": "The announcement stated a target to complete mass-production preparations in the second half of 2025.",
            "evidence_ids": ["EVD-HBM4-MASS-PRODUCTION-TARGET"],
        },
        {
            "text": "The publisher presented the sample provision as first in the world.",
            "evidence_ids": ["EVD-HBM4-INDUSTRY-FIRST-CLAIM"],
        },
    ]
    all_evidence_ids = [
        evidence_id
        for statement in fact_statements
        for evidence_id in statement["evidence_ids"]
    ]
    trace = build_source_trace(all_evidence_ids, evidence_map, source_map)
    memo = {
        "memo_id": "MEMO-HBM4-VS-001",
        "run_id": run_id,
        "review_status": "PENDING_HUMAN_REVIEW",
        "what_changed": "HBM4 moved to customer sample delivery, while customer certification and mass-production preparation remained subsequent gates.",
        "evidence_level": ["A_DIRECT_FACT", "B_COMPANY_CLAIM"],
        "why_it_matters": "The event improves visibility into qualification and TTM work, but does not establish qualified demand, committed volume, or commercial shipment.",
        "demand_or_supply": "BOTH",
        "transmission_path": graph_context["edge_ids"],
        "current_bottleneck_candidate": "CUSTOMER_QUALIFICATION",
        "assumption_updated": "Sample shipment must not be treated as completed qualification or confirmed commercial volume; an industry-first claim must not be treated as commercial leadership.",
        "decision_variables_affected": ["CUSTOMER_PRIORITY", "DEMAND_FORECAST", "QUALIFICATION", "SUPPLY_RISK", "TTM"],
        "confidence": {
            **signal_summary,
            "reason": "One first-party source directly distinguishes samples from a pending certification step, but provides no independent confirmation or commercial volume.",
        },
        "counterevidence": [item["contradiction_id"] for item in audit["contradictions"]],
        "invalidate_if": [
            "A dated official record shows qualification was already complete at the sample-announcement date.",
            "A customer or shipment record demonstrates that the announced samples were already commercial volume.",
        ],
        "monitor_next": [
            "Customer qualification completion or approved-vendor status",
            "Design-in or platform-specific adoption",
            "Commercial shipment and committed price/volume",
            "Mass-production ramp and qualified good-volume evidence",
        ],
        "fact_statements": fact_statements,
        "source_evidence_trace": trace,
    }
    validate_fact_trace(memo, evidence_map)
    return memo


def render_markdown(memo: dict[str, Any]) -> str:
    lines = [
        "# Draft Decision Memo — HBM4 Sample to Qualification Gate",
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
