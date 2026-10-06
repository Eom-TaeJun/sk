"""Offline integrity/reference checks for the dated API and purpose packages.

Run from a clone with only the Python standard library. This reads existing
artifacts; it does not call providers, write receipts, approve Evidence, or
validate source truth, demand, causality, legal effect, or leadingness.
"""
from __future__ import annotations

import argparse
from collections import Counter
from datetime import datetime, timedelta
import hashlib
import json
from pathlib import Path, PurePosixPath
import re


ROOT = Path(__file__).resolve().parents[1]
API_DIR = "data/research/api_signal_feasibility/2026-10-05"
PURPOSE_DIR = "data/research/indicator_purpose_review/2026-10-05"
PURPOSE_DOC = "docs/research/supply_chain/indicator_collection_purpose.md"
CANDIDATE = "RESEARCH_CANDIDATE_NOT_GOVERNED_EVIDENCE"
API_FILES = {
    "ai_usage_technology.json", "finance_macro_etf.json",
    "power_policy_infrastructure.json", "taiwan_company_activity.json",
    "trade_industry_materials.json", "collection_index.json", "manifest.json",
}
PRIOR_INPUT_HASHES = {
    "data/research/semiconductor_supply_chain/2026-10-03/supply_chain_map_v3.json": "0f6e7130d9d8ecc7bdb243e44c504b9b32ecfdbec19dd6c05bd37ca544efa138",
    "data/research/semiconductor_supply_chain/2026-10-03/api_issuance_plan_v3.json": "7d4e25761fa99f704660537f9a8e31d0bbef5263fcb4b4264c75156030e19be2",
    "data/research/semiconductor_macro_structure/2026-10-04/sources.json": "891e1f83bb78795396b98358a16de63e3bd64a314955e233d50d6867a6fc43c8",
    "data/research/ai_technology_memory_links/2026-10-04/links.json": "6cd95b606851dc66e86c36eb498258093eaf8967bcc24e402de517a4d8ec2b45",
    "data/research/semiconductor_industry_routes/2026-10-05/product_routes.json": "f6d7e5c8d62aa6d46ed05d87b77fceec2d9eccfb84fd6a4a96aabc1a653db283",
    "data/research/semiconductor_industry_routes/2026-10-05/policy_infrastructure_routes.json": "bedba1e6430e59d44501c95d3fd780feffbb8b3df5302a5a5c62b6cd362c1ea8",
}
# These are review objects, including overlapping contracts, not 40 independent
# economic variables. Pin the dated selection rather than trusting its own count.
PRIORITY_IDS = {
    "핵심 질문": "AIAPI04-MODEL-VERSION-TASK AIAPI05-SOFTWARE-RELEASE ROOTAPI01-CUSTOMER-CASH ROOTAPI02-CONTRACT-FILING-EVENT ROOTAPI03-KR-CASH-INVENTORY ROOTAPI04-KR-FILING-SEARCH TM-04-KOSIS".split(),
    "관계 확인 후": "AIAPI01-PLATFORM-TOKENS API-PP-01 API-PP-02 API-PP-05 API-PP-06 API-PP-07 API-PP-08 API-PP-09 API-PP-10 API-PP-14".split(),
    "보조": "AIAPI02-MODEL-DOWNLOADS30 ROOTAPI05-US-PRODUCTION ROOTAPI06-US-UTILIZATION ROOTAPI07-ELECTRICAL-BACKLOG ROOTAPI09-ETF-POSITION API-PP-03 API-PP-04 API-PP-11 API-PP-12 API-PP-13 TWAPI01-MONTHLY-REVENUE TWAPI02-PROVIDER-COMPARATIVES TM-01-UN-COMTRADE TM-02-EUROSTAT TM-03-OECD-TIVA TM-05-KOREA-CUSTOMS TM-06-USGS-MATERIAL-FILES".split(),
    "분석 보류": "AIAPI03-MODEL-LIKES AIAPI06-DEVELOPER-INTEREST ROOTAPI10-ETF-NETCREATION".split(),
    "필수 검증": "AIAPI07-REPO-FRESHNESS ROOTAPI08-FX-CONTROL TWAPI03-PERIOD-COVERAGE-FRESHNESS".split(),
}
EXPECTED_PRIORITIES = {ident: label for label, ids in PRIORITY_IDS.items() for ident in ids}
FALSE_FIELDS = {
    "governed_evidence", "human_evidence_approved", "h1_admitted",
    "human_approved", "h1_eligible", "governed_dataset_changed",
    "predictive_signal_validated", "predictive_validity_established",
    "strong_inference_approved", "continuous_collection_implemented",
    "recurring_collection_implemented", "authenticated_collection_implemented",
    "new_data_api_calls_performed", "accounts_created", "keys_issued",
    "private_credentials_read", "external_messages_sent",
    "credential_inventory_included", "public_full_raw_responses_included",
    "raw_originals_redistributed", "public_full_response_included",
    "raw_original_redistributed", "raw_redistributed",
    "actual_demand_supply_or_cash_counterparty_validated",
    "observed_change_this_review", "empirical_leadingness_validated",
}
SENSITIVE = re.compile(
    r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"
    r"|(?<![A-Za-z0-9])[A-Za-z]:[\\/]"
    r"|\.secrets[/\\]|-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"
    r"|\bgh[pousr]_[A-Za-z0-9]{30,}\b|\bgithub_pat_[A-Za-z0-9_]{30,}\b"
)


def require(condition, message):
    if not condition:
        raise ValueError(message)


def local_file(root: Path, relative: str) -> Path:
    require(isinstance(relative, str) and relative and "\\" not in relative,
            "invalid local artifact path")
    path = PurePosixPath(relative)
    require(not path.is_absolute() and ".." not in path.parts and ":" not in relative,
            "artifact path escapes workspace")
    resolved = (root / path).resolve()
    require(resolved.is_relative_to(root) and resolved.is_file(),
            f"missing or escaping artifact: {relative}")
    return resolved


def pointer(value, reference: str):
    require(isinstance(reference, str) and reference.startswith("/"), "invalid JSON pointer")
    try:
        for token in reference[1:].split("/"):
            require(not re.search(r"~(?![01])", token), "invalid JSON pointer escape")
            token = token.replace("~1", "/").replace("~0", "~")
            if isinstance(value, list):
                require(bool(re.fullmatch(r"0|[1-9][0-9]*", token)), "invalid array pointer")
                value = value[int(token)]
            else:
                value = value[token]
        return value
    except (KeyError, IndexError, TypeError) as error:
        raise ValueError(f"broken JSON pointer: {reference}") from error


def unique_rows(rows, key, expected_count, label):
    ids = [row[key] for row in rows]
    require(len(ids) == expected_count and len(set(ids)) == expected_count,
            f"{label}: missing or duplicate IDs")
    return set(ids)


def inspect_public(value, label):
    if isinstance(value, dict):
        for key, nested in value.items():
            if key in FALSE_FIELDS:
                require(nested is False, f"{label}: candidate boundary changed: {key}")
            if key.endswith("_at_utc") and nested is not None:
                try:
                    parsed = datetime.fromisoformat(nested.replace("Z", "+00:00"))
                except (AttributeError, TypeError, ValueError) as error:
                    raise ValueError(f"{label}: invalid UTC instant: {key}") from error
                require(parsed.utcoffset() == timedelta(0), f"{label}: non-UTC instant: {key}")
            inspect_public(nested, label)
    elif isinstance(value, list):
        for nested in value:
            inspect_public(nested, label)


def validate(workspace: Path = ROOT) -> dict:
    root = workspace.resolve()
    documents = {}

    def read(relative):
        if relative not in documents:
            raw = local_file(root, relative).read_bytes()
            require(raw.endswith(b"\n") and b"\r" not in raw and not raw.startswith(b"\xef\xbb\xbf"),
                    f"{relative}: expected UTF8 no-BOM LF artifact")
            text = raw.decode("utf8")
            require(not SENSITIVE.search(text), f"{relative}: sensitive public value pattern")
            documents[relative] = json.loads(text)
            inspect_public(documents[relative], relative)
        return documents[relative]

    def refs(entries, size_key, expected_paths):
        paths = [entry["path"] for entry in entries]
        require(len(paths) == len(set(paths)) and set(paths) == set(expected_paths),
                "manifest reference membership changed")
        for entry in entries:
            raw = local_file(root, entry["path"]).read_bytes()
            require(len(raw) == entry[size_key] and hashlib.sha256(raw).hexdigest() == entry["sha256"],
                    f"{entry['path']}: hash or byte-length mismatch")

    api_paths = {f"{API_DIR}/{name}" for name in API_FILES}
    purpose_paths = {f"{PURPOSE_DIR}/manifest.json", f"{PURPOSE_DIR}/purpose_registry.json"}
    for directory, names in ((API_DIR, API_FILES), (PURPOSE_DIR, {"manifest.json", "purpose_registry.json"})):
        require({p.name for p in (root / directory).glob("*.json")} == names,
                f"{directory}: JSON package membership changed")
    for path in sorted(api_paths | purpose_paths):
        read(path)
    api_manifest = read(f"{API_DIR}/manifest.json")
    index = read(f"{API_DIR}/collection_index.json")
    manifest = read(f"{PURPOSE_DIR}/manifest.json")
    registry = read(f"{PURPOSE_DIR}/purpose_registry.json")
    for path, document in documents.items():
        if path.endswith("trade_industry_materials.json"):
            require(document.get("research_candidate") is True, "trade contract lost candidate status")
            required_flags = {"human_approved", "h1_eligible", "governed_dataset_changed"}
        else:
            require(document.get("status") == CANDIDATE, f"{path}: lost candidate status")
            required_flags = {"human_evidence_approved", "h1_admitted"}
            if not path.endswith(f"{API_DIR}/manifest.json"):
                required_flags.add("governed_evidence")
        require(all(document.get(flag) is False for flag in required_flags),
                f"{path}: required candidate flags missing or changed")
    refs(api_manifest["files"], "byte_length", api_paths - {f"{API_DIR}/manifest.json"})
    refs(api_manifest["preserved_input_refs"], "byte_length", PRIOR_INPUT_HASHES)
    require(index["preserved_input_refs"] == api_manifest["preserved_input_refs"],
            "index prior-input references disagree with manifest")
    for ref in api_manifest["preserved_input_refs"]:
        require(ref["sha256"] == PRIOR_INPUT_HASHES[ref["path"]], "prior immutable input digest changed")
    refs(manifest["files"], "byte_size", {f"{PURPOSE_DIR}/purpose_registry.json"})
    refs(manifest["immutable_input_refs"], "byte_size", api_paths)
    require(manifest["immutable_input_refs"] == registry["immutable_input_refs"],
            "purpose immutable references disagree")
    packet_paths = api_paths - {f"{API_DIR}/manifest.json", f"{API_DIR}/collection_index.json"}
    refs(index["packet_refs"], "byte_length", packet_paths)
    require(registry["source_index_path"] == f"{API_DIR}/collection_index.json", "wrong purpose source index")

    family_ids = unique_rows(index["families"], "family_id", 22, "families")
    numbered = unique_rows(index["numbered_indicators"], "indicator_id", 34, "numbered indicators")
    contracts = unique_rows(index["trade_industry_measurement_contracts"], "contract_id", 6, "measurement contracts")
    require(not numbered & contracts and numbered | contracts == set(EXPECTED_PRIORITIES), "exact 40 review ID set changed")

    def original(row):
        require(row["packet_path"] in packet_paths, "index points outside packet manifest")
        return pointer(read(row["packet_path"]), row["json_pointer"])

    probe_owners = {}
    for row in index["families"]:
        source = original(row)
        require(source.get("id", source.get("family_id")) == row["family_id"], "family pointer/ID mismatch")
        probe_ids = list(source.get("probe_ids", []))
        for endpoint in source.get("endpoints", []):
            if isinstance(endpoint, dict):
                probe_ids.extend(endpoint.get("probe_receipt_ids", []))
        for probe_id in set(probe_ids):
            require(probe_id not in probe_owners, "probe references more than one source family")
            probe_owners[probe_id] = row["family_id"]
    for row in index["numbered_indicators"]:
        source = original(row)
        require(source.get("id", source.get("metric_id")) == row["indicator_id"] and row["family_id"] in family_ids,
                "indicator pointer/ID/family mismatch")
    for row in index["trade_industry_measurement_contracts"]:
        require(original(row) == row["measurement_contract"], "measurement-contract pointer mismatch")
    access_ids = unique_rows(index["bounded_access_results"], "probe_id", 23, "bounded attempts")
    require(access_ids <= set(probe_owners), "bounded attempt has no original family reference")
    failed_modes = Counter()
    success_families = set()
    for row in index["bounded_access_results"]:
        source = original(row)
        require(source.get("id", source.get("probe_id")) == row["probe_id"], "access pointer/ID mismatch")
        if row["result"] == "FAILED_NO_DATA":
            # FRED CSV failure is a file attempt, while a failed SDMX API
            # request is still API access. Use the original receipt's request
            # mode rather than accepting the index's reclassification.
            source_mode = "STATIC_DATA_FILE" if source.get("mode") == "csv" else "DATA_API"
            require(row["acquisition_mode"] == source_mode, "failed-attempt mode disagrees with original receipt")
            failed_modes[source_mode] += 1
        if row["result"] == "NON_EMPTY_API_DATA":
            nonempty = (row["returned_count_as_recorded"] or 0) > 0 or (
                source.get("top_level_type") == "dict" and source.get("sample_rows") and source.get("actual_fields"))
            require(row["http_status"] == 200 and nonempty, "recorded API response is not HTTP200/nonempty")
            success_families.add(probe_owners[row["probe_id"]])
    counts = Counter(row["result"] for row in index["bounded_access_results"])
    require(counts == {"NON_EMPTY_API_DATA": 11, "METADATA_RETURNED_NOT_OBSERVATION": 2,
                       "NON_EMPTY_FILE_DATA": 1, "DOCUMENT_FILE_RECEIVED_NOT_API_DATA": 2, "FAILED_NO_DATA": 7},
            "bounded access result classifications changed")
    actual_summary = {
        "source_families_including_files": len(index["families"]),
        "numbered_indicator_definitions": len(index["numbered_indicators"]),
        "trade_industry_family_measurement_contracts": len(index["trade_industry_measurement_contracts"]),
        "bounded_data_access_attempts": len(index["bounded_access_results"]),
        "non_empty_data_api_responses": counts["NON_EMPTY_API_DATA"],
        "distinct_data_api_families_with_data": len(success_families),
        "metadata_responses": counts["METADATA_RETURNED_NOT_OBSERVATION"],
        "static_data_file_responses": counts["NON_EMPTY_FILE_DATA"],
        "static_document_file_responses": counts["DOCUMENT_FILE_RECEIVED_NOT_API_DATA"],
        "failed_data_api_attempts": failed_modes["DATA_API"],
        "failed_static_file_attempts": failed_modes["STATIC_DATA_FILE"],
    }
    require(index["summary_counts"] == actual_summary and api_manifest["summary_counts"] == actual_summary,
            "access summary counts disagree with recorded arrays/results/families")
    require(index["exactly_one_next_task"]["implemented"] is False, "historical pilot boundary changed")

    question_ids = unique_rows(registry["question_contracts"], "question_id", 7, "questions")
    require(question_ids == {f"Q{i}" for i in range(1, 8)}, "question ID set changed")
    unique_rows(registry["review_entries"], "review_id", 40, "purpose entries")
    require({row["review_id"] for row in registry["review_entries"]} == set(EXPECTED_PRIORITIES), "purpose review ID set changed")
    require(set(registry["priority_definitions_ko"]) == set(PRIORITY_IDS), "priority definitions changed")
    for row in registry["review_entries"]:
        ident = row["review_id"]
        expected_unit = "NUMBERED_INDICATOR" if ident in numbered else "FAMILY_MEASUREMENT_CONTRACT"
        require(row["review_unit"] == expected_unit, "purpose review unit changed")
        source = pointer(index, row["source_index_pointer"])
        require(source.get("indicator_id", source.get("contract_id")) == ident, "purpose index pointer/ID mismatch")
        require((source["packet_path"], source["json_pointer"]) ==
                (row["source_packet_path"], row["source_packet_pointer"]), "purpose packet pointer disagrees with index")
        require(row["collection_priority_ko"] == EXPECTED_PRIORITIES[ident], "purpose classification changed")
        require(set(row["question_ids"]) <= question_ids and bool(row["question_ids"]) ==
                (row["collection_priority_ko"] != "필수 검증"), "purpose question references changed")
        for key in ("actor_relationship_ko", "check_ko", "followup_action_ko", "prohibited_inference_ko", "readiness_ko"):
            require(isinstance(row[key], str) and row[key].strip(), f"purpose entry lacks {key}")
        require(row["priority_is_research_judgment"] is True, "purpose priority lost research judgment boundary")
        require(row["observed_change_this_review"] is False and row["empirical_leadingness_validated"] is False,
                "purpose observation/leadingness boundary changed")
    require(registry["exactly_one_next_task"]["implemented"] is False, "purpose next-task boundary changed")
    require(len(registry["common_validation_contract_ko"]) >= 6, "common validation contract missing")

    table = {}
    for line in local_file(root, PURPOSE_DOC).read_text(encoding="utf8").splitlines():
        match = re.fullmatch(r"\| `([^`]+)` \| ([^|]+) \| ([^|]+) \| ([^|]+) \|", line)
        if match:
            ident, _, _, priority = (part.strip() for part in match.groups())
            require(ident not in table, "duplicate purpose document ID")
            table[ident] = priority
    require(table == EXPECTED_PRIORITIES, "purpose document table/classification mismatch")
    for document in documents.values():
        for path in document.get("documentation_paths", []):
            local_file(root, path)  # Mutable navigation is not an immutable input.
    return {
        "status": "PASS", "scope": "offline dated research integrity and references only",
        "public_json_files": 9, "preserved_prior_inputs": 6,
        "review_objects": {"numbered_indicators": 34, "family_measurement_contracts": 6},
        "family_pointer_refs": 22, "access_pointer_refs": 23,
        "priority_counts_across_review_objects": dict(Counter(EXPECTED_PRIORITIES.values())),
        "live_sources_rechecked": False, "source_truth_validated": False,
        "evidence_approved": False, "predictive_validity_established": False,
    }


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace", type=Path, default=ROOT)
    args = parser.parse_args(argv)
    try:
        print(json.dumps(validate(args.workspace), ensure_ascii=False, indent=2))
        return 0
    except (OSError, UnicodeError, ValueError, KeyError, TypeError) as error:
        print(json.dumps({"status": "FAIL", "error": str(error)}, ensure_ascii=False))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
