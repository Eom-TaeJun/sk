from __future__ import annotations

from dataclasses import dataclass

from .models import (
    EvidenceLevel,
    EvidenceRecord,
    EvidenceStatus,
    ReviewDecision,
    ReviewRecord,
    Transition,
)


class InvalidTransition(ValueError):
    pass


class HumanReviewRequired(PermissionError):
    pass


class ReviewLevelMismatch(PermissionError):
    pass


class BlockingAuditFinding(PermissionError):
    pass


class IndependentSupportRequired(PermissionError):
    pass


class UnresolvedContradiction(PermissionError):
    pass


class PromotionProhibited(PermissionError):
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
    ) -> None:
        current = evidence.status
        if target not in TERMINAL_FAILURES and NORMAL_NEXT.get(current) != target:
            raise InvalidTransition(f"invalid transition {current} -> {target}")
        if current == EvidenceStatus.HUMAN_REVIEW.value and target == EvidenceStatus.PROMOTED.value:
            raise HumanReviewRequired("PROMOTED is only reachable through apply_review")
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

    def apply_review(
        self,
        evidence: EvidenceRecord,
        review: ReviewRecord,
        *,
        blocking_findings: list[dict],
        independent_source_count: int,
        unresolved_contradiction_ids: list[str],
    ) -> str:
        if evidence.status != EvidenceStatus.HUMAN_REVIEW.value:
            raise InvalidTransition(f"review requires HUMAN_REVIEW, got {evidence.status}")
        if review.evidence_id != evidence.evidence_id:
            raise HumanReviewRequired("review record belongs to another Evidence ID")
        if review.approved_evidence_level != evidence.evidence_level:
            raise ReviewLevelMismatch(
                f"review approves {review.approved_evidence_level}, evidence is {evidence.evidence_level}"
            )
        decision = ReviewDecision(review.decision)
        if decision == ReviewDecision.HOLD:
            return evidence.status
        if decision == ReviewDecision.REJECT:
            self.transition(
                evidence,
                EvidenceStatus.REJECTED.value,
                f"Human reviewer rejected evidence: {review.reason}",
                review.run_id,
                review.reviewed_at,
            )
            return evidence.status

        level = EvidenceLevel(evidence.evidence_level)
        if level == EvidenceLevel.F_HYPOTHESIS:
            raise PromotionProhibited("F_HYPOTHESIS is retained but cannot be PROMOTED")
        evidence_blockers = [
            item for item in blocking_findings if item.get("evidence_id") == evidence.evidence_id
        ]
        if evidence_blockers:
            raise BlockingAuditFinding(
                f"{evidence.evidence_id} has blocking audit findings"
            )
        if level == EvidenceLevel.E_STRONG_INFERENCE:
            if independent_source_count < 2:
                raise IndependentSupportRequired(
                    "E_STRONG_INFERENCE requires at least two independent sources"
                )
            if unresolved_contradiction_ids:
                raise UnresolvedContradiction(
                    "E_STRONG_INFERENCE cannot be promoted with unresolved contradictions"
                )

        transition = Transition(
            from_status=evidence.status,
            to_status=EvidenceStatus.PROMOTED.value,
            timestamp=review.reviewed_at,
            actor=f"human-review:{review.reviewer}",
            reason=f"Evidence-level APPROVE at {review.approved_evidence_level}: {review.reason}",
            run_id=review.run_id,
        )
        transition.validate()
        evidence.transitions.append(transition)
        evidence.status = EvidenceStatus.PROMOTED.value
        return evidence.status
