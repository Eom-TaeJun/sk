# Project Fact Sheet

- 기간: 2026-08-26, First Vertical Slice
- 프로젝트명: Memory Market Decision Intelligence v2
- 목적: 공개 시장정보 한 건을 Source 검증부터 Decision Memo와 원문 trace까지 재현 가능한 직무 판단 workflow로 변환
- 기존 문제: sample, qualification, mass production, commercial shipment와 회사의 `industry-first` 주장이 한 문서 안에서 쉽게 혼동됨
- 내 역할: 문제·책임 경계 승인, deterministic rule 설계, Evidence/Graph/Memo 계약 결정, 자동 승격 결함 검토 및 수정
- Source/Data 규모: 공식 T1 Source 1건, Atomic Evidence 4건, Graph node 10개, edge 9개
- 내가 직접 설계한 것: 특정 runtime과 Evidence Governance Harness의 책임 분리(초기 Hermes 후보 포함), Source/Evidence 분리, 상태전이, semantic contradiction 3종, confidence rubric, human gate, sentence-level trace
- RAG 역할: 답변 생성이 아니라 Evidence ID→Source ID→excerpt→locator 회수. 초기 retrieval과 2-hop graph-aware retrieval을 분리
- Graph 역할: Customer→Platform→Memory Product→Qualification→TTM→Decision Variable의 최소 subgraph와 Evidence 연결
- Agent/Runtime 역할: 실제 연동하지 않음. Manual Adapter가 runtime-agnostic contract를 사용하며 Hermes는 현재 optional candidate
- Evidence Governance Harness/Auditor 역할: 상태전이, provenance, unsupported inference, semantic boundary, confidence, human-review 보류를 deterministic rule로 통제
- 사람이 최종 판단한 영역: sample을 qualification으로 승격하지 않음, 회사의 first claim을 상업 리더십으로 해석하지 않음, human approval 없는 Evidence를 PROMOTED하지 않음
- AI가 한 일: 공식 Source 후보 확인, Atomic Evidence 후보 구조화, 코드·테스트·Memo 생성, rule 위반 탐지 지원
- 검증 방법: 11개 unit/integration test, 실제 scenario 실행, 동일 입력 replay, trace hash 비교
- 실패/수정: 최초 run에서 HUMAN_REVIEW 통과를 실제 승인처럼 취급해 A/B Evidence를 자동 PROMOTED함. 이를 폐기하고 모든 미승인 Evidence를 HUMAN_REVIEW에 보류하도록 수정. Graph edge 목록을 화살표로 이어 단일 인과경로처럼 보이던 표현도 2-hop subgraph 목록으로 수정
- 버린 대안: Hermes 우선 설치, LLM 자유 판단, Vector/Graph DB, 전체 H1/H2/H3 Backtest, Dashboard
- Before: Canonical 자료에는 출처명이 있었지만 Atomic Evidence 상태, sentence trace, deterministic replay가 없었음
- After: 4개 Memo fact가 각각 Evidence ID, Source ID, original excerpt, locator, URL, content hash로 추적됨
- 최종 결과: run `RUN-HBM4-VS-001`, trace hash `B09E8807B3AC2B86CAB0C5CA5623BAC3A33A906813FEF91615378B52922603BC`, blocking finding 0, open contradiction 3, confidence MEDIUM, human review pending
- 확인된 한계: Source가 1개라 independence가 낮고 고객 qualification·확정 물량·commercial shipment를 확인하지 못함. 검색 Precision과 운영 성능은 평가하지 않음
- SK하이닉스 직무 연결: Qualification/TTM gate, Demand Forecast 신호 품질, Customer Priority, Supply Risk를 공개정보 한계 안에서 구분

## Human Review + Temporal Update 보완 수행 Fact

- 범위: H1 Backtest 이전 Core contract 보완. Hermes/H1/H2/H3/UI/DB는 추가하지 않음
- Source/Data 누적: T1 공식 Source 2건, Atomic Evidence 6건, Graph node 13개, edge 14개
- Human Review: global boolean을 제거하고 Evidence별 immutable Review Manifest를 구현. 2025 Evidence 4건은 사용자 승인 범위를 A_DIRECT_FACT/B_COMPANY_CLAIM level에 고정해 PROMOTED
- Promotion rule: A~D는 명시적 APPROVE와 blocking audit 0건, E는 추가로 독립 Source 2개 이상과 unresolved contradiction 0건, F는 승격 불가
- Temporal Update: 2025 sample/qualification-pending baseline을 보존한 채 2026 mass-shipment event 1건(A)과 H2 ramp plan 1건(B)을 추가
- 사람이 판단한 영역: 2026 신규 Evidence는 아직 Evidence별 review를 받지 않았으므로 HUMAN_REVIEW에 유지. mass shipment를 qualification/customer share/price/volume으로 확장하지 않음
- 실제 판단 변화: TTM은 준비 목표에서 관찰된 mass-shipment event로 이동. Demand Forecast visibility와 initial supply readiness 판단은 개선됐지만 규모·고객 경제성은 미확인
- 재현성: baseline→temporal state diff hash `52111BFF0AA10AD3BE1EE7B94A1868F0C36122587D129D5D97B1D515619EC340`
- 검증: 18개 unit/integration test 통과. prior Evidence 보존, 최신 Source 비덮어쓰기, diff replay 일치 포함
- 실패/수정: Windows cp949 console에서 Unicode 출력 실패를 발견해 persisted UTF-8과 console-safe JSON을 분리
- 남은 unknown: customer qualification status, customer identity/share, price/contract terms, shipment volume/qualified-good-volume

## H1 Measurement Contract 구현 수행 Fact

- 범위: 승인된 H1-P Product Commercialization과 H1-C Customer/Platform Realization의 측정 계약 및 deterministic validation만 구현. 실제 Historical Source 수집, empirical H1 실행, 성능 계산과 verdict는 수행하지 않음
- 구현 계약: Track/Event/Snapshot JSON Schema와 Python dataclass contract를 추가하고 `SIGNAL`/`OUTCOME`/`CONTEXT`, transmission layer, decision question을 필수화
- 의미 통제: sample≠qualification complete, qualification underway≠complete, preview/plan≠platform operational realization, supplier O1≠platform P1을 코드와 합성 반례로 검증
- 시간 통제: `event_at`/`published_at`/`available_at`을 분리하고 cutoff 이후 정보 차단, date-only Source의 publisher-local 다음 날 fallback, immutable revision/supersession을 구현
- Source/Scope 통제: `source_id`와 `origin_group`을 분리해 mirror Source를 독립 근거로 중복 계산하지 않고, 서로 다른 Track 또는 호환되지 않는 scope의 join을 차단
- Censoring 통제: 6/12/18개월별 관찰 상태를 계산하고 right-censored record를 failure/no-realization denominator에서 제외. left truncation을 Track/Event에 명시적으로 보존
- 재현성: cutoff, freeze, horizon, included Track/Event/Source, HOLD/EXCLUDE 이유, observation assessment를 canonical SHA-256 manifest로 고정하고 동일 입력 replay hash 일치를 검증
- 검증 규모: synthetic Track 4개, valid Event 12개, invalid semantic fixture 3개. 신규 측정 계약 test 18개와 기존 regression 18개를 합쳐 36개 통과; 기존 baseline/temporal pipeline 두 개도 exit code 0
- 구현 중 수정한 판단: raw Event에 하나의 `right_censored=true`를 고정하면 같은 Event의 6/12/18개월 sensitivity가 충돌함을 확인. raw 선언은 nullable로 두고 snapshot의 freeze+horizon마다 상태를 계산하도록 수정
- AI가 수행한 일: 계약/검증 코드와 adversarial fixture 초안, deterministic test/replay 수행. 사람이 통제할 일: 최종 Track·stage·scope admissibility, origin-group 적정성, proxy availability 승인, empirical sufficiency와 H1 verdict
- 보존한 한계: 실제 수요 신호의 우열, forecasting accuracy, realization/false-positive rate, 시간 절감 수치를 주장하지 않음
