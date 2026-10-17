from __future__ import annotations

import copy
import json
from pathlib import Path
import shutil
import tempfile
import unittest

from src.audit.auditor import DeterministicAuditor
from src.core.harness import (
    DeterministicHarness,
    HumanReviewRequired,
    IndependentSupportRequired,
    InvalidTransition,
    PromotionProhibited,
)
from src.core.models import (
    ContractError,
    EvidenceRecord,
    EvidenceStatus,
    ReviewRecord,
    SourceRecord,
)
from src.memo.builder import validate_fact_trace
from src.pipeline import ReviewManifestError, SourceHashMismatch, run_vertical_slice


REPO_ROOT = Path(__file__).resolve().parents[1]
BASELINE_SCENARIO = Path("data/raw/scenarios/hbm4_vertical_slice.json")
UPDATE_SCENARIO = Path("data/raw/scenarios/hbm4_temporal_update_2026.json")


class VerticalSliceTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.workspace = Path(self.tempdir.name)
        for relative in (
            BASELINE_SCENARIO,
            UPDATE_SCENARIO,
            Path("data/raw/sources/SRC-SKH-20250319-HBM4-SAMPLE.md"),
            Path("data/raw/sources/SRC-SKH-20260729-HBM4-MASS-SHIPMENT.md"),
            Path("data/reviews/hbm4_review_manifest.jsonl"),
        ):
            target = self.workspace / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(REPO_ROOT / relative, target)
        self.baseline_path = self.workspace / BASELINE_SCENARIO
        self.update_path = self.workspace / UPDATE_SCENARIO

    def tearDown(self) -> None:
        self.tempdir.cleanup()

    def run_baseline(self) -> dict:
        return run_vertical_slice(self.workspace, self.baseline_path)

    def run_sequence(self) -> tuple[dict, dict]:
        return self.run_baseline(), run_vertical_slice(self.workspace, self.update_path)

    def scenario_source_evidence(self, level: str = "A_DIRECT_FACT") -> EvidenceRecord:
        scenario = json.loads(self.baseline_path.read_text(encoding="utf-8"))
        source = SourceRecord.from_dict(scenario["source"])
        spec = copy.deepcopy(scenario["evidence"][0])
        spec["evidence_level"] = level
        evidence = EvidenceRecord.from_spec(
            spec, source, scenario["run_id"], scenario["run_at"], "test"
        )
        evidence.status = EvidenceStatus.HUMAN_REVIEW.value
        return evidence

    def review(self, evidence: EvidenceRecord, decision: str = "APPROVE") -> ReviewRecord:
        return ReviewRecord.from_dict(
            {
                "review_id": f"REV-{evidence.evidence_id}-{decision}",
                "evidence_id": evidence.evidence_id,
                "reviewer": "test-reviewer",
                "decision": decision,
                "approved_evidence_level": evidence.evidence_level,
                "reason": "deterministic unit-test review",
                "reviewed_at": "2026-08-26T09:00:00+09:00",
                "run_id": "RUN-TEST-REVIEW",
            }
        )

    def test_missing_provenance_rejection(self) -> None:
        scenario = json.loads(self.baseline_path.read_text(encoding="utf-8"))
        scenario["source"]["locator"] = ""
        with self.assertRaises(ContractError):
            SourceRecord.from_dict(scenario["source"])

    def test_invalid_state_transition(self) -> None:
        scenario = json.loads(self.baseline_path.read_text(encoding="utf-8"))
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
        first = self.run_baseline()
        second = self.run_baseline()
        self.assertEqual(first, second)
        evidence_lines = (self.workspace / "data/evidence/atomic_evidence.jsonl").read_text(
            encoding="utf-8"
        ).strip().splitlines()
        self.assertEqual(4, len(evidence_lines))

    def test_global_approval_flag_rejected_before_cached_replay(self) -> None:
        result = self.run_baseline()
        result_path = self.workspace / "data/runs" / result["run_id"] / "run_result.json"
        evidence_path = self.workspace / "data/evidence/atomic_evidence.jsonl"
        before_result = result_path.read_bytes()
        before_evidence = evidence_path.read_bytes()
        scenario = json.loads(self.baseline_path.read_text(encoding="utf-8"))
        for value in (True, False):
            with self.subTest(human_approved=value):
                scenario["human_approved"] = value
                self.baseline_path.write_text(json.dumps(scenario), encoding="utf-8")
                with self.assertRaisesRegex(ValueError, "global human_approved is prohibited"):
                    self.run_baseline()
                self.assertEqual(before_result, result_path.read_bytes())
                self.assertEqual(before_evidence, evidence_path.read_bytes())

    def test_cached_replay_rejects_changed_source_and_preserves_approval(self) -> None:
        first = self.run_baseline()
        self.assertEqual(first["memo"]["review_status"], "HUMAN_APPROVED")
        result_path = self.workspace / "data/runs" / first["run_id"] / "run_result.json"
        evidence_path = self.workspace / "data/evidence/atomic_evidence.jsonl"
        before_result = result_path.read_bytes()
        before_evidence = evidence_path.read_bytes()
        scenario = json.loads(self.baseline_path.read_text(encoding="utf-8"))
        archive = self.workspace / scenario["source"]["local_archive_path"]
        original = archive.read_bytes()
        archive.write_bytes(original + b"\nSynthetic changed source for replay test.\n")

        with self.assertRaises(SourceHashMismatch):
            self.run_baseline()

        self.assertEqual(result_path.read_bytes(), before_result)
        self.assertEqual(evidence_path.read_bytes(), before_evidence)
        archive.write_bytes(original)
        self.assertEqual(self.run_baseline(), first)

    def test_cached_temporal_replay_checks_prior_source_dependency(self) -> None:
        _, update = self.run_sequence()
        scenario = json.loads(self.baseline_path.read_text(encoding="utf-8"))
        archive = self.workspace / scenario["source"]["local_archive_path"]
        archive.write_bytes(archive.read_bytes() + b"\nSynthetic changed prior source.\n")
        result_path = self.workspace / "data/runs" / update["run_id"] / "run_result.json"
        before_result = result_path.read_bytes()

        with self.assertRaises(SourceHashMismatch):
            run_vertical_slice(self.workspace, self.update_path)

        self.assertEqual(result_path.read_bytes(), before_result)

    def workspace_bytes(self) -> dict[str, bytes]:
        return {
            path.relative_to(self.workspace).as_posix(): path.read_bytes()
            for path in self.workspace.rglob("*")
            if path.is_file()
        }

    def test_changed_cached_approval_rejects_without_overwriting_history(self) -> None:
        first = self.run_baseline()
        scenario = json.loads(self.baseline_path.read_text(encoding="utf-8"))
        manifest = self.workspace / scenario["review_manifest_path"]
        reviews = [json.loads(line) for line in manifest.read_text(encoding="utf-8").splitlines()]
        for review in reviews:
            if review["run_id"] == first["run_id"]:
                review["decision"] = "REJECT"
        manifest.write_text("\n".join(json.dumps(item) for item in reviews) + "\n", encoding="utf-8")
        before = self.workspace_bytes()

        with self.assertRaisesRegex(ReviewManifestError, "review manifest changed.*new run_id"):
            self.run_baseline()

        self.assertEqual(before, self.workspace_bytes())

    def test_approval_added_to_pending_cached_run_requires_a_new_run(self) -> None:
        scenario = json.loads(self.baseline_path.read_text(encoding="utf-8"))
        manifest = self.workspace / scenario["review_manifest_path"]
        original = manifest.read_bytes()
        reviews = [json.loads(line) for line in original.decode("utf-8").splitlines()]
        unrelated = [item for item in reviews if item["run_id"] != scenario["run_id"]]
        manifest.write_text("\n".join(json.dumps(item) for item in unrelated) + "\n", encoding="utf-8")
        pending = self.run_baseline()
        self.assertEqual(pending["memo"]["review_status"], "PENDING_HUMAN_REVIEW")
        manifest.write_bytes(original)
        before = self.workspace_bytes()

        with self.assertRaisesRegex(ReviewManifestError, "review manifest changed.*new run_id"):
            self.run_baseline()

        self.assertEqual(before, self.workspace_bytes())
        # A separate run may apply the new approval, preserving the pending run.
        scenario["run_id"] += "-REVIEWED"
        for review in reviews:
            if review["run_id"] == pending["run_id"]:
                review["run_id"] = scenario["run_id"]
                review["review_id"] += "-REVIEWED"
        manifest.write_text("\n".join(json.dumps(item) for item in reviews) + "\n", encoding="utf-8")
        reviewed_path = self.workspace / "reviewed_scenario.json"
        reviewed_path.write_text(json.dumps(scenario), encoding="utf-8")
        reviewed = run_vertical_slice(self.workspace, reviewed_path)
        self.assertEqual(reviewed["memo"]["review_status"], "HUMAN_APPROVED")
        historical = self.workspace / "data/runs" / pending["run_id"] / "run_result.json"
        self.assertEqual(json.loads(historical.read_text(encoding="utf-8")), pending)

    def test_cached_run_rejects_missing_review_manifest(self) -> None:
        self.run_baseline()
        scenario = json.loads(self.baseline_path.read_text(encoding="utf-8"))
        (self.workspace / scenario["review_manifest_path"]).unlink()
        before = self.workspace_bytes()

        with self.assertRaisesRegex(ReviewManifestError, "review manifest changed"):
            self.run_baseline()

        self.assertEqual(before, self.workspace_bytes())

    def test_legacy_cached_run_is_preserved_without_inventing_review_identity(self) -> None:
        first = self.run_baseline()
        result_path = self.workspace / "data/runs" / first["run_id"] / "run_result.json"
        legacy = dict(first)
        legacy.pop("review_fingerprint", None)
        result_path.write_text(json.dumps(legacy), encoding="utf-8")
        before = self.workspace_bytes()

        with self.assertRaisesRegex(ReviewManifestError, "legacy run.*new run_id"):
            self.run_baseline()

        self.assertEqual(before, self.workspace_bytes())

    def test_review_reordering_and_unrelated_reviews_do_not_invalidate_cache(self) -> None:
        first = self.run_baseline()
        scenario = json.loads(self.baseline_path.read_text(encoding="utf-8"))
        manifest = self.workspace / scenario["review_manifest_path"]
        reviews = [json.loads(line) for line in manifest.read_text(encoding="utf-8").splitlines()]
        for review in reviews:
            if review["run_id"] != first["run_id"]:
                review["reason"] = "Unrelated run review changed"
        manifest.write_text("\n".join(json.dumps(item) for item in reversed(reviews)) + "\n", encoding="utf-8")
        self.assertEqual(self.run_baseline(), first)

    def test_fresh_temporal_run_rejects_prior_archive_damage_before_any_writes(self) -> None:
        self.run_baseline()
        scenario = json.loads(self.baseline_path.read_text(encoding="utf-8"))
        archive = self.workspace / scenario["source"]["local_archive_path"]
        original = archive.read_bytes()
        for damage in ("tampered", "missing"):
            with self.subTest(damage=damage):
                if damage == "tampered":
                    archive.write_bytes(original + b"\nSynthetic prior-source corruption.\n")
                    error = SourceHashMismatch
                else:
                    archive.unlink()
                    error = FileNotFoundError
                before = self.workspace_bytes()

                with self.assertRaises(error):
                    run_vertical_slice(self.workspace, self.update_path)

                self.assertEqual(before, self.workspace_bytes())
                archive.write_bytes(original)
        # Failed preflights leave no orphan source registration or partial run.
        update = json.loads(self.update_path.read_text(encoding="utf-8"))
        self.assertEqual(run_vertical_slice(self.workspace, self.update_path)["run_id"], update["run_id"])

    def test_unused_orphan_source_does_not_block_a_fresh_temporal_run(self) -> None:
        self.run_baseline()
        scenario = json.loads(self.baseline_path.read_text(encoding="utf-8"))
        orphan = dict(scenario["source"])
        orphan["source_id"] = "SRC-UNUSED-ORPHAN"
        orphan["local_archive_path"] = "data/raw/sources/unused-missing.md"
        registry = self.workspace / "data/sources/source_registry.jsonl"
        with registry.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(orphan) + "\n")

        update = json.loads(self.update_path.read_text(encoding="utf-8"))
        self.assertEqual(run_vertical_slice(self.workspace, self.update_path)["run_id"], update["run_id"])

    def test_retrieval_source_trace(self) -> None:
        result = self.run_baseline()
        required = {"evidence_id", "source_id", "excerpt", "locator", "date", "evidence_level"}
        self.assertTrue(result["retrieval"]["initial"])
        for item in result["retrieval"]["initial"]:
            self.assertTrue(required.issubset(item))

    def test_graph_edge_trace_uses_evidence_ids(self) -> None:
        self.run_baseline()
        edges = json.loads((self.workspace / "data/graph/edges.json").read_text(encoding="utf-8"))
        self.assertTrue(edges)
        for edge in edges:
            self.assertTrue(edge["evidence_ids"])
            self.assertNotIn("source_id", edge)

    def test_contradiction_preservation(self) -> None:
        result = self.run_baseline()
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
        scenario = json.loads(self.baseline_path.read_text(encoding="utf-8"))
        source = SourceRecord.from_dict(scenario["source"])
        spec = copy.deepcopy(scenario["evidence"][0])
        spec["evidence_id"] = "EVD-UNSUPPORTED-INFERENCE"
        spec["evidence_level"] = "E_STRONG_INFERENCE"
        spec["claim"] = "Uncorroborated commercial leadership inference"
        evidence = EvidenceRecord.from_spec(spec, source, scenario["run_id"], scenario["run_at"], "test")
        audit = DeterministicAuditor().audit([evidence.to_dict()], {source.source_id: source.to_dict()})
        self.assertIn("UNSUPPORTED_INFERENCE", {item["code"] for item in audit["blocking_findings"]})

    def test_direct_transition_cannot_bypass_review_record(self) -> None:
        evidence = self.scenario_source_evidence()
        with self.assertRaises(HumanReviewRequired):
            DeterministicHarness().transition(
                evidence,
                EvidenceStatus.PROMOTED.value,
                "attempt automatic promotion",
                "RUN-TEST",
                "2026-08-26T09:00:00+09:00",
            )

    def test_evidence_level_review_approval(self) -> None:
        result = self.run_baseline()
        self.assertEqual({EvidenceStatus.PROMOTED.value}, set(result["state_by_evidence"].values()))
        self.assertEqual(4, len(result["review_outcomes"]))
        self.assertTrue(all(not item["promotion_blocked"] for item in result["review_outcomes"]))
        self.assertEqual("HUMAN_APPROVED", result["memo"]["review_status"])

    def test_hold_evidence_cannot_promote(self) -> None:
        evidence = self.scenario_source_evidence()
        result = DeterministicHarness().apply_review(
            evidence,
            self.review(evidence, "HOLD"),
            blocking_findings=[],
            independent_source_count=1,
            unresolved_contradiction_ids=[],
        )
        self.assertEqual(EvidenceStatus.HUMAN_REVIEW.value, result)
        with self.assertRaises(HumanReviewRequired):
            DeterministicHarness().transition(
                evidence,
                EvidenceStatus.PROMOTED.value,
                "bypass HOLD",
                "RUN-TEST",
                "2026-08-26T09:00:00+09:00",
            )

    def test_reject_evidence_cannot_promote(self) -> None:
        evidence = self.scenario_source_evidence()
        result = DeterministicHarness().apply_review(
            evidence,
            self.review(evidence, "REJECT"),
            blocking_findings=[],
            independent_source_count=1,
            unresolved_contradiction_ids=[],
        )
        self.assertEqual(EvidenceStatus.REJECTED.value, result)
        with self.assertRaises(InvalidTransition):
            DeterministicHarness().transition(
                evidence,
                EvidenceStatus.PROMOTED.value,
                "bypass REJECT",
                "RUN-TEST",
                "2026-08-26T09:00:00+09:00",
            )

    def test_strong_inference_requires_independent_sources(self) -> None:
        evidence = self.scenario_source_evidence("E_STRONG_INFERENCE")
        with self.assertRaises(IndependentSupportRequired):
            DeterministicHarness().apply_review(
                evidence,
                self.review(evidence),
                blocking_findings=[],
                independent_source_count=1,
                unresolved_contradiction_ids=[],
            )

    def test_hypothesis_cannot_promote(self) -> None:
        evidence = self.scenario_source_evidence("F_HYPOTHESIS")
        with self.assertRaises(PromotionProhibited):
            DeterministicHarness().apply_review(
                evidence,
                self.review(evidence),
                blocking_findings=[],
                independent_source_count=2,
                unresolved_contradiction_ids=[],
            )

    def test_every_memo_fact_has_evidence_trace(self) -> None:
        _, result = self.run_sequence()
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

    def test_temporal_update_preserves_prior_evidence(self) -> None:
        self.run_sequence()
        evidence_map = {
            item["evidence_id"]: item
            for item in (
                json.loads(line)
                for line in (self.workspace / "data/evidence/atomic_evidence.jsonl").read_text(
                    encoding="utf-8"
                ).splitlines()
            )
        }
        self.assertEqual(6, len(evidence_map))
        self.assertIn("EVD-HBM4-SAMPLE-SHIPMENT", evidence_map)
        self.assertIn("EVD-HBM4-MASS-SHIPMENT-Q2-2026", evidence_map)

    def test_newer_source_does_not_overwrite_older_evidence(self) -> None:
        before, after = self.run_sequence()
        before_snapshot = {
            item["evidence_id"]: item
            for item in json.loads(
                (self.workspace / "data/runs" / before["run_id"] / "evidence_snapshot.json").read_text(
                    encoding="utf-8"
                )
            )
        }
        final_map = {
            item["evidence_id"]: item
            for item in (
                json.loads(line)
                for line in (self.workspace / "data/evidence/atomic_evidence.jsonl").read_text(
                    encoding="utf-8"
                ).splitlines()
            )
        }
        prior_id = "EVD-HBM4-CERTIFICATION-PENDING"
        for field in ("source_id", "publication_date", "excerpt", "locator", "claim", "evidence_level"):
            self.assertEqual(before_snapshot[prior_id][field], final_map[prior_id][field])
        self.assertEqual(EvidenceStatus.PROMOTED.value, after["state_by_evidence"][prior_id])

    def test_decision_state_diff_is_reproducible(self) -> None:
        _, first = self.run_sequence()
        _, second = self.run_sequence()
        self.assertEqual(first["temporal_state_diff"], second["temporal_state_diff"])
        self.assertEqual(
            first["temporal_state_diff"]["diff_hash"],
            second["temporal_state_diff"]["diff_hash"],
        )

    def test_replay_is_deterministic(self) -> None:
        _, first = self.run_sequence()
        _, second = self.run_sequence()
        self.assertEqual(first["state_by_evidence"], second["state_by_evidence"])
        self.assertEqual(first["graph_diff"], second["graph_diff"])
        self.assertEqual(first["source_trace"], second["source_trace"])
        self.assertEqual(first["trace_hash"], second["trace_hash"])


if __name__ == "__main__":
    unittest.main()
