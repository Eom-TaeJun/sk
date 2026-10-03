"""Synthetic-only regression cases; no live availability or economic finding.

All HTML below is a small SYNTHETIC TEST FIXTURE, written only in temporary
directories. Passing these tests does not establish a successful SEC capture.
"""
from __future__ import annotations

import contextlib
import hashlib
import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from urllib.error import HTTPError

from scripts.collect_customer_commitment import (
    ACCESSION, DOCUMENT_NAME, INDEX_NAME, SOURCE_URLS, ISSUER_FILING_ID,
    ISSUER_SOURCE_URLS, ISSUER_DOCUMENT_NAME, ISSUER_FEED_NAME, CaptureError,
    capture, fetch_source, main, parse_case, parse_issuer_case,
    validate_source_url, verify_capture,
)


SYNTHETIC_DOCUMENT = b"""<!doctype html><html><head><title>SYNTHETIC TEST FIXTURE</title></head><body>
<p>SYNTHETIC TEST FIXTURE - NOT A RETRIEVED SEC DOCUMENT</p>
<a name="D17274D8K_HTM"></a>
<p>FORM 8-K</p>
<p>Date of Report (date of earliest event reported): September 25, 2025 (September 23, 2025)</p>
<p>Item 1.01 Entry into a Material Definitive Agreement.</p>
<p>On September 23, 2025, CoreWeave, Inc. (the "Company") and OpenAI OpCo, LLC ("OpenAI")
entered into a new order form (the "Order Form") under the existing Master Services Agreement
("MSA") dated as of May 8, 2025, pursuant to which the Company provides OpenAI access to cloud computing capacity.</p>
<p>Subject to any termination described below and satisfaction of delivery and availability of service requirements,
OpenAI has committed to pay the Company up to approximately $6.5 billion through May 31, 2031 under the Order Form.</p>
<p>Either party may terminate the MSA (and any order thereunder) for cause.</p>
<p>The foregoing description does not purport to be complete and is qualified in its entirety by reference to Exhibit 10.1.</p>
<p>Item 9.01 Financial Statements and Exhibits.</p></body></html>"""

SYNTHETIC_INDEX = f"""<!doctype html><html><body>
<p>SYNTHETIC TEST FIXTURE - NOT A RETRIEVED SEC DOCUMENT</p>
<p>Form 8-K - Current report</p><p>SEC Accession No. {ACCESSION}</p>
<div>Filing Date</div><div>2025-09-25</div>
<div>Accepted</div><div>2025-09-25 09:00:25</div>
<div>Period of Report</div><div>2025-09-23</div>
<p>CoreWeave, Inc. CIK: 0001769628</p><a href="{DOCUMENT_NAME}">8-K</a>
</body></html>""".encode("utf-8")


def synthetic_issuer_feed(change=None):
    """Small synthetic issuer metadata; never a real SEC filing-index substitute."""
    row = {
        "FilingId": ISSUER_FILING_ID, "FilingTypeMnemonic": "8-K",
        "StockExchange": "CIK", "StockSymbol": "0001769628", "FilingDate": "09/25/2025 00:00:00",
        "ReceivedDate": "09/25/2025 09:00:25",
        "DocumentList": [{"DocumentType": "HTML", "Url": ISSUER_SOURCE_URLS["document"]}],
    }
    if change:
        change(row)
    return json.dumps({"test_fixture_label": "SYNTHETIC TEST FIXTURE", "GetEdgarFilingListResult": [row]}).encode("utf-8")


class CustomerCommitmentCollectionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.output = Path(self.temp.name) / "candidate"
        self.documents = {"document": SYNTHETIC_DOCUMENT, "index": SYNTHETIC_INDEX}

    def parse(self, document=SYNTHETIC_DOCUMENT, index=SYNTHETIC_INDEX):
        return parse_case(document, index, allow_synthetic=True)

    def collect(self, documents=None, timestamp="2026-10-03T01:00:00Z"):
        return capture(self.output, documents or self.documents, mode="offline_import", allow_synthetic=True, timestamp=timestamp)

    def test_conditional_maximum_is_not_actual_cash_or_minimum(self):
        record = self.parse()
        self.assertEqual(record["event_kind"], "NEW_ORDER_FORM")
        self.assertEqual(record["stage"], "CONDITIONAL_CUSTOMER_COMMITMENT")
        self.assertEqual(record["maximum_commitment_usd"], 6_500_000_000)
        self.assertEqual(record["amount_qualifiers"], ["UP_TO", "APPROXIMATE", "CONDITIONAL"])
        self.assertTrue(all(record["conditions"].values()))
        for field in ("minimum_purchase_usd", "actual_cash_received_usd", "prepayment_usd", "actual_usage", "revenue_recognized_usd"):
            self.assertIsNone(record[field])
        self.assertFalse(record["human_evidence_approved"])
        self.assertFalse(record["automatic_h1_admission"])
        self.assertEqual(record["known_at"], "2025-09-25")
        self.assertEqual(record["event_date"], "2025-09-23")
        self.assertEqual(record["existing_msa_date"], "2025-05-08")
        self.assertIsNone(record["accepted_at_source_timezone"])

    def test_values_are_extracted_instead_of_returning_a_hardcoded_amount_or_term(self):
        changed = SYNTHETIC_DOCUMENT.replace(b"$6.5 billion", b"$7.25 billion").replace(b"May 31, 2031", b"June 30, 2032")
        record = self.parse(changed)
        self.assertEqual(record["maximum_commitment_usd"], 7_250_000_000)
        self.assertEqual(record["commitment_end_date"], "2032-06-30")

    def test_source_drift_is_closed_for_missing_maximum_or_conditions(self):
        changes = (
            (b"up to approximately", b"exactly"),
            (b"Subject to any termination described below", b"Unconditionally"),
            (b"delivery and availability of service requirements", b"normal operations"),
            (b"Either party may terminate", b"Neither party can terminate"),
            (b"new order form", b"nonbinding discussion"),
            (b"$6.5 billion", b"$6..5 billion"),
        )
        for old, new in changes:
            with self.subTest(anchor=old), self.assertRaises(CaptureError):
                self.parse(SYNTHETIC_DOCUMENT.replace(old, new))

    def test_hidden_anchors_do_not_make_an_error_page_a_valid_document(self):
        hidden = b'<html><body>Access denied<div style="display:none">' + SYNTHETIC_DOCUMENT + b'</div></body></html>'
        with self.assertRaisesRegex(CaptureError, "visible Item"):
            self.parse(hidden)

    def test_index_document_link_and_dates_are_cross_checked(self):
        for index in (
            SYNTHETIC_INDEX.replace(DOCUMENT_NAME.encode(), b"another-document.htm"),
            SYNTHETIC_INDEX.replace(b"2025-09-23", b"2025-09-22"),
            SYNTHETIC_INDEX.replace(ACCESSION.encode(), b"0001193125-25-999999"),
        ):
            with self.subTest(index=index[-50:]), self.assertRaises(CaptureError):
                self.parse(index=index)

    def test_offline_capture_preserves_raw_hash_locator_and_does_not_claim_network(self):
        result = self.collect()
        record = json.loads((self.output / "record.json").read_text())
        self.assertEqual(result["status"], "CAPTURED")
        self.assertEqual(record["retrieval_method"], "offline_import")
        self.assertFalse(record["remote_availability_verified_in_this_run"])
        self.assertTrue(record["source_is_synthetic"])
        for name, source in zip(("document", "index"), record["sources"]):
            self.assertEqual(source["sha256"], hashlib.sha256(self.documents[name]).hexdigest())
            self.assertEqual((self.output / source["raw_file"]).read_bytes(), self.documents[name])
            self.assertIsNone(source["remote_retrieved_at_utc"])
        self.assertEqual(record["locator"]["section"], "Item 1.01")
        self.assertTrue(record["source_original_excerpt"].endswith("under the Order Form."))
        self.assertEqual(verify_capture(self.output)["status"], "PASS")

    def test_identical_hash_is_idempotent_and_preserves_first_retrieval_time(self):
        first = self.collect()
        before = (self.output / "record.json").read_bytes()
        repeated = self.collect(timestamp="2026-10-04T01:00:00Z")
        self.assertEqual(repeated["status"], "ALREADY_CAPTURED")
        self.assertEqual(repeated["capture_id"], first["capture_id"])
        self.assertEqual(repeated["capture_count"], 1)
        self.assertEqual((self.output / "record.json").read_bytes(), before)

    def test_changed_raw_hash_keeps_the_previous_immutable_revision(self):
        first = self.collect()
        first_path = self.output / "captures" / first["capture_id"] / "record.json"
        original = first_path.read_bytes()
        changed = dict(self.documents, document=SYNTHETIC_DOCUMENT + b"\n<!-- synthetic revision -->\n")
        second = self.collect(changed, timestamp="2026-10-04T01:00:00Z")
        self.assertNotEqual(first["capture_id"], second["capture_id"])
        self.assertEqual(second["capture_count"], 2)
        self.assertEqual(first_path.read_bytes(), original)
        current = json.loads((self.output / "record.json").read_text())
        self.assertEqual(current["supersedes_capture_id"], first["capture_id"])
        self.assertEqual(verify_capture(self.output)["capture_count"], 2)

    def test_tampered_raw_source_is_rejected(self):
        self.collect()
        record = json.loads((self.output / "record.json").read_text())
        (self.output / record["sources"][0]["raw_file"]).write_bytes(b"tampered")
        with self.assertRaisesRegex(CaptureError, "raw source content hash"):
            verify_capture(self.output)

    def test_synthetic_fixture_cannot_be_accepted_by_the_public_import_cli(self):
        source = Path(self.temp.name) / "input"
        source.mkdir()
        (source / DOCUMENT_NAME).write_bytes(SYNTHETIC_DOCUMENT)
        (source / INDEX_NAME).write_bytes(SYNTHETIC_INDEX)
        stderr = io.StringIO()
        with contextlib.redirect_stderr(stderr):
            result = main(["--source-dir", str(source), "--output-dir", str(self.output)])
        self.assertEqual(result, 1)
        self.assertIn("synthetic fixture", stderr.getvalue())
        self.assertFalse((self.output / "record.json").exists())
        failures = list((self.output / "acquisition_failures").glob("*.json"))
        self.assertEqual(len(failures), 1)
        self.assertFalse(json.loads(failures[0].read_text())["accepted_record_created"])

    def test_verify_only_replays_saved_capture_without_any_network_call(self):
        self.collect()
        with patch("scripts.collect_customer_commitment.fetch_source", side_effect=AssertionError("network forbidden")), contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(main(["--verify-only", "--output-dir", str(self.output)]), 0)

    def test_http_403_is_not_a_success_or_source_record_and_contact_is_not_stored(self):
        error = HTTPError(SOURCE_URLS["document"], 403, "blocked TEST_USER_AGENT_DO_NOT_PERSIST", {}, None)
        opener = unittest.mock.Mock()
        opener.open.side_effect = error
        stderr = io.StringIO()
        with patch("scripts.collect_customer_commitment.build_opener", return_value=opener), contextlib.redirect_stderr(stderr):
            result = main(["--output-dir", str(self.output), "--user-agent", "TEST_USER_AGENT_DO_NOT_PERSIST"])
        self.assertEqual(result, 1)
        self.assertNotIn("TEST_USER_AGENT_DO_NOT_PERSIST", stderr.getvalue())
        self.assertFalse((self.output / "record.json").exists())
        receipts = list((self.output / "acquisition_failures").glob("*.json"))
        self.assertEqual(len(receipts), 1)
        raw = receipts[0].read_text()
        self.assertNotIn("TEST_USER_AGENT_DO_NOT_PERSIST", raw)
        self.assertEqual(json.loads(raw)["http_status"], 403)
        self.assertEqual(json.loads(raw)["sources_obtained_before_failure"], [])

    def test_network_requires_an_identifying_user_agent_before_requesting(self):
        with patch("scripts.collect_customer_commitment.build_opener", side_effect=AssertionError("request forbidden")):
            with self.assertRaisesRegex(CaptureError, "User-Agent"):
                fetch_source(SOURCE_URLS["document"], "")

    def test_only_bounded_sec_urls_and_safe_output_paths_are_allowed(self):
        for url in (
            SOURCE_URLS["document"].replace("www.sec.gov", "example.com"),
            SOURCE_URLS["document"].replace("https://", "http://"),
            SOURCE_URLS["document"] + "?token=secret",
            "https://www.sec.gov/Archives/another-case.htm",
        ):
            with self.subTest(url=url), self.assertRaises(CaptureError):
                validate_source_url(url)
        with self.assertRaisesRegex(CaptureError, "parent traversal"):
            capture(self.output / ".." / "outside", self.documents, mode="offline_import", allow_synthetic=True)

    def test_empty_and_oversize_source_fail_without_candidate_record(self):
        for raw in (b"", b"x" * 1_048_577):
            with self.subTest(size=len(raw)), self.assertRaises(CaptureError):
                self.parse(raw)
        self.assertFalse((self.output / "record.json").exists())

    def test_issuer_metadata_does_not_claim_observed_sec_accession_or_acceptance_clock(self):
        record = parse_issuer_case(SYNTHETIC_DOCUMENT, synthetic_issuer_feed(), allow_synthetic=True)
        self.assertEqual(record["source_route"], "issuer")
        self.assertIsNone(record["accession"])
        self.assertFalse(record["accession_observed_in_raw_source"])
        self.assertEqual(record["canonical_sec_reference"]["accession"], ACCESSION)
        self.assertFalse(record["sec_raw_byte_identity_verified"])
        self.assertEqual(record["canonical_sec_match_status"], "RESEARCH_REFERENCE_REQUIRES_REVIEW_NOT_AUTOMATED_MATCH")
        self.assertIsNone(record["accepted_at_source"])
        self.assertEqual(record["known_at"], "2025-09-25")
        self.assertEqual(record["known_at_precision"], "day")
        self.assertEqual(record["maximum_commitment_usd"], 6_500_000_000)
        self.assertEqual(record["amount_qualifiers"], ["UP_TO", "APPROXIMATE", "CONDITIONAL"])

    def test_issuer_parser_extracts_changed_amount_from_the_document(self):
        document = SYNTHETIC_DOCUMENT.replace(b"$6.5 billion", b"$6.75 billion")
        record = parse_issuer_case(document, synthetic_issuer_feed(), allow_synthetic=True)
        self.assertEqual(record["maximum_commitment_usd"], 6_750_000_000)

    def test_issuer_feed_identity_document_url_and_cover_date_drift_is_rejected(self):
        changes = (
            lambda row: row.update(FilingId=999999),
            lambda row: row.update(StockSymbol="0000000001"),
            lambda row: row.update(StockExchange="NASDAQ"),
            lambda row: row.update(FilingTypeMnemonic="10-K"),
            lambda row: row.update(FilingDate="09/26/2025 00:00:00"),
            lambda row: row["DocumentList"][0].update(Url="https://example.com/filing.html"),
        )
        for change in changes:
            with self.subTest(change=change), self.assertRaises(CaptureError):
                parse_issuer_case(SYNTHETIC_DOCUMENT, synthetic_issuer_feed(change), allow_synthetic=True)

    def test_issuer_duplicate_filing_id_is_rejected(self):
        metadata = json.loads(synthetic_issuer_feed())
        metadata["GetEdgarFilingListResult"].append(metadata["GetEdgarFilingListResult"][0].copy())
        with self.assertRaisesRegex(CaptureError, "duplicated"):
            parse_issuer_case(SYNTHETIC_DOCUMENT, json.dumps(metadata).encode(), allow_synthetic=True)

    def test_issuer_main_document_anchor_drift_is_rejected(self):
        document = SYNTHETIC_DOCUMENT.replace(b"D17274D8K_HTM", b"DIFFERENT_DOCUMENT_HTM")
        with self.assertRaisesRegex(CaptureError, "main-document anchor"):
            parse_issuer_case(document, synthetic_issuer_feed(), allow_synthetic=True)

    def test_synthetic_feed_cannot_be_promoted_with_an_unmarked_document(self):
        document = SYNTHETIC_DOCUMENT.replace(b"SYNTHETIC TEST FIXTURE", b"UNMARKED TEST DOCUMENT")
        with self.assertRaisesRegex(CaptureError, "synthetic issuer feed"):
            parse_issuer_case(document, synthetic_issuer_feed())
        record = parse_issuer_case(document, synthetic_issuer_feed(), allow_synthetic=True)
        self.assertTrue(record["source_is_synthetic"])

    def test_sec_index_only_synthetic_marker_is_rejected_by_cli_and_remains_synthetic(self):
        document = SYNTHETIC_DOCUMENT.replace(b"SYNTHETIC TEST FIXTURE", b"UNMARKED TEST DOCUMENT")
        record = parse_case(document, SYNTHETIC_INDEX, allow_synthetic=True)
        self.assertTrue(record["source_is_synthetic"])
        source = Path(self.temp.name) / "sec-marker-input"
        source.mkdir()
        (source / DOCUMENT_NAME).write_bytes(document)
        (source / INDEX_NAME).write_bytes(SYNTHETIC_INDEX)
        with contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(main(["--source-dir", str(source), "--output-dir", str(self.output)]), 1)
        self.assertFalse((self.output / "record.json").exists())

    def test_issuer_feed_only_synthetic_marker_is_rejected_by_cli(self):
        document = SYNTHETIC_DOCUMENT.replace(b"SYNTHETIC TEST FIXTURE", b"UNMARKED TEST DOCUMENT")
        source = Path(self.temp.name) / "issuer-marker-input"
        source.mkdir()
        (source / ISSUER_DOCUMENT_NAME).write_bytes(document)
        (source / ISSUER_FEED_NAME).write_bytes(synthetic_issuer_feed())
        with contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(main(["--issuer-source-dir", str(source), "--output-dir", str(self.output)]), 1)
        self.assertFalse((self.output / "record.json").exists())

    def test_offline_issuer_capture_preserves_actual_roles_urls_and_json_raw_hash(self):
        documents = {"document": SYNTHETIC_DOCUMENT, "feed": synthetic_issuer_feed()}
        result = capture(self.output, documents, mode="offline_import", source_route="issuer", allow_synthetic=True)
        record = json.loads((self.output / "record.json").read_text())
        self.assertEqual(result["status"], "CAPTURED")
        self.assertFalse(record["remote_availability_verified_in_this_run"])
        self.assertEqual([source["source_role"] for source in record["sources"]], ["ISSUER_HOSTED_FILING_MIRROR", "ISSUER_FILING_METADATA_FEED"])
        for name, source in zip(("document", "feed"), record["sources"]):
            self.assertEqual(source["source_url"], ISSUER_SOURCE_URLS[name])
            self.assertEqual(source["sha256"], hashlib.sha256(documents[name]).hexdigest())
            self.assertEqual((self.output / source["raw_file"]).read_bytes(), documents[name])
        self.assertTrue(record["sources"][1]["raw_file"].endswith(".json"))
        self.assertEqual(verify_capture(self.output)["status"], "PASS")

    def test_issuer_url_route_is_explicit_and_cannot_expand_to_another_mirror(self):
        validate_source_url(ISSUER_SOURCE_URLS["document"], "issuer")
        validate_source_url(ISSUER_SOURCE_URLS["feed"], "issuer")
        with self.assertRaises(CaptureError):
            validate_source_url(ISSUER_SOURCE_URLS["document"], "sec")
        with self.assertRaises(CaptureError):
            validate_source_url(ISSUER_SOURCE_URLS["document"].replace("a5d34350", "b5d34350"), "issuer")


if __name__ == "__main__":
    unittest.main()
