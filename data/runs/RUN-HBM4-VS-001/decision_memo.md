# Draft Decision Memo — HBM4 Sample to Qualification Gate

Run ID: `RUN-HBM4-VS-001`
Review status: `PENDING_HUMAN_REVIEW`

## 1. WHAT CHANGED?
HBM4 moved to customer sample delivery, while customer certification and mass-production preparation remained subsequent gates.

## 2. EVIDENCE LEVEL
A_DIRECT_FACT, B_COMPANY_CLAIM

## 3. WHY DOES IT MATTER?
The event improves visibility into qualification and TTM work, but does not establish qualified demand, committed volume, or commercial shipment.

## 4. DEMAND OR SUPPLY?
BOTH

## 5. WHICH TRANSMISSION PATH CHANGED?
The retrieved 2-hop transmission subgraph contains:
- `EDGE-AI-PLATFORM-REQUIRES-HBM4`
- `EDGE-CUSTOMER-AFFECTS-PRIORITY`
- `EDGE-CUSTOMER-EVALUATES-AI-PLATFORM`
- `EDGE-CUSTOMER-RECEIVES-HBM4-SAMPLE`
- `EDGE-HBM4-REQUIRES-QUALIFICATION`
- `EDGE-QUALIFICATION-AFFECTS-DEMAND-FORECAST`
- `EDGE-QUALIFICATION-AFFECTS-DV`
- `EDGE-QUALIFICATION-GATES-TTM`

## 6. CURRENT BOTTLENECK CANDIDATE
CUSTOMER_QUALIFICATION

## 7. WHICH ASSUMPTION CHANGED?
Sample shipment must not be treated as completed qualification or confirmed commercial volume; an industry-first claim must not be treated as commercial leadership.

## 8. WHICH MARKETING DECISION VARIABLE IS AFFECTED?
CUSTOMER_PRIORITY, DEMAND_FORECAST, QUALIFICATION, SUPPLY_RISK, TTM

## 9. CONFIDENCE
MEDIUM — One first-party source directly distinguishes samples from a pending certification step, but provides no independent confirmation or commercial volume. This is not a probability.

## 10. COUNTEREVIDENCE / OPEN CONTRADICTIONS
- `CONTRA-FIRST-IS-NOT-COMMERCIAL-LEADERSHIP`
- `CONTRA-QUALIFICATION-IS-NOT-VOLUME`
- `CONTRA-SAMPLE-IS-NOT-QUALIFICATION`

## 11. WHAT WOULD INVALIDATE THIS?
- A dated official record shows qualification was already complete at the sample-announcement date.
- A customer or shipment record demonstrates that the announced samples were already commercial volume.

## 12. WHAT TO MONITOR NEXT?
- Customer qualification completion or approved-vendor status
- Design-in or platform-specific adoption
- Commercial shipment and committed price/volume
- Mass-production ramp and qualified good-volume evidence

## 13. SOURCE / EVIDENCE TRACE
- `EVD-HBM4-CERTIFICATION-PENDING` → `SRC-SKH-20250319-HBM4-SAMPLE` → excerpt stored → body paragraph 2 → https://news.skhynix.com/en/sk-hynix-ships-worlds-first-12-layer-hbm4-samples-to-customers/
- `EVD-HBM4-INDUSTRY-FIRST-CLAIM` → `SRC-SKH-20250319-HBM4-SAMPLE` → excerpt stored → headline; body paragraph 1 → https://news.skhynix.com/en/sk-hynix-ships-worlds-first-12-layer-hbm4-samples-to-customers/
- `EVD-HBM4-MASS-PRODUCTION-TARGET` → `SRC-SKH-20250319-HBM4-SAMPLE` → excerpt stored → News Highlights; body paragraph 2 → https://news.skhynix.com/en/sk-hynix-ships-worlds-first-12-layer-hbm4-samples-to-customers/
- `EVD-HBM4-SAMPLE-SHIPMENT` → `SRC-SKH-20250319-HBM4-SAMPLE` → excerpt stored → headline; body paragraphs 1-2 → https://news.skhynix.com/en/sk-hynix-ships-worlds-first-12-layer-hbm4-samples-to-customers/

### Fact statements
- SK hynix reported delivery of 12-layer HBM4 samples to major customers. [`EVD-HBM4-SAMPLE-SHIPMENT`]
- The announcement described customer certification as a next process rather than completed qualification. [`EVD-HBM4-CERTIFICATION-PENDING`]
- The announcement stated a target to complete mass-production preparations in the second half of 2025. [`EVD-HBM4-MASS-PRODUCTION-TARGET`]
- The publisher presented the sample provision as first in the world. [`EVD-HBM4-INDUSTRY-FIRST-CLAIM`]
