# Agent Architecture — Capability-First, Runtime-Agnostic

**Reference scope updated 2026-10-07:** This document preserves design choices and future interfaces. Current learning/data-definition work follows [indicator_collection_purpose.md](research/supply_chain/indicator_collection_purpose.md). An architecture role is not a requirement to install a runtime or implement an execution/evaluation system; see [implementation status](reference_index.md).

## 1. Purpose

The AI architecture exists to support a real analytical problem: public semiconductor signals are heterogeneous in meaning, scope and timing, so the project must determine where each signal sits in the demand/supply transmission chain, what it can and cannot establish, and whether later evidence changes a business decision.

```text
Real decision problem
→ economic / industry model
→ evidence and data
→ AI-assisted research
→ empirical validation
→ decision update
→ project evidence
→ application / interview translation
```

`application_evidence/` is the final downstream layer. It does not choose the analytical question or justify technical complexity.

## 2. Economic core and milestone order

Demand is derived demand:

```text
AI workload / service
→ customer economics
→ CAPEX
→ compute platform
→ memory requirement
→ qualification / commercial confirmation
→ order / shipment
→ realized demand
```

Supply is a binding-constraint problem: a reported shortage is only a candidate until Evidence scopes it to a period and platform and shows that relaxing or tightening it changes downstream realization.

Product mix is an opportunity-cost problem: common constrained resources can change relative economics, but public evidence generally cannot reveal internal yield, contribution margin or allocation. H3 therefore remains a conceptual/`KNOWN_UNKNOWN` framework.

Milestone priority:

1. H1 Demand Signal Quality — primary empirical milestone
2. H2 Bottleneck Migration — secondary extension after H1 credibility
3. H3 Product-Mix Opportunity Cost — deferred empirical claim

## 3. Capability architecture

Whole-project domain selection, decision relevance and module activation are frozen in
`docs/decision_architecture.md`. This document governs execution capabilities; H1 is the first
empirical module, not the boundary of the architecture.

```text
Task request
↓
Agent Execution Harness (future capability)
├─ task framing and smallest-sufficient context
├─ tool and logical-role selection
├─ optional decomposition / parallel delegation
├─ result aggregation and execution trace
└─ failure capture / human escalation
↓
Adapter contract
↓
Evidence Governance Harness (implemented deterministic core)
├─ verify / classify / link
├─ contradiction and signal rules
├─ human review / promotion policy
└─ provenance and replay
↓
Evidence → Graph → Audit → Decision Memo
```

`Evidence` and `Decision Impact` are separate layers. Evidence retains source-backed claims,
scope, date and uncertainty. Decision Impact is a conceptual, human-reviewed translation of a
validated state change into an affected decision, decision horizon, flexibility/commitment,
possible action, missing internal information and invalidation condition. No Decision Engine is
implemented, and a Decision Impact record cannot alter Evidence or promote an inference.

The architecture is runtime-agnostic. Codex-native capabilities, Hermes through an adapter, or another compatible runtime may implement orchestration. A runtime is selected only after an experiment identifies an actual task-decomposition problem and measures incremental value. It never owns Evidence promotion or analytical truth.

## 4. Logical domain roles

Roles preserve domain responsibility without forcing fixed agent processes.

| Logical role | Responsibility | Typical activation condition |
|---|---|---|
| Demand / Platform | Workload, customer economics, CSP investment, accelerator/platform deployment | A demand-chain event or H1 case needs interpretation |
| Memory Product | Product generation, sample, qualification, design-in, shipment and TTM boundaries | A memory commercialization stage is present |
| Supply / Infrastructure | Wafer, good die, base die, packaging/test, power/grid/cooling constraint candidates | A supply or H2 question is in scope |
| Commercial / Policy | LTA, commitments, pricing/inventory, multi-source and policy | Commercial distance or regional risk is material |
| Auditor | Provenance, semantic boundary, contradiction, numeric and unsupported-inference checks | Before promotion or decision use |

The orchestrator activates only the roles needed. Parallel execution is appropriate for independent Source discovery or independent counterevidence searches. Sequentially dependent work—Verify → Classify → Human Review → Promote—remains sequential. Auditor responsibility stays logically separate from market conclusion generation.

## 5. Two different harnesses

| Term | Status | Owns | Must not own |
|---|---|---|---|
| Evidence Governance Harness | Implemented in `src/core/` and `src/pipeline.py` | Schema, provenance, state transitions, contradiction rules, confidence rubric, review manifest, promotion and replay | Task delegation, model runtime, final causal truth |
| Agent Execution Harness | Architectural concept; not implemented | Task framing, context/tool/role selection, optional execution, deterministic pre/postprocessing, trace, eval, failure capture, escalation | Evidence promotion, Harness rule override, final business recommendation |

Keeping the names distinct prevents a model/runtime wrapper from being mistaken for the rule-owning deterministic core.

## 6. Context engineering

Agents receive the smallest sufficient context for the current task.

```text
AGENTS.md                      stable map and invariants
↓
task-relevant master/doc       economic or architecture contract
↓
selected schemas/sources       only the entities, dates and evidence in scope
↓
run-specific subgraph/trace    1–2 hop context and linked excerpts
```

Large Canonical folders and historical application files are not default prompt context. Historical decisions remain discoverable by reference instead of being duplicated into every task. A task trace should record which context IDs/files were selected so context changes can be evaluated.

## 7. Model work vs deterministic program work

| Model-assisted semantic work | Deterministic programmatic work |
|---|---|
| Relevance and scope interpretation | Required-field/schema validation |
| Atomic Evidence candidate extraction | Filtering and deduplication |
| FACT/CLAIM/INFERENCE candidate classification | Date/cutoff alignment and revision preservation |
| Relation candidate generation | Unit normalization, joins and lag construction |
| Contradiction/counterexample discovery | Numeric consistency and aggregation |
| Context-sensitive hypothesis generation | State transition, source trace and replay hash |

Model output remains a candidate until the deterministic contract and required human review are satisfied. The goal is not maximum LLM usage; it is to use probabilistic judgment only where fixed rules are insufficient.

## 8. Agent Evaluation layer — future design only

Software tests answer: **does code follow its specified deterministic rules?**

Agent evals answer: **does the AI-assisted workflow behave correctly on an analytical task?**

Future location:

```text
evals/agent/cases/       versioned minimal cases
evals/agent/manifests/   expected/forbidden behavior and context contract
evals/agent/runs/        runtime output, trace and evaluator decision
```

Future case interface:

```text
eval_id
input_event
allowed_context_refs
available_tools
expected_role_selection
required_trace_fields
forbidden_inferences
expected_human_escalation
evaluator_decision
```

No runner or score is implemented in this task. Any future aggregate result must report case count, runtime/model/config, evaluator rule and failures; an unsupported “accuracy” number is prohibited.

Candidate dimensions:

- source-attribution correctness
- temporal correctness and future-information leakage
- semantic-boundary preservation
- unsupported-inference behavior
- contradiction discovery
- appropriate tool and logical-role selection
- correct human escalation
- context relevance and unnecessary-context avoidance

Initial regression candidates:

| Case | Input | Forbidden inference | Expected behavior |
|---|---|---|---|
| A | `HBM4 samples shipped` | `customer qualification completed` | Preserve sample/qualification boundary and escalate if promotion is requested |
| B | `CSP CAPEX increased` | `memory demand increased proportionally` | Mark CAPEX as upstream/broad and request realization evidence |
| C | `CoWoS shortage reported` | `CoWoS binds every AI platform` | Require period/platform scope and counterevidence |
| D | Evidence reached `HUMAN_REVIEW` | `human approved` | Require an Evidence-level Review Manifest |
| E | A retrieved 2-hop subgraph | `validated single causal path` | Render structural branches without causal overstatement |

Cases D and E originate from observed Vertical Slice failures. They are project assets, not defects to erase from history.

## 9. Failure → Eval → Harness Improvement

```text
Observed failure
→ capture minimal failure case
→ classify failure mode
→ add regression eval
→ modify context / tool / deterministic rule / orchestration
→ rerun eval and software tests
→ document the decision change
```

Failure classes should distinguish at least provenance, temporal leakage, semantic-boundary violation, unsupported inference, wrong tool/role/context, deterministic contract failure and missing human escalation. A fix is incomplete if the minimal failure cannot be replayed.

## 10. Human responsibility

AI may discover, retrieve, extract, classify candidates, connect entities, search for contradictions and generate candidate hypotheses. Humans remain responsible for Strong Inference promotion, causal validity, final H1/H2 verdict, case exclusion and final business-decision framing.

## 11. Superseded and preserved decisions

Superseded:

- Hermes mandatory orchestration → optional runtime/adapter candidate
- fixed agent team → selectively activated logical roles
- ambiguous single Harness → Evidence Governance Harness plus future Agent Execution Harness
- recruiting proof as primary objective → downstream evidence from actual analytical work
- H1/H2 joint MVP → H1 first, H2 after H1 credibility

Preserved:

- deterministic Evidence Governance Harness and evidence-level human review
- Source/Evidence separation and sentence-level provenance
- file-based RAG, Graph and 1–2 hop retrieval
- contradiction preservation and temporal non-overwrite
- Vertical Slice, its failures, corrections and software test history
- no dedicated LLM/Fine-tuning/Vector DB/Graph DB without demonstrated need

## 12. Unresolved architecture questions

- Which H1 tasks, if any, produce enough repeated decomposition value to justify an Agent Execution Harness experiment?
- What human-review record should approve H1 case inclusion and the final hypothesis verdict without overloading Evidence promotion records?
- Which eval dimensions are deterministic assertions and which require a human rubric?
- What minimum improvement would justify Hermes or another runtime over direct Codex-native execution?

These questions must not block H1 empirical design. They should be answered only when an actual H1 workflow exposes the need.
