# Architecture Decisions

## ADR-001 — Real analytical objective first

- Previous decision: 채용 경험 증명을 프로젝트의 직접 목적이자 Architecture 선택 기준으로 두었다.
- Why it was reasonable: 초기 범위를 제한하고 직무와 무관한 기술 확장을 막는 데 유용했다.
- New principle: 구현된 Workflow가 먼저 실제 분석 문제를 풀고 검증 가능한 판단을 남겨야 한다.
- Updated decision: 프로젝트의 1차 목적은 signal quality와 binding constraint를 Evidence로 검증하는 decision intelligence다. `application_evidence/`는 실제 수행 Fact를 보존하는 downstream layer다.

## ADR-002 — Runtime-agnostic orchestration

- Previous decision: Hermes agent orchestration을 필수 Architecture로 고정했다.
- Why it was reasonable: Demand·Product·Supply·Commercial 관찰을 분리하고 Auditor를 독립시키려는 책임 분해는 타당했다.
- New principle: 책임 분해와 특정 runtime 선택은 별개이며, framework는 측정 가능한 분석 가치가 있을 때만 도입한다.
- Updated decision: Orchestration을 task decomposition, context/tool selection, optional delegation, aggregation capability로 정의한다. Codex-native capability, Hermes adapter 또는 compatible runtime은 교체 가능하다. Hermes는 optional adapter candidate이며 Core rule owner가 아니다.

## ADR-003 — Logical roles, selective execution

Demand/Platform, Memory Product, Supply/Infrastructure, Commercial/Policy, Auditor를 logical domain roles로 유지한다. 모든 작업에서 각 역할을 별도 agent로 실행하지 않는다. 독립 조사나 상호검증에 분해 가치가 있을 때만 병렬 위임하며, Evidence 승인처럼 순서 의존적인 처리는 순차 실행한다. Auditor 책임은 시장 결론 생성과 논리적으로 분리한다.

## ADR-004 — Two harnesses

- `Evidence Governance Harness` — 현재 구현된 deterministic core. Provenance, schema, 상태전이, contradiction, confidence, human review, promotion과 replay 규칙을 소유한다.
- `Agent Execution Harness` — future architectural capability. Task framing, smallest-sufficient context, tool/role selection, optional execution, trace/eval/failure capture와 human escalation을 담당한다.

두 Harness를 하나의 모호한 `Harness`로 부르지 않는다. Agent Execution Harness는 Evidence Governance Harness를 우회하거나 규칙을 변경할 수 없다.

## ADR-005 — Capability allocation

Model 사용이 적합한 영역:

- Evidence 의미·범위 해석
- relation/contradiction 후보 생성
- context-sensitive classification
- hypothesis candidate 생성

Deterministic program이 소유할 영역:

- filtering, deduplication, schema validation
- date alignment, unit normalization, joins, lag construction
- numeric consistency, aggregation
- state transition, source trace, replay hash

목표는 LLM 사용량이 아니라 semantic judgment가 필요한 경계에서만 probabilistic reasoning을 쓰는 것이다.

## ADR-006 — Preserved core

- RAG는 답변 생성이 아니라 Source Trace 회수 계층으로 유지한다.
- Graph/Graph-aware Retrieval은 전파경로와 관련 Evidence 범위를 보존하되 causal proof로 표현하지 않는다.
- Evidence Governance Harness와 Auditor/Human Review를 유지한다.
- file/JSON 기반 저장을 유지한다.

## ADR-007 — Deferred infrastructure

현재 제외:

- dedicated LLM, fine-tuning
- dedicated vector DB, graph DB, enterprise DB
- mandatory multi-agent runtime
- dashboard/UI

제외 이유는 채용용 Prototype이어서가 아니라, 현재 분석 질문·데이터 규모·재현성 요구에 파일 기반 deterministic workflow가 충분하고 추가 인프라의 incremental value가 검증되지 않았기 때문이다.

## Milestone order

1. H1 Demand Signal Quality empirical design and minimum validation
2. H2 Bottleneck Migration extension after H1 pipeline credibility
3. H3 Product-Mix Opportunity Cost as conceptual/`KNOWN_UNKNOWN` framework until public evidence is sufficient

상세 책임·평가 구조는 `docs/agent_architecture.md`를 canonical reference로 사용한다.

## ADR-008 — Interrupted H1 implementation removed from baseline

- Previous event: H1 design approval 전에 execution engine, dataset과 generated output이 만들어졌다.
- Why it stopped: Human steering보다 구현이 앞서 case/outcome/cutoff/verdict contract가 승인되지 않았다.
- Updated decision: 해당 묶음은 current baseline에서 제거하고 Git history와 `docs/exec-plans/completed/interrupted_h1_experiment.md`에만 보존한다.
- Consequence: H1 finding은 아직 없으며 다음 task는 design-only다. Sunk cost는 KEEP 사유가 아니다.
