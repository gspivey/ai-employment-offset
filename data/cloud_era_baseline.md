# Cloud-Era Empirical Baseline (2006–2020)

Research notes for the economics paper (T4). The question: when cloud infrastructure (AWS 2006, Google 2008, Azure 2010) and the SaaS stack cut the fixed cost of starting a firm, what happened to firm formation and to the firm-size distribution of employment? The answers give an empirical prior for the AI-era argument.

Compiled 2026-10-29. Full source list with URLs/DOIs: `data/sources.md`.

**Provenance tags used below**

| Tag | Meaning |
|---|---|
| **[C]** | Computed by us from the official public files listed in `sources.md` (Census BDS 2023 release, Census BFS monthly, Census NES, Eurostat API). Reproducible from those files. |
| **[P]** | Paper finding, as stated in the published abstract/summary (bibliographic data verified). |
| **[V]** | Bibliographic details verified this pass; finding summarised from secondary description. Read the paper before quoting. |
| **[U]** | Not re-verified this pass (cited from domain knowledge). Check before citing. |

---

## 0. Headline findings

1. **US employment did NOT shift toward small firms during the cloud era. It shifted toward large firms, and the shift sped up.** [C] Firms with fewer than 500 employees held 50.9% of private employment in 2006 and 47.0% in 2019 (46.2% in 2023). Firms with 10,000+ employees went from 26.3% to 29.2%. From 2006 to 2019, about **90% of the net rise in employment (+12.6M) showed up in firms of 500+ employees**. The small-firm share fell about 0.30 pp/yr in 2006–2019, against about 0.19 pp/yr in 1990–2006.
2. **The employer startup rate fell and only partly recovered.** [C] The startup rate (age-0 firms / all firms) was 10.3% in 2006, bottomed at 7.6% in 2010, and reached only 8.5% by 2019. It passed 9% only after COVID (9.4% in 2022). Employer startups fell from 541k in 2006 to 453k in 2019 (−16%).
3. **Business formation grew on the nonemployer margin.** [C] Business applications (EIN filings) rose 34% from 2006 to 2019, and nonemployer businesses rose 30.5% (20.8M → 27.1M). Over the same period, high-propensity applications fell 15%, applications with planned wages fell 48%, and actual employer formations within 8 quarters fell 21%. Only 10.2% of 2019 applications became employers within 8 quarters, against 17.3% in 2006.
4. **The sector most exposed to cloud rebounded. The rest did not.** [C] The startup rate in Information (NAICS 51) went from 8.5% in 2010 to 11.3% in 2019, above its 2006 level of 10.6%. Professional services, retail and manufacturing stayed below their 2006 levels.
5. **The micro evidence finds real cloud effects. The macro trend went the other way.** [P] AWS cut the capital a new venture needs, which led VCs to make smaller, more numerous bets (Ewens, Nanda & Rhodes-Kropf 2018). Cloud adoption helps *young* firms grow (DeStefano, Kneller & Timmis 2023; Jin & McElheran WP). Even so, aggregate dynamism kept falling (Decker et al. 2014, 2016, 2020; Akcigit & Ates 2021). Slower labour-force growth explains about half of the long-run startup decline (Karahan, Pugsley & Şahin 2024). Proprietary IT at scale favoured incumbents (Bessen 2020).
6. **In Europe, the SME employment share also fell, but data breaks make the size unclear.** [C] In the EU-27 non-financial business economy, SMEs (<250 persons employed) held 69.2% of employment in 2011 and 64.4% in 2019. Most of the drop falls in 2017–2018, which matches statistical-unit changes in large member states (see §6). In the cleaner 2011–2016 window the large-firm share rose only 0.5 pp. Enterprise birth rates vary widely across countries and are driven by policy, with no common surge.

**Implication for the paper:** Cheaper fixed costs alone did not rebalance the economy toward small employers between 2006 and 2020. What they did was (a) increase experimentation and solo/nonemployer formation, (b) improve outcomes for young firms that adopted, and (c) coexist with stronger forces that favoured scale. An AI-era argument for small-firm rebalancing has to explain why AI differs on (c). The cloud parallel alone does not support it.

---

## 1. Timeline: cloud infrastructure and the startup "stack"

### 1.1 Core infrastructure (dates verified)

| Date | Event | Barrier lowered | Tag |
|---|---|---|---|
| 2006-03-14 | **Amazon S3** launches. This is the public start of AWS. | Storage capex → metered opex | [V] |
| 2006-08-25 | **Amazon EC2** limited beta, open to existing AWS customers only | Server capex → per-hour compute | [V] |
| 2008-04-07/08 | **Google App Engine** preview (first 10,000 developers) | Managed PaaS: no ops staff for web apps | [V] |
| 2010-02-01 | **Windows Azure** general availability in 21 countries (billing from Feb 2) | Enterprise/.NET workloads to cloud | [V] |
| 2012-06 | Google Compute Engine preview (Google I/O) | IaaS competition | [V] |
| 2013-12-02 | **Google Compute Engine** GA: 99.95% SLA, 10% price cut on standard instances, 60% cut on Persistent Disk | Price competition among the three hyperscalers | [V] |

### 1.2 Complementary layers (commonly cited dates, not re-verified) [U]

| Approx. date | Layer | Barrier lowered |
|---|---|---|
| 2005 | Y Combinator (first batch) | Seed capital + mentorship at small ticket size |
| 2006 | Shopify; Google Apps for Your Domain | E-commerce storefront; office/email SaaS |
| 2007 | Heroku | Deploy without sysadmin |
| 2008 | GitHub; Twilio; iPhone App Store (Jul); EC2 leaves beta with SLA (Oct) | Code collaboration; telephony API; global distribution |
| 2011 | Stripe public launch | Payments via API |
| 2013–2014 | Docker; Kubernetes; Slack; AWS Lambda (Nov 2014) | Portability; serverless pay-per-invocation |

### 1.3 Mechanisms by which cloud lowered barriers

1. **Fixed → variable cost conversion.** Servers, storage and data-centre space became metered services. This is the channel Ewens, Nanda & Rhodes-Kropf (2018) identify. After AWS, startups in the sectors that benefited most raised much less in their first VC round: about **20% less on average**, with larger falls in parts of the distribution. [P]
2. **Cheaper experimentation (real-option value).** Elastic capacity makes failure cheaper and reveals information sooner. VCs responded with "spray and pray": small amounts of funding and light governance spread across more startups, which they abandon more readily. Innovation shifted toward ideas whose prospects show up quickly and cheaply. [P] Experimentation tools that run on this stack, such as A/B testing, improve performance at the startups that adopt them by 30–100% after a year (Koning, Hasan & Chatterji 2022). [P]
3. **Renting IT instead of owning it.** Young US manufacturing plants that rented IT, especially through cloud, survived and grew more, while plants that invested in traditional IT capital were *more* likely to fail. The effect is stronger in IT-intensive and high-variance industries and works through **age more than size** (Jin & McElheran, Census microdata 2006–2014; working paper). [V]
4. **Fewer specialist hires.** Managed services (PaaS, managed databases, serverless) replace sysadmin, DBA and ops staff. This is the main reason cloud-era firms can be "employment-light", which matters for any headcount-based size measure.
5. **Distribution and payments as APIs.** App stores, marketplaces and payment APIs cut go-to-market fixed costs. Nonemployer e-commerce (NAICS 4541) rose from 77k (2006) to 188k (2019), +144%. [C]
6. **Financing adaptation.** Accelerators and smaller seed rounds, plus new intermediaries entering finance (Ewens et al. 2018). [P]

**Counter-mechanism: the same technology raised returns to scale.** Proprietary IT systems account for most of the rise in industry concentration, with the top-4 firms gaining the most. Proprietary software investment is about $250B/yr (Bessen 2020). [V] Cloud adoption also changes how incumbents are organised: they close establishments and open fewer, without gaining scale (DeStefano et al. 2023). [V]

---

## 2. US firm formation, 2005–2023

### 2.1 Employer startups and dynamism (Census BDS, 2023 release) [C]

Definitions:
- Startup rate = firms of age 0 ÷ all firms.
- Startup emp share = employment at age-0 firms ÷ total employment.
- Young = firm age 0–5.
- Reallocation = job creation rate + job destruction rate − |net|.
- BDS year *t* covers the March (*t*−1) → March (*t*) flow window; employment counts the pay period including March 12.

| Year | Employer firms | Startup rate % | # startups | Startup emp share % | Young (0–5) share of firms % | Young share of employment % | Young share of gross job creation % | Job reallocation rate % |
|---|---|---|---|---|---|---|---|---|
| 1980 | 3,739,767 | 11.76 | 439,667 | 2.97 | n/a (censored) | n/a | n/a | 30.4 |
| 1990 | 4,445,528 | 11.09 | 493,080 | 3.08 | 44.2 | 18.0 | 38.2 | 28.8 |
| 2000 | 4,902,719 | 9.10 | 446,204 | 2.25 | 38.7 | 14.1 | 30.5 | 27.2 |
| 2005 | 5,166,062 | 10.04 | 518,727 | 2.55 | 37.5 | 13.2 | 32.2 | 27.5 |
| **2006** | 5,254,916 | **10.30** | **541,317** | 2.47 | 38.3 | **13.4** | 30.9 | 25.6 |
| 2007 | 5,291,526 | 9.63 | 509,517 | 2.25 | 38.4 | 13.0 | 28.8 | 29.8 |
| 2008 | 5,230,315 | 9.01 | 471,285 | 2.11 | 37.6 | 12.3 | 28.6 | 28.3 |
| 2009 | 5,088,072 | 7.77 | 395,235 | 1.93 | 36.1 | 11.6 | 30.5 | 22.9 |
| **2010** | 5,016,353 | **7.56** | **379,145** | 2.02 | 34.6 | 11.3 | 30.7 | 23.8 |
| 2012 | 5,039,673 | 8.11 | 408,546 | 1.95 | 33.0 | 10.8 | 27.6 | 23.3 |
| 2014 | 5,100,719 | 8.08 | 411,948 | 1.90 | 32.2 | 10.6 | 27.9 | 21.9 |
| 2016 | 5,212,130 | 8.49 | 442,414 | 1.85 | 33.3 | 10.6 | 28.0 | 21.8 |
| 2018 | 5,281,916 | 8.37 | 442,078 | 1.88 | 33.9 | 10.5 | 28.1 | 22.3 |
| **2019** | 5,330,349 | **8.50** | **453,027** | 1.86 | 34.3 | **10.6** | 29.3 | 20.7 |
| 2020 | 5,335,214 | 8.54 | 455,725 | 1.81 | 34.6 | 10.5 | 28.7 | 22.7 |
| 2021 | 5,391,471 | 9.00 | 485,256 | 1.75 | 35.4 | 10.5 | 29.5 | 23.2 |
| 2022 | 5,541,603 | 9.41 | 521,312 | 1.86 | 36.0 | 10.9 | 25.8 | 22.3 |
| 2023 | 5,593,727 | 9.10 | 508,777 | 1.78 | 36.2 | 10.7 | 26.5 | 22.1 |

How to read this:
- **2006 → 2019:** the startup rate fell from 10.3% to 8.5% (−1.8 pp, −17%). Startup employment fell from 2.95M to 2.45M jobs (−17%). The young-firm employment share fell from 13.4% to 10.6% (−2.8 pp, −21% relative).
- The 2006 → 2010 collapse coincides with the Great Recession. After 2010 the recovery is slow: about +0.1 pp/yr.
- Young firms' share of *gross* job creation held at 28–31% throughout, even as their employment share fell. Conditional on entering, young firms remained the most job-creating group.
- Reallocation averaged 27.6% in 2005–07 and 22.3% in 2017–19. The 2006 and 2007 values are noisy, so use 3-year averages.

### 2.2 Business applications vs. employer formation (Census BFS, annual sums of unadjusted monthly data) [C]

| Year | Business applications (BA) | High-propensity (HBA) | With planned wages (WBA) | Employer formations within 8 qtrs (BF8Q) | BF8Q ÷ BA |
|---|---|---|---|---|---|
| 2005 | 2,485,100 | 1,471,866 | 881,865 | 483,686 | 19.5% |
| **2006** | 2,615,834 | 1,542,329 | 921,405 | 453,468 | **17.3%** |
| 2008 | 2,559,006 | 1,264,549 | 621,488 | 347,968 | 13.6% |
| 2010 | 2,473,934 | 1,151,984 | 533,549 | 323,129 | 13.1% |
| 2014 | 2,691,040 | 1,178,484 | 476,228 | 344,835 | 12.8% |
| 2016 | 2,948,338 | 1,225,243 | 481,583 | 348,854 | 11.8% |
| 2018 | 3,486,829 | 1,330,929 | 503,783 | 368,863 | 10.6% |
| **2019** | 3,498,990 | 1,316,191 | 478,640 | 357,062 | **10.2%** |
| 2020 | 4,356,498 | 1,518,956 | 524,651 | 348,058 | 8.0% |
| 2021 | 5,390,816 | 1,841,954 | 638,140 | 403,072 | 7.5% |
| 2023 | 5,469,302 | 1,848,540 | 613,708 | n/a | n/a |

Change 2006 → 2019: **BA +34%, HBA −15%, WBA −48%, BF8Q −21%.**

By sector, 2006 → 2019:
- Information (NAICS 51): BA rose from 55.9k to 73.3k (+31%), while HBA fell from 26.6k to 19.5k (−27%).
- Professional services (NAICS 54): BA rose from 328k to 457k (+39%), while HBA fell from 204k to 153k (−25%).

The surge in *intent to form* came from businesses unlikely to ever hire. The cloud era looks like an expansion of solo and side ventures, not of employer startups. BFS starts in July 2004, so there is no pre-cloud baseline before 2005.

### 2.3 Nonemployer businesses (Census Nonemployer Statistics) [C]

| | 2006 | 2019 | Change |
|---|---|---|---|
| All nonemployer establishments | 20,768,555 | 27,104,006 | +30.5% |
| Receipts ($bn, nominal) | 970.4 | 1,341.4 | +38% nominal |
| Prof., scientific & technical (54) | 2,904,083 | 3,772,571 | +29.9% |
| Information (51) | 317,695 | 363,625 | +14.5% |
| Electronic shopping & mail-order (4541) | 77,022 | 187,947 | +144% |
| Data processing & hosting (5182) | 36,570 | 46,333 | +26.7% |

Caveats:
- 2006 uses NAICS 2002 and 2019 uses NAICS 2017, so industry-level rows are approximately comparable.
- A large part of nonemployer growth is the gig/platform economy (ride-hail, delivery), which is cloud-*enabled* but is not entrepreneurship in the startup sense.
- In the 2006 → 2019 period, receipts per nonemployer were roughly flat in nominal terms ($46.7k → $49.5k) and fell in real terms.

### 2.4 Startup rate by sector: does cloud exposure matter? (BDS) [C]

| Sector | 2000 | 2006 | 2010 | 2014 | 2019 | 2022 | 2019 vs 2006 |
|---|---|---|---|---|---|---|---|
| 51 Information | 14.4 | 10.6 | 8.5 | 10.1 | **11.3** | 12.0 | **+0.7 pp** |
| 54 Prof./sci./tech. services | 10.9 | 11.1 | 8.5 | 8.9 | 9.2 | 9.9 | −1.9 pp |
| 44–45 Retail | 8.6 | 9.9 | 7.7 | 8.3 | 7.7 | 9.1 | −2.2 pp |
| 31–33 Manufacturing | 6.0 | 5.9 | 4.3 | 5.1 | 5.1 | 5.7 | −0.8 pp |

Information is the only one of these sectors that ended the cloud era above its 2006 startup rate. This fits a cloud effect concentrated where IT is the main input. NAICS 51 also includes publishing, broadcasting and telecom, and the national BDS sector tables do not split out software (5112/5132) or hosting (518). A cleaner test needs the 3/4-digit tables or LBD microdata.

---

## 3. US employment by firm size, 1980–2023 (Census BDS) [C]

BDS firm size is the **average of the firm's employment in t−1 and t** (Davis-Haltiwanger-Schuh convention, which limits regression-to-the-mean bias). Employment is year-t employees. Shares are within the size table; the table total is within 0.5% of the national total.

### 3.1 Employment share by firm size (%)

| Year | 1–4 | <20 | 20–99 | 100–499 | **<500** | 500–9,999 | **10,000+** | Firms <20 as % of firms |
|---|---|---|---|---|---|---|---|---|
| 1980 | 6.9 | 21.6 | 18.2 | 13.3 | 53.0 | 21.4 | 25.6 | 89.1 |
| 1990 | 6.6 | 21.3 | 18.5 | 14.1 | 53.9 | 22.5 | 23.6 | 88.5 |
| 2000 | 5.8 | 19.0 | 17.6 | 14.0 | 50.6 | 22.7 | 26.7 | 88.0 |
| **2006** | 5.9 | 19.1 | 17.5 | 14.4 | **50.9** | 22.8 | **26.3** | 88.3 |
| 2010 | 5.9 | 18.9 | 16.6 | 14.0 | 49.5 | 23.5 | 27.1 | 88.7 |
| 2015 | 5.5 | 17.6 | 16.5 | 14.0 | 48.1 | 23.8 | 28.1 | 88.2 |
| **2019** | 5.2 | 16.8 | 16.3 | 13.9 | **47.0** | 23.8 | **29.2** | 87.9 |
| 2020 | 5.1 | 16.6 | 16.1 | 13.9 | 46.6 | 24.0 | 29.4 | 87.8 |
| 2023 | 5.2 | 16.7 | 16.1 | 13.5 | 46.2 | 23.9 | 29.9 | 88.2 |

### 3.2 Employment levels, 2006 vs 2019

| | 2006 | 2019 | Change | % change |
|---|---|---|---|---|
| Firms <500 employees | 60.74M | 61.98M | +1.24M | +2.0% |
| Firms 500+ employees | 58.52M | 69.86M | +11.34M | +19.4% |
| Total | 119.25M | 131.83M | +12.58M | +10.5% |
| Employer firms (count) | 5.25M | 5.33M | +0.08M | +1.4% |
| Avg. employees per firm | 22.7 | 24.7 | +2.0 | +9% |

**About 90% of the 2006–2019 rise in employment sits in firms of 500+ employees.** By count, the firm distribution barely moved: about 88% of firms have fewer than 20 employees in every year. The change is in where *workers* are, not in how many small firms exist.

### 3.3 Flows vs. stocks: who created the net jobs? (net job creation summed over BDS years) [C]

| Size class | 2010–2019 net jobs | Share |
|---|---|---|
| 1–19 | +2.85M | 15.5% |
| 20–499 | +8.28M | 45.0% |
| 500+ | +7.25M | 39.4% |
| **Total** | **+18.38M** | 100% |

Over 2007–2019, which includes the recession, the 10,000+ class had *negative* cumulative net job creation (−0.57M), while every other class was positive.

Reconciling 3.2 and 3.3: firms under 500 created most of the net *flows*, yet the *stock* moved toward large firms. The gap is **migration across size thresholds**: successful young firms grow into the large classes, and acquisitions move employment into them too. This is why Haltiwanger, Jarmin & Miranda (2013) argue that **age, not size**, is the right lens: once firm age is controlled for, there is no systematic size–growth relationship. Startups and young firms drive job creation. [P]

### 3.4 Answer to Q3: "Did employment shift from large to small firms? By how much?"

**No. In stock terms it moved the other way.**

| Measure | 2006 | 2019 | Change |
|---|---|---|---|
| Large-firm (500+) employment share | 49.1% | 53.0% | +3.9 pp |
| 10,000+ employment share | 26.3% | 29.2% | +2.9 pp |
| <20 employment share | 19.1% | 16.8% | −2.3 pp |
| Young-firm (≤5 yrs) employment share | 13.4% | 10.6% | −2.8 pp |

The shift toward large firms was faster during the cloud era than over 1990–2006.

---

## 4. Europe

### 4.1 Employment share by enterprise size, non-financial business economy (Eurostat SBS `sbs_sc_sca_r2`, NACE B–N excl. K, incl. S95) [C]

Unit: **persons employed**, which includes working proprietors (the US BDS counts employees only). EU size classes: micro 0–9, small 10–49, medium 50–249, large 250+.

| Geo | Year | Micro 0–9 | Small 10–49 | Medium 50–249 | **Large 250+** | **SME <250** |
|---|---|---|---|---|---|---|
| EU-27 (2020) | 2011 | 31.3 | 20.7 | 17.3 | **30.8** | **69.2** |
| EU-27 | 2014 | 31.7 | 20.2 | 17.0 | 31.1 | 68.9 |
| EU-27 | 2016 | n/a | n/a | 17.2 | 31.3 | 68.7 |
| EU-27 | 2017 | 29.9 | 20.1 | 16.9 | 33.0 | 67.0 |
| EU-27 | 2018 | 29.1 | 19.9 | 15.9 | 35.1 | 64.9 |
| EU-27 | **2019** | 28.5 | 20.0 | 16.0 | **35.6** | **64.4** |
| EU-27 | 2020 | 29.2 | 19.3 | 15.7 | 35.7 | 64.3 |
| EU-28 | 2011 | 29.5 | 20.6 | 17.1 | 32.8 | 67.2 |
| EU-28 | 2016 | 29.5 | 20.2 | 17.0 | 33.4 | 66.6 |
| EU-28 | 2017 | 28.5 | 19.9 | 16.7 | 34.9 | 65.1 |

Large-enterprise (250+) employment share by country:

| Country | Years and share | Notes |
|---|---|---|
| DE | 37.5 (2012) → 37.1 (2015) → **41.1 (2018)** → 42.0 (2019) | |
| FR | 36.8 (2010) → 38.6 (2015) → **47.2 (2018)** → 48.7 (2019) | +8.6 pp in three years: statistical-unit break, see §6 |
| IT | 21.3 (2015) → 23.9 (2019) | |
| ES | 24.5 (2010) → 27.2 (2015) → 31.6 (2019) | |

Pre-2011 EU aggregates are not populated in this dataset, and earlier years sit under NACE Rev. 1.1. For a cross-check, Eurostat reports for 2019 that micro+small firms held 48.4% of non-financial employment and medium firms 16.0%, matching our computed 64.4% SME share. The Commission's *Annual Report on European SMEs* (DIW Econ modelled estimates) puts the EU-28 2018 SME employment share at 66.6%, using a different estimation method. [V]

How to read this: the large-firm share in the EU rose **+4.8 pp in 2011–2019**, but **only +0.5 pp in 2011–2016**, before the unit breaks. The cleanest European reading is a **modest drift toward large firms, the same direction as the US but much smaller**. The jump after 2017 should not be used without a break adjustment.

### 4.2 Enterprise birth rates: births ÷ active enterprises, industry + construction + services excl. holding companies (`bd_9bd_sz_cl_r2`) [C]

| Country | 2008 | 2010 | 2012 | 2014 | 2016 | 2018 | 2019 | 2020 |
|---|---|---|---|---|---|---|---|---|
| DE | 9.3 | 8.6 | 7.8 | 7.3 | 6.7 | 8.0 | 9.4 | 7.0 |
| FR | n/a | 12.9 | 10.2 | 10.0 | 9.8 | 10.8 | 12.0 | 11.1 |
| IT | 7.1 | 6.6 | 7.1 | 7.4 | 7.9 | 7.4 | 7.6 | 6.8 |
| ES | 7.8 | 8.0 | 8.3 | 10.1 | 10.3 | 10.2 | 9.8 | 7.5 |
| NL | 13.4 | 11.7 | 10.7 | 10.4 | 9.9 | 10.1 | 10.7 | 10.3 |
| UK | 12.4 | 10.2 | 11.4 | 13.7 | 14.6 | 13.0 | n/a | n/a |

Notes:
- FR 2009 = 13.1. The French *auto-entrepreneur* regime started in 2009, which is a policy shock.
- NL 2007 = 15.5.
- UK coverage ends in 2018 (Brexit).
- In the newer `bd_size` series, the EU-27 business-economy birth rate is 10.8% (2021) → 10.4% (2024). This series is not linked to the pre-2021 one.

**Computer programming & consultancy (J62)**, the most cloud-exposed NACE division, birth rate %:

| Geo | Period | Birth rate % |
|---|---|---|
| EU-27 | 2012 → 2019 → 2020 | 12.0 → 13.6 → 12.0 |
| DE | 2008 → 2016 → 2019 | 13.0 → 9.6 → 11.7 |
| FR | 2008 → 2019 | 15.0 → 16.2 |
| IT | 2008 → 2019 | 8.5 → 10.4 |
| ES | 2008 → 2019 | 12.5 → 12.1 |
| NL | 2007 → 2019 | 20.0 → 10.8 |
| UK | 2008 → 2018 | 13.6 → 12.6 |

J62 birth rates run 2–5 pp above the business-economy average in most countries, but show no common upward trend after 2008.

**Employment share of newborn enterprises** (V97120, business economy, %):

| Country | Period | Share % |
|---|---|---|
| DE | 2008 → 2019 | 1.77 → 1.68 |
| NL | 2007 → 2019 | 2.54 → 1.34 |
| IT | 2008 → 2019 | 3.01 → 2.39 |
| FR | 2009 → 2019 | 3.13 → 3.78 |
| ES | 2008 → 2019 | 2.84 → 3.27 |
| UK | 2008 → 2018 | 2.91 → 3.59 |

Mixed. DE, NL and IT show declines, which fits the US "startup deficit" pattern. FR, ES and UK rose, plausibly because of policy (self-employment regimes, incorporation tax incentives) more than cloud.

### 4.3 Cross-country literature

- **Calvino, Criscuolo & Verlhac (2020), OECD:** business dynamism declined across 18 countries and 22 industries over two decades. The decline happens *within* sectors, not through sectoral reallocation. Market structure and firm heterogeneity are prominent drivers. Investment in intangibles and digital technologies, globalisation and demographics also contribute. [P]
- **Criscuolo, Gal & Menon (2014), OECD DynEmp, 17 OECD countries + Brazil:** among SMEs, young firms create jobs and old SMEs destroy them, extending the US age-not-size result. Young firms stayed net job creators through the crisis, though entry and post-entry growth were hit hardest. [P]

---

## 5. Key academic papers

### A. Declining US dynamism

| Paper | Finding relevant to the parallel | Tag |
|---|---|---|
| Decker, Haltiwanger, Jarmin & Miranda (2014), *JEP* 28(3):3–24 | Startup rate and employment dynamism fell over decades, with the decline speeding up after 2000. Young firms' employment share fell almost 30% over 30 years. Startups account for about 20% of gross job creation. Most startups exit within 10 years, and most survivors stay small. | [P] |
| Decker, Haltiwanger, Jarmin & Miranda (2016), *European Economic Review* 86:4–23 ("Where has all the skewness gone?") | Since 2000, high-growth young firms have declined. The 90th percentile of the growth distribution fell, driven by fewer young firms and a lower share of them reaching high growth. This hit the high-tech sector too, overlapping the cloud era. | [V] |
| Decker, Haltiwanger, Jarmin & Miranda (2020), *AER* 110(12):3952–90 | Reallocation fell *despite* rising shock dispersion, because firm employment became less responsive to productivity. The WP version finds the responsiveness decline was especially large among young high-tech firms. | [P] |
| Akcigit & Ates (2021), *AEJ: Macro* 13(1):257–98 | Ten stylised facts: falling entry, rising concentration, falling labour share, and others. A decline in knowledge diffusion from frontier to laggard firms is a leading explanation. | [P] |
| Karahan, Pugsley & Şahin (2024), *AER* 114(7):1986–2023 | Slower labour-supply growth since the late 1970s, largely set by demographics, explains about half of the startup-rate decline (published figure; WP versions said ~2/3). Incumbent survival and life-cycle growth changed little. | [P] |
| Pugsley & Şahin (2019), *RFS* 32(3):1102–47, "Grown-up Business Cycles" | The declining startup rate shifts employment toward older firms, changing cyclical dynamics. | [U] |
| Hopenhayn, Neira & Singhania (2022), *Econometrica* 90(4):1879–1914 | Falling population growth explains much of the fall in entry and the rise in firm age and concentration. | [U] |

### B. Job creation by firm size vs. age

| Paper | Finding | Tag |
|---|---|---|
| Haltiwanger, Jarmin & Miranda (2013), *REStat* 95(2):347–61 | Once firm age is controlled for, there is no systematic size–growth relationship. Startups and young firms play the outsized role in US job creation. | [P] |
| Criscuolo, Gal & Menon (2014), OECD STI Policy Paper 14 | Same result across 18 countries (see §4.3). | [P] |

### C. Cloud-specific micro evidence

| Paper | Finding | Tag |
|---|---|---|
| Ewens, Nanda & Rhodes-Kropf (2018), *JFE* 128(3):422–42 | After AWS (2006), startups in the most-benefiting sectors raised about 20% less in first-round VC. VCs moved to "spray and pray". Innovations whose prospects reveal quickly and cheaply rose disproportionately. **This is the canonical causal estimate of cloud's effect on entry cost.** | [P] |
| DeStefano, Kneller & Timmis (2023), *REStat*, online, DOI 10.1162/rest_a_01393 | UK firms, using fibre-broadband rollout as an IV for cloud adoption. Young firms grew in revenue, employment and productivity. Incumbents had no scale effect and smaller productivity gains, and restructured by closing establishments and opening fewer. | [V] |
| Jin & McElheran, "Economies before Scale" (WP, NBER SI 2018 / SSRN 2017) | US Census manufacturing plants, 2006–2014. Renting IT, especially cloud, raised survival and productivity of young plants. Owned IT capital raised failure risk. The effect works through age more than size. | [V] |
| Koning, Hasan & Chatterji (2022), *Management Science* 68(9):6434–53 | Few startups adopt A/B testing. Those that do improve performance by 30–100% after a year: more product launches, faster scaling, faster failure. | [P] |
| Zolas et al. (2020), NBER WP 28290 (2018 Annual Business Survey, 850k+ firms) | Cloud use is fairly common, while advanced technologies are rare and concentrated in larger, older firms. Size-specific cloud tables are in the full paper. | [V] |
| Bloom & Pierri (2018), *Harvard Business Review*, "Cloud Computing Is Helping Smaller, Newer Firms Compete" | Argues that cloud diffused more evenly by firm size and age than earlier IT. Descriptive magazine piece. | [U] — read before citing numbers |

### D. Counterforces favouring scale

| Paper | Finding | Tag |
|---|---|---|
| Bessen (2020), *J. Law & Economics* 63(3):531–55 | Proprietary IT systems explain most of the rise in industry concentration, with the top-4 firms gaining the most. | [V] |
| Autor, Dorn, Katz, Patterson & Van Reenen (2020), *QJE* 135(2):645–709 | Superstar firms with low labour shares drive concentration and the falling aggregate labour share. | [U] |

### E. Measurement of formation

| Paper | Finding | Tag |
|---|---|---|
| Bayard, Dinlersoz, Dunne, Haltiwanger, Miranda & Stevens (2018), NBER WP 24364 | Builds the BFS from IRS SS-4 (EIN) filings. Applications are a timely leading indicator. In 2017 high-propensity applications were still well below pre-recession levels. | [P] |
| Guzman & Stern (2020), *AEJ: Economic Policy* 12(4):212–43 | Quality-adjusted entrepreneurship (32 states, 1988–2014) is **cyclical, not in secular decline**. This is the main counterpoint to the "startup deficit" reading: the *potential* of new ventures held up, but realised scale-up fell. | [P] |

---

## 6. Limitations of the parallel

### 6.1 Identification problems in the cloud-era data

1. **The Great Recession is confounded with cloud diffusion.** EC2 (2006–08), App Engine (2008) and Azure GA (2010) launched straight into the 2007–09 collapse. Any aggregate "cloud effect" on 2006–2012 formation is swamped by the cycle. Only cross-sectional designs (Ewens et al.: exposed vs. unexposed sectors; DeStefano et al.: broadband IV) identify cloud effects.
2. **The decline predates cloud.** The US startup rate was about 12% in the late 1980s and 9.1% by 2000. Demographics explain about half of it (Karahan et al. 2024). Cloud would have had to work against a structural headwind.
3. **Treatment intensity was narrow.** Cloud cut costs mainly in IT-intensive activities. Most employer startups are in construction, food service, retail, personal and health services, where server costs were never the binding constraint. The aggregate startup rate is the wrong place to look for a cloud effect. Sector-level (§2.4) and exposure-weighted designs are the right ones.
4. **Adoption lag.** Meaningful SME cloud adoption came well after the launch dates (ABS 2018 is the first broad US measurement). The "treatment period" is closer to 2010–2020 than 2006.

### 6.2 Measurement problems

1. **Employer vs. nonemployer.** BDS counts only employer firms. Much cloud-enabled formation (solo SaaS, e-commerce, freelancing) appears only in NES and BFS (§2.2–2.3). Headcount-based size distributions **understate lean firms' economic size**.
2. **Size thresholds and units differ.** The US uses 500 employees and the EU uses 250 persons employed. The EU counts working proprietors. Cross-Atlantic levels are not comparable; directions are.
3. **Size-class migration.** Stock shares by size class mix in firms growing across thresholds and M&A (§3.3). Use age-based or initial-size (`ifsize`) tabulations for causal claims.
4. **European series breaks:**
   - NACE Rev. 1.1 → Rev. 2 in 2008.
   - EU-28 → EU-27 (Brexit) in 2020.
   - Some NSIs (notably France, and plausibly Germany) switched from legal units to profiled "enterprise" units around reference years 2017–2018. This mechanically raises the large-firm share. Check the Eurostat flags/metadata for each country-year before use.
   - The SBS/business-demography regulation changed in 2021 (EBS), so pre/post-2021 series are not linked.
5. **European birth rates are policy-driven.** Examples: the French auto-entrepreneur regime (2009) and UK incorporation incentives. Cross-country comparison of cloud effects on births is not credible without policy controls.
6. **BDS noise infusion and revisions.** BDS public tables use noise infusion and are revised between releases. Our numbers are from the **2023 release** (data years 1978–2023). Earlier-vintage figures in papers will differ slightly.

### 6.3 What plausibly transfers to the AI era

- **Fixed-to-variable cost conversion leads to more, smaller, cheaper experiments.** Expect smaller initial funding rounds, more ventures started, and a higher failure rate (Ewens et al. mechanism).
- **Formation shifts toward nonemployer/solo firms.** Strong evidence from BFS and NES. An AI parallel likely amplifies this.
- **Benefits accrue to young adopters, conditional on complementary infrastructure.** Broadband in DeStefano et al. is the analogue of compute/API access and skills.
- **Incumbents also adopt and restructure.** The same technology raises returns to proprietary data and systems (Bessen). The cloud era shows these scale forces *won* in aggregate employment shares.

### 6.4 What may NOT transfer

- **Scope of substitution.** Cloud mainly replaced IT *capital* and a narrow set of IT roles. AI targets a broad set of cognitive tasks inside every firm. The labour-substitution channel is much larger, so headcount-based size measures will misread AI-era firms even more. Revenue- or value-added-based size distributions should be preferred.
- **Who receives the cost reduction.** Cloud prices fell through hyperscaler competition (e.g., the 2013 GCE price cuts). Frontier-AI market structure, pricing power and whether model rents accrue to platforms or to users may differ.
- **Sector reach.** Cloud's cost reduction was concentrated in IT-intensive sectors (NAICS 51 was the only clear rebound). If AI lowers fixed costs in professional services, health, legal or finance, the treatment covers a much larger share of formation.
- **Macro backdrop.** The cloud era started in a deep recession with weak labour-supply growth. The AI era's starting conditions differ, so aggregate before/after comparisons are even less informative than cross-sectional exposure designs.

---

## 7. Suggested next steps for the paper

1. Pull the BDS **3-digit / 4-digit industry** tables (or apply for LBD access) to isolate software publishers (5112/5132) and hosting (518). Re-test whether startup rates rose with cloud exposure.
2. Build an **exposure-weighted** difference-in-differences: sectors with high pre-2006 IT-capital intensity vs. low. Outcomes: startup rate, young-firm employment share, and BFS HBA share.
3. Use BDS **initial firm size × firm age** tables (`bds2023_fa_ifz.csv`) to show the size-vs-age decomposition for 2006–2019 directly.
4. For Europe, rebuild 2008–2020 size shares **excluding countries with documented unit breaks**, or use OECD DynEmp/MultiProd harmonised data.
