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
00_MASTER
01_CANONICAL_SOURCES
02_SCHEMAS

MEDIUM:
03_TEMPLATES
generated docs/logs

LOW:
UI/dashboard
extra frameworks

## Folder convention for implementation
docs/
data/raw/
data/evidence/
data/signals/
data/graph/
data/backtest/
src/retrieval/
src/graph/
src/agents/
src/harness/
src/audit/
src/memo/
tests/
logs/
application_evidence/

## Mandatory generated application files
application_evidence/project_fact_sheet.md
application_evidence/decision_change_log.md
application_evidence/before_after.md
application_evidence/recruiter_signal_map.md
