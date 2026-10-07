# Repository Agent Map

## Objective and current task

Build an SK hynix-centered supply-chain and market knowledge base for learning the sales, marketing, product-planning and new-product-commercialization roles described in the 2026 second-half recruitment materials. Explain who needs which memory product, why, through which specification/adoption/purchase process and on what timetable. Application claims must describe actual work and validation.

The current priority is purpose-first free-data observability: define the question, relationship, dataset/fields, units, dates, joins and reuse conditions before collection. Keep the requested links across AI, power, data centers, materials, finance, policy and aerospace. Activate collection only for a specific relationship or comparison question; do not force customer-card convergence now.

- Current collection scope and exactly one next economic task are owned by [indicator_collection_purpose.md](docs/research/supply_chain/indicator_collection_purpose.md). The next task is the KOSIS production/shipment/inventory measurement contract, not bulk API collection.
- Current access receipts belong to [api_signal_feasibility.md](docs/research/supply_chain/api_signal_feasibility.md). Dated JSON next-task recommendations are historical, not new execution instructions.
- DDR5 customer-card convergence, the earlier Comtrade/Eurostat call pilot and recurring collectors remain deferred.
- Preserved H1 contracts, implemented code, historical research and future architecture are routed through [reference_index.md](docs/reference_index.md). Their existence does not make them the current task.

## Read only what the task needs

| Task | Entry point |
| --- | --- |
| Purpose, job roles, product/customer questions | `docs/research/supply_chain/sk_hynix_commercial_role_context.md` |
| Indicator purpose and collection scope | `docs/research/supply_chain/indicator_collection_purpose.md` |
| Exact API access and measurement contracts | `docs/research/supply_chain/api_signal_feasibility.md`, `data/research/api_signal_feasibility/2026-10-05/collection_index.json` |
| Industry, product, AI and policy routes | `docs/research/supply_chain/README.md` |
| Evidence governance, architecture, preserved H1 and historical approvals | `docs/reference_index.md` |
| Core code or regression repair | relevant modules in `src/`, `scripts/`, `tests/`, and schemas in `02_SCHEMAS/` |
| Actual project/application facts | `application_evidence/` |

Do not load all Canonical Sources or copy the Master Instruction into context by default. Select the smallest sufficient files. Keep current instructions in their owner document; link to history instead of repeating it in every entry point.

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

AI may discover, retrieve, extract, classify candidates, link entities, search for contradictions and propose hypotheses. Humans approve strong interpretation, causal validity, final H1/H2 verdicts and business recommendations. Use models for semantic judgment and deterministic code for checks, joins, aggregation, state transitions, trace and replay.

## Preserved approvals and collection boundaries

H1 Gates 1–5 remain human-approved and frozen as separate H1-P commercialization and H1-C platform-realization strata. The measurement contract, 24-Track registry, 4-Track pilot, full primary-source corpus and Gate 6 readiness package are prepared and preserved. Human Gate 6 review/freeze remains pending. Do not calculate H1 metrics, lead/lag, realization rates, outcome analysis or verdict before that freeze. Until then, H1 work is confined to source/corpus review under its frozen contract when assigned; it is not the current collection task.

Without explicit approval, do not start H2/H3 or implement a Decision Engine, Agent Execution Harness/runtime, dashboards or databases. Deleted/interrupted H1 artifacts are historical and cannot be used as findings. H3 remains conceptual/`KNOWN_UNKNOWN` until evidence is sufficient.

Supply-chain research is candidate-only and does not amend H1 or constitute governed Evidence. Preserve stage_raw, unknowns, dates, source roles and hashes. Do not import candidates into H1 automatically or copy private legacy code, personal materials, credentials or local operational paths into public data. A main merge is repository integration, not human Evidence approval.

The bounded customer-commitment collector is a single-case capture/replay. SEC failures and issuer mirrors are different acquisition outcomes; retain actual URLs/source roles and never label a mirror as verified SEC-original bytes. Single-case replay does not establish leadingness or customer equipment/power allocation.

## Purpose and convergence review

Assign an independent purpose reviewer separately from research and integration, using available subagents when useful. This does not imply that Hermes or continuous monitoring is installed. Record reviews in `docs/research/supply_chain/research_convergence_review.md`.

- Start: state the question, scope, required evidence and completion criteria.
- During work: expand only to resolve a relevant definition, alternative explanation, relationship or timing gap; defer unrelated branches.
- Before handoff: check purpose and scope, preserve unknowns, name exactly one next task and use `CONTINUE`, `REWORK` or `DEFER` with observed reasons.

Role counts and agreement are not quality scores or Evidence approvals. Scope cleanup must reduce duplicate instructions and execution work, not erase source history or requested industries.

For structural cleanup, trace the requested output through entry points to actual consumers before adding or removing code, configuration, schemas or dependencies. A passing test proves tested behavior, not that an abstraction is necessary. Review correctness and necessity separately; prefer a small removal with output comparison over a new cleanup framework. Dated methods and findings belong to [structure_cleanup.md](docs/reviews/2026-10-07/structure_cleanup.md); recheck applicable sources when the environment or task changes.

Concise reporting must not shorten authorized investigation or hand back steps the agent can perform. Match completion claims to fresh checks appropriate to the changed surface; a rejection test must fail for the intended violation, not an unrelated command or import error.

## Stable validation commands

Run from the repository root and select checks appropriate to the changed surface:

```powershell
python -m unittest -v
python -m src.pipeline --workspace . --scenario data/raw/scenarios/hbm4_vertical_slice.json
python -m src.pipeline --workspace . --scenario data/raw/scenarios/hbm4_temporal_update_2026.json
python scripts/validate_supply_chain_research.py
python scripts/validate_current_research.py
```

The first research validator checks the 2026-10-03 intake; the second checks the fixed 2026-10-05 API/purpose packages offline. Neither verifies current remote access, economic truth, predictive validity or human approval. No Agent Evaluation runner exists; do not fabricate eval results or commands.

Corpus/Gate 6 tests build in copied temporary workspaces. If restricted Windows Temp is unavailable, point Python `tempfile.tempdir` to writable scratch space before discovery; do not build into the source checkout.

## Definition of done

- The requested problem, scope and current document owners are explicit.
- Only relevant files were read or changed; duplicated instructions were replaced with references.
- Source trace, original data, approved contracts and history remain intact.
- Unknowns remain `KNOWN_UNKNOWN`/`TO_VERIFY`; AI review and human approval are distinct.
- Appropriate validation passes; real failures become minimal regression cases.
- The handoff states the actual change, limitations and exactly one next task.
