# 반도체 공급망 학습 자료 안내

하이닉스의 상품·고객·채택·공급을 중심으로 반도체와 AI·데이터센터·전력·소재·금융·정책·항공우주의 관계를 읽는다. 자료는 **연구 후보**다. 산업 연결의 구조, 공개 관측과 검증된 결과를 구분한다.

## 현재 기준

| 문서 | 담당하는 내용 |
| --- | --- |
| [직무와 상품·고객 관점](sk_hynix_commercial_role_context.md) | 학습 목적, 공식 직무 근거와 상품별 질문 |
| [수요 근거·투자 경로·위험 시나리오](structural_market_scenarios.md) | 공개 기술/상업 성과·기관 타겟·돈/ETF·조건부 위협과 준비 |
| [지표 수집 목적](indicator_collection_purpose.md) | 질문·관계·후속 행동, 수집 실행 범위와 다음 작업 |
| [무료 API 접근 결과](api_signal_feasibility.md) | dataset·필드·단위·접근 결과·권리와 측정 공백 |

현재 수집 판단과 다음 연구 작업은 **지표 수집 목적**을 따른다. 내부 자료 전용 항목은 ACTIVE에서 제외하고 공개 근거로 구조·가정·준비 선택지를 설명한다. 날짜별 API JSON·옛 로드맵의 후속 제안은 당시 기록이다. DDR5 카드와 이전 Comtrade/Eurostat 호출 파일럿은 보류하며 KOSIS도 구체 비교 질문이 있을 때 수행한다.

## 질문에 따라 읽을 자료

| 확인할 질문 | 자료 |
| --- | --- |
| 제품·사업모델·공정·시장·지역과 실제 기업 역할 | [반도체 거시 구조](semiconductor_macro_structure.md) |
| 메모리 수요·공급·재고를 어떻게 관측할 것인가 | [메모리 사이클 측정 계획](memory_cycle_signal_plan.md), [2026Q2 관측 사례](memory_observation_panel_2026q2.md) |
| AI 업무·소프트웨어 조건이 HBM·호스트 DRAM·SSD에 주는 요구 | [AI 기술과 메모리 상품](ai_technology_memory_links.md) |
| 공유 KV 캐시의 요구·상업 단계와 실제 ETF 보유가 어디서 일치하거나 다른가 | [CMX와 투자 대상의 대조](cmx_memory_investment_signals.md), 2026-10-08 |
| 제품·제조 기능에서 전력·정책·통신·항공우주로 전파되는 조건 | [산업 전파 경로](semiconductor_industry_transmission_routes.md) |
| 기명 플랫폼의 사양·채택 단계를 어떻게 구분하는가 | [HBM3E × NVIDIA GB300 사례](customer_product_cards/hbm_nvidia_gb300.md) |
| 고객 약정과 실제 자금·시설 집행은 어디까지 연결되는가 | [단일 사건의 측정 설계](decision_purpose.md), [OpenAI–CoreWeave 사례](first_case_review.md) |
| 이전 저장소에서 무엇을 참고했는가 | [세 저장소 검토](legacy_reference_review.md) |
| 발산·수렴·수정이 목적에 맞았는가 | [독립 목적 검토](research_convergence_review.md) |

전력·소재·금융 등의 모든 수치를 기본 패널로 운영하지 않는다. 같은 상품·법인·사업·시설·관할 연결 또는 구체 비교 질문을 정한 뒤 필요한 자료를 선택한다. 계약/명판/실측 전력, 약정/인출/지급, ETF 증권 배분/기업 자금 수취는 각각 다른 관측이다.

## 날짜별 원자료와 과거 수집 계획

| 자료 묶음 | 원자료와 추적 정보 |
| --- | --- |
| 2026-10-03 공급망 초안 | [지도](../../../data/research/semiconductor_supply_chain/2026-10-03/supply_chain_map_v3.json), [manifest](../../../data/research/semiconductor_supply_chain/2026-10-03/manifest.json), [좌표](../../../data/research/semiconductor_supply_chain/2026-10-03/verified_facilities.geojson) |
| 당시 후보·우선순위·수집 제안 | [32개 후보](../../../data/research/semiconductor_supply_chain/2026-10-03/signal_catalog_v2.json), [14개 로드맵](../../../data/research/semiconductor_supply_chain/2026-10-03/collection_roadmap_v2.json), [수집 계획](collection_plan.md), [API 계획](../../../data/research/semiconductor_supply_chain/2026-10-03/api_issuance_plan_v3.json) |
| 당시 스키마·출처 검토 | [수집 스키마 제안](../../../data/research/semiconductor_supply_chain/2026-10-03/evidence_schema_v2.json), [출처 검토](../../../data/research/semiconductor_supply_chain/2026-10-03/source_benchmark_v2.json) |
| 2026-10-04 거시 관측 근거 | [출처 영수증](../../../data/research/semiconductor_macro_structure/2026-10-04/sources.json), [manifest](../../../data/research/semiconductor_macro_structure/2026-10-04/manifest.json) |
| 2026-10-05 API 접근과 목적 등록 | [API index](../../../data/research/api_signal_feasibility/2026-10-05/collection_index.json), [목적 등록표](../../../data/research/indicator_purpose_review/2026-10-05/purpose_registry.json) |

2026-10-03 지도 스냅샷은 69개 주체·58개 관계·7개 시설·공식 좌표 2곳이다. 관계 17개는 당시 출처를 확인·갱신했고 41개는 이전 조사에서 이월했다. `current_turn_reviewed`는 이 구분이며 사람 승인이나 전체 최신성 보증이 아니다. 공식 좌표는 발전소 2곳만이며 고객 DC의 위치로 대체하지 않는다. 이후 날짜별 자료를 합산해 세계 전체 커버리지로 부르지 않는다.

Crane의 원 발전기 상태 `(OS) Out of service`와 Susquehanna의 `(OP) Operating`은 그대로 보존한다. 모회사·차입법인·보증인·주선 은행은 별도 주체이고, 같은 두 회사의 구매와 지분투자도 별도 관계다. 제안 스키마의 `stage_raw`와 미정규화 상태는 정식 [Atomic Evidence](../../../02_SCHEMAS/atomic_evidence.schema.json)·[Graph](../../../02_SCHEMAS/graph_edge.schema.json) 계약을 대체하지 않는다.

## 검증과 보존

검증 명령과 승인 경계는 [AGENTS.md](../../../AGENTS.md)를 따른다. 원자료·날짜별 JSON/manifest의 바이트와 공개판 변환 이력은 유지하며 `.gitattributes`에서 지정한 원문 줄바꿈을 바꾸지 않는다. 원출처·발췌·locator·공개 시점·hash와 해당 사람 검토 없이 연구 후보를 정식 Evidence나 H1에 자동 편입하지 않는다.

[단일 고객 약정 수집기](../../../scripts/collect_customer_commitment.py)의 [후보 기록](../../../data/research/customer_commitments/coreweave_openai_20250923/record.json)·[수집 이력](../../../data/research/customer_commitments/coreweave_openai_20250923/acquisition.json)은 한 사건의 capture/replay다. 읽기 전용 재검사는 `python scripts/collect_customer_commitment.py --verify-only`다. SEC 직접 요청의 403과 회사 IR mirror의 성공은 구분하며 mirror를 SEC-original bytes로 표시하지 않는다.

과거 구현·H1 계약·미래 실행 설계는 [참조 안내](../../reference_index.md), 코드 오류 수정과 회귀 검증은 [2026-10-06 정비 기록](../../exec-plans/completed/verification_cleanup_20261006.md)에 둔다. 문서·저장소 통합은 사람의 Gate 6 승인·선행성·사업 성과를 뜻하지 않는다. 공개판에 키·개인정보·Private 원코드·로컬 운영 경로를 복사하지 않는다.
