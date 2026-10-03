# Supply-chain research integration — completed

Date: 2026-10-03. Scope: review the three user-named legacy repositories as references and organize the current semiconductor-centered supply-chain research in `Eom-TaeJun/sk`.

## Result

- Added [research navigation](../../research/supply_chain/README.md), [legacy review](../../research/supply_chain/legacy_reference_review.md) and [purpose-specific collection plan](../../research/supply_chain/collection_plan.md).
- Added six public research JSON exports, two verified facility points in GeoJSON, and a hash manifest under `data/research/semiconductor_supply_chain/2026-10-03/`.
- Preserved 69 actors, 58 differently typed relations, seven facilities, six representative paths, seven capture specifications, 32 candidate metrics and 14 first-collection metrics.
- Distinguished 17 relations checked in the v3 update from 41 carried forward; retained prior evidence history. Corrected Coherent's current amount note to match its completed gross cash equity transaction.
- Removed user-specific key possession/activation/test status and local operational paths from the public export. Legacy source code, personal materials and downloaded report/workbook bodies were not imported.
- Added an offline package validator and six regression tests. This is not an API collector, H1 ingestion route, source-truth validator, prediction test or human approval.
- Added `.gitattributes` to preserve exact bytes in source archives and hashed research data on Windows. Restored 51 local checkout newline conversions from the unchanged Git blobs; source text and approved baseline hashes were not rewritten.
- Updated README/AGENTS navigation and the prepared Gate 6 review status without selecting or approving a human Gate 6 decision.

## Validation

| Check | Result |
| --- | --- |
| `python scripts/validate_supply_chain_research.py` | PASS; eight artifacts, hashes, IDs, references, candidate flags and coordinates |
| `python -m unittest -q` | PASS; 90 tests, including six new regression tests |
| `python -m src.pipeline --workspace . --scenario data/raw/scenarios/hbm4_vertical_slice.json` | PASS |
| `python -m src.pipeline --workspace . --scenario data/raw/scenarios/hbm4_temporal_update_2026.json` | PASS |
| Independent legacy and publication review | Completed; material findings incorporated |

The initial Windows checkout caused source-hash failures through CRLF conversion; those passed after restoring original Git bytes and adding checkout protections. Package checks do not establish current availability of every URL, authenticated API access, exhaustive world coverage, customer-specific usage or predictive validity.

## Boundaries and handoff

The new records remain `RESEARCH_CANDIDATE_NOT_GOVERNED_EVIDENCE`. No H1 tracks, frozen measurement rules, empirical outcomes, human approvals, H2/H3 activation, database or dashboard were added. Official plant coordinates are not customer data-center coordinates. Unknown customer quantities, payments, credit draws and actual utilization remain unknown.

Exactly one next implementation candidate: collect one customer-contract event from a public original with publication/event dates, excerpt, locator, hash and an access receipt, following the existing evidence contract before any promotion.
