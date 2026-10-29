# AI-Era Startup Evidence (2023–2026)

Research notes for the economics paper (T9). BDS ends in 2023 and its AI-era cohorts will not show up for years, so this file documents what is visible now: frontier-lab scaling, the AI venture boom, Census BFS applications through September 2026, AI-native firm headcounts, and how the age-not-size dynamic applies. Companion to `data/cloud_era_baseline.md`.

Compiled 2026-10-29. Many 2026 figures postdate published research and come from press and vendor reports gathered this pass. Verify the [R]/[A] items against primary documents before quoting them in the paper.

**Provenance tags used below**

| Tag | Meaning |
|---|---|
| **[C]** | Computed by us from official Census files: `bfs_monthly.csv` (downloaded 2026-10-29, data through Sep 2026), BDS 2023 release `bds2023_fa_fz.csv` and `bds2023_sec_fa_fz.csv`. Reproducible. |
| **[R]** | Reported by a primary data vendor, the company, a government agency or a major outlet (Crunchbase News, PitchBook-NVCA via SiliconANGLE, Census, Stanford HAI, anthropic.com, Orrick, Reuters/FT as relayed). Not checked against the underlying dataset. |
| **[A]** | Third-party aggregator estimate (Revelio, Latka, TrueUp, TipRanks, workforce trackers, blogs). Wide ranges and often conflicting. Use only as orders of magnitude. |
| **[P]** | Published paper finding. |
| **[U]** | From domain knowledge, not re-verified this pass. Check before citing. |

---

## 0. Headline findings

1. **AI now absorbs most venture capital, and the AI share has risen every year since 2023.** [R] Crunchbase puts AI at $55.6B of $304B global VC in 2023 (~18%), $101–114B (~1/3) in 2024, $202–212B (~50%) in 2025, and ~80% / >70% / 64% in Q1 / Q2 / Q3 2026. Global VC through Q3 2026 is **$679B, a record for any first three quarters**. US: AI took **82.7% of deal value Jan–Sep 2026** (PitchBook-NVCA).
2. **The money is extremely concentrated.** [R] OpenAI and Anthropic together raised **$217B, or 43% of all global startup funding, in H1 2026**. In the US, rounds of $100M+ took 87.5% of H1 2026 deal value, and rounds under $100M took 12.5% (43.8% in 2024). The cloud era has no precedent for this.
3. **Breadth is also high, so the market is a barbell.** [R] Newly funded AI companies rose 71% in 2025 (Stanford AI Index 2026). Q3 2026 US deal count (~5,012) was the second-busiest quarter on record. Solo founders rose from 23.7% of new Carta startups in 2019 to 36.3% in H1 2025.
4. **Frontier labs are young and very large by valuation, but mid-sized by employment.** [R/A] Anthropic (founded 2021) was valued at $965B in May 2026 with roughly 2,300–5,000 employees. That is $190–420M of valuation per employee, against $11–17M for Databricks. In headcount, the labs crossed the 500-employee "large firm" line at ages similar to cloud-era winners (3–8 years). In capital they got there 10–100× faster.
5. **AI-native application firms are strongly employment-light.** [A] Cursor reached ~$3B ARR with ~150–300 staff (~$10–20M per employee). Lovable reached $400M ARR with ~146 staff. Cloud-era SaaS ran at roughly $0.25–0.45M revenue per employee [U].
6. **BFS: applications are surging, but intent to hire is falling.** [C] Business applications hit a record 5.67M in 2025 and are up a further **15.3%** Jan–Sep 2026 vs Jan–Sep 2025. Information (NAICS 51) leads at **+39.8%**, followed by Professional/technical (54) at +29.6%. Over the same window, applications with planned wages **fell 15.3%** (−21.5% in Information). Planned-wage applications were 12.3% of Information applications in 2019 and **4.8% in 2026 YTD**. The planned-wage decline shows up in every sector, so it is not AI-specific (see §3.3).
7. **Graduation is real but small in the stock, and AI adds a short-circuit.** [C] In BDS, young firms (age ≤10) held only **4.0% of large-firm (500+) employment in 2019** and 3.9% in 2023, against ~7% in 1990–2000. The rise in the large-firm employment share during the cloud era came mostly from *old* large firms, not from graduates such as Databricks, Snowflake or Stripe. In the AI era, many successful young firms are being **absorbed into old incumbents before they graduate** (Inflection→Microsoft, Character.ai and Windsurf→Google, xAI and Cursor→SpaceX). BDS assigns firm age from the oldest establishment, so this M&A turns young-firm employment into old-firm employment.

**Implication for the paper:** Frontier AI labs follow the Haltiwanger "young high-growth firm" path, but with far less labour per dollar of output and capital. Their combined US headcount (roughly 15–25k across the labs and leading app-layer firms) is about 0.03% of the ~74M employees in 500+ firms. AI-native *graduation* therefore cannot measurably move the BDS firm-size distribution in 2024–2026. Any AI-driven size rebalancing has to come through (a) the nonemployer/solo margin, which BFS suggests is growing, and (b) adoption by incumbents. Census BTOS shows adoption skewed toward large firms. Both channels are measurable; the frontier-lab headline is not the mechanism.

---

## 1. Frontier AI labs: scaling trajectories

None of the labs publishes headcount. Ranges show the spread across sources, and scope differs between them (e.g. OpenAI OpCo vs Foundation, inclusion of contractors).

### 1.1 OpenAI (founded Dec 2015)

| Date | Valuation / funding | Headcount | Tag |
|---|---|---|---|
| 2015 | Non-profit launch, $1B pledged | ~a few dozen | [U] |
| Jul 2019 | Capped-profit LP; Microsoft $1B | ~100–150 | [U] |
| 2020–2021 | n/a | 120–300 (sources conflict) | [A] |
| 2022 (pre-ChatGPT) | n/a | ~335–375 | [A] |
| Jan 2023 | Microsoft multi-year ~$10B; tender at ~$29B | n/a | [U] |
| Nov 2023 | n/a | ~770 (board-crisis staff letter) | [U] |
| Oct 2024 | $6.6B at $157B post | 3,500–4,500 (trackers) | [U]/[A] |
| Mar 2025 | $40B SoftBank-led at $300B post | n/a | [U] |
| Oct 2025 | ~$500B secondary; PBC recapitalisation | n/a | [U] |
| **27 Feb 2026** | **$110B at $730B pre / ~$840B post** (Amazon $50B, Nvidia $30B, SoftBank $30B) | ~4,500 direct payroll (FT, Mar 2026); ~7,850 incl. Foundation (Revelio, end-2025) | [R]/[A] |
| 2026 | Reported $122B raised in 2026 in total; ~$852B; secondary ~$878B (May 2026); confidential IPO filing reported | FT-reported plan to reach ~8,000 by end-2026. Altman reportedly said in Jan 2026 that hiring would "dramatically slow" | [A]/[R] |

Graduation: OpenAI crossed 500 employees around 2023 (age ~7–8) and 1,000 around 2024 (age ~8–9). In headcount terms this is close to the cloud-era pace. Valuation is what departs from it.

### 1.2 Anthropic (founded 2021)

| Date | Round | Amount | Post-money | Tag |
|---|---|---|---|---|
| May 2021 | Series A | $124M | ~$0.5B | [U] |
| Apr 2022 | Series B | $580M | ~$4B | [U] |
| 2023 | Google $300M; Series C $450M; Amazon up to $4B; Google up to $2B | ~$6.5B | ~$4–18B | [U] |
| Nov 2024 | Amazon additional $4B (total $8B) | $4B | n/a | [U] |
| Mar 2025 | Series E | $3.5B | $61.5B | [U] |
| Sep 2025 | Series F | $13B | $183B | [U] |
| Feb 2026 | Series G (GIC, Coatue co-lead) | $30B | $380B ($350B pre) | [R] |
| **28 May 2026** | **Series H** (Altimeter, Dragoneer, Greenoaks, Sequoia) | **$65B** | **~$1T** (derived) | [R] |
| **26 Oct 2026** | **Public S-1 registration filed for proposed IPO** (SEC EDGAR CIK 0002130357) | n/a | n/a | [R] |

**S-1 verified data (October 26, 2026, CIK 0002130357):**
- **Headcount:** 940 (Dec 2024) → **5,300 (Sep 30, 2026)** — 5.6× growth in 21 months
- **Revenue:** $41M (2023) → $386M (2024) → **$4,585M (2025)** → **$16,286M (H1 2026)**
- **Derived Q3 2026 revenue:** ~$16.9B (from "86× Q4'24" in filing)
- **TTM revenue per employee:** >$6.6M as of Sep 2026 (vs $1.4M a year earlier)
- **Operating loss:** $(8.1B) in 2025; **$(693M) in H1 2026** (improving rapidly)
- **Net loss:** $(42B) in 2025; $(81B) in H1 2026 — **but ~90% is non-cash mark-to-market on convertible notes**
- **Adjusted operating income:** First profit quarter was Q2 2026 (+$974M). H1 2026 adjusted operating income = **+$1.6B**
- **Total capital raised:** $141.1B as of Jun 30, 2026
- **Valuation per employee:** ~$1T / 5,300 = **$189M per employee** — 25× higher than Databricks ($7.6M) at comparable headcount

**Key S-1 productivity disclosures:**
- "Over 90% of the contributions to our codebase in September 2026 were written by Claude"
- "Average daily volume of code contributed per engineer" rose **45× from 2024 to Sep 2026**
- "TTM revenue increased approximately 1,200% while headcount increased approximately 170%" (Sep'25 to Sep'26)
- "Claude allows employees to leverage a team of agents... enabling a comparatively small team to take on work that would traditionally require a far larger one by multiplying the impact of each person"
- "The value of our own internal Claude usage at list prices... in April 2026, this monthly value first exceeded our monthly personnel expense"

**Risk factors on labor displacement:**
- Governments "may intervene to slow the rate of adoption of AI" if "the rate of job displacement rapidly increases"
- Company "may from time to time voluntarily elect to take actions intended to ameliorate the impact of such displacement... additional costs... for which we may not receive a corresponding commercial benefit"
- Listed risk: "new or more restrictive laws... including taxes, fees, or other measures specifically applicable to AI companies or AI-related labor displacement"

Graduation: crossed 500 employees around 2023–24 (age 2–3), the fastest of any firm in this note.

### 1.3 Other labs

| Lab | Founded / HQ | Latest valuation | Headcount (est.) | Trajectory / status | Tag |
|---|---|---|---|---|---|
| **xAI** | 2023, US | $250B (in SpaceX deal) | ~1,000+ core plus large annotation workforce | $6B at $24B (May 2024) [U]; merged with X (Mar 2025) [U]; **acquired by SpaceX, announced 2 Feb 2026, xAI valued at $250B**, the largest M&A deal on record [R] | [R]/[U] |
| **Mistral** | Apr 2023, Paris | **>€21B post** (~$24B) | 1,000–1,600 | €105M seed (Jun 2023) [U]; €600M at €5.8B (Jun 2024) [U]; Series C €1.7B at €11.7B led by ASML (Sep 2025) [R]; **Series D €3B led by Samsung, 8 Sep 2026**, the largest European tech equity round [R] | [R]/[A] |
| **Cohere** | 2019, Toronto | $7B (Sep 2025); talks at ~$20B (Sep 2026, unconfirmed) | ~700 | $5.5B (Jul 2024) [U]; $6.8B → $7B (Aug–Sep 2025) [R]; Series E process reported [R]. One directory claims a merger with Aleph Alpha (unconfirmed) [A] | [R]/[A] |
| **AI21 Labs** | 2017, Tel Aviv | ~$1.4B (2023) | ~200 | Jan 2026 reports of a $2–3B Nvidia acqui-hire for its ~200 staff, which AI21 denied [R]. Status unresolved | [R]/[U] |
| **Inflection** | 2022, Palo Alto | ~$4B (Jun 2023) | ~60 | Mar 2024: Microsoft hired both cofounders and most staff and paid ~$650M in licensing [R/U]. Remainder pivoted to enterprise | [R]/[A] |
| **Safe Superintelligence** | 2024 | $32B (Apr 2025) | ~20–50 | $1B at $5B (Sep 2024) [R]; ~$2B at $32B (Apr 2025) [R]; Nvidia investment reported at $5B (2026, amount undisclosed by the companies) [R] | [R]/[A] |
| **Thinking Machines Lab** | 2025 | $12B (Jul 2025 seed) | ~90–110 | $2B seed at $12B [R]; talks for $5–6B at ≥$40B pre-money (Sep 2026) [R]; an earlier ~$50B attempt reportedly collapsed [A] | [R]/[A] |

### 1.4 Are these the "Databricks of AI"?

| Firm | Founded | Years to ~500 emp. | Years to ~1,000 emp. | Valuation at age ~5–6 | Emp. at that age | Valuation per employee, latest | Tag |
|---|---|---|---|---|---|---|---|
| Stripe | 2010 | ~6 | ~8 (2018) | ~$9B (2016) | ~500–800 | $91.5B / ~8,500 ≈ $11M (2025) | [U] |
| Snowflake | 2012 | ~6 | ~7 (2019) | ~$3.9B (2018) | ~600–1,000 | IPO Sep 2020; ~7,800 emp. FY2025 | [U] |
| Databricks | 2013 | ~5 | ~6–7 (2019–20) | $6.2B (Oct 2019) | ~900 (Oct 2019) [A] | $134B / 8,000–12,300 ≈ $11–17M | [U]/[A]/[R] |
| OpenAI | 2015 | ~7–8 | ~8–9 | ~$1B+ (2019–20, Microsoft) | ~150–250 | $840B / 4,500–7,850 ≈ $107–187M | [U]/[A]/[R] |
| Anthropic | 2021 | ~2–3 | ~3–4 | $965B (2026, age 5) | ~2,300–5,000 | ≈ $190–420M | [R]/[A] |
| Mistral | 2023 | ~2–3 | ~3 | ~$24B (age 3) | 1,000–1,600 | ≈ $15–24M | [R]/[A] |
| SSI | 2024 | not yet | not yet | $32B (age 1) | ~20–50 | ≈ $0.6–1.6B | [R]/[A] |

**Assessment.**
- **Yes, in the age dynamics.** Each lab is a young firm that passed or will pass the 500-employee BDS threshold within 2–8 years, which is the "high-growth young firm" pattern behind most net job creation (§5).
- **No, in factor intensity.**
  - Cloud-era winners scaled revenue roughly in line with headcount, at $0.3–0.5M revenue per employee [U].
  - Frontier labs scale *compute* instead. Most of their cost is chips, data centres and power, so the employment their growth creates sits largely at Nvidia, the hyperscalers, construction firms and utilities. Those are old, large firms.
  - Cloud cut startup capex. Frontier AI moves capex back to the frontier, financed through circular strategic deals (Amazon, Nvidia, Microsoft and Google invest in labs that buy their compute).
- **No, in exit path.** Databricks, Snowflake and Stripe stayed independent and grew into large employers. A notable fraction of AI-era winners have been bought or acqui-hired instead (§5.4).

---

## 2. AI startup funding, 2023–2026

### 2.1 Global (Crunchbase) [R]

| Period | Global VC | AI funding | AI share | Notes |
|---|---|---|---|---|
| 2023 | $304B | $55.6B | ~18% | Foundation models ~40% of AI $ |
| 2024 | ~$314B | $101B (later revised to ~$114B) | ~1/3 (34%) | Foundation models ~$31B (~27%) |
| 2025 | ~$425–440B (revised) | $202–212B | ~50% | Foundation models ~$80B (40%). 58% of AI $ in $500M+ rounds. OpenAI+Anthropic = 14% of global VC; top 5 (OpenAI, Scale AI, Anthropic, Project Prometheus, xAI) = $84B, ~20%. 79% of AI $ went to US firms ($159B), with $122B to the Bay Area. |
| Q1 2026 | ~$305B (largest quarter ever) | ~$242B | ~80% | OpenAI $110B round |
| Q2 2026 | ~$205B, >5,000 startups | n/a | >70% | Anthropic $65B Series H. Record Q2 M&A: 24 $1B+ acquisitions totalling $113B |
| Q3 2026 | ~$159B, ~6,000 startups | ~$102B | 64% | Record 27 $1B+ rounds (8 of $3B+), incl. Databricks and SSI at $5B each [A] |
| **Jan–Sep 2026** | **~$679B** | n/a | n/a | Highest Jan–Sep total ever. **H1 alone ($510B) exceeds all of 2025** and the previous half-year peak (~$375B, H2 2021) |

### 2.2 United States (PitchBook-NVCA Venture Monitor) [R]

| Period | US deal value | AI share of value | Other |
|---|---|---|---|
| 2024 | $209B | $97B (~46%) | via Bloomberg |
| 2025 | Second-highest year on record | ~65% (NVCA Yearbook: 65.4%) | 16,707 deals (+9.6% y/y); exits $297.8B (+92.7%) |
| H1 2026 | **$412.7B** (~30% above all of 2025) | **86%** ($355.9B) | $100M+ rounds = 87.5% of value. Deals <$100M = $51.4B (12.5%), vs 43.8% (2024) and 33.1% (2025). CVC in 21% of deals (10-yr low) |
| Q3 2026 | $98.4B (−40% q/q) | 65.9% | ~5,012 deals, second-busiest quarter on record |
| **Jan–Sep 2026** | **$515.8B** (~44% above the previous annual record) | **82.7%** (record) | 179 new unicorns. Record 992 unicorns worth $5.7T. PitchBook model gives an Anthropic IPO within 12 months 86% odds and OpenAI 12% |

### 2.3 Stanford AI Index 2026 (covers 2025) [R]

- Global corporate AI investment: **$581.7B**. Private investment: **$344.7B (+127.5%)**, 60% of the total. AI M&A: $214.4B.
- US AI investment $285.9B, against Europe $20.9B and China $12.4B (China excludes state guidance funds).
- **Newly funded AI companies +71%.** Billion-dollar AI funding events nearly doubled (15 → 28 per secondary coverage).
- Generative AI investment +200%, ~half of private AI funding.
- Labour: employment of software developers aged 22–25 down ~20% from 2024. 32% of surveyed organisations expect AI-related workforce reductions next year.

### 2.4 Comparison with cloud-era VC patterns

| Dimension | Cloud era (2006–2015) | AI era (2023–2026) | Tag |
|---|---|---|---|
| Entry capital | Fell ~20% in AWS-exposed sectors. "Spray and pray": more, smaller first rounds (Ewens, Nanda & Rhodes-Kropf 2018) | **Bimodal.** App layer is even cheaper to start (solo founders 23.7% → 36.3% on Carta, 2019 → H1 2025; fewer 3–5-founder teams than at any point in 10 yrs). Frontier labs need $1–65B rounds | [P]/[R] |
| Distribution of $ | Broad; many Series A/B | Extreme top concentration: 2 firms = 43% of global H1 2026 VC. Sub-$100M rounds = 12.5% of US value | [R] |
| Count vs value | Deal counts and value rose together | AI ≈ 1/3 of global deal *count* but >1/2 of *value* (2025). Counts high, value concentrated | [R] |
| Capex | Startup capex → metered opex (AWS) | App layer: still opex (API tokens). Frontier: capex returns at unprecedented scale (GW-scale compute) | [U] |
| Investor mix | Traditional VC, accelerators | Strategic/hyperscaler and chip-vendor capital (Amazon, Nvidia, Microsoft, Google, SoftBank) plus sovereign funds. Circular compute-for-equity deals | [R] |
| Peak annual VC | 2021: ~$640B global (Crunchbase) [U]; ~$345B US [U] | 2026: $679B global and $516B US by Sep | [U]/[R] |
| Exit path | IPO of independents (Snowflake 2020, Datadog 2019, etc.) | Mega-acquisitions and acqui-hires (§5.4), plus mega-IPOs (SpaceX ~$75B raise, Cerebras, Anthropic S-1) | [R] |
| Fund formation | Many new managers | 211 emerging managers closed funds in 2026 vs 927 in 2022. $500M+ megafunds = 78% of capital | [R] |

**Reading.** The cloud era made firm *entry* cheaper and spread capital thinly. The AI era repeats that at the application layer, more strongly than before. It also adds a capital-intensive frontier tier that absorbs most of the dollars. For firm demography, the question is which tier creates *employer* firms. The evidence in §3–4 says neither creates many employees per dollar.

---

## 3. Census BFS: business applications 2019–2026 [C]

Source: `bfs_monthly.csv`, unadjusted (`sa=U`) US series, summed by calendar year. Data run through September 2026, so YTD comparisons use January–September.

### 3.1 National totals

| Period | Applications (BA) | High-propensity (HBA) | With planned wages (WBA) | HBA/BA | WBA/BA |
|---|---|---|---|---|---|
| 2019 | 3,498,990 | 1,316,191 | 478,640 | 37.6% | 13.7% |
| 2021 | 5,390,816 | 1,841,954 | 638,140 | 34.2% | 11.8% |
| 2022 | 5,062,563 | 1,722,399 | 578,669 | 34.0% | 11.4% |
| 2023 | 5,469,302 | 1,848,540 | 613,708 | 33.8% | 11.2% |
| 2024 | 5,224,176 | 1,715,458 | 550,423 | 32.8% | 10.5% |
| **2025** | **5,671,836** (record) | 1,708,842 | 501,223 | 30.1% | 8.8% |
| Jan–Sep 2019 | 2,730,652 | 1,028,356 | 378,254 | 37.7% | 13.9% |
| Jan–Sep 2025 | 4,273,086 | 1,323,566 | 397,614 | 31.0% | 9.3% |
| **Jan–Sep 2026** | **4,927,840** (+15.3% y/y) | 1,386,358 (+4.7%) | **336,905 (−15.3%)** | 28.1% | **6.8%** |

Total applications in 2026 are running at ~1.8× the 2019 pace. Planned-wage applications in 2026 are running ~11% *below* 2019 (336,905 vs 378,254 for Jan–Sep). The post-2020 surge is entirely on the non-employer-intent margin, and it sped up in 2025–2026.

### 3.2 Sector breakdown

| Sector (NAICS) | BA 2019 | BA 2025 | 2025 vs 2019 | BA YTD26 vs YTD25 | HBA YTD26 vs YTD25 | WBA YTD26 vs YTD25 | WBA/BA 2019 | WBA/BA 2025 | WBA/BA YTD26 |
|---|---|---|---|---|---|---|---|---|---|
| **51 Information** | 73,255 | 110,329 | +50.6% | **+39.8%** | −3.7% | **−21.5%** | 12.3% | 8.0% | **4.8%** |
| **54 Prof., scientific & technical** | 456,938 | 764,007 | +67.2% | **+29.6%** | +9.1% | −9.9% | 11.5% | 8.1% | 5.8% |
| 52 Finance & insurance | 162,845 | 232,425 | +42.7% | +3.2% | −15.2% | −24.0% | 8.7% | 6.1% | 4.8% |
| 56 Admin & support | 237,584 | 377,364 | +58.8% | +21.4% | −8.9% | −12.9% | 15.2% | 10.8% | 8.0% |
| 44–45 Retail | 518,436 | 1,166,015 | +124.9% | +10.4% | +9.3% | −19.1% | 10.7% | 4.7% | 3.8% |
| 23 Construction | 382,136 | 519,090 | +35.8% | +12.1% | +8.6% | −15.7% | 14.4% | 10.1% | 7.9% |
| 62 Health care | 224,871 | 352,046 | +56.6% | +16.4% | +10.9% | −9.8% | 20.5% | 16.0% | 12.9% |
| **Total** | 3,498,990 | 5,671,836 | +62.1% | +15.3% | +4.7% | −15.3% | 13.7% | 8.8% | 6.8% |

- **Is there a tech/AI surge?** Yes, in applications. Information and Professional/technical are the two fastest-growing sectors in 2026. Their combined share of all applications rose from 15.2% (2019) and 15.4% (2025) to 17.2% (2026 YTD). Monthly Information applications were above the prior-year month in every month of 2026; September 2026 was 15,282 against 8,171 in September 2025.
- **But not in high-propensity or wage-planning applications.** In Information, the HBA share of applications fell from 26.6% (2019) to 18.0% (2025) and 12.8% (2026 YTD). The extra Information applications are overwhelmingly the kind that rarely become employers. This is consistent with AI-enabled solo software, content and consulting entities.

### 3.3 Caveats and what BFS cannot yet show

1. **The WBA decline is economy-wide.** Planned-wage applications fall in every sector in 2026 (−10% to −24%). A slowing labour market, or an IRS Form SS-4 or EIN-process change, could be driving the national drop. **Check IRS/Census notices for 2025–26 SS-4 changes before attributing the decline to AI.** What *is* sector-specific is the size of the BA surge in NAICS 51/54.
2. **Employer-formation series lag.** The current file has `BF_BF4Q`/`BF_BF8Q` only through the 2022 application cohort. Actual conversion of 2023–2026 applications into employers is not yet observable.
3. **No AI code.** BFS sectors are 2-digit NAICS self-reported on the SS-4. AI firms fall under 5112/5132 (software publishers), 5182 (data processing/hosting), 5415 (computer systems design) and 5417 (R&D), all inside 51/54.
4. **BDS lag.** The BDS 2023 release is the latest in our pipeline. AI-era cohorts (born 2023+) enter BDS from the 2024 release, and their size outcomes will not be visible until roughly 2027–2029.

### 3.4 Complementary Census signal: who adopts AI (BTOS) [R]

- National AI use was 17–20% (Dec 2025–May 2026) and 19.8% for the period ending 3 May 2026. Third-party analysis of July 2026 data reports 21.7%.
- **By size:** 37% of firms with 250+ employees and 32% with 100–249 use AI, against <20% of firms with ≤4 employees. Firms with 20+ employees increased use between Dec 2025 and May 2026. Firms with <20 showed no significant change.
- **By sector:** Information 39.7%, Finance & insurance 33.9%, Retail ~14%.
- **Break in series:** on 17 Nov 2025 the question changed from AI use "in producing goods or services" to use "in any business function". Do not splice the pre- and post-Nov-2025 series.
- **Reading:** measured adoption is skewed toward larger firms. This is the same scale counter-mechanism the cloud baseline found (Bessen 2020).

---

## 4. AI-native company examples (founded ~2021–2025)

### 4.1 Landscape

| Company | Founded | Latest valuation (date) | Revenue / ARR | Headcount (est.) | Rev. or val. per employee | Status | Tag |
|---|---|---|---|---|---|---|---|
| Anthropic | 2021 | ~$965B (May 2026) | $47B run-rate (May 2026) | 2,300–5,000 | ~$9–20M rev/emp | S-1 filed Oct 2026 | [R]/[A] |
| xAI | 2023 | $250B (Feb 2026) | n/a | ~1,000+ | ~$100–250M val/emp | Absorbed by SpaceX | [R]/[U] |
| Mistral | 2023 | >€21B (Sep 2026) | n/a | 1,000–1,600 | ~$15–24M val/emp | Independent | [R]/[A] |
| Cursor (Anysphere) | 2022 | $60B all-stock (SpaceX deal, Aug 2026) | ~$3B ARR (May 2026) | ~300 (Aug 2025) | **~$10.0M rev/emp** | Acquired by SpaceX | [R] |
| Lovable | 2023, Stockholm | ~$13.3B (Aug 2026); $6.6B (Dec 2025) | $200M ARR (Nov 2025) | ~120 (Dec 2025) | **~$1.7M rev/emp** | Independent | [R] |
| Perplexity | 2022 | ~$20B (latest disclosed) | ~$450–500M annualised | 960–1,500 | ~$0.3–0.5M rev/emp | Independent | [A] |
| Safe Superintelligence | 2024 | $32B (Apr 2025) | pre-revenue | 20–50 | ~$0.6–1.6B val/emp | Independent | [R]/[A] |
| Thinking Machines Lab | 2025 | $12B (2025); ≥$40B talks | early | 90–110 | ~$110–130M val/emp | Independent | [R]/[A] |
| Midjourney | 2021 | no outside VC | ~$200M (2023) | ~40 | ~$5M rev/emp | Independent | [U] |
| Character.ai | 2021 | ~$1B (2023) | n/a | ~100–200 | n/a | Google licence + founder rehire, Aug 2024 (~$2.7B) | [U] |
| Inflection | 2022 | ~$4B (2023) | n/a | ~60 after 2024 | n/a | Most staff to Microsoft, Mar 2024 | [R]/[A] |

### 4.2 Employment-heavy or employment-light?

**Light, in two different ways.**

1. **Application layer: extremely light.** At $100M–$3B ARR, AI-native firms have tens to a few hundred staff. Cloud-era SaaS firms at $100M ARR typically had ~400–800 employees and ran at ~$0.25–0.45M revenue per employee [U]. Cursor (~$10–20M) and Lovable (~$2.7M) are 5–50× that. Perplexity (~$0.3–0.5M) is the exception: a consumer search product with conventional staffing.
2. **Frontier labs: mid-sized by headcount, tiny by headcount per dollar.** Thousands of employees puts them in the BDS 500+ or 1,000+ class. But valuation per employee is ~$100–400M against ~$11–17M at Databricks and Stripe. Most of their marginal spending goes to compute, not payroll.
3. **Where the jobs go.** Frontier-lab spending flows to chipmakers, hyperscalers, data-centre construction and utilities, all old, large firms. Deployment labour is increasingly in partners: Anthropic and partners aim to train 10,000 "Frontier Deployed Engineers" by end-2027 [R]. In BDS terms, the employment counterpart of AI-native growth lands mostly in large *old* firms.

### 4.3 Cloud-era SaaS trajectories for comparison

| Firm | Founded | ~Age 5–6 | ~Age 10 | Recent | Tag |
|---|---|---|---|---|---|
| Databricks | 2013 (7 Berkeley founders) | ~900 emp., $6.2B (Oct 2019) | ~5,000+ emp. (2023) | $134B (Dec 2025/Feb 2026); $3B term sheet at $188B (Jul 2026); 8,000–12,300 emp. | [A]/[U]/[R] |
| Snowflake | 2012 | ~500–1,000 emp. (2018) | IPO Sep 2020; ~2,500 emp. (Jan 2021) | ~7,800 emp. (FY2025); ~$0.46M rev/emp | [U] |
| Stripe | 2010 | ~500–800 emp. (2016) | ~2,500 (2019) → ~8,000 (2022); −14% Nov 2022 | ~8,500 emp.; $91.5B (Feb 2025 tender) | [U] |

Cloud winners took 5–8 years to reach ~1,000 employees and then grew headcount roughly in line with revenue. AI-native app firms reach comparable or larger revenue in 2–4 years with 1/5 to 1/20 of the staff.

---

## 5. The graduation problem: age, not size

### 5.1 The finding

- **Haltiwanger, Jarmin & Miranda (2013), "Who Creates Jobs? Small versus Large versus Young," *REStat* 95(2): 347–361.** [P] Once firm age is controlled for, there is no systematic relationship between firm size and growth. The apparent small-firm advantage is a young-firm advantage. Startups and young firms contribute disproportionately to both job creation and job destruction ("up or out").
- **Decker, Haltiwanger, Jarmin & Miranda (2014), *JEP* 28(3).** [P] A small share of young, high-growth firms accounts for most of the net job creation of a cohort.
- **Sterk, Sedláček & Pugsley (2021), "The Nature of Firm Growth," *AER* 111(2).** [U] Much of the eventual size of a firm is predictable at birth: ex-ante heterogeneity matters more than shocks. Frontier AI labs fit this, being "born to be large" in capital.

### 5.2 How cloud-era winners entered the statistics

- Databricks (2013), Snowflake (2012) and Stripe (2010) were small age-0 firms in BDS. By 2019 each had crossed into the 500+ class while still aged 6–9.
- In a **size-only** table they count as growth in "large-firm employment". In an **age × size** table they are *young large* firms, the high-growth tail Haltiwanger et al. credit with job creation.
- So a rising large-firm share can partly reflect successful young firms *graduating*, not old incumbents gaining. The question is how much.

### 5.3 BDS evidence: how big is graduation? [C]

Young firms' share of large-firm employment (BDS 2023 release, `bds2023_fa_fz.csv`):

| Year | Employment in 500+ firms (M) | Share held by firms aged 0–5 | aged 6–10 | **aged ≤10** | aged 11–15 | # firms aged ≤10 with 500+ emp. |
|---|---|---|---|---|---|---|
| 1990 | 43.2 | 4.0% | 3.0% | **7.1%** | 2.5% | 2,639 |
| 1995 | 46.4 | 2.2% | 5.1% | **7.3%** | 3.9% | 2,658 |
| 2000 | 56.1 | 3.1% | 3.7% | **6.8%** | 6.7% | 2,730 |
| 2006 | 58.5 | 2.2% | 3.3% | **5.5%** | 4.1% | 2,693 |
| 2010 | 56.2 | 1.6% | 2.6% | **4.2%** | 4.1% | 2,173 |
| 2015 | 63.9 | 1.6% | 2.2% | **3.8%** | 3.4% | 2,030 |
| 2019 | 69.8 | 1.4% | 2.6% | **4.0%** | 2.7% | 2,345 |
| 2023 | 73.9 | 1.5% | 2.5% | **3.9%** | 3.2% | 2,283 |

Cumulative net job creation by cell, BDS years 2007–2019 (total +12.49M, matching the baseline's +12.6M):

| Cell | Net job creation 2007–2019 |
|---|---|
| Age 0–5, <500 emp. (startups and young small firms) | **+24.5M** |
| Age 16+, 500+ (old large) | +3.3M |
| Age 0–5, 500+ (young large) | +1.4M |
| Age 6–10, 500+ | +0.7M |
| Age 11–15, 500+ | +0.5M |
| Left-censored (born before 1977), 500+ | −1.3M |
| Age 6–10, <500 | −3.5M |
| Age 11–15, <500 | −3.0M |
| Left-censored, <500 | −3.1M |
| Age 16+, <500 | −7.0M |

How to read this:
- **Graduates are a thin slice of the large-firm stock.** Firms aged ≤10 held ~4% of 500+ employment in 2019–2023, down from ~7% in 1990–2000. The cloud-era rise in the large-firm share was mostly an *old*-large-firm phenomenon. Databricks/Snowflake/Stripe-type graduations did not drive it.
- **Young firms still dominate net job creation.** Young small firms generated +24.5M net, offset by contraction and exit among older small firms. Young large firms (≤10) added +2.1M net, about 17% of the total, against +3.3M for old large firms. This is the Haltiwanger pattern: growth comes from age, and size is where successful firms end up.
- **Information (NAICS 51), same calculation** [C]: young firms held 4.1% of large-firm Information employment in 2019 and 3.9% in 2023, down from 5.6% in 2006. Very few young Information firms reach 5,000+ employees (0–4 per year since 2010).
- **Caveats:**
  - About 10% of young × large cells are suppressed ("D"), so young-firm shares are lower bounds.
  - `fsize` is the average of t−1 and t employment.
  - BDS employment is measured in March.

### 5.4 Are AI labs following the same pattern? Partly, with three differences

1. **The same age dynamics.** OpenAI (age ~8 at 500 employees) and Anthropic (age ~2–3) will appear in BDS 2024–2026 releases as *young large* firms in NAICS 51/54, as Databricks did around 2019. Expect a visible uptick in the age 0–5 × 1,000–4,999 cells for Information and Professional services.
2. **Too small to move the aggregate.** All frontier labs plus the leading app-layer firms total roughly 15–25k US employees (§1, §4) [A]. That is ~0.02–0.03% of the 73.9M employees in 500+ firms (2023). Even a doubling would leave the young share of large-firm employment around 4%. AI-native graduation is economically important but statistically invisible in firm-size shares.
3. **Graduation by absorption.** Many AI-era successes are acquired or acqui-hired before they graduate:

   | Year | Deal | Value | Tag |
   |---|---|---|---|
   | 2024 | Inflection → Microsoft | ~$650M licence, most staff | [R] |
   | 2024 | Adept → Amazon | n/a | [U] |
   | 2024 | Character.ai → Google | ~$2.7B | [U] |
   | 2024 | Covariant → Amazon | n/a | [U] |
   | 2025 | Windsurf → Google | ~$2.4B | [U] |
   | 2025 | Scale AI → Meta | 49% stake for $14.3B | [R] |
   | 2026 | xAI → SpaceX | $250B | [R] |
   | 2026 | Cursor → SpaceX | $60B | [R] |
   | Jan 2026 | AI21 → Nvidia | reported, denied | [R] |

   Q2 2026 had a record 24 $1B+ venture-backed acquisitions [R]. BDS firm age is the age of the firm's oldest establishment, so when an old acquirer absorbs a young AI firm, its workers are **reclassified from young-firm to old-firm employment**. This makes young AI firms' success look like incumbent growth in BDS, which is a measurement trap for any age-based test in the paper. Licence-plus-hire deals move the workers directly into the incumbent's payroll and leave a hollowed-out young firm.
4. **Capital intensity breaks the employment link.** In the cloud era, a graduate's valuation, revenue and headcount moved together. For frontier labs, valuation and revenue grow 10–100× faster than headcount. "Large" by capital, revenue or market power no longer implies "large" by employment, while BDS measures only employment.

### 5.5 Testable signatures for the paper (what to watch as data arrive)

| Signal | Source | Expected if AI → small/solo rebalancing | Expected if AI → scale/incumbents |
|---|---|---|---|
| WBA/BA and HBA/BA in NAICS 51/54 | BFS monthly | BA up and WBA/BA down (already observed) | WBA/BA flat, BA flat |
| Nonemployer counts, NAICS 5112/5415/5182 | Census NES 2024+ | Sharp rise | Flat |
| BF8Q conversion of 2023–26 cohorts | BFS (when published) | Low conversion, small initial size | n/a |
| Age 0–5 × 500+ employment, NAICS 51/54 | BDS 2024–2026 | Small uptick (labs) | Same uptick, then lost to M&A |
| Young (≤10) share of large-firm employment | BDS | Stable or up | Continued decline (absorption) |
| AI use by firm size | Census BTOS | Small-firm use catches up | Gap widens (current: 37% vs <20%) |
| Revenue or value added per employee in young firms | QCEW/BDS + private data | Rises sharply in young firms | Rises mainly in incumbents |

---

## 6. Open items and data gaps

1. **Anthropic S-1 (filed publicly 26 Oct 2026).** Pull official headcount, revenue and compute commitments from SEC EDGAR and replace the [A] figures in §1.2 and §4.1.
2. **OpenAI headcount** has no official source. FT's ~4,500 direct payroll (Mar 2026) is the most credible. Revelio's 7,850 likely includes broader entities.
3. **2026 funding totals** come from Crunchbase/PitchBook press coverage relayed by secondary sites. Confirm the Q1–Q3 2026 figures on news.crunchbase.com and the PitchBook-NVCA PDF.
4. **WBA decline:** check for 2025–26 changes to the IRS SS-4 / EIN online application before giving it a behavioural interpretation.
5. **BDS 2024 release:** if published, re-run `bds2023_fa_fz` → `bds2024_fa_fz` and the sector version to catch the first AI-era cohorts.
6. **[U] items** (cloud-era headcounts, pre-2025 AI round details) come from domain knowledge. Verify against S-1s (Snowflake 2020) and company announcements before citing.

---

## 7. Sources

**Official data (computed, [C])**
- Census BFS monthly CSV: [bfs_monthly.csv](https://www.census.gov/econ/bfs/csv/bfs_monthly.csv) (downloaded 2026-10-29; data through Sep 2026)
- Census BDS 2023 release: [BDS time-series tables](https://www2.census.gov/programs-surveys/bds/tables/time-series/2023/) (`bds2023_fa_fz.csv`, `bds2023_sec_fa_fz.csv`)

**Government / research ([R], [P])**
- Census, "Large Firms With at Least 20 Employees Biggest AI Users" (BTOS, May 2026): [census.gov](https://census.gov/library/stories/2026/05/ai-use-businesses.html)
- Stanford HAI, 2026 AI Index, Economy chapter: [hai.stanford.edu](https://hai.stanford.edu/ai-index/2026-ai-index-report/economy)
- Haltiwanger, Jarmin & Miranda (2013), *REStat* 95(2): 347–361. Decker et al. (2014), *JEP* 28(3): 3–24. Ewens, Nanda & Rhodes-Kropf (2018), *JFE* 128(3). Sterk, Sedláček & Pugsley (2021), *AER* 111(2). (See `data/sources.md` for DOIs of the cloud-era papers.)

**Venture data ([R])**
- Crunchbase, AI funding EOY 2025: [news.crunchbase.com](https://news.crunchbase.com/ai/big-funding-trends-charts-eoy-2025/)
- Crunchbase, 2024 EOY (AI $55.6B in 2023 → $100B+ in 2024): [news.crunchbase.com](https://news.crunchbase.com/venture/global-funding-data-analysis-ai-eoy-2024)
- Crunchbase H1 2026 ($510B) coverage: [startuphub.ai](https://www.startuphub.ai/news/ai-startup-funding-record-h1-2026); [siliconcanals.com](https://siliconcanals.com/t-in-the-first-quarter-of-2026-investors-poured-roughly-242-billion-into-ai-startups/)
- Crunchbase Q3 2026 coverage: [fourweekmba.com](https://fourweekmba.com/ai-crunchbase-q3-2026-159b-venture-27-billion-dollar-rounds-ai/); [aiweekly.co](https://aiweekly.co/alerts/crunchbase-logs-27-billion-dollar-rounds-in-q3-2026-as-ai-grabs-102b-or-64-of)
- PitchBook-NVCA Venture Monitor coverage, 2025 / H1 2026 / Q3 2026: [SiliconANGLE Jan 2026](https://siliconangle.com/2026/01/07/pitchbook-ai-dominates-global-venture-capital-2025-deal-value-nears-record/); [SiliconANGLE Jul 2026](https://siliconangle.com/2026/07/09/pitchbook-us-venture-funding-hits-412-7b); [SiliconANGLE Oct 2026](https://siliconangle.com/?p=849755)
- NVCA 2026 Yearbook: [nvca.org](https://nvca.org/?p=124853)
- PitchBook US 2024 AI $97B (via Bloomberg/Tech Brew): [techbrew.com](https://www.techbrew.com/stories/2025/01/13/ai-startups-venture-capital-2024-crunchbase)
- Carta Solo Founders Report 2025: [carta.com](https://carta.com/data/solo-founders-report)

**Company-level ([R]/[A])**
- Anthropic newsroom (S-1 filing, 26 Oct 2026): [anthropic.com/news](https://www.anthropic.com/news)
- Anthropic Series H coverage: [aimagazine.com](https://aimagazine.com/news/anthropic-claude-enterprise-ai-agents-and-965bn-valuation); [techmarketview.com](https://www.techmarketview.com/ukhotviews/archive/2026/05/29/anthropic-closes-in-on-a-trillion-dollar-valuation); draft-S-1 coverage: [aiweekly.co](https://aiweekly.co/alerts/anthropic-s-1-shows-163b-h1-revenue-25-from-two-customers-and-807b-non-cash)
- Anthropic headcount estimates: [trueup.io](https://trueup.io/co/anthropic); [makerstations.io](https://makerstations.io/anthropic-employee-statistics)
- OpenAI $110B round: [w.media](https://w.media/openai-raises-us-110-billion-and-expands-ties-with-softbank-nvidia-and-amazon/); [AP via sharonherald.com](https://www.sharonherald.com/ap/openai-gets-110-billion-in-funding-from-a-trio-of-tech-powerhouses-led-by-amazon/article_3e889ce8-16ba-5f48-9c7b-af61ad6271c8.html)
- OpenAI headcount: [Revelio Labs](https://reveliolabs.com/companies/openai-opco/employees/); [letsdatascience.com (FT report)](https://letsdatascience.com/news/openai-plans-to-nearly-double-its-workforce-83290b1a)
- SpaceX–xAI: [SCMP](https://www.scmp.com/news/world/united-states-canada/article/3342161/musk-merges-xai-spacex-bid-build-space-data-centres); [Sacra](https://sacra.com/research/why-spacex-acquired-xai/)
- Mistral Series D: [Orrick](https://www.orrick.com/en/News/2026/09/Orrick-Advises-Mistral-in-its-3B-Series-D-at-21B-Post-Money-Valuation); [Sifted](https://sifted.eu/articles/report-mistral-raise-20bn-valuation); [Wikipedia](https://en.wikipedia.org/wiki/Mistral_AI)
- Cohere: [PYMNTS](https://www.pymnts.com/startups/2026/ai-startup-cohere-targets-20-billion-dollar-valuation-funding-round/); [trueup.io](https://www.trueup.io/co/cohere)
- AI21: [Globes](https://en.globes.co.il/en/article-1001531815); [StorageNewsletter](https://www.storagenewsletter.com/2026/01/02/nvidia-in-advanced-talks-to-acquire-ai21-labs/)
- Inflection: [BNN Bloomberg](https://www.bnn.ca/inflection-ai-plans-pivot-after-most-employees-go-to-microsoft-1.2049041); [Axios](https://www.axios.com/2024/08/26/inflection-pi-ai-chatbot-enterprise)
- SSI: [Maginative](https://www.maginative.com/article/safe-superintelligence-raises-1-billion-reaching-5-billion-valuation-in-just-three-months/); [komo.ai](https://komo.ai/directory/safe-superintelligence-funding)
- Thinking Machines Lab: [letsdatascience.com](https://letsdatascience.com/news/thinking-machines-lab-pursues-5-6-billion-funding-round-19b69cd4); [trueup.io](https://trueup.io/co/thinking-machines)
- Cursor: [Wikipedia](https://en.wikipedia.org/wiki/Cursor_(company)); [Enterprise DNA](https://enterprisedna.co/resources/ai-map/company/cursor)
- Lovable: [Dealroom](https://dealroom.co/news/144597-lovable-raises-400m-at-13-3b-valuation-eyes-600m-revenue-run-rate); [letsdatascience.com](https://letsdatascience.com/news/lovable-raises-400-million-at-133-billion-valuation-974a9327)
- Perplexity: [getlatka.com](https://getlatka.com/companies/perplexity.ai); [trueup.io](https://www.trueup.io/co/perplexity-ai)
- Databricks: [Bloomberg Law](https://news.bloomberglaw.com/private-equity/coatue-leads-databricks-funding-round-at-188-billion-valuation); [Forge Global](https://forgeglobal.com/insights/databricks-upcoming-ipo-news/); [getlatka.com](https://getlatka.com/companies/databricks/vs/zaavia)
