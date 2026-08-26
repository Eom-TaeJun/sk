from __future__ import annotations

from typing import Any


MISCONCEPTION_RULES = {
    "SAMPLE_SHIPMENT": {
        "contradiction_id": "CONTRA-SAMPLE-IS-NOT-QUALIFICATION",
        "misconception": "sample = qualification",
        "finding": "A sample shipment does not establish completed customer qualification.",
    },
    "QUALIFICATION_PENDING": {
        "contradiction_id": "CONTRA-QUALIFICATION-IS-NOT-VOLUME",
        "misconception": "qualification = confirmed volume",
        "finding": "Qualification status alone does not establish contracted or confirmed volume.",
    },
    "INDUSTRY_FIRST_CLAIM": {
        "contradiction_id": "CONTRA-FIRST-IS-NOT-COMMERCIAL-LEADERSHIP",
        "misconception": "industry-first = commercial leadership",
        "finding": "An industry-first claim does not establish qualified commercial leadership.",
    },
}


class DeterministicAuditor:
    def audit(
        self,
        evidence_records: list[dict[str, Any]],
        source_map: dict[str, dict[str, Any]],
    ) -> dict[str, Any]:
        contradictions: dict[str, dict[str, Any]] = {}
        blocking_findings: list[dict[str, Any]] = []
        for evidence in evidence_records:
            for field in ("source_id", "excerpt", "locator", "evidence_level", "publication_date"):
                if not evidence.get(field):
                    blocking_findings.append(
                        {
                            "code": "MISSING_PROVENANCE",
                            "evidence_id": evidence.get("evidence_id"),
                            "field": field,
                        }
                    )
            if evidence.get("source_id") not in source_map:
                blocking_findings.append(
                    {
                        "code": "UNKNOWN_SOURCE",
                        "evidence_id": evidence.get("evidence_id"),
                    }
                )
            rule = MISCONCEPTION_RULES.get(evidence.get("event_type"))
            if rule:
                contradiction_id = rule["contradiction_id"]
                record = contradictions.setdefault(
                    contradiction_id,
                    {
                        **rule,
                        "issue_type": "SEMANTIC_BOUNDARY",
                        "trigger_evidence_ids": [],
                        "counterevidence_ids": [],
                        "status": "OPEN",
                        "auto_resolved": False,
                    },
                )
                record["trigger_evidence_ids"].append(evidence["evidence_id"])

            if evidence.get("evidence_level") in {"E_STRONG_INFERENCE", "F_HYPOTHESIS"}:
                unique_sources = {
                    item["source_id"]
                    for item in evidence_records
                    if item.get("claim") == evidence.get("claim") and item.get("source_id")
                }
                if len(unique_sources) < 2:
                    blocking_findings.append(
                        {
                            "code": "UNSUPPORTED_INFERENCE",
                            "evidence_id": evidence["evidence_id"],
                            "detail": "Strong inference or hypothesis lacks two independent sources.",
                        }
                    )

        normalized = []
        for contradiction_id in sorted(contradictions):
            record = contradictions[contradiction_id]
            record["trigger_evidence_ids"] = sorted(set(record["trigger_evidence_ids"]))
            normalized.append(record)
        blocking_findings.sort(key=lambda item: (item["code"], item.get("evidence_id") or ""))
        return {"contradictions": normalized, "blocking_findings": blocking_findings}
