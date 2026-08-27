# Decision Memo — HBM4 Sample Baseline to Mass Shipment Update

Run ID: `RUN-HBM4-TEMPORAL-2026-001`
Review status: `PENDING_HUMAN_REVIEW`

## 1. WHAT CHANGED?
The official state moved from 2025 customer samples and pending certification work to a 2026 company-reported start of HBM4 mass shipments; the H2 production ramp remains a forward-looking company plan.

## 2. EVIDENCE LEVEL
A_DIRECT_FACT, B_COMPANY_CLAIM

## 3. WHY DOES IT MATTER?
Observed mass shipment is closer to commercialization than sample delivery and changes TTM, demand-visibility, and supply-risk judgments, but it does not disclose qualification status, customers, price, or volume.

## 4. DEMAND OR SUPPLY?
BOTH

## 5. WHICH TRANSMISSION PATH CHANGED?
The retrieved 2-hop transmission subgraph contains:
- `EDGE-AI-PLATFORM-REQUIRES-HBM4`
- `EDGE-CUSTOMER-AFFECTS-PRIORITY`
- `EDGE-CUSTOMER-EVALUATES-AI-PLATFORM`
- `EDGE-CUSTOMER-RECEIVES-HBM4-SAMPLE`
- `EDGE-HBM4-ENTERS-MASS-SHIPMENT-Q2-2026`
- `EDGE-HBM4-PLANS-RAMP-H2-2026`
- `EDGE-HBM4-REQUIRES-QUALIFICATION`
- `EDGE-MASS-SHIPMENT-AFFECTS-DEMAND-VISIBILITY`
- `EDGE-MASS-SHIPMENT-AFFECTS-TTM`
- `EDGE-QUALIFICATION-AFFECTS-DEMAND-FORECAST`
- `EDGE-QUALIFICATION-AFFECTS-DV`
- `EDGE-QUALIFICATION-GATES-TTM`
- `EDGE-RAMP-PLAN-AFFECTS-SUPPLY-RISK`

## 6. CURRENT BOTTLENECK CANDIDATE
PRODUCTION_RAMP_EXECUTION; qualification status and qualified-good-volume remain undisclosed.

## 7. WHICH ASSUMPTION CHANGED?
The prior state 'sample delivered, qualification pending' is no longer the latest commercialization state. HBM4 has an observed mass-shipment event, while shipment magnitude and customer economics remain unknown.

## 8. WHICH MARKETING DECISION VARIABLE IS AFFECTED?
DEMAND_FORECAST, SUPPLY_RISK, TTM

## 9. CONFIDENCE
HIGH — Two dated first-party records establish the temporal movement from samples to reported mass shipment. Neither record independently discloses customer qualification, price, customer share, or volume. This is not a probability.

## 10. COUNTEREVIDENCE / OPEN CONTRADICTIONS
- `CONTRA-FIRST-IS-NOT-COMMERCIAL-LEADERSHIP`
- `CONTRA-MASS-SHIPMENT-NO-PRICE-VOLUME-SHARE`
- `CONTRA-QUALIFICATION-IS-NOT-VOLUME`
- `CONTRA-SAMPLE-IS-NOT-QUALIFICATION`

## 11. WHAT WOULD INVALIDATE THIS?
- SK hynix corrects or retracts the statement that HBM4 mass shipments began in Q2 2026.
- The reported category is shown to be non-commercial sample movement rather than mass shipment.

## 12. WHAT TO MONITOR NEXT?
- Actual H2 2026 production-ramp realization
- Customer or platform-specific qualification disclosure
- Commercial shipment volume or mix disclosure
- Price or contract terms from attributable sources

## 13. SOURCE / EVIDENCE TRACE
- `EVD-HBM4-CERTIFICATION-PENDING` → `SRC-SKH-20250319-HBM4-SAMPLE` → excerpt stored → body paragraph 2 → https://news.skhynix.com/en/sk-hynix-ships-worlds-first-12-layer-hbm4-samples-to-customers/
- `EVD-HBM4-MASS-SHIPMENT-Q2-2026` → `SRC-SKH-20260729-HBM4-MASS-SHIPMENT` → excerpt stored → article body, HBM4/HBM4E paragraph, first sentence (web-rendered line 60) → https://news.skhynix.com/en/q2-2026-business-results/
- `EVD-HBM4-RAMP-PLAN-H2-2026` → `SRC-SKH-20260729-HBM4-MASS-SHIPMENT` → excerpt stored → article body, HBM4/HBM4E paragraph, forward-looking clause (web-rendered line 60) → https://news.skhynix.com/en/q2-2026-business-results/
- `EVD-HBM4-SAMPLE-SHIPMENT` → `SRC-SKH-20250319-HBM4-SAMPLE` → excerpt stored → headline; body paragraphs 1-2 → https://news.skhynix.com/en/sk-hynix-ships-worlds-first-12-layer-hbm4-samples-to-customers/

### Fact statements
- In March 2025 SK hynix reported HBM4 sample delivery and described certification as a following process. [`EVD-HBM4-SAMPLE-SHIPMENT`, `EVD-HBM4-CERTIFICATION-PENDING`]
- In July 2026 SK hynix reported that HBM4 mass shipments had begun in the second quarter. [`EVD-HBM4-MASS-SHIPMENT-Q2-2026`]
- The same 2026 release stated a plan to ramp production in the second half. [`EVD-HBM4-RAMP-PLAN-H2-2026`]
