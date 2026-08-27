# H1 Pre-registered Track Registry and Real-data Ingestion Pilot — Execution Note

## Scope and stop boundary

This task tested whether the frozen H1 measurement contract can ingest a small set of real primary disclosures. It did not run empirical H1, calculate lead/lag or signal performance, or produce an H1-P/H1-C verdict.

Sequence preserved:

`outcome-neutral Track universe → registry freeze → primary-source collection → semantic validation → hashed pilot dataset`

Outcome analysis was not performed.

## Registry population

- Canonical candidate registry: 24 Tracks
- Product commercialization: 10
- Customer/platform realization: 14
- Status: 24 `PRE_REGISTERED`, 0 `HOLD`, 0 `EXCLUDED`
- Registry hash: `A3BFDBDD8178E203C63635824985888C76DA10818D64B3E869EC5E30E4A26BB1`
- Freeze hash: `8D973F950CDFB9636CACCB7FE00E0565FB7BECEE2AB043AE1F3224EA8B8B43FB`
- Outcome/performance fields: absent by contract and test

The registry used the feasibility-manifest IDs. No new Track was invented.

## Pilot population

Exactly four frozen Tracks were used:

- `P02-SKH-HBM3E`
- `P04-MU-HBM3E`
- `C02-AZ-H200`
- `C04-GCP-H200`

The pilot contains 13 primary Sources and 15 Atomic Events. Every Source has a publisher, URL, local archived excerpt, locator, publication/availability/access timestamps, origin group, revision ID, and verified SHA-256. The Source registry hash is `C09C9B152B100D593DD6F5B6FDBA61F81319FD410E79BE086EE33B3459B6738B`; the Event dataset hash is `1B68F3C32F684380C1B3CE7671250B64E7376CAAA2A6E4683F1FAAF6C2CFD5A3`.

Ingestion disposition:

- 11 `ACCEPTED` candidates with `review_status=UNREVIEWED`
- 4 `HOLD` candidates with ambiguity and required human judgment
- 0 `REJECTED` ingestion records

`ACCEPTED` means the candidate mapping passes the deterministic contract. It is not human approval and is not empirical inclusion.

## Contract contact with real language

Existing rules were sufficient for:

- sample/evaluation remaining distinct from qualification and commercialization;
- qualification `UNDERWAY` and `FINAL_STAGE` remaining distinct from `COMPLETE`;
- planned preview, preview, and GA remaining separate;
- company CAPEX remaining broad context rather than named-platform attribution;
- H1-P and H1-C records remaining separate, preventing an H200 generation label from proving a supplier-to-CSP bridge.

Two real wording patterns exposed deterministic weaknesses:

1. Production or ramp wording alone could fit `ORDER_ADJACENT_SUPPLY_COMMITMENT` because that class previously lacked affirmative commitment terms.
2. “for supply to a customer” could fit current O1 even when followed by a future qualifier such as “from late March.”

Each weakness was first reduced to a synthetic regression fixture. The smallest rule changes then required affirmative supply-commitment wording and rejected future-dated customer supply as current O1.

One schema gap was corrected: `date_precision` describes publication/availability precision, while a retrospective statement can have a less precise event date. Optional `event_date_precision` now preserves the distinction without changing existing fixtures.

## Remaining ambiguities

- SK hynix customer supply after the March 19, 2024 announcement is `NOT_OBSERVED_PUBLICLY` within this pilot; it is not classified as failure.
- Production readiness/start has no dedicated class in the frozen minimum and remains HOLD rather than being forced into a commitment or outcome.
- Micron’s forward H200 integration statement remains HOLD for empirical admission and cannot establish Micron supply to Azure or Google Cloud.
- Google Cloud’s annual roundup is a living page; the archived R1 excerpt and hash must not be overwritten by later edits.
- GA establishes availability, not utilization, installed capacity, commercial demand volume, or a named memory supplier.
- CAPEX disclosures remain company-level upstream context only.

## Human and AI boundary

- AI-assisted work: candidate source discovery, atomic extraction/classification proposals, deterministic validation, stress-case reduction, code/test drafting.
- Human review required: final admissibility of held events, production-stage taxonomy, design-in interpretation, origin-group adequacy, and any later empirical snapshot or H1 verdict.

No candidate was marked human-approved in this task.

## Validation record

The task added real-pilot replay, Source archive/hash, provenance mismatch, registry neutrality/freeze, HOLD, CAPEX scope, stress-log shape, and no-H1-output tests plus three minimum measurement-contract regressions.

- `python -m unittest -v`: 51 tests passed
- `python -m src.pipeline --workspace . --scenario data/raw/scenarios/hbm4_vertical_slice.json`: exit code 0
- `python -m src.pipeline --workspace . --scenario data/raw/scenarios/hbm4_temporal_update_2026.json`: exit code 0

## Stop

Full registry collection, empirical snapshots, outcome comparisons, H1 metrics/verdicts, H2/H3, agent runtime, Hermes, dashboards, and databases remain outside this task.
