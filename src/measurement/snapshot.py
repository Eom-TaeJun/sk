from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Iterable

from src.core.models import ContractError
from src.core.storage import DuplicateConflict, canonical_json, content_digest, load_json, write_json

from .models import (
    EventRecord,
    ReviewStatus,
    TrackRecord,
    TrackStatus,
    parse_aware_datetime,
    parse_date,
)
from .validation import (
    HistoricalLeakageError,
    ObservationAssessment,
    assess_observation,
    validate_event_for_track,
    validate_revision_chain,
)


APPROVED_WINDOWS = {6, 12, 18}


@dataclass(frozen=True)
class ManifestDecision:
    record_id: str
    record_type: str
    decision: str
    reason: str

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ManifestDecision":
        try:
            item = cls(**data)
        except TypeError as exc:
            raise ContractError(f"invalid manifest decision fields: {exc}") from exc
        if item.decision not in {"EXCLUDE", "HOLD"}:
            raise ContractError("manifest decision must be EXCLUDE or HOLD")
        if item.record_type not in {"TRACK", "EVENT"}:
            raise ContractError("manifest decision record_type must be TRACK or EVENT")
        for name in ("record_id", "record_type", "reason"):
            if not isinstance(getattr(item, name), str) or not getattr(item, name).strip():
                raise ContractError(f"manifest decision {name} is required")
        return item


@dataclass(frozen=True)
class DatasetSnapshotManifest:
    snapshot_id: str
    contract_version: str
    included_track_ids: list[str]
    included_event_ids: list[str]
    source_ids: list[str]
    cutoff_at: str
    dataset_freeze_at: str
    observation_window_months: int
    exclusions_and_holds: list[dict[str, Any]]
    observation_assessments: list[dict[str, Any]]
    created_at: str
    content_hash: str

    def hash_basis(self) -> dict[str, Any]:
        data = asdict(self)
        data.pop("content_hash")
        return data

    def validate_hash(self) -> None:
        expected = content_digest(self.hash_basis())
        if self.content_hash != expected:
            raise ContractError(
                f"snapshot hash mismatch: expected {expected}, got {self.content_hash}"
            )

    def to_dict(self) -> dict[str, Any]:
        self.validate_hash()
        return asdict(self)


class SnapshotBuilder:
    def build(
        self,
        *,
        snapshot_id: str,
        contract_version: str,
        tracks: Iterable[TrackRecord],
        events: Iterable[EventRecord],
        cutoff_at: str,
        dataset_freeze_at: str,
        observation_window_months: int,
        created_at: str,
        requested_track_ids: Iterable[str] | None = None,
        requested_event_ids: Iterable[str] | None = None,
        exclusions_and_holds: Iterable[dict[str, Any]] = (),
    ) -> DatasetSnapshotManifest:
        if observation_window_months not in APPROVED_WINDOWS:
            raise ContractError("observation window must be one of 6, 12, or 18 months")
        cutoff = parse_aware_datetime(cutoff_at, "cutoff_at")
        freeze = parse_aware_datetime(dataset_freeze_at, "dataset_freeze_at")
        parse_aware_datetime(created_at, "created_at")
        if cutoff > freeze:
            raise ContractError("cutoff_at cannot be after dataset_freeze_at")

        track_list = list(tracks)
        event_list = list(events)
        track_map = {track.track_id: track for track in track_list}
        event_map = {event.event_id: event for event in event_list}
        if len(track_map) != len(track_list):
            raise ContractError("track_id must be unique")
        if len(event_map) != len(event_list):
            raise ContractError("event_id must be unique")
        validate_revision_chain(event_list)

        requested_tracks = (
            set(requested_track_ids) if requested_track_ids is not None else set(track_map)
        )
        explicit_event_request = requested_event_ids is not None
        requested_events = (
            set(requested_event_ids) if requested_event_ids is not None else set(event_map)
        )
        missing_tracks = requested_tracks - set(track_map)
        missing_events = requested_events - set(event_map)
        if missing_tracks:
            raise ContractError(f"requested tracks not found: {sorted(missing_tracks)}")
        if missing_events:
            raise ContractError(f"requested events not found: {sorted(missing_events)}")

        decisions = [ManifestDecision.from_dict(item) for item in exclusions_and_holds]
        decision_map: dict[tuple[str, str], ManifestDecision] = {}
        for item in decisions:
            key = (item.record_type, item.record_id)
            if key in decision_map:
                raise ContractError(f"duplicate manifest decision: {key}")
            if item.record_type == "TRACK" and item.record_id not in track_map:
                raise ContractError(f"manifest decision Track not found: {item.record_id}")
            if item.record_type == "EVENT" and item.record_id not in event_map:
                raise ContractError(f"manifest decision Event not found: {item.record_id}")
            decision_map[key] = item

        eligible_tracks: set[str] = set()
        for track_id in requested_tracks:
            track = track_map[track_id]
            decision = decision_map.get(("TRACK", track_id))
            if decision is not None:
                continue
            if track.track_status != TrackStatus.ACTIVE.value:
                raise ContractError(
                    f"non-ACTIVE track {track_id} requires an EXCLUDE/HOLD reason"
                )
            eligible_tracks.add(track_id)

        active_events: dict[str, EventRecord] = {}
        for event_id in sorted(requested_events):
            event = event_map[event_id]
            track = track_map.get(event.track_id)
            if track is None or event.track_id not in requested_tracks:
                raise ContractError(f"event {event_id} is outside requested tracks")
            if event.track_id not in eligible_tracks:
                continue
            if ("EVENT", event_id) in decision_map:
                continue
            if event.review_status != ReviewStatus.APPROVED.value:
                raise ContractError(
                    f"non-approved event {event_id} requires an EXCLUDE/HOLD reason"
                )
            validate_event_for_track(event, track)
            available = parse_aware_datetime(event.available_at, "event.available_at")
            if available > cutoff:
                if explicit_event_request:
                    raise HistoricalLeakageError(
                        f"{event.event_id} was unavailable at cutoff {cutoff_at}"
                    )
                continue
            if available.date() < parse_date(track.start_boundary, "track.start_boundary"):
                if explicit_event_request:
                    raise ContractError(
                        f"{event.event_id} is before the approved historical boundary"
                    )
                continue
            active_events[event.event_id] = event

        # Keep the immutable source/event registry outside the snapshot, but select only
        # the latest revision that was historically available at this cutoff.
        superseded_ids = {
            event.supersedes_event_id
            for event in active_events.values()
            if event.supersedes_event_id in active_events
        }
        for event_id in superseded_ids:
            if event_id is not None:
                active_events.pop(event_id, None)

        assessments: list[ObservationAssessment] = []
        for event in active_events.values():
            if event.data_role != "SIGNAL":
                continue
            assessments.append(
                assess_observation(
                    event,
                    track_map[event.track_id],
                    dataset_freeze_at,
                    observation_window_months,
                )
            )

        basis = {
            "snapshot_id": snapshot_id,
            "contract_version": contract_version,
            "included_track_ids": sorted(eligible_tracks),
            "included_event_ids": sorted(active_events),
            "source_ids": sorted({event.source_id for event in active_events.values()}),
            "cutoff_at": cutoff.isoformat(),
            "dataset_freeze_at": freeze.isoformat(),
            "observation_window_months": observation_window_months,
            "exclusions_and_holds": sorted(
                (asdict(item) for item in decisions),
                key=lambda item: (item["decision"], item["record_type"], item["record_id"]),
            ),
            "observation_assessments": sorted(
                (item.to_dict() for item in assessments), key=lambda item: item["event_id"]
            ),
            "created_at": parse_aware_datetime(created_at, "created_at").isoformat(),
        }
        manifest = DatasetSnapshotManifest(
            **basis,
            content_hash=content_digest(basis),
        )
        manifest.validate_hash()
        return manifest


class SnapshotStore:
    """File-backed immutable manifest store; identical replay is idempotent."""

    def __init__(self, path: Path):
        self.path = path

    def put(self, manifest: DatasetSnapshotManifest) -> bool:
        payload = manifest.to_dict()
        existing = load_json(self.path, None)
        if existing is not None:
            if canonical_json(existing) != canonical_json(payload):
                raise DuplicateConflict(
                    f"snapshot {manifest.snapshot_id} already exists with different content"
                )
            return False
        write_json(self.path, payload)
        return True

    def load(self) -> DatasetSnapshotManifest:
        payload = load_json(self.path, None)
        if payload is None:
            raise FileNotFoundError(self.path)
        try:
            manifest = DatasetSnapshotManifest(**payload)
        except TypeError as exc:
            raise ContractError(f"invalid snapshot manifest: {exc}") from exc
        manifest.validate_hash()
        return manifest
