from __future__ import annotations

import calendar
from dataclasses import asdict, dataclass
from datetime import datetime
from typing import Iterable

from src.core.models import ContractError

from .models import (
    DataRole,
    DecisionQuestion,
    EventRecord,
    ScopeType,
    TrackRecord,
    TrackType,
    TransmissionLayer,
    parse_aware_datetime,
    parse_date,
)


class HistoricalLeakageError(ContractError):
    pass


class SemanticContractError(ContractError):
    pass


class ScopeJoinError(ContractError):
    pass


class StratumPoolingError(ContractError):
    pass


class RevisionContractError(ContractError):
    pass


class CensoringContractError(ContractError):
    pass


PRODUCT_SIGNALS = {
    "HBM_SAMPLE",
    "QUALIFICATION_STAGE",
    "DESIGN_IN",
    "ORDER_ADJACENT_SUPPLY_COMMITMENT",
}
PRODUCT_OUTCOMES = {
    "O1_COMMERCIAL_REALIZATION",
    "O2_OPERATIONAL_CORROBORATION",
    "O3_FINANCIAL_CORROBORATION",
}
PLATFORM_SIGNALS = {
    "CSP_CAPEX",
    "AI_INFRA_COMMITMENT",
    "PLATFORM_LAUNCH",
    "PLATFORM_DEPLOYMENT_STAGE",
}
PLATFORM_OUTCOMES = {"P1_PLATFORM_OPERATIONAL_REALIZATION"}
CONTEXT_CLASSES = {"PRICING_INVENTORY_CONTEXT"}
REMOVED_MINIMUM_CLASSES = {"LTA_COMMERCIAL_COMMITMENT", "POWER_DC_READY"}

PLATFORM_DEPLOYMENT_SUBTYPES = {
    "PLANNED",
    "PREVIEW",
    "LIMITED_AVAILABILITY",
    "GENERAL_AVAILABILITY",
    "INSTALLED_OPERATIONAL",
}
PLATFORM_REALIZATION_SUBTYPES = {
    "LIMITED_AVAILABILITY",
    "GENERAL_AVAILABILITY",
    "INSTALLED_OPERATIONAL",
}
QUALIFICATION_SUBTYPES = {"PLANNED", "UNDERWAY", "FINAL_STAGE", "COMPLETE"}
O1_SUBTYPES = {
    "COMMERCIAL_SHIPMENT_STARTED",
    "CUSTOMER_SUPPLY_STARTED",
    "VOLUME_PRODUCTION_FOR_CURRENT_CUSTOMER_SUPPLY",
}
SUPPLY_COMMITMENT_TERMS = {
    "supply agreement",
    "long-term agreement",
    "long term agreement",
    "committed supply",
    "customer order",
    "allocation agreed",
    "sold out",
}
FUTURE_CUSTOMER_SUPPLY_TERMS = {
    "will begin supply",
    "will begin shipping",
    "will supply",
    "for supply to a customer from",
    "customer supply from a later date",
}

PRODUCT_DECISIONS = {
    DecisionQuestion.DEMAND_FORECAST.value,
    DecisionQuestion.CUSTOMER_PRIORITY.value,
    DecisionQuestion.QUALIFICATION.value,
    DecisionQuestion.TTM.value,
    DecisionQuestion.COMMERCIALIZATION_VISIBILITY.value,
}
PLATFORM_DECISIONS = {
    DecisionQuestion.DEMAND_FORECAST.value,
    DecisionQuestion.CUSTOMER_PRIORITY.value,
    DecisionQuestion.TTM.value,
    DecisionQuestion.PLATFORM_DEPLOYMENT_VISIBILITY.value,
}


def _contains_any(text: str, phrases: set[str]) -> bool:
    lowered = " ".join(text.lower().split())
    return any(phrase in lowered for phrase in phrases)


def validate_event_for_track(event: EventRecord, track: TrackRecord) -> None:
    event.validate()
    track.validate()
    if event.track_id != track.track_id:
        raise SemanticContractError("event.track_id does not match Track")
    if track.track_status != "ACTIVE":
        raise SemanticContractError("only ACTIVE tracks can enter measurement")
    if track.left_truncated and not event.left_truncated:
        raise SemanticContractError(
            "events in a left-truncated track must preserve left_truncated=true"
        )
    if event.signal_class in REMOVED_MINIMUM_CLASSES:
        raise SemanticContractError(
            f"{event.signal_class} is removed from the minimum H1 comparison"
        )

    if event.data_role == DataRole.CONTEXT.value:
        if event.signal_class not in CONTEXT_CLASSES:
            raise SemanticContractError("CONTEXT role requires an approved context class")
        if event.transmission_layer != TransmissionLayer.MARKET_CONTEXT.value:
            raise SemanticContractError("context records must use MARKET_CONTEXT")
        return

    if track.track_type == TrackType.PRODUCT.value:
        allowed = PRODUCT_SIGNALS if event.data_role == DataRole.SIGNAL.value else PRODUCT_OUTCOMES
        if event.signal_class not in allowed:
            raise SemanticContractError(
                f"{event.signal_class} is not valid for H1-P {event.data_role}"
            )
        if event.decision_question not in PRODUCT_DECISIONS:
            raise SemanticContractError("decision_question is incompatible with H1-P")
        if event.signal_class == "HBM_SAMPLE":
            if event.transmission_layer != TransmissionLayer.MEMORY_PRODUCT.value:
                raise SemanticContractError("HBM_SAMPLE must use MEMORY_PRODUCT")
            if "qualification" in event.signal_subtype.lower():
                raise SemanticContractError("sample cannot be qualification completion")
        elif event.signal_class in {
            "QUALIFICATION_STAGE",
            "DESIGN_IN",
            "ORDER_ADJACENT_SUPPLY_COMMITMENT",
        }:
            if event.transmission_layer != TransmissionLayer.QUALIFICATION_COMMERCIAL.value:
                raise SemanticContractError(
                    "product acceptance/commitment signals require QUALIFICATION_COMMERCIAL"
                )
        elif event.transmission_layer != TransmissionLayer.COMMERCIAL_REALIZATION.value:
            raise SemanticContractError("product outcomes require COMMERCIAL_REALIZATION")
    else:
        allowed = PLATFORM_SIGNALS if event.data_role == DataRole.SIGNAL.value else PLATFORM_OUTCOMES
        if event.signal_class not in allowed:
            raise SemanticContractError(
                f"{event.signal_class} is not valid for H1-C {event.data_role}"
            )
        if event.decision_question not in PLATFORM_DECISIONS:
            raise SemanticContractError("decision_question is incompatible with H1-C")
        expected_layer = {
            "CSP_CAPEX": TransmissionLayer.CUSTOMER_ECONOMICS.value,
            "AI_INFRA_COMMITMENT": TransmissionLayer.AI_INFRASTRUCTURE.value,
            "PLATFORM_LAUNCH": TransmissionLayer.PLATFORM.value,
            "PLATFORM_DEPLOYMENT_STAGE": TransmissionLayer.PLATFORM.value,
            "P1_PLATFORM_OPERATIONAL_REALIZATION": TransmissionLayer.PLATFORM.value,
        }[event.signal_class]
        if event.transmission_layer != expected_layer:
            raise SemanticContractError(
                f"{event.signal_class} must use {expected_layer}"
            )

    if event.signal_class == "QUALIFICATION_STAGE":
        if event.signal_subtype not in QUALIFICATION_SUBTYPES:
            raise SemanticContractError("invalid qualification subtype")
        if event.signal_subtype == "COMPLETE":
            text = f"{event.claim} {event.excerpt}"
            if _contains_any(text, {"underway", "planned", "final stage", "to complete"}):
                raise SemanticContractError(
                    "underway/planned/final-stage wording cannot become qualification COMPLETE"
                )
            if not _contains_any(
                text,
                {
                    "qualification complete",
                    "qualification completed",
                    "completed qualification",
                    "certification complete",
                    "certification completed",
                },
            ):
                raise SemanticContractError(
                    "qualification COMPLETE requires explicit completion wording"
                )

    if event.signal_class == "ORDER_ADJACENT_SUPPLY_COMMITMENT":
        text = f"{event.claim} {event.excerpt}"
        if not _contains_any(text, SUPPLY_COMMITMENT_TERMS):
            raise SemanticContractError(
                "production or ramp wording alone cannot become a supply commitment"
            )

    if event.signal_class == "PLATFORM_DEPLOYMENT_STAGE":
        if event.signal_subtype not in PLATFORM_DEPLOYMENT_SUBTYPES:
            raise SemanticContractError("invalid platform deployment subtype")

    if event.signal_class == "P1_PLATFORM_OPERATIONAL_REALIZATION":
        if event.signal_subtype not in PLATFORM_REALIZATION_SUBTYPES:
            raise SemanticContractError(
                "PLANNED or PREVIEW cannot become P1 operational realization"
            )

    if event.signal_class == "O1_COMMERCIAL_REALIZATION":
        if event.signal_subtype not in O1_SUBTYPES:
            raise SemanticContractError("invalid O1 commercialization subtype")
        text = f"{event.claim} {event.excerpt}"
        if _contains_any(text, FUTURE_CUSTOMER_SUPPLY_TERMS):
            raise SemanticContractError(
                "future-dated customer supply cannot become current O1 realization"
            )
        if _contains_any(text, {"planned", "plans to", "target", "ready for"}):
            raise SemanticContractError("plan/readiness wording cannot become O1")
        if not _contains_any(
            text,
            {
                "commercial shipment commenced",
                "commercial shipments commenced",
                "commercial shipment began",
                "commercial shipments began",
                "customer supply commenced",
                "customer supply began",
                "for supply to a customer",
            },
        ):
            raise SemanticContractError(
                "O1 requires explicit current shipment or customer-supply wording"
            )


def validate_revision_chain(events: Iterable[EventRecord]) -> None:
    event_list = list(events)
    event_map = {event.event_id: event for event in event_list}
    if len(event_map) != len(event_list):
        raise RevisionContractError("event_id must be unique")
    for event in event_map.values():
        if not event.supersedes_event_id:
            continue
        prior = event_map.get(event.supersedes_event_id)
        if prior is None:
            raise RevisionContractError(
                f"superseded event not found: {event.supersedes_event_id}"
            )
        if event.track_id != prior.track_id:
            raise RevisionContractError("revision must remain in the same track")
        if event.source_id != prior.source_id or event.origin_group != prior.origin_group:
            raise RevisionContractError(
                "revision must retain source_id and origin_group"
            )
        if event.revision_id == prior.revision_id:
            raise RevisionContractError("revision_id must change")
        if parse_aware_datetime(event.available_at, "event.available_at") <= parse_aware_datetime(
            prior.available_at, "prior.available_at"
        ):
            raise RevisionContractError("revision available_at must be later")


def count_independent_origins(events: Iterable[EventRecord]) -> int:
    return len({event.origin_group for event in events})


def assess_within_track_scope(
    left: EventRecord,
    right: EventRecord,
    track: TrackRecord,
    *,
    allow_partial: bool = False,
) -> str:
    if left.track_id != right.track_id or left.track_id != track.track_id:
        raise ScopeJoinError("events from different tracks cannot be joined")
    validate_event_for_track(left, track)
    validate_event_for_track(right, track)
    if left.scope_type == right.scope_type and left.scope_value == right.scope_value:
        return "EXACT"
    broad = {ScopeType.COMPANY.value, ScopeType.INDUSTRY.value}
    if left.scope_type in broad or right.scope_type in broad:
        if allow_partial:
            return "PARTIAL_BROAD_TO_NARROW"
        raise ScopeJoinError("broad-to-narrow scope join requires explicit partial approval")
    raise ScopeJoinError(
        "narrow scopes are incompatible without an explicit approved link"
    )


def validate_single_stratum_batch(
    events: Iterable[EventRecord], tracks: dict[str, TrackRecord]
) -> str:
    event_list = list(events)
    if not event_list:
        raise StratumPoolingError("analysis batch cannot be empty")
    strata = set()
    for event in event_list:
        track = tracks.get(event.track_id)
        if track is None:
            raise StratumPoolingError(f"track not found: {event.track_id}")
        validate_event_for_track(event, track)
        strata.add(track.track_type)
    if len(strata) != 1:
        raise StratumPoolingError("H1-P and H1-C records cannot be pooled")
    return next(iter(strata))


def _add_months(value: datetime, months: int) -> datetime:
    if months <= 0:
        raise CensoringContractError("observation window must be positive")
    month_index = value.month - 1 + months
    year = value.year + month_index // 12
    month = month_index % 12 + 1
    day = min(value.day, calendar.monthrange(year, month)[1])
    return value.replace(year=year, month=month, day=day)


@dataclass(frozen=True)
class ObservationAssessment:
    event_id: str
    observation_window_months: int
    window_end: str
    fully_observed: bool
    right_censored: bool
    left_truncated: bool
    eligible_for_failure_denominator: bool

    def to_dict(self) -> dict:
        return asdict(self)


def assess_observation(
    event: EventRecord,
    track: TrackRecord,
    dataset_freeze_at: str,
    observation_window_months: int,
) -> ObservationAssessment:
    validate_event_for_track(event, track)
    freeze = parse_aware_datetime(dataset_freeze_at, "dataset_freeze_at")
    available = parse_aware_datetime(event.available_at, "event.available_at")
    if freeze < available:
        raise HistoricalLeakageError("dataset freeze precedes event availability")
    window_end = _add_months(available, observation_window_months)
    right_censored = freeze < window_end
    if event.right_censored is not None and event.right_censored != right_censored:
        raise CensoringContractError(
            "declared right_censored conflicts with the selected window/freeze"
        )
    historical_start = parse_date(track.start_boundary, "track.start_boundary")
    event_at = parse_aware_datetime(event.event_at, "event.event_at")
    left_truncated = track.left_truncated or event.left_truncated or event_at.date() < historical_start
    return ObservationAssessment(
        event_id=event.event_id,
        observation_window_months=observation_window_months,
        window_end=window_end.isoformat(),
        fully_observed=not right_censored,
        right_censored=right_censored,
        left_truncated=left_truncated,
        eligible_for_failure_denominator=not right_censored,
    )
