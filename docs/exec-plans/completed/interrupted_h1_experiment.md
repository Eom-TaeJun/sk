# Interrupted H1 Experiment — Historical Note

## Status

`STOPPED / NOT APPROVED`

An H1 backtest engine, event/source dataset, generated run outputs, H1-only schemas and execution log were created before the empirical design gate was approved. The attempt ran ahead of the repository's human-steered milestone order and was stopped during baseline consolidation.

No output from that experiment is an approved H1 finding. Its case selection, outcome contract, cutoff rules and final interpretation did not receive the required human approval.

## Baseline cleanup

The current baseline removes:

- `src/backtest/`
- `data/backtest/`
- `data/raw/backtest_sources/`
- H1-only backtest schemas
- the H1 execution log

The removed state remains recoverable in Git history at merge baseline `19dc248` and its parent `0a90bdc`.

## Retained lesson

Empirical execution must not precede approval of the question, matched cases, source hierarchy, event-time cutoff, outcome definition, rejection conditions and human verdict boundary. The next task is design-only.
