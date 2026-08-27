# 어디에서 무엇을 사용할지

도구 이름보다 필요한 capability와 책임 경계를 먼저 정한다. 작업자는 `AGENTS.md`에서 현재 task에 필요한 상세 문서만 선택한다.

## 1. Semantic model work

모델은 고정 규칙만으로 처리하기 어려운 작업을 보조한다.

- Source discovery와 relevance 후보 선별
- Evidence 의미·범위 해석
- Atomic Evidence와 relation 후보 생성
- FACT/CLAIM/ESTIMATE/INFERENCE 후보 분류
- contradiction·counterexample 탐색
- 가설 후보와 추가 확인 질문 생성

모델 출력은 candidate다. 원출처 검증, Evidence 승격, causal validity, H1/H2 verdict와 최종 business recommendation은 자동 확정하지 않는다.

## 2. Deterministic program work

다음은 모델 prompt가 아니라 코드·schema·test로 통제한다.

- provenance 필수값과 content hash 검증
- filtering, deduplication, date/cutoff alignment
- unit normalization, joins, lag construction, aggregation
- numeric consistency와 허용 상태전이
- Evidence/Graph/Memo trace 검증
- replay hash와 regression software tests

## 3. Orchestration capability

필요 기능:

- task decomposition
- smallest-sufficient context selection
- tool와 logical domain role 선택
- 독립 subtask의 optional parallel delegation
- 결과 aggregation, trace와 failure capture
- human escalation

Codex-native capability, Hermes adapter 또는 다른 compatible runtime을 사용할 수 있다. 어떤 runtime도 필수가 아니며, Evidence Governance Harness의 규칙을 소유하지 않는다. Hermes를 시험할 경우 실제 version과 공식 interface를 검증하고 가상의 API를 만들지 않는다.

## 4. Logical domain roles

- Demand / Platform
- Memory Product
- Supply / Infrastructure
- Commercial / Policy
- Auditor

역할은 전문성·검사 책임을 뜻하며 고정 agent process 수를 뜻하지 않는다. 모든 역할을 매번 실행하지 않는다. 독립 Source 탐색·cross-check는 병렬화할 수 있지만, Verify → Promote와 같은 상태 의존 흐름은 순차 실행한다. Auditor는 conclusion generation과 논리적으로 분리한다.

## 5. Research capability

공식 공시·IR·제품 발표·정부/규제 자료를 우선해 Source 후보를 찾는다. Deep Research 또는 일반 web research는 retrieval 방식 중 하나이며 Canonical Source 자체가 아니다. 원문 URL, publication/available date, locator, excerpt와 hash가 확보되어야 Evidence Governance Harness 입력이 된다.

## 6. Review and application translation

경제 가설, public-data 한계와 decision impact는 human review 대상이다. `application_evidence/`는 검증된 실행 Fact·실패·수정 이후에만 갱신하며 분석보다 앞서 자기소개 문장을 만들지 않는다.

상세 구조는 `docs/agent_architecture.md`, Evidence 규칙은 `00_MASTER/00_CODEX_MASTER_INSTRUCTION.md`를 참조한다.
