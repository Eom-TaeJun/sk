from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime
import re
from typing import Any


class BacktestContractError(ValueError):
    """Raised when a backtest record violates the deterministic contract."""


class LeakageError(BacktestContractError):
    """Raised when a record uses information before it was available."""


PRIMARY_SOURCE_CLASSES = {"P1_EVENT", "P1_COUNTERPARTY", "P2_OFFICIAL_CONTEXT"}
SOURCE_CLASSES = PRIMARY_SOURCE_CLASSES | {"S1_SECONDARY"}
EVENT_ROLES = {"SIGNAL", "CONTEXT", "COUNTEREVIDENCE", "OUTCOME"}
SIGNAL_TYPES = {
    "CAPEX",
    "SAMPLE",
    "QUALIFICATION",
    "LTA",
    "SUPPLY_COMMITMENT",
    "POWER_READY",
    "SHIPMENT",
    "COMMERCIAL_OUTCOME",
}
DATE_PRECISIONS = {"DAY", "MONTH_END", "QUARTER_END", "YEAR_END"}
SCOPE_MATCH = {"BROAD", "PARTIAL", "EXACT"}


def parse_date(value: str, name: str) -> date:
    try:
        return date.fromisoformat(value)
    except (TypeError, ValueError) as exc:
        raise BacktestContractError(f"{name} must be ISO YYYY-MM-DD") from exc


def parse_datetime(value: str, name: str) -> datetime:
    try:
        parsed = datetime.fromisoformat(value)
    except (TypeError, ValueError) as exc:
        raise BacktestContractError(f"{name} must be an ISO datetime") from exc
    if parsed.tzinfo is None:
        raise BacktestContractError(f"{name} must include a UTC offset")
    return parsed


def require_text(record: dict[str, Any], field: str) -> str:
    value = record.get(field)
    if not isinstance(value, str) or not value.strip():
        raise BacktestContractError(f"{field} is required")
    return value.strip()


@dataclass(frozen=True)
class BacktestSource:
    data: dict[str, Any]

    @property
    def source_id(self) -> str:
        return self.data["source_id"]

    @property
    def origin_group(self) -> str:
        return self.data["origin_group"]

    @property
    def source_class(self) -> str:
        return self.data["source_class"]

    @classmethod
    def from_dict(cls, value: dict[str, Any]) -> "BacktestSource":
        required = (
            "source_id",
            "title",
            "publisher",
            "publication_date",
            "publication_timestamp",
            "available_at",
            "accessed_at",
            "url",
            "local_archive_path",
            "content_hash",
            "source_class",
            "origin_group",
            "revision_id",
            "locator",
        )
        for field in required:
            require_text(value, field)
        parse_date(value["publication_date"], "source.publication_date")
        publication = parse_datetime(value["publication_timestamp"], "source.publication_timestamp")
        available = parse_datetime(value["available_at"], "source.available_at")
        parse_datetime(value["accessed_at"], "source.accessed_at")
        if available < publication:
            raise LeakageError(f"source {value['source_id']} is available before publication")
        if not re.fullmatch(r"[A-F0-9]{64}", value["content_hash"]):
            raise BacktestContractError("source.content_hash must be an uppercase SHA-256 digest")
        if value["source_class"] not in SOURCE_CLASSES:
            raise BacktestContractError(f"invalid source_class: {value['source_class']}")
        return cls(dict(value))


@dataclass(frozen=True)
class AtomicEvent:
    data: dict[str, Any]

    @property
    def event_id(self) -> str:
        return self.data["event_id"]

    @classmethod
    def from_dict(cls, value: dict[str, Any]) -> "AtomicEvent":
        required_text = (
            "case_id",
            "track_id",
            "event_id",
            "event_role",
            "signal_type",
            "signal_subtype",
            "direction",
            "event_at",
            "available_at",
            "date_precision",
            "source_id",
            "entity",
            "product",
            "platform",
            "geography",
            "stated_scope",
            "cutoff_id",
            "cutoff_at",
            "realization_status",
            "false_positive_status",
            "claim",
            "excerpt",
            "locator",
            "evidence_level",
            "scope_match",
        )
        for field in required_text:
            require_text(value, field)
        if value["event_role"] not in EVENT_ROLES:
            raise BacktestContractError(f"invalid event_role: {value['event_role']}")
        if value["signal_type"] not in SIGNAL_TYPES:
            raise BacktestContractError(f"invalid signal_type: {value['signal_type']}")
        if value["direction"] not in {"POSITIVE", "NEGATIVE", "NEUTRAL"}:
            raise BacktestContractError(f"invalid direction: {value['direction']}")
        if value["date_precision"] not in DATE_PRECISIONS:
            raise BacktestContractError(f"invalid date_precision: {value['date_precision']}")
        if value["scope_match"] not in SCOPE_MATCH:
            raise BacktestContractError(f"invalid scope_match: {value['scope_match']}")
        event_at = parse_date(value["event_at"], "event.event_at")
        available_at = parse_datetime(value["available_at"], "event.available_at")
        cutoff_at = parse_datetime(value["cutoff_at"], "event.cutoff_at")
        if event_at > available_at.date():
            raise LeakageError(f"event {value['event_id']} occurs after it was available")
        if cutoff_at < available_at:
            raise LeakageError(f"event {value['event_id']} is included before available_at")
        for name in ("order_distance", "outcome_window"):
            if not isinstance(value.get(name), int) or value[name] < 0:
                raise BacktestContractError(f"{name} must be a non-negative integer")
        for name in ("right_censored", "is_predictor"):
            if not isinstance(value.get(name), bool):
                raise BacktestContractError(f"{name} must be boolean")
        for name in ("counterevidence_ids", "supporting_source_ids", "decision_variables"):
            if not isinstance(value.get(name), list):
                raise BacktestContractError(f"{name} must be a list")
        if not value["supporting_source_ids"]:
            raise BacktestContractError("supporting_source_ids must not be empty")
        return cls(dict(value))
