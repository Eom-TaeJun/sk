# Memory Market Decision Intelligence

SK하이닉스의 영업·마케팅·상품기획·신제품사업화 직무를 이해하기 위해 **상품, 고객의 사용 목적, 채택·구매 과정과 공급 조건을 연결하는 공급망 지식 기반**을 만드는 프로젝트다. 2026년 하반기 공식 직무 안내를 기준으로 “누구에게 어떤 상품을 왜, 언제 제안할 것인가”를 설명하는 데 목적을 둔다. 공개 수요·공급 신호의 검증과 출처 추적은 이 학습을 뒷받침하는 연구 방법이다.

시작 문서: [하이닉스 상품·고객·직무 관점](docs/research/supply_chain/sk_hynix_commercial_role_context.md).

산업 배경: [반도체 산업 거시 구조](docs/research/supply_chain/semiconductor_macro_structure.md) — 제품·사업모델·공정·수요시장·지역과 실제 기업 역할을 연결한다. [메모리 사이클과 지표 수집 계획](docs/research/supply_chain/memory_cycle_signal_plan.md)은 수요·공급·자금의 관측 목적, 무료 경로와 미수집 공백을 정리한다.

첫 구체 사례: [HBM3E × NVIDIA GB300 고객·상품 카드](docs/research/supply_chain/customer_product_cards/hbm_nvidia_gb300.md) — 고객 문제, 직무별 질문, 채택 사건과 무료 관측 후보 8개.

기술 변화와 상품 요구: [AI 업무·병목·메모리·채택·공급 연결표](docs/research/supply_chain/ai_technology_memory_links.md) — HBM·호스트 DRAM·SSD의 역할, 소프트웨어 조건과 대표 채택 사건을 구분한다.

산업 간 연결: [반도체 제품에서 산업으로 이어지는 전파 경로](docs/research/supply_chain/semiconductor_industry_transmission_routes.md) — 제품 축과 파운드리·설계·후공정 기능을 분리하고 데이터센터·전력·통신·항공우주와 정책·협정의 조건부 연결을 점검한다.

```text
Real decision problem
→ economic / industry model
→ evidence and data
→ AI-assisted research
→ empirical validation
→ decision update
→ project evidence
→ application / interview translation
```

2026-10-03 사용자가 직무 준비와 산업·상품 이해를 우선 목적으로 명확히 했다. 배경지식 학습과 실제 수행 증거는 구분한다. 채용·경험기술서에 쓰는 성과는 실제 조사·구현·검증 범위를 따라야 한다.

## Current phase

- 완료: HBM4 Evidence → Graph → Audit → Memo Vertical Slice
- 완료: Evidence별 Human Review와 2025→2026 Temporal Update
- 완료: capability-first, runtime-agnostic architecture reframing과 baseline cleanup
- H1: Gates 1–5, measurement contract, 24-Track registry와 수집·Gate 6 검토 패키지 준비
- H1 검증 대기: 사람의 Gate 6 dataset freeze 및 Event 검토. 지표·lead/lag·실현율·verdict는 미계산
- 연구 자료 추가: [반도체·AI·데이터센터·전력·금융 공급망](docs/research/supply_chain/README.md) — 기존 세 저장소의 방법론 검토와 2026-10-03 후보 자료
- 현재 우선순위: [2026 하반기 직무·상품·고객 구조](docs/research/supply_chain/sk_hynix_commercial_role_context.md) — HBM·서버 DRAM·eSSD의 고객 문제와 채택 단계 학습
- 거시 학습 구조 정리(2026-10-04): 산업 분류·기업 역할·메모리 사이클·18개 지표 후보와 원문 영수증
- [첫 분기 관측표](docs/research/supply_chain/memory_observation_panel_2026q2.md)(2026-10-04): 하이닉스·삼성의 2026Q2 재고·DRAM/NAND 출하·ASP·설비 지출. 제품·사업·기간 범위를 보존한 후보 기록이며 반복·역사 패널과 선행성 검증은 미구축
- [AI 기술과 상품 요구 연결](docs/research/supply_chain/ai_technology_memory_links.md)(2026-10-04): 연결 일곱 가지, 구현·시험 조건과 채택·주문·공급 공백. 업계 총수요나 고객별 물량을 계산한 결과가 아님
- [산업 전파 경로 점검](docs/research/supply_chain/semiconductor_industry_transmission_routes.md)(2026-10-05): 여러 제품과 제조 기능, 전력 규제·국가 간 협력·항공우주의 대표 관계와 연결 공백. 세계 전체 거래·규제 효력 또는 충격 크기를 확인한 결과가 아님
- [독립 목적 관리](docs/research/supply_chain/research_convergence_review.md): 실제 초기·중간·최종 검토와 수정 내역. 산업 간 구조 점검을 바탕으로 서버 DDR5의 Intel 인증·Dell 전시 탑재 사례를 고객·상품 카드로 구체화
- 첫 수집 실험: [경제적 목적](docs/research/supply_chain/decision_purpose.md)과 [OpenAI–CoreWeave 사례 검토](docs/research/supply_chain/first_case_review.md) — 고객 약정과 실제 집행의 공개 연결 범위를 구분
- 후속: H1 최소 검증 후 H2 Bottleneck Migration
- 보류: H3 Product-Mix Opportunity Cost는 공개정보가 충분할 때까지 `KNOWN_UNKNOWN` 중심 framework로 유지

## Architecture

특정 agent runtime을 필수로 두지 않는다. Codex-native capability, Hermes adapter 또는 다른 compatible runtime은 필요성과 측정 가능한 가치가 확인될 때 선택한다.

```text
Agent Execution Harness (future capability)
→ optional orchestration and logical domain roles
→ adapters
→ Evidence Governance Harness (implemented deterministic core)
→ Evidence → Graph → Audit → Decision Memo
```

AI는 discovery·semantic interpretation·candidate linking·contradiction search를 지원한다. Schema validation, deduplication, date alignment, state transition, trace, replay는 deterministic code가 담당한다. Strong Inference, causal validity, hypothesis verdict와 최종 business framing은 사람이 승인한다.

## Canonical documentation

- `AGENTS.md`: concise navigation, invariants, current phase와 validation commands
- `README.md`: human-facing overview와 approved repository state
- `00_MASTER/00_CODEX_MASTER_INSTRUCTION.md`: economic/research contract와 core beliefs
- `00_MASTER/02_ARCHITECTURE_DECISIONS.md`: ADR와 superseded decisions
- `docs/agent_architecture.md`: role/context/two-Harness/eval architecture 상세
- `docs/implementation_plan.md`: 실제 구현된 baseline과 next approved gate
- `docs/exec-plans/`: active task와 completed/historical task 기록
- `docs/research/supply_chain/`: 공급망 관계, 과거 저장소 검토, 목적별 무료 수집 계획
- `data/research/semiconductor_supply_chain/2026-10-03/`: 지도·지표·API 연구 후보와 공개판 manifest
- `scripts/collect_customer_commitment.py`: 단일 고객 약정 원문 수집·재검사; 정식 Evidence 자동 승격 없음
- `data/research/customer_commitments/coreweave_openai_20250923/`: 단일 사건의 수집 결과·원문·접근 실패 이력

작업자는 `AGENTS.md`에서 시작해 progressive disclosure로 필요한 문서만 읽는다.

## Stable validation commands

```powershell
python -m unittest -v
python -m src.pipeline --workspace . --scenario data/raw/scenarios/hbm4_vertical_slice.json
python -m src.pipeline --workspace . --scenario data/raw/scenarios/hbm4_temporal_update_2026.json
python scripts/validate_supply_chain_research.py
```

승인 전에 실행된 H1 실험 코드·데이터·출력은 현재 baseline에서 제거했다. 해당 시도는 `docs/exec-plans/completed/interrupted_h1_experiment.md`와 Git 이력에만 보존되며 H1 finding으로 인용할 수 없다. 현재 active plan은 `docs/exec-plans/active/h1_empirical_validation_design.md`다.

## Baseline preservation

원본 v2 ZIP은 `data/raw/baseline/`에 immutable baseline과 SHA-256 manifest로 보존한다. ZIP 내부 README의 `v1` 표기와 외부 패키지의 `v2` 명칭 불일치는 `docs/research_validation_gaps.md`에 기록되어 있다. 현재 README 갱신은 baseline을 덮어쓰지 않는다.

전용 LLM/Fine-tuning/Vector DB/Graph DB/Dashboard는 현재 범위가 아니다.

공급망 연구 자료는 `RESEARCH_CANDIDATE_NOT_GOVERNED_EVIDENCE`다. 2026-10-03 지도 스냅샷은 69개 주체·58개 관계·7개 시설·32개 후보 지표와 14개 우선 수집 지표를 포함하며, 공식 좌표 2곳만 GeoJSON으로 제공한다. 이후의 상품·거시·산업 경로 자료는 날짜별 보완층으로 참조하며 중복 주체·관계를 이 숫자에 합산하지 않는다. 단일 사건 수집 경로와 지속 수집·예측 검증은 구분하며 이 자료가 H1 Track 또는 승인된 Evidence에 자동 편입되지는 않는다.
