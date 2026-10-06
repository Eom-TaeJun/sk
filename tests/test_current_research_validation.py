"""Offline tamper regressions for the current dated research packages."""
from __future__ import annotations

import contextlib
import hashlib
import io
import json
import shutil
import tempfile
import unittest
from pathlib import Path

from scripts.validate_current_research import (
    API_DIR, API_FILES, PRIOR_INPUT_HASHES, PURPOSE_DIR, PURPOSE_DOC, ROOT, main, validate,
)


class CurrentResearchValidationTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.workspace = Path(temporary.name) / "clone"
        # Copy only the public snapshot dependencies and mutable references.
        # Never build the governed corpus or rewrite repository artifacts.
        paths = {f"{API_DIR}/{name}" for name in API_FILES} | set(PRIOR_INPUT_HASHES)
        paths.update({f"{PURPOSE_DIR}/manifest.json", f"{PURPOSE_DIR}/purpose_registry.json", PURPOSE_DOC})
        for directory in (API_DIR, PURPOSE_DIR):
            manifest = json.loads((ROOT / directory / "manifest.json").read_text(encoding="utf8"))
            paths.update(manifest["documentation_paths"])
        for relative in paths:
            target = self.workspace / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / relative, target)

    def mutate_registry(self, change):
        relative = f"{PURPOSE_DIR}/purpose_registry.json"
        path = self.workspace / relative
        registry = json.loads(path.read_text(encoding="utf8"))
        change(registry)
        raw = (json.dumps(registry, ensure_ascii=False, indent=2) + "\n").encode("utf8")
        path.write_bytes(raw)
        manifest_path = self.workspace / PURPOSE_DIR / "manifest.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf8"))
        entry = next(row for row in manifest["files"] if row["path"] == relative)
        entry.update(sha256=hashlib.sha256(raw).hexdigest(), byte_size=len(raw))
        manifest_path.write_bytes((json.dumps(manifest, ensure_ascii=False, indent=2) + "\n").encode("utf8"))

    def rewrite(self, relative, document):
        (self.workspace / relative).write_bytes(
            (json.dumps(document, ensure_ascii=False, indent=2) + "\n").encode("utf8"))

    def rehash_chain(self):
        """Simulate consistent manifest updates, so hashes cannot mask a bug."""
        def refresh(entries, size_key):
            for entry in entries:
                raw = (self.workspace / entry["path"]).read_bytes()
                entry.update(sha256=hashlib.sha256(raw).hexdigest())
                entry[size_key] = len(raw)

        api_path = f"{API_DIR}/manifest.json"
        api_manifest = json.loads((self.workspace / api_path).read_text(encoding="utf8"))
        refresh(api_manifest["files"], "byte_length")
        self.rewrite(api_path, api_manifest)
        registry_path = f"{PURPOSE_DIR}/purpose_registry.json"
        registry = json.loads((self.workspace / registry_path).read_text(encoding="utf8"))
        refresh(registry["immutable_input_refs"], "byte_size")
        self.rewrite(registry_path, registry)
        manifest_path = f"{PURPOSE_DIR}/manifest.json"
        manifest = json.loads((self.workspace / manifest_path).read_text(encoding="utf8"))
        manifest["immutable_input_refs"] = registry["immutable_input_refs"]
        refresh(manifest["files"], "byte_size")
        self.rewrite(manifest_path, manifest)

    def mutate_both_summaries(self, key, value):
        for relative in (f"{API_DIR}/collection_index.json", f"{API_DIR}/manifest.json"):
            document = json.loads((self.workspace / relative).read_text(encoding="utf8"))
            document["summary_counts"][key] = value
            self.rewrite(relative, document)
        self.rehash_chain()

    def test_clone_is_valid_without_claiming_source_truth_or_approval(self):
        hashes_before = {p: hashlib.sha256(p.read_bytes()).hexdigest()
                         for p in self.workspace.rglob("*") if p.is_file()}
        result = validate(self.workspace)
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["review_objects"], {"numbered_indicators": 34, "family_measurement_contracts": 6})
        for flag in ("live_sources_rechecked", "source_truth_validated", "evidence_approved", "predictive_validity_established"):
            self.assertIs(result[flag], False)
        self.assertEqual(hashes_before, {p: hashlib.sha256(p.read_bytes()).hexdigest()
                                       for p in self.workspace.rglob("*") if p.is_file()})

    def test_cli_can_read_an_explicit_clone_workspace(self):
        with contextlib.redirect_stdout(io.StringIO()) as output:
            exit_code = main(["--workspace", str(self.workspace)])
        self.assertEqual(exit_code, 0)
        self.assertEqual(json.loads(output.getvalue())["status"], "PASS")

    def test_raw_tampering_is_rejected(self):
        path = self.workspace / API_DIR / "finance_macro_etf.json"
        path.write_bytes(path.read_bytes() + b"\n")
        with self.assertRaisesRegex(ValueError, "hash or byte-length mismatch"):
            validate(self.workspace)

    def test_missing_review_id_is_rejected_even_with_a_matching_manifest(self):
        self.mutate_registry(lambda registry: registry["review_entries"].pop())
        with self.assertRaisesRegex(ValueError, "purpose entries: missing or duplicate IDs"):
            validate(self.workspace)

    def test_duplicate_id_is_rejected_even_with_a_matching_manifest(self):
        self.mutate_registry(lambda registry: registry["review_entries"][1].update(
            review_id=registry["review_entries"][0]["review_id"]))
        with self.assertRaisesRegex(ValueError, "purpose entries: missing or duplicate IDs"):
            validate(self.workspace)

    def test_broken_index_pointer_is_rejected_even_with_a_matching_manifest(self):
        self.mutate_registry(lambda registry: registry["review_entries"][0].update(
            source_index_pointer="/numbered_indicators/999"))
        with self.assertRaisesRegex(ValueError, "broken JSON pointer"):
            validate(self.workspace)

    def test_valid_pointer_to_a_different_indicator_is_rejected(self):
        self.mutate_registry(lambda registry: registry["review_entries"][0].update(
            source_index_pointer="/numbered_indicators/1"))
        with self.assertRaisesRegex(ValueError, "purpose index pointer/ID mismatch"):
            validate(self.workspace)

    def test_candidate_cannot_be_promoted_even_with_a_matching_manifest(self):
        self.mutate_registry(lambda registry: registry.update(human_evidence_approved=True))
        with self.assertRaisesRegex(ValueError, "candidate boundary changed"):
            validate(self.workspace)

    def test_required_candidate_flag_cannot_be_removed(self):
        self.mutate_registry(lambda registry: registry.pop("human_evidence_approved"))
        with self.assertRaisesRegex(ValueError, "required candidate flags missing or changed"):
            validate(self.workspace)

    def test_same_count_priority_reclassification_is_rejected(self):
        self.mutate_registry(lambda registry: registry["review_entries"][0].update(collection_priority_ko="보조"))
        with self.assertRaisesRegex(ValueError, "purpose classification changed"):
            validate(self.workspace)

    def test_same_false_response_summary_and_updated_hash_chain_are_rejected(self):
        self.mutate_both_summaries("non_empty_data_api_responses", 99)
        with self.assertRaisesRegex(ValueError, "summary counts disagree with recorded arrays/results/families"):
            validate(self.workspace)

    def test_same_false_distinct_family_summary_and_updated_hash_chain_are_rejected(self):
        self.mutate_both_summaries("distinct_data_api_families_with_data", 11)
        with self.assertRaisesRegex(ValueError, "summary counts disagree with recorded arrays/results/families"):
            validate(self.workspace)

    def test_failure_file_cannot_be_reclassified_as_api_even_with_updated_hashes(self):
        relative = f"{API_DIR}/collection_index.json"
        index = json.loads((self.workspace / relative).read_text(encoding="utf8"))
        row = next(row for row in index["bounded_access_results"] if row["probe_id"] == "fred-IPG3344S")
        row["acquisition_mode"] = "DATA_API"
        self.rewrite(relative, index)
        self.rehash_chain()
        with self.assertRaisesRegex(ValueError, "failed-attempt mode disagrees with original receipt"):
            validate(self.workspace)

    def test_publication_instant_must_be_a_valid_utc_value(self):
        self.mutate_registry(lambda registry: registry.update(prepared_at_utc="2026-99-99T99:99:99Z"))
        with self.assertRaisesRegex(ValueError, "invalid UTC instant"):
            validate(self.workspace)

    def test_mutable_navigation_can_change_without_rehashing_inputs(self):
        path = self.workspace / "docs/research/supply_chain/indicator_collection_purpose.md"
        path.write_bytes(path.read_bytes() + "\n새 안내: 검증 뒤 기존 경제적 측정 계약을 따른다.\n".encode("utf8"))
        self.assertEqual(validate(self.workspace)["status"], "PASS")


if __name__ == "__main__":
    unittest.main()
