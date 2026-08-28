from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter, defaultdict
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Iterable

from src.core.models import ContractError
from src.core.storage import content_digest, load_json, write_json

from .models import parse_aware_datetime, require_text
from .pilot import PilotDataset, PilotEventRecord, PilotSourceRecord, PilotSourceRegistry
from .registry import CandidateTrackRegistry, RegistryFreezeManifest
from .validation import SemanticContractError, validate_event_for_track


INGESTION_STATUSES = {"ACCEPTED", "HOLD", "REJECTED"}
COLLECTION_STATUSES = {
    "COLLECTED_WITH_PRIMARY_EVIDENCE",
    "COLLECTED_WITH_HOLD_ONLY",
    "COLLECTED_NO_MEASUREMENT_EVENT",
}
SEARCH_STATUSES = {"COMPLETE"}
NEGATIVE_SEARCH_RESULTS = {"EXPLICIT_NEGATIVE_OR_DELAY", "NOT_OBSERVED_PUBLICLY"}
MISSINGNESS_STATUSES = {
    "DISCLOSED",
    "UNKNOWN",
    "NOT_OBSERVED_PUBLICLY",
    "PRIVATE_OR_NOT_DISCLOSED",
    "HOLD",
}
FUTURE_DOMAINS = {
    "COMPETITION",
    "ECOSYSTEM_DEPENDENCY",
    "SUPPLY_PRODUCTION",
    "RAW_MATERIAL_LOGISTICS",
    "MACRO",
    "POLICY_GEOPOLITICS",
    "PRODUCT_MIX",
}
CAPABILITY_CLAIM_STATUSES = {
    "VERIFIED_PERFORMED_FACT",
    "VERIFIED_IMPLEMENTATION_FACT",
    "PENDING_EMPIRICAL_RESULT",
}
FORBIDDEN_EMPIRICAL_KEYS = {
    "lead_days",
    "lag_days",
    "realization_rate",
    "false_positive_rate",
    "signal_ranking",
    "h1_p_verdict",
    "h1_c_verdict",
    "h1_verdict",
    "h1_conclusion",
}


def _walk_keys(value: Any) -> Iterable[str]:
    if isinstance(value, dict):
        for key, nested in value.items():
            yield key
            yield from _walk_keys(nested)
    elif isinstance(value, list):
        for nested in value:
            yield from _walk_keys(nested)


def _require_no_empirical_results(value: Any) -> None:
    found = set(_walk_keys(value)) & FORBIDDEN_EMPIRICAL_KEYS
    if found:
        raise ContractError(
            "Gate 6 has not occurred; empirical H1 outputs are forbidden: "
            + ", ".join(sorted(found))
        )


def _archive_text(source: dict[str, Any]) -> str:
    return (
        "# Primary Source Archive\n\n"
        f"- Source ID: `{source['source_id']}`\n"
        f"- Revision: `{source['source_revision_id']}`\n"
        f"- Title: {source['title']}\n"
        f"- Publisher: {source['publisher']}\n"
        f"- Publication date: {source['publication_date']}\n"
        f"- URL: {source['url']}\n"
        f"- Accessed at: {source['accessed_at']}\n\n"
        "## Original excerpt\n\n"
        f"{source['excerpt']}\n\n"
        "## Locator\n\n"
        f"{source['locator']}\n\n"
        "## Archival boundary\n\n"
        "This repository archive preserves the quoted official-source excerpt and locator used "
        "for classification. It is not a full-page mirror and does not imply facts beyond the excerpt. "
        "Line breaks or ellipses mark selected or omitted source text where present.\n"
    )


@dataclass(frozen=True)
class TrackCollectionRecord:
    track_id: str
    collection_status: str
    supporting_search_status: str
    contradictory_search_status: str
    source_family_searches: dict[str, str]
    source_ids: list[str]
    event_ids: list[str]
    negative_search_result: str
    negative_source_ids: list[str]
    negative_search_note: str
    missingness: dict[str, str]
    gate6_readiness: str
    notes: str

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "TrackCollectionRecord":
        try:
            record = cls(**data)
        except TypeError as exc:
            raise ContractError(f"invalid Track collection fields: {exc}") from exc
        record.validate()
        return record

    def validate(self) -> None:
        require_text(self.track_id, "collection.track_id")
        if self.collection_status not in COLLECTION_STATUSES:
            raise ContractError(f"invalid collection_status: {self.collection_status}")
        if self.supporting_search_status not in SEARCH_STATUSES:
            raise ContractError("supporting primary-source search must be COMPLETE")
        if self.contradictory_search_status not in SEARCH_STATUSES:
            raise ContractError("contradictory primary-source search must be COMPLETE")
        if self.negative_search_result not in NEGATIVE_SEARCH_RESULTS:
            raise ContractError(f"invalid negative_search_result: {self.negative_search_result}")
        require_text(self.negative_search_note, "collection.negative_search_note")
        require_text(self.gate6_readiness, "collection.gate6_readiness")
        require_text(self.notes, "collection.notes")
        if not self.source_family_searches:
            raise ContractError("source_family_searches must preserve at least one searched family")
        for family, status in self.source_family_searches.items():
            require_text(family, "collection.source_family_searches key")
            if status not in {"FOUND", "SEARCHED_NOT_OBSERVED", "HOLD"}:
                raise ContractError(f"invalid source-family search status: {status}")
        if len(self.source_ids) != len(set(self.source_ids)):
            raise ContractError(f"duplicate source IDs in collection status: {self.track_id}")
        if len(self.event_ids) != len(set(self.event_ids)):
            raise ContractError(f"duplicate event IDs in collection status: {self.track_id}")
        if self.negative_search_result == "EXPLICIT_NEGATIVE_OR_DELAY" and not self.negative_source_ids:
            raise ContractError("explicit negative/delay status requires a primary Source")
        if self.negative_search_result == "NOT_OBSERVED_PUBLICLY" and self.negative_source_ids:
            raise ContractError("non-observation cannot cite a Source as explicit negative evidence")
        if not self.missingness:
            raise ContractError("collection missingness must be explicit")
        for field, status in self.missingness.items():
            require_text(field, "collection.missingness key")
            if status not in MISSINGNESS_STATUSES:
                raise ContractError(f"invalid missingness status: {status}")

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class CollectionStatusManifest:
    manifest_version: str
    created_at: str
    registry_content_hash: str
    records: list[TrackCollectionRecord]
    content_hash: str

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "CollectionStatusManifest":
        payload = dict(data)
        try:
            payload["records"] = [
                TrackCollectionRecord.from_dict(item) for item in payload["records"]
            ]
            manifest = cls(**payload)
        except (KeyError, TypeError) as exc:
            raise ContractError(f"invalid collection-status manifest: {exc}") from exc
        manifest.validate_shape()
        return manifest

    def hash_basis(self) -> dict[str, Any]:
        data = asdict(self)
        data.pop("content_hash")
        data["records"] = sorted(data["records"], key=lambda item: item["track_id"])
        return data

    def validate_shape(self) -> None:
        require_text(self.manifest_version, "collection_manifest.manifest_version")
        parse_aware_datetime(self.created_at, "collection_manifest.created_at")
        ids = [record.track_id for record in self.records]
        if ids != sorted(ids) or len(ids) != 24 or len(set(ids)) != 24:
            raise ContractError("collection manifest must contain the 24 sorted frozen Track IDs")
        expected = content_digest(self.hash_basis())
        if self.content_hash != expected:
            raise ContractError(
                f"collection manifest hash mismatch: expected {expected}, got {self.content_hash}"
            )

    def validate_links(
        self,
        registry: CandidateTrackRegistry,
        source_registry: PilotSourceRegistry,
        dataset: "CorpusDataset",
    ) -> None:
        self.validate_shape()
        if self.registry_content_hash != registry.content_hash:
            raise ContractError("collection manifest does not match frozen Track registry")
        expected_tracks = sorted(registry.as_map())
        if [record.track_id for record in self.records] != expected_tracks:
            raise ContractError("collection status does not cover the exact frozen Track population")
        source_ids = set(source_registry.as_map())
        events = {record.event.event_id: record for record in dataset.records}
        for record in self.records:
            if not set(record.source_ids).issubset(source_ids):
                raise ContractError(f"collection Source link missing for {record.track_id}")
            if not set(record.negative_source_ids).issubset(source_ids):
                raise ContractError(f"negative Source link missing for {record.track_id}")
            if not set(record.event_ids).issubset(events):
                raise ContractError(f"collection Event link missing for {record.track_id}")
            if any(events[event_id].event.track_id != record.track_id for event_id in record.event_ids):
                raise ContractError(f"cross-Track Event link in {record.track_id}")

    def status_counts(self) -> dict[str, int]:
        return dict(sorted(Counter(record.collection_status for record in self.records).items()))

    def to_dict(self) -> dict[str, Any]:
        self.validate_shape()
        data = asdict(self)
        data["records"] = sorted(data["records"], key=lambda item: item["track_id"])
        return data


@dataclass(frozen=True)
class CorpusDataset:
    corpus_version: str
    contract_version: str
    registry_content_hash: str
    registry_freeze_content_hash: str
    pilot_source_registry_content_hash: str
    pilot_dataset_content_hash: str
    source_registry_content_hash: str
    collection_status_content_hash: str
    track_ids: list[str]
    created_at: str
    records: list[PilotEventRecord]
    content_hash: str

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "CorpusDataset":
        payload = dict(data)
        try:
            payload["records"] = [PilotEventRecord.from_dict(item) for item in payload["records"]]
            dataset = cls(**payload)
        except (KeyError, TypeError) as exc:
            raise ContractError(f"invalid H1 corpus dataset fields: {exc}") from exc
        dataset.validate_shape()
        return dataset

    def hash_basis(self) -> dict[str, Any]:
        data = asdict(self)
        data.pop("content_hash")
        data["records"] = sorted(data["records"], key=lambda item: item["event"]["event_id"])
        return data

    def validate_shape(self) -> None:
        require_text(self.corpus_version, "corpus.corpus_version")
        require_text(self.contract_version, "corpus.contract_version")
        parse_aware_datetime(self.created_at, "corpus.created_at")
        if self.track_ids != sorted(self.track_ids) or len(self.track_ids) != 24:
            raise ContractError("full corpus must retain the 24 sorted frozen Track IDs")
        event_ids = [record.event.event_id for record in self.records]
        if len(event_ids) != len(set(event_ids)):
            raise ContractError("full-corpus event_id must be unique")
        if set(record.event.track_id for record in self.records) - set(self.track_ids):
            raise ContractError("full corpus contains an Event outside the frozen population")
        _require_no_empirical_results(self.hash_basis())
        expected = content_digest(self.hash_basis())
        if self.content_hash != expected:
            raise ContractError(
                f"corpus dataset hash mismatch: expected {expected}, got {self.content_hash}"
            )

    def validate(
        self,
        registry: CandidateTrackRegistry,
        freeze: RegistryFreezeManifest,
        source_registry: PilotSourceRegistry,
        collection: CollectionStatusManifest,
    ) -> list[dict[str, str]]:
        self.validate_shape()
        registry.validate()
        freeze.validate()
        source_registry.validate()
        collection.validate_shape()
        if self.registry_content_hash != registry.content_hash:
            raise ContractError("corpus registry hash does not match the frozen registry")
        if self.registry_freeze_content_hash != freeze.content_hash:
            raise ContractError("corpus registry-freeze hash mismatch")
        if self.source_registry_content_hash != source_registry.content_hash:
            raise ContractError("corpus Source-registry hash mismatch")
        if self.collection_status_content_hash != collection.content_hash:
            raise ContractError("corpus collection-status hash mismatch")
        if self.track_ids != sorted(registry.as_map()):
            raise ContractError("corpus Track population differs from the frozen registry")
        sources = source_registry.as_map()
        tracks = registry.as_map()
        results: list[dict[str, str]] = []
        for record in self.records:
            source = sources.get(record.event.source_id)
            if source is None:
                raise ContractError(f"corpus Source not found: {record.event.source_id}")
            if (
                record.event.origin_group != source.origin_group
                or record.event.excerpt != source.excerpt
                or record.event.locator != source.locator
                or record.event.published_at != source.published_at
                or record.event.available_at != source.available_at
                or record.event.accessed_at != source.accessed_at
            ):
                raise ContractError(f"corpus Event provenance mismatch: {record.event.event_id}")
            track = tracks[record.event.track_id]
            result = "PASS"
            reason = "Frozen semantic contract accepted the candidate classification."
            try:
                validate_event_for_track(record.event, track.to_measurement_track())
            except SemanticContractError as exc:
                result = "REJECTED"
                reason = str(exc)
            if record.ingestion_status == "ACCEPTED" and result != "PASS":
                raise ContractError(
                    f"accepted corpus Event fails deterministic validation: {record.event.event_id}"
                )
            results.append(
                {
                    "event_id": record.event.event_id,
                    "ingestion_status": record.ingestion_status,
                    "deterministic_result": result,
                    "deterministic_reason": reason,
                }
            )
        collection.validate_links(registry, source_registry, self)
        return sorted(results, key=lambda item: item["event_id"])

    def status_counts(self) -> dict[str, int]:
        return dict(sorted(Counter(record.ingestion_status for record in self.records).items()))

    def to_dict(self) -> dict[str, Any]:
        self.validate_shape()
        data = asdict(self)
        data["records"] = sorted(data["records"], key=lambda item: item["event"]["event_id"])
        return data


def _hydrate_event(candidate: dict[str, Any], source: PilotSourceRecord) -> PilotEventRecord:
    event = dict(candidate["event"])
    event.update(
        {
            "published_at": source.published_at,
            "available_at": source.available_at,
            "accessed_at": source.accessed_at,
            "availability_basis": source.availability_basis,
            "publisher_timezone": source.publisher_timezone,
            "date_precision": "TIMESTAMP"
            if source.availability_basis == "EXACT_TIMESTAMP"
            else "DAY",
            "source_id": source.source_id,
            "origin_group": source.origin_group,
            "excerpt": source.excerpt,
            "locator": source.locator,
        }
    )
    return PilotEventRecord.from_dict(
        {
            "event": event,
            "ingestion_status": candidate["ingestion_status"],
            "candidate_classification_reason": candidate["candidate_classification_reason"],
            "ambiguity": candidate.get("ambiguity"),
            "human_judgment_required": candidate.get("human_judgment_required"),
        }
    )


def _coverage_rows(
    registry: CandidateTrackRegistry,
    dataset: CorpusDataset,
    collection: CollectionStatusManifest,
    source_registry: PilotSourceRegistry,
) -> list[dict[str, Any]]:
    events_by_track: dict[str, list[PilotEventRecord]] = defaultdict(list)
    for record in dataset.records:
        events_by_track[record.event.track_id].append(record)
    collection_map = {record.track_id: record for record in collection.records}
    source_map = source_registry.as_map()
    rows: list[dict[str, Any]] = []
    for track in registry.tracks:
        records = events_by_track[track.track_id]
        events = [
            record.event for record in records if record.ingestion_status == "ACCEPTED"
        ]
        hold_classes = sorted(
            {
                record.event.signal_class
                for record in records
                if record.ingestion_status == "HOLD"
            }
        )
        status = collection_map[track.track_id]
        source_families = sorted(
            {source_map[source_id].source_type for source_id in status.source_ids}
        )
        if track.track_type == "PRODUCT_COMMERCIALIZATION_TRACK":
            coverage = {
                "sample": any(event.signal_class == "HBM_SAMPLE" for event in events),
                "qualification": any(event.signal_class == "QUALIFICATION_STAGE" for event in events),
                "design_in": any(event.signal_class == "DESIGN_IN" for event in events),
                "commitment": any(
                    event.signal_class == "ORDER_ADJACENT_SUPPLY_COMMITMENT" for event in events
                ),
                "production_stage_context": any(
                    event.signal_class == "PRODUCTION_STAGE_CONTEXT" for event in events
                ),
                "o1_candidate": any(
                    event.signal_class == "O1_COMMERCIAL_REALIZATION" for event in events
                ),
                "corroboration": any(
                    event.signal_class in {"O2_OPERATIONAL_CORROBORATION", "O3_FINANCIAL_CORROBORATION"}
                    for event in events
                ),
                "negative_delay_evidence": status.negative_search_result
                == "EXPLICIT_NEGATIVE_OR_DELAY",
                "censoring": track.right_censoring_risk
                or any(event.right_censored is True for event in events),
                "hold": any(record.ingestion_status == "HOLD" for record in records),
            }
        else:
            coverage = {
                "capex": any(event.signal_class == "CSP_CAPEX" for event in events),
                "infrastructure_commitment": any(
                    event.signal_class == "AI_INFRA_COMMITMENT" for event in events
                ),
                "announcement": any(event.signal_class == "PLATFORM_LAUNCH" for event in events),
                "preview": any(
                    event.signal_class == "PLATFORM_DEPLOYMENT_STAGE"
                    and event.signal_subtype == "PREVIEW"
                    for event in events
                ),
                "limited_availability": any(
                    event.signal_subtype == "LIMITED_AVAILABILITY" for event in events
                ),
                "ga": any(event.signal_subtype == "GENERAL_AVAILABILITY" for event in events),
                "operational_evidence": any(
                    event.signal_class == "P1_PLATFORM_OPERATIONAL_REALIZATION"
                    for event in events
                ),
                "delay_constraint": status.negative_search_result
                == "EXPLICIT_NEGATIVE_OR_DELAY",
                "censoring": track.right_censoring_risk
                or any(event.right_censored is True for event in events),
                "hold": any(record.ingestion_status == "HOLD" for record in records),
            }
        rows.append(
            {
                "track_id": track.track_id,
                "track_type": track.track_type,
                "coverage": coverage,
                "coverage_basis": "ACCEPTED_UNREVIEWED_CANDIDATES_ONLY",
                "hold_classes": hold_classes,
                "source_families": source_families,
                "source_family_count": len(source_families),
                "missingness": status.missingness,
                "gate6_readiness": status.gate6_readiness,
            }
        )
    return rows


class CorpusBuilder:
    def __init__(self, workspace: Path):
        self.workspace = workspace.resolve()

    def build(self, input_path: Path) -> dict[str, Any]:
        raw = load_json(input_path, None)
        if not isinstance(raw, dict):
            raise ContractError("corpus collection input must be a JSON object")
        _require_no_empirical_results(raw)

        registry = CandidateTrackRegistry.from_dict(
            load_json(self.workspace / "data/h1/registry/candidate_tracks.json", {})
        )
        freeze = RegistryFreezeManifest(
            **load_json(self.workspace / "data/h1/registry/registry_freeze.json", {})
        )
        pilot_sources = PilotSourceRegistry.from_dict(
            load_json(self.workspace / "data/h1/pilot/source_registry.json", {})
        )
        pilot_dataset = PilotDataset.from_dict(
            load_json(self.workspace / "data/h1/pilot/pilot_events.json", {})
        )
        pilot_sources.verify_archives(self.workspace)
        pilot_dataset.validate(registry, freeze, pilot_sources)

        immutable = raw["immutable_pilot"]
        if immutable["source_registry_content_hash"] != pilot_sources.content_hash:
            raise ContractError("pilot Source registry changed after corpus preregistration")
        if immutable["dataset_content_hash"] != pilot_dataset.content_hash:
            raise ContractError("pilot dataset changed after corpus preregistration")

        corpus_dir = self.workspace / "data/h1/corpus"
        archive_dir = corpus_dir / "archive"
        archive_dir.mkdir(parents=True, exist_ok=True)

        sources = list(pilot_sources.sources)
        source_ids = {source.source_id for source in sources}
        for candidate in raw["new_sources"]:
            source_data = dict(candidate)
            source_id = source_data["source_id"]
            if source_id in source_ids:
                raise ContractError(f"new Source duplicates immutable pilot ID: {source_id}")
            reused_path = source_data.pop("reuse_local_archive_path", None)
            reused_hash = source_data.pop("reuse_content_hash", None)
            if reused_path is not None or reused_hash is not None:
                require_text(reused_path, "new_source.reuse_local_archive_path")
                require_text(reused_hash, "new_source.reuse_content_hash")
                local_archive_path = reused_path
                archive_path = (self.workspace / local_archive_path).resolve()
                if not archive_path.is_relative_to(self.workspace) or not archive_path.is_file():
                    raise ContractError(f"reused Source archive is missing: {source_id}")
                content_hash = hashlib.sha256(archive_path.read_bytes()).hexdigest().upper()
                if content_hash != reused_hash.upper():
                    raise ContractError(f"reused Source archive hash changed: {source_id}")
            else:
                local_archive_path = f"data/h1/corpus/archive/{source_id}.md"
                rendered = _archive_text(source_data)
                archive_path = self.workspace / local_archive_path
                archive_path.write_text(rendered, encoding="utf-8")
                content_hash = hashlib.sha256(archive_path.read_bytes()).hexdigest().upper()
            source = PilotSourceRecord.from_dict(
                {
                    **source_data,
                    "local_archive_path": local_archive_path,
                    "content_hash": content_hash,
                }
            )
            sources.append(source)
            source_ids.add(source_id)

        source_basis = {
            "registry_version": raw["source_registry_version"],
            "created_at": raw["created_at"],
            "sources": [source.to_dict() for source in sorted(sources, key=lambda item: item.source_id)],
        }
        source_registry = PilotSourceRegistry.from_dict(
            {**source_basis, "content_hash": content_digest(source_basis)}
        )
        source_registry.verify_archives(self.workspace)
        source_map = source_registry.as_map()

        records = list(pilot_dataset.records)
        event_ids = {record.event.event_id for record in records}
        for candidate in raw["new_events"]:
            source_id = candidate["event"]["source_id"]
            if source_id not in source_map:
                raise ContractError(f"new Event Source missing: {source_id}")
            record = _hydrate_event(candidate, source_map[source_id])
            if record.event.event_id in event_ids:
                raise ContractError(f"new Event duplicates immutable pilot ID: {record.event.event_id}")
            records.append(record)
            event_ids.add(record.event.event_id)

        collection_records = [
            TrackCollectionRecord.from_dict(item) for item in raw["track_collection_status"]
        ]
        collection_basis = {
            "manifest_version": raw["collection_manifest_version"],
            "created_at": raw["created_at"],
            "registry_content_hash": registry.content_hash,
            "records": [
                record.to_dict() for record in sorted(collection_records, key=lambda item: item.track_id)
            ],
        }
        collection = CollectionStatusManifest.from_dict(
            {**collection_basis, "content_hash": content_digest(collection_basis)}
        )

        dataset_basis = {
            "corpus_version": raw["corpus_version"],
            "contract_version": registry.contract_version,
            "registry_content_hash": registry.content_hash,
            "registry_freeze_content_hash": freeze.content_hash,
            "pilot_source_registry_content_hash": pilot_sources.content_hash,
            "pilot_dataset_content_hash": pilot_dataset.content_hash,
            "source_registry_content_hash": source_registry.content_hash,
            "collection_status_content_hash": collection.content_hash,
            "track_ids": sorted(registry.as_map()),
            "created_at": raw["created_at"],
            "records": [record.to_dict() for record in sorted(records, key=lambda item: item.event.event_id)],
        }
        dataset = CorpusDataset.from_dict(
            {**dataset_basis, "content_hash": content_digest(dataset_basis)}
        )
        validation_results = dataset.validate(registry, freeze, source_registry, collection)

        future_queue = raw["future_module_queue"]
        adversarial_verification = raw["adversarial_verification"]
        capability_ledger = raw["capability_evidence_ledger"]
        self._validate_future_queue(future_queue, source_map)
        self._validate_adversarial_verification(
            adversarial_verification, registry, dataset
        )
        self._validate_capability_ledger(capability_ledger)
        _require_no_empirical_results(future_queue)
        _require_no_empirical_results(adversarial_verification)
        _require_no_empirical_results(capability_ledger)

        coverage_rows = _coverage_rows(registry, dataset, collection, source_registry)
        coverage_basis = {
            "coverage_version": "H1-CORPUS-COVERAGE-1.0.0",
            "created_at": raw["created_at"],
            "interpretation_boundary": (
                "Coverage and missingness describe corpus readiness only; they are not H1 results."
            ),
            "tracks": coverage_rows,
        }
        coverage = {**coverage_basis, "content_hash": content_digest(coverage_basis)}

        write_json(corpus_dir / "source_registry.json", source_registry.to_dict())
        write_json(corpus_dir / "events.json", dataset.to_dict())
        write_json(corpus_dir / "track_collection_status.json", collection.to_dict())
        write_json(corpus_dir / "validation_results.json", {"results": validation_results})
        write_json(corpus_dir / "coverage_report.json", coverage)
        write_json(corpus_dir / "future_module_queue.json", future_queue)
        write_json(
            corpus_dir / "adversarial_verification.json",
            adversarial_verification,
        )
        write_json(
            self.workspace / "application_evidence/capability_evidence_ledger.json",
            capability_ledger,
        )

        artifact_paths = [
            "data/h1/corpus/source_registry.json",
            "data/h1/corpus/events.json",
            "data/h1/corpus/track_collection_status.json",
            "data/h1/corpus/validation_results.json",
            "data/h1/corpus/coverage_report.json",
            "data/h1/corpus/future_module_queue.json",
            "data/h1/corpus/adversarial_verification.json",
            "application_evidence/capability_evidence_ledger.json",
        ]
        file_hashes = {
            path: hashlib.sha256((self.workspace / path).read_bytes()).hexdigest().upper()
            for path in artifact_paths
        }
        manifest_basis = {
            "manifest_version": "H1-CORPUS-BUILD-1.0.0",
            "created_at": raw["created_at"],
            "input_path": str(input_path.resolve().relative_to(self.workspace)).replace("\\", "/"),
            "registry_content_hash": registry.content_hash,
            "registry_freeze_content_hash": freeze.content_hash,
            "immutable_pilot": immutable,
            "source_registry_content_hash": source_registry.content_hash,
            "dataset_content_hash": dataset.content_hash,
            "collection_status_content_hash": collection.content_hash,
            "coverage_content_hash": coverage["content_hash"],
            "file_hashes": file_hashes,
            "counts": {
                "tracks": len(collection.records),
                "sources": len(source_registry.sources),
                "events": len(dataset.records),
                "event_statuses": dataset.status_counts(),
                "collection_statuses": collection.status_counts(),
                "future_module_candidates": len(future_queue["records"]),
                "adversarially_verified_tracks": len(
                    adversarial_verification["records"]
                ),
                "capability_evidence_records": len(capability_ledger["records"]),
            },
            "gate6_frozen": False,
            "empirical_h1_calculated": False,
        }
        manifest = {**manifest_basis, "content_hash": content_digest(manifest_basis)}
        write_json(corpus_dir / "build_manifest.json", manifest)
        return manifest

    @staticmethod
    def _validate_future_queue(data: dict[str, Any], source_map: dict[str, PilotSourceRecord]) -> None:
        records = data.get("records")
        if not isinstance(records, list):
            raise ContractError("future-module queue records must be a list")
        ids: set[str] = set()
        for record in records:
            required = {
                "candidate_id",
                "source_ids",
                "observed_fact",
                "domain",
                "possible_transmission_path",
                "possible_decision_relevance",
                "why_outside_h1",
                "activation_condition",
                "status",
            }
            if set(record) != required:
                raise ContractError("future-module queue record fields differ from contract")
            candidate_id = require_text(record["candidate_id"], "future_candidate.candidate_id")
            if candidate_id in ids:
                raise ContractError(f"duplicate future candidate: {candidate_id}")
            ids.add(candidate_id)
            if record["domain"] not in FUTURE_DOMAINS:
                raise ContractError(f"invalid future-module domain: {record['domain']}")
            if not set(record["source_ids"]).issubset(source_map):
                raise ContractError(f"future candidate Source missing: {candidate_id}")
            for field in required - {"candidate_id", "source_ids", "domain"}:
                require_text(record[field], f"future_candidate.{field}")

    @staticmethod
    def _validate_capability_ledger(data: dict[str, Any]) -> None:
        records = data.get("records")
        if not isinstance(records, list) or not 5 <= len(records) <= 15:
            raise ContractError("capability ledger must contain 5-15 material records")
        required = {
            "fact_id",
            "date",
            "capability_tags",
            "initial_problem_or_assumption",
            "action_performed",
            "evidence_or_failure_encountered",
            "judgment_or_change",
            "why_it_mattered",
            "artifact_references",
            "claim_status",
            "overclaim_boundary",
            "potential_role_relevance",
        }
        ids: set[str] = set()
        for record in records:
            if set(record) != required:
                raise ContractError("capability ledger record fields differ from contract")
            fact_id = require_text(record["fact_id"], "capability.fact_id")
            if fact_id in ids:
                raise ContractError(f"duplicate capability fact: {fact_id}")
            ids.add(fact_id)
            if record["claim_status"] not in CAPABILITY_CLAIM_STATUSES:
                raise ContractError(f"invalid capability claim_status: {record['claim_status']}")
            if not record["capability_tags"] or not record["artifact_references"]:
                raise ContractError("capability record requires tags and artifact references")
            for field in required - {
                "capability_tags",
                "artifact_references",
                "potential_role_relevance",
            }:
                require_text(record[field], f"capability.{field}")

    @staticmethod
    def _validate_adversarial_verification(
        data: dict[str, Any],
        registry: CandidateTrackRegistry,
        dataset: CorpusDataset,
    ) -> None:
        require_text(data.get("manifest_version"), "verification.manifest_version")
        parse_aware_datetime(data.get("created_at"), "verification.created_at")
        collector = require_text(data.get("collector_actor"), "verification.collector_actor")
        verifier = require_text(data.get("verifier_actor"), "verification.verifier_actor")
        if collector == verifier:
            raise ContractError("collector and adversarial verifier must be distinct actors")
        records = data.get("records")
        if not isinstance(records, list):
            raise ContractError("adversarial verification records must be a list")
        expected_ids = sorted(registry.as_map())
        actual_ids = [record.get("track_id") for record in records]
        if actual_ids != expected_ids:
            raise ContractError("adversarial verification must cover the 24 sorted Tracks")
        required = {
            "track_id",
            "source_primacy",
            "timestamp",
            "scope",
            "forward_looking",
            "stage_inflation",
            "same_origin",
            "outcome_interpretation",
            "verdict",
            "hold_event_ids",
            "verifier_note",
        }
        event_map = {record.event.event_id: record for record in dataset.records}
        for record in records:
            if set(record) != required:
                raise ContractError("adversarial verification fields differ from contract")
            if record["verdict"] not in {"PASS", "PASS_WITH_HOLD"}:
                raise ContractError("invalid adversarial verification verdict")
            for field in {
                "source_primacy",
                "timestamp",
                "scope",
                "forward_looking",
                "stage_inflation",
                "same_origin",
                "outcome_interpretation",
            }:
                if record[field] not in {"PASS", "PASS_WITH_HOLD"}:
                    raise ContractError(f"invalid verifier checklist status: {field}")
            require_text(record["verifier_note"], "verification.verifier_note")
            for event_id in record["hold_event_ids"]:
                candidate = event_map.get(event_id)
                if candidate is None or candidate.event.track_id != record["track_id"]:
                    raise ContractError("verification HOLD Event link is missing or cross-Track")
                if candidate.ingestion_status != "HOLD":
                    raise ContractError("verification HOLD link must reference a HOLD candidate")
            if record["verdict"] == "PASS_WITH_HOLD" and not record["hold_event_ids"]:
                raise ContractError("PASS_WITH_HOLD requires at least one linked HOLD Event")


def main() -> None:
    parser = argparse.ArgumentParser(description="Build and validate the frozen 24-Track H1 corpus")
    parser.add_argument("--workspace", default=".")
    parser.add_argument("--input", default="data/h1/corpus/collection_input.json")
    args = parser.parse_args()
    workspace = Path(args.workspace).resolve()
    input_path = (workspace / args.input).resolve()
    manifest = CorpusBuilder(workspace).build(input_path)
    print(json.dumps(manifest["counts"], ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
