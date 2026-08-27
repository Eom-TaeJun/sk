from __future__ import annotations

from collections import Counter
from dataclasses import asdict, dataclass
from enum import Enum
from pathlib import Path
from typing import Any

from src.core.models import ContractError
from src.core.storage import DuplicateConflict, canonical_json, content_digest, load_json, write_json

from .models import TrackRecord, TrackType, parse_aware_datetime, parse_date, require_enum, require_text


class RegistryStatus(str, Enum):
    PRE_REGISTERED = "PRE_REGISTERED"
    HOLD = "HOLD"
    EXCLUDED = "EXCLUDED"


@dataclass(frozen=True)
class CandidateTrackRecord:
    track_id: str
    track_type: str
    entity: str
    product: str | None
    platform: str | None
    generation: str
    geography: str | None
    start_boundary: str
    inclusion_reason: str
    first_known_candidate_source_family: str
    left_truncated: bool
    right_censoring_risk: bool
    expected_source_families: list[str]
    known_scope_limitation: str
    registry_status: str
    status_reason: str | None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "CandidateTrackRecord":
        try:
            record = cls(**data)
        except TypeError as exc:
            raise ContractError(f"invalid candidate Track fields: {exc}") from exc
        record.validate()
        return record

    def validate(self) -> None:
        for name in (
            "track_id",
            "entity",
            "generation",
            "inclusion_reason",
            "first_known_candidate_source_family",
            "known_scope_limitation",
        ):
            require_text(getattr(self, name), f"candidate_track.{name}")
        require_enum(TrackType, self.track_type, "candidate_track.track_type")
        require_enum(RegistryStatus, self.registry_status, "candidate_track.registry_status")
        parse_date(self.start_boundary, "candidate_track.start_boundary")
        if not isinstance(self.left_truncated, bool):
            raise ContractError("candidate_track.left_truncated must be boolean")
        if not isinstance(self.right_censoring_risk, bool):
            raise ContractError("candidate_track.right_censoring_risk must be boolean")
        if not isinstance(self.expected_source_families, list) or not self.expected_source_families:
            raise ContractError("candidate_track.expected_source_families must be non-empty")
        for value in self.expected_source_families:
            require_text(value, "candidate_track.expected_source_families[]")
        if self.geography is not None:
            require_text(self.geography, "candidate_track.geography")
        if self.track_type == TrackType.PRODUCT.value:
            require_text(self.product, "candidate_track.product")
        if self.track_type == TrackType.PLATFORM.value:
            require_text(self.platform, "candidate_track.platform")
        if self.registry_status in {RegistryStatus.HOLD.value, RegistryStatus.EXCLUDED.value}:
            require_text(self.status_reason, "candidate_track.status_reason")
        elif self.status_reason is not None:
            require_text(self.status_reason, "candidate_track.status_reason")

    def to_measurement_track(self) -> TrackRecord:
        status = {
            RegistryStatus.PRE_REGISTERED.value: "ACTIVE",
            RegistryStatus.HOLD.value: "HOLD",
            RegistryStatus.EXCLUDED.value: "EXCLUDED",
        }[self.registry_status]
        return TrackRecord.from_dict(
            {
                "track_id": self.track_id,
                "track_type": self.track_type,
                "entity": self.entity,
                "product": self.product,
                "platform": self.platform,
                "generation": self.generation,
                "geography": self.geography,
                "start_boundary": self.start_boundary,
                "left_truncated": self.left_truncated,
                "track_status": status,
            }
        )

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class CandidateTrackRegistry:
    registry_version: str
    contract_version: str
    historical_start: str
    created_at: str
    outcome_neutral: bool
    tracks: list[CandidateTrackRecord]
    content_hash: str

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "CandidateTrackRegistry":
        payload = dict(data)
        try:
            payload["tracks"] = [CandidateTrackRecord.from_dict(item) for item in payload["tracks"]]
            registry = cls(**payload)
        except (KeyError, TypeError) as exc:
            raise ContractError(f"invalid candidate registry fields: {exc}") from exc
        registry.validate()
        return registry

    def hash_basis(self) -> dict[str, Any]:
        data = asdict(self)
        data.pop("content_hash")
        data["tracks"] = sorted(data["tracks"], key=lambda item: item["track_id"])
        return data

    def validate(self) -> None:
        require_text(self.registry_version, "registry.registry_version")
        require_text(self.contract_version, "registry.contract_version")
        historical_start = parse_date(self.historical_start, "registry.historical_start")
        parse_aware_datetime(self.created_at, "registry.created_at")
        if self.outcome_neutral is not True:
            raise ContractError("candidate registry must declare outcome_neutral=true")
        if not self.tracks:
            raise ContractError("candidate registry must contain tracks")
        ids = [track.track_id for track in self.tracks]
        if len(ids) != len(set(ids)):
            raise ContractError("candidate registry track_id must be unique")
        for track in self.tracks:
            track.validate()
            if parse_date(track.start_boundary, "candidate_track.start_boundary") != historical_start:
                raise ContractError("candidate Track boundary must match registry boundary")
        expected = content_digest(self.hash_basis())
        if self.content_hash != expected:
            raise ContractError(
                f"candidate registry hash mismatch: expected {expected}, got {self.content_hash}"
            )

    def to_dict(self) -> dict[str, Any]:
        self.validate()
        data = asdict(self)
        data["tracks"] = sorted(data["tracks"], key=lambda item: item["track_id"])
        return data

    def as_map(self) -> dict[str, CandidateTrackRecord]:
        return {track.track_id: track for track in self.tracks}


@dataclass(frozen=True)
class RegistryFreezeManifest:
    freeze_id: str
    registry_version: str
    contract_version: str
    registry_frozen_at: str
    candidate_track_ids: list[str]
    status_counts: dict[str, int]
    registry_content_hash: str
    content_hash: str

    def hash_basis(self) -> dict[str, Any]:
        data = asdict(self)
        data.pop("content_hash")
        return data

    def validate(self) -> None:
        require_text(self.freeze_id, "registry_freeze.freeze_id")
        parse_aware_datetime(self.registry_frozen_at, "registry_freeze.registry_frozen_at")
        if self.candidate_track_ids != sorted(self.candidate_track_ids):
            raise ContractError("registry freeze track IDs must be sorted")
        if len(self.candidate_track_ids) != len(set(self.candidate_track_ids)):
            raise ContractError("registry freeze track IDs must be unique")
        if sum(self.status_counts.values()) != len(self.candidate_track_ids):
            raise ContractError("registry freeze status counts do not match Track count")
        expected = content_digest(self.hash_basis())
        if self.content_hash != expected:
            raise ContractError(
                f"registry freeze hash mismatch: expected {expected}, got {self.content_hash}"
            )

    def to_dict(self) -> dict[str, Any]:
        self.validate()
        return asdict(self)


class RegistryFreezer:
    def freeze(
        self,
        registry: CandidateTrackRegistry,
        *,
        freeze_id: str,
        registry_frozen_at: str,
    ) -> RegistryFreezeManifest:
        registry.validate()
        frozen_at = parse_aware_datetime(registry_frozen_at, "registry_frozen_at")
        created_at = parse_aware_datetime(registry.created_at, "registry.created_at")
        if frozen_at < created_at:
            raise ContractError("registry freeze cannot precede registry creation")
        basis = {
            "freeze_id": freeze_id,
            "registry_version": registry.registry_version,
            "contract_version": registry.contract_version,
            "registry_frozen_at": frozen_at.isoformat(),
            "candidate_track_ids": sorted(track.track_id for track in registry.tracks),
            "status_counts": dict(
                sorted(Counter(track.registry_status for track in registry.tracks).items())
            ),
            "registry_content_hash": registry.content_hash,
        }
        manifest = RegistryFreezeManifest(**basis, content_hash=content_digest(basis))
        manifest.validate()
        return manifest


class RegistryFreezeStore:
    """Immutable file store; identical registry freezes are idempotent."""

    def __init__(self, path: Path):
        self.path = path

    def put(self, manifest: RegistryFreezeManifest) -> bool:
        payload = manifest.to_dict()
        existing = load_json(self.path, None)
        if existing is not None:
            if canonical_json(existing) != canonical_json(payload):
                raise DuplicateConflict(
                    f"registry freeze {manifest.freeze_id} already exists with different content"
                )
            return False
        write_json(self.path, payload)
        return True

