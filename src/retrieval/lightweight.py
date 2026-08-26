from __future__ import annotations

import re
from typing import Any, Iterable


TOKEN_RE = re.compile(r"[0-9A-Za-z가-힣]+")


def tokenize(text: str) -> set[str]:
    return {token.lower() for token in TOKEN_RE.findall(text)}


def retrieve(
    query: str,
    evidence_records: Iterable[dict[str, Any]],
    source_map: dict[str, dict[str, Any]],
    *,
    allowed_evidence_ids: set[str] | None = None,
    limit: int = 10,
) -> list[dict[str, Any]]:
    query_tokens = tokenize(query)
    results: list[dict[str, Any]] = []
    for evidence in evidence_records:
        if allowed_evidence_ids is not None and evidence["evidence_id"] not in allowed_evidence_ids:
            continue
        source = source_map[evidence["source_id"]]
        candidate_tokens = tokenize(
            " ".join(
                [
                    evidence.get("claim", ""),
                    evidence.get("excerpt", ""),
                    evidence.get("event_type", ""),
                    " ".join(evidence.get("entities", [])),
                ]
            )
        )
        overlap = len(query_tokens & candidate_tokens)
        if overlap == 0:
            continue
        results.append(
            {
                "evidence_id": evidence["evidence_id"],
                "source_id": evidence["source_id"],
                "excerpt": evidence["excerpt"],
                "locator": evidence["locator"],
                "date": source["publication_date"],
                "evidence_level": evidence["evidence_level"],
                "score": overlap,
            }
        )
    results.sort(key=lambda item: (-item["score"], item["evidence_id"]))
    return results[:limit]
