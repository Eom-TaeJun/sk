# Work Review — First Vertical Slice

> Historical review snapshot. 이 문서의 당시 확장 gate는 이후 사용자 승인으로 종료되었다. 현재 next task는 `docs/exec-plans/active/h1_empirical_validation_design.md`가 통제한다.

기준: `00_MASTER/05_WORK_REVIEW_PROMPT.txt`

## 좋은 점

- 시장 요약이 아니라 sample→qualification→TTM gate가 어떤 판단을 바꾸는지 명확히 했다.
- 당시 Hermes 후보를 포함한 어떤 runtime도 판단 규칙을 소유하지 않도록 Adapter와 Evidence Governance Harness를 분리했다.
- Memo의 fact 네 건이 Evidence ID와 원출처 locator까지 추적된다.
- `sample = qualification`, `qualification = confirmed volume`, `industry-first = commercial leadership`을 자동 해소하지 않고 보존했다.
- 최초 자동 승격 결함을 실제 run에서 발견하고 HUMAN_REVIEW 보류로 수정했다.

## 현업 관점의 부족점

- 고객명이 비공개이고 customer-side confirmation이 없다.
- qualification 완료, design-in, 계약 물량, commercial shipment를 확인하지 못했다.
- `CUSTOMER_QUALIFICATION`은 현재 bottleneck의 확정 사실이 아니라 이 Source가 보여주는 다음 gate 후보다.
- generic AI Platform edge는 구조적 연결이며 특정 고객 플랫폼 채택을 의미하지 않는다.

## 과잉 구현 여부

- 전용 DB, UI, Agent 설치, 전체 Backtest를 하지 않아 승인 범위를 지켰다.
- Graph 10 nodes/9 edges는 필수 node type과 decision-variable trace를 증명하는 범위로 제한했다.

## 빠진 검증

- 독립 Source가 없어 Independence factor가 제한된다.
- full-page immutable HTML snapshot 대신 URL과 compact archival excerpt를 보존했다.
- retrieval Precision/Recall은 첫 MVP 종료 조건이 아니므로 측정하지 않았다.
- Human Review는 아직 실제 승인되지 않아 Evidence와 Memo가 보류 상태다.

## 지원서용으로 남겨야 할 증거

- LLM/Agent보다 deterministic Harness에 rule ownership을 둔 설계 판단
- 첫 run의 자동 승격 결함을 폐기하고 human gate로 수정한 과정
- Graph edge 목록을 단일 causal path로 오해하게 만든 표현을 subgraph로 수정한 과정
- Source 1건을 4개 Atomic Evidence와 3개 open contradiction으로 분해한 실행 증거

## 다음 단계 Gate

사용자가 Source trace, draft Memo, open contradiction과 설계 변경을 검토하기 전에는 H1 Backtest나 Hermes monitoring으로 확장하지 않는다.
