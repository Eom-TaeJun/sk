# H1 Primary-Source Collection Runbook

## Purpose

Use this procedure to add or revise official-source candidates for the frozen H1 corpus. It standardizes repeatable collection work; it does not encode an H1 result or approve a candidate for empirical use.

## Collector pass

1. Start from one frozen `track_id`; do not add or remove Tracks based on known outcomes.
2. Search regulatory filings, official earnings material, official product/platform releases, and official counterparties.
3. Search both supporting stages and explicit delay, failure, reduced-scope, constraint, revision, or cancellation wording.
4. Preserve short original excerpts and precise locators. Split sample, qualification, production, supply, and outcome statements into Atomic Events.
5. Use `EXPLICIT_NEGATIVE_OR_DELAY` only when the official wording directly supports it. Otherwise record `NOT_OBSERVED_PUBLICLY`; silence is not success.
6. Keep customer identity, volume, price, supplier share, utilization, yield, margin, and capacity allocation missing unless the primary Source directly discloses them.

## Historical-time contract

- Store `event_at`, `published_at`, `available_at`, and `accessed_at` separately.
- Preserve an official timestamp when the Source provides it.
- For a date-only official Source, set `published_at` to publisher-local 00:00 and `available_at` to publisher-local 00:00 on the next calendar day.
- A later retrospective Source keeps its later `available_at`; never backdate public knowledge.
- A revised Source receives a new revision and availability timestamp. Do not overwrite the earlier record.

## Origin and scope contract

- A press page, PDF mirror, and joint-release mirror for the same disclosure share one `origin_group`.
- Reusing a company-level CAPEX Source across platform Tracks does not increase independence.
- Do not join company CAPEX to a named SKU without an explicit approved bridge.
- Do not join a named platform to an HBM supplier, or GA to utilization/volume, without direct evidence.

## Stage contract

- `HBM_SAMPLE` requires explicit sample or sampling wording.
- Performance evaluation is not automatically qualification.
- Qualification `PLANNED`, `UNDERWAY`, `FINAL_STAGE`, and `COMPLETE` remain separate.
- Production readiness, planning, start, and ramp remain `CONTEXT / PRODUCTION_STAGE_CONTEXT`.
- Current customer supply or commercial shipment requires direct present/observed wording for O1.
- Development, future plans, “industry-first,” and an installed rack alone cannot be promoted to a stronger stage.

## Adversarial verifier pass

The verifier must be different from the collector and challenge source primacy, timestamp, scope, forward-looking wording, stage inflation, same-origin duplication, and outcome interpretation. Every unresolved issue links to a `HOLD` Event and a human Gate 6 question.

## Deterministic build and replay

Run from the repository root with the configured Python runtime:

```powershell
python -m src.measurement.corpus --workspace . --input data/h1/corpus/collection_input.json
python -m unittest -v tests.test_h1_full_corpus
```

The build must preserve the frozen registry and immutable Pilot hashes, verify all Source archives and SHA-256 values, cover exactly 24 Tracks, and keep `gate6_frozen=false` and `empirical_h1_calculated=false`.

## Stop boundary

Collection completion authorizes only a human Gate 6 corpus-readiness review. Do not calculate lead/lag, realization rates, signal ranking, or an H1 verdict from this procedure.
