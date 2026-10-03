# Memory Market Decision Intelligence

공개정보를 이용해 반도체·AI-memory 신호가 수요·공급 전파경로의 어디에 있는지 구분하고, 어떤 신호가 실제 수요 또는 제약 가시성을 개선하는지 검증해 business-decision context로 번역하는 프로젝트다.

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

채용·경험기술서 자료는 실제 분석과 검증에서 파생되는 downstream evidence이며 프로젝트의 1차 목적이 아니다.

## Current phase

- 완료: HBM4 Evidence → Graph → Audit → Memo Vertical Slice
- 완료: Evidence별 Human Review와 2025→2026 Temporal Update
- 완료: capability-first, runtime-agnostic architecture reframing과 baseline cleanup
- H1: Gates 1–5, measurement contract, 24-Track registry와 수집·Gate 6 검토 패키지 준비
- H1 검증 대기: 사람의 Gate 6 dataset freeze 및 Event 검토. 지표·lead/lag·실현율·verdict는 미계산
- 연구 자료 추가: [반도체·AI·데이터센터·전력·금융 공급망](docs/research/supply_chain/README.md) — 기존 세 저장소의 방법론 검토와 2026-10-03 후보 자료
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

공급망 연구 자료는 `RESEARCH_CANDIDATE_NOT_GOVERNED_EVIDENCE`다. 69개 주체·58개 관계·7개 시설·32개 후보 지표와 14개 우선 수집 지표를 포함하며, 공식 좌표 2곳만 GeoJSON으로 제공한다. 단일 사건 수집 경로와 지속 수집·예측 검증은 구분하며 이 자료가 H1 Track 또는 승인된 Evidence에 자동 편입되지는 않는다.
