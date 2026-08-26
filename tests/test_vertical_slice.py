from __future__ import annotations

import copy
import json
from pathlib import Path
import shutil
import tempfile
import unittest

from src.audit.auditor import DeterministicAuditor
from src.core.harness import DeterministicHarness, HumanReviewRequired, InvalidTransition
from src.core.models import ContractError, EvidenceRecord, EvidenceStatus, SourceRecord
from src.memo.builder import validate_fact_trace
from src.pipeline import run_vertical_slice


REPO_ROOT = Path(__file__).resolve().parents[1]


class VerticalSliceTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.workspace = Path(self.tempdir.name)
        for relative in (
            Path("data/raw/scenarios/hbm4_vertical_slice.json"),
            Path("data/raw/sources/SRC-SKH-20250319-HBM4-SAMPLE.md"),
        ):
            target = self.workspace / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(REPO_ROOT / relative, target)
        self.scenario_path = self.workspace / "data/raw/scenarios/hbm4_vertical_slice.json"

    def tearDown(self) -> None:
        self.tempdir.cleanup()

    def run_once(self) -> dict:
        return run_vertical_slice(self.workspace, self.scenario_path)

    def test_missing_provenance_rejection(self) -> None:
        scenario = json.loads(self.scenario_path.read_text(encoding="utf-8"))
        scenario["source"]["locator"] = ""
        with self.assertRaises(ContractError):
            SourceRecord.from_dict(scenario["source"])

    def test_invalid_state_transition(self) -> None:
        scenario = json.loads(self.scenario_path.read_text(encoding="utf-8"))
        source = SourceRecord.from_dict(scenario["source"])
        evidence = EvidenceRecord.from_spec(
            scenario["evidence"][0], source, scenario["run_id"], scenario["run_at"], "test"
        )
        with self.assertRaises(InvalidTransition):
            DeterministicHarness().transition(
                evidence,
                EvidenceStatus.LINKED.value,
                "skip required states",
                scenario["run_id"],
                scenario["run_at"],
            )

    def test_duplicate_evidence_idempotency(self) -> None:
        first = self.run_once()
        second = self.run_once()
        self.assertEqual(first, second)
        evidence_lines = (self.workspace / "data/evidence/atomic_evidence.jsonl").read_text(
            encoding="utf-8"
        ).strip().splitlines()
        self.assertEqual(4, len(evidence_lines))

    def test_retrieval_source_trace(self) -> None:
        result = self.run_once()
        required = {"evidence_id", "source_id", "excerpt", "locator", "date", "evidence_level"}
        self.assertTrue(result["retrieval"]["initial"])
        for item in result["retrieval"]["initial"]:
            self.assertTrue(required.issubset(item))

    def test_graph_edge_trace_uses_evidence_ids(self) -> None:
        self.run_once()
        edges = json.loads((self.workspace / "data/graph/edges.json").read_text(encoding="utf-8"))
        self.assertTrue(edges)
        for edge in edges:
            self.assertTrue(edge["evidence_ids"])
            self.assertNotIn("source_id", edge)

    def test_contradiction_preservation(self) -> None:
        result = self.run_once()
        self.assertEqual(
            {
                "CONTRA-FIRST-IS-NOT-COMMERCIAL-LEADERSHIP",
                "CONTRA-QUALIFICATION-IS-NOT-VOLUME",
                "CONTRA-SAMPLE-IS-NOT-QUALIFICATION",
            },
            set(result["contradiction_ids"]),
        )
        records = [
            json.loads(line)
            for line in (self.workspace / "data/audit/contradictions.jsonl").read_text(
                encoding="utf-8"
            ).splitlines()
        ]
        self.assertTrue(all(not item["auto_resolved"] for item in records))

    def test_unsupported_inference_detection(self) -> None:
        scenario = json.loads(self.scenario_path.read_text(encoding="utf-8"))
        source = SourceRecord.from_dict(scenario["source"])
        spec = copy.deepcopy(scenario["evidence"][0])
        spec["evidence_id"] = "EVD-UNSUPPORTED-INFERENCE"
        spec["evidence_level"] = "E_STRONG_INFERENCE"
        spec["claim"] = "Uncorroborated commercial leadership inference"
        evidence = EvidenceRecord.from_spec(spec, source, scenario["run_id"], scenario["run_at"], "test")
        audit = DeterministicAuditor().audit([evidence.to_dict()], {source.source_id: source.to_dict()})
        self.assertIn("UNSUPPORTED_INFERENCE", {item["code"] for item in audit["blocking_findings"]})

    def test_human_gate_for_strong_inference(self) -> None:
        scenario = json.loads(self.scenario_path.read_text(encoding="utf-8"))
        source = SourceRecord.from_dict(scenario["source"])
        spec = copy.deepcopy(scenario["evidence"][0])
        spec["evidence_level"] = "E_STRONG_INFERENCE"
        evidence = EvidenceRecord.from_spec(spec, source, scenario["run_id"], scenario["run_at"], "test")
        evidence.status = EvidenceStatus.HUMAN_REVIEW.value
        with self.assertRaises(HumanReviewRequired):
            DeterministicHarness().transition(
                evidence,
                EvidenceStatus.PROMOTED.value,
                "attempt automatic promotion",
                scenario["run_id"],
                scenario["run_at"],
                human_approved=False,
            )

    def test_unreviewed_run_stops_at_human_review(self) -> None:
        result = self.run_once()
        self.assertEqual(
            {EvidenceStatus.HUMAN_REVIEW.value},
            set(result["state_by_evidence"].values()),
        )
        self.assertEqual("PENDING_HUMAN_REVIEW", result["memo"]["review_status"])

    def test_every_memo_fact_has_evidence_trace(self) -> None:
        result = self.run_once()
        evidence_map = {
            item["evidence_id"]: item
            for item in (
                json.loads(line)
                for line in (self.workspace / "data/evidence/atomic_evidence.jsonl").read_text(
                    encoding="utf-8"
                ).splitlines()
            )
        }
        validate_fact_trace(result["memo"], evidence_map)
        self.assertTrue(all(item["evidence_ids"] for item in result["memo"]["fact_statements"]))

    def test_replay_is_deterministic(self) -> None:
        first = self.run_once()
        second = self.run_once()
        self.assertEqual(first["state_by_evidence"], second["state_by_evidence"])
        self.assertEqual(first["graph_diff"], second["graph_diff"])
        self.assertEqual(first["source_trace"], second["source_trace"])
        self.assertEqual(first["trace_hash"], second["trace_hash"])


if __name__ == "__main__":
    unittest.main()
