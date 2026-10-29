# US–Europe comparison: evidence notes (Section 7, `sec:disc-europe`)

Compiled 2026-10-29. Tags as in `cloud_era_baseline.md`: **[C]** computed by us from official files/APIs (reproducible commands below), **[P]** paper/document finding, **[S]** secondary source only (verify before quoting).

## 1. Business formation [C]

**EU-27, Eurostat `bd_size` (2021+), business economy `B-S_X_O_S94`.** Employer birth rate = births with ≥1 employee ÷ active enterprises with ≥1 employee (size classes 1–4, 5–9, ≥10). This is the closest analogue to the BDS startup rate (age-0 employer firms ÷ employer firms).

| Aggregate | Year | Birth rate, all % | Employer birth rate % | Zero-employee share of births % | Employment share of births % |
|---|---|---|---|---|---|
| Business economy | 2021 | 10.80 | 5.18 | 82.5 | 2.37 |
| | 2022 | 10.53 | 5.06 | 82.6 | 2.36 |
| | 2023 | 10.50 | 4.91 | 83.4 | 2.29 |
| | 2024 | 10.36 | 4.80 | 83.8 | 2.23 |
| J Information & communication | 2021 | 14.30 | 7.25 | 84.8 | 2.77 |
| | 2022 | 14.34 | 7.66 | 84.1 | 2.90 |
| | 2023 | 13.51 | 6.58 | 85.7 | 2.58 |
| | 2024 | 12.74 | 6.36 | 85.7 | 2.49 |
| J62 Computer programming | 2021 | 15.09 | 8.02 | 84.7 | 3.13 |
| | 2022 | 15.59 | 8.89 | 83.9 | 3.41 |
| | 2023 | 14.33 | 7.42 | 85.6 | n/a |
| | 2024 | 13.17 | 6.97 | 85.1 | 2.74 |

**US, Census BDS (from `cloud_era_baseline.md` §2.1):** startup rate 9.00% (2021), 9.41% (2022), 9.10% (2023); startup employment share 1.75–1.86%. Information (NAICS 51) startup rate 12.0% (2022).

Reading:
- The EU employer birth rate is roughly **half** the US startup rate (4.8% vs 9.1%; ratio 0.53). The EU all-enterprise birth rate (10.4%) is above the US employer rate only because >83% of EU births have no employees.
- In 2022–2024, the first two years of the generative-AI wave, **EU employer births in ICT fell** (J: 7.66% → 6.36%; J62: 8.89% → 6.97%), and the zero-employee share of births rose. US business applications in Information rose sharply over the same period (BFS; see `ai_adoption_evidence.md` §3.1). The EU pattern matches the US "employment-light" signature (more solo/zero-employee formation), without the US surge in total formation.
- Employment share of newborn firms: EU 2.2–2.4% (persons employed, includes proprietors) vs US 1.8–1.9% (employees only). Not comparable in level.

Reproduce: `GET https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/bd_size?format=JSON&geo=EU27_2020&lang=EN&sinceTimePeriod=2021`; indicators `ENT_BRTHR_PC`, `ENT_BRTH_NR`, `ENT_NR`, `EMP_BRTHR_PC`.

## 2. AI adoption by size [C] (from `ai_adoption_evidence.md` §1.3)

EU (10+ persons employed, `isoc_eb_ai`), 2025: 17.0% (10–49), 30.4% (50–249), 55.0% (250+); ratio large/small 3.2 (4.6 in 2021). US BTOS: ratio 250+/1–4 about 1.74. EU barriers among firms that considered AI: lack of expertise 70.9%, **unclear legal consequences 52.5%**, data protection 48.8%.

## 3. Labour-market rigidity [C]: OECD EPL Version 4, 2019 (0–6 scale)

| Country | Individual dismissals (regular) | Individual + collective (regular) | Collective | Temporary |
|---|---|---|---|---|
| United States | 0.75 | 0.77 | 0.81 | 0.26 |
| Germany | 2.22 | 2.33 | 2.61 | 1.36 |
| France | 2.45 | 2.68 | 3.25 | 2.68 |
| Italy | 2.72 | 2.86 | 3.19 | 1.96 |
| Spain | 2.43 | 2.43 | 2.43 | 2.37 |
| Netherlands | 2.85 | 2.88 | 2.96 | 1.24 |
| Sweden | 2.48 | 2.54 | 2.72 | 1.15 |
| Poland | 2.40 | 2.42 | 2.49 | 1.72 |
| Denmark | 1.84 | 1.94 | 2.18 | 1.56 |
| OECD average | 2.15 | 2.20 | 2.35 | 1.58 |

Reproduce: OECD SDMX `https://sdmx.oecd.org/public/rest/data/OECD.ELS.JAI,DSD_EPL@DF_EPL,1.0/all?startPeriod=2019&endPeriod=2019`, rows `VERSION4`.

Literature [P]: Bravo-Biosca, Criscuolo & Menon (2016, *Economic Policy* 31(88)) find stricter EPL is associated with a less dynamic firm-growth distribution (fewer fast growers and fast shrinkers) in labour- and R&D-intensive sectors. Criscuolo, Gal & Menon (2014, DynEmp, 18 countries): young firms are the main source of net job creation in every country; old SMEs destroy jobs. Calvino, Criscuolo & Menon (2016): policy failures hurt start-ups more than incumbents.

## 4. Formal entry costs [C]: OECD PMR 2023 (0–6, higher = more restrictive)

| Country | Admin requirements for LLCs and sole proprietors (`ADBURDEN`) | Admin & regulatory burden (`ADREG_BURDEN`) | Economy-wide PMR |
|---|---|---|---|
| United States | 2.03 | 1.89 | 1.58 |
| Germany | 2.74 | 1.87 | 1.21 |
| France | 1.60 | 1.51 | 1.23 |
| Italy | 1.80 | 1.15 | 1.23 |
| Spain | 1.39 | 1.19 | 1.16 |
| Netherlands | 2.21 | 1.65 | 0.91 |
| Sweden | 1.11 | 1.14 | 0.81 |
| Poland | 1.20 | 0.93 | 1.07 |
| Denmark | 1.31 | 1.03 | 1.05 |

Reading: on the OECD's measure, **formal start-up administrative burden is not systematically higher in Europe** (only Germany and the Netherlands exceed the US on `ADBURDEN`). The transatlantic gap in formation is therefore not explained by registration costs. It lines up with labour-market rigidity, scale-up finance, and (prospectively) AI-specific compliance.

Reproduce: OECD SDMX `OECD.ECO.GCRD,DSD_PMR@DF_PMR/all?startPeriod=2023`.

## 5. AI venture funding

- Stanford AI Index 2026 (covers 2025): US private AI investment $285.9B; Europe $20.9B (ratio ≈ 13.7). [P, via `ai_era_startups_2023_2026.md` §2.3]
- Dealroom (2025): >$21B into European AI start-ups (+58% y/y). Europe invests about 3× less than the US at growth stage and about 12× less at late stage ($12B vs $141B); more than half of European growth-stage AI capital comes from foreign, mostly US, investors. [S: Prosus "The Startup Paradox"; Trending Topics]
- Crunchbase (2025): Europe $17.5B (≈8% of global AI funding) vs US $159B of $211B global (ratio ≈ 9). [S: implicator.ai]
- Range used in the paper: US/Europe ≈ 9–14×.
- Lovable (Stockholm) and Mistral (Paris; Series D €3B at €21B post, Sep 2026) are the European outliers (`ai_era_startups_2023_2026.md`).

## 6. AI Act (Regulation (EU) 2024/1689) and the Digital Omnibus (Regulation (EU) 2026/1744)

Timeline:
- Prohibitions (Art. 5): 2 Feb 2025. GPAI model obligations: 2 Aug 2025.
- Art. 50 transparency: 2 Aug 2026 (watermarking grace to 2 Dec 2026 for systems already on the market).
- High-risk, Annex III (employment, credit, education, etc.): originally 2 Aug 2026 → **2 Dec 2027** (Omnibus).
- High-risk, Annex I (AI in regulated products): 2 Aug 2027 → **2 Aug 2028** (Omnibus).
- National sandboxes: → 2 Aug 2027.
- Omnibus published in OJ 24 Jul 2026, in force 27 Jul 2026. [S: Gibson Dunn; Orrick; ACT; Technology.org]

Proportionality provisions (startup vs incumbent margin):
- Art. 99(6): for SMEs including start-ups, each fine is capped at the **lower** of the percentage and the fixed amount (for others, the higher). Caps: €35M/7% (prohibited practices), €15M/3% (other obligations), €7.5M/1% (incorrect information). [P: Art. 99 text]
- Art. 62: priority sandbox access for SMEs/start-ups, conformity-assessment fees reduced in proportion to size, dedicated guidance channels. [P: Art. 62 text]
- Art. 11(1) simplified technical documentation for SMEs; Art. 63 simplified QMS for microenterprises. [P, from the regulation text; not re-fetched this pass]
- Omnibus extends SME relief to **small mid-caps** (<750 employees, turnover ≤ €150M or balance sheet ≤ €129M): simplified documentation, proportionate QMS, tailored penalty caps, priority sandbox access. [S: Orrick/JD Supra; ACT]

Compliance-cost estimates:
- Commission impact assessment (SWD(2021) 84/85): aggregate compliance cost €100–500M by 2025, about 4–5% of high-risk AI investment, plus 2–5% for verification. [S: Council doc ST-8115-2021-ADD-4]
- PwC NL (citing the IA): up to €160,000 per system for an SME. [S]
- CEPS (2021): QMS set-up €193,000–330,000 plus about €71,400/yr maintenance; the frequently quoted "17%" overhead applies only to firms meeting none of the requirements as business-as-usual. [S: several secondary sources; CEPS page returned 403]

Reading for the model: a quality-management system is a **fixed cost that does not scale with headcount**. For a high-risk-use entrant it raises `entry_cost` and `ai_adoption_fixed_cost`; incumbents with existing compliance functions (ISO 9001, GDPR, sectoral regimes) absorb it at lower marginal cost. The SME/SMC provisions shrink, but do not remove, the gap. The incidence is narrow: most AI-application start-ups (coding tools, marketing, productivity) fall outside Annex III and face only Art. 50 transparency duties.

## 7. Model scenario

See `data/europe_comparison.md` (generated by `scripts/europe_comparison.py`).

## Sources

- Eurostat bd_size: https://ec.europa.eu/eurostat/databrowser/view/bd_size/default/table
- Eurostat isoc_eb_ai: https://ec.europa.eu/eurostat/databrowser/view/isoc_eb_ai/default/table
- OECD EPL: https://www.oecd.org/en/data/datasets/oecd-indicators-of-employment-protection.html
- OECD PMR: https://www.oecd.org/en/topics/sub-issues/product-market-regulation.html
- AI Act Art. 99: https://artificialintelligenceact.eu/article/99/ ; Art. 62: https://artificialintelligenceact.eu/article/62/
- Gibson Dunn on the Omnibus: https://www.gibsondunn.com/eu-ai-act-omnibus-agreement-postponed-high-risk-deadlines-and-other-key-changes/
- Orrick, "EU's Digital Omnibus on AI: 7 Key Changes": https://www.orrick.com/en/Insights/2026/05/EUs-Digital-Omnibus-on-AI-7-Key-Changes-You-Need-to-Know
- ACT, Omnibus enters into force: https://actonline.org/2026/08/06/what-european-startups-and-smes-should-know-as-the-ai-omnibus-enters-into-force/
- Technology.org deadlines: https://www.technology.org/2026/10/13/eu-ai-act-deadlines-after-the-digital-omnibus-what-applies-from-december-2026-to-august-2028/
- Commission IA summary (Council): https://data.consilium.europa.eu/doc/document/ST-8115-2021-ADD-4/en/pdf
- PwC NL: https://pwc.nl/en/insights-and-publications/themes/digitalization/european-artificial-intelligence-act-many-procedural-and-substantive-requirements.html
- CEPS: https://www.ceps.eu/?p=34112
- Prosus, "The Startup Paradox": https://www.prosus.com/~/media/Files/P/prosus-corp-v2/documents/the-prosus-way/the-startup-paradox.pdf
- Trending Topics (Dealroom): https://www.trendingtopics.eu/europeans-consume-ai-brilliantly-but-train-the-algorithms-owned-by-others/
- implicator.ai (Crunchbase): https://www.implicator.ai/why-europes-17-5-billion-ai-bet-still-trails-america-by-9x/
- Bravo-Biosca et al. (2016): https://ideas.repec.org/a/oup/ecpoli/v31y2016i88p703-742..html
- Criscuolo et al. (2014): https://eprints.lse.ac.uk/60286/
- Calvino et al. (2016): https://ideas.repec.org/p/oec/stiaac/29-en.html
