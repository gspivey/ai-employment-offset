# Anthropic, PBC — Form S-1 Extract (filed 2026-10-26)

- **Filer:** Anthropic, PBC — CIK 0002130357 — Accession 0001628280-26-067168
- **Filing index:** https://www.sec.gov/Archives/edgar/data/2130357/000162828026067168/
- **Main prospectus (source for every item below unless noted):** https://www.sec.gov/Archives/edgar/data/2130357/000162828026067168/anthropicpbc-sx1.htm (14.2 MB HTML)
- **Extracted:** 2026-10-29 by PlayEcon

> **How the document was accessed.** The "224 MB" size is the full submission `.txt`, which bundles ~20 multi-MB JPG graphics. The prospectus HTML is only 14.2 MB, so I downloaded it whole and converted it to text. No byte-range requests or full-text search were needed. The XBRL package (`-xbrl.zip`, 3 KB; R1–R3) covers only the cover page and filing-fee data. It contains no financial statements.
>
> **Page references** are the printed page numbers in the prospectus where I could see them in the text (e.g., "p. 23", "F-47"). Otherwise the reference is the section heading.

---

## ⚠️ Big caveat: this is a preliminary ("red herring") S-1

Many key numbers are **left blank** (`$ `) and will be filled in by amendment. Blank in this filing:
- IPO price range, shares offered, and so the **IPO valuation target**
- **Revenue for Q3 2026** (three months ended Sept 30, 2026). The text says "revenue growing from $0 … to $ for the three months ended September 30, 2026" (Prospectus Summary, p. 6)
- **Run-Rate Revenue as of Oct 31, 2026** ("our Run-Rate Revenue was $ as of October 31, 2026", Business, p. 195)
- **Total compute/infrastructure commitments** ("aggregate committed spend of more than $ , substantially all of which is related to compute and infrastructure", p. 6)
- All pro forma / pro forma as-adjusted balance-sheet and EPS figures

Audited/reviewed financials run through **June 30, 2026**. Q3 2026 appears only as operating metrics (headcount, customers, revenue per employee).

---

## 1. Headcount / employees

| Date | Employees | Source quote / section |
|---|---|---|
| Dec 31, 2024 | ~940 | "the number of our employees increased from approximately 940 as of December 31, 2024 to approximately 5,300 as of September 30, 2026" (Risk Factors, "If we fail to manage our growth effectively…", ~p. 63–64) |
| Sep 30, 2025 | ~1,960 (*derived*) | Not stated. Derived from "headcount increased approximately 170%" from Sep 30, 2025 to Sep 30, 2026 (MD&A Overview, p. 137): 5,300 / 2.7 ≈ 1,960 |
| **Sep 30, 2026** | **~5,300** | "As of September 30, 2026, we had approximately 5,300 employees worldwide, a majority of whom work in research, engineering, and product development functions." (Business, "Our Talent") |

Other headcount statements:
- "From December 31, 2024 to September 30, 2026, our headcount grew over five times, while our revenue for the three months ended September 30, 2026 was 86 times our revenue for the three months ended December 31, 2024." (Business, p. 184)
- "TTM revenue per employee of over $6.6 million as of September 30, 2026, compared to $1.4 million as of September 30, 2025." (Prospectus Summary, p. 11)
- Workforce growth plans: there is **no numeric hiring target**. Qualitative only: "We expect personnel expenses to increase in absolute dollars as we continue to expand our headcount…" (MD&A, Components of Results). "We leverage Claude itself to grow our business without growing headcount linearly" (Business, Growth Strategy, p. 197). The company also intends to "grow our direct go-to-market and Applied AI teams" (p. 13).
- Hiring execution risk: "Rapid growth has also created workforce-planning and execution challenges, including limitations in our ability to accurately forecast headcount needs, periods of accelerated hiring followed by corrective actions that may disrupt operations or reduce morale…" (Risk Factors, personnel)
- Collective bargaining: "In certain countries in which we operate, we are subject to… local labor law requirements which may automatically make our employees subject to industry-wide collective bargaining agreements." (Business, Our Talent)

---

## 2. Revenue

**Annual and half-year (Summary Consolidated Financial Data, p. 23; $ millions)**

| | FY2023 | FY2024 | FY2025 | H1 2025 | **H1 2026** |
|---|---|---|---|---|---|
| Revenue | 41 | 386 | **4,585** | 1,163 | **16,286** |

**Quarterly (Quarterly Results of Operations, p. 158; unaudited, $ millions)**

| | Q1'25 | Q2'25 | Q3'25 | Q4'25 | Q1'26 | Q2'26 | Q3'26 |
|---|---|---|---|---|---|---|---|
| Revenue | 376 | 787 | 1,382 | 2,040 | 4,731 | 11,555 | **blank** |

- Q4 2024 revenue: $197M (Risk Factors, growth section).
- "revenue that grew 1,368% year over year for the three months ended June 30, 2026 compared to compute and infrastructure expenses that grew 300%" (p. 11)
- **Projections:** none given. Run-Rate Revenue is defined (trailing-28-day consumption × 13 + monthly subscriptions × 12, p. 5), but the value is blank.
- **Derived Q3 2026 revenue estimate (my calculation, not in the filing): ≈ $16.9B.** It comes from "86 times" × $197M (Q4'24) ≈ $16.9B. A second check: TTM revenue/employee >$6.6M × 5,300 ≈ $35B TTM, minus Q4'25+Q1'26+Q2'26 ($18.3B), gives ≥ ~$16.7B. The two methods agree, but treat the figure as an estimate.

Customer metrics (Sep 30, 2026, p. 9–10): >11,900 customers at ≥$100K TTM (up from >950 a year earlier), >1,900 at ≥$1M, ~250 at ≥$10M. Net Revenue Retention ~900%.

---

## 3. Net income / loss

| $ millions | FY2023 | FY2024 | FY2025 | H1 2025 | **H1 2026** |
|---|---|---|---|---|---|
| Operating loss | (551) | (2,980) | **(8,060)** | (2,135) | **(693)** |
| Change in FV of convertible notes, derivatives, SAFEs | (1,045) | (5,434) | (34,308) | (10,942) | (72,388) |
| **Net loss** | (1,531) | (8,309) | **(41,965)** | (12,969) | **(80,748)** |
| Adjusted Operating Income (Loss) (non-GAAP) | (522) | (2,788) | (4,854) | (1,849) | **1,618** |
| Adjusted Net Income (Loss) (non-GAAP) | (457) | (2,683) | (4,448) | (1,741) | **2,671** |
| Operating margin | (1,344)% | (772)% | (176)% | (184)% | (4)% |
| Adjusted Operating Margin | (1,273)% | (722)% | (106)% | (159)% | 10% |

(p. 23, 25)

- Q2 2026 was the **first operating-profit quarter**: operating income $974M on $11.6B revenue (p. 158).
- ⚠️ **Read the net loss with care.** Most of it is non-cash mark-to-market on convertible instruments (mainly the Amazon notes), driven by rising valuation: "These changes were primarily driven by an increase in the fair value of our outstanding convertible promissory notes resulting from an increase in our enterprise valuation" (p. 23, fn. 2). H1 2026 also includes "Other expense" of $(8,757)M, of which $(8,448)M fell in Q2'26. I did not pin down the cause.
- Quarterly net loss: Q1'25 (6,592); Q2'25 (6,377); Q3'25 (12,138); Q4'25 (16,858); Q1'26 (14,439); Q2'26 (66,309).

---

## 4. Funding raised, valuation, balance sheet

- **Total capital raised:** "As of June 30, 2026, we had raised an aggregate of $141.1 billion of capital and had cash and cash equivalents of $112.4 billion and short-term investments of $19.3 billion." (p. 11)
- Debt: "As of June 30, 2026, our total indebtedness was $6.2 billion", all Amazon convertible notes (Risk Factors, p. 58)
- Balance sheet at Jun 30, 2026: total assets $147.4B; total liabilities $117.5B; redeemable convertible preferred $157.5B; accumulated deficit $(132.9)B (p. 24)

**Recent priced rounds** (Certain Relationships, p. 283; Notes, F-47)

| Round | Dates | Price / preferred share | Proceeds |
|---|---|---|---|
| Series E-1 | Jan–Mar 2025 | $56.0865 | $3.57B (E-1 only) |
| Series F-1 | Aug–Sep 2025 | $140.9676 | $13.0B |
| Series G (G-1 + G-2) | Q1–Q2 2026 | $259.1364 | $30.2B (Q1) + $15.0B (Q2) = $45.2B |
| Series H (H-1 + H-2) | May–Jun 2026 | $589.0095 | $65.2B (incl. Google $10.0B, Amazon $5.0B) |

- **No post-money valuation is stated.** I searched for "post-money", "valued at", and "valuation of"; the filing gives none.
- **IPO valuation target:** blank (no price range).
- ⚠️ **Implied Series H valuation (my calculation, weak):** the preferred-to-common conversion ratio is 10:1 after the 10-for-1 forward split of Sept 17, 2026 (Notes, F-47ff; p. 22). That makes Series H ≈ $58.90 per common share. The filing says 846,840,960 shares equals 5% of fully diluted shares at Jun 30, 2026, so fully diluted ≈ 16.94B shares. Multiplying gives **≈ $1.0 trillion**. This mixes a May–June price with a June 30 share count and assumes the Amazon notes convert in full. Confirm it against the press-reported Series H post-money.

---

## 5. Cost structure

The income statement classifies expenses **by nature**, not the usual R&D / S&M / G&A split. There is **no R&D line**.

| $ millions | FY2023 | FY2024 | FY2025 | H1 2025 | H1 2026 |
|---|---|---|---|---|---|
| Compute and infrastructure | 433 | 2,522 | **7,326** | 2,334 | **8,945** |
| Personnel | 95 | 454 | **1,839** | 538 | **3,152** |
| — of which SBC | 29 | 192 | 1,200 | 286 | 2,200 |
| Bartz settlement (copyright) | — | — | 1,500 | — | — |
| Sales, marketing, partnerships | 2 | 43 | 568 | 120 | 3,168 |
| Other operating & administrative | 62 | 347 | 1,412 | 306 | 1,714 |
| **Total opex** | 592 | 3,366 | 12,645 | 3,298 | 16,979 |

(p. 23)

- Compute as % of revenue fell from **251% (Q1'25) to 48% (Q2'26)**. Personnel fell from 58% to 16% (p. 158–159).
- Compute timing: "Because we typically procure compute 12 to 18 months in advance of availability, these expenses are generally fixed in the near term…" (p. 159)
- Compute is multi-chip: AWS Trainium, Google TPUs, NVIDIA GPUs, AMD GPUs (p. 6). Total commitments are blank. The disclosed fragments are ~$34.9B on a Lambda agreement (MD&A, Contractual Obligations), a Broadcom accelerator lease from March 2026, and AMD MI450 GPUs under a Hardware Supply Agreement.
- The rise in sales/marketing/partnerships comes mainly from "fees paid to channel partners" (CSPs) and media spend (p. 159).

---

## 6. AI's effect on Anthropic's own workforce productivity (direct quotes)

1. "over 90% of the contributions to our codebase in September 2026 were written by Claude. Additionally, the average daily volume of code contributed to our codebase per engineer in the three months ended September 30, 2026 was over 45 times the average daily volume in the year ended December 31, 2024." (MD&A Overview, p. 137; repeated in Business, p. 184, 197)
2. "Claude's success rate on these [open-ended engineering] problems reached approximately 90% in September 2026, up approximately 50 percentage points in nine months, based on our internal benchmarks… This has enabled our engineers to increasingly direct and review its work rather than write code line by line." (Business, p. 184)
3. "Across our research, engineering, go-to-market, and operations teams, Claude allows employees to leverage a team of agents in their daily work, enabling a comparatively small team to take on work that would traditionally require a far larger one by multiplying the impact of each person." (Business, p. 184–185)
4. **Internal usage compared with payroll:** "The value of our own internal Claude usage at list prices has grown by over 250 times from January 2026 to September 2026, and in April 2026, this monthly value first exceeded our monthly personnel expense, excluding stock-based compensation." (Business, p. 185)
5. "From September 30, 2025 to September 30, 2026, TTM revenue increased approximately 1,200% while headcount increased approximately 170%…" (MD&A, p. 137)
6. "Many aspects of the research, training, and testing of subsequent model generations now involve Claude, including running experiments, generating and processing training data, automating evaluations and safety audits, and writing and reviewing code. We refer to this recursive dynamic as 'closing the loop.'" (Prospectus Summary, p. 12)

## 7. Labor displacement and augmentation framing

- Augmentation framing in the summary: "Frontier AI is transforming cognitive work… We believe it will make humans far more capable and expand the world's overall capacity for that work" (p. 7). Knowledge work is valued at ">$40 trillion in economic value globally in 2025" (p. 8). "Virtual Collaborators… work alongside humans" (p. 8). Claude Code / Cowork "multiply the impact of employees… now frequently being used to conduct long-running autonomous work alongside employees" (p. 10).
- Customer value: "more productive employees, faster processes, and embedded intelligence in their products" (p. 10).
- Research commitments: "Our Economics team extends this work to the labor market, publishing recurring data reports and fully open datasets (the Anthropic Economic Index) on how Claude is used across jobs, industries, and regions, as well as modeling potential future economic scenarios…" The filing also mentions the Anthropic Institute (Business, Public Benefit, p. 235).

## 8. Risk factors on employment and labor markets

1. **Regulation driven by job displacement:** "In some jurisdictions, public concern regarding the potential displacement of labor by AI systems… has led, or could lead, to restrictive legislation… to the extent the rate of job displacement rapidly increases due to the adoption of AI… governments… may intervene to slow the rate of adoption of AI, restrict its use, or take other actions that increase the cost… we may from time to time voluntarily elect to take actions intended to ameliorate the impact of such displacement. Any such actions would represent additional costs and expenditures for which we may not receive a corresponding commercial benefit…" (Risk Factors, Regulation)
2. **AI-specific taxes:** a listed factor that could hurt results is "new or more restrictive laws… including taxes, fees, or other measures specifically applicable to AI companies or AI-related labor displacement" (Risk Factors, p. 63–64)
3. **Reputation:** "public perception that our models, platform, and applications contribute to job displacement or economic disruption could generate significant negative media coverage, customer or employee backlash, or organized opposition, regardless of the actual impact… on employment." (Risk Factors, Brand, p. 54–55)
4. **Own public statements used against them:** "Our public statements about… potential societal impacts, including statements regarding job displacement or economic disruption, may be used against us in litigation, regulatory proceedings, or public controversies…" (Risk Factors, Safety, p. 54)
5. **Media narratives:** coverage includes "recurring narratives… that AI may displace or eliminate jobs… We have been, and may continue to be, a particular focus of such narratives" (Risk Factors, Media)
6. **Internal workforce risks:** inaccurate headcount forecasting, "periods of accelerated hiring followed by corrective actions", and threats to employee safety (Risk Factors, Personnel)

---

## 9. Consistency checks

| Check | Result |
|---|---|
| FY2025 quarters sum to annual revenue: 376+787+1,382+2,040 = 4,585 | ✅ |
| FY2025 quarterly net loss sum = (41,965) | ✅ |
| H1 2026 revenue Q1+Q2 = 4,731+11,555 = 16,286 | ✅ |
| H1 2026 net loss Q1+Q2 = (14,439)+(66,309) = (80,748) | ✅ |
| 940 to 5,300 employees = 5.6×, matching "over five times" | ✅ |
| Sep 2025 TTM revenue (197+376+787+1,382 = $2.74B) / $1.4M per employee ≈ 1,960 employees, consistent with "+170%" to 5,300 | ✅ |
| Q3'26 revenue from "86×" (~$16.9B) vs from rev/employee (≥$16.7B) | ✅ consistent (derived) |
| "Six months ended June 30, 2026" vs "H1 2026" | Equivalent; the filing never uses "H1" |
| Q2'26 revenue +1,368% YoY: 787 × 14.68 = 11,553 | ✅ |
| Rounds listed (E-1 + F + G + H ≈ $127B) vs "$141.1B raised" | Plausible. The gap is earlier rounds plus Amazon/Google notes and SAFEs. Not reconciled line by line |

**Needs verification or follow-up**
- Q3 2026 revenue, Run-Rate Revenue, IPO price range, and total compute commitments are **blank**. Watch for an S-1/A on EDGAR.
- The ~$1.0T implied Series H valuation is my derivation. It is not stated in the filing.
- Cause of the $(8.4)B "Other expense" in Q2 2026 not yet identified (check MD&A "Other income (expense), net").
- The "Personnel" line includes SBC, which jumped to $2.2B in H1 2026. Personnel excluding SBC ≈ $0.95B in H1 2026.
