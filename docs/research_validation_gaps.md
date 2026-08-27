# Research Validation Gaps

## Baseline package gaps

1. ZIP 파일명은 v2지만 내부 `README.md` 제목은 `Final Handoff v1`이다. ZIP SHA-256과 이 불일치를 baseline manifest에 보존한다.
2. Canonical Source Register는 출처명과 날짜를 제공하지만 안정적인 URL, 파일 hash, page/paragraph locator가 충분하지 않다.
3. `04_반도체전파경로_추가_DeepResearch.md`는 Source ID 없이 FACT, 회사 주장, 외부 추정과 분석적 함의를 함께 서술한다.
4. PDF와 Markdown 사이에 제품 사양, 발표 시점, 시장점유율, 병목의 표현 강도가 다르다.
5. 기존 schema에는 original excerpt, locator, 검증자·검증시각, 상태전이 이력, run ID, human override가 없다.

## Claims requiring source-level verification

- HBM4/HBM4E의 sample, qualification, mass production, commercial shipment 시점과 정의
- `industry-first`의 기준이 개발·샘플·양산·상업 출하 중 무엇인지
- 플랫폼별 HBM 용량·대역폭·출시 시점
- HBM 시장 규모·점유율·wafer-input 비중
- HBM과 DDR5 RDIMM의 wafer economics 비교
- HBM wafer intensity 범위
- CoWoS 또는 HBM이 모든 플랫폼에 공통된 binding constraint인지
- CSP CAPEX 중 실제 AI·메모리 관련 component 비중
- 전력 계약, grid connection, energized rack과 실제 memory order의 lead/lag
- HBM 확대가 Server DRAM 가격·공급 우선순위에 미치는 H3 경로

## Validation states

- `SUPPORTED`: 원출처가 해당 범위의 주장을 직접 지지
- `CONTRADICTED`: 동등하거나 더 강한 원출처가 주장을 부정
- `PARTIAL`: 주장 일부 또는 더 좁은 범위만 지지
- `UNVERIFIED`: locator가 있는 원출처를 확보하지 못함
- `KNOWN_UNKNOWN`: 공개정보로 확인할 수 없는 내부 값

최신 Source가 과거 Source를 자동 폐기하지 않는다. 적용 시점과 범위를 비교하고 `valid_from`, `valid_to`, `supersedes`를 기록한다. 동일 보도자료를 재인용한 기사는 독립 Source로 계산하지 않는다.

## First Vertical Slice gaps

사용하는 공식 발표는 sample shipment와 certification 시작 예정, mass-production 준비 목표를 구분한다. 이 Source 하나만으로는 다음을 확인할 수 없다.

- 고객 qualification 통과 여부
- design-in 여부
- 계약 가격 또는 확정 물량
- commercial shipment 여부
- 고객별 공급 비중
- 양산 수율과 공급 안정성
- `industry-first`가 상업적 리더십을 의미하는지

따라서 첫 Memo는 위 항목을 사실로 승격하지 않고 monitor/invalidate 조건으로 남긴다.

## Baseline schema gaps resolved in the approved core

Vertical Slice와 Temporal Update에서 다음 계약을 구현·검증했다.

- Source: URL/local archive, content hash, publication/access date, tier, locator
- Evidence: verbatim excerpt, event type, validation result, transition history, actor, run ID
- Graph: evidence IDs, counterevidence IDs, temporal validity, decision variables
- Contradiction: misconception rule, trigger Evidence, resolution status
- Memo: fact statements별 Evidence IDs와 완전한 Source trace

이는 H1 empirical dataset/method가 승인되었다는 뜻이 아니다. H1의 추가 schema 필요성은 design 단계에서 새로 결정한다.
