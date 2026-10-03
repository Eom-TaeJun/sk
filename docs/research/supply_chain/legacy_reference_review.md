# 기존 참고 저장소 검토와 통합 원칙

검토 기준일: 2026-10-03 KST. 이 문서는 사용자가 지정한 세 저장소를 과거 연구의 참고자료로 검토하고, [현재 공급망 연구](README.md)에 이전할 방법론과 재검증할 가정을 기록한다. 최신 시장 사실과 후보 지표의 근거는 현재 연구의 출처 목록을 따른다.

평가는 모델의 세대나 당시 AI 성능에 대한 인상 대신 실제 파일, 연결 경로, 계산 규칙, 검증 장치를 기준으로 했다. 과거의 설계 아이디어와 현재 검증된 결과를 구분한다. Private 저장소의 원코드, 개인정보, 면접 답변, 사적인 커뮤니케이션 및 운영 설정을 공개 저장소로 복사하지 않는다. 여기에는 방법론과 검증 포인트만 남긴다.

## 검토 범위와 고정된 버전

| 참고 저장소 | 공개 범위 | 확인한 기본 브랜치와 커밋 | 기준 커밋 날짜 | 주된 역할 |
| --- | --- | --- | --- | --- |
| `Eom-TaeJun/2nd_skhy` | Private | `main` · [6660e2d773ed354cff35bd2e05475b4de798c86f](https://github.com/Eom-TaeJun/2nd_skhy/commit/6660e2d773ed354cff35bd2e05475b4de798c86f) | 2026-05-06 | 판단 결과를 전달 형태로 바꾸는 downstream 작업공간 |
| `Eom-TaeJun/semi_strategy_harness` | Private | `main` · [bc59854e077dd44588740f818e4f56397f22a7a9](https://github.com/Eom-TaeJun/semi_strategy_harness/commit/bc59854e077dd44588740f818e4f56397f22a7a9) | 2026-05-05 | 지표 수집, 규칙 기반 판단, 사건·개념·이슈 연결 |
| `Eom-TaeJun/aifinance_skhynix` | Public | `main` · [96e34526b74fe2d3d680c75ca38cd7ff527857c0](https://github.com/Eom-TaeJun/aifinance_skhynix/commit/96e34526b74fe2d3d680c75ca38cd7ff527857c0) | 2026-04-22 | 11개 연구 노트와 RAG·wiki 실험을 묶은 제출 패키지 |

아래 GitHub 링크는 모두 위 커밋에 고정되어 있다. Private 링크는 해당 저장소에 접근할 수 있는 사람만 열 수 있으며, 공개 사실의 원출처로 취급하지 않는다. 디렉터리와 관련 파일의 정적 검토를 수행했으며, 개별 프로그램 실행, API 호출 성공, 검색 성능 재현, 예측력 또는 실제 사업 성과를 실증하지 않았다.

## 이전할 공통 원칙

| 유용한 원칙 | 현재 `sk`에서 적용할 방식 | 검증 경계 |
| --- | --- | --- |
| 시장 전체, 개별 제품, 플랫폼, 공급사 몫을 구분 | CAPEX, 주문, 설치, 제품 상용화, 고객 수용, 상업 출하를 별도 관측 대상으로 유지 | CAPEX가 고객별 메모리 매출을 증명하지 않음 |
| 새 사건이 기존 가정을 어떻게 바꾸는지 기록 | 사건 → 이전 가정 → 변화 → 확인 조건 → 반증 조건 → 판단 변수의 변경을 연결 | 변화 후보를 자동으로 FACT나 사업 처방으로 승격하지 않음 |
| 주장마다 근거 경로를 남김 | Evidence ID → Source ID → 원문 발췌 → locator → 날짜 → content hash를 보존 | wiki 요약이나 LLM 문장 자체는 원출처가 아님 |
| 개념, 사건, 판단, 전달을 분리 | 재사용 개념과 날짜가 있는 사건을 구분하고, 공개 근거를 확인한 후 메모로 번역 | 전달 문장이 원래의 caveat와 refute를 지우지 않음 |
| 직렬 공급 제약과 다음 확인 시점을 명시 | 제약별 단위·플랫폼·기간·증거 상태와 후속 공식 자료를 기록 | 그래프 연결이나 시간 순서만으로 인과를 확정하지 않음 |
| 실패·미관측·모의를 드러냄 | API 미실행, fallback, 누락, UNKNOWN, 검증 대기를 출력과 기록에서 분리 | 보기 좋은 출력이나 일부 실데이터가 전체 수집 성공을 의미하지 않음 |

현재 프로젝트의 적용 기준은 [Source Understanding](../../source_understanding.md)과 [AGENTS.md](../../../AGENTS.md)다. 회사의 주장, 외부 추정, sample, qualification, design-in, LTA, mass production, commercial shipment를 구분하고, Strong Inference와 최종 사업 판단의 사람 검토 경계를 유지한다.

## `2nd_skhy`: 판단과 전달의 구분

[README.txt](https://github.com/Eom-TaeJun/2nd_skhy/blob/6660e2d773ed354cff35bd2e05475b4de798c86f/README.txt#L9)는 upstream에서 판단 패키지를 만들고 downstream에서 이를 전달 구조로 바꾸는 역할 계약을 명시한다. `project_result`, `evidence_path`, `trigger`, `refute_condition`, `caveat`, `implication`, `handoff_note`처럼 결론과 조건을 함께 전달하는 필드는 재사용 가치가 있다. 현재 `sk`에서는 판단 변수와 검증 상태를 보존하는 인계 계약으로 참고한다.

다만 이 저장소를 독립적인 시장 수집기나 최신 분석 엔진으로 간주하지 않는다. 다른 저장소에서 가져온 자료는 복사 시점의 스냅샷이다. 지표 사본과 관련 문서에는 48개 registry, 43개 reading 대상, 40개라는 이전 설명이 혼재하므로, 수치만으로 수집 범위나 구현 완성도를 추론하지 않는다. 현재 registry, 실제 collector 대상, 파생 변수, 성공한 관측 수를 각각 확인해야 한다.

[지표 사본](https://github.com/Eom-TaeJun/2nd_skhy/blob/6660e2d773ed354cff35bd2e05475b4de798c86f/source/from_semi/indicators.py#L34)은 금리·환율·신용스프레드를 `revenue`, 주가 수익률을 `shipment`로 기본 분류한다. 이는 출처의 관측 신뢰성과 제품의 상용화 단계를 혼동한다. 공식 금리 관측은 금리 관측이며, 주가는 시장 기대 신호다. 메모리 출하나 고객 매출의 확인으로 승격해서 사용하지 않는다.

공개 통합에는 역할 분리와 조건을 보존하는 인계 원칙만 반영한다. 개인 면접 자료와 답변 문장은 연구 corpus에 포함하지 않는다.

## `semi_strategy_harness`: 사건 갱신과 규칙 기반 판단

[PROJECT_BRIEF.md](https://github.com/Eom-TaeJun/semi_strategy_harness/blob/bc59854e077dd44588740f818e4f56397f22a7a9/PROJECT_BRIEF.md)는 사건·출처에서 전략 판단과 결과 추출로 이어지는 목적을 설명한다. 최상위 README는 없으며, [knowledge/README.md](https://github.com/Eom-TaeJun/semi_strategy_harness/blob/bc59854e077dd44588740f818e4f56397f22a7a9/knowledge/README.md)가 개념·사건·alias·검색·lint 구조의 진입점이다.

| 확인한 구현 | 유용한 부분 | 현재 통합 시 수정하거나 재검증할 부분 |
| --- | --- | --- |
| [지표 registry](https://github.com/Eom-TaeJun/semi_strategy_harness/blob/bc59854e077dd44588740f818e4f56397f22a7a9/registry/indicators.py#L1) | 8개 범주·48개 지표를 한 파일에서 관리하고, 43개 수집 대상과 5개 파생/default 변수를 구분 | 지표 수와 실제 관측 수를 분리. 회사 관점의 고정 호재·악재 점수가 수요 또는 공급의 물리량을 대신하지 않게 함 |
| [수집 진입점](https://github.com/Eom-TaeJun/semi_strategy_harness/blob/bc59854e077dd44588740f818e4f56397f22a7a9/collect/fetch.py#L20) | FRED, yfinance, Claude 검색과 mock fallback을 채널별로 연결 | Perplexity는 구현되어도 기본 경로에 연결되지 않음. 채널 성공·실패·누락·fallback을 따로 기록하고, 일부 실데이터를 전체 성공으로 표현하지 않음 |
| [Claude 판독 parser](https://github.com/Eom-TaeJun/semi_strategy_harness/blob/bc59854e077dd44588740f818e4f56397f22a7a9/collect/channels/claude_collector.py#L349) | 반환 키를 배치 대상과 대조하고 URL을 보관 | 모델이 반환한 URL과 오늘 날짜를 실제 게시·발효·관측 시점으로 대체하지 않음. 기본 evidence stage 부여 전에 원문과 주장의 일치를 확인 |
| [requirements](https://github.com/Eom-TaeJun/semi_strategy_harness/blob/bc59854e077dd44588740f818e4f56397f22a7a9/requirements.txt) | 필수와 선택 채널의 구분 | 실제 import하는 `fredapi`, `anthropic`의 선언이 빠져 있음. 설치 가능성과 API 성공을 문서만으로 인정하지 않음 |
| [출처 registry](https://github.com/Eom-TaeJun/semi_strategy_harness/blob/bc59854e077dd44588740f818e4f56397f22a7a9/knowledge/source_registry.yaml#L1) | `source_id`, `claim_id`, 게시·접근 시점과 주장별 근거 연결 | 현재 `sk`의 원문·locator·hash 및 Evidence trace 계약으로 보강. 과거 등록 URL은 최신 주장 확인 전에 재검증 |
| [사건 영향 메모](https://github.com/Eom-TaeJun/semi_strategy_harness/blob/bc59854e077dd44588740f818e4f56397f22a7a9/knowledge/templates/event_impact_memo_TEMPLATE.yaml) | 이전 가정, 사건 변화, 약한 연결고리, trigger/refute, 영향의 갱신 루프 | 방법론만 새로 구현. 오래된 사건의 수치와 결론을 현재 상태로 이식하지 않음 |
| [lint](https://github.com/Eom-TaeJun/semi_strategy_harness/blob/bc59854e077dd44588740f818e4f56397f22a7a9/knowledge/lint/check.py)·[smoke 검사](https://github.com/Eom-TaeJun/semi_strategy_harness/blob/bc59854e077dd44588740f818e4f56397f22a7a9/knowledge/query/smoke.py#L89) | YAML, 출처 ID, 그래프 연결, 사건과 카드 시점, 검색 routing의 결정적 점검 | 검색 routing 검사와 시장 예측 검증을 구분. 저장소 tree에서 일반적인 `tests/`·pytest 구성은 확인되지 않았으며 이번 검토에서 검사 자체를 실행하지 않음 |

수치 모형에는 다음의 명확한 제한이 있다.

- [CAPEX funnel](https://github.com/Eom-TaeJun/semi_strategy_harness/blob/bc59854e077dd44588740f818e4f56397f22a7a9/analyze/capex_funnel.py#L35)은 고정 기준값과 점수 민감도로 계산한다. 실제 reading의 숫자를 입력값으로 쓰지 않으며, 파생 출하·매출에 `shipment`·`revenue` stage를 고정 부여한다. 이 값들은 검증된 출하·매출 관측이 아니다.
- 패키징 병목 강화에 대한 양의 점수를 [funnel](https://github.com/Eom-TaeJun/semi_strategy_harness/blob/bc59854e077dd44588740f818e4f56397f22a7a9/analyze/capex_funnel.py#L109)은 공급 실현율 증가로, [supply waterfall](https://github.com/Eom-TaeJun/semi_strategy_harness/blob/bc59854e077dd44588740f818e4f56397f22a7a9/analyze/supply_waterfall.py#L105)은 부호를 반전해 공급 감소로 처리한다. [main.py](https://github.com/Eom-TaeJun/semi_strategy_harness/blob/bc59854e077dd44588740f818e4f56397f22a7a9/main.py#L77)에서 두 모형은 별도로 계산된다. 프리미엄에 유리한 점수와 물리 공급량의 증감은 분리해야 한다.
- [근거 단계별 오차 폭](https://github.com/Eom-TaeJun/semi_strategy_harness/blob/bc59854e077dd44588740f818e4f56397f22a7a9/analyze/evidence.py#L25)은 고정 설정이다. 단계별 독립 오차를 가정한 합성까지 포함하여 통계적으로 검증된 신뢰구간으로 사용할 수 없다.
- [검증 캘린더](https://github.com/Eom-TaeJun/semi_strategy_harness/blob/bc59854e077dd44588740f818e4f56397f22a7a9/analyze/verification_calendar.py#L23)는 2026년 4~7월의 예정 일정이다. 현재 후속 IR·정책 자료와 실제 일정을 확인해야 한다.

## `aifinance_skhynix`: 연구 노트와 RAG 실험

[README.md](https://github.com/Eom-TaeJun/aifinance_skhynix/blob/96e34526b74fe2d3d680c75ca38cd7ff527857c0/README.md)는 연구 노트를 사용한 RAG 방법 비교와 wiki 실험의 제출 패키지를 설명한다. 확인한 tree에는 11개 노트가 있으며 README의 문서 수 설명과 차이가 있다. 이 패키지에서 live collector 구현은 확인되지 않았다. 수집 대상의 설계, 저장된 설명, API를 실제로 실행한 관측 결과를 구분해야 한다.

| 고정된 참고 파일 | 이전할 아이디어 | 폐기하거나 재검증할 가정 |
| --- | --- | --- |
| [07 CAPEX→매출](https://github.com/Eom-TaeJun/aifinance_skhynix/blob/96e34526b74fe2d3d680c75ca38cd7ff527857c0/papers/07_hynix_capex_to_revenue_funnel.md) | CAPEX에서 주소 가능한 지출, 공급사 몫, 출하, 매출 인식으로 분해 | 520B, 22%, 52%, 85%, 88%는 현재 입력값이나 검증된 계수로 이전하지 않음. GPU/ASIC package 지출에 공급사 HBM 점유율을 곱하려면 HBM content의 분리와 단위 정합성이 먼저 필요 |
| [08 공급 제약](https://github.com/Eom-TaeJun/aifinance_skhynix/blob/96e34526b74fe2d3d680c75ca38cd7ff527857c0/papers/08_hynix_supply_waterfall.md) | 수율, 패키징, 기판, 고객 수용의 직렬 제약을 별도 관측 | `min` 계산은 같은 기간·플랫폼·출력 단위로 환산된 제약에서만 가능. wafer, package, stack, qualification 비율을 그대로 비교하지 않음 |
| [09 근거 단계](https://github.com/Eom-TaeJun/aifinance_skhynix/blob/96e34526b74fe2d3d680c75ca38cd7ff527857c0/papers/09_hynix_evidence_stage_framework.md) | 발표, 고객 확인, 계약, 출하, 매출을 구분 | 출처 유형과 사건 단계의 단일 서열, 또는 여러 출처 중 최대 단계로 전체 주장을 승격하는 방식은 채택하지 않음. 각 atomic claim의 지원 범위를 따로 확인 |
| [10 공급사 몫](https://github.com/Eom-TaeJun/aifinance_skhynix/blob/96e34526b74fe2d3d680c75ca38cd7ff527857c0/papers/10_hynix_sk_share_attribution.md) | 시장 수요와 개별 공급사의 배정·qualification·실현을 분리 | 비공개 고객별 물량·점유율·가격을 추정치 없이 채우지 않음. 보도된 배정과 공식 고객 수용, 상업 출하는 다른 증거 |
| [11 검증 캘린더](https://github.com/Eom-TaeJun/aifinance_skhynix/blob/96e34526b74fe2d3d680c75ca38cd7ff527857c0/papers/11_hynix_verification_calendar.md) | 다음 공식 자료에서 어떤 주장을 확인할지 사전 지정 | 예정일 자체는 증거가 아니며, 실제 발표 여부와 원문을 확인해야 함 |

실험 결과를 해석할 때도 구현상 한계를 보존한다.

- [고정 지표 상태와 판정 함수](https://github.com/Eom-TaeJun/aifinance_skhynix/blob/96e34526b74fe2d3d680c75ca38cd7ff527857c0/midterm_submission.py#L800)는 당시 상태를 코드에 넣고, 모든 지표가 `substitute`일 때만 SUBSTITUTE를 반환한다. 나머지 입력은 COMPLEMENT가 되므로 미관측·unknown·누락도 보완재로 판정될 수 있다. 새로운 연구에서는 UNKNOWN과 서로 다른 조건부 가설을 보존해야 한다.
- [API 없는 평가 fallback](https://github.com/Eom-TaeJun/aifinance_skhynix/blob/96e34526b74fe2d3d680c75ca38cd7ff527857c0/rag_lab/llm.py#L124)은 정확성·완전성·구체성·종합성에 고정 점수 6/6/5/6을 반환한다. 이 출력은 모델의 답변 품질을 측정한 결과로 사용할 수 없다.
- [wiki 재사용 조건](https://github.com/Eom-TaeJun/aifinance_skhynix/blob/96e34526b74fe2d3d680c75ca38cd7ff527857c0/rag_lab/karpathy_wiki.py#L84)은 index 존재와 페이지 수를 확인한다. 해당 경로에서 원문 content hash를 대조하지 않으므로, 원문 변경 후에도 이전 요약을 재사용할 수 있다. 현재 `sk`에서는 출처 hash, compiler 설정과 생성 시점을 연결해야 한다.

## 현재 통합에서의 개선과 검증 대기

현재 연구는 과거의 메모리 중심 시야를 반도체·AI·데이터센터·전력 공급망으로 넓히되, 계산을 늘리기 전에 관측 대상을 명확히 한다. 전체 CAPEX는 GPU/ASIC, 메모리, 네트워크, 건물, 전력, 냉각 등으로 구분하고, 전력 계통·발전·변압기·배전·냉각의 공급 제약을 독립적인 연구 대상으로 다룬다. 지출 구분만으로 각 항목의 실제 설치나 고객 매출을 확정하지 않는다.

| 과거 방식에서 발견한 제한 | 현재 연구의 적용 기준 |
| --- | --- |
| 수집일을 관측일로 사용 | 게시일, 발효일, 원관측 기간, 수집 시점을 분리 |
| 모델 URL과 요약을 성공한 수집으로 취급 | API 실행 여부, 응답 검증, 원문 접근, locator, hash, 주장 지원을 각각 확인 |
| 근거 유형과 상용화 단계를 하나의 점수로 표현 | 출처 품질·주장 상태·경제적 의미·상용화/고객 수용 단계를 분리 |
| 고정 모형 계수와 비공개 지표를 수치화 | 공개 근거가 없으면 `KNOWN_UNKNOWN` 또는 `TO_VERIFY`로 유지 |
| 병목이나 기술 효율화에 고정 호재·악재 점수 부여 | 플랫폼, 기간, 업무량, 비용, 사용량, 물리 공급 제약에 따라 가설을 구분 |
| wiki나 복사본을 현재 사실로 재사용 | 원문 변경·시간 경과·후속 사건에 따른 재검증과 모순 기록 |

[현재 공급망 연구](README.md)의 32개 후보 지표는 연구용 후보 목록이다. live 수집 성공, 예측 성능, H1 결과 또는 사업 추천으로 승인된 지표가 아니다. 기존에 동결된 H1 24-Track과 자동으로 합치거나 교체하지 않는다. H1 지표 계산, lead/lag, 실현율 및 verdict는 사람의 Gate 6 dataset freeze 전까지 수행하지 않는다. H2/H3와 새로운 판단 엔진의 구현도 이 참고자료 검토로 승인된 것으로 간주하지 않는다.

남은 한계는 각 주장에 대한 최신 원출처 확인, 수집 및 원문 hash 검증, 기간·단위 정합성, 조건부 가설의 실제 평가다. 이번 정적 감사에서 오래된 모형의 예측력과 고객별 매출 귀속을 입증하지 않았다.

현재 연구 자료의 수집 순서와 기존 H1 편입 경계는 [목적별 수집 계획](collection_plan.md)을 따른다. 기존 Gate 6 검토 자료가 준비되어 있어도 사람의 dataset freeze를 대신하지 않는다.
