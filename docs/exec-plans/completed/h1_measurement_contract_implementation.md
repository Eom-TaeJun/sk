# H1 Measurement Contract and Deterministic Validation — Execution Note

## Status and scope

`COMPLETED — SYNTHETIC CONTRACT VALIDATION ONLY`

This task implemented the frozen H1 measurement contract without collecting historical sources, constructing an empirical dataset, calculating signal performance, or issuing an H1 verdict. The validated Evidence Governance core was left intact; the new code is isolated under `src/measurement/`.

## Implemented

- Separate Track contracts for `PRODUCT_COMMERCIALIZATION_TRACK` (H1-P) and `CUSTOMER_PLATFORM_REALIZATION_TRACK` (H1-C).
- Atomic Event contracts with mandatory analytical role, transmission layer, decision question, historical timestamps, scope, provenance, revision, censoring, and review fields.
- JSON Schemas for Track, Event, and immutable snapshot manifests.
- Deterministic validators for stage semantics, stratum-specific signal/outcome classes, historical cutoff eligibility, conservative date-only availability, revision chains, origin independence, scope joins, and H1-P/H1-C pooling.
- Observation-window assessment for 6, 12, and 18 months. Right-censored signals are marked ineligible for failure/no-realization denominators.
- Immutable file-backed snapshot manifests with inclusion IDs, source IDs, cutoff, freeze, horizon, exclusion/HOLD reasons, observation assessments, and a canonical SHA-256 hash.
- Twelve synthetic Events across four synthetic Tracks plus three deliberately invalid semantic records. No fixture represents a real company, product, platform, or empirical finding.

## Machine-enforced rules

- `data_role` is singular and mandatory: `SIGNAL`, `OUTCOME`, or `CONTEXT`.
- H1-P uses supplier-side `O1_COMMERCIAL_REALIZATION`; H1-C uses `P1_PLATFORM_OPERATIONAL_REALIZATION`; mixed-stratum batches fail.
- Sample is not qualification completion; `UNDERWAY`, `PLANNED`, and `FINAL_STAGE` wording cannot become `COMPLETE`.
- Platform `PLANNED` or `PREVIEW` cannot become operational realization.
- Product O1 requires explicit current shipment/customer-supply wording; plan/readiness wording is rejected.
- An Event is historically eligible only when `available_at <= cutoff_at`.
- Date-only official-source fallback begins on the next calendar day in publisher local time and remains labelled as fallback.
- A revision is a new immutable Event with a new revision ID, later availability, stable Source/origin/Track, and an explicit supersession link. Cutoff-specific snapshots select the revision available then.
- Independent support is counted by explicit `origin_group`, not URL or Source count.
- Cross-Track or incompatible narrow-scope joins fail; broad-to-narrow joins require an explicit partial-scope choice.
- Raw-material and supply-constraint transmission layers cannot enter the frozen H1 contract.
- Non-approved Events and non-active Tracks require a reasoned `HOLD` or `EXCLUDE` manifest decision before snapshot construction.

## Implementation decisions and corrections

- The existing Core Harness was not generalized or rewritten. A separate standard-library measurement module keeps the empirical contract from changing the validated Vertical Slice behavior.
- `right_censored` is computed for each snapshot from signal availability, dataset freeze, and selected horizon. The raw fixture declaration is nullable because one Event can be fully observed at 6 months and right-censored at 12 or 18 months.
- Historical snapshots contain the latest revision available at their cutoff; the Event registry retains both old and new records. Later wording therefore changes later snapshots without rewriting earlier knowledge.
- Meaning checks are intentionally conservative phrase/rule gates. Passing them does not replace human review of source semantics.

## Human-controlled decisions

- Final Track admissibility and case boundaries.
- Whether an extracted statement truly supports the proposed stage and source scope.
- Approval of `OTHER_APPROVED_PROXY`, partial broad-to-narrow scope use, and exclusion/HOLD reasons.
- Correctness of manually assigned `origin_group` metadata; automatic semantic origin detection was not built.
- Candidate/outcome admissibility, causal interpretation, empirical sufficiency, and any H1 verdict.

## Validation performed

- `python -m unittest -v`: 36 tests passed, including 18 new measurement-contract tests and all 18 preserved Vertical Slice/Temporal Update tests.
- `python -m src.pipeline --workspace . --scenario data/raw/scenarios/hbm4_vertical_slice.json`: exit code 0.
- `python -m src.pipeline --workspace . --scenario data/raw/scenarios/hbm4_temporal_update_2026.json`: exit code 0.
- Python compilation and JSON parsing checks passed for the new code, schemas, and fixture.

## Not implemented

No historical H1 Source collection, candidate-track manifest, empirical H1 execution, performance metric, lead/lag calculation, realization/failure rate, statistical model, H1 verdict, H2/H3 work, runtime/agent orchestration, dashboard, Vector DB, or Graph DB was added.
