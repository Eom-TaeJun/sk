# Active Execution Plan — H1 Two-Strata Demand Signal Quality Empirical Design

## 0. Document status and boundary

**Status:** `GATES_1_TO_5_APPROVED_AND_FROZEN — MINIMUM_CONTRACT_IMPLEMENTATION_APPROVED`

**Human freeze note (2026-08-28):** The limited public-data review in [`h1_feasibility_manifest.md`](./h1_feasibility_manifest.md) found a finite product universe and a finite platform universe but no provenance-complete CAPEX → platform → named HBM supplier → supplier-side realization bridge. Human review therefore froze H1 as two separate primary strata. Gates 1–5 are approved and frozen; Gates 6–7 remain pending. This document authorizes only the next task named in Section 20, not source collection or empirical H1 execution.

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

### 1.2 Overall H1 question — frozen

> How does the decision value of publicly observable AI-memory signals change as evidence moves closer to operational or commercial realization, particularly in the trade-off between lead time, scope precision, and realization uncertainty?

This is not a causal question, does not create a universal signal ranking, and does not assert that downstream signals are always superior. The overall question is answered through two related but non-pooled strata.

#### H1-P — Product Commercialization Stratum

```text
HBM product introduction / sample
→ qualification / design-in
→ commercial or supply commitment
→ supplier-side commercial realization
```

> Within pre-registered HBM product-generation tracks, what additional commercialization visibility does each publicly observed product-stage signal provide, and how much lead remains before supplier-side commercial realization?

The primary outcome is `O1_COMMERCIAL_REALIZATION`, interpreted only as a public supplier-side commercial-realization proxy.

#### H1-C — Customer / Platform Realization Stratum

```text
CSP CAPEX
→ AI infrastructure commitment
→ named platform launch
→ operational deployment / availability
```

> Within pre-registered CSP/platform tracks, what additional deployment visibility does each successive public signal provide beyond broad CAPEX, and how does that trade off against remaining lead time?

The primary outcome is the separate `P1_PLATFORM_OPERATIONAL_REALIZATION`. Supplier-side O1 is not the platform-stratum outcome.

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

The minimum validation should report, without combining the strata or dimensions into a score:

1. H1-P: within a pre-registered product track, what incremental product-stage scope and commercialization visibility is added by sample, qualification, design-in, or an observed supply commitment before O1?
2. H1-P: do observed product-stage signals retain positive lead before O1, or are they mostly coincident/lagging confirmation?
3. H1-C: within a pre-registered platform track, what deployment visibility is added as evidence moves from CAPEX to infrastructure commitment, launch, and operational availability before P1?
4. H1-C: how do lead, scope, and realization uncertainty trade off across successive public platform stages?
5. Within each stratum, does the descriptive pattern differ by supplier/operator, generation, period, or source restriction?
6. Does either stratum fail its approved sufficiency rules and therefore require `INCONCLUSIVE`?

## 2. Empirical estimands and cross-strata boundary

The minimum design estimates two descriptive signal-usefulness patterns, not a causal coefficient.

**H1-P estimand:** for a pre-registered supplier/product-generation track and O1 contract, how early and at what product scope was each publicly observable product-stage signal seen before later supplier-side realization, delay, weakening, non-realization within a fully observed window, or censoring?

**H1-C estimand:** for a pre-registered CSP/platform track and P1 contract, what deployment information was added as the public state moved from broad CAPEX to AI-infrastructure commitment, named platform launch, and operational availability, and how much lead remained at each stage?

The principal comparisons are **within the same eligible track and within the same stratum**. Cross-company summaries are secondary because disclosure practices, product definitions, customer confidentiality, and fiscal calendars differ.

The study must not directly calculate CAPEX-versus-HBM_SAMPLE superiority, CAPEX-versus-qualification accuracy, a pooled signal ranking, or a pooled outcome. Cross-strata synthesis may later discuss the conceptual upstream/downstream trade-off, but only after separate empirical results exist. `WATCH → PREPARE → PRIORITIZE → CONFIRM` may be proposed only if those later results support the states; it is not hard-coded here.

## 3. Outcome contracts by stratum

### 3.1 Why one convenient variable is inadequate

No public variable perfectly measures realized AI-memory demand. Commercial shipment is close to supplier realization but may still reflect supply readiness, channel movement, or a self-reported milestone. Platform deployment is closer to customer use but often cannot be linked to a named memory supplier. HBM revenue or bit shipment confirms economic realization at a broader scope but is disclosed inconsistently. Broad semiconductor revenue has low product specificity and is not an acceptable primary outcome.

The recommended contract therefore uses a strict primary event plus independent corroboration levels.

### 3.2 Candidate outcomes

| Candidate | Construct validity | Observability / frequency | Product specificity | Comparability and revision risk | Demand vs supply ambiguity | Recommendation |
|---|---|---|---|---|---|---|
| Commercial shipment or customer supply explicitly commenced | High for supplier-side commercial realization when the statement is about an occurred event | Irregular official product/IR event | Usually high | Wording differs by supplier; later restatement must not overwrite the original | Still does not prove customer consumption, repeat volume, price, or share | Primary event when occurrence, product, and scope are explicit |
| Volume production explicitly linked to present customer supply | Medium-high | Irregular official product/IR event | High | `volume production`, `ramp`, and `mass production` are not standardized | Can be manufacturing capability if no actual supply is stated | Eligible only when the same source directly links production to current supply/shipment; otherwise a signal, not outcome |
| Product-specific shipment/ramp realization disclosed in earnings | Medium-high | Quarterly when disclosed | Medium-high | Voluntary disclosure can disappear or change definition | Better economic confirmation, but may aggregate generations/customers | Operational corroboration |
| Customer/platform operational deployment or availability | High for platform realization | Irregular platform/cloud release | Platform high; supplier often low | Preview, capacity block, GA, installed infrastructure, configuration, and region can differ | Confirms the stated platform state, not utilization or a named supplier's volume | Separate H1-C `P1_PLATFORM_OPERATIONAL_REALIZATION`; never substitute it for product O1 |
| Product-specific HBM revenue or bit-shipment realization | Medium | Quarterly/annual but inconsistent | Often product family rather than generation | Definitions and mix vary across companies | Reflects price, mix, and supply as well as demand | Financial corroboration, not sole primary outcome unless specificity is adequate |
| Broad DRAM, semiconductor, data-center, or cloud revenue | Low for the target construct | Quarterly | Low | Accounting definitions are stable within company but not the target product | Many non-HBM drivers | Context only; rejected as primary outcome |
| Equity price or market capitalization | Very low | Daily | None | Market expectations and macro factors dominate | Not demand realization | Excluded |

### 3.3 H1-P outcome hierarchy — frozen

The product stratum preserves separate evidence levels rather than manufacturing one pseudo-precise demand target.

1. **`O1_COMMERCIAL_REALIZATION`** — an official supplier-side source states that commercial shipment, customer supply, or mass/volume production explicitly linked in the same source to current customer supply of the identified HBM product has begun. A plan, target, readiness statement, sample shipment, or qualification activity does not qualify.
2. **`O2_OPERATIONAL_CORROBORATION`** — a separate official origin confirms product-specific shipment/ramp or a counterparty platform event directly linked to the product generation. It corroborates O1 but is not a substitute for O1 and does not retroactively change the earlier signal's evidence level.
3. **`O3_FINANCIAL_CORROBORATION`** — an official result reports product-specific HBM revenue, bit shipment, or ramp contribution at a scope compatible with the track. Broad company revenue cannot qualify.

O1 is a **public supplier-side commercial-realization proxy**. It does not establish end-customer consumption, sustained volume, contract price, customer share, or causal demand.

H1-P outcome states are:

- `REALIZED_CORROBORATED`: O1 plus at least one independent O2 or O3 origin with compatible scope;
- `REALIZED_SINGLE_ORIGIN`: O1 is present but independent corroboration is unavailable;
- `DELAYED`: O1 occurs after the approved 12-month base window but within the approved 18-month sensitivity window;
- `NO_REALIZATION_WITHIN_WINDOW`: no O1 occurs during a fully elapsed window; this is a public-observation state, not proof that demand never existed;
- `FAILED_OR_WEAKENED`: an official source reports cancellation, reduction, qualification failure, or a materially weaker scope;
- `RIGHT_CENSORED`: the required follow-up period has not elapsed at dataset freeze;
- `UNRESOLVED`: public evidence conflicts or is too ambiguous to assign another state.

### 3.4 H1-C platform outcome — frozen

**`P1_PLATFORM_OPERATIONAL_REALIZATION`** is the platform-stratum outcome. It records the latest directly supported operational state without treating the following states as equivalent:

- `PLANNED_AVAILABILITY`;
- `PREVIEW`;
- `LIMITED_AVAILABILITY_OR_CAPACITY_BLOCK`;
- `GENERAL_AVAILABILITY`;
- `INSTALLED_OR_OPERATIONAL_INFRASTRUCTURE`.

The exact P1-eligible state is retained rather than collapsed. Planned availability is not realization. Preview is not GA. Capacity Blocks are not unrestricted GA. Internal installed infrastructure is not a customer-available cloud service. The minimum analysis may compare time to each declared state but must state which state is used in each platform track's approved outcome contract.

H1-C outcome states use the same delay, weakening, right-censoring, and unresolved semantics as H1-P, but they are evaluated against the approved P1 subtype rather than O1. Supplier-side HBM O1 must not be used as the H1-C outcome.

Later evidence may update a track in a later dataset version, but it must not overwrite the earlier snapshot. Gate 2 approved the product O1/O2/O3 contract and the separate P1 platform outcome; the Gate 5 freeze approved the windows and sufficiency treatment.

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

### 4.1 Frozen minimum-design roles

- H1-P primary: `HBM_SAMPLE`.
- H1-P secondary when observed: `QUALIFICATION_STAGE`, `DESIGN_IN`, `ORDER_ADJACENT_SUPPLY_COMMITMENT`. Their absence is not imputed, and they are not required to appear uniformly.
- H1-C primary: `CSP_CAPEX`, `AI_INFRA_COMMITMENT`, `PLATFORM_LAUNCH`, `PLATFORM_DEPLOYMENT`.
- Context only: `PRICING_INVENTORY_CONTEXT`.
- Removed from the minimum H1 comparison: `LTA_COMMERCIAL_COMMITMENT`, `POWER_DC_READY` because public observability and compatible scope are too sparse. An isolated verified event may remain descriptive evidence but cannot recreate a removed primary class. `POWER_DC_READY` remains relevant to later H2 work.

`SHIPMENT_REALIZATION` remains an outcome-role event, not a predictor. Signal roles are frozen by Gate 5 and do not imply an empirical ranking.

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
- `CUSTOMER_PLATFORM_REALIZATION_TRACK`: reporting operator + named platform/deployment scope; it does not require a named memory supplier.

Quarterly company/industry observations are corroborating context, not extra independent product events. Multiple excerpts from the same origin and event do not increase sample size.

The minimum design uses two parallel event-chain strata. H1-P compares product-stage evidence only within product tracks and against O1. H1-C compares successive CAPEX/infrastructure/platform states only within platform tracks and against P1. Quarterly product-specific operational or financial disclosures corroborate realization but are not extra independent events.

Product-commercialization tracks may contain strong downstream stages but no defensible CSP CAPEX link; platform tracks may contain CAPEX and deployment but no named memory supplier. Gate 3 therefore removed `BRIDGE_ELIGIBLE` as a required primary comparison. A complete bridge may be retained as exploratory corroboration only when primary evidence independently closes every link. Market share, reputation, presumed sole sourcing, analyst estimates, and teardown inference cannot close it.

**Gate status:** Gate 3 approved and froze this two-strata observation architecture.

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

For each eligible H1-P track:

- retain each distinct product signal stage and historical availability date;
- observe O1 and any independent O2/O3 corroboration under the frozen contract;
- calculate lead-time intervals and fully observed no-realization/delay/censor flags;
- record what each newly observed product stage added to scope and commercialization visibility; and
- preserve counterevidence and semantic boundaries.

For each eligible H1-C track:

- establish the earliest eligible CSP CAPEX state at its directly stated scope;
- retain distinct AI-infrastructure commitment, named platform launch, and deployment/availability stages;
- observe the approved P1 subtype without collapsing preview, limited availability, GA, or installed internal infrastructure;
- calculate lead-time intervals and fully observed no-realization/delay/censor flags; and
- record what changed from `CAPEX_ONLY` at each successive historical snapshot.

No track must contain every signal class. Absence of a public disclosure is `NOT_OBSERVED_PUBLICLY`, not evidence that the real-world event did not happen. H1-P and H1-C results are never pooled. A bridge has no role in minimum-design eligibility or verdict sufficiency.

### 6.3 Primary outputs

The future minimum result should report:

- eligible tracks and their inclusion/exclusion trace;
- per-signal-class `eligible`, `realized`, `no realization within window`, `delayed`, `failed/weakened`, and `right-censored` counts;
- lead-time median/range only when dates and sample count make them meaningful, otherwise event-level intervals;
- exact/partial/broad scope-match distribution;
- within-track evidence-state changes relative to CAPEX-only;
- counterexamples and leave-one-stratum robustness;
- separate human-approved H1-P and H1-C `SUPPORTED`, `REJECTED`, `QUALIFIED`, or `INCONCLUSIVE` verdicts when their respective Gate 5 sufficiency rules are met.

No overall H1 verdict is required. Useful findings in one stratum and `INCONCLUSIVE` in the other are a valid result.

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

**Gate status:** Gate 4 approved and froze the tiers, origin-group independence, and secondary-source restrictions.

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

**Gate status:** Gate 4 approved and froze cutoff semantics and the conservative date-only rule.

## 9. Ex-ante case inclusion and exclusion contract

### 9.1 Approved eligible universe

The historical boundary starts at **2022-01-01** and ends at a future Gate 6 dataset freeze. The start retains HBM3/H100-era evidence and earlier regime context while avoiding materially earlier HBM generations with weaker comparability. HBM3 tracks whose origin predates the boundary carry explicit left truncation.

The H1-P product universe is official HBM3-or-later product-generation disclosure by:

- SK hynix;
- Samsung Electronics; and
- Micron.

The H1-C platform universe is a named H100, H200, B200, or GB200 platform/installed-infrastructure track disclosed by:

- Microsoft / Azure;
- Alphabet / Google;
- Amazon / AWS;
- Oracle; and
- Meta.

Official counterparties, regulators, utilities, or government sources may verify an event within the declared scope but do not create extra tracks by themselves. Tracks are generated from these ex-ante universes, not famous outcomes. Inclusion does not require later realization, and quarterly rows do not multiply independent track counts.

### 9.2 Signal inclusion

An event is eligible when all are true:

- it was public within the approved period;
- it fits a pre-defined signal class/subtype based on direct wording;
- it has Source ID, publisher, URL/archive, excerpt, locator, publication/availability date, hash, tier, origin group, and revision identity;
- its entity/product/platform/geography scope is explicit or marked unknown;
- its direction and stage can be assigned without using later outcomes;
- a primary official source exists, except secondary-source counterexample discovery retained as `TO_VERIFY` and excluded from primary comparison.

### 9.3 Outcome observation window — frozen

The approved contract uses a **12-month base follow-up**, with **6-month and 18-month sensitivity windows**. Twelve months spans multiple quarterly decision cycles while limiting regime drift; six months tests near-term actionability and eighteen months tests delayed realization. These are pre-frozen design choices, not empirically established product-cycle constants.

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

The Gate 5 sufficiency rules are frozen:

- H1-P requires at least 6 fully traceable and fully observed product tracks, all 3 suppliers, and no supplier contributing more than half of eligible tracks.
- H1-C requires at least 8 fully traceable and fully observed platform tracks, at least 3 reporting operators, and at least 2 accelerator generations.
- A comparative verdict within either stratum requires at least 2 explicit negative/delayed tracks from at least 2 independent origin groups in that stratum.
- H1-P additionally requires at least 1 product-scope explicit delay, cancellation, qualification problem, reduced scope, or withdrawn guidance.
- Silence and non-disclosure never satisfy a negative-case requirement.

If a rule is not met, the relevant stratum is `INCONCLUSIVE`. Thresholds cannot be reduced merely to obtain a verdict. Bridge availability is not a Gate 5 requirement.

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

**Gate status:** Gates 3 and 5 approved and froze the boundary, universe, follow-up windows, sufficiency rules, and exclusions.

## 10. Empirical-strategy comparison

| Strategy | Question answered | Data requirement | Identification strength | Main bias | Timing / false positives / censoring | Business interpretability | Public-data fit |
|---|---|---|---|---|---|---|---|
| Structured historical event-chain | What was known at each stage and what happened later? | Atomic dated events with trace | Strong semantic and temporal validity; no causal identification | Publication and successful-event bias | Directly models order and censoring; false positives require a pre-registered universe | High | High for a small sample |
| Within-stratum matched-case comparison | Did successive product stages add visibility within H1-P, or did successive platform stages add visibility beyond CAPEX within H1-C? | Comparable signals/outcomes in the same stratum and tightly matched tracks | Better controls scope than pooled averages | Few matches; human matching choices | Can compare lead and no-realization within a single outcome contract | High | Medium-high |
| Company-quarter panel/time series | Are regular CAPEX/signal measures associated with later aggregate outcomes? | Many consistently defined quarters and numeric outcomes | Potentially estimates average association, not causality | Mixed products, autocorrelation, disclosure breaks, pseudo-sample size | Coarse timing; censoring manageable with enough history | Medium | Low for product-specific H1 now |
| Hybrid event + quarterly corroboration | Do event-stage patterns hold with broader operational/financial confirmation? | Event tracks plus limited regular context | Best construct/feasibility balance; still descriptive | Combines layers with different scope; must not treat them as equal rows | Event layer handles timing/censoring; quarterly layer corroborates | High | Recommended |

### 10.1 Selected strategy

The minimum credible strategy is the two-strata hybrid in Section 6: event-chain core, within-track/within-stratum comparisons, and quarterly corroboration. The two outcomes and signal sets are not pooled. Statistical inference is not justified by the current feasibility population. Code availability is not a reason to prefer a panel or model.

## 11. Proposed empirical methods and permitted interpretation

| Method | Exact problem solved | Required assumptions / minimum structure | Allowed interpretation | Not allowed / recommendation |
|---|---|---|---|---|
| Event-time ordering and lead intervals | Determine whether and how long a signal preceded O1 | Reliable `available_at`, outcome occurrence, scope match; interval dates when imprecise | Historical precedence and observed lead range | No causal claim; primary method |
| Realization/no-realization/delay proportions | Compare observed outcomes by signal class | Pre-registered denominator, fully observed windows, censoring separated | Descriptive frequency in the selected public sample | No population probability or “accuracy” claim with small/selective N; primary method |
| Within-track evidence-state comparison | H1-P: test whether a later product-stage signal added scope or reduced uncertainty; H1-C: test what each platform stage added beyond CAPEX | Same stratum, track/outcome contract, and frozen earlier snapshot | Incremental decision information in that track | No cross-strata coefficient or universal superiority; primary method |
| Within-stratum matched sign/dominance table | Check whether successive signals show a consistent lead/scope/uncertainty trade-off within H1-P or H1-C | Approved matching keys and multiple independent matches within one stratum | Direction and consistency of trade-offs | No pooling or statistical generalization from a few matches; primary method |
| Descriptive Kaplan–Meier/time-to-event | Describe time to realization while retaining right-censored tracks | Enough independent comparable tracks, stable time origin, non-informative censoring plausibly discussed | Conditional descriptive realization curve for the observed sample | No causal hazard interpretation; defer unless feasibility supports it |
| Correlation / cross-correlation | Explore aggregate lead/lag co-movement | Consistent numeric series, stationarity/seasonality treatment, enough periods | Exploratory association only | Not recommended for minimum H1; cannot prove incremental information or causality |
| Regression / panel methods | Estimate conditional association after specified controls | Many comparable independent units/periods, stable definitions, modeled dependence and confounding | Association under stated specification | Not recommended now; public product-level outcome and N are inadequate until proven otherwise |
| LASSO or predictive classification | Select variables or predict a labeled outcome | Large, stable training sample, pre-specified validation split, repeatable features/outcome | Out-of-sample predictive performance only | Rejected for minimum H1: small heterogeneous events would make selection unstable and distract from construct validity |

No p-value, confidence interval, model “accuracy,” or coefficient should be reported unless the later dataset and dependence structure justify it. The absence of a statistical model is not a design failure.

## 12. Separate-stratum falsification and verdict contract

Verdicts apply to the approved public sample and signal classes, not to undisclosed internal orders. H1-P and H1-C receive separate verdicts from the same state set: `SUPPORTED`, `QUALIFIED`, `REJECTED`, or `INCONCLUSIVE`. An overall H1 verdict is optional and must not be forced.

### 12.1 H1-P verdict meaning

- `SUPPORTED`: after the frozen product sufficiency gate is met, one or more observed product-stage classes add reproducible commercialization visibility or tighter product scope before O1 while retaining positive lead; the pattern survives approved robustness checks and material counterexamples remain visible.
- `QUALIFIED`: the product-stage trade-off is stable but conditional by supplier, generation, stage, or window. Conditions must be named.
- `REJECTED`: after the frozen product sufficiency gate is met, the tested product-stage classes add no reproducible pre-O1 information, are mainly coincident/lagging, or fail under the approved robustness checks.
- `INCONCLUSIVE`: the product track, supplier-diversity, explicit-negative, product-scope-negative, trace, follow-up, stage-consistency, or human-approval rule is not met.

H1-P does not compare its product signals directly with CSP CAPEX.

### 12.2 H1-C verdict meaning

- `SUPPORTED`: after the frozen platform sufficiency gate is met, one or more successive platform stages add reproducible deployment scope or reduce realization uncertainty beyond the prior CAPEX-only state while retaining positive lead before P1; the pattern survives approved robustness checks.
- `QUALIFIED`: CAPEX, infrastructure commitment, launch, and deployment show a stable but conditional lead/scope/uncertainty trade-off by operator, platform generation, availability subtype, or window.
- `REJECTED`: after the frozen platform sufficiency gate is met, successive platform stages add no reproducible information beyond CAPEX, are mainly coincident/lagging, or fail under approved robustness checks.
- `INCONCLUSIVE`: the platform track, operator/generation diversity, explicit-negative, trace, follow-up, P1-state consistency, or human-approval rule is not met.

### 12.3 Cross-strata synthesis boundary

Cross-strata synthesis may describe the conceptual trade-off that upstream evidence can offer broader/earlier visibility while downstream evidence can offer tighter/closer realization scope. It must not pool O1 and P1, calculate CAPEX-versus-HBM signal superiority, or produce one signal ranking. `WATCH → PREPARE → PRIORITIZE → CONFIRM` may be used only if later results empirically support those decision states.

The project may legitimately end with useful findings in one or both strata and no direct cross-strata superiority verdict.

### 12.4 Frozen `INCONCLUSIVE` safeguards

A stratum is `INCONCLUSIVE` when any material approved minimum condition fails, including its track/diversity threshold, explicit-negative requirement, complete primary trace, full follow-up, consistent signal/outcome definition, origin-group independence, reconstructable historical availability, or required human approval. Right-censored records remain descriptive and cannot satisfy full observation or negative-case requirements.

No threshold may be tuned after seeing results. Bridge scarcity is a documented construct boundary, not a reason to relax provenance or a minimum-design verdict input.

## 13. Robustness plan — design only

| Check | Why it matters |
|---|---|
| Strict O1 only vs O1 plus independent O2/O3 corroboration | Tests whether a verdict depends on accepting issuer-side shipment as enough realization evidence |
| P1 state strictness: preview/limited/GA/installed-operational kept separate | Tests whether a platform finding depends on collapsing materially different availability states |
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
- approve sufficiency decisions, causal-language restrictions, separate final H1-P/H1-C verdicts, any optional cross-strata synthesis, and business implication.

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
- whether any exploratory bridge can close CSP CAPEX, a named platform/memory generation, and commercial realization without unsupported inference; bridge scarcity does not block the two-strata minimum design;
- historical utility/operator data that distinguishes permit/PPA from energized or service-ready capacity;
- consistency of HBM revenue/bit-shipment definitions across quarters and suppliers;
- recoverable publication timezone and original file dates for static IR PDFs;
- achievable count of failed/delayed/non-realization tracks under primary-source rules.

The asymmetry between announced successes and silent failures is a structural selection risk. It cannot be fixed by adding more positive press releases.

## 16. Human approval gates

Gates 1–5 are approved and frozen by human decision on 2026-08-28. They may not be changed during implementation or after outcome inspection without a new explicit human decision and decision-change record.

### Gate 1 — H1 question, business scope, and population

`APPROVED_AND_FROZEN — H1-G01`

Overall H1 and the separate H1-P/H1-C questions in Section 1.2 are non-causal and dimension-based. The design does not assume downstream superiority or create a universal ranking.

### Gate 2 — Outcome contracts

`APPROVED_AND_FROZEN — H1-G02`

H1-P uses strict supplier-side `O1_COMMERCIAL_REALIZATION` with O2/O3 corroboration. H1-C uses separate `P1_PLATFORM_OPERATIONAL_REALIZATION`, preserving planned, preview, limited/capacity-block, GA, and installed/operational states. Broad revenue and equity price are not primary outcomes.

### Gate 3 — Boundary, universe, tracks, and bridge

`APPROVED_AND_FROZEN — H1-G03`

The start is 2022-01-01. H1-P includes official HBM3-or-later generation disclosures from SK hynix, Samsung Electronics, and Micron. H1-C includes named H100/H200/B200/GB200 platform or installed-infrastructure tracks from Microsoft, Alphabet, Amazon, Oracle, and Meta. HBM3 pre-2022 origins carry left truncation. Two primary strata are frozen; bridge material is exploratory corroboration only and cannot be closed by reputation, share estimates, presumed sole sourcing, analyst estimates, or teardown inference.

### Gate 4 — Source hierarchy and historical-information contract

`APPROVED_AND_FROZEN — H1-G04`

The P1/P2/S1/S2 hierarchy, `origin_group` independence, primary-source requirement, `event_at/published_at/available_at/accessed_at` clocks, `available_at <= cutoff_at`, EDGAR acceptance proxy, conservative next-calendar-day rule for date-only sources, revision preservation, and future-information-leakage prohibition are frozen.

### Gate 5 — Signal roles, windows, sufficiency, and verdicts

`APPROVED_AND_FROZEN — H1-G05`

- H1-P: at least 6 fully traceable and observed tracks, all 3 suppliers, and no supplier over half of eligible tracks.
- H1-C: at least 8 fully traceable and observed tracks, at least 3 operators, and at least 2 accelerator generations.
- Each stratum: at least 2 explicit negative/delayed tracks from at least 2 origin groups.
- H1-P additionally: at least 1 product-scope explicit delay/cancellation/qualification problem/reduced scope/withdrawn guidance.
- Windows: 12-month primary, 6/18-month sensitivity; right-censored tracks remain descriptive and never enter negative/no-realization denominators.
- Signal roles are frozen in Section 4.1.
- Verdicts are separate H1-P/H1-C `SUPPORTED/QUALIFIED/REJECTED/INCONCLUSIVE`; unmet sufficiency forces the relevant stratum to `INCONCLUSIVE`.

### Gate 6 — Dataset freeze before outcome analysis

`HUMAN_APPROVAL_REQUIRED — H1-G06`

After implementation and limited data construction, approve the track manifest, source/evidence trace, exclusions/HOLDs, signal dictionary version, historical cutoff snapshots, outcome contract version, and immutable hash before the outcome pass begins. Approval authorizes analysis, not a verdict.

### Gate 7 — Final empirical interpretation

`HUMAN_APPROVAL_REQUIRED — H1-G07`

Approve the final sufficiency decision, counterevidence treatment, robustness interpretation, separate H1-P/H1-C verdicts, scope of generalization, any cross-strata synthesis, and Marketing implications. AI or deterministic code may calculate candidate results but cannot approve this gate.

## 17. Minimum future dataset specification — conceptual only

No physical schema or data file is created by this design. The primary analytical row is one atomic event; supporting logical records prevent sources, tracks, outcomes, and reviews from being conflated.

### 17.1 Logical records and row definitions

| Logical record | One row means | Primary key / role |
|---|---|---|
| Source manifest | One immutable source revision | `source_id + source_revision_id`; provenance and historical availability |
| Track manifest | One pre-registered product-commercialization or customer/platform-realization track | `track_id`; eligible universe, stratum, and O1/P1 outcome contract |
| Atomic event | One directly supported signal, outcome, or counterevidence statement at one scope | `event_id`; primary analytical row |
| Cutoff snapshot | One track's eligible source/event set at one historical cutoff | `snapshot_id`; leakage-controlled state and hash |
| Outcome evaluation | One event-to-outcome-window evaluation under one specification | `evaluation_id`; derived lead/status/censor result |
| Review record | One append-only human decision about track/event/exclusion/freeze/verdict | `review_id`; responsibility and approval trace |

### 17.2 Required conceptual fields

| Field group | Required fields |
|---|---|
| Dataset/version | `dataset_version`, `contract_version`, `signal_dictionary_version`, `outcome_contract_version`, `created_at`, `snapshot_hash` |
| Identifiers | `track_id`, `track_stratum`, `event_id`, `evidence_id`, `source_id`, `source_revision_id`, `origin_group`, `target_outcome_id`, `counterevidence_ids` |
| Entity/scope | `supplier`, `customer_if_disclosed`, `platform`, `memory_product`, `product_generation`, `geography`, `stated_scope`, `scope_match`, optional exploratory `bridge_eligibility`, `bridge_evidence_ids` |
| Event role | `record_role` = `SIGNAL/OUTCOME/COUNTEREVIDENCE/CONTEXT`, `signal_class`, `signal_subtype`, `direction`, `economic_stage`, `information_distance`, `observed_statement` |
| Dates | `event_at_lower`, `event_at_upper`, `expected_event_at`, `published_at`, `available_at`, `accessed_at`, `publisher_timezone`, `date_precision`, `cutoff_at` |
| Outcome | `outcome_family` = `O1_PRODUCT/P1_PLATFORM`, `outcome_level`, `platform_realization_subtype`, `outcome_state`, `outcome_event_at_lower`, `outcome_event_at_upper`, `window_start`, `window_end`, `extended_window_end` |
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
| Human-approved H1-P/H1-C verdicts and decision-state changes | Evidence-driven decision revision and Marketing translation without outcome pooling |
| Failure/regression cases created during execution | Reproducible correction of AI or deterministic workflow failures |

Resume, cover-letter, or interview prose remains downstream and must use only actually executed, source-traced facts.

## 19. Design acceptance checklist

A reviewer should be able to answer from this document:

- H1 is frozen as separate product-commercialization and customer/platform-realization strata with no required direct bridge;
- H1-P uses O1 supplier-side commercial realization, optionally corroborated by O2/O3, with unresolved scope preserved;
- H1-C uses separate P1 platform operational realization and keeps planned, preview, limited, GA, and installed/operational states distinct;
- a signal is an atomic, historically available public event assigned independently of its later outcome;
- better visibility is a vector of lead, realization, false-positive risk, scope, stability, incremental information, and availability;
- the units are two non-pooled track strata with atomic events, not convenient quarter rows;
- future knowledge is blocked by immutable `available_at` cutoff snapshots and source revisions;
- false positives require full observation, delays and censoring are separate, and quiet failures remain a limitation;
- cases arise from an approved universe before outcome review;
- separate support, rejection, qualification, and inconclusive patterns are explicit;
- H1-G01 through H1-G05 are frozen; dataset and final-interpretation approvals remain H1-G06 and H1-G07;
- the design may legitimately end with one or both strata `INCONCLUSIVE` and no cross-strata superiority verdict.

## 20. Exactly one approved next task

Implement **only the H1 measurement contract and deterministic validation layer using synthetic or tiny hand-authored fixtures**, including separate H1-P/H1-C outcome contracts, provenance, revision, origin-group deduplication, cutoff/leakage rejection, left-truncation/right-censor flags, and replay-hash tests. Do not collect the historical dataset, calculate lead-time results, classify candidate outcomes, or run empirical H1 in that task.
