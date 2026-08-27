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
