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
- 다음 task: H1 Demand Signal Quality empirical validation 설계만 수행
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

작업자는 `AGENTS.md`에서 시작해 progressive disclosure로 필요한 문서만 읽는다.

## Stable validation commands

```powershell
python -m unittest -v
python -m src.pipeline --workspace . --scenario data/raw/scenarios/hbm4_vertical_slice.json
python -m src.pipeline --workspace . --scenario data/raw/scenarios/hbm4_temporal_update_2026.json
```

승인 전에 실행된 H1 실험 코드·데이터·출력은 현재 baseline에서 제거했다. 해당 시도는 `docs/exec-plans/completed/interrupted_h1_experiment.md`와 Git 이력에만 보존되며 H1 finding으로 인용할 수 없다. 현재 active plan은 `docs/exec-plans/active/h1_empirical_validation_design.md`다.

## Baseline preservation

원본 v2 ZIP은 `data/raw/baseline/`에 immutable baseline과 SHA-256 manifest로 보존한다. ZIP 내부 README의 `v1` 표기와 외부 패키지의 `v2` 명칭 불일치는 `docs/research_validation_gaps.md`에 기록되어 있다. 현재 README 갱신은 baseline을 덮어쓰지 않는다.

전용 LLM/Fine-tuning/Vector DB/Graph DB/Dashboard는 현재 범위가 아니다.
