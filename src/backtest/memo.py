from __future__ import annotations

from typing import Any


def validate_memo_trace(memo: dict[str, Any], event_map: dict[str, dict[str, Any]]) -> None:
    for statement in memo.get("fact_statements", []):
        event_ids = statement.get("event_ids", [])
        if not event_ids:
            raise ValueError(f"memo fact has no Event ID: {statement.get('text')}")
        missing = [event_id for event_id in event_ids if event_id not in event_map]
        if missing:
            raise ValueError(f"memo fact references unknown Event IDs: {missing}")


def build_h1_memo(result: dict[str, Any]) -> dict[str, Any]:
    evaluated = {item["event_id"]: item for item in result["evaluated_events_primary"]}
    matched_count = result["h1_verdict"]["fully_observed_matched_track_count"]
    verdict = result["h1_verdict"]["verdict"]
    facts = [
        {
            "text": "Microsoft's FY2022 datacenter investment evidence was followed by a broad memory downturn and only later by supplier recovery.",
            "event_ids": ["EVT-C1-MSFT-CAPEX", "EVT-C1-DRAM-DOWNTURN", "EVT-C1-MEMORY-RECOVERY"],
        },
        {
            "text": "Micron's final-stage HBM3E qualification disclosure preceded its volume-production announcement by less than 90 days.",
            "event_ids": ["EVT-C2-MU-HBM3E-QUAL-FINAL", "EVT-C2-MU-HBM3E-VOLUME"],
        },
        {
            "text": "SK hynix HBM3E sample evaluation preceded reported volume production and customer supply by more than 90 days.",
            "event_ids": ["EVT-C2-SKH-HBM3E-SAMPLE", "EVT-C2-SKH-HBM3E-VOLUME"],
        },
        {
            "text": "Microsoft reported power and space constraints after large cloud/AI CAPEX, then later reported powered/chipped readiness and deployed capacity.",
            "event_ids": ["EVT-C3-MSFT-CAPEX", "EVT-C3-MSFT-POWER-SPACE-SHORT", "EVT-C3-MSFT-POWER-READY", "EVT-C3-MSFT-CAPACITY-ONLINE"],
        },
        {
            "text": "The 2025 HBM4 sample signal was followed by a supply commitment and a 2026 mass-shipment event, while the newly disclosed LTA remains right-censored.",
            "event_ids": ["EVT-C4-SKH-HBM4-SAMPLE", "EVT-C4-SKH-HBM4-SUPPLY-COMMITMENT", "EVT-C4-SKH-LTA", "EVT-C4-SKH-HBM4-SHIPMENT"],
        },
        {
            "text": f"Only {matched_count} fully observed track contains both CAPEX and an order-proximate predictor, so the deterministic H1 verdict is {verdict}.",
            "event_ids": ["EVT-C3-MSFT-CAPEX", "EVT-C3-MSFT-POWER-READY", "EVT-C3-MSFT-CAPACITY-ONLINE"],
        },
    ]
    memo = {
        "memo_id": "MEMO-H1-DEMAND-SIGNAL-QUALITY-001",
        "run_id": result["run_id"],
        "title": "H1 Decision Memo — Demand Signal Quality Historical Backtest",
        "question": result["question"],
        "verdict": verdict,
        "verdict_reason": result["h1_verdict"]["reason"],
        "case_results": result["case_results"],
        "signal_comparison": result["signal_summary_primary"],
        "matched_track_comparison": result["h1_verdict"]["matched_tracks"],
        "sensitivity_summary": result["sensitivity_summary"],
        "marketing_decision_implications": {
            "CAPEX": "WATCH: update long-range direction, but do not confirm customer volume or memory CAPA from spend alone.",
            "SAMPLE": "PREPARE: update qualification schedule, target specification, and technical-response priority.",
            "QUALIFICATION": "PREPARE: raise customer priority and TTM readiness, without treating it as contracted volume.",
            "SUPPLY_COMMITMENT_OR_LTA": "COMMIT_CANDIDATE only after scope and human review; use for price-volume and CAPA reservation scenarios, not disclosed allocation percentages.",
            "POWER_READY": "COMMIT_CANDIDATE when operational readiness is source-backed; update deployment timing and regional supply risk.",
            "SHIPMENT": "CONFIRMED for commercialization timing and forecast-bias review; shipment is not a predictor in this comparison.",
        },
        "known_unknowns": [
            "Customer-specific memory order quantities across the four cases",
            "HBM contract prices and allocation percentages",
            "Memory content per deployed Microsoft AI-capacity unit",
            "Forward realization of the July 2026 LTA inside a completed 12-month window",
            "A second fully observed track containing both CAPEX and an order-proximate signal",
        ],
        "counterevidence": [
            "C3 CAPEX was followed by deployed capacity inside 12 months and provided longer lead than the later power-ready statement.",
            "Micron final-stage qualification provided less than 90 days of lead to volume production.",
            "The C1 relationship is broad and cannot attribute supplier recovery to one CSP's spend.",
        ],
        "invalidation_conditions": [
            "A second independently sourced matched track shows CAPEX equal or superior on both false positives and useful lead.",
            "A primary source correction changes any sample, qualification, LTA, capacity, or shipment stage used here.",
            "Additional event-time data changes the number of fully observed matched tracks or right-censor status.",
        ],
        "fact_statements": facts,
        "source_event_trace": result["source_event_trace"],
        "methodology_note": "Small descriptive backtest; internal rubric values are not probabilities and no predictive-accuracy or statistical-significance claim is made.",
    }
    validate_memo_trace(memo, evaluated)
    return memo


def render_h1_memo(memo: dict[str, Any]) -> str:
    lines = [
        f"# {memo['title']}",
        "",
        f"- Run: `{memo['run_id']}`",
        f"- Verdict: **{memo['verdict']}**",
        f"- Question: {memo['question']}",
        "",
        "## Direct Answer",
        "",
        memo["verdict_reason"],
        "",
        "## Evidence-backed Findings",
        "",
    ]
    for item in memo["fact_statements"]:
        trace = ", ".join(f"`{event_id}`" for event_id in item["event_ids"])
        lines.append(f"- {item['text']} ({trace})")
    lines.extend(["", "## Marketing Decision Implications", ""])
    for name, text in memo["marketing_decision_implications"].items():
        lines.append(f"- **{name}:** {text}")
    lines.extend(["", "## Counterevidence", ""])
    lines.extend(f"- {item}" for item in memo["counterevidence"])
    lines.extend(["", "## Known Unknowns", ""])
    lines.extend(f"- {item}" for item in memo["known_unknowns"])
    lines.extend(["", "## Invalidation Conditions", ""])
    lines.extend(f"- {item}" for item in memo["invalidation_conditions"])
    lines.extend(["", "## Source / Event Trace", ""])
    for item in memo["source_event_trace"]:
        lines.append(
            f"- `{item['event_id']}` → `{item['source_id']}` → {item['locator']} → {item['url']} → `{item['content_hash']}`"
        )
    lines.extend(["", f"_Methodology: {memo['methodology_note']}_", ""])
    return "\n".join(lines)
