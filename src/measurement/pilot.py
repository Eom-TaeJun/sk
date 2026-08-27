from __future__ import annotations

import hashlib
from collections import Counter
from dataclasses import asdict, dataclass
from enum import Enum
from pathlib import Path
from typing import Any

from src.core.models import ContractError
from src.core.storage import content_digest

from .models import EventRecord, ReviewStatus, parse_aware_datetime, parse_date, require_text
from .registry import CandidateTrackRegistry, RegistryFreezeManifest
from .validation import SemanticContractError, validate_event_for_track


class IngestionStatus(str, Enum):
    ACCEPTED = "ACCEPTED"
    HOLD = "HOLD"
    REJECTED = "REJECTED"


@dataclass(frozen=True)
class PilotSourceRecord:
    source_id: str
    source_revision_id: str
    origin_group: str
    title: str
    publisher: str
    source_type: str
    source_tier: str
    primary_source: bool
    publication_date: str
    published_at: str
    available_at: str
    availability_basis: str
    publisher_timezone: str
    accessed_at: str
    url: str
    local_archive_path: str
    content_hash: str
    excerpt: str
    locator: str

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "PilotSourceRecord":
        try:
            record = cls(**data)
        except TypeError as exc:
            raise ContractError(f"invalid pilot Source fields: {exc}") from exc
        record.validate()
        return record

    def validate(self) -> None:
        for field in (
            "source_id",
            "source_revision_id",
            "origin_group",
            "title",
            "publisher",
            "source_type",
            "source_tier",
            "publisher_timezone",
            "url",
            "local_archive_path",
            "content_hash",
            "excerpt",
            "locator",
        ):
            require_text(getattr(self, field), f"pilot_source.{field}")
        parse_date(self.publication_date, "pilot_source.publication_date")
        published = parse_aware_datetime(self.published_at, "pilot_source.published_at")
        available = parse_aware_datetime(self.available_at, "pilot_source.available_at")
        accessed = parse_aware_datetime(self.accessed_at, "pilot_source.accessed_at")
        if published > available or available > accessed:
            raise ContractError("pilot Source time order must be published <= available <= accessed")
        if self.primary_source is not True:
            raise ContractError("real-data pilot accepts primary Sources only")
        if len(self.content_hash) != 64:
            raise ContractError("pilot Source content_hash must be SHA-256")

    def verify_archive(self, workspace: Path) -> None:
        archive = (workspace / self.local_archive_path).resolve()
        root = workspace.resolve()
        if not archive.is_relative_to(root) or not archive.is_file():
            raise ContractError(f"pilot Source archive is missing: {self.source_id}")
        actual = hashlib.sha256(archive.read_bytes()).hexdigest().upper()
        if actual != self.content_hash.upper():
            raise ContractError(f"pilot Source archive hash mismatch: {self.source_id}")
        archived_text = archive.read_text(encoding="utf-8")
        if self.excerpt not in archived_text or self.locator not in archived_text:
            raise ContractError(f"pilot Source excerpt/locator is not preserved: {self.source_id}")

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class PilotSourceRegistry:
    registry_version: str
    created_at: str
    sources: list[PilotSourceRecord]
    content_hash: str

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "PilotSourceRegistry":
        payload = dict(data)
        try:
            payload["sources"] = [PilotSourceRecord.from_dict(item) for item in payload["sources"]]
            registry = cls(**payload)
        except (KeyError, TypeError) as exc:
            raise ContractError(f"invalid pilot Source registry fields: {exc}") from exc
        registry.validate()
        return registry

    def hash_basis(self) -> dict[str, Any]:
        data = asdict(self)
        data.pop("content_hash")
        data["sources"] = sorted(data["sources"], key=lambda item: item["source_id"])
        return data

    def validate(self) -> None:
        require_text(self.registry_version, "pilot_source_registry.registry_version")
        parse_aware_datetime(self.created_at, "pilot_source_registry.created_at")
        ids = [source.source_id for source in self.sources]
        if len(ids) != len(set(ids)):
            raise ContractError("pilot Source IDs must be unique")
        expected = content_digest(self.hash_basis())
        if self.content_hash != expected:
            raise ContractError(
                f"pilot Source registry hash mismatch: expected {expected}, got {self.content_hash}"
            )

    def verify_archives(self, workspace: Path) -> None:
        self.validate()
        for source in self.sources:
            source.verify_archive(workspace)

    def as_map(self) -> dict[str, PilotSourceRecord]:
        return {source.source_id: source for source in self.sources}

    def to_dict(self) -> dict[str, Any]:
        self.validate()
        data = asdict(self)
        data["sources"] = sorted(data["sources"], key=lambda item: item["source_id"])
        return data


@dataclass(frozen=True)
class PilotEventRecord:
    event: EventRecord
    ingestion_status: str
    candidate_classification_reason: str
    ambiguity: str | None
    human_judgment_required: str | None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "PilotEventRecord":
        try:
            record = cls(
                event=EventRecord.from_dict(data["event"]),
                ingestion_status=data["ingestion_status"],
                candidate_classification_reason=data["candidate_classification_reason"],
                ambiguity=data.get("ambiguity"),
                human_judgment_required=data.get("human_judgment_required"),
            )
        except (KeyError, TypeError) as exc:
            raise ContractError(f"invalid pilot Event fields: {exc}") from exc
        record.validate_review_boundary()
        return record

    def validate_review_boundary(self) -> None:
        try:
            status = IngestionStatus(self.ingestion_status)
        except ValueError as exc:
            raise ContractError(f"invalid pilot ingestion status: {self.ingestion_status}") from exc
        require_text(self.candidate_classification_reason, "pilot_event.candidate_classification_reason")
        expected_review = {
            IngestionStatus.ACCEPTED: ReviewStatus.UNREVIEWED.value,
            IngestionStatus.HOLD: ReviewStatus.HOLD.value,
            IngestionStatus.REJECTED: ReviewStatus.REJECTED.value,
        }[status]
        if self.event.review_status != expected_review:
            raise ContractError(
                f"{status.value} pilot Event must use review_status={expected_review}"
            )
        if status == IngestionStatus.HOLD:
            require_text(self.ambiguity, "pilot_event.ambiguity")
            require_text(self.human_judgment_required, "pilot_event.human_judgment_required")

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class PilotValidationResult:
    event_id: str
    ingestion_status: str
    deterministic_result: str
    deterministic_reason: str

    def to_dict(self) -> dict[str, str]:
        return asdict(self)


@dataclass(frozen=True)
class PilotDataset:
    pilot_version: str
    contract_version: str
    registry_content_hash: str
    registry_freeze_content_hash: str
    source_registry_content_hash: str
    pilot_track_ids: list[str]
    created_at: str
    records: list[PilotEventRecord]
    content_hash: str

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "PilotDataset":
        payload = dict(data)
        try:
            payload["records"] = [PilotEventRecord.from_dict(item) for item in payload["records"]]
            dataset = cls(**payload)
        except (KeyError, TypeError) as exc:
            raise ContractError(f"invalid pilot dataset fields: {exc}") from exc
        dataset.validate_shape()
        return dataset

    def hash_basis(self) -> dict[str, Any]:
        data = asdict(self)
        data.pop("content_hash")
        data["records"] = sorted(data["records"], key=lambda item: item["event"]["event_id"])
        return data

    def validate_shape(self) -> None:
        require_text(self.pilot_version, "pilot.pilot_version")
        require_text(self.contract_version, "pilot.contract_version")
        parse_aware_datetime(self.created_at, "pilot.created_at")
        if self.pilot_track_ids != sorted(self.pilot_track_ids):
            raise ContractError("pilot Track IDs must be sorted")
        if len(self.pilot_track_ids) != 4 or len(set(self.pilot_track_ids)) != 4:
            raise ContractError("real-data pilot must contain exactly four Tracks")
        event_ids = [record.event.event_id for record in self.records]
        if len(event_ids) != len(set(event_ids)):
            raise ContractError("pilot event_id must be unique")
        if not 12 <= len(self.records) <= 24:
            raise ContractError("real-data pilot must contain 12-24 atomic Events")
        if set(record.event.track_id for record in self.records) != set(self.pilot_track_ids):
            raise ContractError("pilot Event Tracks must exactly match pilot_track_ids")
        expected = content_digest(self.hash_basis())
        if self.content_hash != expected:
            raise ContractError(f"pilot dataset hash mismatch: expected {expected}, got {self.content_hash}")

    def validate(
        self,
        registry: CandidateTrackRegistry,
        freeze: RegistryFreezeManifest,
        source_registry: PilotSourceRegistry,
    ) -> list[PilotValidationResult]:
        self.validate_shape()
        registry.validate()
        freeze.validate()
        if self.registry_content_hash != registry.content_hash:
            raise ContractError("pilot registry hash does not match frozen registry")
        if self.registry_freeze_content_hash != freeze.content_hash:
            raise ContractError("pilot registry-freeze hash mismatch")
        source_registry.validate()
        if self.source_registry_content_hash != source_registry.content_hash:
            raise ContractError("pilot Source-registry hash mismatch")
        sources = source_registry.as_map()
        registry_tracks = registry.as_map()
        results: list[PilotValidationResult] = []
        for record in self.records:
            candidate = registry_tracks.get(record.event.track_id)
            if candidate is None or candidate.registry_status != "PRE_REGISTERED":
                raise ContractError(f"pilot Event uses an unfrozen Track: {record.event.track_id}")
            source = sources.get(record.event.source_id)
            if source is None:
                raise ContractError(f"pilot Source not found: {record.event.source_id}")
            if (
                record.event.origin_group != source.origin_group
                or record.event.excerpt != source.excerpt
                or record.event.locator != source.locator
                or record.event.published_at != source.published_at
                or record.event.available_at != source.available_at
                or record.event.accessed_at != source.accessed_at
            ):
                raise ContractError(f"pilot Event provenance mismatch: {record.event.event_id}")
            deterministic_result = "PASS"
            deterministic_reason = "Current semantic contract accepted the candidate classification."
            try:
                validate_event_for_track(record.event, candidate.to_measurement_track())
            except SemanticContractError as exc:
                deterministic_result = "REJECTED"
                deterministic_reason = str(exc)
            if record.ingestion_status == IngestionStatus.ACCEPTED.value and deterministic_result != "PASS":
                raise ContractError(
                    f"accepted pilot Event fails deterministic validation: {record.event.event_id}"
                )
            results.append(
                PilotValidationResult(
                    event_id=record.event.event_id,
                    ingestion_status=record.ingestion_status,
                    deterministic_result=deterministic_result,
                    deterministic_reason=deterministic_reason,
                )
            )
        return results

    def status_counts(self) -> dict[str, int]:
        return dict(sorted(Counter(record.ingestion_status for record in self.records).items()))

    def to_dict(self) -> dict[str, Any]:
        self.validate_shape()
        data = asdict(self)
        data["records"] = sorted(data["records"], key=lambda item: item["event"]["event_id"])
        return data
