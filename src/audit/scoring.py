from __future__ import annotations

from datetime import date
from typing import Any


DIRECTNESS = {
    "A_DIRECT_FACT": 0.90,
    "B_COMPANY_CLAIM": 0.65,
    "C_EXTERNAL_ESTIMATE": 0.55,
    "D_DERIVED_FACT": 0.80,
    "E_STRONG_INFERENCE": 0.60,
    "F_HYPOTHESIS": 0.30,
}


def score_evidence(
    evidence: dict[str, Any],
    as_of: str,
    independent_source_count: int,
    contradiction_count: int,
) -> dict[str, Any]:
    days = max(
        0,
        (date.fromisoformat(as_of) - date.fromisoformat(evidence["publication_date"])).days,
    )
    if days <= 180:
        temporal_fit = 1.0
    elif days <= 540:
        temporal_fit = 0.75
    else:
        temporal_fit = 0.50
    factors = {
        "directness": DIRECTNESS[evidence["evidence_level"]],
        "independence": min(1.0, independent_source_count / 2.0),
        "temporal_fit": temporal_fit,
        "scope_fit": 1.0 if evidence.get("entities") and evidence.get("decision_variables") else 0.5,
        "contradiction_penalty": min(1.0, contradiction_count * 0.25),
    }
    score = (
        0.35 * factors["directness"]
        + 0.20 * factors["independence"]
        + 0.20 * factors["temporal_fit"]
        + 0.25 * factors["scope_fit"]
        - 0.20 * factors["contradiction_penalty"]
    )
    score = round(max(0.0, min(1.0, score)), 4)
    label = "HIGH" if score >= 0.75 else "MEDIUM" if score >= 0.50 else "LOW"
    return {
        "score": score,
        "label": label,
        "factors": factors,
        "interpretation": "Rubric score for evidence handling; not a probability.",
    }


def summarize_scores(scores: list[dict[str, Any]]) -> dict[str, Any]:
    value = round(sum(item["score"] for item in scores) / len(scores), 4)
    label = "HIGH" if value >= 0.75 else "MEDIUM" if value >= 0.50 else "LOW"
    return {
        "score": value,
        "label": label,
        "interpretation": "Average deterministic rubric score; not a probability.",
    }
