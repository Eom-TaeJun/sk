# CODEX MASTER INSTRUCTION
## SK hynix Memory Market Decision Intelligence

### 0. 이 프로젝트의 본질

2026-10-03 사용자는 프로젝트의 우선 목적을 SK하이닉스 관점의 공급망 지도와
2026년 하반기 영업·마케팅·상품기획·신제품사업화 직무에 필요한 산업·상품 배경지식 학습으로 명확히 했다.
따라서 **누가 어떤 메모리 상품을 왜 필요로 하고, 누가 사양·인증·구매를 결정하며,
어떤 공급 조건과 일정 아래 고객 채택으로 연결되는가**를 먼저 구조화한다.
현재 사용자 목적과 공식 직무 근거는 `docs/research/supply_chain/sk_hynix_commercial_role_context.md`에 둔다.

공개정보로 신호의 전파경로·시간축을 구분하고 수요 또는 binding constraint 가시성을
검증해 business-decision context로 번역하는 기존 연구 방법은 유지한다.
제품·직무 학습은 예측력 검증과 다르며, 채용에 활용하는 수행·성과 주장은 실제 작업 범위를 따라야 한다.

이 시스템은 H1 predictor나 HBM commercialization tracker 하나가 아니다. H1은
Demand/Customer Economics부터 Product Mix/Opportunity Cost까지 이어지는 전체
decision architecture의 첫 empirical module이다. 분석 domain, dataset admission gate,
decision flexibility와 module activation의 canonical contract는
`docs/decision_architecture.md`가 소유한다.

핵심 analytical capability는 다음이다.

> 서로 다른 시간축과 신뢰도의 고객·시장·기술·공급 정보를
> 수요·공급·병목·가격·사업화 경로로 구조화하고,
> AI를 근거 회수·관계 연결·변화 감지·반론 검증에 사용해
> Demand Forecast / Customer Priority / Product Mix / CAPA /
> Target Spec / Qualification / TTM 판단에 필요한 신호로 바꿀 수 있다.

따라서 다음 순서를 지킨다.

Real decision problem
→ economic / industry model
→ evidence and data
→ AI-assisted research
→ empirical validation
→ decision update
→ project evidence
→ application / interview translation

`application_evidence/`는 실제 분석·실패·검증에서 파생되는 downstream 기록 계층이다.

---

## 1. 분석 원칙과 downstream project evidence

### M1. 시장 정보를 의사결정 변수로 번역한다
뉴스 요약이 아니라 "어떤 판단이 바뀌는가"까지 간다.

### M2. 메모리 수요를 파생수요로 본다
AI 성장 → HBM 성장으로 직결하지 않는다.

Workload
→ Customer Economics
→ CAPEX
→ Platform
→ Memory Requirement
→ Qualification/LTA
→ Order

### M3. 공급을 Binding Constraint 문제로 본다
Fab capacity 하나가 아니라:
Wafer / Yield / Good Die / Base Die / Packaging / Test /
Qualification / Power / Water / AMHS 중
시점별 Marginal Constraint 후보를 찾는다.

### M4. 가격과 Product Mix를 기회비용 문제로 본다
highest ASP = highest contribution으로 가정하지 않는다.
Opportunity Cost / Shadow Price / Switching Cost /
Qualification / Contract / Strategic Option Value를 함께 본다.

### M5. AI를 판단자가 아니라 분석 구조의 증폭기로 쓴다
AI는 수집, 검색, 추출, 연결, 모니터링, 반론 점검을 맡는다.
FACT 승인과 Strong Inference 승격은 사람 검토를 남긴다.

### M6. Evidence에 따라 판단을 수정한다
처음 가정을 방어하지 않는다.
Contradiction과 Backtest가 기존 판단을 깨면 Confidence를 수정한다.

모든 기능은 M1~M6 중 하나 이상의 실제 분석 문제를 해결해야 한다.
그 결과가 검증된 뒤에만 downstream application evidence로 사용할 수 있다.

---

## 2. 프로젝트 가설과 우선순위

### H1. Demand Signal Quality
공개된 AI-memory 신호가 operational 또는 commercial realization에 가까워질수록
lead time / scope precision / realization uncertainty의 trade-off와
의사결정 가치가 어떻게 달라지는가?

H1은 direct CAPEX-versus-HBM 우열 비교나 universal signal ranking이 아니다.
H1-P Product Commercialization과 H1-C Customer/Platform Realization을
서로 다른 outcome contract로 검증하고 결과를 pooling하지 않는다.

### H2. Bottleneck Migration
AI-memory 공급의 Marginal Constraint가
GPU → Packaging → HBM/Good Stack → Power/Data Center처럼
시간에 따라 이동하는가?

### H3. Product-Mix Opportunity Cost
HBM 수요 증가가 동일 선단 DRAM Resource의 희소가치를 높여
Server DRAM 등 다른 제품의 경제성과 우선순위까지 바꾸는가?

H1은 다음 primary empirical milestone이다. "더 유용한 신호"의 정의와 판정 기준부터 설계하고 검증하며, 가설이 참이라고 가정하지 않는다.

H2는 H1의 최소 empirical pipeline이 신뢰할 수 있을 때 시작하는 secondary extension이다.

H3는 내부 원가·수율·allocation 정보가 없는 상태에서 강한 empirical conclusion을 내리지 않고 conceptual/`KNOWN_UNKNOWN` framework로 유지한다.

---

## 3. AI Architecture — capability first, runtime agnostic

이 문서는 다음 불변조건만 고정한다.

- Source-trace RAG와 Evidence-linked Graph를 사용한다.
- Evidence Governance Harness가 deterministic rule을 소유한다.
- Auditor/Human Review를 conclusion generation과 분리한다.
- Orchestration은 optional capability이며 특정 runtime은 필수가 아니다.
- Agent evaluation 결과는 runner가 구현·실행되기 전에 주장하지 않는다.

Architecture decision과 supersession은 `00_MASTER/02_ARCHITECTURE_DECISIONS.md`, role/context/Harness/eval 상세는 `docs/agent_architecture.md`가 canonical source다.

### 이번 버전에서 제외
- 전용 LLM Fine-tuning
- 별도 사내형 전용 LLM 구축
- 별도 Vector DB 제품 구축
- Graph DB 구축
- 대규모 데이터베이스 인프라 구축
- mandatory multi-agent runtime

구조화된 파일 저장(JSON/CSV/Markdown)과
가벼운 로컬 인덱스/메모리 기반 검색은 허용한다.

현재 질문과 데이터 규모에서 추가 infrastructure의 incremental value가 검증되지 않았기 때문이다.

---

## 4. RAG가 필요한 이유

RAG의 목적은 최신 시장 답변 생성이 아니라
**판단 근거를 원출처까지 되돌릴 수 있게 하는 것**이다.

RAG = Evidence Retrieval Layer

필수 기능:
- Query → 관련 원문 Evidence 검색
- 최신 문서 우선
- 동일 주장에 대한 복수 Source 회수
- Evidence Level 표시
- 결과 문장에 Source ID 연결

금지:
- RAG 결과를 자동 FACT 처리
- RAG가 인과관계를 확정
- RAG가 CAPA/가격을 결정

DB 구축은 제외하므로 MVP는
Markdown/Text corpus + metadata JSON + lightweight local retrieval
형태로 구현한다.

---

## 5. Graph Engineering이 필요한 이유

Graph의 목적은 "멋진 지식그래프"가 아니라
**전파경로와 병목을 구조적으로 보존하는 것**이다.

핵심 경로:

External/Macro/Policy
→ AI Economics
→ Customer Investment
→ Compute Platform
→ Memory Requirement
→ Qualification/Commercial Confirmation
→ Supply Constraint
→ Marketing Decision Variable

Supply path:

Equipment/EUV
→ Node Capacity
→ Wafer
→ Yield/Good Die
→ Base Die
→ Stacking/Packaging
→ Test
→ Qualification
→ Deliverable Qualified Volume

Data-center realization path:

CAPEX
→ Permit/Land
→ Grid/Transformer
→ Cooling
→ Rack Commissioning
→ Accelerator Install
→ Cloud Availability
→ Utilization

Graph는 단일 인과선이 아니라 여러 경로를 연결한다.

권장 구현:
- nodes.json / edges.json
- NetworkX 또는 동등한 경량 Graph library
- Graph DB 금지
- Edge마다 evidence_ids / confidence / counterevidence /
  first_observed / last_observed / decision_variable 저장

주의:
Edge는 항상 "통계적으로 증명된 인과효과"가 아니다.
STRUCTURAL_RELATION / SUPPORTED_HYPOTHESIS / VALIDATED_PATTERN 등을 구분한다.

---

## 6. Graph-aware Retrieval

전체 Graph를 LLM에 넣지 않는다.

질문 또는 새 사건과 관련된:
1. seed entities
2. 1~2 hop subgraph
3. 연결된 evidence_ids
4. RAG 원문

만 Context로 구성한다.

예:
Rubin Spec 변화
→ NVIDIA
→ HBM4
→ Base Die
→ Packaging
→ TTM
관련 Evidence만 회수.

목적:
"문서 검색"에서 "Decision Context Retrieval"로 확장.

---

## 7. Orchestration과 Logical Domain Roles

Demand/Platform, Memory Product, Supply/Infrastructure, Commercial/Policy와 Auditor를 logical roles로 유지한다. 이는 전문성·검사 책임이지 고정 agent process가 아니다.

독립 탐색·상호검증에 분석 가치가 있을 때만 분해·병렬화하고, Verify → Review → Promote처럼 상태 의존적인 처리는 순차 실행한다. Runtime 선택, context hierarchy와 role interface의 canonical 정의는 `docs/agent_architecture.md`를 따른다.

---

## 8. 두 Harness의 책임 분리

### A. Evidence Governance Harness — implemented deterministic core

모든 Evidence는 동일한 절차를 통과한다.

DISCOVER
→ VERIFY
→ CLASSIFY
→ EXTRACT
→ LINK
→ CONTRADICTION_CHECK
→ SIGNAL_SCORE
→ DECISION_IMPACT
→ HUMAN_REVIEW
→ PROMOTE / REJECT

상태:
NEW
VERIFIED
CLASSIFIED
LINKED
CONTRADICTION_CHECKED
DECISION_RELEVANT
PROMOTED

실패/보류:
REJECTED
DUPLICATE
STALE
UNRESOLVED_CONFLICT

목적:
LLM이 문서마다 다른 기준으로 결론을 내리지 못하게 한다.

### B. Agent Execution Harness — future architecture

Task/context/tool/role selection, optional execution, trace/eval/failure capture와 human escalation을 담당할 future capability다. 아직 구현하지 않으며 Evidence Governance Harness를 우회할 수 없다.

Model/program allocation과 `Observed failure → regression eval → improvement → rerun → decision record` loop의 canonical 정의는 `docs/agent_architecture.md`를 따른다.

---

## 9. Evidence Governance

Evidence Level:

A_DIRECT_FACT
공식 문서에 직접 확인되는 사건/수치/규격/일정

B_COMPANY_CLAIM
회사 자사 성능/리더십/전망 주장

C_EXTERNAL_ESTIMATE
시장조사/애널리스트 추정

D_DERIVED_FACT
공식 값으로 직접 계산한 값
formula와 source IDs 필수

E_STRONG_INFERENCE
복수 근거를 연결한 해석
가능하면 독립 Source 2개 이상

F_HYPOTHESIS
추가 검증 필요

규칙:
- CLAIM/ESTIMATE → FACT 자동 승격 금지
- Strong Inference는 Auditor + Human Review 필요
- 충돌은 삭제하지 말고 Contradiction Register에 보존

---

## 10. Economic Decision Model

### Demand
Memory는 Derived Demand.

AI service/workload
→ compute
→ accelerator/server
→ memory content
→ qualification/order

### Supply
공급은 연속된 제약 중 현재 Binding Constraint에 의해 제한.

### Product Mix
HBM과 Server DRAM 등은 선단 Resource를 경쟁할 수 있음.

실제 내부 최적화는 하지 않는다.
대신 어떤 Evidence가 희소 Resource의 Shadow Value를 변화시키는지 기록.

### Bargaining
Memory suppliers / NVIDIA / Hyperscalers / TSMC /
Packaging / ASML 간 가격·물량·인증·TTM 통제권을 구분.

### Decision Loss
수요 과대평가와 과소평가의 비용이 다르다는 점을 기록.

Overestimate:
재고 / 고정비 / 가격 하락

Underestimate:
allocation 실패 / TTM 손실 / 전략고객 관계 악화

### Decision relevance와 조정 가능성

새 변수나 dataset은 economic state, transmission path, analytical role, uncertainty,
affected decision, adjustability, competing explanation, invalidation condition을 모두
설명할 수 있을 때만 채택한다. Evidence 자체와 사람이 검토하는 conceptual
`Decision Impact`는 별도 record로 유지한다.

- Strategic/highly committed: fab, cleanroom, long-lead equipment
- Tactical/partially adjustable: install, ramp, wafer/product mix, packaging, utilization
- Commercial/highly adjustable: monitoring, sample, qualification, marketing, platform, TTM

공개정보는 내부 allocation 결정을 대신하지 않는다. 어느 판단을 준비·우선순위화하고
어떤 내부정보를 추가 확인해야 하는지까지 번역한다.

---

## 11. Signal Dictionary — 필수

최소 Signal:

AI revenue/utilization
CSP CAPEX
platform launch/tape-out
sample
qualification
design-in
LTA
PO/reservation
wafer input
yield
equipment shipment
tool move-in
cleanroom opening
package lead time
server shipment
cloud availability
utilization
contract/spot price
inventory
grid/power/cooling

각 Signal:
- demand_or_supply
- lead/coincident/lag
- what_it_means
- what_it_does_not_mean
- false_positive_risk
- time_horizon
- affected_decision_variable
- confidence_rule

---

## 12. Contradiction Register — 필수

보존할 대표 충돌:

1. HBM always best economics
vs
Server DRAM opportunity cost / constrained-resource economics

2. CAPEX = actual memory demand
vs
Grid/Power/Qualification delay

3. CoWoS = universal bottleneck
vs
Platform-specific wafer/base-die/package/qualification/power constraints

4. Industry-first claims
vs
서로 다른 sample/mass production/commercial shipment 정의

Contradiction은 LLM이 자동 화해시키지 않는다.

---

## 13. Empirical Validation Contract

H1 Gates 1–5는 `docs/exec-plans/active/h1_empirical_validation_design.md`에서 human-approved/frozen 상태다. H1-P는 strict supplier-side `O1_COMMERCIAL_REALIZATION`, H1-C는 separate `P1_PLATFORM_OPERATIONAL_REALIZATION`을 사용한다. 두 strata는 outcome과 signal을 pooling하지 않으며 provenance-complete bridge가 없는 상태에서 direct CAPEX-versus-HBM 비교를 만들지 않는다.

승인된 계약은 temporal ordering, `event_at`/`published_at`/`available_at`/`accessed_at` 분리, future-information leakage, origin-group independence, explicit negative evidence, lead/lag, left truncation과 right censoring을 보존한다. Gates 6–7의 dataset freeze와 최종 H1-P/H1-C verdict는 사람이 별도 승인한다.

삭제되었거나 interrupted 상태인 H1 실행물은 finding으로 사용하지 않는다. 다음 승인 범위는 synthetic 또는 tiny hand-authored fixture를 이용한 measurement contract와 deterministic validation layer뿐이다.

---

## 14. 최종 Decision Memo

최종 시스템의 가장 중요한 결과물.

형식:

1. WHAT CHANGED?
2. EVIDENCE LEVEL
3. WHY DOES IT MATTER?
4. DEMAND OR SUPPLY?
5. WHICH TRANSMISSION PATH CHANGED?
6. CURRENT BOTTLENECK CANDIDATE
7. WHICH ASSUMPTION CHANGED?
8. WHICH MARKETING DECISION VARIABLE IS AFFECTED?
9. CONFIDENCE
10. COUNTEREVIDENCE
11. WHAT WOULD INVALIDATE THIS?
12. WHAT TO MONITOR NEXT?

금지:
"SK하이닉스는 고객 A에 X% CAPA를 배정해야 한다."

허용:
"공개정보상 수요 확정도를 높이는/낮추는 신호가 무엇이며,
어떤 추가 정보가 Product Mix/CAPA/TTM 판단에 필요하다."

---

## 15. Milestone 순서

### Completed foundation

- Repository/Canonical Source 이해
- Evidence Registry, Source-trace RAG
- 최소 Graph/Graph-aware Retrieval
- Evidence Governance Harness, Auditor/Human Review
- HBM4 Vertical Slice와 Temporal Update Decision Memo

### Primary empirical milestone — H1

먼저 H1의 "useful visibility"를 operationally 정의하고 최소 Source·case·cutoff·outcome 계약을 승인한다. 그 뒤 작은 historical validation을 실행한다. 예측 ML을 우선하지 않는다.

### Secondary milestone — H2

H1 pipeline의 temporal/provenance/replay 품질이 검증된 뒤에만 Bottleneck Migration을 확장한다.

### Deferred — H3

공개정보로 opportunity-cost 결론을 지지하지 못하면 conceptual/`KNOWN_UNKNOWN` 상태를 유지한다.

### Optional orchestration experiment

Agent Execution Harness와 특정 runtime은 H1/H2 분석에서 반복 가능한 task decomposition 문제가 확인되고, 추가 복잡성 대비 측정 가능한 가치가 있을 때만 시험한다. Hermes는 가능한 adapter 중 하나다.

---

## 16. Validated baseline

다음 Vertical Slice 경로와 Temporal Update는 구현·검증 완료했다.

New evidence
→ Source verification
→ Evidence classification
→ RAG trace
→ Demand/Supply classification
→ Graph update
→ Contradiction check
→ Signal/confidence update
→ Decision variable impact
→ Decision memo
→ source trace

Dashboard는 필요하지 않다.

---

## 17. Downstream Application Evidence

아래 파일은 산업·직무 학습 내용과 구분하는 실제 분석 수행 증거의 downstream 기록이다. Source trace, run, test, failure 또는 human decision으로 입증된 뒤에만 갱신한다. 학습·지원 목적이 우선이어도 수행하지 않은 분석이나 검증 성과를 기록하지 않는다.

### project_fact_sheet.md
- 기간
- 목적
- 기존 문제
- 내 역할
- 내가 선택한 설계
- 사용 Source 수
- AI가 한 일
- 사람이 한 판단
- 검증
- 실패/수정
- 결과
- 한계

### decision_change_log.md
최소 2개 사례:
Initial assumption
→ New evidence
→ Contradiction
→ Updated conclusion
→ Why this matters to the role

### before_after.md
기존 방식과 비교:
- 정보 Traceability
- 반복분석 시간
- Source 검증 가능성
- 동일 사건 재분석 일관성
- Contradiction 보존
- 판단 업데이트 가능성

정량 수치가 실제로 측정된 경우에만 숫자를 기록.

### recruiter_signal_map.md
각 구현물이 무엇을 증명하는지 매핑.

예:
RAG → 근거 회수/검증
Graph → System-level 전파경로
Signal Dictionary → Demand Forecast
Bottleneck → Supply/CAPA 이해
Empirical validation → 가설 검증
Evidence Governance Harness → AI 결과 통제
Decision Memo → 현업 판단 번역

---

## 18. 개발 규칙

1. 먼저 최소구현.
2. 별도 DB 구축 금지.
3. Fine-tuning 금지.
4. Graph DB 금지.
5. 모든 결과는 파일로 재현 가능.
6. Source ID 없는 결론 금지.
7. 날짜 없는 시장정보는 Strong Evidence로 쓰지 않음.
8. LLM 자유서술을 최종 데이터 구조로 사용하지 않음.
9. Parser/Agent 오류를 로그로 보존.
10. 사람이 수정한 Override도 로그로 보존.
11. 새로운 기술은 문제를 해결할 때만 도입.
12. 구현 중 기존 설계가 과하면 적극적으로 단순화하되,
    Source-trace RAG / Graph / Evidence Governance Harness / Auditor는 유지.
13. 특정 agent runtime이나 multi-agent 수를 Architecture 목표로 삼지 않음.
14. agent failure를 조용히 patch하지 않고 minimal regression eval 후보로 보존.

---

## 19. Current task routing

첫 Vertical Slice와 Temporal Update는 완료되어 보존한다. 새 작업은 루트 `AGENTS.md`를 먼저 읽고 필요한 상세 문서만 추가로 로드한다.

H1 empirical design의 Gates 1–5, measurement contract, deterministic validation layer,
24-Track pre-registration과 4-Track real-data pilot은 구현·보존되었다. H1-P는
customer/commercial acceptance와 supply readiness를 분리하고, H1-C는 broad investment
context와 operational deployment를 분리한다. Production-stage record는 CONTEXT이며
customer order, qualification, O1 또는 demand volume을 증명하지 않는다.

다음 승인 작업은 **revised economic and business interpretation contract 아래 24개
pre-registered Track의 full frozen H1 primary-source corpus를 수집하는 것**이다. 이
수집 작업은 outcome-neutral Gate 6 dataset freeze를 만들기 위한 것이며 H1 metric,
lead/lag, realization rate 또는 verdict 계산을 포함하지 않는다. H2/H3, Decision Engine,
orchestration runtime, dashboard와 database 확장은 아직 승인되지 않았다.
