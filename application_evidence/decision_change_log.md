# Decision Change Log

## Change 1 — 자동 승격 통제

- Initial assumption: A_DIRECT_FACT와 B_COMPANY_CLAIM은 schema/audit을 통과하면 HUMAN_REVIEW 상태 뒤 자동 PROMOTED해도 된다.
- New evidence: 첫 실제 run의 transition log에서 `actor=deterministic-core`가 human approval 없이 PROMOTED한 사실을 확인했다.
- Evidence level: 프로젝트 실행 Fact
- Contradiction: `HUMAN_REVIEW` 상태를 통과했다는 것과 실제 사람이 승인했다는 것은 다르다.
- Why the old view was insufficient: 자동 승격은 Harness가 human-review gate를 소유한다는 Architecture와 경험기술서의 AI 통제 주장을 약화한다.
- Updated conclusion: `human_approved=false`인 모든 Evidence는 HUMAN_REVIEW에서 중단한다. Memo는 `PENDING_HUMAN_REVIEW` draft로 표시한다. Strong Inference를 포함한 어떤 Evidence도 approval 없이 PROMOTED할 수 없다.
- Affected decision variable: 전체 판단의 Evidence Governance
- Job relevance: AI 결과를 그대로 확정하지 않고 검토 책임과 승격 권한을 분리하는 역량

## Change 2 — Graph 표현 수정

- Initial assumption: 2-hop neighborhood의 edge ID를 화살표로 이어 transmission path로 표시해도 된다.
- New evidence: 첫 Memo 렌더링 결과에서 서로 다른 분기 edge가 하나의 순차 인과경로처럼 읽혔다.
- Evidence level: 프로젝트 실행 Fact
- Contradiction: Graph-aware retrieval 결과는 subgraph이며 단일 validated causal path가 아니다.
- Why the old view was insufficient: 구조적 관계와 검증된 인과경로를 혼동하게 만들 수 있다.
- Updated conclusion: Memo에서 `retrieved 2-hop transmission subgraph`라고 명시하고 edge를 목록으로 표시한다.
- Affected decision variable: Demand Forecast, Qualification, TTM 해석의 범위 통제
- Job relevance: 공급·수요 전파경로를 과도한 인과 주장 없이 설명하는 역량
