from __future__ import annotations

import json
import unittest
from collections import Counter
from pathlib import Path

from src.measurement.corpus import FORBIDDEN_EMPIRICAL_KEYS
from src.measurement.gate6_review import Gate6ReviewBuilder
from tests.workspace_helpers import isolated_h1_workspace


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


class H1Gate6ReviewTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.workspace = isolated_h1_workspace(cls)
        cls.output = cls.workspace / "data/h1/gate6_review"
        cls.builder = Gate6ReviewBuilder(cls.workspace)
        cls.manifest = cls.builder.build()
        cls.events = load_json(cls.output / "event_review_matrix.json")
        cls.holds = load_json(cls.output / "hold_resolution_sheet.json")
        cls.tracks = load_json(cls.output / "track_readiness_matrix.json")
        cls.product = load_json(cls.output / "h1_p_observability_matrix.json")
        cls.platform = load_json(cls.output / "h1_c_observability_matrix.json")
        cls.negative = load_json(cls.output / "negative_evidence_sufficiency.json")
        cls.censoring = load_json(cls.output / "censoring_readiness_matrix.json")
        cls.capex = load_json(cls.output / "capex_independence_reuse_audit.json")
        cls.o1 = load_json(cls.output / "o1_timing_policy_options.json")
        cls.authorization = load_json(cls.output / "analysis_authorization_proposal.json")
        cls.checklist = load_json(cls.output / "human_decision_checklist.json")

    def test_all_75_events_have_complete_human_review_rows_and_source_trace(self) -> None:
        required = {
            "event_id",
            "track_id",
            "track_type",
            "source_id",
            "publisher",
            "direct_excerpt",
            "locator",
            "data_role",
            "signal_class",
            "signal_subtype",
            "transmission_layer",
            "event_at",
            "published_at",
            "available_at",
            "event_date_precision",
            "scope_type",
            "scope_value",
            "origin_group",
            "evidence_level",
            "ingestion_status",
            "deterministic_validation_result",
            "adversarial_verifier_result",
            "missingness_relevant_to_interpretation",
            "codex_recommendation",
            "recommendation_reason",
            "main_risk",
            "required_human_judgment",
        }
        self.assertEqual(len(self.events["records"]), 75)
        source_map = {
            row["source_id"]: row
            for row in load_json(self.workspace / "data/h1/corpus/source_registry.json")["sources"]
        }
        for row in self.events["records"]:
            self.assertTrue(required <= set(row))
            source = source_map[row["source_id"]]
            self.assertEqual(row["direct_excerpt"], source["excerpt"])
            self.assertEqual(row["locator"], source["locator"])
            self.assertEqual(row["source_content_hash"], source["content_hash"])

    def test_accepted_events_are_not_defaulted_to_include(self) -> None:
        accepted = [row for row in self.events["records"] if row["ingestion_status"] == "ACCEPTED"]
        counts = Counter(row["codex_recommendation"] for row in accepted)
        self.assertEqual(counts["RECOMMEND_INCLUDE"], 56)
        self.assertEqual(counts["RECOMMEND_HOLD"], 4)
        self.assertEqual(counts["RECOMMEND_EXCLUDE"], 3)
        self.assertEqual(
            self.events["recommendation_counts"],
            {"RECOMMEND_EXCLUDE": 10, "RECOMMEND_HOLD": 9, "RECOMMEND_INCLUDE": 56},
        )

    def test_raw_review_status_is_preserved(self) -> None:
        corpus = load_json(self.workspace / "data/h1/corpus/events.json")
        raw_status = {
            record["event"]["event_id"]: record["event"]["review_status"]
            for record in corpus["records"]
        }
        self.assertEqual(
            {row["event_id"]: row["current_review_status"] for row in self.events["records"]},
            raw_status,
        )
        self.assertEqual(Counter(raw_status.values()), {"UNREVIEWED": 63, "HOLD": 12})

    def test_all_12_holds_receive_individual_nonbinding_resolution_options(self) -> None:
        self.assertEqual(len(self.holds["records"]), 12)
        self.assertEqual(self.holds["unresolved_raw_hold_count"], 12)
        self.assertEqual(self.holds["human_resolutions_selected"], 0)
        for row in self.holds["records"]:
            self.assertTrue(row["semantic_issue"])
            self.assertTrue(row["historical_time_issue"])
            self.assertTrue(row["resolving_primary_source"])
            self.assertTrue(row["human_options"])
            self.assertIsNone(row["human_resolution"])
        by_id = {row["event_id"]: row for row in self.holds["records"]}
        self.assertIn("backdated", by_id["EVT-C03-20240410-H100-RETRO-GA-HOLD"]["historical_time_issue"])
        self.assertIn("planned H200 integration", by_id["EVT-P04-20240226-H200-DESIGN-IN"]["semantic_issue"])
        self.assertIn("without an admissible H1-P signal", by_id["EVT-P10-20260624-DEVELOPMENT-AS-SAMPLE-HOLD"]["exclusion_effect"])

    def test_track_readiness_covers_frozen_population_without_admission(self) -> None:
        self.assertEqual(len(self.tracks["records"]), 24)
        self.assertEqual(Counter(row["track_type"] for row in self.tracks["records"]), {
            "PRODUCT_COMMERCIALIZATION_TRACK": 10,
            "CUSTOMER_PLATFORM_REALIZATION_TRACK": 14,
        })
        self.assertTrue(all(row["human_track_admission_decision"] is None for row in self.tracks["records"]))
        p10 = next(row for row in self.tracks["records"] if row["track_id"] == "P10-MU-HBM4E")
        self.assertEqual(p10["codex_proposed_use"], "DESCRIPTIVE_ONLY_NO_ADMISSIBLE_SIGNAL")

    def test_product_observability_does_not_force_complete_ladder(self) -> None:
        self.assertEqual(self.product["complete_sequential_ladder_assessment"], "NOT_IDENTIFIABLE_WITH_PUBLIC_CORPUS")
        stages = {row["stage"]: row for row in self.product["records"]}
        self.assertEqual(stages["SAMPLE"]["recommended_include_track_count"], 8)
        self.assertEqual(stages["QUALIFICATION"]["recommended_include_track_count"], 3)
        self.assertEqual(stages["DESIGN_IN"]["recommended_include_track_count"], 0)
        self.assertEqual(stages["COMMERCIAL_COMMITMENT"]["recommended_include_track_count"], 0)
        self.assertEqual(stages["O1_CUSTOMER_SUPPLY_OR_COMMERCIAL_SHIPMENT"]["recommended_hold_track_count"], 6)

    def test_platform_observability_preserves_state_and_scope_boundaries(self) -> None:
        states = {row["state"]: row for row in self.platform["records"]}
        self.assertEqual(states["CAPEX"]["recommended_include_track_count"], 11)
        self.assertEqual(states["GENERAL_AVAILABILITY"]["recommended_include_track_count"], 9)
        self.assertEqual(states["EXPLICIT_NAMED_TRACK_DELAY_OR_CONSTRAINT"]["observability_assessment"], "NOT_IDENTIFIABLE_WITH_PUBLIC_CORPUS")
        self.assertEqual(
            self.platform["complete_state_ladder_assessment"],
            "SPARSE_AND_HETEROGENEOUS_NOT_A_UNIVERSAL_SEQUENCE",
        )

    def test_negative_thresholds_are_preserved_and_unmet(self) -> None:
        audit = {row["stratum"]: row for row in self.negative["records"]}
        self.assertEqual(audit["H1-P"]["required_explicit_negative_or_delayed_tracks"], 2)
        self.assertEqual(audit["H1-P"]["observed_track_count"], 1)
        self.assertEqual(len(audit["H1-P"]["observed_origin_groups"]), 1)
        self.assertEqual(audit["H1-C"]["observed_track_count"], 0)
        self.assertIn("not met", audit["H1-C"]["consequence"])

    def test_censoring_readiness_has_24_tracks_by_3_windows_without_failures(self) -> None:
        self.assertEqual(len(self.censoring["records"]), 72)
        self.assertEqual({row["observation_window_months"] for row in self.censoring["records"]}, {6, 12, 18})
        for row in self.censoring["records"]:
            self.assertFalse(set(row["right_censored_event_ids"]) & set(row["denominator_eligible_event_ids"]))
            if row["usable_only_descriptively"]:
                self.assertFalse(row["usable_for_failure_no_realization_denominator"])
            if row["right_censored"]:
                self.assertFalse(row["fully_observed"])
        p01_rows = [row for row in self.censoring["records"] if row["track_id"] == "P01-SKH-HBM3"]
        self.assertTrue(all(row["left_truncated"] for row in p01_rows))

    def test_capex_reuse_does_not_create_independent_denominators(self) -> None:
        self.assertEqual(self.capex["raw_track_references"], 14)
        self.assertEqual(self.capex["independent_company_period_origins"], 5)
        for row in self.capex["records"]:
            self.assertTrue(row["may_be_reused_as_context"])
            self.assertFalse(row["may_be_counted_repeatedly_in_empirical_denominator"])
            self.assertTrue(row["one_independent_company_period_observation"])

    def test_o1_policy_and_authorization_are_nonbinding(self) -> None:
        self.assertIsNone(self.o1["human_selected_policy"])
        self.assertEqual(len(self.o1["options"]), 3)
        self.assertEqual({row["policy_id"] for row in self.o1["options"]}, {
            "POLICY_A_EXACT_DATE_ONLY",
            "POLICY_B_PUBLIC_CONFIRMATION_PROXY",
            "POLICY_C_INTERVAL_CENSORED_REALIZATION",
        })
        levels = {row["stratum"]: row["codex_proposed_maximum_level"] for row in self.authorization["strata"]}
        self.assertEqual(levels["H1-P"], "LEVEL_1_DESCRIPTIVE_TIMELINE")
        self.assertEqual(levels["H1-C"], "LEVEL_2_BOUNDED_LEAD_TIME_DESCRIPTION")
        self.assertFalse(self.authorization["human_authorization_selected"])

    def test_human_checklist_selects_nothing(self) -> None:
        self.assertFalse(self.checklist["checklist_complete"])
        self.assertEqual(len(self.checklist["event_admission"]), 75)
        self.assertTrue(all(row["human_decision"] is None for row in self.checklist["event_admission"]))
        self.assertTrue(all(row["human_resolution"] is None for row in self.checklist["hold_resolution"]))
        self.assertIsNone(self.checklist["o1_timing_policy"]["human_selected_policy"])
        self.assertIsNone(self.checklist["h1_p_readiness"]["human_decision"])
        self.assertIsNone(self.checklist["h1_c_readiness"]["human_decision"])
        self.assertIsNone(self.checklist["gate6"]["human_decision"])

    def test_package_has_no_empirical_h1_output_fields(self) -> None:
        for path in self.output.glob("*.json"):
            forbidden = set(walk_keys(load_json(path))) & FORBIDDEN_EMPIRICAL_KEYS
            self.assertFalse(forbidden, f"forbidden fields in {path}: {forbidden}")
        self.assertFalse(self.manifest["gate6_frozen"])
        self.assertFalse(self.manifest["empirical_h1_calculated"])
        self.assertFalse(self.manifest["human_decisions_selected"])

    def test_same_input_review_replay_is_byte_and_hash_stable(self) -> None:
        before = {
            path: (self.workspace / path).read_bytes()
            for path in self.manifest["file_hashes"]
        }
        replay = self.builder.build()
        self.assertEqual(replay, self.manifest)
        for path, content in before.items():
            self.assertEqual((self.workspace / path).read_bytes(), content)


if __name__ == "__main__":
    unittest.main()
