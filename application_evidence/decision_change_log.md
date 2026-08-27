# Decision Change Log

## Change 1 — 자동 승격 통제

- Initial assumption: A_DIRECT_FACT와 B_COMPANY_CLAIM은 schema/audit을 통과하면 HUMAN_REVIEW 상태 뒤 자동 PROMOTED해도 된다.
- New evidence: 첫 실제 run의 transition log에서 `actor=deterministic-core`가 human approval 없이 PROMOTED한 사실을 확인했다.
- Evidence level: 프로젝트 실행 Fact
- Contradiction: `HUMAN_REVIEW` 상태를 통과했다는 것과 실제 사람이 승인했다는 것은 다르다.
- Why the old view was insufficient: 자동 승격은 Evidence Governance Harness가 human-review gate를 소유한다는 Architecture와 AI 통제 원칙을 약화한다.
- Updated conclusion: `human_approved=false`인 모든 Evidence는 HUMAN_REVIEW에서 중단한다. Memo는 `PENDING_HUMAN_REVIEW` draft로 표시한다. Strong Inference를 포함한 어떤 Evidence도 approval 없이 PROMOTED할 수 없다.
- Affected decision variable: 전체 판단의 Evidence Governance
- Job relevance: AI 결과를 그대로 확정하지 않고 검토 책임과 승격 권한을 분리하는 역량

> 후속 수정: 단일 `human_approved` boolean은 Evidence별 판단을 표현하지 못해 Change 3의 Review Manifest로 대체했다.

## Change 2 — Graph 표현 수정

- Initial assumption: 2-hop neighborhood의 edge ID를 화살표로 이어 transmission path로 표시해도 된다.
- New evidence: 첫 Memo 렌더링 결과에서 서로 다른 분기 edge가 하나의 순차 인과경로처럼 읽혔다.
- Evidence level: 프로젝트 실행 Fact
- Contradiction: Graph-aware retrieval 결과는 subgraph이며 단일 validated causal path가 아니다.
- Why the old view was insufficient: 구조적 관계와 검증된 인과경로를 혼동하게 만들 수 있다.
- Updated conclusion: Memo에서 `retrieved 2-hop transmission subgraph`라고 명시하고 edge를 목록으로 표시한다.
- Affected decision variable: Demand Forecast, Qualification, TTM 해석의 범위 통제
- Job relevance: 공급·수요 전파경로를 과도한 인과 주장 없이 설명하는 역량

## Change 3 — Evidence별 승인과 시간축 판단 갱신

- Initial assumption: 첫 Vertical Slice 전체를 승인하면 하나의 global approval flag로 모든 Evidence를 함께 승격할 수 있다.
- New evidence: 같은 Source 안에서도 `A_DIRECT_FACT`인 sample/certification 문장과 `B_COMPANY_CLAIM`인 mass-production target/industry-first 표현의 승인 범위가 달랐다. 또한 2026년 공식 실적 발표는 HBM4 mass shipment 시작은 관찰 사건으로, H2 ramp는 미래 계획으로 구분했다.
- Evidence level: 프로젝트 실행 Fact + T1 공식 Source
- Contradiction: Scenario 승인과 각 Atomic Evidence의 level별 승인은 동일하지 않다. 최신 Source도 이전 Evidence를 삭제하지 않으며, mass shipment는 price·volume·customer share를 뜻하지 않는다.
- Why the old view was insufficient: global boolean은 누가 어떤 Evidence를 어느 level로 승인·보류·거절했는지 남기지 못하고, 새 사건이 과거 상태를 덮어쓰게 만들 위험이 있다.
- Updated conclusion: `review_id/evidence_id/reviewer/decision/approved_evidence_level/reason/reviewed_at/run_id`를 갖는 immutable Review Manifest를 도입했다. 2025 Evidence 4건은 사용자 승인 범위를 각 level에 고정해 PROMOTED했고, 새 2026 Evidence 2건은 별도 human record가 없어 HUMAN_REVIEW에 보류했다. 판단은 `sample·qualification pending → mass shipment observed`로 바뀌었지만 qualification/customer/price/volume은 계속 unknown으로 유지했다.
- Affected decision variable: TTM, Demand Forecast, Supply Risk
- Job relevance: 신제품사업화 단계 전이를 구분하고, 새 시장정보가 들어왔을 때 기존 근거를 보존하면서 판단만 갱신하는 역량

## Change 4 — Windows replay 출력 호환성

- Initial assumption: UTF-8 Memo를 그대로 console JSON으로 출력해도 재실행이 끝까지 성공한다.
- New evidence: 실제 baseline 실행은 산출물을 모두 생성했지만 Windows `cp949` stdout이 em dash를 인코딩하지 못해 마지막 print 단계에서 `UnicodeEncodeError`가 발생했다.
- Evidence level: 프로젝트 실행 Fact
- Contradiction: 파일 산출물 성공과 CLI process 성공은 동일하지 않다.
- Updated conclusion: 저장 파일은 UTF-8을 유지하고 CLI JSON만 ASCII escape로 직렬화했다. 이후 baseline→temporal 순차 실행이 exit code 0으로 완료됐다.
- Affected decision variable: 분석 내용이 아니라 replay 신뢰성
- Job relevance: 실패 지점을 숨기지 않고 재현 경로 전체를 검증·수정하는 AI 기반 문제해결

## Change 5 — Public-data 한계에 따른 H1 two-strata 전환

- Initial assumption: broad CSP CAPEX와 downstream HBM commercialization signal을 동일한 provenance-compatible track에서 직접 비교하는 것을 H1의 primary estimand로 유지할 수 있다.
- New evidence: outcome을 보지 않고 구성한 public-data feasibility universe에서 product track 10개와 customer/platform track 14개 후보는 확인했지만, broad CAPEX → named platform → named HBM supplier → strict supplier-side realization을 모두 연결한 provenance-complete bridge는 0개였다. Product-scope explicit negative evidence도 검증되지 않았다.
- Evidence level: 프로젝트 research/design 수행 Fact. Candidate count는 feasibility count이며 empirical outcome 또는 H1 result가 아니다.
- Contradiction: 경제적 전파경로가 개념적으로 타당하다는 것과 공개정보로 동일 track의 모든 고리를 관찰할 수 있다는 것은 다르다.
- Why the old view was insufficient: direct comparison을 유지하려면 market reputation, share estimate, presumed sole sourcing 또는 non-disclosure를 관계/실패로 대체해야 하며, 이는 construct validity와 provenance contract를 훼손한다.
- AI-assisted work: ex-ante candidate universe와 official source-family feasibility, bridge gap, timestamp recoverability, negative-disclosure bias를 구조화하고 Gate 대안을 제안했다.
- Human decision: H1을 H1-P Product Commercialization과 H1-C Customer/Platform Realization으로 분리하고 Gates 1–5를 승인·동결했다. H1-P는 O1 supplier-side proxy, H1-C는 separate P1 platform outcome을 사용하며 direct superiority와 pooled ranking을 금지했다.
- Updated conclusion: 질문을 데이터에 맞춰 약화한 것이 아니라, 관찰 가능한 두 estimand로 분리하고 bridge는 complete primary-source chain이 닫힐 때만 exploratory corroboration으로 남긴다. Sufficiency가 부족하면 해당 stratum은 `INCONCLUSIVE`다.
- Affected decision variable: Demand Forecast, Customer Priority, Qualification, TTM의 public-signal 해석 경계
- Job relevance: 공개정보가 원래 질문을 지지하는지 구현 전에 검증하고, 근거가 부족할 때 인과·고객/공급자 연결을 만들지 않은 채 분석 범위를 수정한 수행 Fact

## Change 6 — Right censoring을 Event 속성에서 Snapshot 판단으로 수정

- Initial assumption: 합성 right-censor Event에 `right_censored=true`를 고정하면 관찰 미완료 상태를 충분히 표현할 수 있다.
- New evidence: 동일 Event와 동일 dataset freeze에서도 6개월 window는 fully observed지만 12개월·18개월 window는 right-censored가 되는 합성 sensitivity test를 확인했다.
- Evidence level: 프로젝트 구현·테스트 수행 Fact
- Contradiction: right censoring은 Event 자체의 영구 속성이 아니라 `available_at + observation window`와 dataset freeze의 관계다.
- Why the old view was insufficient: Event에 단일 boolean을 확정하면 horizon을 바꿀 때 모순이 발생하고, 아직 끝나지 않은 관찰을 실패로 셀 위험이 있다.
- Updated conclusion: raw Event의 censor 선언은 nullable로 유지하고, immutable snapshot 생성 시 6/12/18개월별 `fully_observed`, `right_censored`, `eligible_for_failure_denominator`를 계산한다. right-censored Event는 기술적 기록으로 남기되 실패 분모에는 들어가지 않는다.
- Affected decision variable: H1 Demand Signal Quality의 failure/no-realization 비교 신뢰성
- Job relevance: 시계열 관찰 가능성과 실제 실패를 구분해 Demand Forecast 신호 평가의 편향을 통제한 수행 Fact

## Change 7 — 실제 공시 문구로 production/customer-supply 경계 보강

- Initial assumption: `ORDER_ADJACENT_SUPPLY_COMMITMENT`는 Track/layer 검증만으로 충분하고, O1의 `for supply to a customer` 문구는 현재 customer supply를 나타내는 것으로 처리할 수 있다.
- New evidence: 4개 Pilot Track의 공식 공시를 Atomic Event로 분해하자 “volume production 시작”과 “향후 시점부터 customer supply”가 한 문장에 공존했다. 별도 공시에서는 volume production만 확인되고 order·allocation·agreement는 확인되지 않았다.
- Evidence level: 프로젝트 real-data ingestion/validation 수행 Fact. H1 empirical result가 아니다.
- Contradiction: 생산 시작은 supply commitment가 아니며, 미래 고객 공급 표현은 공시 시점의 commercial realization이 아니다.
- Why the old view was insufficient: 기존 phrase rule은 생산 단계나 미래 표현을 주문근접 신호/O1로 과대승격할 수 있었다.
- AI-assisted work: 13개 Primary Source에서 15개 Atomic Event 후보를 구조화하고, 실제 실패 문구를 최소 합성 fixture로 축약해 회귀 테스트를 제안했다.
- Human decision required: HOLD 4건의 최종 admissibility와 생산단계를 별도 context class로 둘지는 아직 승인되지 않았다.
- Updated conclusion: commitment class에는 agreement/order/allocation 등 affirmative term을 요구하고, future-dated customer supply는 current O1에서 차단한다. 실제 Pilot Event는 11개 미검토 수용 후보와 4개 HOLD로 보존하며 자동 승인하지 않는다.
- Affected decision variable: Commercialization Visibility, Qualification, TTM, Demand Forecast
- Job relevance: 제품 양산·고객 공급·주문 신호를 구분하고, 실제 공시가 규칙의 약점을 드러냈을 때 fixture→test→최소 rule change로 수정한 수행 Fact

## Change 8 — 공시일 정밀도와 회고 사건일 정밀도 분리

- Initial assumption: Event의 단일 `date_precision`으로 게시/가용 시점과 사건 발생 정밀도를 함께 표현할 수 있다.
- New evidence: Google Cloud 공식 자료는 게시일은 일 단위로 확인되지만 GA 발생은 “2024년 말까지”라는 회고형 기간으로만 표현했다.
- Evidence level: 프로젝트 schema validation 수행 Fact. GA의 성과나 H1 우열을 뜻하지 않는다.
- Contradiction: day-known publication과 month-bounded event를 하나의 precision으로 저장하면 둘 중 하나의 시간정보가 왜곡된다.
- Updated conclusion: 기존 `date_precision`은 publication/availability fallback 통제에 유지하고 optional `event_date_precision`을 추가했다. 보수적 event boundary와 실제 `available_at`을 분리해 future-information leakage를 막는다.
- Affected decision variable: Platform Deployment Visibility의 temporal ordering
- Job relevance: 실제 공개자료의 시간 정밀도 차이를 데이터 계약에 반영하고, 후대 공시를 과거 snapshot에 누출하지 않는 수행 Fact
