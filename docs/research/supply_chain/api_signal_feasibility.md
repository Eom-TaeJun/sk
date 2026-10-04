# 공급망 지표: 무엇을 왜 API로 수집할 수 있는가

기준일 **2026-10-05**, 상태 **연구 후보**. 사용자가 고객·상품 카드 수렴을 보류하고 API 수집 가능성과 지표 탐색을 먼저 요청했다. 이 문서가 현재 수집 단계의 안내다. 앞선 날짜의 지도·API 발급 계획·검토 기록은 역사 자료로 보존한다.

**무키 데이터 API 10개 source family에서 11개 비어 있지 않은 응답을 확인했다.** ECOS 공개 sample도 포함한 숫자이며 일반 키 인증·전체 역사·반복 수집 성공을 뜻하지 않는다. 별도로 API metadata 2건, ETF CSV와 USGS PDF 파일 3건을 받았다. SEC 403, OpenRouter 401, 오래된 OECD 코드 404, FRED CSV의 시간 초과·접속 종료도 남겼다. 22개 source family에는 인증 미시험 API와 파일·원문 자료도 포함되므로 ‘22개 API가 준비됐다’고 해석하지 않는다.

이번 산출물은 질문 → 지표 → 정확한 경로·필드 → 접근 결과 → 단위·기간 → 연결 조건의 수집 계약이다. 회사 총액·국가 산업·플랫폼 사용을 하이닉스의 고객별 주문량으로 환산하거나 선행 기간·예측력을 계산하지 않았다.

집계의 metadata 2건은 OECD DSD와 ECOS 항목목록 같은 **구조·코드 조회**다. HF 모델 다운로드 snapshot과 GitHub 릴리스도 일반적으로 metadata라고 부르지만, 여기서는 각각 기술 관심·버전 사건의 유효 관측 응답으로 집계했다. 실제 AI 추론·메모리 구매를 확인한 응답이라는 뜻은 아니다.

## 수집할 질문과 관측 위치

| 경제적 질문 | 먼저 볼 지표 | API가 줄 수 있는 것 | 후속 확인이 필요한 것 |
| --- | --- | --- | --- |
| AI 사용이 무엇으로 이동하는가 | 모델별 토큰, 공개 모델 배포·다운로드, 추론 소프트웨어 버전 | 플랫폼·모델·날짜별 사용 후보 또는 개발·배포 관심 | workload·context·backend·메모리 요구, 유료 사용·실제 고객 채택. 다운로드는 추론량이 아님 |
| 고객이 투자 계획을 실행했는가 | 현금 시설투자, 공시·계약 사건, 정부 거래별 의무액·지급 보고 | 법인 회계 기간의 현금 취득, 문서 사건, award·transaction | 동일 시설·장비·공급자의 연결, 리스·선급·누적/분기 구분. 정부 약정과 실제 지급은 별개 |
| 공급이 실제로 움직이는가 | 생산·출하·재고 지수, 가동률, 국가별 메모리 IC 교역, 대만 월매출 | 산업 실행·국경 이동·회사 신고매출의 서로 다른 관측 | 비트 출하·ASP·제품 믹스·SKU·공장 배정. 무역이나 매출은 생산량 자체가 아님 |
| 설치·가동이 전력 제약을 받는가 | 발전기 상태·MW, 발전량 MWh, 실제 권역 부하, 접속 단계 | 발전·계통·지역 운영의 상태와 측정 | 같은 DC의 계약·수전·미터·실제 부하. 권역 부하에는 다른 산업과 날씨가 섞임 |
| 정책·협정이 일정에 영향을 주는가 | 규칙·정정·docket·의견 기한·개별 승인 단계 | 문서 ID·관할·공표·절차 사건 | 상세 원문·시행일·품목/end-use·예외·후속 허가. 검색 결과나 MOU는 가동 승인 아님 |
| 소재 조달 위험은 어디에 있는가 | 갈륨·희토류 국가별 생산·수입 의존·교역 | 연간 소재 구조와 품목별 국가 이동 | 순도·형태·등급·공정 적용·직접 공급사·대체 가능성. 원소명이 같아도 메모리/RF/전력 조달은 다름 |
| 투자자가 어느 테마로 배분하는가 | 액티브 ETF 수량·비중·발행좌수 | 운용사 시점별 보유 구성 | 가격 효과·설정/환매·리밸런싱·기업 직접 조달 구분. 증권 매수가 기업 CAPEX 지급은 아님 |

이 표의 ‘먼저’는 수집 목적의 순서다. 지표가 결과에 선행한다는 실증 순위가 아니다. 사용·관심·예산·약정·인출·현금 지급·설치·가동을 별도 열로 유지해야 돈과 실행의 차이를 볼 수 있다.

## 지금 접근한 API와 파일

아래 결과는 이번 환경에서 제한 조회한 실제 응답이다. 작은 응답의 성공을 모든 국가·품목·기간·계정 권한으로 확대하지 않는다. 세부 URL·요청 범위·응답 schema·receipt는 [통합 인덱스](../../../data/research/api_signal_feasibility/2026-10-05/collection_index.json)와 각 packet에서 확인한다.

| source family / 수집 대상 | 정확한 dataset·series 또는 경로 | 실제 결과 | 무료·키·공개 사용 조건 |
| --- | --- | --- | --- |
| UN Comtrade / 메모리 IC 국가 교역 | `public/v1/preview/C/M/HS`; reporter `410`, HS `854232`, flow `X`, period `202501` | 200·조건에 맞는 1행. 반환 분류 `H6`의 판 대응은 추가 확인 | preview 무키. 무료 등록 basic은 키 필요; preview 500행/1기간/1품목, 등록 100,000행/호출·500회/일·1회/초. 원자료 재배포 조건 별도 |
| Eurostat / 전자부품 생산지수 | `sts_inpr_m`: `M/I21/C261/SCA/DE/2025-01` | JSON-stat 200·1관측 | 무료 무키. 고정 수치 quota 미확인. Comext/Prodcom은 별도 base와 DSD가 필요하며 미호출 |
| OECD TiVA / 수출의 해외 부가가치 | `DSD_TIVA_MAINSH@DF_MAINSH,1.1`; `EXGR_FVA.KOR.C26.W.PT_EXGR.A`, 2020 | DSD metadata 200, 수정 코드의 SDMX CSV 200·1행. 구 코드 404 보존 | 무료 무키; 공식 안내 60 data downloads/hour. 연간 구조 자료이며 현재 월간 수급 신호 아님 |
| KOSIS / 한국 생산·출하·재고 후보 | `statisticsParameterData.do`; `orgId/tblId/itmId/objL*` | 공식 API 확인·미호출. 반도체 exact 표·item·단위 미확정 | 무상 제공 원칙, 회원·API 신청/키 필요. 현재 정량 quota 미확인 |
| 관세청 / 한국 품목×국가 수출입 | `1220000/nitemtrade/getNitemtradeList`; `strtYymm/endYymm/cntyCd/hsSgn` | 공식 dataset·필드 확인·미호출 | 무료, 공공데이터포털 활용 신청/키. 1회 최대 12개월; 개발 트래픽 10,000의 기간 단위 미확정 |
| USGS / 갈륨·희토류 구조 | MCS 2026 gallium·rare-earths PDF | 두 파일 200. **API 아님** | 무료 무키 파일; 연간·주로 2025 추정치. USGS 저작물/제3자 예외 구분 |
| TWSE / 대만 반도체 기업 월매출 | `opendata/t187ap05_L`; 회사 `2330/2344/2408/3711` | 200·1,086행 중 4회사 매칭. 관측 2026-08, 출표 2026-09-17 | 무료 무키·정부 open data licence. 호출 한도 미확인. Winbond만 단위 대조 완료 |
| SEC / 미국 법인 현금투자·공시 | `companyconcept/CIK0000789019/us-gaap/PaymentsToAcquirePropertyPlantAndEquipment.json`, `submissions/CIK0000789019.json` | 둘 다 403, 데이터 없음 | 공식 무키 무료 API, 식별된 자동 접근·10회/초/사용자. 403를 유료/키 필요로 해석하지 않음 |
| FRED / 미국 산업 실행·전기장비 backlog | v1 `series/observations`: `IPG3344S`, `CAPUTLG3344S`, `A35SUO` | 키 API 미시험. 별도 무키 CSV 3건 시간 초과/접속 종료 | 등록 키 필요. 보유 키 연결·인증 확인과 신규 발급은 별개. series별 권리·vintage 확인 |
| OpenDART / 한국 법인 공시·회계 | `fnlttSinglAcntAll.json`, `list.json`, `document.xml`, `corpCode.xml` | 문서 확인·인증 미시험. 상세 안내 일부 접근 실패 | 등록 키 필요. 호출 제한 오류 안내와 계정별 quota·리셋 조건 구분 |
| ECOS / 환율 통제 변수 | `StatisticItemList` / `StatisticSearch`; `731Y001/D/0000001` | 공개 sample metadata 10행 + KRW/USD 3일 데이터 | 공개 `sample` 시험만 성공. 일반 키·계정 권한·quota·재사용 조건 추가 확인 |
| iShares BAI / 액티브 ETF 구성 | 운용사 `latest-holdings.csv` | Equity 50행, holdings as-of 2026-10-01. **API 아님** | 공개 파일 무키. 전체 재배포 권리 미확정; 정기 snapshot 제안만 |
| EIA / 발전기·발전량·권역 부하 | v2 `operating-generator-capacity`, `facility-fuel`, `rto`; 대안 860M/923 파일 | 공식 문서 확인, 인증 미시험. 과거 860M 확인은 재사용 표시 | 무료 등록 키; bulk 파일 무키. JSON max 5,000행/요청, throttle 안내는 고정 보장 quota 아님 |
| ENTSO-E / 유럽 전력 부하 | `web-api.tp.entsoe.eu/api`, A65/A16·EIC area | 공식 token 절차 확인·XML 미호출 | 플랫폼 가입·API 접근 승인·token. 400회/분/token 안내. 비용·국가/항목 재사용 추가 확인 |
| Federal Register / 미국 규칙 사건 | `api/v1/documents.json`, large-load 검색 | 200·3행/300 결과, 첫 페이지만 | 무키; 정량 quota 미확인. 현행 법적 효력은 GPO/상세 원문에서 별도 확인 |
| Regulations.gov / docket·문서 단계 | v4 `documents`, `dockets` | 문서 확인·GET 미호출 | api.data.gov 키. 기본 1,000회/시간/key, 서비스별 차이·실제 header 확인. 댓글 제출 제외 |
| USAspending / award·transaction·outlays | v2 `search/spending_by_award/`; 후속 `spending_by_transaction/` | read-only POST 200·award 3행. transaction 미수집 | 무키. 정량 quota·재사용 전수 확인 미완료. 반환금액은 분기 지출 아닌 누적 award 요약 |
| PJM / 접속 준비·권역 부하·예측 | 공개 service requests; Data Miner `hrl_load_*`, `load_frcstd_hist` | 문서·공개 planning 확인, Data Miner 인증·queue export 미시험 | Data Miner 무료 키·계정/provisioning. 비회원 6회/분, 회원 600회/분. 원자료·파생 자료 재배포는 active membership 조건; 공개 데이터 게시 보류 |
| Singapore / 국가 발전량·전력 협정 | data.gov.sg `datastore_search`, resource `d_ae4afbaf5bc96bde19d8ce85810ab9f4`; EMA 원문 | 무키 200·wide 1행에 2026-04/05 2개월. 프로젝트 승인 API는 미확인 | 무키 탐색 무료, search 4회/10초; dev 8/prod 20. Open Data Licence 1.0. 협정·승인은 사건별 원문 |
| OpenRouter / 공개 모델 토큰 사용 | `api/v1/datasets/rankings-daily` | 무키 401, token 관측 없음 | key 필요; 30회/분/key·500회/일/account. 집계 자료 CC BY 4.0. **Dataset 호출 무료 여부 미확정** |
| Hugging Face / 배포 관심·버전 | `api/models`, task=text-generation, downloads 정렬·limit 2 | 200·2모델 | 공개 무키; 공식/실제 header 500회/5분. 모델 가중치 licence와 metadata 재사용 범위 구분 |
| GitHub / 추론 소프트웨어 변화 | `repos/vllm-project/vllm`, `releases?per_page=1` | repo·release 각각 200 | 공개 무키 60회/시간/IP. 저장소 licence와 API metadata 이용 조건 구분 |

[Comtrade](https://uncomtrade.org/docs/what-is-data-preview/), [Eurostat](https://ec.europa.eu/eurostat/web/user-guides/data-browser/api-data-access/api-introduction), [TWSE](https://openapi.twse.com.tw/), [SEC](https://www.sec.gov/search-filings/edgar-application-programming-interfaces), [FRED](https://fred.stlouisfed.org/docs/api/fred/), [EIA](https://www.eia.gov/opendata/), [Federal Register](https://www.federalregister.gov/developers/documentation/api/v1), [USAspending](https://api.usaspending.gov/), [Hugging Face](https://huggingface.co/.well-known/openapi.md), [GitHub](https://docs.github.com/en/rest)에서 공식 접근 설명을 확인할 수 있다. 위 실제 호출 결과는 별도 receipt이며, 문서 열람만으로 호출 성공을 표시하지 않았다.

## 먼저 저장할 관측 계약

| 수집 지표 / ID | 필드·단위·관측 단위 | 시점·개정과 연결 규칙 | 신호 후보와 한계 |
| --- | --- | --- | --- |
| 국가 메모리 IC 교역 / TM-01 | `primaryValue/fobvalue/cifvalue` USD; `netWgt` kg; `qty/qtyUnitCode`. 신고국×상대국×HS 판×품목×flow×월 | 수출 FOB/수입 CIF 분리. `H6` 판 대응·추계 플래그·제출/수정·조회 hash 저장. World 합계 1행으로 집중도 계산 불가 | 지역별 이동·가치/중량의 괴리 후보. 재수출·단가·믹스가 섞이며 HBM/비트 생산량 미식별 |
| 유럽 전자부품 생산 / TM-02 | `sts_inpr_m`, `indic_bt=PRD`, NACE C261, I21=2021년100, SCA. geo×월×분류×단위×조정 | 후속 query에 PRD·기준년·조정·status 명시 고정. 단일 2025-01 응답으로 현재 최신월·공표 지연 확정 불가 | 산업 실행 비교. 전자부품 전체이며 기업/SKU 생산·재고와 다름 |
| 한국 생산·출하·재고 / TM-04 | KOSIS 후보: `ORG_ID/TBL_ID/ITM_ID/C1…C8/PRD_DE/DT/UNIT_NM` | exact 반도체 표·기준년·KSIC·잠정·계절조정 미확정. `LST_CHN_DE`는 최초 공개일 아님 | 생산↑·출하↓·재고↑ 등의 조합을 나중에 검토. 지금 관측치·선행성 결과 없음 |
| 대만 회사 월매출 / TWAPI01–03 | 회사코드×`資料年月`×`出表日期`×snapshot; 당월·전월·전년동월·누적·제공자 증감률 | ROC `11508`→2026-08. Winbond NT$1,000와 5금액 공식 대조. 다른 3회사 원단위·연결범위 미확정, 합산/환산 금지 | 분기 전 월별 사업 실현 배경. 매출에는 가격·믹스·사업범위가 섞임; 기업 총액을 HBM/OSAT 물량으로 변환 금지 |
| 고객 현금투자 / ROOTAPI01·03 | SEC `cik/tag/units/start/end/val/filed/accn`; DART `corp_code/rcept_no/bsns_year/reprt_code/fs_div/account_id` | CFS/OFS, 회계연도/달력, CF 누적/단독 분기, 통화·정정 분리. 원문과 계정 정의 대조 | 계획 대비 법인 지출 실행 확인 후보. SEC 403·DART 미시험이며 시설/상품 배분 없음 |
| 미국 산업 실행 / ROOTAPI05–07 | `IPG3344S` 생산지수 2017=100 SA; `CAPUTLG3344S` 가동률 % SA; `A35SUO` 미충족 주문 백만USD SA | 월·산업분류·end-of-period·단위·realtime/vintage 저장; 첫 공표일이 없으면 null | 생산/가동과 전기장비 backlog 배경. 3344는 반도체만 아님; A35SUO는 변압기 개수·납기 전용 아님 |
| 정부 돈의 실행 / API-PP-07–09 | award ID·유형·recipient·장소; 거래 `action_date/federal_action_obligation`; 보고기간 outlays, USD | award 검색의 기간 filter가 반환금액을 분기 증분으로 바꾸지 않음. 거래 수정·감액·File C 보고기간·갱신일 필요 | 기명 프로젝트의 약정/의무액/지급 구분. 키워드 semiconductor 3행의 산업 적합성·분기 지급 미검증 |
| 발전·실제 전력 / API-PP-01–04·11·13 | 발전소/발전기 ID·월·상태·MW, net generation MWh, 권역×시간 MW. SG 국가×월 GWh | 명판·계약·실제 부하·에너지 분리. 실제 feed/시간대·revision 확인. SG 최신 2026-05는 10월 사용량 아님 | 운영 전환·지역 부하 배경. 동일 DC/고객 미터 없으면 AI 전용 사용 미식별 |
| 규제·승인 단계 / API-PP-05·06·14 | 문서/docket ID·관할·당사자·프로젝트·공표·시행·신청·허가일·원 단계 | FR list에 시행일 없어 상세 확인 필요. MOU/JDA/조건부 승인/가동은 별도 사건. current_effect는 null | 일정·적용 범위 변화 후보. 문서 개수로 공급 제한 크기나 승인 완료를 계산하지 않음 |
| AI 사용·개발 / AIAPI01–07 | OpenRouter UTC day×model variant×token/as-of/version; HF model ID·sha·rolling downloads; GitHub repo·release tag·published_at | OpenRouter 미인증·가격 미확정. HF 30일 rolling window, 차분≠신규 다운로드. vLLM 1 release와 backend 호환 별도 | 모델·소프트웨어 변화의 탐색. 관심·릴리스와 실제 inference·기업 채택·GPU/HBM 주문은 다름 |
| ETF 배분 / ROOTAPI09–10 | holdings as-of×fund×security×asset class×`Quantity/Weight/Price`; fund shares outstanding | CSV preamble의 날짜·발행좌수 보존. 동일 시점/단위·과거 snapshot·NAV 필요. 현재 1개 snapshot뿐 | q/S 비교와 설정·환매 후보를 가격 효과와 분리. 현재 flow 미계산, 회사 자금 수취와 다름 |
| 소재 구조 / TM-06 | commodity×형태/순도×국가×측정 연도×표×추정 기호. 갈륨 함량 kg, 희토류 REO equivalent t | MCS2026 발행 에디션과 주로2025 추정 연도 구분. 광산·저순도·정제·capacity·reserves 분리 | 공급국 구조 배경. 메모리 공정 직접 구매·고순도 수급·현재 수출통제는 추가 원문 필요 |

숫자가 없는 슬롯은 `null/TO_VERIFY`로 남긴다. 원문에 없는 주문·가격·생산량·품목·시설을 산업 합계로 채우지 않는다. 실제 관측월·공표일·최초 공개일·개정일·수집시각은 독립 필드다. UTC로 이름 붙인 수집 시각은 UTC로 저장하되 제공자의 원 날짜 정밀도를 보존한다.

## 지도에 연결할 키와 멈추는 지점

공통 관측 키는 `provider + dataset/series/version + entity/area/product classification + period + unit + adjustment + release/vintage`다. source URL·request filter·response hash·출처 역할도 같이 저장한다. 회사는 DART corp_code/SEC CIK/TWSE company code를 법인명·유효기간과 crosswalk하고, 통계 지역은 ISO와 제공자 country/EIC/BA code를 별도 대응한다.

제품 경로는 [산업 경로](semiconductor_industry_transmission_routes.md)의 PROD-01…12를 재사용한다. **HS 854232↔메모리, NACE C261↔전자부품, TiVA C26↔컴퓨터·전자·광학의 구조 연결**은 SKU나 같은 고객 주문의 join이 아니다. TiVA 부가가치 비율을 HS 상대국 집중도와 같은 지표로 합치지 않는다. 권역 전력 지표를 DC 좌표 근접만으로 배분하지 않는다.

직접 거래·실행의 연결에는 같은 법인, 계약/award/project ID, 시설, 상품·플랫폼 세대, 기간과 원문이 필요하다. 정부 지원은 recipient/UEI·award·장소를 실제 fab/DC 프로젝트와 확인하고 transaction/보고기간으로 넘어간다. 발전기와 DC는 PPA·접속·서비스 개시·실제 미터가 필요하다. AI 플랫폼의 model ID를 추론 소프트웨어 release와 연결하려면 실행 backend·버전·사용 사실을 먼저 확인한다. API 필드가 없는 연결은 별도의 기업·고객·정부 원문 조사로 남긴다.

## 가입·발급은 어디에 필요한가

| 분류 | 사이트 / 필요한 조치 | 지금의 판단 |
| --- | --- | --- |
| 기존 인증 연결 확인 | [OpenDART](https://opendart.fss.or.kr/), [FRED key 관리](https://fred.stlouisfed.org/docs/api/api_key.html) | 키 보유·활성화·인증 성공을 구분. 이번 개인 키를 읽거나 인증 호출하지 않았으므로 재발급 필요로 판정하지 않음 |
| 무료 계정·키 후보 | [Comtrade 개발자](https://comtradedeveloper.un.org/), [관세청 dataset](https://www.data.go.kr/data/15100475/openapi.do), [KOSIS OpenAPI](https://kosis.kr/openapi/), [EIA 등록](https://www.eia.gov/opendata/register.php) | Comtrade preview를 넘는 조회, 한국 무역·생산, 미국 운영 통계에 필요. KOSIS는 발급 전 exact 표/item도 확정해야 함 |
| 지역/문서 사례를 정한 뒤 | [ENTSO-E](https://transparency.entsoe.eu/), [Regulations.gov 개발자](https://open.gsa.gov/api/regulationsgov/), [PJM API](https://dataminer2.pjm.com/) | EU area/token, 미국 docket, PJM 내부 사용 목적·재배포 조건을 먼저 고정 |
| 비용·권한 확인이 먼저 | [OpenRouter key](https://openrouter.ai/keys), [ECOS](https://ecos.bok.or.kr/api/) 일반 키 | OpenRouter Dataset 무료 여부를 확인하기 전 무료 수집원으로 확정하지 않음. ECOS sample 성공을 일반 권한으로 승계하지 않음 |
| 지금 신규 키가 필요 없는 것 | Comtrade preview, Eurostat, OECD, TWSE, FR, USAspending, HF, 공개 GitHub; ETF/USGS 파일 | 작은 조회 가능. API 접근·전체 역사·quota·재배포 권리를 각각 확인하며 필요한 만큼 수집 |

이번 작업은 신규 가입·키 발급·결제·추론·메시지 전송을 수행하지 않았다. 공개 packet은 개인 계정·연락처·키 값·사용자별 보유 목록·비공개 원본을 포함하지 않는다. SEC 식별 요청에 개인정보를 넣는 방식은 자동 승인 검토에서 실행 전에 거절됐고, 이후 개인정보 없는 요청의 403 결과를 보존했다.

## 우선순위와 남은 공백

**당장 관측 설계를 고정할 대상**은 Comtrade preview·Eurostat 생산지수·TWSE 월매출이다. 실제 데이터가 나왔고 공급 이동·산업 실행·기업 실현이라는 서로 다른 관측 위치를 제공한다. TWSE의 최신월·회사별 단위 공백은 보완이 필요하다. FR는 규칙 사건 탐색, HF/GitHub는 기술 변화 탐색에 바로 쓸 수 있다. USAspending은 기명 award 적합성·기간별 거래를 확인한 뒤 돈흐름에 쓴다. SG 발전과 ECOS 환율은 지역/거시 배경이다.

**인증 후 우선 확인할 대상**은 기존 DART/FRED의 연결, 한국 관세청·KOSIS와 미국 EIA다. 상장사 IR의 DRAM/NAND bit shipment·ASP 설명, 고객 계약·설치/채택·전력 허가 원문은 API 회계/거시 필드만으로 대체되지 않는다. 갈륨·희토류는 소재 구조·품목 바스켓·현행 규칙·기명 공급자 연결을 따로 확인한다. ETF는 보유 snapshot부터 저장하고 ‘기업 투자금’이라는 열에 넣지 않는다.

공백은 고객별 AI 가동/유료사용·GPU시간, 메모리 실제 주문/납기·HBM 물량·공장/패키징 배정, 개별 DC 미터 부하, 허가의 현재 효력, 지표별 최초 공개 이력과 실증 선행성이다. API를 더 발급하는 것만으로 이 공백이 모두 해결되지는 않는다. 반복 수집기·전체 역사 패널·알림·DB·H1 편입은 아직 구현하지 않았다.

**다음 작업 하나:** Comtrade의 한국 HS854232 수출과 Eurostat의 독일 C261 생산지수에 대해 H6 분류 판 대응과 `indic_bt=PRD`·기준년·계절조정을 먼저 고정하고, 2025년 월별 소량 관측 파일럿을 만든다. 결측·수정·기간·단위·공표시점과 요청 종료를 검증하며 서로 다른 국가의 두 지표를 같은 거래나 인과로 합치지 않는다. DDR5 고객·상품 카드는 사용자 보류를 유지한다.

## 자료와 검증 경계

공개 자료는 [무역·생산·소재](../../../data/research/api_signal_feasibility/2026-10-05/trade_industry_materials.json), [회사·거시·ETF](../../../data/research/api_signal_feasibility/2026-10-05/finance_macro_etf.json), [전력·정책](../../../data/research/api_signal_feasibility/2026-10-05/power_policy_infrastructure.json), [AI 사용·기술](../../../data/research/api_signal_feasibility/2026-10-05/ai_usage_technology.json), [대만 회사 활동](../../../data/research/api_signal_feasibility/2026-10-05/taiwan_company_activity.json)의 다섯 packet이다. 번호가 있는 지표 34개와 무역·산업의 family별 측정 계약 6개를 담고 있으며 중복 없는 세계 지표 총수로 합산하지 않는다.

[통합 인덱스](../../../data/research/api_signal_feasibility/2026-10-05/collection_index.json)는 family·지표·실제 접근 결과를 원 packet에 연결한다. [Manifest](../../../data/research/api_signal_feasibility/2026-10-05/manifest.json)는 공개 바이트와 보존 입력을 고정한다. 원 HTTP 본문·실패 body, 파일 원문, 웹 도구 정규화 리뷰와 문서 확인을 별도 표현으로 추적하며 전체 원본은 이 공개 저장소에 재배포하지 않는다. 원문이 없는 web review에 원 HTTP hash를 만들지 않았다.

검증은 JSON schema/필드·참조·UTF8 LF·해시·단위/시점 구분·실패 보존·공개 정보 경계에 대한 것이다. 공개 패키지만으로 외부 원문 전체 재생·자료의 완전성·선행성·경제적 인과를 보장하지 않는다. [독립 목적 검토](research_convergence_review.md)는 현재 사용자 지시에 대한 범위를 별도로 점검하며 H1/Gate 6·정식 Evidence·사람 승인 상태는 바뀌지 않는다.
