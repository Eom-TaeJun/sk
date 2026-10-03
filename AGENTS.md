# Repository Agent Map

## Objective

Build a traceable decision-intelligence workflow that uses public information to distinguish semiconductor and AI-memory signals by their position in the demand/supply transmission chain, tests which signals improve demand or constraint visibility, and translates validated evidence into business-decision context. Recruiting evidence is a downstream record of real project work.

## Current phase

- Vertical Slice and 2025→2026 Temporal Update: implemented and preserved
- Architecture: whole-project decision domains frozen; runtime-agnostic and capability-first
- H1 Gates 1–5: human-approved and frozen as separate product-commercialization (H1-P) and customer/platform-realization (H1-C) strata
- H1 measurement contract, deterministic validation, 24-Track registry and 4-Track real-data pilot: implemented and preserved
- H1-P now distinguishes customer/commercial acceptance from supply readiness; production stage is context only
- H1 full primary-source corpus and Gate 6 readiness package: prepared; human Gate 6 review/freeze remains pending
- Supply-chain research intake (2026-10-03): candidate-only map, metric and free-access plans; not governed Evidence or an H1 dataset amendment
- Bounded customer-commitment collection: purpose-first single-case capture/replay, with source provenance and separate failed attempts; not continuous monitoring or empirical validation
- H1 metrics, lead/lag, realization rates, outcome analysis and verdict: not yet approved; require Gate 6 dataset freeze
- H2: only after a credible H1 minimum pipeline
- H3: conceptual/`KNOWN_UNKNOWN` until public evidence is sufficient
- Interrupted H1 implementation: removed from the current baseline and preserved only in Git history and its completed execution-plan note

Do not treat deleted, historical, or interrupted H1 experiment artifacts as approved findings.

## Read only what the task needs

- Project/economic contract: `00_MASTER/00_CODEX_MASTER_INSTRUCTION.md`
- Architecture decisions and supersessions: `00_MASTER/02_ARCHITECTURE_DECISIONS.md`
- Model/program/runtime allocation: `00_MASTER/03_WHERE_TO_USE_WHAT.md`
- Detailed agent architecture and future eval interface: `docs/agent_architecture.md`
- Whole-project decision domains, admission gate and module activation: `docs/decision_architecture.md`
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
- Supply-chain research intake and legacy reference review: `docs/research/supply_chain/README.md`
- Public candidate data and hashes: `data/research/semiconductor_supply_chain/2026-10-03/manifest.json`
- Economic question and single-case boundaries: `docs/research/supply_chain/decision_purpose.md`
- Customer-commitment collector and case review: `scripts/collect_customer_commitment.py`, `docs/research/supply_chain/first_case_review.md`

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
python scripts/validate_supply_chain_research.py
```

No Agent Evaluation runner is implemented yet. Do not fabricate eval results or document a command that does not exist.

H1 remains confined to primary-source corpus collection/review across the frozen 24-Track registry until a human Gate 6 dataset freeze. Do not calculate H1 metrics, lead/lag, realization rate or verdict before that freeze. Without explicit approval, do not start H2/H3, add a Decision Engine, Agent Execution Harness/runtime, dashboards or databases.

The supply-chain research intake is an authorized documentation/data integration, not approval of an empirical module. Preserve raw stage descriptions, review flags, dated source history and unknowns. Source review is not human Evidence approval. Do not import these records into H1 automatically or copy private legacy source code, personal materials, credentials or local operational paths into public data. Its standalone validator checks package integrity, not source truth or predictive validity.

The bounded customer-commitment collector preserves source bytes, locators, publication/event dates and candidate-only records separately from H1. SEC access failures and issuer-hosted mirrors are different acquisition outcomes. Preserve actual retrieval URLs and source roles; never label an issuer mirror as verified SEC-original bytes. Single-case retrieval and replay do not establish leadingness, realization rates or customer-specific equipment/power allocation.

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
