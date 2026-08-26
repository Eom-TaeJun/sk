# CODEX MASTER INSTRUCTION
## SK hynix Memory Market Decision Intelligence Harness

### 0. 이 프로젝트의 본질

이 프로젝트는 "AI 기술을 많이 구현한 프로젝트"가 아니다.
목표는 SK하이닉스 영업/마케팅·상품기획·신제품사업화 직무에서 실제로 필요한 사고방식을,
공개정보를 이용한 반도체·메모리 전파경로 분석으로 증명하는 것이다.

최종 지원서에서 평가자에게 보내야 할 핵심 신호는 다음이다.

> 서로 다른 시간축과 신뢰도의 고객·시장·기술·공급 정보를
> 수요·공급·병목·가격·사업화 경로로 구조화하고,
> AI를 근거 회수·관계 연결·변화 감지·반론 검증에 사용해
> Demand Forecast / Customer Priority / Product Mix / CAPA /
> Target Spec / Qualification / TTM 판단에 필요한 신호로 바꿀 수 있다.

따라서 구현의 화려함보다 다음 순서가 더 중요하다.

문제정의
→ Evidence
→ 경제학적 구조
→ 전파경로
→ AI 역할 설계
→ 검증/반례
→ 판단 수정
→ Decision Memo
→ 지원서용 경험 증거

---

## 1. 평가자 관점에서 반드시 남겨야 할 메시지

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

모든 기능은 M1~M6 중 하나 이상을 증명해야 한다.
그렇지 않은 기능은 구현하지 않는다.

---

## 2. 고정할 프로젝트 가설

### H1. Demand Signal Quality
Headline CAPEX보다 Qualification / LTA / Power-ready /
실제 Platform deployment에 가까운 신호가
Memory Demand visibility를 더 잘 설명하는가?

### H2. Bottleneck Migration
AI-memory 공급의 Marginal Constraint가
GPU → Packaging → HBM/Good Stack → Power/Data Center처럼
시간에 따라 이동하는가?

### H3. Product-Mix Opportunity Cost
HBM 수요 증가가 동일 선단 DRAM Resource의 희소가치를 높여
Server DRAM 등 다른 제품의 경제성과 우선순위까지 바꾸는가?

MVP는 최소 H1과 H2를 End-to-End로 검증한다.
H3는 공개자료 한계가 크므로 Evidence가 충분할 때만 강하게 결론낸다.

---

## 3. AI Architecture — 필수와 제외

### 필수
1. RAG
2. Graph Engineering
3. Graph-aware Retrieval
4. Hermes Agent Orchestration
5. Harness / State Machine
6. Auditor / Human Review

### 이번 버전에서 제외
- 전용 LLM Fine-tuning
- 별도 사내형 전용 LLM 구축
- 별도 Vector DB 제품 구축
- Graph DB 구축
- 대규모 데이터베이스 인프라 구축

구조화된 파일 저장(JSON/CSV/Markdown)과
가벼운 로컬 인덱스/메모리 기반 검색은 허용한다.

즉:
"전용 DB를 만드는 프로젝트"가 아니라
"Decision Intelligence Workflow를 증명하는 프로젝트"로 유지한다.

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

## 7. Hermes Agent Team — 필수

Hermes는 이 프로젝트에서 **Orchestration Layer**로 사용한다.
Hermes 자체가 성과가 아니다.

현재 구현 전에 Hermes의 실제 설치 버전과 공식 문서를 확인하고
지원하는 Tool/Subagent/Scheduling 방식에 맞춰 구현한다.
가상의 API를 만들지 않는다.

### Agent 1. DEMAND_PLATFORM_AGENT
관찰:
AI service / CSP / NVIDIA / AMD / TPU / Trainium / Maia / MTIA / Custom XPU

출력:
- Demand signal
- Platform change
- Memory requirement
- deployment timing

### Agent 2. MEMORY_PRODUCT_AGENT
관찰:
HBM / DDR / SOCAMM / LPDDR / eSSD / HBF / CXL / PIM
SK hynix product announcements

출력:
- product generation
- sample
- qualification
- mass production
- TTM signal

### Agent 3. SUPPLY_INFRA_AGENT
관찰:
SK hynix / Samsung / Micron / TSMC / ASML /
Packaging / Yield / Cleanroom / Power / Grid / Cooling

출력:
- capacity change
- bottleneck candidate
- lead-time / ramp / infrastructure signal

### Agent 4. COMMERCIAL_POLICY_AGENT
관찰:
LTA / Contract / Price / Inventory /
Multi-source / Export Control / Sovereign AI

출력:
- demand visibility
- bargaining-power signal
- regional/policy change

### Agent 5. AUDITOR_AGENT
입력:
모든 Agent 결과

검사:
- Source duplication
- stale evidence
- FACT/CLAIM/ESTIMATE 혼동
- numeric inconsistency
- unsupported inference
- contradiction
- missing provenance

Auditor는 시장 결론을 새로 만들지 않는다.

### ORCHESTRATOR
Hermes parent/orchestrator 역할.

순서:
Collect
→ Verify
→ Classify
→ Graph update
→ Contradiction check
→ Signal update
→ Decision memo

MVP에서 Agent 수가 과하면
Demand+Memory / Supply+Infra / Commercial+Policy의 3개 Sensor로 합칠 수 있다.
단 Auditor는 분리한다.

---

## 8. Harness / State Machine — 필수

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

## 13. Historical Backtest — 필수

### Case A: 2022-2023 Downcycle
Demand↓
→ Inventory↑
→ Order cut
→ Price↓
→ Profit↓
→ CAPEX↓
→ Supply growth↓
→ Recovery

### Case B: 2023-2025 AI/HBM Upswing
GenAI
→ CSP CAPEX
→ Accelerator
→ HBM requirement
→ Qualification
→ HBM/Packaging capacity
→ Conventional DRAM resource pressure
→ Price/Supply response

### Case C: Bottleneck Migration
GPU
→ Packaging
→ HBM/Good Stack
→ Power/Data Center

각 Edge 검증:
- temporal ordering
- independent support
- counterexample
- false positive
- lead/lag
- confidence

틀린 Edge는 삭제하거나 Confidence를 낮춘다.

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

## 15. 구현 순서

### M0 — Repository & Canonical Sources
Canonical source만 읽고 프로젝트 목표를 재확인.

### M1 — Evidence Registry
Source → Atomic Evidence 변환.

### M2 — RAG
Evidence 원문 회수 및 Source trace.

### M3 — Demand/Supply Graph
두 Graph를 먼저 따로 구축.

### M4 — Graph Integration
Demand + Supply + Data Center path 연결.

### M5 — Signal / Contradiction
Signal Dictionary, Contradiction Register.

### M6 — Historical Backtest
2022~2025 검증.

### M7 — Hermes Agents + Harness
새 Evidence를 동일 Workflow에 넣는 구조.

### M8 — Current 2026 State
Deep Research Evidence 적용.

### M9 — Decision Memo
End-to-End 실행.

### M10 — Application Evidence
프로젝트 수행 Fact / 판단변화 / Before-After 기록.

---

## 16. MVP 종료 조건

다음 한 Scenario가 End-to-End로 돌아가면 MVP 완료.

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

## 17. 반드시 남길 Application Evidence

Codex는 구현만 하지 말고 아래 파일을 계속 갱신한다.

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
Backtest → 가설 검증
Harness → AI 결과 통제
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
    RAG / Graph / Hermes orchestration / Harness / Auditor는 유지.

---

## 19. 처음 Codex가 해야 할 일

코드를 바로 많이 작성하지 말 것.

Step 1.
01_CANONICAL_SOURCES를 읽고
`docs/source_understanding.md` 작성.

Step 2.
현재 Deep Research의 주장 중
FACT/CLAIM/ESTIMATE 구분이 불분명한 항목을
`docs/research_validation_gaps.md`에 기록.

Step 3.
MVP Architecture와 Repository Tree를 제안.

Step 4.
세 가설 H1/H2/H3에 필요한 최소 Dataset을 정의.

Step 5.
그 후 구현을 시작.

첫 구현 목표는:
"한 개의 새 Evidence가 들어와 Decision Memo까지 가는 End-to-End path."

기능 수를 늘리기 전에 이 Path를 먼저 완성한다.
