# CMX로 보는 메모리 요구와 실제 투자 대상

기준일 **2026-10-08**. 공개 자료를 연결한 연구 후보다. **CMX의 변화는 HBM 옆에 공유 flash KV 캐시 계층을 추가하는 것**이다. 하이닉스 관점에서는 HBM·호스트 DRAM·eSSD의 요구를 함께 보되, 각 계층의 지연·용량·전력·소프트웨어 조건과 실제 제공 단계를 구분해야 한다. 운용사의 AI 투자 대상과 겹치는 부분은 있지만, 기업 지분 보유가 해당 제품의 주문을 입증하지는 않는다.

이 사례는 [공개 구조와 시나리오](structural_market_scenarios.md)의 긴 문맥·효율·계층 재배치 가정을 구체화한다. [출처 기록](../../../data/research/cmx_memory_investment_signals/2026-10-08/sources.json)에 Source ID, 짧은 원문, locator, 날짜, 접근 결과와 hash를 둔다.

## 고객이 해결하려는 문제와 메모리 계층

NVIDIA는 긴 문맥과 반복 추론에서 계산한 KV를 보관·공유·재사용하는 CMX 아키텍처를 설명한다. 조사할 경제적 문제는 **재계산 시간, 첫 응답 지연, 동시 요청 처리와 저장·이동·전력 비용**이다. 효율이 좋아져도 총 사용량과 실제 장비 구매의 방향은 별도로 확인해야 한다. 다음 계층은 NVIDIA의 정의이며, 모든 시스템이 같은 구성이라는 뜻은 아니다. **CMX-NV-BLOG26**. [NVIDIA 기술 설명](https://developer.nvidia.com/blog/introducing-nvidia-bluefield-4-powered-inference-context-memory-storage-platform-for-the-next-frontier-of-ai/).

| 계층 | 공식 설명의 역할 | 상품·시스템에서 확인할 요구 |
| --- | --- | --- |
| G1, GPU HBM | 현재 생성에 쓰는 hot KV | 실행에 필요한 용량·대역폭·전력. 저장장치의 용량으로 대체 계산하지 않음 |
| G2, system RAM | staging·buffering | 호스트 메모리 용량·이동 경로. CMX라는 이유로 DDR5 규격을 지정하지 않음 |
| G3, local SSD | 노드에 묶인 warm KV | 재사용 지연·I/O·용량·내구성 |
| G3.5, CMX 공유 flash | Ethernet으로 연결된 pod 차원의 KV 캐시 | 여러 노드의 공유·재사용, SSD와 fabric·저장 처리기·소프트웨어의 조합 |
| G4, durable storage | 오래 보관할 artifact·history·results | 보관·재읽기·복구의 요구. CMX 캐시 시험과 별도 |

CMX의 KV는 decode 전에 G2 또는 G1으로 prestage한다. 일반 Dynamo **v1.4.0 KVBM 설계**에는 optional GDS를 사용하는 disk→GPU 직접 이동도 있다. 따라서 모든 CMX 경로가 반드시 CPU RAM을 거친다고 고정할 수 없다. 이 일반 설계 문서에는 CMX/Memos가 명시되지 않아 특정 CMX connector의 상용 지원 근거로 쓰지 않는다. **CMX-NV-BLOG26 / CMX-DYNAMO-DESIGN140**. [버전이 붙은 KVBM 설계](https://docs.nvidia.com/dynamo/v1.4.0/knowledge-base/modular-components/kvbm/kvbm-design).

현재 상품 페이지는 BlueField-4의 NVMe SSD 관리, DOCA Memos의 KV 관리, Spectrum-X fabric과 Dynamo의 배치·재사용 역할을 설명한다. 상품 페이지의 파트너 이름은 생태계 관계이며, 메모리 SKU·인증·고객 발주를 정하는 부품 목록은 아니다. **CMX-NV-PRODUCT26**. [NVIDIA CMX 상품 설명](https://www.nvidia.com/en-us/data-center/ai-storage/cmx/).

## 실제로 어디까지 진행됐는가

| 자료 시점 | 기명 주체와 확인한 사건 | 원 단계와 해석 |
| --- | --- | --- |
| 2026-03-16 | NVIDIA의 STX reference architecture, Vera CPU·BlueField-4·ConnectX-9·Spectrum-X 조합; CoreWeave·Crusoe·OCI 등의 도입 계획 | 본문은 **planning to adopt**. 파트너 제공은 2026년 하반기 계획. 고객 가동·메모리 구매량은 미확인. **CMX-NV-STX26**. [STX 발표](https://nvidianews.nvidia.com/news/nvidia-launches-bluefield-4-stx-storage-architecture-with-broad-industry-adoption) |
| 2026-04-28 표시 | Solidigm이 D7-PS1010과 D5-P5336을 KV 업무별 선택지로 설명 | **공급사의 제품 포지셔닝**. 특정 CMX 시스템의 인증·선정·주문 발표가 아님. **CMX-SOLIDIGM26**. [Solidigm 설명](https://www.solidigm.com/products/technology/what-is-cmx-context-memory-storage.html) |
| 2026-05-18 표시 | Dell이 Grace CPU로 Vera ARM64 환경을 모사한 working system 설명 | 당시 CMX/BlueField-4 전용 장비는 상용 제공 전이라고 명시. 모사 시험과 실제 전용 장비 출하를 구분. **CMX-DELL-DEMO26**. [Dell 설명](https://infohub.delltechnologies.com/en-us/p/breaking-the-ai-inference-context-memory-barrier-with-dell-storage/) |
| 2026-05-31 | NVIDIA가 STX 파트너 제공 시점을 재안내 | 여전히 **2026년 하반기 예상**. 5월의 계획을 10월의 출시 판정으로 바꾸지 않음. **CMX-NV-AVAIL26**. [제공 계획](https://nvidianews.nvidia.com/news/nvidia-vera-bluefield-4-stx-brings-agentic-ai-storage-processing-with-in-silicon-security) |
| 2026-10-08 조회 | CMX 상품·생태계 페이지와 고정 버전 Dynamo 설계; 아래의 실제 release API 응답 | 설명·소프트웨어 사건을 확인. 이 선정 원문에서는 현재의 기명 CMX 상용 제공·고객 구매를 확인하지 못함. 세계 전체에서 없다는 판정은 아님 |

NVIDIA CMX 블로그의 **최대 5배 TPS·5배 전력 효율**과 STX 발표의 **최대 4배 에너지 효율**은 회사 주장이고 비교 대상도 다르다. 읽은 설명에는 재현에 필요한 전체 모델·입출력·동시성·재사용률·장비·전력 측정 조건이 없다. Dell의 **19배 TTFT 개선·5.3배 TPS**는 기존 G4 저장 시스템의 내부 시험이며 CMX 납품 성과로 합치지 않는다. 이번에 독립 벤치마크를 실행하지 않았다. **CMX-NV-BLOG26 / CMX-NV-STX26 / CMX-DELL-DEMO26**.

Dell 공식 웹 본문은 읽었지만 별도 원문 GET은 **403**이었다. 출처 기록에 웹 본문 검토와 raw 응답 확보 실패를 분리했다. 다른 11건은 원 응답 hash·bytes를 확보했다. 동적 페이지의 조회일·수정 헤더는 최초 공개일이나 채택일을 대신하지 않는다.

## 하이닉스의 상품 질문으로 바꾸기

Solidigm은 **D7-PS1010(TLC)**을 재사용이 많고 지연에 민감한 KV 업무, **D5-P5336(QLC)**을 용량·밀도와 warm spillover의 선택지로 제시한다. 동일한 NAND 수요로 묶기보다 **응답 지연을 줄이는 저장**과 **많은 KV를 보관하는 저장**의 요구를 나눠야 한다. 실제 적합성은 workload·QoS·읽기/쓰기·내구성·전력·지원 구성으로 확인한다. 공급사 권장만으로 특정 제품의 매출 증가를 예상할 수는 없다. **CMX-SOLIDIGM26**. [제품 선택 설명](https://www.solidigm.com/products/technology/what-is-cmx-context-memory-storage.html).

이 원문의 FAQ는 G3를 local DRAM으로 표기하지만 NVIDIA 원문은 local SSD로 정의한다. 계층 표에는 플랫폼 원문을 사용하고 불일치를 보존한다. Solidigm의 제품 선택 설명은 별도의 상품 관점으로 읽는다.

하이닉스도 HBM·AI-DRAM·AI-NAND를 함께 설명하고 AI-NAND를 성능·대역폭·밀도 방향으로 나눈다. 이는 회사의 포트폴리오·개발 방향이다. **SRC-HY26-PORTFOLIO**, 기존 2026-07-08 자료 재사용. [하이닉스 공식 설명](https://news.skhynix.com/en/hbm-to-essd/). CMX가 호스트 메모리 수요를 모두 DDR5로 만들거나 HBF와 같은 상품이 된다고 연결하지 않는다.

| 직무 | 이 사례에서 준비할 공개 질문 |
| --- | --- |
| 영업 | 사양 결정자인 플랫폼 회사, 시스템 판매자인 OEM, 서비스 운영자인 CSP의 일정·지원 범위는 각각 무엇인가? |
| 마케팅 | 구매자가 원하는 것이 첫 응답 지연·처리량·용량·전력 중 무엇이며, 같은 조건에서 재계산·캐시 재사용 대안과 비교할 수 있는가? |
| 상품기획 | HBM·호스트 메모리·SSD 중 어느 계층의 요구인가? SSD는 지연·내구성·밀도 중 무엇을 우선하며 네트워크/소프트웨어 지원은 무엇인가? |
| 신제품사업화 | 권장·모사 시험·지원·인증·상용 제공·출하 중 현재 단계는 무엇이며, 공식 지원 조합과 제공 범위가 다음 단계에서 명시되는가? |

## 운용사의 타겟과 실제 보유 증권을 대조하기

iShares의 **2026-08-24 중간 전망**은 AI 인프라 투자와 실제 활용·수익화를 함께 보며 BAI를 AI 기술 스택에 대한 액티브 주식 노출로 소개한다. 이 자료의 투자 관점과 기업의 실제 구매는 다른 관측이다. 이 한 편을 기관 전체의 최신 견해로 부르지 않는다. **SRC-STRUCT-BLACKROCK26**, 기존 원문 기록 재사용. [iShares 전망](https://www.ishares.com/us/insights/portfolio-insights/thematic-investing-mid-year-2026-outlook-ai-economy).

아래는 **BAI 2026-10-01 보유 snapshot**에서 골라 연결한 다섯 행이다. 기존 CSV의 관측일을 사용하며 10월 8일 현재 비중으로 갱신한 값이 아니다. Quantity는 주식 보유 수량, Weight는 펀드 비중이다. 원본의 금액·Price 통화는 USD이고 Market Currency·FX는 별도여서 다시 환산하지 않는다. 기존 조회는 10-04 UTC, 원본 10,282 bytes·Equity 50행. **ishares-bai**, [기존 접근 기록](../../../data/research/api_signal_feasibility/2026-10-05/finance_macro_etf.json), [발행사의 무료 CSV 경로](https://www.ishares.com/us/products/339081/ishares-a-i-innovation-and-tech-active-etf/latest-holdings.csv).

| 보유 증권 | Weight (%) | Quantity | 공식 상품·산업 역할 | CMX와의 연결·불일치 |
| --- | ---: | ---: | --- | --- |
| MU, Micron | 6.68 | 893,093 | HBM·DDR5/RDIMM·NVMe SSD. **CMX-MICRON-PORTFOLIO**. [제품군](https://www.micron.com/markets-industries/data-center-servers) | 메모리·저장 역할은 겹침. 6.68%를 HBM 전용 또는 CMX 매출 노출로 분해 불가 |
| SNDK, Sandisk | 2.43 | 199,799 | DC SN861 PCIe Gen5 NVMe eSSD, MGX 방향. **CMX-SANDISK-PORTFOLIO**, 2026-06-02. [회사 설명](https://www.sandisk.com/company/newsroom/blogs/2026/powering-ai-factories-from-the-data-layer-up) | enterprise 저장 역할. MGX 설명이 CMX 인증·제품 선정·주문 증거는 아님 |
| ANET, Arista | 2.16 | 1,550,409 | AI Ethernet; 7060X6의 Broadcom Tomahawk 5. **CMX-ARISTA-ETHERLINK24**, 2024-06-05. [플랫폼 발표](https://investors.arista.com/Communications/Press-Releases-and-Events/Press-Release-Detail/2024/Arista-Unveils-Etherlink-AI-Networking-Platforms/default.aspx) | 네트워크라는 산업 역할은 겹침. NVIDIA Spectrum-X의 기명 CMX 구성과 다른 제품이며 직접 공급 관계 미확인 |
| 2308, Delta Electronics | 1.95 | 4,783,000 | power shelves·HVDC·액체냉각·DCIM. **CMX-DELTA-AI**. [AI 제품군](https://www.deltaww.com/en-US/landing/Delta-for-AI) | 데이터센터의 전원·냉각 인접 역할. 특정 CMX 부품 목록·수주 증가와 연결 불가 |
| 000660, SK hynix | 1.76 | 190,963 | HBM·시스템 DRAM·NAND/eSSD의 회사 포트폴리오; Solidigm의 위 SSD 선택지와 별도 상품 연결 | 상장 회사의 지분 노출. Solidigm SKU의 실제 채택·메모리 발주 비중을 ETF 행에서 알 수 없음 |

이 표로 확인한 것은 **메모리·저장·네트워크·전원/냉각에 걸친 실제 증권 노출**이다. 한 snapshot으로 비중 변화·운용사 신규 매수·ETF 자금 유입을 계산할 수 없다. 실제로 돈이 이동했는지는 `증권 배분`, `고객의 장비 대금`, `공급자의 매출/현금 투자`, `AI 사용자의 수익·생산성`에서 각각 직접 확인해야 한다. 기술 효율 개선은 이 네 경로를 같은 방향으로 자동 움직이지 않는다.

## 어떤 공개 시그널을 왜 수집할 것인가

| 확인할 변화와 목적 | 무료 공개 경로·필드 | 관측 뒤 재검토할 내용·반례 |
| --- | --- | --- |
| **상용 제공 단계**: 계획이 구매 가능한 시스템으로 진행됐는가 | NVIDIA/OEM/CSP 공식 웹·IR. 상품×법인 역할×원 단계, 사건/공개/목표일, 지원 버전·SKU·지역·제공 범위 | 기명 시스템의 상용 제공·지원 범위가 새로 명시되면 해당 상품 관계를 갱신. demo·예정만 반복되거나 지연/축소되면 상업 실행 가정을 보류 |
| **소프트웨어 지원**: KV 이동·재사용 경로가 실제 지원표에 들어갔는가 | GitHub releases API 무키 단일 요청 성공; tag·target_commitish·draft/prerelease·공개/갱신 시각·본문·지원 backend/connector. 고정 버전 Dynamo/DOCA 문서 병행 | release는 기술 사건. CMX/Memos 명시·버전/구성 지원이 없다면 CMX 배포로 승격 불가 |
| **SSD 요구의 변화**: 지연과 용량 중 무엇이 선택 기준인가 | Solidigm/OEM 공개 datasheet·지원 자료. SKU/폼팩터·capacity(GB/TB)·I/O(IOPS/GB/s)·지연(µs/ms)·QoS·내구성(DWPD/TBW)·전력(W)·시험 조건 | 같은 조건의 지연·밀도·내구성 tradeoff를 비교. 순차 최고속도나 최대 용량만으로 KV 적합성을 판단하지 않음 |
| **조건별 기술 성과**: 공유/재사용이 고객 문제를 실제로 줄이는가 | 공개된 시험·논문·공식 benchmark만 선택. 모델/dtype·입출력 토큰·동시성·prefix 재사용 조건·장비·backend, TTFT/ITL(ms), TPS(tokens/s), p99, 전력(W), 비교 baseline | 비용·지연 개선은 시험 범위에서 해석. 품질·장비·전력/재사용 조건 누락, 전송 비용·tail latency 악화가 있으면 일반화를 철회. 사업자의 비공개 /metrics는 수집 대상에서 제외 |
| **공개 공급·지출 실행**: 기술 방향이 회사 실적/투자와 정합적인가 | 기존 하이닉스 분기 원문·공급사 IR/공시. 공개 eSSD/제품 믹스·bit/ASP·인증/출하 사건, 투자 계획과 현금 취득, 기간·통화·회계 범위 | 회사 전체 실적은 공급 배경. CMX 전용 매출·현금으로 배분하지 않음. ASP·물량·믹스와 계획·집행을 분리 |
| **증권 배분**: 운용사가 어느 산업 역할에 노출되는가 | 기존 iShares CSV. fund/security/as-of·Weight·Quantity·Price·Market Value·Currency/FX·발행좌수 | 공식 전망의 타겟과 실제 보유 역할을 비교. 같은 시점/정의의 후속 자료 없이 추세·flow를 만들지 않으며 기업의 대금 수취로 해석하지 않음 |

이들은 **먼저 확인할 공개 사건·요구의 후보 신호**다. 경제적 선행성과 예측력은 아직 검증하지 않았다. 제품 출시·인증·지원 변화가 어느 구매/매출보다 앞섰는지 같은 대상으로 후속 확인해야 한다.

실제 무료 API 최소 응답은 `GET https://api.github.com/repos/ai-dynamo/dynamo/releases?per_page=1&page=1`이다. 인증 없이 HTTP 200으로 **한 행**을 받았다. 반환된 tag는 **v1.5.1**, 공개 시각은 **2026-10-07T01:54:13Z**, draft/prerelease는 false였고 이 release 본문에는 CMX/Memos 언급이 없었다. 고정 v1.4.0 설계와 다른 버전의 release 사건이므로 두 자료를 같은 지원표로 합치지 않는다. 첫 반환 한 행은 전체 역사나 최신 안정판 판정이 아니다. **CMX-DYNAMO-RELEASE-PROBE**. [확인한 release](https://github.com/ai-dynamo/dynamo/releases/tag/v1.5.1).

공식 제품·지원·IR 웹은 무료 수동 열람 경로이며 전용 데이터 API를 확인한 것은 아니다. GitHub API와 ETF CSV의 최소 접근 성공도 반복 수집·전체 기록·재배포 권리를 보장하지 않는다. 새 계정/키나 수집 실행 체계를 추가하지 않았다.

## 조건부 기회·위협과 준비

**재사용이 성과를 내고 서비스 사용이 늘 때:** 공유 KV가 재계산과 응답 지연을 줄인다는 같은 조건의 공개 시험, 기명 시스템 제공·채택을 확인한다. SSD·fabric·저장 소프트웨어의 요구가 늘 수 있지만 HBM의 총 구매 증가까지 전제하지 않는다. 준비는 HBM 실행 요구와 SSD 지연/밀도 요구를 따로 설명하는 것이다.

**효율이 요구를 바꾸거나 다른 구조가 등장할 때:** 더 높은 재사용, KV 압축/정밀도·모델 구조 변경은 같은 요청의 메모리·전송 요구를 줄이거나 계층별 믹스를 바꿀 수 있다. 같은 품질·업무·서비스 목표의 비교가 없으면 총수요 방향은 미확인이다. 준비는 기존 상품의 용량 주장보다 호환성·QoS·내구성과 소프트웨어 대안을 함께 비교하는 것이다.

**상업화·자금·전력 준비가 늦을 때:** 기명 제공일의 지연·지원 조합 축소, 공개 투자 집행/제품 출하 설명과 계획의 불일치를 확인한다. 전력 부족은 해당 시설의 규제·접속·통전 자료가 있을 때만 연결하며 이번 CMX 원문에 특정 시설을 붙이지 않는다. ETF 비중만 먼저 움직이면 투자 관심과 실제 장비 구매를 구분한다. 공개정보 부재를 취소나 공급 부재로 쓰지 않는다.

**다음 검토 하나:** D7-PS1010과 D5-P5336의 공개 사양·시험 조건을 대조해 KV 재사용 지연과 저장 밀도의 tradeoff를 구체화한다. 내부 주문·원가·실제 이용률 없이 상품 요구를 이해하는 비교이며 CMX 선정 SKU라고 전제하지 않는다. 현재 범위의 소유 문서는 [지표 수집 목적](indicator_collection_purpose.md)이다.

원문 확보와 공개 해석의 한계를 유지한다. Sandisk의 최근 IR PDF는 웹 도구의 크기 제한과 두 번의 다운로드 시간 초과로 본문을 읽지 못해 제외했다. 자료 통합은 사람의 정식 Evidence 승인·H1 Gate 6 동결·현재 주문/선행성/사업 성과의 판정이 아니다.
