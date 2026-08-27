from __future__ import annotations

import json
import tempfile
import unittest
from dataclasses import replace
from pathlib import Path

from src.core.models import ContractError
from src.measurement.models import EventRecord, TrackRecord
from src.measurement.snapshot import SnapshotBuilder, SnapshotStore
from src.measurement.validation import (
    HistoricalLeakageError,
    ScopeJoinError,
    SemanticContractError,
    StratumPoolingError,
    assess_observation,
    assess_within_track_scope,
    count_independent_origins,
    validate_event_for_track,
    validate_single_stratum_batch,
)


FIXTURE_PATH = (
    Path(__file__).parent / "fixtures" / "h1_measurement" / "tiny_contract.json"
)


class H1MeasurementContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.raw = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
        cls.tracks = {
            item["track_id"]: TrackRecord.from_dict(item)
            for item in cls.raw["tracks"]
        }
        cls.events = {
            item["event_id"]: EventRecord.from_dict(item)
            for item in cls.raw["events"]
        }
        cls.builder = SnapshotBuilder()

    def build_snapshot(self, **overrides):
        values = {
            "snapshot_id": "SNP-H1-TINY-2024-03",
            "contract_version": self.raw["contract_version"],
            "tracks": self.tracks.values(),
            "events": self.events.values(),
            "cutoff_at": "2024-03-01T00:00:00+00:00",
            "dataset_freeze_at": "2025-08-01T00:00:00+00:00",
            "observation_window_months": 12,
            "created_at": "2026-08-28T12:00:00+09:00",
        }
        values.update(overrides)
        return self.builder.build(**values)

    def test_valid_product_signal_record(self) -> None:
        event = self.events["EVT-P-A-SAMPLE"]
        validate_event_for_track(event, self.tracks[event.track_id])
        self.assertEqual(event.data_role, "SIGNAL")
        self.assertEqual(event.transmission_layer, "MEMORY_PRODUCT")

    def test_valid_platform_signal_record(self) -> None:
        event = self.events["EVT-C-A-CAPEX"]
        validate_event_for_track(event, self.tracks[event.track_id])
        self.assertEqual(event.data_role, "SIGNAL")
        self.assertEqual(event.transmission_layer, "CUSTOMER_ECONOMICS")

    def test_missing_data_role_is_invalid(self) -> None:
        payload = dict(self.raw["events"][0])
        payload.pop("data_role")
        with self.assertRaises(ContractError):
            EventRecord.from_dict(payload)

    def test_context_is_distinct_from_signal_and_outcome(self) -> None:
        event = self.events["EVT-P-A-MARKET-CONTEXT"]
        validate_event_for_track(event, self.tracks[event.track_id])
        self.assertEqual(event.data_role, "CONTEXT")
        self.assertNotEqual(event.data_role, "SIGNAL")
        self.assertNotEqual(event.data_role, "OUTCOME")

    def test_unapproved_transmission_layer_is_invalid(self) -> None:
        payload = dict(self.raw["events"][0])
        payload["transmission_layer"] = "RAW_MATERIAL"
        with self.assertRaises(ContractError):
            EventRecord.from_dict(payload)

    def test_historical_leakage_is_blocked(self) -> None:
        with self.assertRaises(HistoricalLeakageError):
            self.build_snapshot(
                requested_track_ids=["TRK-C-B"],
                requested_event_ids=["EVT-C-B-LATER-DISCLOSURE"],
                cutoff_at="2024-12-31T23:59:59+00:00",
                dataset_freeze_at="2025-12-31T23:59:59+00:00",
            )

    def test_preview_is_not_operational_realization(self) -> None:
        invalid = EventRecord.from_dict(
            self.raw["invalid_cases"]["preview_as_outcome"]
        )
        with self.assertRaises(SemanticContractError):
            validate_event_for_track(invalid, self.tracks[invalid.track_id])
        preview = self.events["EVT-C-A-PREVIEW"]
        validate_event_for_track(preview, self.tracks[preview.track_id])
        self.assertEqual(preview.data_role, "SIGNAL")

    def test_sample_is_not_qualification_completion(self) -> None:
        invalid = EventRecord.from_dict(
            self.raw["invalid_cases"]["sample_as_qualification_complete"]
        )
        with self.assertRaises(SemanticContractError):
            validate_event_for_track(invalid, self.tracks[invalid.track_id])

    def test_qualification_underway_is_not_complete(self) -> None:
        invalid = EventRecord.from_dict(
            self.raw["invalid_cases"]["qualification_underway_as_complete"]
        )
        with self.assertRaises(SemanticContractError):
            validate_event_for_track(invalid, self.tracks[invalid.track_id])

    def test_future_customer_supply_is_not_current_o1(self) -> None:
        invalid = EventRecord.from_dict(
            self.raw["invalid_cases"]["future_supply_as_current_o1"]
        )
        with self.assertRaisesRegex(
            SemanticContractError, "future-dated customer supply"
        ):
            validate_event_for_track(invalid, self.tracks[invalid.track_id])

    def test_production_start_is_not_supply_commitment(self) -> None:
        invalid = EventRecord.from_dict(
            self.raw["invalid_cases"]["production_as_supply_commitment"]
        )
        with self.assertRaisesRegex(
            SemanticContractError, "production or ramp wording alone"
        ):
            validate_event_for_track(invalid, self.tracks[invalid.track_id])

    def test_event_and_publication_date_precision_can_differ(self) -> None:
        payload = dict(self.raw["events"][0])
        payload["date_precision"] = "DAY"
        payload["event_date_precision"] = "MONTH"
        payload["availability_basis"] = "PUBLISHER_DATE_FALLBACK"
        payload["published_at"] = "2023-01-10T00:00:00+09:00"
        payload["available_at"] = "2023-01-11T00:00:00+09:00"
        event = EventRecord.from_dict(payload)
        self.assertEqual(event.date_precision, "DAY")
        self.assertEqual(event.event_date_precision, "MONTH")

    def test_revision_preserves_earlier_record_and_activates_by_cutoff(self) -> None:
        before = self.build_snapshot(
            snapshot_id="SNP-BEFORE-REVISION",
            cutoff_at="2024-01-31T23:59:59+00:00",
        )
        after = self.build_snapshot(snapshot_id="SNP-AFTER-REVISION")
        self.assertIn("EVT-C-B-PLAN-R1", self.events)
        self.assertIn("EVT-C-B-PLAN-R2", self.events)
        self.assertIn("EVT-C-B-PLAN-R1", before.included_event_ids)
        self.assertNotIn("EVT-C-B-PLAN-R2", before.included_event_ids)
        self.assertNotIn("EVT-C-B-PLAN-R1", after.included_event_ids)
        self.assertIn("EVT-C-B-PLAN-R2", after.included_event_ids)

    def test_independence_counts_origin_groups_not_urls(self) -> None:
        mirrored = [
            self.events["EVT-P-A-SAMPLE"],
            self.events["EVT-P-A-SAMPLE-MIRROR"],
        ]
        self.assertNotEqual(mirrored[0].source_id, mirrored[1].source_id)
        self.assertEqual(count_independent_origins(mirrored), 1)

    def test_right_censored_event_is_not_failure_denominator_eligible(self) -> None:
        event = self.events["EVT-P-B-RIGHT-CENSORED"]
        primary = assess_observation(
            event,
            self.tracks[event.track_id],
            "2026-06-01T00:00:00+00:00",
            12,
        )
        shorter = assess_observation(
            event,
            self.tracks[event.track_id],
            "2026-06-01T00:00:00+00:00",
            6,
        )
        longer = assess_observation(
            event,
            self.tracks[event.track_id],
            "2026-06-01T00:00:00+00:00",
            18,
        )
        self.assertTrue(primary.right_censored)
        self.assertFalse(primary.fully_observed)
        self.assertFalse(primary.eligible_for_failure_denominator)
        self.assertTrue(shorter.fully_observed)
        self.assertTrue(longer.right_censored)

    def test_left_truncation_is_explicit(self) -> None:
        event = self.events["EVT-P-B-RIGHT-CENSORED"]
        result = assess_observation(
            event,
            self.tracks[event.track_id],
            "2026-06-01T00:00:00+00:00",
            12,
        )
        self.assertTrue(self.tracks[event.track_id].left_truncated)
        self.assertTrue(result.left_truncated)

    def test_incompatible_scope_join_is_rejected(self) -> None:
        product_event = self.events["EVT-P-A-SAMPLE"]
        platform_event = self.events["EVT-C-A-PREVIEW"]
        with self.assertRaises(ScopeJoinError):
            assess_within_track_scope(
                product_event,
                platform_event,
                self.tracks[product_event.track_id],
            )

    def test_outcomes_from_two_strata_cannot_be_pooled(self) -> None:
        outcomes = [
            self.events["EVT-P-A-O1"],
            self.events["EVT-C-A-P1-GA"],
        ]
        with self.assertRaises(StratumPoolingError):
            validate_single_stratum_batch(outcomes, self.tracks)

    def test_held_event_requires_and_preserves_a_manifest_reason(self) -> None:
        held = replace(self.events["EVT-P-A-SAMPLE"], review_status="HOLD")
        arguments = {
            "snapshot_id": "SNP-HELD-EVENT",
            "contract_version": self.raw["contract_version"],
            "tracks": [self.tracks[held.track_id]],
            "events": [held],
            "requested_track_ids": [held.track_id],
            "requested_event_ids": [held.event_id],
            "cutoff_at": "2024-01-01T00:00:00+00:00",
            "dataset_freeze_at": "2025-01-01T00:00:00+00:00",
            "observation_window_months": 12,
            "created_at": "2026-08-28T12:00:00+09:00",
        }
        with self.assertRaises(ContractError):
            self.builder.build(**arguments)
        manifest = self.builder.build(
            **arguments,
            exclusions_and_holds=[
                {
                    "record_id": held.event_id,
                    "record_type": "EVENT",
                    "decision": "HOLD",
                    "reason": "Synthetic ambiguity requires human semantic review.",
                }
            ],
        )
        self.assertNotIn(held.event_id, manifest.included_event_ids)
        self.assertEqual(manifest.exclusions_and_holds[0]["decision"], "HOLD")
        self.assertTrue(manifest.exclusions_and_holds[0]["reason"])

    def test_publisher_date_fallback_starts_next_calendar_day(self) -> None:
        revision = self.events["EVT-C-B-PLAN-R2"]
        self.assertEqual(revision.availability_basis, "PUBLISHER_DATE_FALLBACK")
        self.assertTrue(revision.available_at.endswith("T00:00:00-08:00"))

    def test_snapshot_hash_and_replay_are_deterministic_and_immutable(self) -> None:
        first = self.build_snapshot()
        replay = self.build_snapshot()
        self.assertEqual(first.content_hash, replay.content_hash)
        self.assertEqual(first.to_dict(), replay.to_dict())
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "snapshot.json"
            store = SnapshotStore(path)
            self.assertTrue(store.put(first))
            self.assertFalse(store.put(replay))
            self.assertEqual(store.load().content_hash, first.content_hash)
            changed = replace(first, snapshot_id="SNP-CHANGED")
            with self.assertRaises(ContractError):
                changed.to_dict()


if __name__ == "__main__":
    unittest.main()
