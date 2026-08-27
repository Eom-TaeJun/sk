from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import date, datetime
from enum import Enum
import re
from typing import Any


class ContractError(ValueError):
    """Raised when an input violates a deterministic data contract."""


class EvidenceLevel(str, Enum):
    A_DIRECT_FACT = "A_DIRECT_FACT"
    B_COMPANY_CLAIM = "B_COMPANY_CLAIM"
    C_EXTERNAL_ESTIMATE = "C_EXTERNAL_ESTIMATE"
    D_DERIVED_FACT = "D_DERIVED_FACT"
    E_STRONG_INFERENCE = "E_STRONG_INFERENCE"
    F_HYPOTHESIS = "F_HYPOTHESIS"


class EvidenceStatus(str, Enum):
    NEW = "NEW"
    VERIFIED = "VERIFIED"
    CLASSIFIED = "CLASSIFIED"
    LINKED = "LINKED"
    CONTRADICTION_CHECKED = "CONTRADICTION_CHECKED"
    DECISION_RELEVANT = "DECISION_RELEVANT"
    HUMAN_REVIEW = "HUMAN_REVIEW"
    PROMOTED = "PROMOTED"
    REJECTED = "REJECTED"
    DUPLICATE = "DUPLICATE"
    STALE = "STALE"
    UNRESOLVED_CONFLICT = "UNRESOLVED_CONFLICT"


class ReviewDecision(str, Enum):
    APPROVE = "APPROVE"
    HOLD = "HOLD"
    REJECT = "REJECT"


def _require_text(value: Any, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ContractError(f"{name} is required")
    return value.strip()


def _parse_date(value: str, name: str) -> None:
    try:
        date.fromisoformat(value)
    except (TypeError, ValueError) as exc:
        raise ContractError(f"{name} must be ISO YYYY-MM-DD") from exc


def _parse_datetime(value: str, name: str) -> None:
    try:
        datetime.fromisoformat(value)
    except (TypeError, ValueError) as exc:
        raise ContractError(f"{name} must be an ISO datetime") from exc


@dataclass(frozen=True)
class SourceRecord:
    source_id: str
    title: str
    publisher: str
    publication_date: str
    accessed_at: str
    url: str | None
    local_archive_path: str | None
    content_hash: str
    source_tier: str
    locator: str

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "SourceRecord":
        record = cls(**data)
        record.validate()
        return record

    def validate(self) -> None:
        for name in ("source_id", "title", "publisher", "source_tier", "locator"):
            _require_text(getattr(self, name), name)
        _parse_date(self.publication_date, "publication_date")
        _parse_datetime(self.accessed_at, "accessed_at")
        if not self.url and not self.local_archive_path:
            raise ContractError("url or local_archive_path is required")
        if not re.fullmatch(r"[A-Fa-f0-9]{64}", self.content_hash or ""):
            raise ContractError("content_hash must be a SHA-256 hex digest")
        if self.source_tier not in {"T1", "T2", "T3"}:
            raise ContractError("source_tier must be T1, T2, or T3")

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class Transition:
    from_status: str | None
    to_status: str
    timestamp: str
    actor: str
    reason: str
    run_id: str

    def validate(self) -> None:
        _require_text(self.to_status, "to_status")
        _parse_datetime(self.timestamp, "transition.timestamp")
        for name in ("actor", "reason", "run_id"):
            _require_text(getattr(self, name), f"transition.{name}")


@dataclass(frozen=True)
class ReviewRecord:
    review_id: str
    evidence_id: str
    reviewer: str
    decision: str
    approved_evidence_level: str
    reason: str
    reviewed_at: str
    run_id: str

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ReviewRecord":
        record = cls(**data)
        record.validate()
        return record

    def validate(self) -> None:
        for name in (
            "review_id",
            "evidence_id",
            "reviewer",
            "approved_evidence_level",
            "reason",
            "run_id",
        ):
            _require_text(getattr(self, name), f"review.{name}")
        try:
            ReviewDecision(self.decision)
        except ValueError as exc:
            raise ContractError(f"invalid review decision: {self.decision}") from exc
        try:
            EvidenceLevel(self.approved_evidence_level)
        except ValueError as exc:
            raise ContractError(
                f"invalid approved evidence level: {self.approved_evidence_level}"
            ) from exc
        _parse_datetime(self.reviewed_at, "review.reviewed_at")

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class EvidenceRecord:
    evidence_id: str
    source_id: str
    publication_date: str
    excerpt: str
    locator: str
    claim: str
    event_type: str
    evidence_level: str
    demand_or_supply: str
    entities: list[str]
    relationship: str
    decision_variables: list[str]
    verification_status: str
    status: str = EvidenceStatus.NEW.value
    transitions: list[Transition] = field(default_factory=list)
    counterevidence_ids: list[str] = field(default_factory=list)
    confidence: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_spec(
        cls,
        spec: dict[str, Any],
        source: SourceRecord,
        run_id: str,
        timestamp: str,
        actor: str,
    ) -> "EvidenceRecord":
        record = cls(
            evidence_id=spec["evidence_id"],
            source_id=source.source_id,
            publication_date=source.publication_date,
            excerpt=spec["excerpt"],
            locator=spec["locator"],
            claim=spec["claim"],
            event_type=spec["event_type"],
            evidence_level=spec["evidence_level"],
            demand_or_supply=spec["demand_or_supply"],
            entities=list(spec.get("entities", [])),
            relationship=spec["relationship"],
            decision_variables=list(spec.get("decision_variables", [])),
            verification_status=spec["verification_status"],
        )
        record.transitions.append(
            Transition(
                from_status=None,
                to_status=EvidenceStatus.NEW.value,
                timestamp=timestamp,
                actor=actor,
                reason="Evidence accepted from adapter as NEW",
                run_id=run_id,
            )
        )
        record.validate_provenance(source)
        return record

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "EvidenceRecord":
        copied = dict(data)
        copied["transitions"] = [Transition(**item) for item in copied.get("transitions", [])]
        return cls(**copied)

    def validate_provenance(self, source: SourceRecord) -> None:
        for name in ("evidence_id", "source_id", "excerpt", "locator", "claim", "event_type", "relationship"):
            _require_text(getattr(self, name), name)
        if self.source_id != source.source_id:
            raise ContractError("evidence source_id does not match the registered source")
        _parse_date(self.publication_date, "evidence.publication_date")
        try:
            EvidenceLevel(self.evidence_level)
        except ValueError as exc:
            raise ContractError(f"unsupported evidence_level: {self.evidence_level}") from exc
        if self.demand_or_supply not in {"DEMAND", "SUPPLY", "BOTH", "NEITHER"}:
            raise ContractError("demand_or_supply must be DEMAND, SUPPLY, BOTH, or NEITHER")
        if self.verification_status not in {"SUPPORTED", "CONTRADICTED", "PARTIAL", "UNVERIFIED", "KNOWN_UNKNOWN"}:
            raise ContractError("invalid verification_status")
        for transition in self.transitions:
            transition.validate()

    def to_dict(self) -> dict[str, Any]:
        result = asdict(self)
        return result
