# H1 Public-Data Feasibility Manifest

**Record scope updated 2026-10-07:** This is the pre-approval feasibility review dated below. Its unapproved proposal labels describe that review stage. Later Gates 1–5 approval is recorded in the [frozen empirical contract](h1_empirical_validation_design.md); human Gate 6 freeze remains pending. Current work is routed through [the reference index](../../reference_index.md).

## 0. Status and scope

**Review date:** 2026-08-28  
**Task type:** limited public-data feasibility review  
**Empirical status:** no H1 dataset, backtest, signal ranking, lead-time calculation, false-positive rate, or H1 verdict was produced  
**Feasibility classification:** `FEASIBLE_ONLY_AS_TWO_STRATA`

This manifest asks whether a credible, historically timestamped candidate population can be constructed without first selecting known commercialization successes. It does not label any candidate as realized, failed, or predictive. References to later-stage source wording are used only to assess whether the outcome contract could be observed; they are not track outcomes.

The review preserves the provisional contracts in the empirical design:

- `O1_COMMERCIAL_REALIZATION` requires commercial shipment, customer supply, or current volume/mass production explicitly linked in the same source to current customer supply.
- O1 does not establish customer consumption, sustained volume, price, share, or causality.
- `PRODUCT_COMMERCIALIZATION_TRACK` and `CUSTOMER_PLATFORM_REALIZATION_TRACK` remain distinct.
- Quarterly disclosures are context, not independent events.
- `NOT_DISCLOSED` is not `NO_REALIZATION`.

Gates 3–5 remain unapproved. Every proposed choice or threshold in Section 12 is marked `HUMAN_APPROVAL_REQUIRED`.

## 1. Method: population before outcomes

### 1.1 Ex-ante inclusion rules

The candidate universe was formed before any realization label was assigned.

`PRODUCT_COMMERCIALIZATION_TRACK` candidates meet all of the following:

1. supplier is one of the three publicly reporting HBM suppliers with accessible official archives: SK hynix, Samsung Electronics, or Micron;
2. product generation is HBM3 or later and has an official product, IR, or regulatory disclosure dated from 2022-01-01 through the review date;
3. the disclosure identifies the supplier and HBM generation; and
4. inclusion does not require a known later outcome.

`CUSTOMER_PLATFORM_REALIZATION_TRACK` candidates meet all of the following:

1. entity is a major reporting CSP with recurring CAPEX disclosure and named NVIDIA accelerator infrastructure, or Meta as a major reporting internal AI-infrastructure operator;
2. the platform is a separately announced H100, H200, B200, or GB200 generation/SKU during the period;
3. an official platform, cloud-availability, engineering, earnings, or regulatory source family is accessible; and
4. inclusion does not depend on whether the platform later became generally available.

This produces a finite feasibility universe of **10 product tracks** and **14 customer/platform tracks**. Quarterly observations were not multiplied into extra tracks.

### 1.2 Exclusions made before outcome review

- HBM2E and earlier products are outside the AI-accelerator generation boundary and mostly precede the proposed start.
- Unannounced supplier/customer combinations are excluded.
- Rubin-only future roadmaps without a concrete CSP SKU or installed platform are not platform tracks yet.
- Analyst-estimated supplier share, teardown-derived supplier identity, and market-reputation customer relationships are excluded from bridge closure.
- General data-center construction without a named accelerator platform is context, not a platform track.

### 1.3 Discovery standard and count meaning

Counts in this document mean “a source family appears capable of yielding the named field for this candidate.” They are not counts of positive signals, successful outcomes, independent statistical observations, or final eligible records. A final record would still require archive capture, excerpt, locator, content hash, origin-group deduplication, and cutoff validation.

## 2. Candidate-track manifest

Legend:

- `likely O1`: whether official source families appear capable of exposing the strict O1 wording, not whether O1 occurred.
- `scope link`: feasibility of matching the disclosed signal and outcome at product/platform scope.
- `bridge`: `YES_CANDIDATE`, `NO`, or `TO_VERIFY`; none is promoted to `BRIDGE_ELIGIBLE` in this review.
- `negative/delay`: feasibility of finding explicit negative evidence, not silence.

### 2.1 Product commercialization tracks

| candidate_track_id | track_type | entity/entities | product/platform generation | ex-ante rationale | approximate first public date in boundary | observable signal classes | candidate primary-source families | likely O1 | likely O2/O3 | timestamp quality | scope link | bridge | negative/delay | major limitation |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| P01-SKH-HBM3 | PRODUCT_COMMERCIALIZATION_TRACK | SK hynix | HBM3 / NVIDIA H100 | Public supplier-generation disclosure in 2022 | 2022-03 | DESIGN_IN, QUALIFICATION_STAGE, ORDER_ADJACENT_SUPPLY_COMMITMENT | Supplier press; counterparty platform release | HIGH | O2 MEDIUM; O3 MEDIUM | date | product/platform medium | TO_VERIFY | TO_VERIFY | Development/sample origin is left-truncated before 2022; CSP-instance supplier identity is not established |
| P02-SKH-HBM3E | PRODUCT_COMMERCIALIZATION_TRACK | SK hynix | HBM3E 8H/12H | Official product generation announced in period | 2023-08 | HBM_SAMPLE, QUALIFICATION_STAGE, ORDER_ADJACENT_SUPPLY_COMMITMENT | Supplier press; IR/earnings | HIGH | O2 MEDIUM; O3 MEDIUM | date; filing fallback possible | product high, customer low | TO_VERIFY | NOT_OBSERVABLE | Customer is generally unnamed; official archive is announcement-biased |
| P03-SEC-HBM3E | PRODUCT_COMMERCIALIZATION_TRACK | Samsung Electronics | HBM3E 8H/12H | Official product generation and sampling disclosure | 2023-10 | HBM_SAMPLE, QUALIFICATION_STAGE candidate, ORDER_ADJACENT_SUPPLY_COMMITMENT candidate | Supplier newsroom; DART/earnings | LOW | O2 LOW; O3 LOW | date; DART date-only | product medium | TO_VERIFY | TO_VERIFY | Stage language is inconsistent; strict customer-supply wording may not be public |
| P04-MU-HBM3E | PRODUCT_COMMERCIALIZATION_TRACK | Micron | HBM3E 8H/12H | Official qualification/product disclosure | 2023-07 | HBM_SAMPLE, QUALIFICATION_STAGE, DESIGN_IN, ORDER_ADJACENT_SUPPLY_COMMITMENT | SEC exhibit/8-K; IR press | HIGH | O2 HIGH; O3 MEDIUM | SEC timestamp or date | product/platform high | TO_VERIFY | TO_VERIFY | H200 link is strong at platform family, not necessarily at each CSP instance |
| P05-SKH-HBM4 | PRODUCT_COMMERCIALIZATION_TRACK | SK hynix | HBM4 12H | Official sample disclosure in period | 2025-03 | HBM_SAMPLE, QUALIFICATION_STAGE, ORDER_ADJACENT_SUPPLY_COMMITMENT, LTA candidate | Supplier press; IR/earnings | HIGH | O2 MEDIUM; O3 MEDIUM | date | product high, customer low | TO_VERIFY | TO_VERIFY | Customer qualification, volume, price, and share remain private |
| P06-SEC-HBM4 | PRODUCT_COMMERCIALIZATION_TRACK | Samsung Electronics | HBM4 | Official generation disclosure in period | 2025, exact first-source date TO_VERIFY | HBM_SAMPLE candidate, DESIGN_IN, ORDER_ADJACENT_SUPPLY_COMMITMENT | Supplier newsroom; DART/earnings; official counterparties | HIGH | O2 MEDIUM; O3 LOW | date; DART date-only | product/platform medium | TO_VERIFY | TO_VERIFY | Early source chain and stage wording require archive verification |
| P07-MU-HBM4 | PRODUCT_COMMERCIALIZATION_TRACK | Micron | HBM4 12H | Official sample/product disclosure in period | 2025-06 | HBM_SAMPLE, DESIGN_IN, ORDER_ADJACENT_SUPPLY_COMMITMENT, LTA candidate | SEC exhibit/8-K; IR materials | HIGH | O2 MEDIUM; O3 MEDIUM | SEC timestamp or date | product/platform high | TO_VERIFY | TO_VERIFY | Recent disclosures can be right-censored; contracts are often HBM-family rather than generation-specific |
| P08-SKH-HBM4E | PRODUCT_COMMERCIALIZATION_TRACK | SK hynix | HBM4E 12H | Official sample disclosure exists before review freeze | 2026-06 | HBM_SAMPLE | Supplier press | LOW / right-censored candidate | O2 LOW; O3 LOW | date | product high | NO | NOT_OBSERVABLE | Too recent for 6/12/18-month outcome windows |
| P09-SEC-HBM4E | PRODUCT_COMMERCIALIZATION_TRACK | Samsung Electronics | HBM4E 12H | Official sample disclosure exists before review freeze | 2026-05 | HBM_SAMPLE | Supplier newsroom; DART/earnings | LOW / right-censored candidate | O2 LOW; O3 LOW | date; DART date-only | product high | NO | NOT_OBSERVABLE | Too recent; customer/platform and downstream stages not public at review date |
| P10-MU-HBM4E | PRODUCT_COMMERCIALIZATION_TRACK | Micron | HBM4E | Official development disclosure exists before review freeze | 2026-06 | HBM_SAMPLE candidate, ORDER_ADJACENT_SUPPLY_COMMITMENT candidate | SEC exhibit/8-K; IR materials | LOW / right-censored candidate | O2 LOW; O3 LOW | SEC timestamp | product medium | NO | NOT_OBSERVABLE | Development is not sample; too recent and downstream stage is unavailable |

### 2.2 Customer/platform realization tracks

| candidate_track_id | track_type | entity/entities | product/platform generation | ex-ante rationale | approximate first public date | observable signal classes | candidate primary-source families | likely O1 | likely O2/O3 | timestamp quality | scope link | bridge | negative/delay | major limitation |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| C01-AZ-H100 | CUSTOMER_PLATFORM_REALIZATION_TRACK | Microsoft Azure / NVIDIA | ND H100 v5 | Reporting CSP plus named H100 cloud SKU | 2023 | CSP_CAPEX, AI_INFRA_COMMITMENT, PLATFORM_LAUNCH, PLATFORM_DEPLOYMENT | SEC/earnings; Azure release | N/A supplier-side | O2 HIGH; O3 LOW | timestamp/date | platform high, memory supplier low | TO_VERIFY | TO_VERIFY | Broad Microsoft CAPEX cannot be allocated to this SKU |
| C02-AZ-H200 | CUSTOMER_PLATFORM_REALIZATION_TRACK | Microsoft Azure / NVIDIA | ND H200 v5 | Separately announced H200 SKU | 2024 | CSP_CAPEX, AI_INFRA_COMMITMENT, PLATFORM_LAUNCH, PLATFORM_DEPLOYMENT | SEC/earnings; Azure release | N/A supplier-side | O2 HIGH; O3 LOW | timestamp/date | platform high, memory supplier medium | TO_VERIFY | TO_VERIFY | HBM generation is known; installed supplier lot is not |
| C03-GCP-H100 | CUSTOMER_PLATFORM_REALIZATION_TRACK | Google Cloud / NVIDIA | A3 H100 | Reporting CSP plus named H100 cloud SKU | 2023 | CSP_CAPEX, AI_INFRA_COMMITMENT, PLATFORM_LAUNCH, PLATFORM_DEPLOYMENT | SEC/earnings; Google Cloud release | N/A supplier-side | O2 HIGH; O3 LOW | timestamp/date | platform high, memory supplier low | TO_VERIFY | TO_VERIFY | Alphabet CAPEX covers internal and external workloads and multiple asset classes |
| C04-GCP-H200 | CUSTOMER_PLATFORM_REALIZATION_TRACK | Google Cloud / NVIDIA | A3 Ultra H200 | Separately announced H200 SKU | 2024 | CSP_CAPEX, AI_INFRA_COMMITMENT, PLATFORM_LAUNCH, PLATFORM_DEPLOYMENT | SEC/earnings; Google Cloud release | N/A supplier-side | O2 HIGH; O3 LOW | timestamp/date | platform high, memory supplier medium | TO_VERIFY | OBSERVABLE_CANDIDATE | Capacity/deployment timing is sometimes explicit but not memory-product failure |
| C05-AWS-H100 | CUSTOMER_PLATFORM_REALIZATION_TRACK | AWS / NVIDIA | EC2 P5 H100 | Reporting CSP plus named H100 cloud SKU | 2023 | CSP_CAPEX, AI_INFRA_COMMITMENT, PLATFORM_LAUNCH, PLATFORM_DEPLOYMENT | SEC/earnings; AWS launch release | N/A supplier-side | O2 HIGH; O3 LOW | timestamp/date | platform high, memory supplier low | TO_VERIFY | TO_VERIFY | Amazon investment disclosure is broad; GPU-specific allocation requires verification |
| C06-AWS-H200 | CUSTOMER_PLATFORM_REALIZATION_TRACK | AWS / NVIDIA | EC2 P5e/P5en H200 | Separately announced H200 SKU | 2024 | CSP_CAPEX, AI_INFRA_COMMITMENT, PLATFORM_LAUNCH, PLATFORM_DEPLOYMENT | SEC/earnings; AWS launch release | N/A supplier-side | O2 HIGH; O3 LOW | timestamp/date | platform high, memory supplier medium | TO_VERIFY | TO_VERIFY | Availability may begin through limited Capacity Blocks; scope must be preserved |
| C07-OCI-H100 | CUSTOMER_PLATFORM_REALIZATION_TRACK | Oracle Cloud / NVIDIA | OCI H100 | Reporting CSP plus named H100 cloud offer | 2023 | CSP_CAPEX, AI_INFRA_COMMITMENT, PLATFORM_LAUNCH, PLATFORM_DEPLOYMENT | SEC/earnings; OCI release | N/A supplier-side | O2 HIGH; O3 LOW | timestamp/date | platform high, memory supplier low | TO_VERIFY | TO_VERIFY | Oracle CAPEX and cloud SKU disclosures may have different fiscal/event cadence |
| C08-OCI-H200 | CUSTOMER_PLATFORM_REALIZATION_TRACK | Oracle Cloud / NVIDIA | OCI H200 | Separately announced H200 cloud offer | 2024 | CSP_CAPEX, AI_INFRA_COMMITMENT, PLATFORM_LAUNCH, PLATFORM_DEPLOYMENT | SEC/earnings; OCI release | N/A supplier-side | O2 MEDIUM | timestamp/date | platform medium, memory supplier medium | TO_VERIFY | TO_VERIFY | “orderable,” planned GA, and GA must remain distinct |
| C09-META-H100 | CUSTOMER_PLATFORM_REALIZATION_TRACK | Meta / NVIDIA | Internal H100 clusters | Major reporter with named installed H100 fleet | 2023 | CSP_CAPEX, AI_INFRA_COMMITMENT, PLATFORM_DEPLOYMENT | SEC/earnings; Meta engineering | N/A supplier-side | O2 HIGH internal; O3 LOW | timestamp/date | platform high, memory supplier low | TO_VERIFY | TO_VERIFY | Internal deployment is not a customer-available cloud service |
| C10-AZ-GB200 | CUSTOMER_PLATFORM_REALIZATION_TRACK | Microsoft Azure / NVIDIA | ND GB200 v6 | Reporting CSP plus named Blackwell SKU | 2024-03 | CSP_CAPEX, AI_INFRA_COMMITMENT, PLATFORM_LAUNCH, PLATFORM_DEPLOYMENT, POWER_DC_READY candidate | SEC/earnings; Azure/Microsoft release | N/A supplier-side | O2 HIGH; O3 LOW | timestamp/date | platform high, memory supplier low | TO_VERIFY | OBSERVABLE_CANDIDATE | Preview, online cluster, and customer availability are different events |
| C11-GCP-B200 | CUSTOMER_PLATFORM_REALIZATION_TRACK | Google Cloud / NVIDIA | A4 B200 / A4X GB200 | Reporting CSP plus named Blackwell SKU | 2025-01 | CSP_CAPEX, AI_INFRA_COMMITMENT, PLATFORM_LAUNCH, PLATFORM_DEPLOYMENT | SEC/earnings; Google Cloud release | N/A supplier-side | O2 HIGH; O3 LOW | timestamp/date | platform high, memory supplier low | TO_VERIFY | OBSERVABLE_CANDIDATE | A4 and A4X have different preview/GA dates; must not be merged |
| C12-AWS-B200 | CUSTOMER_PLATFORM_REALIZATION_TRACK | AWS / NVIDIA | EC2 P6-B200 / P6e-GB200 | Reporting CSP plus named Blackwell SKU | 2025-05 | CSP_CAPEX, AI_INFRA_COMMITMENT, PLATFORM_LAUNCH, PLATFORM_DEPLOYMENT | SEC/earnings; AWS launch release | N/A supplier-side | O2 HIGH; O3 LOW | timestamp/date | platform high, memory supplier low | TO_VERIFY | OBSERVABLE_CANDIDATE | B200 and GB200 are separate SKUs; later source cannot backdate availability |
| C13-OCI-B200 | CUSTOMER_PLATFORM_REALIZATION_TRACK | Oracle Cloud / NVIDIA | OCI B200 / GB200 | Reporting CSP plus named Blackwell offers | 2024-10 | CSP_CAPEX, AI_INFRA_COMMITMENT, PLATFORM_LAUNCH, PLATFORM_DEPLOYMENT, POWER_DC_READY candidate | SEC/earnings; OCI release | N/A supplier-side | O2 MEDIUM | timestamp/date | platform medium, memory supplier low | TO_VERIFY | OBSERVABLE_CANDIDATE | “taking orders,” planned GA, actual GA, and dedicated-region deployment differ |
| C14-META-GB200 | CUSTOMER_PLATFORM_REALIZATION_TRACK | Meta / NVIDIA | Catalina GB200 rack | Major reporter with named installed Blackwell infrastructure | 2025 | CSP_CAPEX, AI_INFRA_COMMITMENT, PLATFORM_DEPLOYMENT, POWER_DC_READY candidate | SEC/earnings; Meta engineering | N/A supplier-side | O2 HIGH internal; O3 LOW | timestamp/date | platform high, memory supplier low | TO_VERIFY | OBSERVABLE_CANDIDATE | Internal fleet has no cloud-availability outcome; memory supplier remains unnamed |

### 2.3 Population result

| Track type | Candidate count | What the count establishes | What it does not establish |
|---|---:|---|---|
| PRODUCT_COMMERCIALIZATION_TRACK | 10 | A finite, supplier/product-generation universe can be enumerated without requiring a known outcome | Comparable stage disclosure or enough negative cases |
| CUSTOMER_PLATFORM_REALIZATION_TRACK | 14 | Named platform tracks can be enumerated across five reporting operators and multiple accelerator generations | CAPEX allocated to each platform or memory supplier identity |
| Total | 24 | A human-reviewable feasibility population exists | A final analytical sample or independent event count |

## 3. F1 — Product-track population feasibility

The product population is feasible at a small descriptive scale. Official supplier archives expose product-generation announcements across all three suppliers, and O1-compatible wording appears in the source families often enough to make strict outcome verification possible for some older tracks. However:

- suppliers disclose stages unevenly;
- a product release may skip sample, qualification, or customer identity;
- Samsung strict O1 and negative-stage disclosure appear less consistent than SK hynix and Micron;
- HBM4E candidates are structurally right-censored at the review date; and
- the 2022 start left-truncates pre-announcement stages for HBM3.

The ten candidates are sufficient to test data construction feasibility. They are not sufficient by themselves to claim signal superiority, especially if explicit negative cases remain absent.

## 4. F2 — CSP/platform population feasibility

The platform population is feasible separately. Microsoft, Alphabet, Amazon, Oracle, and Meta provide recurring official CAPEX/infrastructure materials, while their cloud or engineering sites identify named H100, H200, and Blackwell deployments. O2-style platform availability or installed infrastructure is generally more observable than the supplier identity of HBM in a specific deployment.

The main scope problem is not the absence of CAPEX or platform events; it is their mismatch. CAPEX is usually company-wide or data-center/AI-wide, whereas platform releases are SKU-, region-, or internal-cluster-specific. The two may coexist in a company timeline without proving that a CAPEX event funded a specific platform.

## 5. F3 — Bridge feasibility

### 5.1 Result

- Potential bridge candidates discovered: **14** platform tracks.
- Fully defensible bridges closed in this feasibility review: **0**.
- Current status: **too sparse for the primary H1 comparison**.
- Manifest status: all 14 remain `TO_VERIFY`; none is `YES_CANDIDATE`.

The count of 14 means each platform has a plausible primary-source search path, not that the bridge exists.

### 5.2 Candidate bridge groups and weakest links

| Candidate group | Count | Why it might qualify | Weakest link | Can primary evidence plausibly close it? |
|---|---:|---|---|---|
| CSP H100 offers plus SK hynix HBM3/H100 disclosure | 5 | Official supplier source links HBM3 to NVIDIA H100; CSP/Meta sources identify H100 infrastructure | HBM generation/supplier → exact CSP deployment; CAPEX → platform | Sometimes at platform-family level; exact deployed supplier lot is unlikely to be public |
| CSP H200 offers plus Micron HBM3E/H200 disclosure | 4 | Micron official release links its HBM3E to NVIDIA H200; CSP sources identify H200 offers | CAPEX → named H200 SKU; supplier → exact CSP deployment | Platform-family link is plausible; CSP-specific supplier identity remains unlikely |
| CSP/Meta Blackwell offers plus supplier design-in disclosures | 5 | Official platform pages state B200/GB200 and HBM3E; some supplier sources identify Blackwell design-ins | CAPEX → platform and exact supplier → deployed platform | Platform generation can be closed; exact supplier/customer instance usually cannot |

The provenance standard must not be weakened by substituting market share, reputation, or presumed sole sourcing. Direct CAPEX-versus-HBM comparison therefore cannot be the required primary estimand on present evidence. Bridge candidates can remain an exploratory corroboration layer and may be promoted only after their complete primary-source chain is independently verified.

## 6. F4 — Negative and delayed-case feasibility

### 6.1 Explicit-negative candidates found

Limited discovery found **three independent origin families** that can seed a negative/delay search:

1. NVIDIA official financial commentary around a Blackwell mask change and changed production-shipment timing;
2. Alphabet official earnings commentary that capacity constraints and deployment timing separate investment from revenue capacity; and
3. Microsoft official earnings commentary describing capacity constraints despite continued infrastructure investment.

These are feasibility candidates only. They are mostly platform/company-scope delays or constraints, not public supplier-product qualification failures, cancellations, or fully observed no-realization cases.

### 6.2 Structural disclosure bias

| Negative type | Public observability | Feasibility assessment |
|---|---|---|
| Explicit platform delay or schedule revision | MEDIUM | Official issuer materials sometimes disclose it, especially when financially material |
| Reduced infrastructure scope/guidance | MEDIUM | Earnings guidance can expose it, but scope is usually broad |
| Product qualification difficulty | LOW | Customer and supplier rarely disclose named failures at product/customer scope |
| HBM cancellation or withdrawn customer order | LOW | Commercial confidentiality makes systematic coverage unlikely |
| Fully observed no-realization | LOW | Absence of a later announcement cannot prove no realization |
| Private qualification or commercial terms | NOT DISCLOSED by design | Must remain `KNOWN_UNKNOWN`, not a negative case |

The present public archive does **not** appear sufficient to guarantee a balanced product-level negative sample. The design can preserve explicit delay evidence where available, but it must not calculate a product false-positive rate from announcement silence. A product-stratum comparative verdict must be forced to `INCONCLUSIVE` if the approved explicit-negative threshold cannot be met.

## 7. F5 — Signal-class feasibility

Counts are potential observability across the 24 candidates. One disclosure may support more than one candidate but remains one origin group for independence.

| Signal class | Candidate tracks potentially observable | Likely primary source family | Date quality | Scope quality | Main disclosure bias | Negative-case observability | Recommended H1 role | Reason |
|---|---:|---|---|---|---|---|---|---|
| CSP_CAPEX | 14 | SEC/earnings/annual reports | timestamp/date | company/broad | Asset mix and workload mix often undisclosed | MEDIUM | PRIMARY | Common upstream reference, but never a memory order proxy |
| AI_INFRA_COMMITMENT | 14 | Earnings, official infrastructure announcements | timestamp/date | company/platform | Plans and intended capacity are announced more often than pushouts | MEDIUM | PRIMARY | More AI-specific than broad CAPEX and observable across operators |
| PLATFORM_LAUNCH | 14 | CSP/cloud and accelerator releases | date | platform | Preview and roadmap announcements are publication-biased | MEDIUM | PRIMARY | Named platform scope is usually reconstructable |
| PLATFORM_DEPLOYMENT | 14 | GA releases, engineering posts, official availability pages | date | platform/region | Limited availability may be presented as broad launch | MEDIUM | PRIMARY | O2-style realization is relatively observable if preview/GA are separated |
| HBM_SAMPLE | 8 | Supplier product releases; SEC exhibits | timestamp/date | product | Successful samples are announced; unsuccessful samples are not | LOW | PRIMARY | Most common product-stage signal, with explicit publication-bias caveat |
| QUALIFICATION_STAGE | 4 | Supplier/counterparty release; SEC exhibit | timestamp/date | product/platform | Private, inconsistent verbs; planned/underway/complete often blurred | LOW | SECONDARY | Too sparse for a required cross-supplier class but valuable when explicit |
| DESIGN_IN | 5 | Supplier and platform counterparty releases | timestamp/date | product/platform | Named wins are preferentially disclosed | LOW | SECONDARY | Strong scope when jointly confirmed, insufficiently common alone |
| LTA_COMMERCIAL_COMMITMENT | 2 | Earnings/SEC/DART | timestamp/date | HBM family/company | Terms and generation scope are private; “interest” is not signed LTA | LOW | DROP_CANDIDATE | Too sparse and inconsistent as a standalone minimum-H1 signal class |
| ORDER_ADJACENT_SUPPLY_COMMITMENT | 6 | Earnings and supplier releases | timestamp/date | product/HBM family | Sold-out/supply-discussion language can lack customer, volume, and binding status | LOW | SECONDARY | Preserve explicit records but do not equate them with orders or LTA |
| POWER_DC_READY | 3 | Operator engineering, utility/commissioning, cloud availability | date | site/platform at best | Permits, PPAs, construction, powered racks, and service availability are conflated | MEDIUM | DROP_CANDIDATE | Too sparse and scope-incompatible for H1 minimum; retain for later H2/context research |
| PRICING_INVENTORY_CONTEXT | 10 | Supplier earnings/SEC/DART | timestamp/date | company/product family/broad | Market commentary cannot identify a track outcome | MEDIUM | CONTEXT | Useful regime context only; quarterly rows are not independent events |

### Recommended keep/drop/downgrade summary

- Keep as `PRIMARY`: `CSP_CAPEX`, `AI_INFRA_COMMITMENT`, `PLATFORM_LAUNCH`, `PLATFORM_DEPLOYMENT`, `HBM_SAMPLE`.
- Downgrade to `SECONDARY`: `QUALIFICATION_STAGE`, `DESIGN_IN`, `ORDER_ADJACENT_SUPPLY_COMMITMENT`.
- Keep as `CONTEXT`: `PRICING_INVENTORY_CONTEXT`.
- `DROP_CANDIDATE` from the minimum H1 comparison: `LTA_COMMERCIAL_COMMITMENT`, `POWER_DC_READY`. An explicitly verified record may still be retained descriptively without reviving the signal class as primary.

This does not rank signal quality. It limits the design to classes that can be populated without pretending private disclosures are systematic.

## 8. F6 — Outcome observability

| Outcome layer | Feasibility | What is observable | Main limitation |
|---|---|---|---|
| O1_COMMERCIAL_REALIZATION | MEDIUM | Strict customer-supply or commercial/volume shipment wording appears in official supplier families for older HBM tracks | “Mass production,” “ramp,” “ready,” and “shipment planned” are not O1 unless current customer supply is explicit; supplier disclosure is uneven |
| O2_CUSTOMER_PLATFORM_DEPLOYMENT | HIGH within platform stratum | Named preview, GA, region availability, installed internal cluster, and current customer use can be separated | Does not identify the HBM supplier, memory order, utilization, or end-customer consumption |
| O3_REVENUE_OR_RAMP_CORROBORATION | MEDIUM at supplier/company level; LOW by generation | HBM-family revenue/ramp and AI-infrastructure financial context appear in filings and earnings | Usually too broad to attribute to a product generation or customer; corroboration only |

Vocabulary must be stored literally before mapping:

- `mass/volume production planned` → not O1;
- `mass-production readiness` → not O1;
- `mass/volume production commenced` without current customer supply → production-stage fact, not automatically O1;
- `for supply to a customer from [current period]` or `commercial/volume shipments commenced` → O1 candidate;
- `ramp` → context unless the same source satisfies O1 wording;
- `preview`, `orderable`, `GA`, `service available`, and `installed internal cluster` → distinct O2 subtypes.

## 9. F7 — Historical timestamp feasibility

| Source family | Recoverable availability | Quality | Required fallback/limitation |
|---|---|---|---|
| SEC filings and filed exhibits | EDGAR acceptance datetime plus accession/revision history | timestamp/high | Use SEC `accepted` time; a later exhibit copy does not backdate the source |
| DART/OpenDART | receipt date, report ID, correction markers | date/medium | Public API commonly exposes date rather than publication time; use conservative next-day availability |
| Official supplier releases | displayed publication date; sometimes separate filed exhibit | date/medium | Use next-day availability unless a filed exhibit or auditable timestamp exists |
| Earnings materials/transcripts | scheduled event time, posted materials, or filed exhibit | timestamp/date | Use official event time only when shown; otherwise SEC acceptance or next-day fallback |
| Platform/cloud releases | displayed publication date and named launch status | date/medium | Use next-day fallback; later-edited availability pages require revision capture |
| CSP disclosures | earnings event time and SEC filing metadata; engineering/blog date | timestamp/date | Do not infer first availability from search-engine crawl dates |

Historical ordering is feasible if the final collection contract archives each retrieved revision and applies conservative date-only rules. Exact first-byte publication time is not consistently recoverable. That limitation is manageable for 6/12/18-month windows but can affect same-day ordering and short lead calculations.

Official timestamp anchors include the SEC [Financial Statement Data Sets](https://www.sec.gov/file/financial-statement-data-sets), SEC [EDGAR access guidance](https://www.sec.gov/search-filings/edgar-search-assistance/accessing-edgar-data), and OpenDART [disclosure-list API guide](https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS001&apiId=2019001).

## 10. F8 — Observation-window feasibility

No event-to-outcome durations were calculated. The recommendation is structural:

- **6 months:** plausible as a short-window sensitivity for qualification, design-in, launch, and customer-supply transitions; too short for many CAPEX-to-deployment paths.
- **12 months:** plausible base window spanning several quarterly disclosure cycles while retaining a meaningful signal-to-realization interval.
- **18 months:** necessary sensitivity for infrastructure and delayed commercialization, but reduces the number of recent fully observed tracks.

The final dataset freeze must be separated from the latest fully observed eligibility date. A track whose follow-up window is incomplete remains right-censored and descriptive; it cannot enter a no-realization denominator.

## 11. Historical-boundary recommendation

`HUMAN_APPROVAL_REQUIRED — H1-F-G03-01`

**Recommend keeping 2022-01-01.** It preserves the SK hynix HBM3/H100 commercialization-era anchor and earlier-cycle/CAPEX context, and official archives are accessible enough for date-level reconstruction. Moving later would improve HBM3E cross-supplier comparability but remove the only in-boundary HBM3 anchor and useful regime context. Moving earlier would add HBM2E and pre-H100 events with weaker comparability and is not necessary for the minimum feasibility population.

The HBM3 track must explicitly carry left-truncation because its development/sample origin predates 2022.

## 12. Recommended human choices for Gates 3–5

These are review inputs, not approvals.

### Gate 3 — boundary, universe, tracks, and bridge

`HUMAN_APPROVAL_REQUIRED — H1-F-G03-01`

- Freeze historical start at 2022-01-01.
- Product universe: official HBM3-or-later generation disclosures by SK hynix, Samsung Electronics, and Micron during the boundary.
- Platform universe: named H100/H200/B200/GB200 offers or installed infrastructure from Microsoft, Alphabet, Amazon, Oracle, and Meta during the boundary.
- Carry left truncation and right censoring explicitly; do not exclude a candidate because a later outcome is unknown.

`HUMAN_APPROVAL_REQUIRED — H1-F-G03-02`

- Freeze two separate primary strata: product commercialization and customer/platform realization.
- Remove `BRIDGE_ELIGIBLE` as a required primary H1 comparison.
- Retain bridge analysis as exploratory corroboration only after the full primary-source chain closes. Until then, do not issue a blanket CAPEX-versus-downstream superiority verdict.

### Gate 4 — source hierarchy and cutoff

`HUMAN_APPROVAL_REQUIRED — H1-F-G04-01`

- `P1_REGULATORY`: SEC/DART/exchange filings and filed exhibits.
- `P1_EVENT`: official earnings, product, platform, cloud-launch, and engineering event releases containing direct event facts.
- `P1_COUNTERPARTY`: official evidence from a named platform/customer/supplier counterparty.
- `P2_OFFICIAL_CONTEXT`: government, utility, standards body, official aggregate research, and company editorial/technology context that does not itself establish the event.
- `S1_INDUSTRY` and `S2_ESTIMATE`: discovery/terminology only; never eligibility, bridge closure, outcome, or independence.
- Same-origin mirrors and re-reports count as one origin group.

`HUMAN_APPROVAL_REQUIRED — H1-F-G04-02`

- SEC availability equals EDGAR acceptance datetime.
- DART and official pages with only a date become eligible at 00:00 on the next calendar day in publisher local time.
- Official earnings event time may be used only when the publisher displays it; otherwise use filed-exhibit acceptance or the next-day rule.
- Revisions receive a new `available_at` and never overwrite an earlier snapshot.

`HUMAN_APPROVAL_REQUIRED — H1-F-G04-03`

- Exclude search-engine crawl timestamps, secondary transcript timestamps, analyst-estimated customer/supplier identity, teardown inference, and market-share-based bridge claims.
- Downgrade company newsroom/editorial pages to `P2_OFFICIAL_CONTEXT` unless their text directly records the event; an “industry-first” or leadership phrase remains a company claim.

### Gate 5 — minimum feasibility thresholds and analysis boundary

`HUMAN_APPROVAL_REQUIRED — H1-F-G05-01`

- A product-stratum verdict requires at least **6 fully traceable, fully observed product tracks spanning all 3 suppliers**, with no supplier contributing more than half of eligible tracks.

`HUMAN_APPROVAL_REQUIRED — H1-F-G05-02`

- A platform-stratum verdict requires at least **8 fully traceable, fully observed tracks spanning at least 3 reporting operators and at least 2 accelerator generations**.

`HUMAN_APPROVAL_REQUIRED — H1-F-G05-03`

- Any stratum-level comparative verdict requires at least **2 explicit negative/delayed tracks from at least 2 independent origin groups within that stratum**.
- A product-stratum verdict additionally requires at least **1 product-scope explicit delay, cancellation, qualification problem, reduced scope, or withdrawn guidance**. If this is unavailable, the product comparison is `INCONCLUSIVE`; silence cannot satisfy the threshold.

`HUMAN_APPROVAL_REQUIRED — H1-F-G05-04`

- If a direct bridge comparison is later restored, require at least **4 fully closed bridge tracks spanning at least 2 CSPs and at least 2 independent supplier/platform origin groups**.
- Until that threshold is met, bridge material is descriptive and the direct CAPEX-to-HBM comparison is `INCONCLUSIVE`.

`HUMAN_APPROVAL_REQUIRED — H1-F-G05-05`

- Use 12 months as the base observation window and 6/18 months as pre-frozen sensitivities.
- Exclude right-censored tracks from no-realization/negative denominators while retaining their observed history descriptively.
- Set the latest fully observed eligibility date to `dataset_freeze - applicable_window`; do not relabel recent candidates as failures.

`HUMAN_APPROVAL_REQUIRED — H1-F-G05-06`

- Primary classes: `CSP_CAPEX`, `AI_INFRA_COMMITMENT`, `PLATFORM_LAUNCH`, `PLATFORM_DEPLOYMENT`, `HBM_SAMPLE`.
- Secondary classes: `QUALIFICATION_STAGE`, `DESIGN_IN`, `ORDER_ADJACENT_SUPPLY_COMMITMENT`.
- Context only: `PRICING_INVENTORY_CONTEXT`.
- Drop from the minimum H1 comparison: `LTA_COMMERCIAL_COMMITMENT`, `POWER_DC_READY`.

`HUMAN_APPROVAL_REQUIRED — H1-F-G05-07`

- Force `INCONCLUSIVE` for a stratum when its track minimum, origin diversity, explicit-negative requirement, primary trace, or full follow-up requirement is not met.
- Force the direct H1 comparison to `INCONCLUSIVE` when the bridge threshold is not met, even if both strata contain useful descriptive findings.
- Do not convert O2/O3 corroboration, a graph path, or temporal ordering into O1 or causality.

## 13. Feasibility classification

### `FEASIBLE_ONLY_AS_TWO_STRATA`

The public archive can support a finite product-commercialization population and a finite CSP/platform population with usable historical dates. It cannot currently support a sufficiently populated, provenance-complete bridge from broad CAPEX through a named platform and HBM supplier to strict O1. Product-level negative disclosure is also too sparse to assume that a false-positive comparison will be estimable.

Proceeding is defensible only if the human reviewer freezes the reduced two-strata design, strict source/timestamp rules, minimum diversity requirements, and mandatory `INCONCLUSIVE` conditions. The design should not be made to look feasible by guessing supplier relationships or treating non-observation as failure.

## 14. Representative primary-source anchors used for feasibility

These are discovery anchors, not a final corpus or selected outcome dataset.

### Supplier/product families

- SK hynix HBM3 supplier/platform disclosure: [June 2022 official release](https://news.skhynix.com/en/sk-hynix-to-supply-industrys-first-hbm3-dram-to-nvidia/)
- SK hynix HBM3E sample/evaluation: [August 2023 official release](https://news.skhynix.com/en/sk-hynix-develops-worlds-best-performing-hbm3e/)
- SK hynix HBM3E current production/customer-supply wording family: [March 2024 official release](https://news.skhynix.com/en/sk-hynix-begins-volume-production-of-industry-first-hbm3e/)
- SK hynix HBM4 sample/certification: [March 2025 official release](https://news.skhynix.com/en/sk-hynix-ships-world-first-12-layer-hbm4-samples-to-customers/)
- SK hynix HBM4E sample: [June 2026 official release](https://news.skhynix.com/en/sk-hynix-ships-samples-of-12-layer-next-gen-hbm4e-2/)
- Samsung HBM3E sample: [February 2024 official release](https://news.samsung.com/global/samsung-develops-industry-first-36gb-hbm3e-12h-dram)
- Samsung HBM4 O1-language feasibility: [February 2026 official release](https://news.samsung.com/global/samsung-ships-industry-first-commercial-hbm4-with-ultimate-performance-for-ai-computing)
- Samsung HBM4E sample: [May 2026 official release](https://news.samsung.com/kr/%EC%82%BC%EC%84%B1%EC%A0%84%EC%9E%90-%EC%84%B8%EA%B3%84-%EC%B5%9C%EC%B4%88-hbm4e-12%EB%8B%A8-%EC%83%98%ED%94%8C-%EC%B6%9C%ED%95%98)
- Micron HBM3E production/platform wording family: [February 2024 official release](https://investors.micron.com/news/press-release/2024/Micron-Commences-Volume-Production-of-Industry-Leading-HBM3E-Solution-to-Accelerate-the-Growth-of-AI-02-26-2024/default.aspx)
- Micron HBM4 sample source family: [June 2025 official filing/exhibit](https://investors.micron.com/static-files/23e319ba-a44e-4da4-9462-d4eea7376787)
- Micron HBM4E development source family: [June 2026 official 8-K exhibit](https://investors.micron.com/static-files/f2205e01-6759-4427-8ab1-d70647c3f78f)

### Platform/deployment families

- Azure H100 availability: [official Azure release](https://azure.microsoft.com/en-us/blog/scale-generative-ai-with-new-azure-ai-infrastructure-advancements-and-availability/)
- Azure H200 availability: [official Azure release](https://azure.microsoft.com/en-us/blog/microsoft-launches-latest-azure-virtual-machines-optimized-for-ai-supercomputing-the-nd-h200-v5-series/)
- Azure Blackwell platform: [official Azure announcement](https://azure.microsoft.com/en-us/blog/microsoft-and-nvidia-partnership-continues-to-deliver-on-the-promise-of-ai/)
- Google Cloud A3/H100: [official Google Cloud release](https://cloud.google.com/blog/products/compute/announcing-cloud-tpu-v5e-and-a3-gpus-in-ga)
- Google Cloud A3 Ultra/H200: [official Google Cloud release](https://cloud.google.com/blog/products/compute/a3-ultra-with-nvidia-h200-gpus-are-ga-on-ai-hypercomputer/)
- Google Cloud A4/B200: [official Google Cloud release](https://cloud.google.com/blog/products/compute/google-cloud-goes-to-nvidia-gtc)
- AWS P5/H100: [official AWS release](https://aws.amazon.com/about-aws/whats-new/2023/07/amazon-ec2-p5-instances-generative-ai-hpc-generally-available/)
- AWS P5e/H200: [official AWS release](https://aws.amazon.com/about-aws/whats-new/2024/09/amazon-ec2-p5e-instances-ec2-capacity-blocks/)
- AWS P6/B200: [official AWS release](https://aws.amazon.com/blogs/aws/new-amazon-ec2-p6-b200-instances-powered-by-nvidia-blackwell-gpus-to-accelerate-ai-innovations/)
- OCI H100: [official OCI release](https://blogs.oracle.com/cloud-infrastructure/general-availability-oci-compute-nvidia-h100)
- OCI H200/Blackwell roadmap and ordering: [official OCI release](https://blogs.oracle.com/cloud-infrastructure/worlds-largest-ai-supercomputer-in-the-cloud)
- Meta H100 installed clusters: [official Meta engineering release](https://engineering.fb.com/2024/03/12/data-center-engineering/building-metas-genai-infrastructure/)
- Meta Blackwell installed infrastructure: [official Meta engineering release](https://engineering.fb.com/2025/09/29/data-infrastructure/metas-infrastructure-evolution-and-the-advent-of-ai/)

### CAPEX and explicit-delay discovery families

- Microsoft CAPEX composition/capacity context: [FY2024 Q4 official earnings](https://www.microsoft.com/en-us/investor/events/fy-2024/earnings-fy-2024-q4)
- Alphabet CAPEX/capacity-deployment context: [2024 Q4 official earnings](https://abc.xyz/investor/events/event-details/2025/2024-Q4-Earnings-Call/)
- Meta CAPEX context: [Q1 2024 filed earnings exhibit](https://investor.fb.com/files/doc_financials/2024/q1/Meta-03-31-2024-Exhibit-99-1_FINAL.pdf)
- NVIDIA Blackwell schedule-change candidate: [FY2025 Q3 official CFO commentary](https://investor.nvidia.com/files/doc_financials/2025/Q325/Q3FY25-CFO-Commentary.pdf)

## 15. Unresolved feasibility gaps

- Exact first official disclosure date for Samsung HBM4 requires archive verification.
- Amazon and Oracle CAPEX events need event-level scope inspection before any platform match.
- No supplier-product explicit cancellation or qualification-failure candidate was verified in this limited pass.
- No candidate bridge has yet closed both broad CAPEX → named platform and exact deployed platform → named HBM supplier.
- Official web pages can be edited; final work requires immutable archive capture, hash, locator, and revision ID.
- HBM4E tracks are right-censored under every proposed observation window at the review date.
- Public evidence cannot reveal customer volume, price, share, yield, cost, or CAPA; these remain `KNOWN_UNKNOWN`.

