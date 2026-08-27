# HBM4 Temporal State Diff — 2025 Sample to 2026 Mass Shipment

Baseline: `RUN-HBM4-BASELINE-2025-002`
Update: `RUN-HBM4-TEMPORAL-2026-001`
Reproducibility hash: `52111BFF0AA10AD3BE1EE7B94A1868F0C36122587D129D5D97B1D515619EC340`

## Before State
HBM4 moved to customer sample delivery, while customer certification and mass-production preparation remained subsequent gates.

## New Evidence
- `EVD-HBM4-MASS-SHIPMENT-Q2-2026`: SK hynix reported that it began HBM4 mass shipments in the second quarter of 2026.
- `EVD-HBM4-RAMP-PLAN-H2-2026`: SK hynix stated a plan to ramp HBM4 production in the second half of 2026.

## Changed Evidence Confidence
- `EVD-HBM4-CERTIFICATION-PENDING`: {'score': 0.815, 'label': 'HIGH'} → {'score': 0.765, 'label': 'HIGH'}
- `EVD-HBM4-INDUSTRY-FIRST-CLAIM`: {'score': 0.7275, 'label': 'MEDIUM'} → {'score': 0.6775, 'label': 'MEDIUM'}
- `EVD-HBM4-MASS-PRODUCTION-TARGET`: {'score': 0.7775, 'label': 'HIGH'} → {'score': 0.7275, 'label': 'MEDIUM'}
- `EVD-HBM4-SAMPLE-SHIPMENT`: {'score': 0.815, 'label': 'HIGH'} → {'score': 0.765, 'label': 'HIGH'}

## Changed Graph Edge
- `EDGE-HBM4-ENTERS-MASS-SHIPMENT-Q2-2026`: ADDED
- `EDGE-HBM4-PLANS-RAMP-H2-2026`: ADDED
- `EDGE-MASS-SHIPMENT-AFFECTS-DEMAND-VISIBILITY`: ADDED
- `EDGE-MASS-SHIPMENT-AFFECTS-TTM`: ADDED
- `EDGE-RAMP-PLAN-AFFECTS-SUPPLY-RISK`: ADDED
- `EDGE-AI-PLATFORM-REQUIRES-HBM4`: UPDATED
- `EDGE-CUSTOMER-AFFECTS-PRIORITY`: UPDATED
- `EDGE-CUSTOMER-EVALUATES-AI-PLATFORM`: UPDATED
- `EDGE-CUSTOMER-RECEIVES-HBM4-SAMPLE`: UPDATED
- `EDGE-HBM4-REQUIRES-QUALIFICATION`: UPDATED
- `EDGE-QUALIFICATION-AFFECTS-DEMAND-FORECAST`: UPDATED
- `EDGE-QUALIFICATION-AFFECTS-DV`: UPDATED
- `EDGE-QUALIFICATION-GATES-TTM`: UPDATED
- `EDGE-TTM-AFFECTS-DV`: UPDATED

## Changed Decision Variable
- `DEMAND_FORECAST`: Commercial visibility moved from sample-stage evidence to an observed mass-shipment signal, without enough data to estimate volume.
- `SUPPLY_RISK`: Mass-shipment start reduces uncertainty about initial production readiness; H2 ramp execution and qualified-good-volume remain open.
- `TTM`: The state moved from a mass-production preparation target to an observed mass-shipment event.

## Still Unknown
- customer qualification completion/status
- customer identity and customer share
- HBM4 price or contract terms
- mass-shipment volume and qualified-good-volume

## Invalidation Condition
- SK hynix corrects or retracts the Q2 2026 mass-shipment statement.
- The reported mass shipment is shown to refer only to non-commercial samples.
