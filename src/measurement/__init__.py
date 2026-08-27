"""Deterministic measurement contracts for frozen H1-P and H1-C research."""

from .models import EventRecord, TrackRecord
from .pilot import (
    IngestionStatus,
    PilotDataset,
    PilotEventRecord,
    PilotSourceRecord,
    PilotSourceRegistry,
    PilotValidationResult,
)
from .registry import (
    CandidateTrackRecord,
    CandidateTrackRegistry,
    RegistryFreezeManifest,
    RegistryFreezer,
)
from .snapshot import DatasetSnapshotManifest, SnapshotBuilder, SnapshotStore
from .validation import (
    ObservationAssessment,
    assess_observation,
    assess_within_track_scope,
    count_independent_origins,
    validate_event_for_track,
    validate_single_stratum_batch,
)

__all__ = [
    "DatasetSnapshotManifest",
    "CandidateTrackRecord",
    "CandidateTrackRegistry",
    "EventRecord",
    "IngestionStatus",
    "ObservationAssessment",
    "PilotDataset",
    "PilotEventRecord",
    "PilotSourceRecord",
    "PilotSourceRegistry",
    "PilotValidationResult",
    "RegistryFreezeManifest",
    "RegistryFreezer",
    "SnapshotBuilder",
    "SnapshotStore",
    "TrackRecord",
    "assess_observation",
    "assess_within_track_scope",
    "count_independent_origins",
    "validate_event_for_track",
    "validate_single_stratum_batch",
]
