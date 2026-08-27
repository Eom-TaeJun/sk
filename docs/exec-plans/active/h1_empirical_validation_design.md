# Active Execution Plan — H1 Demand Signal Quality Empirical Validation Design

## 0. Document status and boundary

**Status:** `READY_FOR_HUMAN_REVIEW — NOT APPROVED FOR EXECUTION`

This document defines the empirical contract for H1 before a dataset, backtest, statistical model, or automated research workflow exists. It does not select cases, collect a corpus, calculate a signal ranking, or make an H1 finding. The deleted interrupted H1 experiment is not a methodological or evidentiary input to this design.

The design preserves the project transmission model:

```text
AI workload / service
→ customer economics
→ CAPEX
→ compute platform
→ memory requirement
→ qualification / commercial confirmation
→ order / shipment
→ realized memory demand
```

This is an economic map for locating information. It is not a proven causal path.

## 1. Business decision problem

### 1.1 Decision to support

SK hynix Marketing must distinguish a broad indication that AI infrastructure investment may grow from evidence that a particular memory product, platform, or customer scope is moving toward commercial realization. The practical question is not whether an announcement sounds positive. It is whether the information available at that historical date could defensibly change one or more of the following decisions:

- `Demand Forecast`: remain at broad market watch, prepare a scenario, or recognize stronger realization evidence;
- `Customer Priority`: increase attention to a customer/platform track without inventing customer share or volume;
- `Qualification` and `Target Spec`: prioritize evaluation support or specification response;
- `TTM`: update the expected commercialization path and monitor delay risk;
- `CAPA Allocation` and `Price·Volume`: identify when an internal decision would require additional private confirmation, not prescribe an allocation from public data;
- `Product Mix` and `Supply Risk`: identify which demand path is becoming more credible and which constraints remain unresolved.

H1 therefore evaluates public signal quality for a decision update. It does not estimate an optimal CAPA percentage or a numeric memory-demand forecast.

### 1.2 Primary H1 question

> Among publicly observable AI-memory demand-chain signals, which signal classes provide more decision-useful visibility into later realized AI-memory demand than broad upstream CSP CAPEX, and what lead time do they provide?

The comparison is against CAPEX as an upstream reference signal, not against a claim that CAPEX is useless. A valid result may show that CAPEX is better for long-horizon direction while order-proximate signals are better for scope precision or false-positive control.

### 1.3 What “better demand visibility” means

`Decision-useful visibility` is a vector of interpretable dimensions. The primary analysis must not collapse them into one weighted score.

| Dimension | Operational question | Proposed observable |
|---|---|---|
| Temporal precedence | Was the signal public before realization? | `outcome_event_at - signal_available_at`, reported as an interval when dates are imprecise |
| Useful lead | Was there enough time for a Marketing action? | Continuous lead days first; any actionability band is a sensitivity rule, not the primary result |
| Realization | Did the approved outcome occur within the observation window? | Outcome status under the hierarchy in Section 3 |
| False-positive risk | Did a positive signal fail to reach the approved outcome while fully observed? | Fully observed no-realization count/rate, separated from delay and censoring |
| Scope precision | Did signal and outcome refer to the same product/platform/customer scope? | Exact, partial, or broad scope match with the mismatch stated |
| Stability | Does the pattern survive reasonable case and rule changes? | Robustness checks in Section 13 |
| Incremental information | Did the downstream signal change what was knowable beyond CAPEX alone? | Within-track evidence-state comparison before and after the new signal |
| Historical availability | Could an analyst actually have used it then? | Strict `available_at <= cutoff_at` eligibility |

The dimensions answer different questions and can trade off. A signal with long lead but many non-realizations may be useful for `WATCH`; a later signal with shorter lead and tighter scope may be useful for `PREPARE` or internal confirmation. Neither dominates automatically.

### 1.4 Three meanings that must remain separate

- **Signal usefulness:** Could the signal have changed a bounded decision at the time, given its meaning, scope, and lead?
- **Forecast accuracy:** Does a repeatable model predict a numeric outcome with validated error? H1's minimum design does not claim this.
- **Causal effect:** Did the observed event cause realized demand? H1 does not identify causal effects.

Temporal ordering, a graph edge, or correlation cannot be reported as causality.

### 1.5 Testable subquestions

The minimum validation should report, without combining them into a score:

1. Do order-proximate signal classes reduce fully observed non-realization relative to CSP CAPEX within comparable tracks?
2. Do they retain positive, decision-usable lead rather than merely confirm an outcome after it occurs?
3. Do they improve product/platform scope or change the evidence state beyond what CAPEX already established?
4. Does the answer differ by supplier, product generation, platform, period, or source restriction?

## 2. Empirical estimand and comparison boundary

The minimum design estimates descriptive signal performance, not a causal coefficient:

> For a pre-registered public-information track and outcome contract, how often and how early was each signal class observed before later commercial realization, non-realization, delay, or censoring, and what incremental scope did it add relative to CAPEX?

The principal comparison is **within the same eligible track**. Cross-company averages are secondary because disclosure practices, product definitions, customer confidentiality, and fiscal calendars differ.

The study must report signal-class results and matched track narratives together. A pooled average cannot erase a product-specific contradiction, and a famous success cannot establish a general pattern.

## 3. Outcome contract: realized AI-memory demand

### 3.1 Why one convenient variable is inadequate

No public variable perfectly measures realized AI-memory demand. Commercial shipment is close to supplier realization but may still reflect supply readiness, channel movement, or a self-reported milestone. Platform deployment is closer to customer use but often cannot be linked to a named memory supplier. HBM revenue or bit shipment confirms economic realization at a broader scope but is disclosed inconsistently. Broad semiconductor revenue has low product specificity and is not an acceptable primary outcome.

The recommended contract therefore uses a strict primary event plus independent corroboration levels.

### 3.2 Candidate outcomes

| Candidate | Construct validity | Observability / frequency | Product specificity | Comparability and revision risk | Demand vs supply ambiguity | Recommendation |
|---|---|---|---|---|---|---|
| Commercial shipment or customer supply explicitly commenced | High for supplier-side commercial realization when the statement is about an occurred event | Irregular official product/IR event | Usually high | Wording differs by supplier; later restatement must not overwrite the original | Still does not prove customer consumption, repeat volume, price, or share | Primary event when occurrence, product, and scope are explicit |
| Volume production explicitly linked to present customer supply | Medium-high | Irregular official product/IR event | High | `volume production`, `ramp`, and `mass production` are not standardized | Can be manufacturing capability if no actual supply is stated | Eligible only when the same source directly links production to current supply/shipment; otherwise a signal, not outcome |
| Product-specific shipment/ramp realization disclosed in earnings | Medium-high | Quarterly when disclosed | Medium-high | Voluntary disclosure can disappear or change definition | Better economic confirmation, but may aggregate generations/customers | Operational corroboration |
| Customer/platform deployment or cloud general availability explicitly linked to the relevant memory generation | High for deployed compute demand | Irregular platform/cloud release | Platform high; supplier often low | Configuration and regional scope may change | Confirms platform availability, not utilization or a named supplier's volume | Independent operational corroboration when linkage is direct |
| Product-specific HBM revenue or bit-shipment realization | Medium | Quarterly/annual but inconsistent | Often product family rather than generation | Definitions and mix vary across companies | Reflects price, mix, and supply as well as demand | Financial corroboration, not sole primary outcome unless specificity is adequate |
| Broad DRAM, semiconductor, data-center, or cloud revenue | Low for the target construct | Quarterly | Low | Accounting definitions are stable within company but not the target product | Many non-HBM drivers | Context only; rejected as primary outcome |
| Equity price or market capitalization | Very low | Daily | None | Market expectations and macro factors dominate | Not demand realization | Excluded |

### 3.3 Recommended outcome hierarchy

The future analysis should preserve separate evidence levels rather than manufacture a single pseudo-precise target.

1. **`O1_COMMERCIAL_REALIZATION`** — an official source states that commercial/mass/volume shipment or customer supply of the identified HBM product has actually begun. A plan, target, readiness statement, sample shipment, or qualification activity does not qualify.
2. **`O2_OPERATIONAL_CORROBORATION`** — a separate official origin confirms either product-specific shipment/ramp or counterparty platform/cloud availability directly linked to the product generation. It strengthens O1 but does not retroactively change the earlier signal's evidence level.
3. **`O3_FINANCIAL_CORROBORATION`** — an official result reports product-specific HBM revenue, bit shipment, or ramp contribution at a scope compatible with the track. Broad company revenue cannot qualify.

Outcome state is then represented as:

- `REALIZED_CORROBORATED`: O1 plus at least one independent O2 or O3 origin with compatible scope;
- `REALIZED_SINGLE_ORIGIN`: O1 is present but independent corroboration is unavailable;
- `DELAYED`: O1 occurs after the approved base observation window but within the approved extended window;
- `NO_REALIZATION_WITHIN_WINDOW`: no O1 occurs during a fully elapsed window; this is an observed signal outcome, not proof that demand never existed;
- `FAILED_OR_WEAKENED`: an official source reports cancellation, reduction, qualification failure, or a materially weaker scope;
- `RIGHT_CENSORED`: the required follow-up period has not elapsed at dataset freeze;
- `UNRESOLVED`: public evidence conflicts or is too ambiguous to assign another state.

Later realization evidence may change a track from `RIGHT_CENSORED` or `NO_REALIZATION_WITHIN_WINDOW` to `DELAYED` in a later dataset version. It must not overwrite the prior snapshot.

**Gate reference:** the hierarchy, the treatment of production-linked supply, and these states require Gate 2 approval.

## 4. Signal taxonomy independent of the outcome

Signal class is assigned from what the source directly establishes at its historical availability date. A positive tone is not sufficient. Each record also keeps subtype, direction, scope, and evidence level so different stages are not collapsed.

| Signal | What is observed | Economic meaning | Transmission stage / distance | Historical availability | Scope | Main false positive | Main false negative | Public-data feasibility |
|---|---|---|---|---|---|---|---|---|
| `CSP_CAPEX` | Reported or guided capital expenditure with stated infrastructure mix where available | Investment intention or asset build, potentially supporting future compute | Customer economics → infrastructure; broad/upstream | Quarterly/annual filing or earnings release `available_at`, never quarter end | Company, sometimes cloud/AI mix | Land/buildings, long-lived assets, leases, timing shifts, non-AI mix, throttling or delayed activation | Demand served from existing/leased capacity or mix detail not disclosed | `HIGH` for total CAPEX; AI/memory attribution remains `TO_VERIFY` |
| `AI_INFRA_COMMITMENT` | Announced data-center, accelerator, capacity, or investment commitment | Intent to create future AI capacity | CAPEX → platform capacity; upstream/intermediate | Official announcement date | Company/region/site; product often broad | Permit, construction, power, equipment, or demand delay | Quiet expansion or leased capacity | `MEDIUM` |
| `PLATFORM_LAUNCH` | Accelerator/system launch or planned ship date | A product architecture requiring a memory generation enters market roadmap | Compute platform → memory requirement; intermediate | Official launch/filing date | Platform/product generation | Schedule slip, limited availability, alternative memory configurations | Undisclosed custom platforms | `HIGH` for major public platforms; linkage can be `MEDIUM` |
| `PLATFORM_DEPLOYMENT` | Platform shipment, cloud general availability, or service availability has occurred | Compute capacity is deployable by customers | Platform → operational use; intermediate/order-adjacent | Official release date; region/version retained | Platform/region/cloud service | Availability without material utilization; small initial region | Private deployment and internal workloads | `MEDIUM` |
| `HBM_SAMPLE` | Identified product samples delivered for evaluation | Product entered customer evaluation | Memory requirement → evaluation; intermediate | Official product/IR event date | Supplier/product; customer often unnamed | Evaluation failure, redesign, platform delay, multiple suppliers sampled | Quiet sampling or non-disclosure | `MEDIUM`; the complete population remains `LOW` |
| `QUALIFICATION_STAGE` | Qualification is planned, underway, final-stage, or explicitly complete | Technical/commercial acceptance process is progressing | Qualification; order-proximate but stage-dependent | Official disclosure date | Product/platform/customer when disclosed | `planned`/`underway` mistaken for completion; platform-specific approval generalized | Confidential completion not disclosed | `LOW`; substage must remain separate |
| `DESIGN_IN` | Product is explicitly selected or incorporated into a named platform/design | Stronger technical selection than sampling | Qualification/commercial confirmation; order-proximate | Official supplier or counterparty disclosure | Product/platform/customer | Design may be delayed, dual-sourced, resized, or canceled | Customer confidentiality | `LOW` |
| `LTA_COMMERCIAL_COMMITMENT` | Signed/finalized long-term agreement or binding commitment, with scope stated | Longer-duration commercial commitment | Commercial confirmation → order; order-proximate | Filing/official IR when signed or disclosed | Parties/product/period; volume often absent | Non-binding language, renegotiation, minimum terms undisclosed | Confidential contracts | `LOW`; discussion and signed agreement must not be combined |
| `ORDER_ADJACENT_SUPPLY_COMMITMENT` | Allocation, supply plan, sold-out status, or commercial negotiation milestone that is not a disclosed LTA/order | Indicates demand/supply coordination nearer commercialization | Commercial confirmation; order-proximate candidate | Official disclosure date | Supplier/product/period | Company optimism, ambiguous binding force, double counting with LTA | Purchase orders are normally private | `LOW`; never relabel as LTA |
| `POWER_DC_READY` | Site/capacity is energized, commissioned, rack-ready, or service-available | Removes a downstream infrastructure barrier to accelerator operation | Data-center realization path; intermediate/order-adjacent | Utility, operator, regulator, or service announcement date | Site/region/platform when known | PPA, permit, or building completion mistaken for energized usable capacity; low utilization | Private commissioning and behind-the-meter supply | `LOW`; product linkage is often unresolved |
| `PRICING_INVENTORY_CONTEXT` | Official or independently sourced price/inventory direction at compatible product scope | Conditions affecting order timing and supplier revenue realization | Market/commercial context; broad/intermediate | Release/publication date | Product family/industry/company | Spot/contract mismatch, channel inventory, price-led revenue without bit demand | Confidential contract prices/customer inventory | `MEDIUM` for context, `LOW` for HBM product specificity |
| `SHIPMENT_REALIZATION` | Commercial shipment/customer supply actually started | Confirms the outcome event | Realization | Official occurrence disclosure | Product/supplier/platform | Shipment does not prove sustained demand, end use, price, volume, or share | Unannounced shipments | `MEDIUM`; used as O1 outcome, **not as a predictor of that same outcome** |

Subtypes are mandatory where language can change meaning. At minimum:

- qualification: `PLANNED`, `UNDERWAY`, `FINAL_STAGE`, `COMPLETE`;
- commitment: `DISCUSSION`, `SUPPLY_PLAN`, `ALLOCATION`, `SIGNED_LTA`;
- readiness: `PERMIT`, `PPA_OR_GRID_COMMITMENT`, `CONSTRUCTION`, `ENERGIZED`, `RACK_READY`, `SERVICE_AVAILABLE`;
- production: `READINESS`, `STARTED`, `RAMPING`, `CUSTOMER_SUPPLY_STARTED`.

Only the direct wording and scope determine subtype. The transmission distance is a descriptive taxonomy and must not be encoded as an outcome-favoring score.

## 5. Unit-of-observation alternatives

| Design | Construct validity | Data/sample feasibility | Selection and comparability risk | Timing, false positives, censoring | Decision usefulness | Assessment |
|---|---|---|---|---|---|---|
| A. Product-generation event tracks | High for sample → qualification → commercial realization | Small and disclosure-dependent | Successful products overrepresented; supplier wording differs | Event timing is good; failures and silent qualifications are hard to observe | High for Qualification, TTM, product scope | Strong core, insufficient alone |
| B. Customer/platform realization tracks | High for CAPEX → deployment → memory requirement when direct linkage exists | Sparse because supplier/customer links are confidential | Bespoke platforms and disclosure practices differ | Can observe deployment delays; memory-supplier outcome often unresolved | High for Customer Priority and demand transmission | Valuable only with explicit linkage |
| C. Company-quarter or industry-quarter panel | More repeated rows and regular reporting | Highest mechanical sample availability | Mixed products, accounting/mix confounding, disclosure breaks | Coarse event ordering; apparent sample size exceeds independent events | Medium for regime context, low for product-stage validation | Reject as primary unit |
| D. Hybrid event tracks plus quarterly corroboration | Preserves product events while using regular financial/context evidence | Feasible if kept small | Still exposed to event-publication bias, but biases remain visible by layer | Supports event-time sequencing, delay/censoring, and broader confirmation | Highest balance for public-data Marketing interpretation | Recommended |

### 5.1 Recommended unit

The primary analytical unit is an **atomic public event nested in a pre-registered track**.

- `PRODUCT_COMMERCIALIZATION_TRACK`: supplier + HBM product generation + declared platform/customer scope where available;
- `PLATFORM_REALIZATION_TRACK`: CSP/platform + deployment scope, linked to a memory product only when primary evidence makes that link explicit.

Quarterly company/industry observations are corroborating context, not extra independent product events. Multiple excerpts from the same origin and event do not increase sample size.

The minimum comparison uses a hybrid design: structured event chains are the core; CAPEX and downstream signals are compared within compatible tracks; quarterly product-specific operational or financial disclosures corroborate realization. Unsupported links between a CSP's CAPEX and a supplier's shipment are forbidden.

This creates an important feasibility boundary. Product-commercialization tracks may contain strong downstream stages but no defensible CSP CAPEX link; CSP tracks may contain CAPEX and deployment but no named memory supplier. A direct CAPEX-versus-HBM comparison is admissible only in a `BRIDGE_ELIGIBLE` track with primary evidence linking platform, memory generation, and realization at compatible scope. Otherwise the two strata are reported separately and H1 cannot receive a blanket superiority verdict.

**Gate reference:** this hybrid observation unit and its two track strata require Gate 3 approval.

## 6. Recommended minimum empirical design

### 6.1 Design class

Use a **pre-registered, outcome-first historical event-chain design with matched within-track comparisons and limited quarterly corroboration**.

It has four parts:

1. Freeze the eligible track universe, outcome hierarchy, signal dictionary, source rules, and cutoff rules before evaluating results.
2. In a signal pass, classify only information available at each historical cutoff and freeze the signal snapshot plus content hash.
3. In a separate outcome pass, reveal later eligible realization/counterevidence and assign outcome/censor states without changing the earlier evidence classification.
4. Compare interpretable dimensions within matched tracks and then summarize cross-track stability. Do not fit a predictive model in the minimum analysis.

This is intentionally a small-N validation of measurement and signal usefulness. It can discover that the public data is insufficient.

### 6.2 Within-track comparison

For each eligible track:

- establish the earliest eligible CAPEX or broad investment signal only when its entity/platform scope can be linked without inference;
- retain each distinct downstream signal stage and historical availability date;
- observe the approved outcome state and independent corroboration;
- calculate lead-time intervals and fully observed no-realization/delay/censor flags;
- record what changed from `CAPEX_ONLY` to each later evidence snapshot in scope, confidence explanation, and affected Marketing decision variable;
- preserve counterevidence and semantic boundaries.

No track must contain every signal class. Absence of a public disclosure is `NOT_OBSERVED_PUBLICLY`, not evidence that the real-world event did not happen.

The analysis has two nested estimands. Product tracks estimate the usefulness of sample/qualification/commitment stages for later O1. CSP/platform tracks estimate the usefulness of CAPEX/infrastructure/readiness for later platform deployment. Only `BRIDGE_ELIGIBLE` tracks contribute to a direct cross-stage CAPEX-versus-HBM comparison. If the feasibility manifest finds too few bridge tracks, the direct H1 comparison is `INCONCLUSIVE` even if each stratum yields useful descriptive findings.

### 6.3 Primary outputs

The future minimum result should report:

- eligible tracks and their inclusion/exclusion trace;
- per-signal-class `eligible`, `realized`, `no realization within window`, `delayed`, `failed/weakened`, and `right-censored` counts;
- lead-time median/range only when dates and sample count make them meaningful, otherwise event-level intervals;
- exact/partial/broad scope-match distribution;
- within-track evidence-state changes relative to CAPEX-only;
- counterexamples and leave-one-stratum robustness;
- a human-approved `SUPPORTED`, `REJECTED`, `QUALIFIED`, or `INCONCLUSIVE` H1 verdict.

Any class with insufficient independent, fully observed tracks remains `INSUFFICIENT_EVIDENCE`; it is not ranked.

### 6.4 Why no composite score in the minimum design

A weighted score would hide the central trade-off between lead, false-positive control, and scope. Its weights would encode business loss preferences not observable from public data. A composite may be proposed later only if a specific decision supplies approved loss weights; it cannot be a discovery metric.

## 7. Source hierarchy and independence contract

| Tier | Source class | Can establish | Cannot establish by itself | Independence / revision risk | Historical availability |
|---|---|---|---|---|---|
| `P1_REGULATORY` | SEC/DART filings, exchange filings, audited reports | Filed financials, contracts/material events when disclosed, filing acceptance time | Undisclosed customer/product detail; causal linkage | Amendments are new revisions; same filing quoted elsewhere is one origin | Usually high; acceptance metadata can be retained |
| `P1_EVENT` | Official earnings materials, product releases, platform/cloud releases | What the issuer directly states occurred/plans at a timestamp | Independent validation of self-claims, hidden commercial terms | Multiple pages/decks from one event may be one origin group; pages can be revised | High to medium; archive/hash required |
| `P1_COUNTERPARTY` | Official customer, platform, supplier, utility counterpart disclosure | Independent operational linkage within the stated scope | Facts outside its role or unnamed supplier identity | Independent only if it has a distinct evidentiary basis, not a syndicated quote | Medium; events are irregular |
| `P2_OFFICIAL_CONTEXT` | Government, regulator, standards, utility statistics | Aggregate infrastructure, power, economic, or technical context | Product-specific memory demand unless directly linked | Revisions and methodological vintages retained | Medium-high, often annual/periodic |
| `S1_INDUSTRY` | Credible trade/industry sources | Candidate discovery, terminology, potential negative cases | Primary outcome or independent confirmation without original evidence | Re-reporting does not create independence; archives may be unstable | Variable |
| `S2_ESTIMATE` | Analyst/market-research estimates | Sensitivity context when unavoidable | FACT, hidden volume/share, or realization | Methodology and revisions may be inaccessible | Low/`TO_VERIFY` |

Independence is counted by `origin_group`, not URL count. A press release, its newsroom mirror, and a news article quoting it are one origin unless the later source contributes independently obtained evidence. A supplier's leadership or demand outlook remains `B_COMPANY_CLAIM`; counterparty confirmation can corroborate only the overlapping statement and scope.

### 7.1 Limited source-family feasibility check

Checked for design feasibility on 2026-08-28; these examples are not selected cases and were not extracted into a dataset.

| Source family | Representative official evidence | Public frequency / period observed | What appears feasible | Limitation / status |
|---|---|---|---|---|
| SEC EDGAR filings | SEC explains that filing headers contain acceptance timestamps and that filings are generally available shortly after acceptance: [SEC EDGAR timestamp guidance](https://www.sec.gov/about/webmaster-frequently-asked-questions) | Event/quarter/annual; full-text search covers long historical periods | Reconstruct filing availability and preserve accession/revision metadata | Exact first-public byte timestamp is not provided; acceptance time is the conservative proxy |
| CSP official earnings and filings | Microsoft separates cloud/AI CAPEX components and discusses capacity timing in its [FY24 Q4 earnings call](https://www.microsoft.com/en-us/investor/events/fy-2024/earnings-fy-2024-q4); Alphabet defines technical infrastructure and reports CAPEX in its [2024 Q4 call](https://abc.xyz/investor/events/event-details/2025/2024-Q4-Earnings-Call/) | Quarterly/annual; representative 2024–2025 pages have explicit event dates | Build historically dated CAPEX and capacity-context signals | CAPEX includes land, buildings, servers, leases, and internal/external workloads; no direct HBM volume mapping |
| Memory-supplier product events | SK hynix distinguishes samples under customer evaluation in its [2023 HBM3E release](https://news.skhynix.com/en/sk-hynix-develops-worlds-best-performing-hbm3e/) and production for customer supply in its [2024 HBM3E release](https://news.skhynix.com/en/sk-hynix-begins-volume-production-of-industry-first-hbm3e/); Micron publishes product-stage events in its [2024 HBM3E production release](https://investors.micron.com/news/press-release/2024/Micron-Commences-Volume-Production-of-Industry-Leading-HBM3E-Solution-to-Accelerate-the-Growth-of-AI-02-26-2024/default.aspx) | Irregular product events; representative official archive spans multiple HBM generations from 2022 onward | Observe sample, evaluation, production, and some supply/platform links with publication dates | Issuer-reported success bias; qualification completion, failed evaluations, customer volume/price/share often absent |
| Memory-supplier earnings/IR | SK hynix reports HBM share of DRAM revenue in [4Q24 results](https://news.skhynix.com/en/sk-hynix-announces-4q24-financial-results/); Micron reports HBM ramp/revenue in [official FY24 Q4 prepared remarks](https://investors.micron.com/static-files/5890f96b-bf35-4c4d-b8b8-b9d0f9ed63e4) | Quarterly when voluntarily disclosed | Add broader operational/financial corroboration | Product-generation and customer specificity vary; definitions can change; full historical file/index stability is `TO_VERIFY` |
| Platform/cloud official releases | Microsoft announced regional general availability of H100-based VMs in an [Azure infrastructure release](https://azure.microsoft.com/en-us/blog/scale-generative-ai-with-new-azure-ai-infrastructure-advancements-and-availability/) | Irregular event pages; representative availability events exist from 2023 onward | Observe a dated operational deployment/availability stage | General availability does not establish utilization, exact HBM supplier, or memory order volume; page revision history needs archiving |
| Government power/context | DOE/LBNL published a dated aggregate [U.S. data-center electricity-use report](https://www.energy.gov/articles/doe-releases-new-report-evaluating-increase-electricity-demand-data-centers) | Periodic/annual aggregate studies; example includes historical estimates and a forecast | Supply macro context and aggregate power-demand trend | Not a site-level `POWER_DC_READY` event and not product-specific; utility/operator data feasibility remains `TO_VERIFY` |

Feasibility conclusion: public evidence is adequate for a small event-chain design, but not for a complete event population or a precise numeric demand target. Product-stage positives are much easier to observe than failed qualifications or confidential contracts. The minimum study must therefore expose selection and censoring rather than imply statistical representativeness.

**Gate reference:** tiers, origin-group independence, and the admissible use of secondary sources require Gate 4 approval.

## 8. Temporal and information-cutoff contract

### 8.1 Required clocks

- `event_at`: when the directly stated real-world event occurred. Store lower/upper bounds and `date_precision` when exact timing is unknown.
- `published_at`: the timestamp printed by the publisher or filing system.
- `available_at`: the earliest timestamp at which the chosen historical analyst could defensibly access that exact information. This is the cutoff field.
- `accessed_at`: when the project retrieved the source; it cannot substitute for historical availability.

A future plan has `expected_event_at`; it must not be stored as an occurred `event_at`.

### 8.2 Eligibility rule

For every historical snapshot:

```text
eligible(source, cutoff_at) :=
  source.available_at <= cutoff_at
  AND source.revision_available_at <= cutoff_at
```

The snapshot must retain the source revision, excerpt, locator, content hash, and origin group that were eligible then. Later truth may evaluate the old signal but cannot rewrite what the signal meant at the cutoff.

### 8.3 Publication and revision rules

1. Earnings for a completed quarter become available only at the earnings release/filing timestamp, never at quarter end.
2. A source with a printed date but no time is conservatively usable from `00:00` on the next calendar day in the publisher's local timezone. The raw date, timezone assumption, and UTC normalization are retained.
3. EDGAR acceptance time is used as the availability proxy for an SEC filing; post-acceptance amendments or corrections receive a new revision record and availability time.
4. Revised CAPEX guidance is a new event. It does not overwrite the guidance known in an earlier snapshot.
5. A retrospective statement is available only when published, even if it describes an earlier event. It may set `event_at` earlier than `available_at` but cannot be used at the earlier cutoff.
6. A re-reporting article keeps its own publication time but cannot move the original claim earlier or increase source independence.
7. Later disclosure of customer identity, qualification status, or commercial shipment cannot backfill an earlier signal classification.
8. If an official page changes without a visible revision identifier, the archived content/hash is preserved as a separate source revision. Unarchived prior wording is `TO_VERIFY`, not reconstructed from memory.
9. Material timezone ambiguity is resolved conservatively to the later eligible instant; interval sensitivity is required when the choice can affect ordering.

### 8.4 Future deterministic enforcement

The later deterministic layer—not a model prompt—must:

- validate date types, timezone, precision, and `available_at <= cutoff_at`;
- reject an outcome or source revision leaked into a signal snapshot;
- preserve immutable snapshot manifests and hashes;
- join events only on approved track and scope keys;
- calculate lead intervals, windows, and censor flags;
- prevent duplicate origin groups from inflating independence;
- reproduce every inclusion, exclusion, and derived status.

No enforcement code is created in this task.

**Gate reference:** cutoff semantics and the conservative date-only rule require Gate 4 approval.

## 9. Ex-ante case inclusion and exclusion contract

### 9.1 Proposed eligible universe

The recommended starting boundary is public information available from **2022-01-01 through a future approved dataset freeze**. The start is proposed because it admits an earlier AI-memory commercialization regime and broad investment signals while official HBM and CSP archives are plausibly available; it is not a claim that 2022 is an economic breakpoint.

Eligible entities are:

- publicly reporting memory suppliers with official HBM product/IR evidence;
- publicly reporting accelerator/platform providers or CSPs with official deployment/CAPEX evidence;
- official counterparties, regulators, utilities, or government sources needed to verify an event within the declared track scope.

Eligible tracks are generated from an ex-ante supplier/product or platform universe, not from a list of famous outcomes. A product/platform is included when it meets the source and follow-up rules whether the public evidence later indicates success, delay, weakening, or unresolved status.

### 9.2 Signal inclusion

An event is eligible when all are true:

- it was public within the approved period;
- it fits a pre-defined signal class/subtype based on direct wording;
- it has Source ID, publisher, URL/archive, excerpt, locator, publication/availability date, hash, tier, origin group, and revision identity;
- its entity/product/platform/geography scope is explicit or marked unknown;
- its direction and stage can be assigned without using later outcomes;
- a primary official source exists, except secondary-source counterexample discovery retained as `TO_VERIFY` and excluded from primary comparison.

### 9.3 Outcome observation window

The proposed future contract uses a **12-month base follow-up**, with **6-month and 18-month sensitivity windows**. Twelve months spans multiple quarterly decision cycles while limiting regime drift; six months tests near-term actionability and eighteen months tests delayed realization. These are design choices, not empirically established product-cycle constants.

Lead time remains continuous in the primary report. Binary “useful lead” bands, if desired for a specific Marketing workflow, are sensitivity outputs and require an approved decision rationale.

### 9.4 Outcome and censor treatment

- `NO_REALIZATION_WITHIN_WINDOW` requires the complete base window to have elapsed and no eligible O1 event.
- `DELAYED` requires O1 after the base window but inside the extended window.
- `FAILED_OR_WEAKENED` requires affirmative official counterevidence; silence alone is insufficient.
- `RIGHT_CENSORED` applies when the dataset freeze occurs before the relevant window closes. It is excluded from false-positive denominators.
- An unresolved scope or date conflict is retained as `UNRESOLVED`, not force-fit to realized or false positive.
- Later dataset versions append outcomes and state changes; earlier snapshots and classifications remain reproducible.

### 9.5 Negative-case and selection-bias controls

The track manifest is generated before outcome review. It must not require a known success. The future feasibility pass should actively search every eligible track for delay, cancellation, reduced guidance, qualification difficulty, or lack of realization, but a model-found negative remains a candidate until primary evidence is verified.

At minimum, a comparative H1 verdict should not be allowed unless the approved dataset includes:

- more than one independent supplier/product or platform stratum so one famous success cannot determine the verdict;
- `BRIDGE_ELIGIBLE` matched tracks in which CAPEX and at least one downstream signal class are both eligible at compatible scope;
- at least one fully observed delayed, failed/weakened, or no-realization track, rather than successes only;
- enough follow-up that right censoring does not determine the result.

The exact sufficiency threshold must be set after a source-availability manifest, before outcome calculation. It cannot be reduced merely to obtain a verdict.

### 9.6 Exclusion and duplicate rules

Exclude from the primary comparison, with a recorded reason:

- missing primary provenance, excerpt, locator, date, or hash;
- signal and outcome whose product/platform scope cannot be matched without unsupported inference;
- a source first available after the relevant cutoff;
- broad commentary that cannot be atomized to a signal stage;
- duplicate/reprinted material from the same origin group;
- planned shipment mislabeled as occurred shipment;
- sample shipment mislabeled as commercial shipment;
- quarter/company aggregates used as if they were independent product events.

Exclusion is itself reviewable. A human can approve `INCLUDE`, `EXCLUDE`, or `HOLD`, with reason and dataset version; prior decisions are not overwritten.

**Gate reference:** the time boundary, eligible universe, follow-up windows, sufficiency rule, and exclusions require Gate 3 and Gate 5 approval.

## 10. Empirical-strategy comparison

| Strategy | Question answered | Data requirement | Identification strength | Main bias | Timing / false positives / censoring | Business interpretability | Public-data fit |
|---|---|---|---|---|---|---|---|
| Structured historical event-chain | What was known at each stage and what happened later? | Atomic dated events with trace | Strong semantic and temporal validity; no causal identification | Publication and successful-event bias | Directly models order and censoring; false positives require a pre-registered universe | High | High for a small sample |
| Matched-case comparison | Did downstream evidence add value versus CAPEX within similar tracks? | Comparable signals/outcome in the same or tightly matched track | Better controls scope than pooled averages | Few matches; human matching choices | Can compare lead and no-realization within matches | High | Medium-high |
| Company-quarter panel/time series | Are regular CAPEX/signal measures associated with later aggregate outcomes? | Many consistently defined quarters and numeric outcomes | Potentially estimates average association, not causality | Mixed products, autocorrelation, disclosure breaks, pseudo-sample size | Coarse timing; censoring manageable with enough history | Medium | Low for product-specific H1 now |
| Hybrid event + quarterly corroboration | Do event-stage patterns hold with broader operational/financial confirmation? | Event tracks plus limited regular context | Best construct/feasibility balance; still descriptive | Combines layers with different scope; must not treat them as equal rows | Event layer handles timing/censoring; quarterly layer corroborates | High | Recommended |

### 10.1 Selected strategy

The minimum credible strategy is the hybrid in Section 6: event-chain core, within-track/matched comparisons, and quarterly corroboration. Statistical inference is not justified until a source-feasibility manifest demonstrates enough independent, consistently defined observations. Code availability is not a reason to prefer a panel or model.

## 11. Proposed empirical methods and permitted interpretation

| Method | Exact problem solved | Required assumptions / minimum structure | Allowed interpretation | Not allowed / recommendation |
|---|---|---|---|---|
| Event-time ordering and lead intervals | Determine whether and how long a signal preceded O1 | Reliable `available_at`, outcome occurrence, scope match; interval dates when imprecise | Historical precedence and observed lead range | No causal claim; primary method |
| Realization/no-realization/delay proportions | Compare observed outcomes by signal class | Pre-registered denominator, fully observed windows, censoring separated | Descriptive frequency in the selected public sample | No population probability or “accuracy” claim with small/selective N; primary method |
| Within-track evidence-state comparison | Test whether a later signal added scope or reduced uncertainty beyond CAPEX | Same track/outcome contract and frozen earlier snapshot | Incremental decision information in that track | No coefficient or universal superiority; primary method |
| Matched sign/dominance table | Check whether downstream signals consistently improve some dimensions without losing all lead | Approved matching keys and multiple independent matches | Direction and consistency of trade-offs | No statistical generalization from a few matches; primary method |
| Descriptive Kaplan–Meier/time-to-event | Describe time to realization while retaining right-censored tracks | Enough independent comparable tracks, stable time origin, non-informative censoring plausibly discussed | Conditional descriptive realization curve for the observed sample | No causal hazard interpretation; defer unless feasibility supports it |
| Correlation / cross-correlation | Explore aggregate lead/lag co-movement | Consistent numeric series, stationarity/seasonality treatment, enough periods | Exploratory association only | Not recommended for minimum H1; cannot prove incremental information or causality |
| Regression / panel methods | Estimate conditional association after specified controls | Many comparable independent units/periods, stable definitions, modeled dependence and confounding | Association under stated specification | Not recommended now; public product-level outcome and N are inadequate until proven otherwise |
| LASSO or predictive classification | Select variables or predict a labeled outcome | Large, stable training sample, pre-specified validation split, repeatable features/outcome | Out-of-sample predictive performance only | Rejected for minimum H1: small heterogeneous events would make selection unstable and distract from construct validity |

No p-value, confidence interval, model “accuracy,” or coefficient should be reported unless the later dataset and dependence structure justify it. The absence of a statistical model is not a design failure.

## 12. H1 falsification and verdict contract

Verdicts apply to the approved public sample and signal classes, not to undisclosed internal orders.

### 12.1 `SUPPORTED`

Support requires all of the following pattern after the approved sufficiency gate:

- in multiple independent `BRIDGE_ELIGIBLE` matched strata, at least one downstream signal class shows better realization/no-realization discrimination and adds tighter outcome scope or incremental information than CAPEX;
- that class is usually observed before O1 with usable lead, rather than mainly on or after realization;
- the signal changes the frozen evidence state beyond `CAPEX_ONLY` in a way connected to a Marketing decision variable;
- the direction survives the pre-approved outcome, window, source-tier, grouping, and leave-one-stratum checks;
- material counterexamples and trade-offs are reported rather than averaged away.

This would support only the named signal classes and scopes, not the blanket statement that all order-proximate signals are superior.

### 12.2 `REJECTED` / counterevidence

H1 is rejected when, across sufficient `BRIDGE_ELIGIBLE`, matched, and fully observed tracks:

- CAPEX is equal or better on realization/no-realization and scope while offering longer lead; or
- downstream signals add no reproducible information beyond CAPEX; or
- downstream signals are predominantly coincident/lagging confirmations and therefore do not improve decisions at a useful historical point;
- this result remains under the approved robustness checks.

A specific signal class can be rejected even when H1 overall is `QUALIFIED`.

### 12.3 `QUALIFIED`

Use `QUALIFIED` when the trade-off is real and stable but conditional—for example, CAPEX provides longer broad direction while qualification improves product scope with shorter lead, or usefulness differs by product/platform/regime. The conditions must be named; `QUALIFIED` is not a substitute for insufficient evidence.

### 12.4 `INCONCLUSIVE`

No H1 verdict is allowed when any material minimum condition fails, including:

- too few independent comparable tracks;
- too few `BRIDGE_ELIGIBLE` tracks for a direct CAPEX-versus-HBM comparison;
- no fully observed delay, failed/weakened, or no-realization case;
- the primary outcome is too broad or unavailable at product/platform scope;
- right-censored tracks dominate the relevant class;
- signal/stage definitions cannot be made consistent;
- apparent independent evidence is actually one origin group;
- reasonable outcome, date, grouping, or exclusion rules reverse the result;
- historical availability cannot be reconstructed;
- case exclusion or final interpretation lacks human approval.

Any numeric minimum, window, decision band, or robustness pass rule capable of changing the verdict is fixed before analysis and recorded under Gate 5. No threshold may be tuned after seeing the result.

## 13. Robustness plan — design only

| Check | Why it matters |
|---|---|
| Strict O1 only vs O1 plus independent O2/O3 corroboration | Tests whether a verdict depends on accepting issuer-side shipment as enough realization evidence |
| 6/12/18-month outcome windows | Separates near-term non-realization from delayed commercialization |
| Continuous lead intervals vs approved actionability bands | Prevents an arbitrary lead cutoff from creating the result |
| Narrow vs economically adjacent signal grouping | Tests whether combining qualification substages, commitments, or deployment stages hides semantic differences |
| Exact-scope only vs partial-scope inclusion | Shows sensitivity to supplier/product/platform linkage quality |
| `P1_REGULATORY/P1_EVENT/P1_COUNTERPARTY` only vs adding official context | Tests dependence on weaker or broader evidence |
| Date lower bound vs upper bound for imprecise events | Tests event ordering when day-level timing is unknown |
| Leave one supplier/company out | Detects dominance by a disclosure-heavy issuer |
| Leave one product generation/platform out | Detects a famous commercialization path driving the conclusion |
| Delayed as separate vs grouped with no realization | Tests whether timing semantics change the result |
| Alternative right-censor treatment | Ensures incomplete 2025/2026-type tracks are not mislabeled false positives |
| Origin-group deduplication on/off diagnostic | Quantifies how re-reporting could falsely inflate independence; only deduplicated output is admissible |
| Snapshot/revision replay | Confirms later corrections or customer disclosures do not leak backward |

Robustness outputs remain dimension-level tables. They do not justify a composite score.

## 14. AI, deterministic code, and human responsibility

### 14.1 AI/model-assisted candidate work

- discover candidate official sources and possible counterexamples;
- extract candidate atomic excerpts without paraphrasing away stage language;
- propose signal/subtype and entity/product/platform scope;
- identify possible duplicate origins, relations, contradictions, and missing evidence;
- propose `TO_VERIFY`, `KNOWN_UNKNOWN`, or exclusion candidates.

AI output is not an inclusion decision, primary fact approval, case match, or H1 verdict.

### 14.2 Deterministic future program work

- required provenance/schema validation;
- content-hash/revision preservation and origin-group deduplication;
- cutoff, timezone, date-precision, and leakage enforcement;
- track/scope-key joins and duplicate-event handling;
- lead interval, observation-window, realization, delay, and censor calculations;
- reproducible grouping, aggregation, sensitivity runs, and snapshot hashes;
- complete Evidence ID → Source ID → excerpt → locator trace.

### 14.3 Human responsibility

- approve H1 wording, economic scope, outcome hierarchy, and decision interpretation;
- approve track universe, inclusion/exclusion, matching, and source-independence judgments;
- resolve ambiguous stage/scope classifications and consequential `HOLD` records;
- approve dataset freeze before outcome analysis;
- approve sufficiency thresholds, verdict rule, causal-language restrictions, final H1 verdict, and business implication.

The Evidence Governance Harness remains the deterministic rule owner. This design creates no Agent Execution Harness and selects no runtime.

## 15. Public-data limitations and known unknowns

### 15.1 `KNOWN_UNKNOWN`

The public study cannot generally observe or infer:

- customer purchase-order volume, contract price, or supplier share;
- exact customer qualification completion and internal pass/fail criteria when confidential;
- design-in allocation across multiple suppliers;
- product-generation-level HBM revenue or bit shipment for every supplier and quarter;
- internal inventory, yield, cost, wafer starts, CAPA reservation, or contribution margin;
- whether a platform deployment uses a named supplier when the counterparty does not say so;
- site-level energized power, rack utilization, and the exact memory order tied to it;
- quiet cancellations, failed samples, non-announced qualifications, and demand served without disclosure;
- the causal effect of any signal on demand;
- SK hynix's internal forecast, loss function, customer priority, or final allocation decision.

### 15.2 `TO_VERIFY` before implementation

- completeness and stable archival access of supplier IR/product pages across the approved period;
- DART/KRX timestamp and revision metadata needed for non-SEC issuers;
- whether official platform configuration sources explicitly identify HBM generation and supplier often enough for matched tracks;
- whether enough `BRIDGE_ELIGIBLE` tracks connect CSP CAPEX, a named platform/memory generation, and commercial realization without unsupported inference;
- historical utility/operator data that distinguishes permit/PPA from energized or service-ready capacity;
- consistency of HBM revenue/bit-shipment definitions across quarters and suppliers;
- recoverable publication timezone and original file dates for static IR PDFs;
- achievable count of failed/delayed/non-realization tracks under primary-source rules.

The asymmetry between announced successes and silent failures is a structural selection risk. It cannot be fixed by adding more positive press releases.

## 16. Human approval gates

No gate is assumed approved by this document.

### Gate 1 — H1 question, business scope, and population

`HUMAN_APPROVAL_REQUIRED — H1-G01`

Approve or revise: the primary question in Section 1.2; CAPEX as the upstream reference rather than a presumed inferior baseline; decision-useful visibility as a dimension vector; HBM commercialization and explicitly linked AI platform tracks as the population; non-causal interpretation.

### Gate 2 — Outcome contract

`HUMAN_APPROVAL_REQUIRED — H1-G02`

Approve or revise: O1 commercial shipment/customer supply as the primary realization event; the narrow eligibility of volume production linked to actual supply; O2/O3 corroboration; outcome states; prohibition on broad semiconductor revenue and stock price as primary outcomes.

### Gate 3 — Observation unit and case inclusion

`HUMAN_APPROVAL_REQUIRED — H1-G03`

Approve or revise: atomic events nested in hybrid product-commercialization/platform-realization tracks; `BRIDGE_ELIGIBLE` requirement for a direct CAPEX-versus-HBM comparison; quarterly data as corroboration only; proposed 2022-01-01 start; eligible entity/product/platform universe; scope-match, negative-case, duplicate, exclusion, and case-review rules.

### Gate 4 — Source hierarchy and cutoff

`HUMAN_APPROVAL_REQUIRED — H1-G04`

Approve or revise: source tiers; `origin_group` independence; primary-source requirement; `available_at <= cutoff_at`; EDGAR acceptance proxy; conservative next-day availability for date-only sources; timezone, revision, retrospective, and re-reporting rules.

### Gate 5 — Minimum method, windows, sufficiency, and verdict

`HUMAN_APPROVAL_REQUIRED — H1-G05`

Approve or revise: event-chain plus within-track matched comparison; 12-month base and 6/18-month sensitivity windows; continuous lead as primary; minimum multi-stratum/negative-case sufficiency; dimension-level comparison; robustness pass rule; `SUPPORTED/REJECTED/QUALIFIED/INCONCLUSIVE` contract. Exact sample and actionability thresholds must be frozen here after the feasibility manifest.

### Gate 6 — Dataset freeze before outcome analysis

`HUMAN_APPROVAL_REQUIRED — H1-G06`

After implementation and limited data construction, approve the track manifest, source/evidence trace, exclusions/HOLDs, signal dictionary version, historical cutoff snapshots, outcome contract version, and immutable hash before the outcome pass begins. Approval authorizes analysis, not a verdict.

### Gate 7 — Final empirical interpretation

`HUMAN_APPROVAL_REQUIRED — H1-G07`

Approve the final sufficiency decision, counterevidence treatment, robustness interpretation, H1 verdict, scope of generalization, and Marketing implications. AI or deterministic code may calculate candidate results but cannot approve this gate.

## 17. Minimum future dataset specification — conceptual only

No physical schema or data file is created by this design. The primary analytical row is one atomic event; supporting logical records prevent sources, tracks, outcomes, and reviews from being conflated.

### 17.1 Logical records and row definitions

| Logical record | One row means | Primary key / role |
|---|---|---|
| Source manifest | One immutable source revision | `source_id + source_revision_id`; provenance and historical availability |
| Track manifest | One pre-registered product-commercialization or platform-realization track | `track_id`; eligible universe and outcome contract |
| Atomic event | One directly supported signal, outcome, or counterevidence statement at one scope | `event_id`; primary analytical row |
| Cutoff snapshot | One track's eligible source/event set at one historical cutoff | `snapshot_id`; leakage-controlled state and hash |
| Outcome evaluation | One event-to-outcome-window evaluation under one specification | `evaluation_id`; derived lead/status/censor result |
| Review record | One append-only human decision about track/event/exclusion/freeze/verdict | `review_id`; responsibility and approval trace |

### 17.2 Required conceptual fields

| Field group | Required fields |
|---|---|
| Dataset/version | `dataset_version`, `contract_version`, `signal_dictionary_version`, `outcome_contract_version`, `created_at`, `snapshot_hash` |
| Identifiers | `track_id`, `track_stratum`, `event_id`, `evidence_id`, `source_id`, `source_revision_id`, `origin_group`, `target_outcome_id`, `counterevidence_ids` |
| Entity/scope | `supplier`, `customer_if_disclosed`, `platform`, `memory_product`, `product_generation`, `geography`, `stated_scope`, `scope_match`, `bridge_eligibility`, `bridge_evidence_ids` |
| Event role | `record_role` = `SIGNAL/OUTCOME/COUNTEREVIDENCE/CONTEXT`, `signal_class`, `signal_subtype`, `direction`, `economic_stage`, `information_distance`, `observed_statement` |
| Dates | `event_at_lower`, `event_at_upper`, `expected_event_at`, `published_at`, `available_at`, `accessed_at`, `publisher_timezone`, `date_precision`, `cutoff_at` |
| Outcome | `outcome_level`, `outcome_state`, `outcome_event_at_lower`, `outcome_event_at_upper`, `window_start`, `window_end`, `extended_window_end` |
| Derived timing | `lead_days_lower`, `lead_days_upper`, `precedence_status`, `realization_within_window`, `delayed`, `right_censored`, `fully_observed` |
| Source/provenance | `publisher`, `title`, `url_or_archive`, `source_tier`, `original_excerpt`, `locator`, `content_sha256`, `evidence_level`, `independent_origin_count` |
| Inclusion/exclusion | `eligibility_status`, `inclusion_reason`, `exclusion_code`, `duplicate_of`, `scope_conflict`, `date_conflict`, `missing_required_field` |
| Decision context | `decision_variable_candidates`, `capex_only_state`, `updated_state_candidate`, `incremental_information_note`, `known_unknowns` |
| Review | `review_scope`, `reviewer`, `decision` = `APPROVE/HOLD/REJECT`, `reason`, `reviewed_at`, `approval_gate_id`, `run_or_snapshot_id` |

Derived fields must retain formula/specification version and input IDs. Unknown customer, volume, price, share, or qualification status remains null plus `KNOWN_UNKNOWN`; it is never inferred to complete a row.

## 18. Application-evidence artifact map — future only

The following future artifacts could demonstrate capabilities only after approved execution. This task does not claim they exist or prove performance.

| Future artifact | Capability it could demonstrate |
|---|---|
| Approved H1/outcome/signal contract | Economic problem framing and semiconductor commercialization-stage discipline |
| Immutable source and cutoff manifest | Temporal data discipline, provenance, and leakage prevention |
| Track inclusion/exclusion review log | Selection-bias control and human judgment transparency |
| Atomic event and contradiction trace | AI-assisted research with evidence governance |
| Matched event-chain result and counterexamples | Hypothesis testing and counterevidence handling |
| Robustness/specification table | Sensitivity analysis and refusal to overclaim small public samples |
| Human-approved verdict and decision-state changes | Evidence-driven decision revision and Marketing translation |
| Failure/regression cases created during execution | Reproducible correction of AI or deterministic workflow failures |

Resume, cover-letter, or interview prose remains downstream and must use only actually executed, source-traced facts.

## 19. Design acceptance checklist

A reviewer should be able to answer from this document:

- realized demand is O1 commercial realization, optionally corroborated by O2/O3, with unresolved scope preserved;
- a signal is an atomic, historically available public event assigned independently of its later outcome;
- better visibility is a vector of lead, realization, false-positive risk, scope, stability, incremental information, and availability;
- the unit is a hybrid track with atomic events, not a convenient quarter row;
- future knowledge is blocked by immutable `available_at` cutoff snapshots and source revisions;
- false positives require full observation, delays and censoring are separate, and quiet failures remain a limitation;
- cases arise from an approved universe before outcome review;
- support, rejection, qualification, and inconclusive patterns are explicit;
- every consequential choice is routed through H1-G01 to H1-G07;
- the design may legitimately end in `INCONCLUSIVE`.

## 20. Exactly one proposed next implementation task

After Gates 1–5 are approved, implement **only the H1 measurement-contract records and deterministic cutoff/snapshot validation with synthetic or tiny hand-authored fixtures**, including provenance, revision, origin-group deduplication, leakage rejection, censor flags, and replay-hash tests. Do not collect the full historical dataset or calculate an H1 verdict in that task.
