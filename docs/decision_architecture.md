# Whole-Project Decision Architecture

**Reference scope updated 2026-10-07:** This is the preserved analytical architecture. The current learning and free-data measurement task is owned by [indicator_collection_purpose.md](research/supply_chain/indicator_collection_purpose.md); these domains are not a simultaneous implementation or collection checklist. See [preserved status and future boundaries](reference_index.md).

## 1. Status and purpose

**Status:** `WHOLE_PROJECT_ARCHITECTURE_FROZEN — H1_FIRST_EMPIRICAL_MODULE`

**Human freeze date:** 2026-08-28

This system is not a single H1 predictor or an HBM-demand model. It is a decision-intelligence framework that structures heterogeneous semiconductor signals by economic transmission path, evidence quality, timing, uncertainty, and decision relevance.

The framework uses public information to support external-signal interpretation, decision preparation, escalation, prioritization, and identification of internal information that must be checked. It cannot make internal company decisions from public data alone and must not invent customer volume, price, share, yield, cost, or capacity allocation.

The project flow is:

```text
Heterogeneous public signal
→ atomic Evidence with provenance
→ economic transmission-path position
→ empirical validation within an approved module
→ uncertainty and competing explanations
→ impact on a realistically adjustable decision
→ human-approved business interpretation
```

H1 supplies the first empirical evidence state—commercialization and deployment visibility. It is one module of this architecture, not the architecture itself.

## 2. Whole-project analytical domains

| Domain | Economic question | Potential evidence | Primary decision relevance | Current status |
|---|---|---|---|---|
| **A. Demand / Customer Economics** | Is underlying demand for AI compute and memory strengthening, weakening, or merely becoming more visible? | CSP CAPEX; AI-infrastructure commitments; credibly scoped AI/cloud revenue or backlog/RPO; utilization or capacity-constraint commentary; platform deployment | Demand Forecast; Customer Monitoring; Customer Priority | H1-C is the minimum empirical module |
| **B. Product Commercialization** | Is a memory product moving from technical possibility toward customer acceptance and commercial realization? | Sample; evaluation; qualification; design-in; commercial/supply commitment; customer supply; shipment; product-compatible revenue or bit-shipment corroboration | Qualification Priority; TTM; Customer Priority; Product/Platform Focus | H1-P is the minimum empirical module |
| **C. Competition / Industrial Organization** | How does competitor progress change the opportunity available to the company even if total demand is unchanged? | Competitor generation, qualification, design-in, production/ramp, officially disclosed customer/platform linkage, capacity commentary, spec/performance differentiation | Customer Priority; qualification urgency; competitive response; product positioning | Future context; not H1 signal-performance input |
| **D. Ecosystem / Partner Dependency** | Can ecosystem readiness prevent technically ready memory from becoming commercially realized? | Accelerator/platform roadmap and availability; advanced packaging context; cloud/platform deployment; OEM/server availability; data-center readiness | TTM; customer timing; supply planning; risk escalation | Activate only for a scoped dependency question |
| **E. Supply / Production Constraints** | Given installed capacity and committed investment, what prevents one additional unit of AI-memory supply from being realized? | Wafer starts; yield; good die; TSV/stacking; advanced packaging; test; equipment; substrate; utilization; capacity/ramp | Supply Risk; tactical capacity/ramp decisions; escalation | Future H2; analyze the **marginal binding constraint**, not a generic important issue |
| **F. Raw Materials / Logistics** | Does a material or logistics shock transmit into the current semiconductor production constraint? | Wafers; gases; chemicals; photoresist; slurry; substrates; directly relevant critical minerals; supplier concentration; lead time; inventory buffer; export/logistics disruption | Procurement or supply-risk escalation only when the path reaches an adjustable constraint | Future H2 input only after transmission-path proof |
| **G. Macro / Policy / Geopolitics** | Does an external rule or macro condition change customer economics, accessible markets, or equipment/material access for the decision under study? | Interest rates; FX; trade policy; export controls; tariffs; sanctions; industrial policy; country restrictions | Investment context; margin/procurement context; accessible-market or supply-risk escalation | Conditional context, never a mandatory feature set |
| **H. Product Mix / Opportunity Cost** | When advanced DRAM resources are scarce, how does greater HBM allocation change the opportunity cost of other memory products? | Credibly scoped shared-resource, allocation, capacity, and contribution-economics evidence | Product Mix; scarce-resource allocation; CAPA trade-off | Future H3; `KNOWN_UNKNOWN` until public or approved internal evidence is sufficient |

Domain C must be interpreted with oligopoly, customer concentration, multi-sourcing, switching and qualification cost, capacity pre-emption, bargaining power, and product differentiation in view. A competitor event does not prove share change by itself.

Domain F admits a price or disruption only through a credible path:

```text
raw-material or logistics shock
→ semiconductor-relevant input availability or cost
→ current marginal production constraint
→ realistically adjustable business decision
```

Rare-earth or critical-mineral prices remain context unless both process directness and constraint relevance are established.

Domain G likewise requires an explicit path. Examples include interest rate → cost of capital → investment intention; FX → procurement/revenue economics → margin or investment context; and export control → market/equipment/material access → demand or supply constraint. Ordinary interest-rate sensitivity must not be presumed for mega-cap hyperscalers without evidence.

## 3. Decision-relevance admission gate

Every proposed variable or dataset must answer all eight questions before entering an empirical dataset:

1. What economic state does the variable measure?
2. Where is it in the transmission path?
3. Is its role `SIGNAL`, `OUTCOME`, `CONTEXT`, or `CONSTRAINT`?
4. What business uncertainty can it reduce?
5. Which decision can it inform?
6. Is that decision realistically adjustable at the relevant horizon?
7. What competing explanation could produce the same observation?
8. What evidence would invalidate the interpretation?

Failure to answer any question means `EXCLUDE_FROM_EMPIRICAL_DATASET` until the missing contract is resolved. Data availability, market popularity, or model convenience is not an admission reason. This gate prevents feature accumulation without a decision purpose.

## 4. Semiconductor decision flexibility

Decision impact depends on adjustment cost, sunk commitment, and horizon. The same Evidence can justify monitoring while remaining far too weak for a capital decision.

| Decision level | Examples | Adjustment characteristics | Public-signal use |
|---|---|---|---|
| **Strategic / highly committed** | New fab; major cleanroom expansion; large long-lead equipment program | Multi-year; high fixed and sunk cost; difficult to reverse | Short-horizon public signals must not directly recommend creation or cancellation |
| **Tactical / partially adjustable** | Equipment-install timing; ramp timing; wafer or product mix; packaging allocation; utilization | Material adjustment cost; partially committed; requires persistent, stronger evidence and internal confirmation | Prepare scenarios, identify escalation triggers, and state required private checks |
| **Commercial / highly adjustable** | Customer monitoring; sample allocation; qualification priority; sales/marketing focus; product/platform priority; TTM escalation | Shorter horizon; comparatively reversible | Primary near-term decision target for H1 |

Conceptual flexibility values are `HIGH`, `MEDIUM`, and `LOW`. Conceptual commitment values are `REVERSIBLE`, `PARTIALLY_COMMITTED`, `HIGHLY_COMMITTED`, and `EFFECTIVELY_IRREVERSIBLE`.

## 5. Evidence and Decision Impact remain separate

Evidence records establish what a source directly supports, when it was available, and where it sits in a transmission path. They do not contain or automatically produce a business recommendation.

A future, human-reviewed Decision Impact record may contain:

- `decision_type`
- `decision_horizon`
- `decision_flexibility`
- `commitment_level`
- `baseline_expectation`
- `supporting_evidence`
- `counterevidence`
- `competitor_context`
- `ecosystem_context`
- `constraint_context`
- `known_unknowns`
- `proposed_decision_update`
- `confidence`
- `human_approval`

This is a documentation contract, not a production Decision Engine. A Decision Impact record must reference governed Evidence IDs, preserve counterevidence and known unknowns, explain adjustability, and require human approval. It must not retroactively alter Evidence classification or confidence.

## 6. H1 as the first empirical module

H1 asks:

> What information reduces commercialization or deployment uncertainty, and how much lead remains when that information becomes public?

H1-P covers two distinct paths that may converge at commercial realization:

```text
Customer / Commercial Acceptance
product introduction or sample
→ evaluation
→ qualification
→ design-in or commercial selection
→ customer supply or commercial realization

Supply Readiness
production readiness
→ production planned
→ mass or volume production start
→ ramp
→ supply capability
```

Qualification reduces technical/customer-acceptance uncertainty. Production start reduces supply-readiness uncertainty. Neither proves customer demand volume. Customer supply is a supplier-side commercialization proxy, not final demand.

H1-C keeps two information states separate:

```text
Investment Context
CSP CAPEX → infrastructure commitment → broad capacity commentary

Operational Deployment
platform announcement → preview → limited availability → general availability → installed or operational infrastructure
```

H1-C asks what platform-specific operational evidence adds beyond broad investment context. CAPEX is not a direct unit measure of HBM demand, and an exact CAPEX → named platform funding bridge requires direct primary evidence.

H1 does **not** determine:

- the marginal production bottleneck;
- the most important raw-material shock;
- which competitor will win share;
- optimal capacity allocation or product mix;
- whether a fab should be built or cancelled;
- the causal effect of CAPEX on HBM demand.

These are later-module or internal-data questions. H1 precedes H2 because it establishes the demand/commercialization side of the decision state, not because it represents the whole project.

## 7. Module activation rules

| Module or domain | Activate when | Do not activate merely because |
|---|---|---|
| Competition | Relative customer/product position is the business question and competitor evidence could change priority even if total demand is unchanged | Competitor news is available |
| Ecosystem / partner dependency | A scoped external dependency may block a technically ready product or alter customer timing | A partner roadmap mentions AI |
| H2 supply/production | Demand/commercialization evidence is positive but realization is delayed, making “what prevents one additional unit of supply?” the active question | Any supply issue is described as important |
| Raw materials / logistics | A shock has a credible path to the current marginal production constraint and an adjustable decision | A commodity price moved |
| Macro | A variable has a defensible transmission path to the decision under study | A macro series is easy to download |
| Geopolitical / policy | Policy changes accessible markets, customer deployment, supplier access, or equipment/material availability | A policy event is broadly semiconductor-related |
| H3 opportunity cost | Public or approved internal evidence can support a scarce-resource allocation and product-mix comparison | HBM and conventional DRAM share some resources in principle |

Activation requires a bounded business question, a valid transmission path, an approved evidence contract, and a realistic adjustable decision. A module remains inactive when those conditions are absent.

## 8. AI, deterministic code, and human authority

AI may discover candidate sources, extract atomic claims, propose classifications and decision-relevance mappings, search for contradictions, and generate minimal regression fixtures.

Deterministic code enforces timestamps, source scope, schema and semantic boundaries, frozen populations, censoring, replay, and non-promotion rules.

Humans retain authority over economic interpretation, track admissibility, competitor/customer relationship interpretation, transmission-path validity, decision flexibility, final H1/H2/H3 conclusions, and business recommendations.

The architecture therefore prepares and disciplines a decision; it does not automate analytical truth or substitute public signals for internal operating data.
