# H1 Decision Memo — Demand Signal Quality Historical Backtest

- Run: `RUN-H1-BACKTEST-001`
- Verdict: **INCONCLUSIVE**
- Question: Do qualification, LTA, power-ready, supply-commitment, and commercial-deployment-adjacent signals provide more stable memory-demand visibility than headline CAPEX?

## Direct Answer

Only 1 fully observed matched track contains both CAPEX and an order-proximate signal; the rule requires 2. The case evidence is useful for stage and timing diagnostics but cannot establish H1 superiority.

## Evidence-backed Findings

- Microsoft's FY2022 datacenter investment evidence was followed by a broad memory downturn and only later by supplier recovery. (`EVT-C1-MSFT-CAPEX`, `EVT-C1-DRAM-DOWNTURN`, `EVT-C1-MEMORY-RECOVERY`)
- Micron's final-stage HBM3E qualification disclosure preceded its volume-production announcement by less than 90 days. (`EVT-C2-MU-HBM3E-QUAL-FINAL`, `EVT-C2-MU-HBM3E-VOLUME`)
- SK hynix HBM3E sample evaluation preceded reported volume production and customer supply by more than 90 days. (`EVT-C2-SKH-HBM3E-SAMPLE`, `EVT-C2-SKH-HBM3E-VOLUME`)
- Microsoft reported power and space constraints after large cloud/AI CAPEX, then later reported powered/chipped readiness and deployed capacity. (`EVT-C3-MSFT-CAPEX`, `EVT-C3-MSFT-POWER-SPACE-SHORT`, `EVT-C3-MSFT-POWER-READY`, `EVT-C3-MSFT-CAPACITY-ONLINE`)
- The 2025 HBM4 sample signal was followed by a supply commitment and a 2026 mass-shipment event, while the newly disclosed LTA remains right-censored. (`EVT-C4-SKH-HBM4-SAMPLE`, `EVT-C4-SKH-HBM4-SUPPLY-COMMITMENT`, `EVT-C4-SKH-LTA`, `EVT-C4-SKH-HBM4-SHIPMENT`)
- Only 1 fully observed track contains both CAPEX and an order-proximate predictor, so the deterministic H1 verdict is INCONCLUSIVE. (`EVT-C3-MSFT-CAPEX`, `EVT-C3-MSFT-POWER-READY`, `EVT-C3-MSFT-CAPACITY-ONLINE`)

## Marketing Decision Implications

- **CAPEX:** WATCH: update long-range direction, but do not confirm customer volume or memory CAPA from spend alone.
- **SAMPLE:** PREPARE: update qualification schedule, target specification, and technical-response priority.
- **QUALIFICATION:** PREPARE: raise customer priority and TTM readiness, without treating it as contracted volume.
- **SUPPLY_COMMITMENT_OR_LTA:** COMMIT_CANDIDATE only after scope and human review; use for price-volume and CAPA reservation scenarios, not disclosed allocation percentages.
- **POWER_READY:** COMMIT_CANDIDATE when operational readiness is source-backed; update deployment timing and regional supply risk.
- **SHIPMENT:** CONFIRMED for commercialization timing and forecast-bias review; shipment is not a predictor in this comparison.

## Counterevidence

- C3 CAPEX was followed by deployed capacity inside 12 months and provided longer lead than the later power-ready statement.
- Micron final-stage qualification provided less than 90 days of lead to volume production.
- The C1 relationship is broad and cannot attribute supplier recovery to one CSP's spend.

## Known Unknowns

- Customer-specific memory order quantities across the four cases
- HBM contract prices and allocation percentages
- Memory content per deployed Microsoft AI-capacity unit
- Forward realization of the July 2026 LTA inside a completed 12-month window
- A second fully observed track containing both CAPEX and an order-proximate signal

## Invalidation Conditions

- A second independently sourced matched track shows CAPEX equal or superior on both false positives and useful lead.
- A primary source correction changes any sample, qualification, LTA, capacity, or shipment stage used here.
- Additional event-time data changes the number of fully observed matched tracks or right-censor status.

## Source / Event Trace

- `EVT-C1-DRAM-DOWNTURN` → `SRC-SKH-20230201-FY22Q4` → article body, paragraph 4 (web-rendered line 48) → https://news.skhynix.com/en/sk-hynix-reports-2022-and-fourth-quarter-financial-results/ → `7D940160D60A5C40758F5FB98BEA173778D4768164375A76655E42352DD12EAD`
- `EVT-C1-MEMORY-RECOVERY` → `SRC-SKH-20240125-FY23Q4` → article body, market recovery paragraph (web-rendered line 46) → https://news.skhynix.com/en/sk-hynix-reports-fourth-quarter-2023-financial-results/ → `6DA412591475438425A02C30A55E60A2F7237EF0340709FA527D4FDFCBE5FCC2`
- `EVT-C1-MSFT-CAPEX` → `SRC-MSFT-20220728-AR22` → Financial Review, Cash Flows Statements, Investing, ‘Additions to property and equipment’ → https://www.microsoft.com/investor/reports/ar22/ → `D60CE13C0F533B50329944C3BD8487EF73D3DAA4780AB8C0614ED25A99B51A17`
- `EVT-C1-MSFT-DC-COMMITMENT` → `SRC-MSFT-20220728-AR22` → Note 7 — Property and Equipment, paragraph after depreciation expense → https://www.microsoft.com/investor/reports/ar22/ → `D60CE13C0F533B50329944C3BD8487EF73D3DAA4780AB8C0614ED25A99B51A17`
- `EVT-C1-SKH-CAPEX-CUT` → `SRC-SKH-20230201-FY22Q4` → article body, investment paragraph (web-rendered line 52) → https://news.skhynix.com/en/sk-hynix-reports-2022-and-fourth-quarter-financial-results/ → `7D940160D60A5C40758F5FB98BEA173778D4768164375A76655E42352DD12EAD`
- `EVT-C2-MU-HBM3E-QUAL-FINAL` → `SRC-MU-20231220-Q1FY24` → fiscal Q1 2024 earnings prepared remarks, HBM3E paragraph → https://investors.micron.com/static-files/25b84c7c-7959-49ef-abb4-e81dea252f32 → `4EACE157E39BB3023498FAF50700A291D65BACB9DC3E24BD1311D10C4D243366`
- `EVT-C2-MU-HBM3E-RAMP-PLAN` → `SRC-MU-20231220-Q1FY24` → fiscal Q1 2024 earnings prepared remarks, HBM3E paragraph → https://investors.micron.com/static-files/25b84c7c-7959-49ef-abb4-e81dea252f32 → `4EACE157E39BB3023498FAF50700A291D65BACB9DC3E24BD1311D10C4D243366`
- `EVT-C2-MU-HBM3E-SAMPLE` → `SRC-MU-20230726-HBM3E-SAMPLE` → opening paragraph → https://investors.micron.com/news/press-release/2023/Micron-Delivers-Industrys-Fastest-Highest-Capacity-HBM-to-Advance-Generative-AI-Innovation-07-26-2023/default.aspx → `B81FF6B7D012E2E8299BF951C0C96B33D1B360C723A393ACB18D1E7CFAD9AC31`
- `EVT-C2-MU-HBM3E-VOLUME` → `SRC-MU-20240226-HBM3E-VOLUME` → opening paragraph (web-rendered line 14) → https://investors.micron.com/news/press-release/2024/Micron-Commences-Volume-Production-of-Industry-Leading-HBM3E-Solution-to-Accelerate-the-Growth-of-AI-02-26-2024/default.aspx → `28B76D28B9489DC11E0DCB41F95420BB5C86A6BFB619005E7C5810366A007364`
- `EVT-C2-SKH-HBM3E-SAMPLE` → `SRC-SKH-20230821-HBM3E-SAMPLE` → article body, first paragraph (web-rendered line 49) → https://news.skhynix.com/en/sk-hynix-develops-worlds-best-performing-hbm3e/ → `6054B7C9DCF18C810A88E8A605494A3181D9117C860153A49470186151F7C697`
- `EVT-C2-SKH-HBM3E-VOLUME` → `SRC-SKH-20240319-HBM3E-VOLUME` → article body, opening paragraph (web-rendered line 49) → https://news.skhynix.com/en/sk-hynix-begins-volume-production-of-industry-first-hbm3e/ → `6EE4D43313FFD3ADE9E93D4C831AD336B44BE5EB075BBA1E4344F36114984A84`
- `EVT-C3-MSFT-AI-REVENUE-RUNRATE` → `SRC-MSFT-20250129-FY25Q2` → CEO prepared remarks (web-rendered lines 31-35) → https://www.microsoft.com/en-us/investor/events/fy-2025/earnings-fy-2025-q2 → `48A5B8131DDFEF20A5AA4203B109EACDA620634BBFDC0FDCF612C3CEFBC1F902`
- `EVT-C3-MSFT-AZURE-REVENUE` → `SRC-MSFT-20250730-FY25Q4` → CEO prepared remarks (web-rendered lines 37-46) → https://www.microsoft.com/en-us/investor/events/fy-2025/earnings-fy-2025-q4 → `CB8061A7AB83FBB962F3B7B2B15FE6D266F07BC0F5253AAEF5DC32BAF3829AE0`
- `EVT-C3-MSFT-CAPACITY-CONSTRAINT` → `SRC-MSFT-20240730-FY24Q4` → Intelligent Cloud results (web-rendered line 233) → https://www.microsoft.com/en-us/investor/events/FY-2024/earnings-fy-2024-q4 → `ED53CDAB8466FF95543C2F800AF167532575920210F5B543E44AE8291E7A9769`
- `EVT-C3-MSFT-CAPACITY-ONLINE` → `SRC-MSFT-20250730-FY25Q4` → CEO prepared remarks (web-rendered lines 50-55) → https://www.microsoft.com/en-us/investor/events/fy-2025/earnings-fy-2025-q4 → `CB8061A7AB83FBB962F3B7B2B15FE6D266F07BC0F5253AAEF5DC32BAF3829AE0`
- `EVT-C3-MSFT-CAPEX` → `SRC-MSFT-20240730-FY24Q4` → CFO results, capital expenditures (web-rendered lines 253-255) → https://www.microsoft.com/en-us/investor/events/FY-2024/earnings-fy-2024-q4 → `ED53CDAB8466FF95543C2F800AF167532575920210F5B543E44AE8291E7A9769`
- `EVT-C3-MSFT-POWER-READY` → `SRC-MSFT-20250304-MORGAN-TMT` → capacity-planning Q&A (web-rendered lines 81-86) → https://www.microsoft.com/en-us/investor/events/fy-2025/morgan-stanley-tmt-conference → `F1A8371AA1E5DF82D4DEE1693C7ACD6589C252DB3CAE5BEF91D589AB604FAAC2`
- `EVT-C3-MSFT-POWER-SPACE-SHORT` → `SRC-MSFT-20250129-FY25Q2` → Q&A, capacity explanation (web-rendered line 301) → https://www.microsoft.com/en-us/investor/events/fy-2025/earnings-fy-2025-q2 → `48A5B8131DDFEF20A5AA4203B109EACDA620634BBFDC0FDCF612C3CEFBC1F902`
- `EVT-C4-SKH-HBM4-QUAL-PENDING` → `SRC-SKH-20250319-HBM4-SAMPLE` → body paragraph 2 → https://news.skhynix.com/en/sk-hynix-ships-worlds-first-12-layer-hbm4-samples-to-customers/ → `E1FA035EA3E4284632CC30722EFA45B05212C79B7BB1D1A4DBA72A4FA2F44020`
- `EVT-C4-SKH-HBM4-SAMPLE` → `SRC-SKH-20250319-HBM4-SAMPLE` → headline; body paragraphs 1-2 → https://news.skhynix.com/en/sk-hynix-ships-worlds-first-12-layer-hbm4-samples-to-customers/ → `E1FA035EA3E4284632CC30722EFA45B05212C79B7BB1D1A4DBA72A4FA2F44020`
- `EVT-C4-SKH-HBM4-SHIPMENT` → `SRC-SKH-20260729-Q2FY26-BACKTEST` → article body, HBM4 paragraph (web-rendered line 60) → https://news.skhynix.com/en/q2-2026-business-results/ → `E7041578BC7861488AEEE91C0154FF372B9DD1B77C8E7396832CC3BF109D367A`
- `EVT-C4-SKH-HBM4-SUPPLY-COMMITMENT` → `SRC-SKH-20251029-Q3FY25` → article body, HBM supply paragraph (web-rendered line 56) → https://news.skhynix.com/en/sk-hynix-announces-3q25-financial-results/ → `42832CD21D67E19AC5101504CB70BE343E707BF8A9C08875CE6187C004EED1C9`
- `EVT-C4-SKH-LTA` → `SRC-SKH-20260729-Q2FY26-BACKTEST` → article body, contract paragraph (web-rendered line 58) → https://news.skhynix.com/en/q2-2026-business-results/ → `E7041578BC7861488AEEE91C0154FF372B9DD1B77C8E7396832CC3BF109D367A`

_Methodology: Small descriptive backtest; internal rubric values are not probabilities and no predictive-accuracy or statistical-significance claim is made._
