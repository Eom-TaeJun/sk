"""Validate a public research bundle without admitting it to H1 or calling APIs."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_BUNDLE = ROOT / "data/research/semiconductor_supply_chain/2026-10-03"
CANDIDATE = "RESEARCH_CANDIDATE_NOT_GOVERNED_EVIDENCE"
PRIVATE_FIELDS = {
    "existing_access", "existing_keys_names_only", "auth_status", "local_file",
    "schema_file", "registered_new_accounts", "actual_api_keys_used",
}
SENSITIVE = re.compile(
    r"(?<![A-Za-z0-9])[A-Za-z]:[\\/]"
    r"|-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"
    r"|\bgh[pousr]_[A-Za-z0-9]{30,}\b"
    r"|\bgithub_pat_[A-Za-z0-9_]{30,}\b"
    r"|\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
)


def walk(value, path="$", problems=None):
    problems = [] if problems is None else problems
    if isinstance(value, dict):
        for key, nested in value.items():
            here = f"{path}.{key}"
            if key in PRIVATE_FIELDS:
                problems.append(f"{here}: user-specific or local-only field")
            walk(nested, here, problems)
    elif isinstance(value, list):
        for index, nested in enumerate(value):
            walk(nested, f"{path}[{index}]", problems)
    elif isinstance(value, str) and SENSITIVE.search(value):
        problems.append(f"{path}: sensitive value pattern; value withheld")
    return problems


def validate(bundle: Path = DEFAULT_BUNDLE) -> dict:
    bundle = bundle.resolve()
    manifest = json.loads((bundle / "manifest.json").read_text(encoding="utf-8"))
    errors = []
    documents = {"manifest.json": manifest}
    listed = set()
    for entry in manifest["artifacts"]:
        name = entry["file"]
        path = (bundle / name).resolve()
        if path.parent != bundle or name in listed:
            errors.append("manifest: invalid or duplicate artifact path")
            continue
        listed.add(name)
        if not path.is_file():
            errors.append(f"{name}: missing artifact")
            continue
        raw = path.read_bytes()
        if hashlib.sha256(raw).hexdigest() != entry["sha256"] or len(raw) != entry["bytes"]:
            errors.append(f"{name}: hash or byte-length mismatch")
        documents[name] = json.loads(raw.decode("utf-8"))
    actual = {p.name for p in bundle.iterdir() if p.is_file()}
    if actual != listed | {"manifest.json"}:
        errors.append("manifest: artifact membership mismatch")
    for name, doc in documents.items():
        errors.extend(f"{name}:{item}" for item in walk(doc))
        context = doc.get("publication_context", {})
        if context.get("status") != CANDIDATE:
            errors.append(f"{name}: missing candidate intake boundary")
        for key in ("empirical_dataset_admitted", "human_gate_6_approved",
                    "predictive_validity_established", "continuous_collection_implemented"):
            if context.get(key) is not False:
                errors.append(f"{name}: {key} must remain false in this intake bundle")
        if context.get("as_of") != manifest.get("as_of"):
            errors.append(f"{name}: inconsistent research cutoff")

    graph = documents["supply_chain_map_v3.json"]
    signals = documents["signal_catalog_v2.json"]
    roadmap = documents["collection_roadmap_v2.json"]
    geo = documents["verified_facilities.geojson"]

    def ids(records, field, label):
        values = [record.get(field) for record in records]
        if any(not isinstance(value, str) or not value for value in values):
            errors.append(f"{label}: missing IDs")
        if len(values) != len(set(values)):
            errors.append(f"{label}: duplicate IDs")
        return set(values)

    actor_ids = ids(graph["companies"], "id", "actors")
    relation_ids = ids(graph["relations"], "id", "relations")
    facility_ids = ids(graph["facilities"], "facility_id", "facilities")
    ids(graph["events"], "event_id", "events")
    ids(graph["contracts"], "contract_id", "contracts")
    metric_ids = ids(signals["metrics"], "id", "metrics")
    for actor in graph["companies"]:
        if actor.get("parent_id") and actor["parent_id"] not in actor_ids:
            errors.append(f"actor {actor['id']}: unknown parent")
    for relation in graph["relations"]:
        if relation["from"] not in actor_ids or relation["to"] not in actor_ids:
            errors.append(f"relation {relation['id']}: dangling actor reference")
        if relation.get("intake_status") != CANDIDATE:
            errors.append(f"relation {relation['id']}: missing intake status")
    for facility in graph["facilities"]:
        if facility["entity_id"] not in actor_ids:
            errors.append(f"facility {facility['facility_id']}: dangling actor reference")
    for event in graph["events"]:
        if event.get("relation_id") and event["relation_id"] not in relation_ids:
            errors.append(f"event {event['event_id']}: dangling relation reference")
        if not event.get("stage_raw") or event.get("normalized_stage") is not None:
            errors.append(f"event {event['event_id']}: raw stage or normalization boundary lost")
    for case in graph["case_paths"]:
        if not set(case.get("relation_ids", [])) <= relation_ids:
            errors.append(f"case {case['id']}: dangling relation reference")
        if not set(case.get("facility_ids", [])) <= facility_ids:
            errors.append(f"case {case['id']}: dangling facility reference")
    for contract in graph["contracts"]:
        for key in ("borrower_id", "parent_guarantor_id", "lender_cohort_id"):
            if contract.get(key) and contract[key] not in actor_ids:
                errors.append(f"contract {contract['contract_id']}: dangling {key}")
        if not set(contract.get("arranger_ids", [])) <= actor_ids:
            errors.append(f"contract {contract['contract_id']}: dangling arranger reference")
    for key in ("complete_world_map", "continuous_collectors_running", "validated_predictive_signal"):
        if graph.get(key) is not False:
            errors.append(f"graph: {key} must remain false")
    for metric in signals["metrics"]:
        if metric.get("leading_prediction_validated") is not False:
            errors.append(f"metric {metric['id']}: predictive validity not established")
    first = signals["first_collection_ids"]
    if len(first) != len(set(first)) or not set(first) <= metric_ids:
        errors.append("signals: invalid first-collection references")
    if set(roadmap["first_metric_ids"]) != set(first):
        errors.append("roadmap: first-collection metrics disagree")

    facilities = {f["facility_id"]: f for f in graph["facilities"]}
    expected_points = {f["facility_id"] for f in graph["facilities"] if f.get("coordinates")}
    point_ids = [feature.get("id") for feature in geo["features"]]
    if geo.get("type") != "FeatureCollection" or set(point_ids) != expected_points or len(point_ids) != len(set(point_ids)):
        errors.append("GeoJSON: point coverage must match verified facility coordinates")
    for feature in geo["features"]:
        facility = facilities.get(feature.get("id"))
        if not facility or not facility.get("coordinates"):
            errors.append("GeoJSON: unverified facility point")
            continue
        coordinate = facility["coordinates"]
        wanted = [coordinate["longitude"], coordinate["latitude"]]
        if feature["geometry"] != {"type": "Point", "coordinates": wanted}:
            errors.append(f"GeoJSON {feature['id']}: coordinate or order mismatch")
        if not (-180 <= wanted[0] <= 180 and -90 <= wanted[1] <= 90):
            errors.append(f"GeoJSON {feature['id']}: coordinate range invalid")
        properties = feature["properties"]
        if properties.get("coordinate_source_url") != coordinate["source_url"]:
            errors.append(f"GeoJSON {feature['id']}: source trace mismatch")
        if properties.get("generator_statuses") != facility.get("generator_statuses", []):
            errors.append(f"GeoJSON {feature['id']}: raw generator status lost")
        if properties.get("coordinate_scope") != "POWER_PLANT_NOT_CUSTOMER_DATA_CENTER":
            errors.append(f"GeoJSON {feature['id']}: coordinate scope lost")

    expected_coverage = {
        "actors": len(actor_ids), "relations": len(relation_ids),
        "facilities": len(facility_ids), "coordinate_facilities": len(expected_points),
        "case_paths": len(graph["case_paths"]), "capture_specs": len(graph["signal_capture_specs"]),
        "candidate_metrics": len(metric_ids), "first_collection_metrics": len(first),
        "complete_world_map": False,
    }
    if manifest["coverage"] != expected_coverage:
        errors.append("manifest: coverage counts disagree with data")
    if errors:
        raise ValueError("\n".join(errors))
    return {"status": "PASS", "scope": "offline research-package validation only",
            "artifact_count": len(documents), "coverage": expected_coverage,
            "live_sources_rechecked": False, "evidence_approved": False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bundle", type=Path, default=DEFAULT_BUNDLE)
    args = parser.parse_args()
    print(json.dumps(validate(args.bundle), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
