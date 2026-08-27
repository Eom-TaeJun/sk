from __future__ import annotations

import json
import unittest
from collections import Counter
from dataclasses import replace
from pathlib import Path

from src.core.models import ContractError
from src.measurement.pilot import PilotDataset, PilotSourceRegistry
from src.measurement.registry import (
    CandidateTrackRegistry,
    RegistryFreezeManifest,
    RegistryFreezer,
)
from src.measurement.validation import ScopeJoinError, assess_within_track_scope


ROOT = Path(__file__).resolve().parents[1]


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


class H1RealDataPilotTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.registry = CandidateTrackRegistry.from_dict(
            load_json(ROOT / "data/h1/registry/candidate_tracks.json")
        )
        cls.freeze = RegistryFreezeManifest(
            **load_json(ROOT / "data/h1/registry/registry_freeze.json")
        )
        cls.source_registry = PilotSourceRegistry.from_dict(
            load_json(ROOT / "data/h1/pilot/source_registry.json")
        )
        cls.dataset = PilotDataset.from_dict(
            load_json(ROOT / "data/h1/pilot/pilot_events.json")
        )
        cls.results = cls.dataset.validate(
            cls.registry, cls.freeze, cls.source_registry
        )
        cls.records = {
            record.event.event_id: record for record in cls.dataset.records
        }

    def test_outcome_neutral_registry_is_complete_and_frozen(self) -> None:
        counts = Counter(track.track_type for track in self.registry.tracks)
        self.assertTrue(self.registry.outcome_neutral)
        self.assertEqual(len(self.registry.tracks), 24)
        self.assertEqual(counts["PRODUCT_COMMERCIALIZATION_TRACK"], 10)
        self.assertEqual(counts["CUSTOMER_PLATFORM_REALIZATION_TRACK"], 14)
        forbidden = {
            "realized",
            "failed",
            "h1_verdict",
            "lead_days",
            "false_positive",
        }
        for track in self.registry.to_dict()["tracks"]:
            self.assertTrue(forbidden.isdisjoint(track))

    def test_registry_freeze_replay_is_deterministic(self) -> None:
        replay = RegistryFreezer().freeze(
            self.registry,
            freeze_id=self.freeze.freeze_id,
            registry_frozen_at=self.freeze.registry_frozen_at,
        )
        self.assertEqual(replay.to_dict(), self.freeze.to_dict())

    def test_every_primary_source_archive_and_hash_is_traceable(self) -> None:
        self.source_registry.verify_archives(ROOT)
        self.assertEqual(len(self.source_registry.sources), 13)
        self.assertTrue(all(source.primary_source for source in self.source_registry.sources))

    def test_exactly_four_pilot_tracks_and_atomic_event_range(self) -> None:
        self.assertEqual(
            self.dataset.pilot_track_ids,
            ["C02-AZ-H200", "C04-GCP-H200", "P02-SKH-HBM3E", "P04-MU-HBM3E"],
        )
        self.assertEqual(len(self.dataset.records), 15)
        self.assertEqual(self.dataset.status_counts(), {"ACCEPTED": 11, "HOLD": 4})

    def test_accepted_candidates_are_not_human_approved(self) -> None:
        accepted = [
            record for record in self.dataset.records
            if record.ingestion_status == "ACCEPTED"
        ]
        self.assertTrue(accepted)
        self.assertTrue(
            all(record.event.review_status == "UNREVIEWED" for record in accepted)
        )

    def test_hold_preserves_ambiguity_and_human_question(self) -> None:
        held = [
            record for record in self.dataset.records
            if record.ingestion_status == "HOLD"
        ]
        self.assertEqual(len(held), 4)
        self.assertTrue(all(record.ambiguity for record in held))
        self.assertTrue(all(record.human_judgment_required for record in held))

    def test_real_contract_failures_are_deterministically_rejected(self) -> None:
        rejected = {
            result.event_id: result.deterministic_reason
            for result in self.results
            if result.deterministic_result == "REJECTED"
        }
        self.assertEqual(
            set(rejected),
            {
                "EVT-P02-20230821-PRODUCTION-PLAN",
                "EVT-P02-20240319-FUTURE-CUSTOMER-SUPPLY",
                "EVT-P04-20240226-PRODUCTION",
            },
        )

    def test_broad_capex_cannot_be_joined_to_named_platform_without_approval(self) -> None:
        capex = self.records["EVT-C02-20240730-CAPEX"].event
        ga = self.records["EVT-C02-20241002-H200-GA"].event
        track = self.registry.as_map()["C02-AZ-H200"].to_measurement_track()
        with self.assertRaises(ScopeJoinError):
            assess_within_track_scope(capex, ga, track)
        self.assertEqual(
            assess_within_track_scope(capex, ga, track, allow_partial=True),
            "PARTIAL_BROAD_TO_NARROW",
        )

    def test_pilot_source_trace_mismatch_is_rejected(self) -> None:
        record = self.dataset.records[0]
        changed_event = replace(record.event, locator="invented locator")
        changed_record = replace(record, event=changed_event)
        records = [changed_record, *self.dataset.records[1:]]
        basis = self.dataset.hash_basis()
        basis["records"] = sorted(
            [item.to_dict() for item in records], key=lambda item: item["event"]["event_id"]
        )
        from src.core.storage import content_digest

        changed = replace(
            self.dataset,
            records=records,
            content_hash=content_digest(basis),
        )
        with self.assertRaisesRegex(ContractError, "provenance mismatch"):
            changed.validate(self.registry, self.freeze, self.source_registry)

    def test_replay_has_identical_dataset_and_validation_results(self) -> None:
        replay = PilotDataset.from_dict(
            load_json(ROOT / "data/h1/pilot/pilot_events.json")
        )
        replay_results = replay.validate(
            self.registry, self.freeze, self.source_registry
        )
        self.assertEqual(replay.to_dict(), self.dataset.to_dict())
        self.assertEqual(
            [result.to_dict() for result in replay_results],
            [result.to_dict() for result in self.results],
        )

    def test_pilot_does_not_store_h1_performance_outputs(self) -> None:
        forbidden = {
            "lead_days",
            "lag_days",
            "realization_rate",
            "false_positive_rate",
            "h1_p_verdict",
            "h1_c_verdict",
            "h1_conclusion",
        }
        self.assertTrue(forbidden.isdisjoint(self.dataset.to_dict()))
        for record in self.dataset.to_dict()["records"]:
            self.assertTrue(forbidden.isdisjoint(record))
            self.assertTrue(forbidden.isdisjoint(record["event"]))

    def test_contract_stress_log_is_complete_and_action_bounded(self) -> None:
        log = load_json(ROOT / "data/h1/pilot/contract_stress_log.json")
        required = {
            "issue_id",
            "source_ids",
            "event_ids",
            "original_wording",
            "model_candidate_classification",
            "current_deterministic_result",
            "human_interpretation",
            "rule_assessment",
            "action",
            "affected_decision_question",
        }
        allowed_actions = {
            "NO_CHANGE",
            "FIXTURE_ONLY",
            "VALIDATION_RULE_CHANGE",
            "SCHEMA_CHANGE",
            "DOCUMENTATION_CHANGE",
        }
        self.assertEqual(len(log["issues"]), 9)
        for issue in log["issues"]:
            self.assertEqual(set(issue), required)
            self.assertIn(issue["action"], allowed_actions)
            self.assertTrue(issue["source_ids"])
            self.assertTrue(issue["event_ids"])


if __name__ == "__main__":
    unittest.main()
