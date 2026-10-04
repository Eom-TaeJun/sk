# 반도체·AI 공급망 공개 지표 수집 계획

확인 기준일: **2026-10-03**. 대상은 반도체를 중심으로 AI 서비스, 데이터센터, 전력, 장비·소재와 금융의 연결을 관측할 공개 자료다. 이 문서는 **32개 시그널 후보와 1차 14개 수집 후보의 측정·접근 계획**이다. 선행 예측력, 기업의 투자 매력, 인과관계 또는 H1/H2의 결과를 검증한 문서가 아니다.

현재 완료된 범위는 원문 조사, 지표 정의, 일부 무키 파일·미리보기의 접근 시험이다. 이 계획의 신규 계정·토큰은 발급하지 않았고, 연속 수집기도 구현하지 않았다. `documentation_only`는 수집 성공을 의미하지 않는다. 인증 경로와 무료 여부가 미확인인 경로는 `TO_VERIFY`로 유지한다.

이번 진행의 경제적 목적과 첫 실험은 [목적·관측 계약](decision_purpose.md)에 정했다. 첫 질문은 **고객 구매 약정으로부터 공급자의 실제 실현을 공개 자료로 어디까지 연결할 수 있는가**다. 14개 후보를 동시에 구현하기보다, SEC의 2025-09-23 OpenAI–CoreWeave 추가 주문서 관련 공시 한 건을 추적 가능한 수집·검토 후보로 삼는다. 한 사례의 공개 연결 가능성을 확인하며 선행 예측력을 검증하지 않는다. 2025-09 역사 사건의 점검이며, 2026-10-03 현재 두 회사의 전체 약정·돈흐름 현황 조사와 구분한다.

## 1. 경제적 질문과 관측의 경계

돈과 물량이 어디로 움직이는지 보려면 **계약 ≠ 현금 지급 ≠ 설치 ≠ 가동 ≠ 이용**을 각각 관측해야 한다. 한 기업은 고객이면서 공급자일 수 있다. 클라우드 기업은 컴퓨팅 판매자이자 칩·시설·전력 구매자이고, 데이터센터 개발사는 설비 구매자이자 시설 공급자이며, 전력회사는 공급자이자 발전·송전 장비 구매자다. 정부 승인기관과 계통 운영자도 별도 역할로 연결한다.

| 목적 | 먼저 관측할 것 | 연결할 경제 주체·단위 | 수집 후 만들 수 있는 결과와 한계 |
|---|---|---|---|
| 계약 수요 | 고객·공급자·조건·기간·계약 변경, 전력 서비스 약정 | 법인 ↔ 계약 ↔ 프로젝트 | 계획이 법적 약정으로 진행되는 사건표. 계약 총액이나 MW를 당기 현금·현재 사용으로 바꾸지 않는다. |
| 실제 돈의 집행 | 현금 시설투자·차입 수취·직접 공개된 선수금 수취 | 법인 ↔ 현금흐름 기간; 고객·계약은 공개된 경우만 | 예산과 현금의 구분. 전체 법인 CAPEX에서 AI·HBM 또는 개별 시설의 몫을 임의 배분하지 않는다. |
| 공급 준비 | 기명 장비 주문·인도·설치·인수, 공급 제약과 취소 | 공급자 ↔ 제품 ↔ 고객 ↔ 부지 | 수주와 실행의 사건표. 총 수주잔고 전부를 AI 수요로 분류하지 않는다. |
| 시설 준비 | 동일 건물의 공사·운영 상태, IT 용량·칩 배치, 일정 수정 | 시설 소유자·운영자·장비 소유자·최종 사용자 | 같은 시설의 준비 상태 변화. 설치·소유·추정 용량은 GPU 이용률과 다르다. |
| 전력 확보·실현 | 전력 약정, 필요한 송전 사업, 실제 부하, 발전기 상태·발전량 | 고객 ↔ 유틸리티 ↔ 계통 운영자; 발전소·발전기·승인기관 | 수요 계획과 실제 공급의 별도 확인. PPA MW나 발전 접속 대기는 현재 AI 소비량이 아니다. |
| 자원·실물 교역 | 품목·형태·상대국별 금액·수량·순중량, 공급 집중 | 국가 ↔ HS/HTS 품목 ↔ 공정·용도 | 공급 노출과 교역 변화. 국가 무역을 생산량이나 기업 간 납품으로 부르지 않는다. |
| AI 사용·기관 배분 | 모델별 플랫폼 토큰, ETF 종목 수량·발행 주수·NAV | 모델 ↔ 관측 플랫폼; 펀드 ↔ 증권 ↔ 법인 역할 | 서비스 사용과 투자자 배분의 별도 관측. 토큰은 GPU시간이 아니며 ETF 설정은 발행기업의 설비투자금이 아니다. |

현재 지표 후보는 승인된 H1 24-Track registry를 변경하지 않는다. H1의 lead/lag·실현율·결과 판정은 기존 Gate 6 데이터셋 동결 이후의 별도 승인 범위다. H2/H3, 순위, 사업 권고를 이 수집 계획에서 시작하지 않는다.

지표 선택 전에 **경제적 질문 → 관측 단위 → `known_at` → 결과 변수 → 반증·제외 기준**을 적는다. `known_at`은 해당 주장의 공개 시점이며 계약 사건일·측정 기간·수집 시각과 다르다. 날짜만 확인되면 정밀도와 시각 미확인을 보존한다. 결과는 서비스 개시·매출 인식·현금 회수 등 구체적인 사건으로 나누고, 회사 전체 수치를 계약별 결과로 임의 배분하지 않는다. ETF의 투자자 배분과 기업의 발행·차입·고객 현금은 각각 별도 돈의 흐름이다.

## 2. 1차 수집 후보 14개

아래 번호는 카탈로그의 수집 순서 설명이며 **예측력 순위가 아니다**. 먼저 고른 이유는 공개 원문이 있고, 기업·계약·시설 또는 같은 기간의 단위로 연결할 수 있으며, 계획과 실현을 구분하는 데 도움이 되기 때문이다. 접근이 조건부인 후보는 무료·인증 검증을 통과한 뒤 수집한다. 전체 정의·필드는 [지표 카탈로그](../../../data/research/semiconductor_supply_chain/2026-10-03/signal_catalog_v2.json)를 따른다.

| # · 지표 ID | 경제적 목적·측정값 | 수집처·방법 | 연결·주기 | 1차 선정 이유와 해석 한계 |
|---|---|---|---|---|
| 1 · `capital-contract-event-stage` | 투자·구매 계획의 발표, 조건부, 서명, 발효, 지급, 완료를 원문 통화·기간과 함께 기록 | [SEC submissions API](https://www.sec.gov/search-filings/edgar-application-programming-interfaces)로 8-K/6-K/10-Q/10-K·정정 식별 후 원문·exhibit 검토 | 법인 CIK/LEI·상대 법인·계약/프로젝트·accession·사건일. 공시 사건별 | 돈·장비·전력 관계의 시작점을 연결할 수 있다. 중요 계약만 공개되며 전용 계약 API는 없다. 지급·완료는 별도 근거가 필요하다. |
| 2 · `power-p1-binding-load` | 원문이 signed/binding으로 정의한 전력 서비스 약정 MW와 담보 형태 | [AEP Ohio 공개 업데이트](https://www.aepohio.com/company/news/view?releaseID=10753), [tariff 문서](https://www.aepohio.com/company/about/rates/data-center-tariff/)와 제출 문서 검토 | 유틸리티 법인·tariff docket·cohort·관측 기준일. 비정기 사건별 | 비용 없는 관심표명과 법적 약정을 구분한다. 현재 전력 소비·AI 비중·담보 현금 수취액은 알 수 없다. |
| 3 · `power-p4-transmission-service-date` | 필수 송전 사업 ID, 계획·승인·설계·착공·준공·통전, 예상 서비스일의 수정 | [AEP 부하 연구 원문](https://www.aepohio.com/lib/docs/ratesandtariffs/ohio/AEP-Ohio_DCT_Load_Study_Letter_25.11.7.pdf), 계통 운영자·PUC 공개 문서 | 부하 프로젝트/cluster ↔ 송전 사업 ↔ 서비스 조건 ↔ 문서 버전. 사건별 | 약정이 가동으로 이어지는 연결 병목을 확인한다. 예상일은 보장된 가동일이 아니며 고객·부지 비공개 시 연결을 보류한다. |
| 4 · `power-p8-named-equipment-order` | 공개된 고객·부지·제품의 주문/계약/인도/설치/인수; 대수·금액·지원 MW는 원문 범위만 | [GE Vernova 공식 발표](https://www.gevernova.com/news/press-releases), [Vertiv 공식 발표](https://www.vertiv.com/en-us/about/news-and-insights/news-releases/), 기업 IR·공시 | 공급자 법인·고객 법인·제품·시설·계약·사건일. 사건별·분기 공시 | 실제 구매자와 공급자를 잇는다. 설계 협력·제품 출시·총 backlog를 기명 주문과 혼동하지 않는다. |
| 5 · `capital-sec-actual-cash` | 현금 CAPEX·영업 현금흐름·차입 수취액을 각각 기록 | [SEC companyfacts/companyconcept](https://www.sec.gov/search-filings/edgar-application-programming-interfaces)와 현금흐름표 주석 | CIK·taxonomy/tag·통화·start/end·accession. 분기/연간 | 투자 가이던스와 실제 집행을 분리할 수 있다. 영업 현금흐름은 고객 현금 수취액 자체가 아니며 비현금 리스 취득을 현금 CAPEX에 섞지 않는다. |
| 6 · `supply-same-site-operational-conversion` | 동일 시설·건물의 운영 상태, IT MW·칩 종류별 수량과 계획일 수정 | [Epoch AI 문서·CSV 다운로드](https://epoch.ai/data/data-centers-documentation/downloads); 원저자 제공 세 데이터셋의 연결 정의 검토 | 시설·건물·관측일·칩 종류·데이터 버전. 공개 버전마다 보존; 일정한 갱신 주기는 보장되지 않음 | 지도 위치를 시간별 준비 상태와 연결한다. 원문 조사 단계이며 CSV 적재 미실행. 실측/추정과 IT/시설 MW를 보존하고 이용률로 해석하지 않는다. |
| 7 · `power-p2-actual-dc-peak` | 즉시 수집 대상은 연간 Historical July Peak와 vintage별 Load Forecast July Peak MW | [PJM 연간 XLS](https://www.pjm.com/-/media/DotCom/planning/res-adeq/load-forecast/2026-accuracy-report.xlsx), [별도 PDF](https://www.pjm.com/-/media/DotCom/planning/res-adeq/load-forecast/2026-load-forecast-accuracy-report.pdf) | canonical Zone/EDC/LSE·Year·원 Metric·예측 버전·상하위 영역. 연간 공개 자료 | 확인된 실제 부하 범위를 계획과 비교할 수 있다. XLS 23시트는 `Zone/Year/Metric/Load MW`이며 월별 열이 없다. PDF의 DC-filtered 월별 peak/average daily peak는 별도 범위다. XLS를 월별 DC 소비량으로 표시하지 않는다. |
| 8 · `power-p5-supply-realization-eia` | 발전기 계획·상태·운전 월·MW와 발전소 월 순발전 MWh를 별도 저장 | [EIA-860M 공개 XLS](https://www.eia.gov/electricity/data/eia860m/), [EIA-923 공개 ZIP](https://www.eia.gov/electricity/data/eia923/) | 860M은 plant_id·generator_id; 923은 plant_id·prime_mover·fuel·월, generator가 제공되는 경우만 추가. 월간·잠정 수정 | 발전 계획을 실제 공급 확인으로 이어갈 수 있다. 운영 목록의 standby/out-of-service도 구분한다. `DC Net Capacity`는 **direct current**다. 923 내부 최신 월은 아직 미검증이며 발전량을 특정 AI 고객 소비로 배정하지 않는다. |
| 9 · `capital-comtrade-physical-trade` | 같은 HS 분류판·품목·단위의 금액·qty/altQty·순중량과 추정·집계 플래그 | [UN Comtrade](https://uncomtrade.org/docs/un-comtrade-api/); 무키 preview로 schema 확인, 전체 반복 수집은 등록 API 접근 검증 후 | reporter·period·HS edition/cmdCode·flow·partner/partner2·customs·운송수단. 월간/연간·국가별 지연 | 가격과 물량·상대국 변화를 함께 볼 수 있다. HS854231은 GPU 전용, HS854232는 HBM 전용이 아니다. 개수 미제공을 0으로 바꾸지 않는다. |
| 10 · `capital-usitc-material-form-trade` | 미국 HTS10별 수입 금액·수량·단위; 갈륨 금속·undoped/doped GaAs wafer를 분리 | [USITC DataWeb Query API](https://www.usitc.gov/applications/dataweb/api/dataweb_query_api.html); 저장한 공식 query payload 사용 | 수입 기준·월·HTS10 적용 연도·원산국·measure·수량 단위. 월간 | HS6의 소재 바구니를 형태별로 보완한다. 인증 호출 미실행. 서로 다른 화합물·웨이퍼를 contained gallium kg으로 합산하지 않는다. 미국 수입은 세계 공급량이 아니다. |
| 11 · `capital-etf-position-normalized` | 종목 보유수량 q, 비중, 발행 주수 S, ETF 1주당 보유수량 q/S | [공식 액티브 ETF holdings CSV](https://www.ishares.com/us/products/339081/ishares-a-i-innovation-and-tech-active-etf/latest-holdings.csv)의 기준일·preamble·Equity 행 | 펀드/share class·증권 ID·기준일. 일별 snapshot 제안 | 비중 상승의 가격 효과와 보유수량·펀드 규모 변화를 분리한다. 현물 설정·기업행동을 조정해도 실제 운용사 매매대금을 알 수 없다. 단일 펀드를 기관 전체로 일반화하지 않는다. |
| 12 · `capital-etf-netcreation-estimate` | 같은 기준일의 발행 주수 변화 × NAV, split 조정 후 NAV 평가 순설정 추정 | [공식 ETF 페이지](https://www.ishares.com/us/products/339081/ishares-a-i-innovation-and-tech-active-etf)와 holdings의 Shares Outstanding | 펀드/share class·동일 기준일·통화. 일별 | 펀드로의 순설정 압력과 종목 재배분을 구분한다. 전일 S나 같은 날짜 NAV가 없으면 계산하지 않는다. 현금 유입·gross 설정/환매가 아니며 이번 조사에서는 흐름을 계산하지 않았다. |
| 13 · `industry-ai-observed-token-usage` | 플랫폼 내 UTC 일자·모델 variant별 token/request. 동일 필터·완료 구간끼리 비교 | [OpenRouter Datasets](https://openrouter.ai/docs/api/api-reference/datasets/daily-token-totals-for-top-50-models); 공개 rankings는 수동 확인 가능 | model_permaslug·UTC date·modality/context filter·source version·meta.as_of. 일별 완료 bucket | 생산 능력 밖의 실제 사용 방향을 관측할 후보다. **API 무료 여부·권한 `TO_VERIFY`**, 인증 호출 미실행. top50+other와 주간 표본 분류를 구분한다. 토큰은 세계 수요·매출·GPU 이용시간이 아니다. |
| 14 · `supply-schedule-downside-and-data-staleness` | 같은 계획의 지연·보류·축소·명시 취소와 자료 시리즈 중단 | Epoch 버전·공식 회사 변경 발표, [SEMI 중단 안내](https://www.semi.org/en/products-services/market-data/equipment/billings-report), [WRI 갱신 상태](https://github.com/wri/global-power-plant-database) | project/contract/source·vintage·원 예정일·수정일. 사건별 | 발표만 누적되는 가짜 성장과 오래된 지도 시그널을 줄인다. 레코드 소실은 취소가 아니다. SEMI 중단 시리즈와 WRI 역사 자료는 현재 흐름에서 제외한다. |

PJM 자료는 2026-05-29 게시, XLS의 역사 관측은 최대 2025년이다. EIA-860M에서 확인한 파일은 2026-08 자료, 09-24 공개다. EIA-923 페이지의 June 표기와 ZIP의 July 표기가 달라 내부 파일 검사 전 최신 관측월은 미확정이다. **문서를 확인한 날짜를 모든 행의 경제 사건일로 채우지 않는다.**

## 3. 보조 후보 18개를 어디에 붙일 것인가

보조 후보는 1차 자료의 해석·교차검증을 보완한다. 현재 관측되지 않은 내부 값이나 유료 상세 데이터가 공개 API로 대체됐다고 가정하지 않는다.

| 목적 | 카탈로그 ID | 무료 수집 경로·후속 결과 | 제한 |
|---|---|---|---|
| 고객 비용 부담 | `capital-customer-prepayments` | SEC 원문에서 직접 명시한 기간 현금 수취, 예치금 잔액, RPO·약정을 별도 수집 | 부채 잔액 증가는 현금 수취와 다르다. 익명 고객은 기명 기업 edge로 만들지 않는다. |
| 전력 신청의 강도 | `power-p6-paid-load-study` | AEP 요청 MW·연구비 납부 MW·site count를 원 cohort·기준일별로 기록 | 연구 신청은 계약·가동이 아니다. 프로젝트 매칭 없이 단계 aggregate의 전환율을 계산하지 않는다. |
| 접속·부하 계획 | `power-p3-energization-stage`, `power-p7-forecast-vintage`, `power-p9-grid-baseload-proxy` | [ERCOT large load 공개 문서](https://www.ercot.com/services/rq/large-load-integration), PJM 예측 버전, [SPP actual load](https://portal.spp.org/pages/stlf-vs-actual)·[GridStatus 공개 코드](https://github.com/gridstatus/gridstatus/blob/main/gridstatus/spp.py) | 승인·통전·운영·비동시 peak를 분리. 예측과 실제 계통 부하 잔차는 DC/AI 직접 부하가 아니다. 공개 코드는 API 실행·커버리지 검증과 다르다. |
| 공급 후보·계약 변경 | `power-p10-generation-queue`, `supply-new-power-generation-realization`, `supply-power-contract-revision-termination` | [LBNL 발전 접속 대기](https://emp.lbl.gov/queues), EIA 또는 [PUDL](https://github.com/catalyst-cooperative/pudl)의 발전·EQR 문서 | generation queue는 DC load queue가 아니다. PUDL EQR은 WIP·중복·자연키 문제를 검토해야 하며 거래요금은 현금 입금이 아니다. 무료 기본 경로는 익명 S3/공개 파일로 제한하고 requester-pays 경로를 섞지 않는다. |
| 칩 공급과 설치 | `supply-chip-supply-versus-deployment` | [Epoch ai-chip-counts](https://github.com/epoch-research/ai-chip-counts)와 같은 분기말 시설·소유 snapshot의 정의 검토 | 공급·소유 추정 모델의 공통 입력을 독립 검증으로 계산하지 않는다. GPU die·superchip·rack·H100e를 구분한다. |
| 구조적 자원 노출 | `capital-usgs-structural-resource-risk`, `supply-component-country-concentration` | [USGS MCS 2026](https://www.usgs.gov/publications/mineral-commodity-summaries-2026), Comtrade/HTS와 [OECD 공정·품목 분류](https://doi.org/10.1787/4154cdbf-en) | 연례 자원 지도는 현재 주문·재고가 아니다. 갈륨은 GaAs/GaN 응용, 희토류는 자석·연마·광학 등의 공정·용도에 연결한다. 모든 GPU의 직접 핵심 투입물로 일반화하지 않는다. |
| 항로 차질 | `capital-portwatch-seaborne-disruption` | [IMF PortWatch 공개 FeatureServer](https://services9.arcgis.com/weJ1QsnbMYJlCHdG/arcgis/rest/services/Daily_Ports_Data/FeatureServer/0)의 항만·일별 AIS 추정 | 상품 HS·기업·순도를 알 수 없고 칩의 항공 이동은 빠진다. 기명 시설·공급사 노출은 별도 증거가 필요하다. |
| 산업 실행 확인 | `industry-us-semi-production-utilization`, `industry-us-electrical-backlog`, `industry-japan-equipment-billings` | [FRED IPG3344S](https://fred.stlouisfed.org/series/IPG3344S)·CAPUTLG3344S, [A35SUO](https://fred.stlouisfed.org/series/A35SUO), [Census M3 공개 파일](https://www.census.gov/manufacturing/m3/data/index.html), [SEAJ 월간 공개 요약](https://www.seaj.or.jp/english/statistics/index.html) | 광범위 산업지수·금액이다. AI 칩·변압기 대수를 분리하지 못한다. billings는 bookings가 아니며 SEAJ 무료 열람은 재배포 허가와 다르다. 현행 Census 반도체 단독 M3 계열이나 무료 SEMI Book-to-Bill API를 가정하지 않는다. |
| 사용 비용·효율 | `industry-ai-session-spend`, `industry-ai-efficiency-control` | OpenRouter session Datasets는 무료 여부 확인 후, [Artificial Analysis 공식 API](https://artificialanalysis.ai/api-reference/)는 모델 성능·게시가격·속도 통제 후보 | median session spend × 다른 모집단의 session 수로 시장 매출을 만들지 않는다. 벤치마크와 게시가격은 실제 수요가 아니다. |
| 기관 보유 확인 | `capital-nport-holdings-validation` | [SEC N-PORT 공개 파일](https://www.sec.gov/data-research/sec-markets-data/form-n-port-data-sets)·개별 공시를 운용사 CSV와 대조 | 공개 지연·분기 bulk와 월말 보고를 구분. BALANCE의 단위는 주수·원금 등 다양하며 HOLDING_ID는 제출 간 영속 증권 ID가 아니다. |

## 4. 공적 API·파일 접근 계획

공식 발급 절차와 데이터 이용 조건만 기록한다. 추가 접근의 상세 원문·미검증 상태는 [API 발급 계획](../../../data/research/semiconductor_supply_chain/2026-10-03/api_issuance_plan_v3.json)을 따른다. 아래 제한은 2026-10-03 조사 기준이며 실제 수집 전 공식 정책을 재확인한다.

| 수집처 | 공적 endpoint·발급 방법 | 무료 범위·미검증 조건 |
|---|---|---|
| UN Comtrade | [계정·API portal](https://comtradeplus.un.org/MyComtrade/APIPortal)에서 가입 후 API key 생성. preview는 `https://comtradeapi.un.org/public/v1/preview/C/M/HS`, 등록 data 경로는 공식 문서 기준 | 무키 preview는 500행·단일 기간·단일 상품. 무료 등록 tier는 100,000행/호출, 500회/일, 초당 1회; bulk/async 제외. preview 소량 응답 확인과 인증 전체 수집 검증은 별개다. |
| 한국 관세청 HS×국가 | [공공데이터포털 서비스 활용신청](https://www.data.go.kr/data/15100475/openapi.do) → 서비스키. `https://apis.data.go.kr/1220000/nitemtrade/getNitemtradeList` | 무료; 개발 자동승인·운영 심의승인. 개발 트래픽 10,000 표기는 시간 단위 미확인. 월별·전월까지 매월 15일경 현행화, 최대 1년 조회. 인증 호출 `TO_VERIFY`. 순중량은 칩 개수가 아니다. 10일·20일 보도자료는 별도 집계다. |
| USITC DataWeb | [무료 계정/Login.gov](https://www.usitc.gov/dataweb_login_process) 연결 후 DataWeb의 API → Generate Token. `https://datawebws.usitc.gov/dataweb/api/v2/report2/runReport` | Bearer token 필요, 6개월 유효·자동 갱신 없음. 수치형 호출·행수 한도 미확인. 공식 문서 검색 본문 검토와 실제 인증 호출을 구분하고 payload·현행 HTS 단위를 `TO_VERIFY`로 둔다. |
| ENTSO-E: 유럽 확대 시 | [Transparency Platform](https://transparency.entsoe.eu/) 가입·인증 → 공식 지원 창구의 RESTful API access 절차 → 승인 후 My Account에서 security token 생성. `https://web-api.tp.entsoe.eu/api` | 공개 무료 접근, 공식 안내상 승인 확인 3영업일·토큰당 400회/분. [토큰 절차](https://transparencyplatform.zendesk.com/hc/en-us/articles/12845911031188-How-to-get-security-token), [rate limit](https://transparencyplatform.zendesk.com/hc/en-us/articles/12783148966036-API-Rate-Limit-Part-1). 실제 인증 호출 `TO_VERIFY`. 국가·항목별 재사용 조건 확인; 개별 AI DC 소비는 없음. |
| SEC·기업 IR | `https://data.sec.gov/submissions/CIK{10-digit-cik}.json`, `https://data.sec.gov/api/xbrl/companyfacts/CIK{10-digit-cik}.json`와 accession 원문 | 무키, 식별 User-Agent·전체 합산 초당 10회 이하. 계약·프로젝트별 원문 구조화는 따로 필요하며 companyfacts는 전체 법인·표준 태그 중심. 이번 연구에서 SEC API 실행은 미확인. |
| EIA·Epoch·ETF 공개 파일 | EIA-860M/923 다운로드 페이지, Epoch Downloads, 운용사 공식 holdings CSV/NAV 페이지 | 계정·키 없는 경로로 시작 가능. EIA-860M과 ETF 일부 CSV 접근은 확인했지만 EIA-923 내부 파일·Epoch CSV 적재는 미실행. 각 자료의 기준일·개정·라이선스·과거 파일 보존 가능성 확인. |
| WSTS 총 billings 공개 파일 | [Historical Billings](https://www.wsts.org/67/Historical-Billings-Report)의 Excel/PDF. [2026-10-04 거시 조사 영수증](../../../data/research/semiconductor_macro_structure/2026-10-04/sources.json) | 로그인·키 없는 지역별 전체 반도체 월간/3MMA 경로를 확인했다. 제품별 상세 월자료 구독과 별개이며 DRAM/NAND 비트·ASP가 아니다. 파일 접근·스키마·제한된 기준값만 확인했으며 반복 시계열 적재는 미실행. |
| Eurostat | `https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/{datasetCode}`. [공식 API 안내](https://ec.europa.eu/eurostat/web/user-guides/data-browser/api-data-access/api-introduction) | 가입·키 없는 무료 API. `nrg_cb_em`/`nrg_cb_pem` 월간 전력, `nrg_cb_e` 연간 후보. 이번 GET 응답 미검증, 과거 버전은 직접 보존. 국가 통계로 DC 사용량을 분리하지 않는다. |
| Artificial Analysis | [공식 API 안내](https://artificialanalysis.ai/api-reference/)에 따라 Insights Platform 가입 후 키. `https://artificialanalysis.ai/api/v2/data/llms/models` | 무료 1,000회/일·출처 표시 조건. `x-api-key` 인증 호출 `TO_VERIFY`. 실제 수요 대신 성능·가격·속도 비교용이다. |
| OpenRouter Datasets | `https://openrouter.ai/api/v1/datasets/rankings-daily`; 공식 API key·Bearer 인증 | **무료 API 접근 여부 `TO_VERIFY`**. 문서의 30회/분/키·500회/일/계정 제한을 무료 요금 보장으로 해석하지 않는다. 확인 전 자동 요청하지 않고 공개 rankings의 수동 관측을 별도로 표시한다. |
| Census: 선택적 확대 | [무료 API key 신청](https://api.census.gov/data/key_signup.html), 필요한 dataset·변수 확정 후 사용 | 현재 문서상 데이터 조회는 키 필요, 메타데이터는 무키 가능. 시작은 M3 공개 Excel/PDF도 가능하다. 특정 데이터 인증 응답과 범위는 `TO_VERIFY`. |

무료 열람, 무료 API 접근, 재배포 권리는 별도 조건이다. 기관 리포트가 사용한 Omdia·SEMI 등의 입력을 모두 무료 자료로 간주하지 않는다. 원문·라이선스·출처 표시를 기록하고 공개 배포 범위를 확인한다.

## 5. 기업·시설·계약·지표의 연결 계약

[지도 데이터](../../../data/research/semiconductor_supply_chain/2026-10-03/supply_chain_map_v3.json)에는 원문으로 확인된 관계와 산업·제품 역할을 분리한다. 실제 고객·공급 계약은 기명 근거가 있을 때만 연결한다. [Evidence schema](../../../data/research/semiconductor_supply_chain/2026-10-03/evidence_schema_v2.json)와 저장소의 Source → Evidence → Graph → Memo 추적 규칙을 함께 적용한다.

| 객체 | 필요한 연결 키·필드 | 지켜야 할 경계 |
|---|---|---|
| 법인·증권 | legal entity ID, CIK/LEI, 상장 모회사, 유효기간; 증권은 ISIN/CUSIP 또는 ticker+exchange+asset class+currency | 모회사·계약 자회사·운영 브랜드를 자동으로 같은 주체로 만들지 않는다. ETF 보유증권은 계약 법인과 별도 매핑한다. |
| 시설·발전기 | facility/building ID, 국가·지역, 좌표 출처, owner/operator/hardware owner/end user; EIA plant_id·generator_id | 본사 국가와 생산·시설 국가를 구분한다. 발전소 좌표를 인접 DC 좌표로 복사하지 않는다. 기존 발전소와 신규 발전기를 같은 상태로 합치지 않는다. |
| 관계·계약 | buyer/supplier/owner/operator/grid operator/approver, contract/project ID, 계약 유형·범위·조건, source accession/URL/locator | 산업상 사용 가능성이나 파트너십은 실제 구매 계약과 다르다. PJM 같은 계통 운영자와 FERC/PUC/NRC 같은 승인기관의 역할을 구분한다. |
| 관측값 | metric ID·단위·currency·capacity basis·population/cohort·measurement period·estimated/suppressed/missing flag | MW는 IT/시설/계약/명판/순용량/peak 정의가 다르다. MW와 MWh, 칩·rack·H100e, 현금·약정·잔액을 섞지 않는다. |
| 사건·버전 | event_date, publication/filing date, retrieved_at, observed_asof, target_date, source version·hash, supersedes | 발표일·사건일·목표일·확인일을 각각 저장. 역사 시점에 공개되지 않았던 정보를 과거 시그널에 넣지 않는다. 변경·취소·상충은 덮어쓰지 않는다. |
| 국가 교역 | reporter/partner·flow·period·HS/HTS edition·code·수량 단위·customs/mot·집계/추정 flag | 숫자형 품목·티커의 앞자리 0을 보존. 재수출·가공무역·반복 국경 이동을 중복 생산량으로 합산하지 않는다. |

실제 연결 예시는 다음처럼 좁게 유지한다.

- **Microsoft ↔ Constellation / Crane**: PPA 체결, 발전소 복원, NRC 환경검토·면허 심사, EIA 운영 상태는 별도 사건이다. 835MW 복원 계획을 Microsoft의 현재 AI 소비로 넣지 않는다.
- **AWS ↔ Talen / Susquehanna**: 기존 계약과 개정 계약의 유효 시점을 나누고, Talen의 발전·판매, PPL의 전달, PJM의 계통 역할을 분리한다. 최종 계약 1,920MW와 발전기의 운영 상태는 별도 값이다.
- **Laidley LLC / Evest LLC ↔ Entergy Louisiana / Hyperion**: 초기 시설과 인접 확대 계약의 고객 법인을 구분한다. LPSC의 발전·송전 자원 인증 범위를 ESA 계약 자체 승인으로 확대하지 않는다. Meta의 compute 계획과 발전 자원 신청 MW를 현재 소비로 합산하지 않는다.
- **AEP Ohio cohort**: 5,642MW 신규 약정과 12,219MW 기존 약정은 각각 2026-02-12 기준 집계다. 연구 신청 13,022.7MW와 프로젝트별 동일 cohort·정의가 확인되기 전 전환율을 만들지 않는다. 익명 cohort에 임의 빅테크 고객을 배정하지 않는다.

## 6. 관측 주기·수정·결측 관리

일별 ETF·플랫폼 사용은 제공자가 표시한 기준일을 보존한다. 월별 EIA·무역은 관측월과 공표일을 따로 저장하고, 국가별 지연·잠정치·단위 수정·분류판 변경을 기록한다. 계약·허가·장비 인수는 사건별 자료이므로 공시가 없는 날을 수요 0으로 만들지 않는다.

모든 수집 영수증에는 원 URL, 원문 hash·locator, 제공자 기준일, 확인 시각, 응답/파일 상태, 사용한 필터·단위, 포함 범위와 누락을 남긴다. `missing`, 비공개·억제값, API 오류·한도, 수정값과 진짜 0은 각각 구분한다. 같은 공동 발표를 재인용한 여러 자료는 독립 증거로 세지 않는다.

공급망의 edge 수나 그래프 중심성은 경제적 의존도·인과효과가 아니다. IEA·LBNL·EPRI의 연례 전망, Uptime 설문, OECD/CSET의 구조 지도는 정의·분류와 누락을 보완하는 참고층으로 둔다. 보고서 모델의 전력 전망을 유틸리티 약정·현재 계측 부하와 합산하지 않는다. 근거와 기관별 차이는 [합본 소스 벤치마크](../../../data/research/semiconductor_supply_chain/2026-10-03/source_benchmark_v2.json)에 보존한다.

## 7. 수집 뒤 남길 결과

실행 순서는 [수집 로드맵](../../../data/research/semiconductor_supply_chain/2026-10-03/collection_roadmap_v2.json)을 따른다. 첫 결과는 예측 verdict가 아니라 **원문 snapshot·접근 영수증·연결 가능 범위**다.

1. **원문 보존**: 제출·파일·CSV 버전과 해시, 관측 기간·공표 시점·라이선스를 고정한다.
2. **정의 확인**: 원문 단위·집계 범위와 실제 응답 필드를 점검하고 문서상 정의와 응답 차이를 기록한다.
3. **연결 확인**: 회사·시설·계약·공정의 근거가 있는 연결만 작성하고 나머지는 `KNOWN_UNKNOWN` 또는 `TO_VERIFY`로 남긴다.
4. **변경 사건 보존**: 일정 수정·조건 변경·취소·가동·출하·현금 확인을 같은 대상의 이력에 추가한다. 사라진 행은 자동 취소하지 않는다.
5. **후속 검증 설계**: 결과 변수를 유료 구매·인도·설비 인수·실제 부하·현금 집행 중 구체적으로 정의한 다음, 자료 범위와 별도 승인 조건을 확인한다. 임의 선행 개월·임계값·전환율을 정하지 않는다.

첫 구현은 `capital-contract-event-stage`의 단일 사례다. [수집기](../../../scripts/collect_customer_commitment.py)와 [사례 결과](first_case_review.md)는 원문·접근 상태·hash·locator·날짜·조건을 보존한다. 결과 위치는 `data/research/customer_commitments/coreweave_openai_20250923/`다. SEC 직접 요청은 403으로 기록하고, 공식 회사 IR의 공개·무키 feed와 회사 제공 원문은 별도 issuer 경로로 수집한다. 실제 URL·source role과 SEC 원출처 참조를 구분하며 SEC 바이트 동일성은 주장하지 않는다. 다른 지표와 연속 수집은 아직 이 구현의 범위 밖이다.

**단일 약정 실험의 후속 후보:** 같은 주문서와 직접 연결되는 후속 공시 한 건에서 서비스 개시 또는 실제 현금 수취의 공개 여부를 확인한다. 현재 학습 우선순위는 [거시 구조 기준판](semiconductor_macro_structure.md)과 [메모리 수급 지표 계획](memory_cycle_signal_plan.md)에 따른다. 연구·수집 자료의 `main` 병합은 H1/Gate 6·Evidence 승인이나 선행성 판정이 아니다.
