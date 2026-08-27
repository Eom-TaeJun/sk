# Repository Agent Map

## Objective

Build a traceable decision-intelligence workflow that uses public information to distinguish semiconductor and AI-memory signals by their position in the demand/supply transmission chain, tests which signals improve demand or constraint visibility, and translates validated evidence into business-decision context. Recruiting evidence is a downstream record of real project work.

## Current phase

- Vertical Slice and 2025→2026 Temporal Update: implemented and preserved
- Architecture: runtime-agnostic, capability-first
- Next approved task: H1 Demand Signal Quality empirical validation design only
- H2: only after a credible H1 minimum pipeline
- H3: conceptual/`KNOWN_UNKNOWN` until public evidence is sufficient
- Interrupted H1 implementation: removed from the current baseline and preserved only in Git history and its completed execution-plan note

Do not treat deleted, historical, or interrupted H1 experiment artifacts as approved findings.

## Read only what the task needs

- Project/economic contract: `00_MASTER/00_CODEX_MASTER_INSTRUCTION.md`
- Architecture decisions and supersessions: `00_MASTER/02_ARCHITECTURE_DECISIONS.md`
- Model/program/runtime allocation: `00_MASTER/03_WHERE_TO_USE_WHAT.md`
- Detailed agent architecture and future eval interface: `docs/agent_architecture.md`
- Implemented Vertical Slice plan: `docs/implementation_plan.md`
- Active/completed task records: `docs/exec-plans/`
- Source limitations: `docs/research_validation_gaps.md`
- Evidence interpretation: `docs/source_understanding.md`
- Schemas: `02_SCHEMAS/`
- Core code: `src/core/`, `src/pipeline.py`
- Retrieval/Graph/Audit/Memo: `src/retrieval/`, `src/graph/`, `src/audit/`, `src/memo/`
- Runtime boundary: `src/adapters/`
- Software tests: `tests/`
- Historical project facts: `application_evidence/`

Do not load all Canonical Sources or copy the Master Instruction into task context by default. Select the smallest sufficient files for the current question.

## Invariants

1. Source ID, original excerpt, locator, date and content hash must remain traceable.
2. Memo facts must trace to Evidence ID → Source ID → original excerpt → locator.
3. Sample, qualification, design-in, LTA, mass production and commercial shipment are distinct stages.
4. Company claims and external estimates do not auto-promote to FACT.
5. Strong Inference requires explicit human review; hypotheses do not promote.
6. Contradictions and prior temporal evidence are preserved, not silently overwritten.
7. Agent/runtime output cannot bypass the deterministic Evidence Governance Harness.
8. No public-data analysis may invent customer volume, price, share, yield, cost or CAPA.
9. Do not imply causality from graph structure or temporal ordering alone.
10. A specific runtime, multi-agent topology, LLM, Vector DB or Graph DB is never mandatory without demonstrated value.

## Responsibility boundary

AI may discover, retrieve, extract, classify candidates, link entities, search for contradictions and propose hypotheses. Humans approve strong interpretation, causal validity, final H1/H2 verdicts and business recommendations.

Use models for semantic judgment. Use deterministic code for filtering, deduplication, schema/date/unit checks, joins, lag construction, aggregation, state transitions, trace and replay.

## Stable validation commands

Run from the repository root:

```powershell
python -m unittest -v
python -m src.pipeline --workspace . --scenario data/raw/scenarios/hbm4_vertical_slice.json
python -m src.pipeline --workspace . --scenario data/raw/scenarios/hbm4_temporal_update_2026.json
```

No Agent Evaluation runner is implemented yet. Do not fabricate eval results or document a command that does not exist.

Without explicit approval, do not design or run H1, start H2/H3, add an Agent Execution Harness/runtime, or add dashboards/databases.

## Definition of done for a Codex task

- The requested decision problem and scope are explicit.
- Relevant detailed docs were read; unrelated context was not duplicated.
- Changes preserve the invariants and prior evidence/history.
- Source-backed claims have complete trace; limitations use `KNOWN_UNKNOWN` or `TO_VERIFY`.
- Software tests appropriate to the changed surface pass.
- Failures are captured as minimal future regression cases instead of silently patched.
- AI actions and human approvals remain distinguishable.
- Only requested artifacts are changed; prohibited expansion is not performed.
- The handoff states what changed, what remains unresolved and exactly one next task.
