# Implementation Plan — First Vertical Slice Only

## Architecture

```text
Hermes → Agent Adapter Layer → Deterministic Core Harness
                                      ↓
                          Evidence → Graph → Audit → Memo
```

Hermes는 이 단계에서 설치하거나 연결하지 않는다. `DemandMemorySensor`, `SupplyInfraSensor`, `CommercialPolicySensor`, `Auditor`의 Adapter contract만 정의한다. 수동 Adapter가 같은 contract로 scenario를 입력하며 Core Harness는 Agent 없이 순차 실행된다.

## Scope

공식 HBM4 발표 한 건을 Source Registry에 등록하고, sample·qualification pending·mass-production target·industry-first claim을 Atomic Evidence로 분리한다. Evidence는 deterministic state machine을 통과한 뒤 파일 기반 Graph, Contradiction Register, Signal/Confidence rubric과 Decision Memo를 갱신한다.

이번 단계에서는 Dashboard, UI, 전용 LLM, Fine-tuning, Vector DB, Graph DB, 대규모 DB, 실시간 monitoring, H2/H3 전체 Backtest를 구현하지 않는다.

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

첫 scenario 실행과 모든 테스트 결과, graph diff, contradiction, Memo, application evidence를 생성한 뒤 중단한다. 다음 단계는 Work 리뷰에서 실제 설계 판단·실패·수정이 증명된 경우에만 H1 Historical Backtest로 확장한다.

## Application evidence

각 문서는 실제 run ID와 테스트 결과를 근거로 갱신한다. 선택한 설계, 버린 대안, 실패와 수정, AI와 사람의 역할, 직무 판단 연결을 기록한다. 측정하지 않은 시간 절감·정확도·성과 수치는 작성하지 않는다.
