"""Regression checks for unsafe or broken public research intake."""
from __future__ import annotations

import hashlib
import json
import shutil
import tempfile
import unittest
from pathlib import Path

from scripts.validate_supply_chain_research import DEFAULT_BUNDLE, validate


class SupplyChainResearchTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.bundle = Path(self.temp.name) / "bundle"
        shutil.copytree(DEFAULT_BUNDLE, self.bundle)

    def mutate(self, name, change):
        path = self.bundle / name
        doc = json.loads(path.read_text(encoding="utf-8"))
        change(doc)
        raw = (json.dumps(doc, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
        path.write_bytes(raw)
        manifest_path = self.bundle / "manifest.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        for entry in manifest["artifacts"]:
            if entry["file"] == name:
                entry["sha256"] = hashlib.sha256(raw).hexdigest()
                entry["bytes"] = len(raw)
        manifest_path.write_text(json.dumps(manifest), encoding="utf-8")

    def test_complete_bundle_is_valid_but_not_evidence_approval(self):
        result = validate(self.bundle)
        self.assertEqual(result["status"], "PASS")
        self.assertFalse(result["evidence_approved"])

    def test_dangling_customer_reference_is_rejected_even_with_updated_hash(self):
        self.mutate("supply_chain_map_v3.json", lambda d: d["relations"][0].update(to="unverified-customer"))
        with self.assertRaisesRegex(ValueError, "dangling actor"):
            validate(self.bundle)

    def test_candidate_cannot_silently_become_validated_predictor(self):
        self.mutate("signal_catalog_v2.json", lambda d: d["metrics"][0].update(leading_prediction_validated=True))
        with self.assertRaisesRegex(ValueError, "predictive validity"):
            validate(self.bundle)

    def test_unverified_facility_coordinate_is_rejected(self):
        self.mutate("verified_facilities.geojson", lambda d: d["features"][0].update(id="unverified-site"))
        with self.assertRaisesRegex(ValueError, "unverified facility"):
            validate(self.bundle)

    def test_user_access_inventory_is_rejected(self):
        self.mutate("api_issuance_plan_v3.json", lambda d: d.update(existing_access=[]))
        with self.assertRaisesRegex(ValueError, "user-specific"):
            validate(self.bundle)

    def test_raw_generator_status_cannot_disappear_from_geojson(self):
        self.mutate("verified_facilities.geojson", lambda d: d["features"][0]["properties"].update(generator_statuses=[]))
        with self.assertRaisesRegex(ValueError, "raw generator status"):
            validate(self.bundle)


if __name__ == "__main__":
    unittest.main()
