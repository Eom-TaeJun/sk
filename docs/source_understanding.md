# Source Understanding

## 프로젝트의 본질

이 프로젝트는 메모리 시장 뉴스 요약기가 아니다. 공개된 고객·플랫폼·제품·공급 Evidence를 검증하고, 서로 다른 시간축의 신호를 SK하이닉스 영업/마케팅·상품기획·신제품사업화 판단 변수로 번역하는 재현 가능한 Decision Intelligence workflow다.

지원하는 판단 변수는 다음과 같다.

- Demand Forecast
- Customer Priority
- Product Mix
- CAPA Allocation
- Target Spec
- Price·Volume
- Qualification
- TTM
- Supply Risk

MVP의 성공 기준은 자연스러운 답변이 아니라 다음 trace가 끊기지 않는 것이다.

`Memo sentence → Evidence ID → Source ID → Original excerpt → Locator`

## v2 패키지의 역할

- `00_MASTER`: 목적, 책임 경계, 금지사항, 구현 순서와 검토 기준을 통제하는 운영 계약
- `01_CANONICAL_SOURCES`: 직무 맥락과 검증 대상 시장 주장의 기준선
- `02_SCHEMAS`: Evidence, Graph, Memo가 자유서술로 흐르지 않게 하는 초기 데이터 계약
- `03_TEMPLATES`: 구현 과정에서 경험기술서용 실제 수행 증거를 누적하는 기록 계약

Canonical Deep Research는 원출처가 아니라 검증할 주장과 가설의 목록으로 취급한다. 원출처 확인 전에는 어떤 문장도 자동으로 FACT로 승격하지 않는다.

## 고정 Architecture와 책임 경계

```text
                 Hermes
                   ↓
          Agent Adapter Layer
                   ↓
        ┌────────────────────┐
        │ Deterministic      │
        │ Core Harness       │
        └────────────────────┘
                   ↓
       Evidence → Graph → Audit → Memo
```

Hermes와 Agent는 workflow를 호출·분배하고 관찰 후보를 반환한다. Adapter는 그 결과를 고정 입력 계약으로 변환한다. Evidence 승인, 상태전이, confidence rubric, contradiction 보존, human-review gate와 Memo trace 규칙은 Core Harness만 소유한다.

Core Harness는 Hermes 없이도 순차 실행과 전체 테스트가 가능해야 한다. Hermes 변경이나 실패가 Evidence·Graph·Audit·Memo 규칙을 바꾸면 안 된다.

## RAG의 역할

RAG는 AI 검색 기능이나 답변 생성기가 아니라 Evidence Retrieval Layer다. 첫 MVP에서는 검색 Precision보다 다음 필드의 완전성을 우선한다.

- Evidence ID
- Source ID
- Original excerpt
- Locator
- Publication date
- Evidence level

검색 결과가 좋아 보여도 Source trace가 끊기면 Decision Memo의 근거로 사용할 수 없다.

## Evidence 해석 원칙

- CAPEX는 주문이나 설치 완료와 동일하지 않다.
- Sample, qualification, design-in, LTA, mass production, commercial shipment를 분리한다.
- 회사의 `industry-first`, 최고 성능, 리더십 표현은 독립 검증 전까지 Company Claim이다.
- 병목은 고정 명사가 아니라 시점·플랫폼별 상태다.
- HBM ASP와 constrained-resource 기준 공헌가치를 동일시하지 않는다.
- 공개되지 않은 고객별 점유율, 수율, 원가, CAPA 수치를 만들지 않는다.
- Strong Inference는 Auditor와 Human Review를 모두 통과해야 한다.
- 충돌은 자동으로 화해하거나 삭제하지 않고 Contradiction Register에 보존한다.

## 첫 Vertical Slice

SK하이닉스의 공식 12-layer HBM4 sample 발표 한 건을 Source로 사용한다. 하나의 문서를 통째로 사실 처리하지 않고 sample shipment, certification pending, mass-production preparation target, industry-first claim을 별도 Atomic Evidence로 분해한다. 목표는 수요 전망을 확정하는 것이 아니라 qualification·TTM·Demand Forecast·Customer Priority에 대한 조건부 변화와 아직 확인되지 않은 것을 함께 남기는 것이다.
