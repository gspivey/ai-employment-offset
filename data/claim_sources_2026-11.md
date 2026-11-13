# Primary sources for `% [claim]` items in 07-discussion.tex (and Bonney et al. check)

Compiled 2026-11-07. Every URL below was opened during this pass unless the entry says otherwise. Quotes are verbatim from the opened page or PDF. Lines marked **Inference** are our own arithmetic or reading and are not stated by the source.

Status key: **VERIFIED** (source supports the paper's figure) / **CORRECTED** (source gives a different figure, shown) / **NOT FOUND** (no openable primary source; attempts listed).

---

## Item 1. CoreWeave (SEC filings)

| Claim as stated in paper | Status | Correct figure / note |
|---|---|---|
| 2,189 employees (2025) | VERIFIED | 2,189 at 31 Dec 2025 |
| $5.13B revenue (2025) | VERIFIED | $5,131M FY2025 ($1,915M FY2024) |
| $35.1B debt (June 2026) | VERIFIED (by summation) | Balance-sheet debt lines at 30 Jun 2026 sum to $35,068M |
| Microsoft = 67% of revenue | VERIFIED, needs date | 67% is **FY2025** (year ended 31 Dec 2025). FY2024 was 62%. The Q2 2026 10-Q does not name Microsoft. |
| ~940 employees Dec 2024 | CORRECTED / misattributed | CoreWeave had **881** at 31 Dec 2024. In the paper, "940 (December 2024)" is Anthropic's S-1 figure (07-discussion.tex line 108), not CoreWeave's. |

**1a. FY2025 Form 10-K** (filed 2026-03-02). URL: https://www.sec.gov/Archives/edgar/data/1769628/000176962826000104/crwv-20251231.htm
- Headcount: "As of December 31, 2025, we had 2,189 employees, with 1,967 in the United States and 222 in 19 other countries."
- Revenue: "Our revenue was $5.1 billion, $1.9 billion, and $229 million for the years ended December 31, 2025, 2024, and 2023". The results-of-operations table gives $5,131 million (2025) and $1,915 million (2024).
- Microsoft share: "We recognized an aggregate of approximately 67% of our revenue from our top customer, Microsoft, for the year ended December 31, 2025."
- Context, year-end debt: "As of December 31, 2025, our total indebtedness was $21.6 billion."

**1b. Q2 2026 Form 10-Q** (period ended 2026-06-30, filed 2026-08-12). URL: https://www.sec.gov/Archives/edgar/data/1769628/000176962826000366/crwv-20260630.htm
- Condensed balance sheet at 30 Jun 2026 (in $M): "Recourse debt, current" 6,235; "Non-recourse debt, current" 1,278; "Recourse debt, non-current" 25,170; "Non-recourse debt, non-current" 2,385.
- **Inference:** the four lines sum to $35,068M ≈ $35.1B in book value. The parts of the 10-Q we read contain no single "total debt" sentence. Note 10 (Debt) was not read.
- Customer concentration in this 10-Q is anonymised: Customer A was 36% of revenue for the three months and 40% for the six months ended 30 Jun 2026. The filing does not say which customer is Microsoft, so the paper should not attach "67%" to June 2026.
- Secondary corroboration (not primary): runtimewire.com, "CoreWeave reports $2.58 billion Q2 revenue with $35 billion in debt".

**1c. IPO prospectus (424B4, 2025-03-31)**, for Dec 2024 headcount and FY2024 Microsoft share. URL: https://www.sec.gov/Archives/edgar/data/1769628/000119312525067651/d899798d424b4.htm
- Microsoft "accounted for 35% and 62% of our revenue, respectively" for 2023 and 2024.
- Headcount, 881: EDGAR full-text search for the exact phrase `"881 employees" "December 31, 2024"` within CoreWeave's CIK returns this 424B4 and the S-1/S-1A/DRS filings (https://efts.sec.gov/LATEST/search-index?q=%22881%20employees%22%20%22December%2031%2C%202024%22&ciks=0001769628). We could not render the Human Capital paragraph itself (the page truncates), so 881 rests on the full-text match. stockanalysis.com and TipRanks also report 881.

**Suggested text fix (inference):** "...(Microsoft represented 67\% of 2025 revenue)".

```bibtex
@misc{coreweave2026tenk,
  author       = {{CoreWeave, Inc.}},
  title        = {Form 10-K: Annual Report for the Fiscal Year Ended December 31, 2025},
  howpublished = {U.S. Securities and Exchange Commission, EDGAR},
  year         = {2026},
  month        = mar,
  url          = {https://www.sec.gov/Archives/edgar/data/1769628/000176962826000104/crwv-20251231.htm},
  urldate      = {2026-11-07}
}
@misc{coreweave2026tenq,
  author       = {{CoreWeave, Inc.}},
  title        = {Form 10-Q: Quarterly Report for the Period Ended June 30, 2026},
  howpublished = {U.S. Securities and Exchange Commission, EDGAR},
  year         = {2026},
  month        = aug,
  url          = {https://www.sec.gov/Archives/edgar/data/1769628/000176962826000366/crwv-20260630.htm},
  urldate      = {2026-11-07}
}
@misc{coreweave2025prospectus,
  author       = {{CoreWeave, Inc.}},
  title        = {Prospectus (Form 424B4)},
  howpublished = {U.S. Securities and Exchange Commission, EDGAR},
  year         = {2025},
  month        = mar,
  url          = {https://www.sec.gov/Archives/edgar/data/1769628/000119312525067651/d899798d424b4.htm},
  urldate      = {2026-11-07}
}
```

---

## Item 2. Cursor, Lovable, Vercel

### 2a. Cursor (Anysphere)

| Claim as stated in paper | Status | Correct figure / note |
|---|---|---|
| ~$3B ARR (May 2026) | VERIFIED, with nuance | Bloomberg, 21 May 2026: $3B reached "in late April" 2026. Forbes (8 Jun 2026) later reported >$4B; we did not open it. |
| ~300 employees (dated Aug 2025) | CORRECTED | Company blog, 13 Nov 2025: "over 300". **Most recent credible figure: about 800 (Business Insider, 15 May 2026).** |
| $10.0M revenue per employee | CORRECTED (inference) | $3B / ~800 ≈ **$3.75M**. The paper's $10M pairs a May 2026 ARR with a 2025 headcount. |
| $60B SpaceX acquisition (Aug 2026) | VERIFIED | Agreement 16 Jun 2026, closed 14 Aug 2026, implied equity value $60.0B paid in SpaceX Class A stock (item 3) |

**ARR source.** R. Metz, "Cursor Hits \$3 Billion Annual Sales Rate Ahead of SpaceX Deal", *Bloomberg*, 21 May 2026. URL: https://www.bloomberg.com/news/articles/2026-05-21/cursor-hits-3-billion-annual-sales-rate-ahead-of-spacex-deal. Bloomberg returned HTTP 403. The quote comes from Investing.com's report of the Bloomberg story (https://ca.investing.com/news/stock-market-news/cursors-annual-revenue-hits-3-billion-ahead-of-spacex-acquisition--bloomberg-93CH-4655150, 21 May 2026): "Cursor's annualized revenue reached $3 billion in late April, a person familiar with the matter told Bloomberg".

**Headcount sources.**
- Company blog, "Past, Present, and Future", 13 Nov 2025 (https://cursor.com/blog/series-d): "grown to a team of over 300 engineers, researchers, designers, and operators", and "crossed $1B in annualized revenue". At that date, $1B / 300 ≈ $3.3M per employee (inference).
- B. Nolan, *Fortune*, 8 Dec 2025 (https://fortune.com/2025/12/08/cursor-developed-an-internal-ai-help-desk-that-handles-80-of-its-employees-support-tickets-says-the-29-billion-startups-ceo/): Cursor "now has more than 300 employees". Wikipedia uses this article for its "August 2025, roughly 300" line, but the article itself dates the figure to November 2025.
- **Most recent:** *Business Insider*, republished by Agooka News on 15 May 2026 (https://agooka.com/news/usa/cursor-is-gearing-up-for-a-6-month-hiring-spree-in-one-region/): "Cursor has about 800 employees in San Francisco and New York." Analytics India Magazine reported the same on 1 Jun 2026, crediting Business Insider (https://analyticsindiamag.com/ai-news/ai-coding-startup-cursor-to-hire-200-across-asia-pacific-in-major-expansion-push): "Cursor currently employs around 800 people across its offices in San Francisco and New York." businessinsider.com blocks our fetcher, so we could not open or confirm the original BI URL.
- Aggregator estimates range from ~180 to ~1,800 (Latka, Revelio, UnifyGTM) and were not used.

```bibtex
@misc{metz2026cursor,
  author       = {Metz, Rachel},
  title        = {Cursor Hits \$3 Billion Annual Sales Rate Ahead of {SpaceX} Deal},
  howpublished = {Bloomberg},
  year         = {2026},
  month        = may,
  day          = {21},
  url          = {https://www.bloomberg.com/news/articles/2026-05-21/cursor-hits-3-billion-annual-sales-rate-ahead-of-spacex-deal},
  urldate      = {2026-11-07}
}
@misc{cursor2025seriesd,
  author       = {{Cursor (Anysphere, Inc.)}},
  title        = {Past, Present, and Future},
  howpublished = {Company blog},
  year         = {2025},
  month        = nov,
  day          = {13},
  url          = {https://cursor.com/blog/series-d},
  urldate      = {2026-11-07}
}
@misc{bi2026cursorhiring,
  author       = {{Business Insider}},
  title        = {Cursor Is Gearing Up for a 6-Month Hiring Spree in One Region},
  howpublished = {Business Insider, republished by Agooka News},
  year         = {2026},
  month        = may,
  day          = {15},
  url          = {https://agooka.com/news/usa/cursor-is-gearing-up-for-a-6-month-hiring-spree-in-one-region/},
  urldate      = {2026-11-07},
  note         = {Original Business Insider URL not accessible}
}
```

### 2b. Lovable

| Claim as stated in paper | Status | Correct figure / note |
|---|---|---|
| $200M ARR (November 2025) | VERIFIED | TechCrunch, 19 Nov 2025 |
| ~120 employees | NOT FOUND (primary) | Wikipedia cites *NYT* DealBook, 18 Dec 2025; nytimes.com is blocked to our fetcher. Lovable's Series B post and Fortune's 18 Dec 2025 article give no headcount. **Earliest verifiable figure: 146 full-time employees at $400M ARR (Feb 2026, TechCrunch).** |
| $1.7M revenue per employee | Replace (inference) | With the verifiable pair: $400M / 146 ≈ **$2.7M** (Feb 2026) |
| $13.3B valuation (Aug 2026) | VERIFIED | Company blog and TechCrunch, 12 Aug 2026 |

- R. Szkutak, "As Lovable hits \$200M ARR, its CEO credits staying in Europe for its success", *TechCrunch*, 19 Nov 2025 (https://techcrunch.com/2025/11/19/as-lovable-hits-200m-arr-its-ceo-credits-staying-in-europe-for-its-success/): Lovable "doubled its annual recurring revenue (ARR) to $200 million in just four months". No headcount given.
- A. Heim, "Lovable says it added \$100M in revenue last month alone, with just 146 employees", *TechCrunch*, 11 Mar 2026 (https://techcrunch.com/2026/03/11/lovable-says-it-added-100m-in-revenue-last-month-alone-with-just-146-employees/): Lovable "crossed $400 million in annual recurring revenue in February" and "achieved $400 million ARR with only 146 full-time employees". The headcount comes from the company's CRO via Business Insider.
- J. Bort, "Lovable confirms new \$13.3B valuation, raises another \$400M", *TechCrunch*, 12 Aug 2026 (https://techcrunch.com/2026/08/12/lovable-confirms-new-13-3b-valuation-raises-another-400m/): the round was "at a $13.3 billion valuation", and Lovable reached "$500 million in annualized run rate revenue" in June 2026.
- Company blog, 12 Aug 2026 (https://lovable.dev/blog/series-c): "raised $400 million in Series C funding at a $13.3 billion valuation". The post also plans to "grow to roughly 450 team members this year".

```bibtex
@misc{szkutak2025lovable,
  author       = {Szkutak, Rebecca},
  title        = {As {Lovable} Hits \$200M {ARR}, Its {CEO} Credits Staying in {Europe} for Its Success},
  howpublished = {TechCrunch},
  year         = {2025},
  month        = nov,
  day          = {19},
  url          = {https://techcrunch.com/2025/11/19/as-lovable-hits-200m-arr-its-ceo-credits-staying-in-europe-for-its-success/},
  urldate      = {2026-11-07}
}
@misc{heim2026lovable,
  author       = {Heim, Anna},
  title        = {Lovable Says It Added \$100M in Revenue Last Month Alone, with Just 146 Employees},
  howpublished = {TechCrunch},
  year         = {2026},
  month        = mar,
  day          = {11},
  url          = {https://techcrunch.com/2026/03/11/lovable-says-it-added-100m-in-revenue-last-month-alone-with-just-146-employees/},
  urldate      = {2026-11-07}
}
@misc{bort2026lovable,
  author       = {Bort, Julie},
  title        = {Lovable Confirms New \$13.3B Valuation, Raises Another \$400M},
  howpublished = {TechCrunch},
  year         = {2026},
  month        = aug,
  day          = {12},
  url          = {https://techcrunch.com/2026/08/12/lovable-confirms-new-13-3b-valuation-raises-another-400m/},
  urldate      = {2026-11-07}
}
```

### 2c. Vercel

| Claim as stated in paper | Status | Correct figure / note |
|---|---|---|
| $9.3B valuation (Sep 2025) | VERIFIED | Company blog, 30 Sep 2025 |
| ~550 employees | VERIFIED but **dated January 2025** | *Fortune*, 24 Jan 2025, when Vercel was valued at $3.25B |
| ~$300M revenue estimate | NOT FOUND as stated | No primary source gives ~$300M for Sep 2025. Nearest primary-reported figure: **$340M run-rate (end Feb 2026)**, from Forbes via TechCrunch. **Inference:** "$300M" may be confused with the $300M Series F raise, or the ~$300M tender offer. |

- Company blog, "Towards the AI Cloud: Our Series F", 30 Sep 2025 (https://vercel.com/blog/series-f): a $300M Series F co-led by Accel and GIC at a $9.3B valuation, plus a "~$300M tender offer". No revenue or headcount is given. The Reuters report (https://www.reuters.com/business/ai-coding-startup-vercel-raises-300-million-valued-93-billion-2025-09-30/) is blocked to our fetcher.
- A. Garfinkle, *Fortune*, 24 Jan 2025 (https://fortune.com/2025/01/24/for-startups-remote-work-versus-return-to-office-is-a-balance-and-an-experiment/): "Vercel, which currently has 550 employees and is valued at $3.25 billion,"
- M. Temkin, "Vercel CEO … signals IPO readiness as AI agents fuel revenue surge", *TechCrunch*, 13 Apr 2026 (https://techcrunch.com/2026/04/13/vercel-ceo-guillermo-rauch-signals-ipo-readiness-as-ai-agents-fuel-revenue-surge/): ARR grew from "$100 million" at the start of 2024 to "a run rate of $340 million by the end of February 2026". The article credits the $340M figure to Forbes, which we did not open.
- Aggregators (Sacra, Latka) put ARR at ~$200M in mid-2025 and headcount at 875–893 in late 2025. These are not primary.

```bibtex
@misc{vercel2025seriesf,
  author       = {{Vercel}},
  title        = {Towards the {AI} Cloud: Our Series {F}},
  howpublished = {Company blog},
  year         = {2025},
  month        = sep,
  day          = {30},
  url          = {https://vercel.com/blog/series-f},
  urldate      = {2026-11-07}
}
@misc{garfinkle2025vercel,
  author       = {Garfinkle, Allie},
  title        = {For Startups, Remote Work versus Return-to-Office Is a Balance---and an Experiment},
  howpublished = {Fortune},
  year         = {2025},
  month        = jan,
  day          = {24},
  url          = {https://fortune.com/2025/01/24/for-startups-remote-work-versus-return-to-office-is-a-balance-and-an-experiment/},
  urldate      = {2026-11-07}
}
@misc{temkin2026vercel,
  author       = {Temkin, Marina},
  title        = {Vercel {CEO} Signals {IPO} Readiness as {AI} Agents Fuel Revenue Surge},
  howpublished = {TechCrunch},
  year         = {2026},
  month        = apr,
  day          = {13},
  url          = {https://techcrunch.com/2026/04/13/vercel-ceo-guillermo-rauch-signals-ipo-readiness-as-ai-agents-fuel-revenue-surge/},
  urldate      = {2026-11-07}
}
```

---

## Item 3. Acquisitions

| Claim as stated in paper | Status | Note |
|---|---|---|
| SpaceX acquired Cursor for $60B in August 2026 | VERIFIED | Agreement 16 Jun 2026; closed 14 Aug 2026; "implied equity value of Cursor of $60.0 billion", paid in SpaceX Class A shares |
| SpaceX absorbed xAI ($250B) in February 2026 | VERIFIED | Announced 2 Feb 2026. The $250B valuation is from Reuters' "person familiar with the matter", not a filing. |
| Microsoft absorbed Inflection's staff, March 2024 | VERIFIED, soften wording | Microsoft (19 Mar 2024): two co-founders plus "several members of the Inflection team" joined. The company says "several", not "all". |
| Google licensed Character.ai and rehired its founders (2024) | VERIFIED | 2 Aug 2024: a non-exclusive licence, and both co-founders moved to Google |

**SpaceX–Cursor.**
- SpaceX 8-K, 16 Jun 2026 (https://www.sec.gov/Archives/edgar/data/1181412/000162828026043411/spaceexplorationtechnologi.htm): "On June 16, 2026, Space Exploration Technologies Corp. (the "Company"), X67 Inc., a wholly owned subsidiary of the Company"; consideration "based on an implied equity value of Cursor of $60.0 billion".
- SpaceX 8-K, 14 Aug 2026 (https://www.sec.gov/Archives/edgar/data/1181412/000162828026056945/spcx-20260814.htm): "on August 14, 2026 (the "Effective Time"), the Merger became effective"; holders receive "an aggregate of 389,289,254 shares of the Company's Class A common stock".
- Press: A. Capoot, "SpaceX to acquire the AI coding startup Cursor for \$60 billion", *CNBC*, 16 Jun 2026 (https://www.cnbc.com/2026/06/16/spacex-spcx-cursor-acquisition-ipo.html): "for $60 billion worth of stock".

**SpaceX–xAI.** E. Wang and J. Roulette, "SpaceX acquires xAI in record-setting deal as … looks to unify AI and space ambitions", *Reuters*, 2 Feb 2026, read via the KSL.com syndication (https://www.ksl.com/article/51442147/spacex-acquires-xai-in-record-setting-deal-as-musk-looks-to-unify-ai-and-space-ambitions): "The transaction values SpaceX at $1 trillion, and xAI at $250 billion, according to a person familiar with the matter." Bloomberg and Fortune (2 Feb 2026) report a combined value of $1.25T. An EDGAR full-text search for "xAI" "$250 billion" in SpaceX filings returned no hits.

**Microsoft–Inflection.** Microsoft Corporate Blogs, "...DeepMind and Inflection Co-founder, joins Microsoft to lead Copilot", 19 Mar 2024 (https://blogs.microsoft.com/blog/2024/03/19/mustafa-suleyman-deepmind-and-inflection-co-founder-joins-microsoft-to-lead-copilot/): "Several members of the Inflection team have chosen to join [the co-founders] at Microsoft." The ~$650M licensing payment in the data file was not checked against a primary source this pass.

**Google–Character.ai.** I. Mehta, "Character.AI CEO … returns to Google", *TechCrunch*, 2 Aug 2024 (https://techcrunch.com/2024/08/02/character-ai-ceo-noam-shazeer-returns-to-google/): "Google is also signing a non-exclusive agreement with Character.AI to use its tech." Both co-founders and several employees moved to Google. Character.AI's own blog post URL (blog.character.ai/our-next-phase-of-growth/) returned 404. The ~$2.5–2.7B price comes from press (The Information) and was not verified.

```bibtex
@misc{spacex2026cursoragreement,
  author       = {{Space Exploration Technologies Corp.}},
  title        = {Form 8-K: Entry into a Material Definitive Agreement (Anysphere, Inc.)},
  howpublished = {U.S. Securities and Exchange Commission, EDGAR},
  year         = {2026},
  month        = jun,
  day          = {16},
  url          = {https://www.sec.gov/Archives/edgar/data/1181412/000162828026043411/spaceexplorationtechnologi.htm},
  urldate      = {2026-11-07}
}
@misc{spacex2026cursorclose,
  author       = {{Space Exploration Technologies Corp.}},
  title        = {Form 8-K: Completion of Acquisition of Anysphere, Inc.},
  howpublished = {U.S. Securities and Exchange Commission, EDGAR},
  year         = {2026},
  month        = aug,
  day          = {14},
  url          = {https://www.sec.gov/Archives/edgar/data/1181412/000162828026056945/spcx-20260814.htm},
  urldate      = {2026-11-07}
}
@misc{capoot2026spacexcursor,
  author       = {Capoot, Ashley},
  title        = {{SpaceX} to Acquire the {AI} Coding Startup {Cursor} for \$60 Billion},
  howpublished = {CNBC},
  year         = {2026},
  month        = jun,
  day          = {16},
  url          = {https://www.cnbc.com/2026/06/16/spacex-spcx-cursor-acquisition-ipo.html},
  urldate      = {2026-11-07}
}
@misc{wang2026spacexxai,
  author       = {Wang, Echo and Roulette, Joey},
  title        = {{SpaceX} Acquires {xAI} in Record-Setting Deal},
  howpublished = {Reuters (via KSL.com)},
  year         = {2026},
  month        = feb,
  day          = {2},
  url          = {https://www.ksl.com/article/51442147/spacex-acquires-xai-in-record-setting-deal-as-musk-looks-to-unify-ai-and-space-ambitions},
  urldate      = {2026-11-07}
}
@misc{microsoft2024inflection,
  author       = {{Microsoft}},
  title        = {{DeepMind} and {Inflection} Co-founder Joins {Microsoft} to Lead {Copilot}},
  howpublished = {Official Microsoft Blog},
  year         = {2024},
  month        = mar,
  day          = {19},
  url          = {https://blogs.microsoft.com/blog/2024/03/19/mustafa-suleyman-deepmind-and-inflection-co-founder-joins-microsoft-to-lead-copilot/},
  urldate      = {2026-11-07}
}
@misc{mehta2024characterai,
  author       = {Mehta, Ivan},
  title        = {{Character.AI} {CEO} Returns to {Google}},
  howpublished = {TechCrunch},
  year         = {2024},
  month        = aug,
  day          = {2},
  url          = {https://techcrunch.com/2024/08/02/character-ai-ceo-noam-shazeer-returns-to-google/},
  urldate      = {2026-11-07}
}
```

---

## Item 4. Cloud-era rows of Table `tab:ai-vs-cloud`

### 4a. Snowflake (2020 IPO)

| Table cell | Status | Filing / announcement says |
|---|---|---|
| Valuation $70B | VERIFIED, but define it | $70B was the **market value after the first day of trading** (Bloomberg). At the IPO price the valuation was **$33.3B** (CNBC). |
| Revenue $0.6B | VERIFIED | FY2021 (year ended 31 Jan 2021): **$592.0M** |
| Employees 3,500 | **CORRECTED** | **2,495** at 31 Jan 2021 |
| Rev./Emp. $0.17M | **CORRECTED** (inference) | $592.0M / 2,495 ≈ **$0.24M** |

- Snowflake Inc., Form 10-K for FY ended 31 Jan 2021, filed 2021-03-31 (https://www.sec.gov/Archives/edgar/data/1640147/000164014721000073/snow-20210131.htm): "As of January 31, 2021, we had 2,495 employees operating across 19 countries."; "our revenue was $592.0 million, $264.7 million, and $96.7 million, respectively" (FY2021, FY2020, FY2019).
- A. Levy and L. Picker, *CNBC*, 15 Sep 2020 (https://www.cnbc.com/2020/09/15/snowflake-prices-ipo-above-increased-range-implying-initi.html): Snowflake "priced its IPO above its increased range in an offering that values the company at $33.3 billion."
- *Bloomberg*, "Snowflake Soars Into Tech Big Leagues With \$70 Billion Value", 16 Sep 2020 (https://www.bloomberg.com/news/articles/2020-09-16/snowflake-soars-130-in-3-36-billion-record-software-ipo-debut). Not opened directly; the *Boston Globe* reprint with a Bloomberg byline (https://www.bostonglobe.com/2020/09/16/business/snowflake-soars-130-336-billion-record-software-ipo-debut/) says market value was "more than $70 billion".

### 4b. Databricks (2021)

| Table cell | Status | Announcements say |
|---|---|---|
| Valuation $38B | VERIFIED | Series H, 31 Aug 2021, "$38 billion post-money valuation" |
| Revenue $1.6B | **CORRECTED** | $1.6B was the **size of the Series H round**. Revenue: **>$600M ARR** (Aug 2021) and **>$800M ARR** (end of 2021). |
| Employees 5,000 | **NOT FOUND** | No 2021 primary headcount found. Latest company figure: **"nearly 1,500"** (Sep 2020). **Inference:** "5,000" probably comes from the press release's "More than 5,000 … organizations" customer count. |
| Rev./Emp. $0.32M | Cannot be reproduced | $1.6B / 5,000 = $0.32M, and both inputs are wrong. No same-date pair exists from primary sources. |

- Databricks press release, "Databricks Raises \$1.6 Billion Series H Investment at \$38 Billion Valuation", 31 Aug 2021 (https://www.databricks.com/company/newsroom/press-releases/databricks-raises-1-6-billion-series-h-investment-at-38-billion-valuation): "The Series H funding, led by Counterpoint Global (Morgan Stanley), puts Databricks at a $38 billion post-money valuation." The release gives no revenue or headcount.
- A. Wilhelm and R. Miller, *TechCrunch*, 31 Aug 2021 (https://techcrunch.com/2021/08/31/databricks-raises-1-6b-at-38b-valuation-as-it-blasts-past-600m-arr/): "Databricks has reached the $600 million annual recurring revenue (ARR) milestone".
- A. Wilhelm, *TechCrunch*, 5 Aug 2022 (https://techcrunch.com/2022/08/05/squaring-databricks-2021-valuation-as-it-crosses-a-1b-annual-run-rate/): "By the end of 2021, Databricks said that it crossed $800 million in ARR."
- Databricks blog, "It's a Good Time to be a Brickster!", 23 Sep 2020 (https://www.databricks.com/blog/2020/09/23/its-a-good-time-to-be-a-brickster.html): "Databricks now has nearly 1,500 employees worldwide".
- Searches tried for a 2021 headcount: Databricks newsroom (Series G Feb 2021, Series H Aug 2021), Forbes Cloud 100 2021, Databricks blog milestones. None gave one. An aggregator reports ~3,300 for Dec 2022 (not primary).

**Inference for the text (07-discussion.tex line 42):** the "$0.17–0.32M" range for cloud comparators is not supported. Snowflake's filing gives $0.24M. Databricks cannot be computed from primary sources. With $800M ARR and an unverified headcount of roughly 2,000–3,000, it would be about $0.3–0.4M, but that is speculative and should not be used.

```bibtex
@misc{snowflake2021tenk,
  author       = {{Snowflake Inc.}},
  title        = {Form 10-K: Annual Report for the Fiscal Year Ended January 31, 2021},
  howpublished = {U.S. Securities and Exchange Commission, EDGAR},
  year         = {2021},
  month        = mar,
  url          = {https://www.sec.gov/Archives/edgar/data/1640147/000164014721000073/snow-20210131.htm},
  urldate      = {2026-11-07}
}
@misc{levy2020snowflake,
  author       = {Levy, Ari and Picker, Leslie},
  title        = {Snowflake Prices {IPO} above Increased Range, Implying Initial Market Cap of \$33.3 Billion},
  howpublished = {CNBC},
  year         = {2020},
  month        = sep,
  day          = {15},
  url          = {https://www.cnbc.com/2020/09/15/snowflake-prices-ipo-above-increased-range-implying-initi.html},
  urldate      = {2026-11-07}
}
@misc{bloomberg2020snowflake,
  author       = {{Bloomberg News}},
  title        = {Snowflake Soars into Tech Big Leagues with \$70 Billion Value},
  howpublished = {Bloomberg},
  year         = {2020},
  month        = sep,
  day          = {16},
  url          = {https://www.bloomberg.com/news/articles/2020-09-16/snowflake-soars-130-in-3-36-billion-record-software-ipo-debut},
  urldate      = {2026-11-07}
}
@misc{databricks2021seriesh,
  author       = {{Databricks}},
  title        = {Databricks Raises \$1.6 Billion Series {H} Investment at \$38 Billion Valuation},
  howpublished = {Press release},
  year         = {2021},
  month        = aug,
  day          = {31},
  url          = {https://www.databricks.com/company/newsroom/press-releases/databricks-raises-1-6-billion-series-h-investment-at-38-billion-valuation},
  urldate      = {2026-11-07}
}
@misc{wilhelm2021databricks,
  author       = {Wilhelm, Alex and Miller, Ron},
  title        = {Databricks Raises \$1.6B at \$38B Valuation as It Blasts Past \$600M {ARR}},
  howpublished = {TechCrunch},
  year         = {2021},
  month        = aug,
  day          = {31},
  url          = {https://techcrunch.com/2021/08/31/databricks-raises-1-6b-at-38b-valuation-as-it-blasts-past-600m-arr/},
  urldate      = {2026-11-07}
}
@misc{wilhelm2022databricks,
  author       = {Wilhelm, Alex},
  title        = {Squaring {Databricks}' 2021 Valuation as It Crosses a \$1B Annual Run Rate},
  howpublished = {TechCrunch},
  year         = {2022},
  month        = aug,
  day          = {5},
  url          = {https://techcrunch.com/2022/08/05/squaring-databricks-2021-valuation-as-it-crosses-a-1b-annual-run-rate/},
  urldate      = {2026-11-07}
}
@misc{databricks2020brickster,
  author       = {Reichanadter, Amy},
  title        = {It's a Good Time to Be a Brickster!},
  howpublished = {Databricks blog},
  year         = {2020},
  month        = sep,
  day          = {23},
  url          = {https://www.databricks.com/blog/2020/09/23/its-a-good-time-to-be-a-brickster.html},
  urldate      = {2026-11-07}
}
```

---

## Item 5. Kim & Koning (2026) URL; Bonney et al. (2026) denominator and the 4.7% figure

### 5a. Kim & Koning (2026), "AI-Native Firms": FOUND

- HBS faculty page: https://www.hbs.edu/faculty/Pages/item.aspx?num=69077. Found by search; a direct fetch returned HTTP 403.
- PDF: https://www.hbs.edu/ris/download.aspx?name=26-090.pdf (also returned 403 to our fetcher).
- SSRN: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6905079, linked from Marginal Revolution on 18 Jun 2026.
- HBS AI Institute post, 23 Jun 2026 (https://aiinstitute.hbs.edu/less-headcount-more-valuation-how-ai-native-firms-change-the-game/), which we opened, gives the citation as: "Kim, Hyunjin, and Rembrand Koning, 'AI-Native Firms,' Harvard Business School Working Paper, No. 26-090 (June 2026)", and links the faculty page above.

```bibtex
@techreport{kim2026ainative,
  author      = {Kim, Hyunjin and Koning, Rembrand},
  title       = {{AI}-Native Firms},
  institution = {Harvard Business School},
  type        = {Working Paper},
  number      = {26-090},
  year        = {2026},
  month       = jun,
  url         = {https://www.hbs.edu/faculty/Pages/item.aspx?num=69077},
  urldate     = {2026-11-07}
}
```

### 5b. Bonney et al. (2026), NBER w35141: the "2%" is a share of **AI-using firms**

We opened the full PDF (https://www.nber.org/system/files/working_papers/w35141/w35141.pdf, "April 2026").
- Table 4 title: "**Share of AI-using firms** by AI-driven employment change (last six months)". Firm-weighted: Increased 2.3%, **Decreased 2.0%**, No Change 95.7%. Employment-weighted: Increased 3.7%, Decreased 2.4%, No Change 93.9%.
- Introduction: "AI-driven employment change instances remain modest, with only about 5% of AI-using firms reporting any headcount impact – distributed nearly equally between increases (2.3% firm-weighted and 3.7% employment-weighted) and decreases (2.0% firm-weighted and 2.4% employment-weighted)."
- The abstract is ambiguous on its own: "Most firms (66%) use AI for task augmentation, while employment reductions are rare (2%)." The body and Table 4 show the base is AI-using firms.
- Section 5.2: "an overwhelming fraction of AI-users (95%, firm-weighted) do not experience any change in employment. The ones that experience an increase or decrease each constitute a small fraction of firms (about 2% each)".

**Paper consequences:**
- 08-conclusion.tex line 20 and 05-simulation.tex line 219 say "about 2% of firms". This should read "about 2% of AI-using firms". Since only ~18% of all firms use AI, the share of all firms would be far smaller (inference).
- 02-theory.tex line 69 says "AI-adopting **establishments**". The paper's unit is **firms**.

### 5c. Coordinator check: the "4.7% increased headcount" (02-theory.tex line 69)

**NOT FOUND in Bonney et al.** The paper reports AI-driven employment **increases at 2.3% of AI-using firms (firm-weighted) and 3.7% (employment-weighted)** (Table 4 and the introduction, quoted above). A search of the full PDF text for "4.7" finds only "44.7%" in two unrelated adoption-rate cells (an appendix size-class table and the "Firm or worker task (AI)" employment-weighted rate). No 4.7% figure appears.

**Inference:** 4.7% matches the Census BFS figure in our own notes: high-propensity business applications **+4.7%** Jan–Sep 2026 vs Jan–Sep 2025 (`data/ai_era_startups_2023_2026.md`, §3.1 table and headline finding 6). This looks like a mix-up. Suggested replacement: "...only 2.0\% of AI-using firms reduced employment because of AI, while 2.3\% increased it (2.4\% and 3.7\% employment-weighted)".

**Bibliography error.** The existing `bonney2026` entry in `paper/references.bib` has the wrong authors and title. The NBER page (https://www.nber.org/papers/w35141) and the PDF title page list: Kathryn Bonney, Cory L. Breaux, Emin Dinlersoz, Lucia S. Foster, John C. Haltiwanger, and Aditya A. Pande, "The Microstructure of AI Diffusion: Evidence from Firms, Business Functions, and Worker Tasks", NBER WP 35141, April 2026, DOI 10.3386/w35141. A parallel Census release exists as CES-WP-26-25 (https://www.census.gov/library/working-papers/2026/adrm/CES-WP-26-25.html; not opened).

```bibtex
@techreport{bonney2026,
  author      = {Bonney, Kathryn and Breaux, Cory L. and Dinlersoz, Emin and Foster, Lucia S. and Haltiwanger, John C. and Pande, Aditya A.},
  title       = {The Microstructure of {AI} Diffusion: Evidence from Firms, Business Functions, and Worker Tasks},
  institution = {National Bureau of Economic Research},
  type        = {NBER Working Paper},
  number      = {35141},
  year        = {2026},
  month       = apr,
  doi         = {10.3386/w35141},
  url         = {https://www.nber.org/papers/w35141},
  urldate     = {2026-11-07},
  note        = {Data: 2026 AI supplement to the Census Business Trends and Outlook Survey, November 2025--January 2026}
}
```

---

## Item 6. Breadth of generative-AI exposure vs cloud computing or earlier IT

**Cloud computing: NOT FOUND.** We found no published source that compares the occupational or industry breadth of generative-AI exposure with that of cloud computing. Searches covered occupational and industry exposure studies, cloud-adoption studies, and NBER/arXiv/Brookings/ILO material. The nearest cloud-vs-AI paper (Lu, Phillips and Yang, NBER w32811) compares effects on industry concentration in China, not breadth of exposure. We did not open it.

**Earlier IT (personal computers): FOUND, but it measures adoption, not exposure.** Bick, Blandin and Deming compare the spread of generative-AI adoption across occupations and industries with early PC adoption in the CPS. We opened the PDF (NBER w32966, Sep 2024, revised Feb 2025):
- "We also find similar adoption patterns by occupation and industry, although computer adoption was somewhat more concentrated in a few occupations whereas genAI adoption is more evenly dispersed."
- Abstract: "Generative AI and PCs have very similar early adoption patterns by education, occupation, and other characteristics."

**Supporting, not a breadth comparison.** Eloundou et al. (the paper's `eloundou2024gpts`; arXiv v5 opened) regress LLM exposure on earlier technology-exposure measures, including Webb's (2020) software and robot exposure. They report: "The variance explained by these earlier efforts … along with wage controls, ranges from 60 to 72%, indicating that 28 to 40% of the variation in our AI exposure measure remains unaccounted for by previous technology exposure measurements." This shows overlap with earlier IT exposure. It does not show that LLM exposure is broader.

**Implication for the text (07-discussion.tex lines 114–116, inference).** The claim that "the effects of cloud computing were concentrated in sectors that relied heavily on computing" has no direct published support we could find. A defensible rewording: "Compared with the personal computer, early generative-AI adoption is more evenly dispersed across occupations \citep{bick2025rapid}; we know of no comparable measure for cloud computing." Alternatively, the cloud half of the sentence could be dropped.

```bibtex
@techreport{bick2025rapid,
  author      = {Bick, Alexander and Blandin, Adam and Deming, David J.},
  title       = {The Rapid Adoption of Generative {AI}},
  institution = {National Bureau of Economic Research},
  type        = {NBER Working Paper},
  number      = {32966},
  year        = {2024},
  note        = {Revised February 2025},
  url         = {https://www.nber.org/papers/w32966},
  urldate     = {2026-11-07}
}
```

---

## Not opened or blocked (for the record)

- Blocked to our fetcher: Bloomberg (Cursor $3B ARR; Snowflake $70B), Reuters (Vercel), nytimes.com (Lovable ~120), businessinsider.com (Cursor ~800, Lovable 146), the HBS faculty page and PDF, SSRN, techspot.com.
- Not attempted: Forbes articles on Cursor (>$4B ARR, 8 Jun 2026) and Vercel ($340M); Character.AI's blog post (old URL returned 404).
