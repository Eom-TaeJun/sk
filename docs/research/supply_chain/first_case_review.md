# 첫 사례: OpenAI–CoreWeave 주문서의 공개 연결 범위

검토일: **2026-10-03**. 연구 후보이며 승인 Evidence·선행성 검증 결과가 아니다. 관측 대상은 **2025-09-23의 주문서 사건** 한 건이며 현재 두 회사의 전체 계약 잔액을 나타내지 않는다.

경제적 질문은 고객의 구매 약정을 특정 시설·장비·전력·현금의 실제 실현과 어디까지 연결할 수 있는가다. [경제적 목적](decision_purpose.md)의 첫 실험으로, 기존 지도에서 `openai-coreweave-capacity` 관계를 선택했다.

## 공개 원문에서 읽은 범위

원출처는 [SEC 8-K Item 1.01](https://www.sec.gov/Archives/edgar/data/1769628/000119312525216497/d17274d8k.htm)과 [제출 목록](https://www.sec.gov/Archives/edgar/data/1769628/000119312525216497/0001193125-25-216497-index.html)이다. 검색 도구로 두 페이지를 읽었다. 아래는 수동 원문 검토이며 수집기의 성공 산출물로 표시하지 않는다.

| 관측 | 공개 확인 범위 |
|---|---|
| 계약 당사자 | 공급자 CoreWeave, Inc.; 고객 OpenAI OpCo, LLC. 지도 그룹명과 실제 계약 법인을 구분한다. |
| 사건 | 기존 2025-05-08 MSA 아래 2025-09-23 새 주문서 체결. 공시일은 2025-09-25다. |
| 대상·금액 | 예약 클라우드 컴퓨팅 용량에 관한 최대 약 USD 65억 지급약정, 2031-05-31까지. 납품·서비스 가용성과 해지 조건이 있다. |
| 실제 실현 | 최소 구매액, 실제 지급·선수금·사용량·서비스 개시·주문서별 매출은 이 요약으로 확인하지 못했다. 0으로 채우지 않는다. |
| 시설·칩·전력 | 특정 부지, GPU/HBM 종류·수량, 전력 MW/MWh와 이 주문서의 배정을 확인하지 못했다. |

[Exhibit 10.1](https://www.sec.gov/Archives/edgar/data/1769628/000119312525216497/d17274dex101.htm)은 5월 MSA다. 9월 주문서 전체가 공개됐다고 가정하지 않는다. 비공개·생략 조건을 추정해 빈칸을 채우지 않는다.

## 기존 지도와 연결할 때

| 관계 ID | 역할 | 이번 주문서와의 연결 |
|---|---|---|
| `openai-coreweave-capacity` | 선택한 고객 약정 | 공시 accession·법인·사건일로 식별하는 직접 대상 |
| `nvidia-coreweave-platform` | CoreWeave 플랫폼 배경 | 해당 주문서의 장비 배정은 미확인 |
| `coreweave-corescientific-colocation` | 시설 공급 계약 배경 | 해당 주문서의 시설 배정은 미확인 |
| `coreweave-corescientific-funded-capex` | 다른 상대방이 공시한 고객부담 CAPEX | OpenAI 약정으로 조달된 돈이라는 연결은 미확인 |
| `v3-ddtl-lenders-borrower` | 별도 차입법인의 금융 약정 | 해당 주문서의 자금 용도·실제 인출은 미확인 |

회사 전체 수치와 인접한 관계가 존재해도 주문서별 결과를 계산할 수는 없다. 이 사례에서 얻은 판단은 **조건부 구매 약정은 관측되지만, 특정 설비의 실현과 연결하려면 추가 직접 근거가 필요하다**는 것이다. 후속 공개가 없다는 사실은 이행 실패·취소를 뜻하지 않는다.

## 접근 시험과 검증 상태

직접 원문 다운로드 시험에서 SEC 서버의 **HTTP 403**을 확인했다. 이 실패는 [접근 실패 이력](../../../data/research/customer_commitments/coreweave_openai_20250923/acquisition_failures/)에 보존한다. 이후 [공식 투자자 사이트](https://investors.coreweave.com/financials/sec-filings/default.aspx)의 공개·무키 filings feed에서 회사가 제공하는 HTML 경로를 찾았다. 실제 파일을 읽어 같은 사건의 조건을 추출할 수 있음을 확인했다.

회사 제공 파일은 8-K 본문과 MSA 첨부를 결합한 형식이다. SEC 원본 바이트와의 동일성은 확인하지 못했다. Feed의 `FilingId=18796309`는 제공자 식별자이며 SEC accession이 아니다. `FilingDate`는 날짜 정밀도로 사용하고 `ReceivedDate`를 SEC acceptance 시각으로 바꾸지 않는다. 실제 수집 URL·host·source role·hash를 SEC 원출처 참조와 구분한다. 공식 페이지에서 원문까지의 [발견 경로와 JSON locator](../../../data/research/customer_commitments/coreweave_openai_20250923/discovery.json)를 함께 남겼다.

수집기의 실제 산출물은 [후보 기록](../../../data/research/customer_commitments/coreweave_openai_20250923/record.json)과 [수집 manifest](../../../data/research/customer_commitments/coreweave_openai_20250923/acquisition.json)로 연결한다. 네트워크 접근·해시 재검사와 합성 회귀 검사는 다른 검증이다. 수집 성공을 실제 지급·가동 확인이나 선행성 검증으로 해석하지 않는다.

2026-10-03 `--source issuer` 실행은 원문 HTML 119,503 bytes와 feed JSON 32,802 bytes를 수집했고 capture 한 건을 생성했다. `--verify-only`는 원문 해시·추출 결과 재검사에 통과했다. 전체 115개 테스트 중 신규 수집 회귀는 25개이며, 이 테스트 자료는 합성 자료다. 라이브 접근 결과는 실제 capture와 실패 영수증으로 확인한다.

**2026-10-03 당시의 다음 작업 권고:** 같은 주문서와 직접 연결되는 후속 공시 한 건에서 서비스 개시 또는 실제 현금 수취의 공개 여부를 확인한다. 현재 수집 순서와 다음 경제적 조사는 [지표 수집 목적](indicator_collection_purpose.md)을 따른다.
