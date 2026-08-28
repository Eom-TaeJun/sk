from __future__ import annotations

import json
import unittest
from collections import Counter
from pathlib import Path

from src.measurement.corpus import (
    CollectionStatusManifest,
    CorpusBuilder,
    CorpusDataset,
    FORBIDDEN_EMPIRICAL_KEYS,
)
from src.measurement.pilot import PilotDataset, PilotSourceRegistry
from src.measurement.registry import CandidateTrackRegistry, RegistryFreezeManifest


ROOT = Path(__file__).resolve().parents[1]


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def walk_keys(value):
    if isinstance(value, dict):
        for key, nested in value.items():
            yield key
            yield from walk_keys(nested)
    elif isinstance(value, list):
        for nested in value:
            yield from walk_keys(nested)


class H1FullCorpusTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.builder = CorpusBuilder(ROOT)
        cls.input_path = ROOT / "data/h1/corpus/collection_input.json"
        cls.manifest = cls.builder.build(cls.input_path)
        cls.registry = CandidateTrackRegistry.from_dict(
            load_json(ROOT / "data/h1/registry/candidate_tracks.json")
        )
        cls.freeze = RegistryFreezeManifest(
            **load_json(ROOT / "data/h1/registry/registry_freeze.json")
        )
        cls.pilot_sources = PilotSourceRegistry.from_dict(
            load_json(ROOT / "data/h1/pilot/source_registry.json")
        )
        cls.pilot = PilotDataset.from_dict(
            load_json(ROOT / "data/h1/pilot/pilot_events.json")
        )
        cls.sources = PilotSourceRegistry.from_dict(
            load_json(ROOT / "data/h1/corpus/source_registry.json")
        )
        cls.collection = CollectionStatusManifest.from_dict(
            load_json(ROOT / "data/h1/corpus/track_collection_status.json")
        )
        cls.dataset = CorpusDataset.from_dict(
            load_json(ROOT / "data/h1/corpus/events.json")
        )
        cls.results = load_json(ROOT / "data/h1/corpus/validation_results.json")[
            "results"
        ]

    def test_exact_frozen_population_has_collection_status(self) -> None:
        expected = sorted(self.registry.as_map())
        self.assertEqual(self.dataset.track_ids, expected)
        self.assertEqual([record.track_id for record in self.collection.records], expected)
        counts = Counter(track.track_type for track in self.registry.tracks)
        self.assertEqual(counts["PRODUCT_COMMERCIALIZATION_TRACK"], 10)
        self.assertEqual(counts["CUSTOMER_PLATFORM_REALIZATION_TRACK"], 14)

    def test_immutable_pilot_is_imported_without_rewrite(self) -> None:
        self.assertEqual(
            self.dataset.pilot_source_registry_content_hash,
            self.pilot_sources.content_hash,
        )
        self.assertEqual(self.dataset.pilot_dataset_content_hash, self.pilot.content_hash)
        source_map = self.sources.as_map()
        corpus_events = {record.event.event_id: record.to_dict() for record in self.dataset.records}
        for source in self.pilot_sources.sources:
            self.assertEqual(source_map[source.source_id].to_dict(), source.to_dict())
        for record in self.pilot.records:
            self.assertEqual(corpus_events[record.event.event_id], record.to_dict())

    def test_all_sources_are_primary_and_archived_with_trace(self) -> None:
        self.sources.verify_archives(ROOT)
        self.assertEqual(len(self.sources.sources), 51)
        for source in self.sources.sources:
            self.assertTrue(source.primary_source)
            self.assertTrue(source.url.startswith("https://"))
            self.assertTrue(source.excerpt)
            self.assertTrue(source.locator)
            self.assertEqual(len(source.content_hash), 64)

    def test_every_track_has_completed_supporting_and_adverse_search(self) -> None:
        for record in self.collection.records:
            self.assertEqual(record.supporting_search_status, "COMPLETE")
            self.assertEqual(record.contradictory_search_status, "COMPLETE")
            self.assertTrue(record.source_ids)
            if record.negative_search_result == "EXPLICIT_NEGATIVE_OR_DELAY":
                self.assertTrue(record.negative_source_ids)
            else:
                self.assertEqual(record.negative_search_result, "NOT_OBSERVED_PUBLICLY")
                self.assertFalse(record.negative_source_ids)

    def test_adversarial_verifier_is_independent_and_covers_every_hold(self) -> None:
        verification = load_json(
            ROOT / "data/h1/corpus/adversarial_verification.json"
        )
        self.assertNotEqual(
            verification["collector_actor"], verification["verifier_actor"]
        )
        self.assertEqual(
            [record["track_id"] for record in verification["records"]],
            sorted(self.registry.as_map()),
        )
        linked_holds = {
            event_id
            for record in verification["records"]
            for event_id in record["hold_event_ids"]
        }
        corpus_holds = {
            record.event.event_id
            for record in self.dataset.records
            if record.ingestion_status == "HOLD"
        }
        self.assertEqual(linked_holds, corpus_holds)

    def test_accepted_candidates_remain_unreviewed_and_holds_are_preserved(self) -> None:
        counts = self.dataset.status_counts()
        self.assertEqual(counts, {"ACCEPTED": 63, "HOLD": 12})
        for record in self.dataset.records:
            if record.ingestion_status == "ACCEPTED":
                self.assertEqual(record.event.review_status, "UNREVIEWED")
            elif record.ingestion_status == "HOLD":
                self.assertEqual(record.event.review_status, "HOLD")
                self.assertTrue(record.ambiguity)
                self.assertTrue(record.human_judgment_required)

    def test_deterministic_validation_catches_real_stage_inflation(self) -> None:
        rejected = {
            item["event_id"]: item["deterministic_reason"]
            for item in self.results
            if item["deterministic_result"] == "REJECTED"
        }
        self.assertIn("EVT-P10-20260624-DEVELOPMENT-AS-SAMPLE-HOLD", rejected)
        self.assertIn("explicit sample or sampling wording", rejected[
            "EVT-P10-20260624-DEVELOPMENT-AS-SAMPLE-HOLD"
        ])
        self.assertIn("EVT-C14-20250929-GB200-INSTALLED-HOLD", rejected)
        self.assertIn("installed disclosure alone", rejected[
            "EVT-C14-20250929-GB200-INSTALLED-HOLD"
        ])
        self.assertTrue(
            all(
                item["deterministic_result"] == "PASS"
                for item in self.results
                if item["ingestion_status"] == "ACCEPTED"
            )
        )

    def test_production_context_revision_preserves_pilot_history(self) -> None:
        records = {record.event.event_id: record for record in self.dataset.records}
        old = records["EVT-P04-20240226-PRODUCTION"]
        revised = records["EVT-P04-20240226-PRODUCTION-CONTEXT-R2"]
        self.assertEqual(old.ingestion_status, "HOLD")
        self.assertEqual(revised.ingestion_status, "ACCEPTED")
        self.assertEqual(revised.event.data_role, "CONTEXT")
        self.assertEqual(revised.event.signal_class, "PRODUCTION_STAGE_CONTEXT")
        self.assertEqual(revised.event.supersedes_event_id, old.event.event_id)

    def test_event_source_trace_and_historical_dates_are_complete(self) -> None:
        source_map = self.sources.as_map()
        for record in self.dataset.records:
            event = record.event
            source = source_map[event.source_id]
            self.assertEqual(event.excerpt, source.excerpt)
            self.assertEqual(event.locator, source.locator)
            self.assertEqual(event.published_at, source.published_at)
            self.assertEqual(event.available_at, source.available_at)
            self.assertEqual(event.origin_group, source.origin_group)

    def test_coverage_contract_separates_product_and_platform_fields(self) -> None:
        coverage = load_json(ROOT / "data/h1/corpus/coverage_report.json")
        self.assertEqual(len(coverage["tracks"]), 24)
        for row in coverage["tracks"]:
            fields = set(row["coverage"])
            if row["track_type"] == "PRODUCT_COMMERCIALIZATION_TRACK":
                self.assertIn("production_stage_context", fields)
                self.assertIn("o1_candidate", fields)
                self.assertNotIn("capex", fields)
            else:
                self.assertIn("capex", fields)
                self.assertIn("operational_evidence", fields)
                self.assertNotIn("production_stage_context", fields)

    def test_no_empirical_h1_output_exists_before_gate6(self) -> None:
        paths = [
            ROOT / "data/h1/corpus/collection_input.json",
            ROOT / "data/h1/corpus/events.json",
            ROOT / "data/h1/corpus/coverage_report.json",
            ROOT / "data/h1/corpus/build_manifest.json",
            ROOT / "data/h1/corpus/adversarial_verification.json",
            ROOT / "application_evidence/capability_evidence_ledger.json",
        ]
        for path in paths:
            found = set(walk_keys(load_json(path))) & FORBIDDEN_EMPIRICAL_KEYS
            self.assertFalse(found, f"forbidden pre-Gate-6 fields in {path}: {found}")
        self.assertFalse(self.manifest["gate6_frozen"])
        self.assertFalse(self.manifest["empirical_h1_calculated"])

    def test_capability_ledger_contains_only_traceable_performed_facts(self) -> None:
        ledger = load_json(ROOT / "application_evidence/capability_evidence_ledger.json")
        self.assertEqual(len(ledger["records"]), 8)
        allowed = {
            "VERIFIED_PERFORMED_FACT",
            "VERIFIED_IMPLEMENTATION_FACT",
            "PENDING_EMPIRICAL_RESULT",
        }
        for record in ledger["records"]:
            self.assertIn(record["claim_status"], allowed)
            self.assertTrue(record["artifact_references"])
            for artifact in record["artifact_references"]:
                self.assertTrue((ROOT / artifact).exists(), artifact)
            self.assertTrue(record["overclaim_boundary"])

    def test_same_input_replay_is_byte_and_hash_stable(self) -> None:
        before = {
            path: (ROOT / path).read_bytes()
            for path in self.manifest["file_hashes"]
        }
        replay = self.builder.build(self.input_path)
        self.assertEqual(replay, self.manifest)
        for path, content in before.items():
            self.assertEqual((ROOT / path).read_bytes(), content)


if __name__ == "__main__":
    unittest.main()
