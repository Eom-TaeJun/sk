from __future__ import annotations

from dataclasses import dataclass

from .models import EvidenceLevel, EvidenceRecord, EvidenceStatus, Transition


class InvalidTransition(ValueError):
    pass


class HumanReviewRequired(PermissionError):
    pass


NORMAL_NEXT = {
    EvidenceStatus.NEW.value: EvidenceStatus.VERIFIED.value,
    EvidenceStatus.VERIFIED.value: EvidenceStatus.CLASSIFIED.value,
    EvidenceStatus.CLASSIFIED.value: EvidenceStatus.LINKED.value,
    EvidenceStatus.LINKED.value: EvidenceStatus.CONTRADICTION_CHECKED.value,
    EvidenceStatus.CONTRADICTION_CHECKED.value: EvidenceStatus.DECISION_RELEVANT.value,
    EvidenceStatus.DECISION_RELEVANT.value: EvidenceStatus.HUMAN_REVIEW.value,
    EvidenceStatus.HUMAN_REVIEW.value: EvidenceStatus.PROMOTED.value,
}

TERMINAL_FAILURES = {
    EvidenceStatus.REJECTED.value,
    EvidenceStatus.DUPLICATE.value,
    EvidenceStatus.STALE.value,
    EvidenceStatus.UNRESOLVED_CONFLICT.value,
}


@dataclass
class DeterministicHarness:
    actor: str = "deterministic-core"

    def transition(
        self,
        evidence: EvidenceRecord,
        target: str,
        reason: str,
        run_id: str,
        timestamp: str,
        *,
        human_approved: bool = False,
    ) -> None:
        current = evidence.status
        if target not in TERMINAL_FAILURES and NORMAL_NEXT.get(current) != target:
            raise InvalidTransition(f"invalid transition {current} -> {target}")
        if (
            current == EvidenceStatus.HUMAN_REVIEW.value
            and target == EvidenceStatus.PROMOTED.value
            and not human_approved
        ):
            level = EvidenceLevel(evidence.evidence_level).value
            raise HumanReviewRequired(
                f"{level} cannot be promoted without explicit human approval"
            )
        transition = Transition(
            from_status=current,
            to_status=target,
            timestamp=timestamp,
            actor=self.actor,
            reason=reason,
            run_id=run_id,
        )
        transition.validate()
        evidence.transitions.append(transition)
        evidence.status = target
