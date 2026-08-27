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

## ADR-009 — H1 two-strata empirical contract after public-data feasibility

- Previous analytical intention: broad CSP CAPEX와 downstream HBM commercialization signal을 provenance-compatible matched track에서 직접 비교한다.
- Feasibility evidence: ex-ante public universe에서 product-commercialization과 customer/platform-realization 후보군은 각각 구성할 수 있었지만, broad CAPEX → named platform → named HBM supplier → strict supplier-side commercial realization을 모두 연결한 provenance-complete bridge는 0건이었다. Product-scope explicit negative disclosure도 희소했다.
- Human decision: construct validity를 지키기 위해 H1을 H1-P Product Commercialization과 H1-C Customer/Platform Realization의 separate primary strata로 동결한다. H1-P는 O1 supplier-side proxy, H1-C는 separate P1 platform-operational outcome을 사용하며 outcomes와 signal ranking을 pooling하지 않는다.
- Bridge boundary: complete primary-source chain이 독립적으로 닫힐 때만 exploratory corroboration으로 유지한다. Market share, reputation, presumed sole sourcing, analyst estimate 또는 teardown inference로 bridge를 채우지 않는다.
- Frozen gates: historical boundary/universe, source/timestamp contract, signal roles, 6/12/18-month windows, negative-case requirements와 stratum-specific sufficiency thresholds는 H1 Gates 1–5에서 human-approved/frozen 상태다.
- Consequence: H1 finding은 여전히 없으며, 다음 승인 범위는 synthetic 또는 tiny hand-authored fixture를 이용한 measurement contract와 deterministic validation layer뿐이다. Historical dataset 수집과 empirical H1 실행은 별도 승인이 필요하다.
