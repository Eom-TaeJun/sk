# Vertical Slice 구현 기록

## Status and decision history

이 문서의 First Vertical Slice 범위는 구현·검증 완료되었으며 아래 계약은 historical implementation record로 보존한다.

- Previous decision: Hermes를 eventual mandatory orchestrator로 두고 동일 adapter contract를 먼저 검증했다.
- Why it was reasonable then: Agent가 rule을 소유하지 못하게 하고 deterministic core를 먼저 완성하는 데 효과적이었다.
- Updated decision: adapter/core 분리는 유지하되 Hermes 의무화는 해제한다. Orchestration은 runtime-agnostic capability이며 특정 runtime은 측정 가능한 incremental value가 있을 때만 선택한다.
- 당시 다음 단계: H1 empirical validation design 승인. 이후 승인·자료 준비 상태는 [참조 안내](reference_index.md), 현재 작업은 [지표 수집 목적](research/supply_chain/indicator_collection_purpose.md)을 따른다.
- Baseline cleanup: 승인 전에 생성된 H1 engine/data/run/schema/log는 제거했다. H1 finding은 없으며 역사 note는 `docs/exec-plans/completed/interrupted_h1_experiment.md`에 있다.

## Architecture

```text
Optional runtime / orchestration capability
→ Agent Execution Harness (future)
→ Agent Adapter Layer
→ Evidence Governance Harness (implemented deterministic core)
→ Evidence → Graph → Audit → Memo
```

`DemandMemorySensor`, `SupplyInfraSensor`, `CommercialPolicySensor`, `Auditor`는 logical role contract다. 수동 Adapter가 같은 contract로 scenario를 입력하며 Evidence Governance Harness는 Agent 없이 순차 실행된다. Hermes는 삭제하지 않지만 optional adapter candidate로만 남긴다.

## Scope

공식 HBM4 발표 한 건을 Source Registry에 등록하고, sample·qualification pending·mass-production target·industry-first claim을 Atomic Evidence로 분리한다. Evidence는 deterministic state machine을 통과한 뒤 파일 기반 Graph, Contradiction Register, Signal/Confidence rubric과 Decision Memo를 갱신한다.

이 범위에서는 Dashboard, UI, 전용 LLM, Fine-tuning, Vector DB, Graph DB, 대규모 DB, 실시간 monitoring, orchestration runtime과 H2/H3 전체 Backtest를 구현하지 않았다.

## Repository layout

```text
00_MASTER/                 # immutable source-package instructions
01_CANONICAL_SOURCES/      # immutable canonical context
02_SCHEMAS/                # original schema baseline
03_TEMPLATES/              # original application templates
docs/
data/
  raw/baseline/
  raw/scenarios/
  sources/
  evidence/
  graph/
  audit/
  signals/
  runs/
src/
  core/
  retrieval/
  graph/
  audit/
  memo/
  adapters/
tests/
logs/
application_evidence/
```

## Data and workflow

1. Source Registry가 provenance와 content hash를 검증한다.
2. Manual Adapter가 고정 scenario payload를 반환한다.
3. Harness가 Evidence를 `NEW → VERIFIED → CLASSIFIED`로 전이한다.
4. lightweight retrieval이 Evidence/Source trace를 반환한다.
5. file Graph가 Evidence ID를 가진 edge만 추가한다.
6. Harness가 `LINKED → CONTRADICTION_CHECKED`로 전이한다.
7. Auditor가 세 가지 semantic misconception과 unsupported inference를 기록한다.
8. deterministic rubric이 Directness, Independence, Temporal Fit, Scope Fit, Contradiction Penalty를 계산한다.
9. 관련 decision variables가 확인되면 `DECISION_RELEVANT → HUMAN_REVIEW`로 전이한다.
10. A/B/C/D Evidence는 규칙과 audit을 통과하면 promote할 수 있다. E Strong Inference는 human approval 없이는 promote할 수 없다.
11. Memo Builder가 모든 fact statement의 Evidence ID와 Source trace를 검증한다.
12. 같은 scenario를 fresh workspace에서 replay해 동일 state, graph diff, trace hash를 확인한다.

## State machine

정상 상태:

`NEW → VERIFIED → CLASSIFIED → LINKED → CONTRADICTION_CHECKED → DECISION_RELEVANT → HUMAN_REVIEW → PROMOTED`

실패·보류 상태:

`REJECTED`, `DUPLICATE`, `STALE`, `UNRESOLVED_CONFLICT`

모든 transition은 timestamp, actor, reason, run ID를 기록한다.

## Confidence rubric

내부 점수는 다음 가중 합으로 계산한다.

- Directness: 35%
- Independence: 20%
- Temporal Fit: 20%
- Scope Fit: 25%
- Contradiction Penalty: 최대 20% 차감

Memo에는 확률로 표현하지 않고 `LOW`, `MEDIUM`, `HIGH`와 요인 설명을 표시한다.

## Test and exit gate

필수 테스트는 missing provenance, invalid transition, duplicate idempotency, retrieval trace, graph edge trace, contradiction preservation, unsupported inference, Strong Inference human gate, Memo fact trace, deterministic replay다.

첫 scenario와 Temporal Update 실행, 테스트, graph diff, contradiction, Memo는 완료되었다. 당시 다음 단계는 empirical question, matched case, Source hierarchy, cutoff, outcome과 기각 조건을 설계·승인하는 것이었다. 이 문서는 그 시점의 구현 이력이다.

## Application evidence

각 문서는 실제 run ID와 테스트 결과를 근거로만 갱신한다. Application Evidence는 분석의 downstream layer이며 Architecture 요구를 결정하지 않는다. 선택한 설계, 버린 대안, 실패와 수정, AI와 사람의 역할, 직무 판단 연결을 기록하되 측정하지 않은 시간 절감·정확도·성과 수치는 작성하지 않는다.

## Next implementation gate

이 구현 당시에는 **H1 empirical validation design**이 다음 작업이었고 승인 전 수집·dataset·실행을 금지했다. 이후 Gates 1–5 승인과 corpus/Gate 6 검토 패키지 준비는 [참조 안내](reference_index.md)에 정리한다. 사람 Gate 6 동결은 여전히 대기 중이다.

현재 작업과 구현 제한은 [AGENTS.md](../AGENTS.md)를 따른다. 이 역사 계획의 next-task 문구로 H1 분석이나 미래 runtime·dashboard·DB를 활성화하지 않는다.
