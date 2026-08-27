# 권장 프로젝트 설정

## Codex working rules
- Plan-first: ON
- Human approval before large implementation
- Minimal MVP first
- Tests before feature expansion
- All market claims require source_id
- All Strong Inference requires review
- Preserve conflicts, do not auto-resolve
- Log human overrides
- No invented SK hynix internal values
- No hidden assumptions

## Context priority
HIGH:
AGENTS.md
00_MASTER
02_SCHEMAS

MEDIUM:
task-relevant 01_CANONICAL_SOURCES only
docs/agent_architecture.md
03_TEMPLATES
generated docs/logs

LOW:
UI/dashboard
extra frameworks

## Folder convention for implementation
docs/
docs/exec-plans/active/
docs/exec-plans/completed/
data/raw/
data/evidence/
data/signals/
data/graph/
src/retrieval/
src/graph/
src/adapters/
src/core/                 # Evidence Governance Harness
src/audit/
src/memo/
evals/agent/              # future interface only; create when eval implementation is approved
tests/
logs/
application_evidence/

## Downstream application evidence files
application_evidence/project_fact_sheet.md
application_evidence/decision_change_log.md
application_evidence/before_after.md
application_evidence/recruiter_signal_map.md

이 파일들은 실제 run/test/human decision에서 확인된 사실만 기록한다. 프로젝트 목적이나 Architecture를 먼저 결정하지 않는다.

## Runtime policy

- Orchestration은 capability이며 특정 framework를 필수로 두지 않음
- logical domain role은 task에 필요한 것만 활성화
- Evidence Governance Harness와 future Agent Execution Harness를 구분
- 모델에는 smallest-sufficient task context만 제공
