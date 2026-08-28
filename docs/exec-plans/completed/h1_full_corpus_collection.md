# H1 Full Primary-Source Corpus Collection

## Status and stop boundary

- Status: `COLLECTION_COMPLETE_GATE6_PENDING`
- Collection cutoff: 2026-08-28
- Frozen population: 10 H1-P Product Tracks + 14 H1-C Platform Tracks
- Human Gate 6 dataset freeze: not performed
- H1 lead/lag, realization, ranking, rate, model, and verdict: not calculated
- Next boundary: human corpus-readiness review only

This task built the primary-source candidate corpus and the transferable capability ledger. It did not change Track selection, empirical interpretation, or source rules for application convenience.

## Baseline preserved

- Candidate registry hash: `A3BFDBDD8178E203C63635824985888C76DA10818D64B3E869EC5E30E4A26BB1`
- Registry freeze hash: `8D973F950CDFB9636CACCB7FE00E0565FB7BECEE2AB043AE1F3224EA8B8B43FB`
- Pilot Source registry hash: `C09C9B152B100D593DD6F5B6FDBA61F81319FD410E79BE086EE33B3459B6738B`
- Pilot dataset hash: `1B68F3C32F684380C1B3CE7671250B64E7376CAAA2A6E4683F1FAAF6C2CFD5A3`

The full builder imports the 13 Pilot Sources and 15 Pilot Events by those immutable hashes. Revised production-context records are additive and retain links to the original Pilot HOLD IDs.

## Research and verification workflow

Independent collector streams covered suppliers and platform operators. The separate adversarial verifier challenged source primacy, timestamp, scope, forward-looking language, stage inflation, same-origin duplication, and outcome interpretation for all 24 Tracks. The verifier linked every unresolved issue to one of 12 HOLD Events.

Deterministic code handled archive naming, SHA-256, Source/Event links, Track population, timestamp shape, provenance equality, duplicate IDs, coverage, manifest hashes, and replay. It did not approve semantic candidates.

## Corpus counts

- Primary Sources: 51 = 13 immutable Pilot + 38 new/reused official archives
- Atomic Events: 75 = 15 immutable Pilot + 60 new/revised candidates
- Candidate ingestion: 63 `ACCEPTED`/`UNREVIEWED`, 12 `HOLD`, 0 ingestion `REJECTED`
- Deterministic validation: 63 accepted-pass, 2 hold-pass, 10 hold-rejected
- Collection status: 23 `COLLECTED_WITH_PRIMARY_EVIDENCE`, 1 `COLLECTED_WITH_HOLD_ONLY`
- Adversarial verification: 24/24 Tracks
- Explicit negative/delay: 1 Product Track; all other Tracks are `NOT_OBSERVED_PUBLICLY`
- Future-module candidates: 4
- Capability evidence records: 8

`ACCEPTED` means the unreviewed candidate passes the deterministic contract. It does not mean human approval or empirical inclusion.

## 24-Track collection status

| Track | Status | Accepted | HOLD | Negative/delay |
|---|---:|---:|---:|---|
| C01-AZ-H100 | PRIMARY | 3 | 0 | NOT_OBSERVED_PUBLICLY |
| C02-AZ-H200 | PRIMARY | 3 | 0 | NOT_OBSERVED_PUBLICLY |
| C03-GCP-H100 | PRIMARY | 2 | 1 | NOT_OBSERVED_PUBLICLY |
| C04-GCP-H200 | PRIMARY | 4 | 0 | NOT_OBSERVED_PUBLICLY |
| C05-AWS-H100 | PRIMARY | 2 | 0 | NOT_OBSERVED_PUBLICLY |
| C06-AWS-H200 | PRIMARY | 3 | 0 | NOT_OBSERVED_PUBLICLY |
| C07-OCI-H100 | PRIMARY | 3 | 0 | NOT_OBSERVED_PUBLICLY |
| C08-OCI-H200 | PRIMARY | 3 | 0 | NOT_OBSERVED_PUBLICLY |
| C09-META-H100 | PRIMARY | 2 | 0 | NOT_OBSERVED_PUBLICLY |
| C10-AZ-GB200 | PRIMARY | 3 | 0 | NOT_OBSERVED_PUBLICLY |
| C11-GCP-B200 | PRIMARY | 4 | 0 | NOT_OBSERVED_PUBLICLY |
| C12-AWS-B200 | PRIMARY | 3 | 0 | NOT_OBSERVED_PUBLICLY |
| C13-OCI-B200 | PRIMARY | 2 | 0 | NOT_OBSERVED_PUBLICLY |
| C14-META-GB200 | PRIMARY | 1 | 1 | NOT_OBSERVED_PUBLICLY |
| P01-SKH-HBM3 | PRIMARY | 1 | 1 | NOT_OBSERVED_PUBLICLY |
| P02-SKH-HBM3E | PRIMARY | 3 | 2 | NOT_OBSERVED_PUBLICLY |
| P03-SEC-HBM3E | PRIMARY | 3 | 1 | EXPLICIT_NEGATIVE_OR_DELAY |
| P04-MU-HBM3E | PRIMARY | 5 | 3 | NOT_OBSERVED_PUBLICLY |
| P05-SKH-HBM4 | PRIMARY | 3 | 1 | NOT_OBSERVED_PUBLICLY |
| P06-SEC-HBM4 | PRIMARY | 4 | 0 | NOT_OBSERVED_PUBLICLY |
| P07-MU-HBM4 | PRIMARY | 3 | 0 | NOT_OBSERVED_PUBLICLY |
| P08-SKH-HBM4E | PRIMARY | 1 | 0 | NOT_OBSERVED_PUBLICLY |
| P09-SEC-HBM4E | PRIMARY | 2 | 0 | NOT_OBSERVED_PUBLICLY |
| P10-MU-HBM4E | HOLD_ONLY | 0 | 2 | NOT_OBSERVED_PUBLICLY |

All rows remain `HUMAN_REVIEW_REQUIRED`.

## Coverage for Gate 6 readiness

Coverage below counts only `ACCEPTED` but still `UNREVIEWED` candidates. HOLD classes are listed separately in each Track row of `coverage_report.json`.

### H1-P Product Tracks

| Field | Covered Tracks / 10 |
|---|---:|
| Sample | 8 |
| Qualification | 3 |
| Design-in | 0 |
| Commitment | 0 |
| Production-stage context | 7 |
| O1 candidate | 3 |
| Operational/financial corroboration | 2 |
| Explicit negative/delay | 1 |
| Censoring risk | 6 |
| Any HOLD | 6 |

The zero accepted design-in and commitment coverage is an observed disclosure limitation, not a negative H1 result. The immutable Pilot design-in candidate remains HOLD.

### H1-C Platform Tracks

| Field | Covered Tracks / 14 |
|---|---:|
| Broad CSP CAPEX | 14 |
| AI infrastructure commitment | 1 |
| Announcement/planned launch | 3 |
| Preview | 4 |
| Limited availability | 2 |
| GA | 10 |
| Operational outcome candidate | 11 |
| Explicit named-Track delay/constraint | 0 |
| Censoring risk | 4 |
| Any HOLD | 2 |

The 14 CAPEX rows reuse company-level disclosures across named platforms. They do not allocate spending to those SKUs and do not add independent origins when reused.

## Negative evidence and disclosure bias

Samsung's official HBM3E disclosure explicitly reported a delayed start of business with a major customer; customer identity, stack, root cause, and original target date remain unavailable. It is the sole Track-level `EXPLICIT_NEGATIVE_OR_DELAY` in this corpus.

NVIDIA's official Blackwell system constraint disclosure is preserved in the future H2 queue. It was not promoted into a named CSP Track delay because the Source does not identify those Track outcomes. Oracle capacity purchases remain investment context and were corrected from an initial negative-evidence candidate to `NOT_OBSERVED_PUBLICLY`.

Official archives are announcement-biased. The other 23 Tracks record completed adverse searches as `NOT_OBSERVED_PUBLICLY`, not “no failure.”

## Major missingness

- Product: customer identity, customer volume, price, supplier share, exclusivity, qualified-supplier count, yield, and margin are generally private or not publicly observed.
- Platform: utilization, named HBM supplier/lot, platform-specific CAPEX, demand volume, price, and capacity allocation are not established.
- Recent HBM4/HBM4E and Blackwell Tracks are materially right-censored.
- P10-MU-HBM4E has development and future production-plan wording but no admissible public sample, qualification, design-in, commitment, or O1 candidate.
- A Google Cloud H100 retrospective GA month conflicts with the contemporaneous forward-looking statement and remains HOLD rather than being backdated.

## Harness failures and durable improvements

1. Development-only wording could pass an `HBM_SAMPLE` subtype check. The validator now requires explicit sample/sampling language.
2. An installed GB200 rack caption could pass `INSTALLED_OPERATIONAL`. The validator now requires explicit operational/current-use language.
3. Production-start validation originally rejected a valid atomic production fact because the same excerpt also contained unrelated future platform-shipment wording. Future-word checks are now production-specific.
4. Real official wording required narrow lexical additions such as `has begun mass/volume production`, `mass production is slated`, and current commercial/volume shipment phrases. These additions remain inside the frozen stage contract.
5. Coverage initially counted HOLD commitment and design-in candidates as covered facts. Coverage now uses accepted-unreviewed candidates only and lists `hold_classes` separately.
6. An Oracle capacity-purchase disclosure was initially considered negative evidence during synthesis. Scope review corrected it to investment context and public non-observation of a named-Track negative.

Each change was reduced to a validation or corpus regression check; no architecture redesign or H1 conclusion followed.

## Capability evidence

Eight records preserve performed facts for problem definition, structural reasoning, uncertainty discipline, provenance/replay governance, AI/human workflow boundaries, hypothesis revision, counterevidence search, and decision translation. They point to repository artifacts and include explicit overclaim boundaries. No application narrative, resume bullet, or subjective capability claim was produced.

## Reproducibility and validation

- Full unit suite: 70 tests passed after the corpus and verifier checks were added.
- Preserved HBM4 baseline pipeline: exit code 0.
- Preserved 2025→2026 temporal pipeline: exit code 0.
- Same-input corpus replay: byte-identical registered outputs and identical manifest hashes.
- `gate6_frozen=false`; `empirical_h1_calculated=false`.

The authoritative final hashes are stored in `data/h1/corpus/build_manifest.json`; hand-written copies are intentionally not duplicated here because any later approved corpus correction must produce a new manifest.

## Human Gate 6 issues

- Approve, retain, or exclude all 63 unreviewed accepted candidates.
- Resolve 12 HOLD candidates. Ten are deterministically rejected; two pass shape/stage rules but remain semantic HOLD: retrospective GCP H100 GA timing and Micron HBM3E planned H200 design-in scope.
- Decide whether current-shipping disclosures without a first shipment date may serve as interval O1 proxies.
- Confirm event precision for retrospective/month/quarter statements.
- Confirm same-origin groups for joint releases and repeated earnings disclosures.
- Decide whether the corpus is sufficient separately for H1-P and H1-C; no pooled sufficiency decision is allowed.

## Exactly one next task

Human Gate 6 corpus-readiness review and empirical dataset freeze before calculating any H1 result.
