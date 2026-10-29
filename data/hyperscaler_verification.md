# Hyperscaler capex-for-headcount claims: verification log

Verified 2026-10-29. This covers the claims in `paper/sections/07-discussion.tex` (§ "Labs as the hyperscalers of AI" and § "Hyperscaler capex-for-headcount substitution").

Evidence strength: **strong** means two or more independent sources agree, **moderate** means a single source, **weak** means secondary only or unconfirmed.

## Summary

| # | Original claim in paper | Verdict | Corrected / softened text | Strength |
|---|---|---|---|---|
| 1 | Microsoft Oct 2026 voluntary exit offered to 60,000 employees | **Verified** | Kept. Added eligibility scope and the caveat "eligibility, not exits" | strong |
| 2 | "25% of its workforce" | **Approximately true** | Changed to "roughly a quarter". 60,000 / 223,000 ≈ 27% | strong |
| 3 | "4,800 layoffs in July 2025" | **FALSE** | ~9,000 layoffs (<4% of workforce) starting July 2, 2025 | strong |
| 4 | AI capex "reached $80 billion annually" | **Stale / misleading** | $80B was the *FY2025 plan*. Q4 FY26 alone was $41B and CY2026 guidance is ~$175B | strong |
| 5 | Bridgewater: hyperscaler AI capex $650B in 2026 | **Verified via secondary only** | Changed to "reportedly"; added the $410B 2025 baseline and the four named firms | weak–moderate |
| 6 | "four times the scale of any prior technology infrastructure buildout" | **Unsupported, no source found** | **Removed** | none |
| 7 | "Microsoft is trading headcount for data-center capacity" | Interpretive | Softened to "consistent with ...", with a causation caveat | n/a |
| 8 | Microsoft 238,000 employees | **Wrong / stale** | ~223,000 (end of June 2026) | moderate |
| 9 | Google 186,000 employees | **Stale** | "roughly 190,000" (190,820 at YE2025; 198,933 at Jun 30, 2026, per secondary sources) | weak–moderate |
| 10 | Nvidia 29,600 employees | **Not verified** (likely FY2024 / Jan 2024 figure; stale) | Number removed | — |

## Detail and sources

### 1–2. Microsoft October 2026 voluntary exit offer
- Announced and confirmed Oct 26, 2026. About 60,000 eligible employees at VP level and below on select teams in the US, Canada, India, and UK. Some data-center, sales, and marketing staff are excluded. Terms are similar to standard severance. Chief People Officer Amy Coleman: "The Voluntary Exit Offer is new for us." TechCrunch cites a headcount of 223,000 at the end of June. Participating divisions per Bloomberg: Xbox, Windows, Copilot, and Finance.
- Acceptance decisions are due in early December, and those who accept leave on Dec 31, 2026. **Uptake has not been reported.** Forbes' figure of "18,000 if 30% accept" is a hypothetical.
- Earlier in 2026 (Apr): a voluntary retirement offer to ~8,750 US staff, with >30% acceptance per Bloomberg.
- Sources:
  - [TechCrunch, Oct 26 2026](https://techcrunch.com/2026/10/26/microsoft-offers-buyouts-to-around-60000-employees-reports-say/) (fetched; cited in the paper)
  - [Bloomberg, Oct 26 2026](https://www.bloomberg.com/news/articles/2026-10-26/microsoft-to-offer-buyouts-to-60-000-workers-in-latest-cost-cut)
  - [CNBC](https://www.cnbc.com/2026/10/26/microsoft-msft-voluntary-buyouts.html)
  - [Forbes](https://www.forbes.com/sites/maryroeloffs/2026/10/26/microsoft-offers-buyouts-to-25-of-company/)
  - [KUOW](https://www.kuow.org/technology/2026-10-26/microsoft-offers-voluntary-buyouts-to-a-quarter-of-its-workforce)
  - [CTV](https://www.ctvnews.ca/world/article/microsoft-offers-voluntary-exit-packages-to-60000-staff/)
- No SEC filing (8-K) was located for the buyout. Coleman's note is reportedly on Microsoft's blog, but I did not fetch it.

### 3. July 2025 layoffs
- About 9,000 roles cut, beginning July 2, 2025, described as "less than 4%" of the June 2024 workforce of 228,000. This followed ~6,000 cuts in May 2025 and ~300 in June 2025. No source anywhere gives **4,800**, so that figure appears to be an error.
- Sources:
  - [Verdict / AP, Jul 3 2025](https://www.verdict.co.uk/microsoft-layoffs-affecting-9000-roles/) (fetched; cited in the paper)
  - [Seeking Alpha](https://seekingalpha.com/news/4464877-microsoft-plans-to-reduce-workforce-by-about-9000-in-latest-round-of-layoffs-report)
  - Reuters, via the Seattle Times, reports ~9,100.

### 4. Microsoft capex
- Brad Smith, Jan 3, 2025: "In FY 2025, Microsoft is on track to invest approximately $80 billion to build out AI-enabled datacenters." [Microsoft blog](https://blogs.microsoft.com/on-the-issues/2025/01/03/the-golden-opportunity-for-american-ai/) (fetched)
- FY26 Q4 earnings call (July 2026), CFO Amy Hood: "Capital expenditures were $41 billion" in the quarter. CY2026 capex is guided to "approximately $175 billion" after a finance-to-operating-lease reclassification; the underlying expectation is unchanged from ~$190B. FY27 Q1 is expected at >$50B. "Total company headcount declined 2% year-over-year." [Microsoft IR](https://www.microsoft.com/en-us/investor/events/fy-2026/earnings-fy-2026-q4) (fetched)
- Aggregators put full-year FY2026 capex at ~$116B, up ~80% YoY: [fiscal.ai](https://fiscal.ai/company/NASDAQ_MSFT/metrics/cash-flow-statement/capital-expenditure/), [investmentvisual](https://www.investmentvisual.com/stocks/msft/financials/capital-expenditures). Not checked against the 10-K.
- One secondary source says the Oct 28, 2026 call cut CY2026 to ~$170B because of third-party capacity delays: [FourWeekMBA](https://fourweekmba.com/ai-microsoft-lowers-2026-capex-view-to-170b-eyes-new-funding/). Unconfirmed, so the paper uses the July primary figure.

### 5–6. Bridgewater $650B
- Secondary summaries of Bridgewater research say Alphabet, Amazon, Meta, and Microsoft are on track for ~$650B of AI infrastructure spend in 2026, up from ~$410B in 2025, with buybacks at their lowest since 2019.
  - [Alpha-Maven / HedgeCo](https://www.alpha-maven.com/story/hedge-fund/bridgewater-associates-issues-structural-warning-ai-boom-enteringdangerous-phase): returned 403 and could not be read directly.
  - [AI 2027 tracker](https://ai2027-tracker.com/predictions/infra-investment/)
- Independent corroboration of the magnitude: [LPL Research](https://www.lpl.com/research/blog/hyperscalers-plan-to-live-up-to-their-name.html) cites >$600B for 5 firms; [IEEE ComSoc techblog](https://techblog.comsoc.org/2025/12/22/hyperscaler-capex-600-bn-in-2026) cites ~$600B.
- **Bridgewater's original publication was not located.** The "four times any prior buildout" comparison appears in none of these sources, so it was removed.

### 8–10. Headcounts
- Microsoft: ~223,000 at end of June 2026, per [TechCrunch](https://techcrunch.com/2026/10/26/microsoft-offers-buyouts-to-around-60000-employees-reports-say/). This is consistent with 228,000 (Jun 2024/2025) less a 2% decline.
- Alphabet: 190,820 at YE2025 (10-K, per secondary sources) and 198,933 at Jun 30, 2026 (secondary): [Octagon](https://octagonai.co/markets/financials/kpis/google-headcount-in-2026/). **TODO:** confirm against the 10-K/10-Q on EDGAR.
- Nvidia: not checked. 29,600 matches the FY2024 10-K (Jan 2024) and is likely stale. **TODO:** pull the FY2026 10-K if a number is reinstated.

## Remaining open items
- Bridgewater primary source (Daily Observations / client note) is needed if the $650B figure is to carry weight.
- Microsoft 10-K FY2026: full-year capex and exact headcount.
- Buyout uptake numbers after the December 2026 deadline.
