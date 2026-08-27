from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import date, datetime
from enum import Enum
from typing import Any

from src.core.models import ContractError, EvidenceLevel


class TrackType(str, Enum):
    PRODUCT = "PRODUCT_COMMERCIALIZATION_TRACK"
    PLATFORM = "CUSTOMER_PLATFORM_REALIZATION_TRACK"


class TrackStatus(str, Enum):
    ACTIVE = "ACTIVE"
    HOLD = "HOLD"
    EXCLUDED = "EXCLUDED"


class DataRole(str, Enum):
    SIGNAL = "SIGNAL"
    OUTCOME = "OUTCOME"
    CONTEXT = "CONTEXT"


class TransmissionLayer(str, Enum):
    CUSTOMER_ECONOMICS = "CUSTOMER_ECONOMICS"
    AI_INFRASTRUCTURE = "AI_INFRASTRUCTURE"
    PLATFORM = "PLATFORM"
    MEMORY_PRODUCT = "MEMORY_PRODUCT"
    QUALIFICATION_COMMERCIAL = "QUALIFICATION_COMMERCIAL"
    COMMERCIAL_REALIZATION = "COMMERCIAL_REALIZATION"
    MARKET_CONTEXT = "MARKET_CONTEXT"


class DecisionQuestion(str, Enum):
    DEMAND_FORECAST = "DEMAND_FORECAST"
    CUSTOMER_PRIORITY = "CUSTOMER_PRIORITY"
    QUALIFICATION = "QUALIFICATION"
    TTM = "TTM"
    COMMERCIALIZATION_VISIBILITY = "COMMERCIALIZATION_VISIBILITY"
    PLATFORM_DEPLOYMENT_VISIBILITY = "PLATFORM_DEPLOYMENT_VISIBILITY"


class ScopeType(str, Enum):
    COMPANY = "COMPANY"
    PRODUCT_FAMILY = "PRODUCT_FAMILY"
    PRODUCT_GENERATION = "PRODUCT_GENERATION"
    PLATFORM = "PLATFORM"
    CUSTOMER = "CUSTOMER"
    REGION = "REGION"
    SITE = "SITE"
    INDUSTRY = "INDUSTRY"


class AvailabilityBasis(str, Enum):
    EXACT_TIMESTAMP = "EXACT_TIMESTAMP"
    PUBLISHER_DATE_FALLBACK = "PUBLISHER_DATE_FALLBACK"
    OTHER_APPROVED_PROXY = "OTHER_APPROVED_PROXY"


class DatePrecision(str, Enum):
    TIMESTAMP = "TIMESTAMP"
    DAY = "DAY"
    MONTH = "MONTH"


class ReviewStatus(str, Enum):
    UNREVIEWED = "UNREVIEWED"
    APPROVED = "APPROVED"
    HOLD = "HOLD"
    REJECTED = "REJECTED"


def require_text(value: Any, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ContractError(f"{name} is required")
    return value.strip()


def parse_date(value: str, name: str) -> date:
    try:
        return date.fromisoformat(value)
    except (TypeError, ValueError) as exc:
        raise ContractError(f"{name} must be ISO YYYY-MM-DD") from exc


def parse_aware_datetime(value: str, name: str) -> datetime:
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except (AttributeError, TypeError, ValueError) as exc:
        raise ContractError(f"{name} must be an ISO-8601 datetime") from exc
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise ContractError(f"{name} must include a timezone offset")
    return parsed


def require_enum(enum_type: type[Enum], value: str, name: str) -> None:
    try:
        enum_type(value)
    except (TypeError, ValueError) as exc:
        raise ContractError(f"invalid {name}: {value}") from exc


@dataclass(frozen=True)
class TrackRecord:
    track_id: str
    track_type: str
    entity: str
    product: str | None
    platform: str | None
    generation: str
    geography: str | None
    start_boundary: str
    left_truncated: bool
    track_status: str

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "TrackRecord":
        try:
            record = cls(**data)
        except TypeError as exc:
            raise ContractError(f"invalid Track fields: {exc}") from exc
        record.validate()
        return record

    def validate(self) -> None:
        for name in ("track_id", "entity", "generation"):
            require_text(getattr(self, name), f"track.{name}")
        require_enum(TrackType, self.track_type, "track.track_type")
        require_enum(TrackStatus, self.track_status, "track.track_status")
        parse_date(self.start_boundary, "track.start_boundary")
        if not isinstance(self.left_truncated, bool):
            raise ContractError("track.left_truncated must be boolean")
        if self.geography is not None:
            require_text(self.geography, "track.geography")
        if self.track_type == TrackType.PRODUCT.value:
            require_text(self.product, "track.product")
        if self.track_type == TrackType.PLATFORM.value:
            require_text(self.platform, "track.platform")

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class EventRecord:
    event_id: str
    track_id: str
    data_role: str
    signal_class: str
    signal_subtype: str
    transmission_layer: str
    decision_question: str
    event_at: str
    published_at: str
    available_at: str
    accessed_at: str | None
    availability_basis: str
    publisher_timezone: str
    date_precision: str
    scope_type: str
    scope_value: str
    source_id: str
    origin_group: str
    evidence_level: str
    claim: str
    excerpt: str
    locator: str
    revision_id: str
    supersedes_event_id: str | None
    right_censored: bool | None
    left_truncated: bool
    review_status: str
    event_date_precision: str | None = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "EventRecord":
        try:
            record = cls(**data)
        except TypeError as exc:
            raise ContractError(f"invalid Event fields: {exc}") from exc
        record.validate()
        return record

    def validate(self) -> None:
        for name in (
            "event_id",
            "track_id",
            "signal_class",
            "signal_subtype",
            "publisher_timezone",
            "scope_value",
            "source_id",
            "origin_group",
            "claim",
            "excerpt",
            "locator",
            "revision_id",
        ):
            require_text(getattr(self, name), f"event.{name}")
        require_enum(DataRole, self.data_role, "event.data_role")
        require_enum(TransmissionLayer, self.transmission_layer, "event.transmission_layer")
        require_enum(DecisionQuestion, self.decision_question, "event.decision_question")
        require_enum(AvailabilityBasis, self.availability_basis, "event.availability_basis")
        require_enum(DatePrecision, self.date_precision, "event.date_precision")
        if self.event_date_precision is not None:
            require_enum(
                DatePrecision,
                self.event_date_precision,
                "event.event_date_precision",
            )
        require_enum(ScopeType, self.scope_type, "event.scope_type")
        require_enum(EvidenceLevel, self.evidence_level, "event.evidence_level")
        require_enum(ReviewStatus, self.review_status, "event.review_status")
        event_at = parse_aware_datetime(self.event_at, "event.event_at")
        published_at = parse_aware_datetime(self.published_at, "event.published_at")
        available_at = parse_aware_datetime(self.available_at, "event.available_at")
        if event_at > available_at:
            raise ContractError("event.event_at cannot be after event.available_at")
        if published_at > available_at:
            raise ContractError("event.published_at cannot be after event.available_at")
        if self.accessed_at is not None:
            accessed_at = parse_aware_datetime(self.accessed_at, "event.accessed_at")
            if accessed_at < available_at:
                raise ContractError("event.accessed_at cannot be before event.available_at")
        if self.availability_basis == AvailabilityBasis.PUBLISHER_DATE_FALLBACK.value:
            if self.date_precision != DatePrecision.DAY.value:
                raise ContractError("publisher-date fallback requires DAY precision")
            if (available_at.date() - published_at.date()).days != 1:
                raise ContractError(
                    "publisher-date fallback must use the next calendar day"
                )
            if any((available_at.hour, available_at.minute, available_at.second)):
                raise ContractError(
                    "publisher-date fallback must begin at 00:00 publisher local time"
                )
        if self.supersedes_event_id == self.event_id:
            raise ContractError("event cannot supersede itself")
        if self.right_censored is not None and not isinstance(self.right_censored, bool):
            raise ContractError("event.right_censored must be boolean or null")
        if not isinstance(self.left_truncated, bool):
            raise ContractError("event.left_truncated must be boolean")

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
