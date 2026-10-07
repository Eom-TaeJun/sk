# SK하이닉스 공급망과 시장 학습

SK하이닉스의 영업·마케팅·상품기획·신제품사업화 직무를 이해하기 위해 상품, 고객의 사용 목적, 채택·구매 과정과 공급 조건을 연결한다. HBM·서버 DRAM·eSSD를 중심으로 AI 기술과 관련 산업의 변화가 누구의 어떤 요구와 일정에 영향을 주는지 설명하는 것이 목적이다.

## 현재 작업

공개 자료로 **왜 반도체가 필요했고, 어떤 기술·상업 성과가 어떤 상품의 채택으로 이어졌으며, 앞으로 어떤 투자 경로와 위험에 대비할지** 구조화한다. 지표마다 수집 목적·단위·시점·변화 뒤 확인할 관계를 정한다. 내부 주문량·원가·수율·공급 배정은 현재 과제에서 제외하며 고객·상품 카드의 강제 수렴과 API 일괄 수집은 보류한다.

| 읽을 순서 | 확인할 내용 |
| --- | --- |
| [직무와 상품·고객 관점](docs/research/supply_chain/sk_hynix_commercial_role_context.md) | 이 학습의 목적과 고객·사양·인증·구매 역할 |
| [지표 수집 목적](docs/research/supply_chain/indicator_collection_purpose.md) | 질문별 관측 목적, 수집 실행 범위와 다음 작업 |
| [무료 API 접근 결과](docs/research/supply_chain/api_signal_feasibility.md) | dataset·필드·단위·인증·접근 실패와 재사용 조건 |

[수요 근거·투자 경로·위험 시나리오](docs/research/supply_chain/structural_market_scenarios.md)는 공개 성과, 기관/운용사의 타겟, ETF와 기업 현금의 경로, 지정학·KV/효율·AI 수익성·대체 기술을 연결한다. 다음 연구 질문은 지표 목적 문서를 따른다. KOSIS는 회사 설명과 산업 실행의 비교가 필요할 때 정확한 측정 계약부터 정할 조건부 작업이다.

## 필요한 산업 배경

| 질문 | 필요한 문서 |
| --- | --- |
| 반도체 제품·사업모델·제조 기능과 실제 기업은 어떻게 나뉘는가 | [거시 산업 구조](docs/research/supply_chain/semiconductor_macro_structure.md) |
| AI 업무와 기술 변화는 어떤 메모리 요구를 만드는가 | [AI 기술과 상품 요구](docs/research/supply_chain/ai_technology_memory_links.md) |
| 전력·소재·정책·금융·항공우주는 반도체와 어떻게 연결되는가 | [산업 전파 경로](docs/research/supply_chain/semiconductor_industry_transmission_routes.md) |
| 측정 설계·관측 사례·출처를 더 확인해야 하는가 | [공급망 자료 안내](docs/research/supply_chain/README.md) |

관련 산업의 연결 구조는 학습 범위다. 해당 분야의 모든 수치를 동시에 수집하지 않으며, 같은 상품·법인·프로젝트·시설·관할 또는 구체 비교 질문이 있을 때 필요한 자료를 선택한다.

## 보존된 구현과 연구

원자료·승인 계약·기능코드와 과거 검증은 [구현과 설계 참조](docs/reference_index.md)에 정리한다. H1은 Gates 1–5 승인 및 corpus/Gate 6 검토 패키지 준비 상태이며, 사람의 Gate 6 동결은 대기 중이다. H1 지표·선행 기간·실현율·verdict는 미계산이다. H2/H3·에이전트 실행체계·대시보드·DB는 현재 구현 과제가 아니다.

연구 후보와 학습 노트는 정식 Evidence·예측력·사업 성과로 자동 승격하지 않는다. 세계 전체 공급망이나 지속 수집 체계의 완성을 주장하지 않으며, 직무·지원서 설명에는 실제 수행과 검증 범위만 사용한다.

## Stable validation commands

저장소 루트에서 실행한다. 작업자 규칙과 테스트 격리 조건은 [AGENTS.md](AGENTS.md)를 따른다.

```powershell
python -m unittest -v
python scripts/validate_supply_chain_research.py
python scripts/validate_current_research.py
```

두 연구 검증기는 날짜별 자료의 무결성과 참조를 검사한다. 현재 원격 접근·경제적 선행성·사람 승인을 검증하지 않는다. 원문과 연구 JSON의 hash는 보존한다.
