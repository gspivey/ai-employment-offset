# Sources: Cloud-Era Baseline (2006–2020) and AI-Era Evidence (2017–2026)

Bibliography for `data/cloud_era_baseline.md` (§1–§4) and `data/ai_adoption_evidence.md` (§5–§8). Compiled 2026-10-29.

Status column:
- **used** = numbers in the baseline were computed from this file.
- **verified** = bibliographic details checked this pass.
- **unverified** = cited from domain knowledge; check before citing.

---

## 1. Official data sources

### 1.1 United States

#### Census Business Dynamics Statistics (BDS): used

The task brief calls this "BLS BDS", but **BDS is a Census Bureau product** built from the Longitudinal Business Database. BLS publishes a different series, BED (§1.1.5).

- **What it is:** the annual universe of US employer firms and establishments, 1978–2023 (current release). Gives firms, establishments, employment, entry/exit, job creation/destruction and reallocation, tabulated by firm age, firm size, sector, state and metro.
- **Landing page:** [Census BDS](https://www.census.gov/programs-surveys/bds.html)
- **Time-series CSV directory, 2023 release:** [www2.census.gov BDS tables 2023](https://www2.census.gov/programs-surveys/bds/tables/time-series/2023/)
- **Files used:**

| File | Contents |
|---|---|
| `bds2023.csv` | Economy-wide totals |
| `bds2023_fz.csv` | By firm size, 10 classes |
| `bds2023_fa.csv` | By firm age, 12 classes |
| `bds2023_sec.csv` | By NAICS sector |
| `bds2023_sec_fa.csv` | Sector × firm age |

- **Also available, recommended next:**
  - `bds2023_fa_ifz.csv`: firm age × initial firm size
  - `bds2023_fac_fzc.csv`: coarse age × coarse size
- **Codebook:** [BDS codebook/glossary (PDF)](https://www.census.gov/content/dam/Census/programs-surveys/business-dynamics-statistics/codebook-glossary.pdf). Key definitions:
  - `fsize` = average of the firm's employment in t−1 and t.
  - `ifsize` = size in t−1 (or t if the firm enters).
  - Firm age = age of the firm's oldest establishment.
  - `denom` = DHS average of employment in t and t−1.
- **Methodology:** [BDS methodology](https://www.census.gov/programs-surveys/bds/documentation/methodology.html). Employment counts the pay period including March 12; flows run March-to-March.
- **API:** `api.census.gov/data/timeseries/bds`. It **needs a free API key**; unauthenticated calls redirect to `missing_key.html`. The CSVs need no key.
- **Caveats:**
  - Employer firms only.
  - Noise infusion is applied to the public tables.
  - Each release revises history.
  - Firm age is left-censored for firms born before 1977. Age-based shares are meaningful only from about 1987.

#### Census Business Formation Statistics (BFS): used

- **What it is:** monthly counts of applications for Employer Identification Numbers (IRS Form SS-4) from July 2004, plus the share and number that become employers within 4 and 8 quarters.
- **Landing page:** [Census BFS](https://www.census.gov/econ/bfs/index.html)
- **File used:** [bfs_monthly.csv](https://www.census.gov/econ/bfs/csv/bfs_monthly.csv). Annual figures in the baseline are sums of the unadjusted (`sa=U`) monthly values for the US total and NAICS sectors.
- **Series used:**

| Series | Meaning |
|---|---|
| `BA_BA` | All business applications |
| `BA_HBA` | High-propensity applications |
| `BA_WBA` | Applications with planned wages |
| `BF_BF4Q` / `BF_BF8Q` | Employer business formations within 4 or 8 quarters of application |

- **Method paper:** Bayard et al. (2018), §2.E below.
- **Caveats:**
  - No pre-2004 baseline.
  - Applications measure *intent*. The low and falling conversion rate (17.3% in 2006 → 10.2% in 2019 for BF8Q/BA) is itself a finding.

#### Census Nonemployer Statistics (NES): used

- **What it is:** annual counts and receipts of businesses with no paid employees (≥$1,000 receipts), from IRS tax records.
- **Landing page:** [Census Nonemployer Statistics](https://www.census.gov/programs-surveys/nonemployer-statistics.html)
- **Files used:**
  - [nonemp06us.txt (2006, US by NAICS)](https://www2.census.gov/programs-surveys/nonemployer-statistics/datasets/2006/historical-datasets/nonemp06us.txt)
  - [nonemp19us.zip (2019, US by NAICS × receipts size)](https://www2.census.gov/programs-surveys/nonemployer-statistics/datasets/2019/historical-datasets/nonemp19us.zip)
- **Caveats:**
  - NAICS vintages differ (2002 vs 2017).
  - The 2022 release changed methodology, so do not link post-2021 NES to earlier years without adjustment.

#### Census Annual Business Survey (ABS) and Longitudinal Business Database (LBD): referenced

- ABS, including the 2018 technology module that measures cloud adoption: [Census ABS](https://www.census.gov/programs-surveys/abs.html)
- LBD, restricted microdata behind BDS (FSRDC access): [Census LBD](https://www.census.gov/programs-surveys/ces/data/restricted-use-data/longitudinal-business-database.html)

#### BLS Business Employment Dynamics (BED): referenced, not used

- **What it is:** quarterly gross job flows from QCEW/UI records, 1992+. Includes establishment-age ("Entrepreneurship and the U.S. Economy") and firm-size-class tabulations. A useful cross-check on BDS with a different source (UI records vs. IRS/Census business register) and different timing (quarterly).
- **URLs:**
  - [BLS BED home](https://www.bls.gov/bdm/)
  - [BED establishment age](https://www.bls.gov/bdm/bdmage.htm)
  - [BED firm size](https://www.bls.gov/bdm/bdmfirmsize.htm)
  - [Entrepreneurship and the U.S. Economy](https://www.bls.gov/bdm/entrepreneurship/entrepreneurship.htm)
- **Access note:** bls.gov returns HTTP 403 to non-browser clients, so open these in a browser. No BED numbers appear in the baseline.

### 1.2 European Union

#### Eurostat Structural Business Statistics (SBS): used

- **Dataset used:** `sbs_sc_sca_r2`, "Annual enterprise statistics by size class for special aggregates of NACE Rev.2 activities (2005–2020)". [Data browser](https://ec.europa.eu/eurostat/databrowser/view/sbs_sc_sca_r2/default/table)
  - Aggregate: `nace_r2=B-N_S95_X_K`, the non-financial business economy.
  - Indicators: `V16110` persons employed, `V11110` number of enterprises.
  - Size classes: `size_emp` = 0–9, 10–19, 20–49, 50–249, 250+.
  - Geographies: EU27_2020 and EU28 are populated from 2011; DE, FR, IT, ES also pulled.
- **Successor, 2021+ (EBS regulation, not linked to the above):** `sbs_sc_ovw`. [Data browser](https://ec.europa.eu/eurostat/databrowser/view/sbs_sc_ovw/default/table)
- **API used:** `https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/<dataset>?format=JSON&...`. Large queries return HTTP 413 "ASYNCHRONOUS_RESPONSE"; retry after about 30 s or narrow the filters.
- **Topic page:** [Eurostat SBS](https://ec.europa.eu/eurostat/web/structural-business-statistics)
- **Cross-check:** [Eurostat news, 27 June 2022, "EU small and medium-sized enterprises: an overview"](https://ec.europa.eu/eurostat/web/products-eurostat-news/-/edn-20220627-1). For 2019 it reports micro+small at 48.4% and medium at 16.0% of non-financial employment, which matches our computation.
- **Caveats:**
  - NACE Rev. 1.1 → Rev. 2 break in 2008.
  - Statistical-unit changes from legal unit to profiled enterprise in some member states around 2017–2018 (visible in FR and DE).
  - The unit is persons employed, which includes proprietors.

#### Eurostat business demography: used

- **Pre-2021 dataset:** `bd_9bd_sz_cl_r2`, "Business demography by size class and NACE Rev. 2 activity (2004–2020)". [Data browser](https://ec.europa.eu/eurostat/databrowser/view/bd_9bd_sz_cl_r2/default/table)

| Indicator | Meaning |
|---|---|
| `V97020` | Birth rate |
| `V97042` | 2-year survival rate |
| `V97120` | Employment share of births |
| `V11920` | Births (number) |
| `V11910` | Active enterprises |
| `V16910` | Persons employed in active enterprises |

- **NACE aggregates used:**

| Code | Meaning |
|---|---|
| `B-S_X_K642` | Industry, construction and services excluding holding companies |
| `B-N_X_K642` | Business economy excluding holding companies |
| `J` | Information and communication |
| `J62` | Computer programming and consultancy |

- **Current dataset:** `bd_size`, 2021+ for EU27. [Data browser](https://ec.europa.eu/eurostat/databrowser/view/bd_size/default/table)
- **Explainer:** [Statistics Explained: Business demography statistics](https://ec.europa.eu/eurostat/statistics-explained/index.php?title=Business_demography_statistics)
- **Caveats:**
  - EU aggregates for the total business economy are not populated in the pre-2021 dataset.
  - UK coverage ends in 2018.
  - Birth rates are strongly affected by national self-employment and incorporation policy, e.g. the French auto-entrepreneur regime from 2009.

#### European Commission SME Performance Review / Annual Report on European SMEs: referenced

- [SME Performance Review (DG GROW)](https://single-market-economy.ec.europa.eu/smes/sme-strategy/sme-performance-review_en)
- The 2018/2019 edition reports SMEs at 99.8% of enterprises, 66.6% of employment and 56.4% of value added in the EU-28 non-financial business sector (2018). These are modelled estimates by DIW Econ, so they are not identical to raw SBS.

#### OECD DynEmp / MultiProd: referenced

- Harmonised cross-country firm-dynamics microdata projects behind Criscuolo et al. (2014) and Calvino et al. (2020). Recommended for break-free European comparisons.
- Project page URL not verified this pass; the OECD site returned 403 to non-browser clients. Use the publication link in §2.

---

## 2. Academic papers

### A. Declining business dynamism

1. **Decker, R., Haltiwanger, J., Jarmin, R., & Miranda, J. (2014).** "The Role of Entrepreneurship in US Job Creation and Economic Dynamism." *Journal of Economic Perspectives*, 28(3), 3–24.
   - DOI: [10.1257/jep.28.3.3](https://doi.org/10.1257/jep.28.3.3)
   - Replication: [openICPSR 113932](https://www.openicpsr.org/openicpsr/project/113932)
   - Status: verified
2. **Decker, R., Haltiwanger, J., Jarmin, R., & Miranda, J. (2016).** "Where Has All the Skewness Gone? The Decline in High-Growth (Young) Firms in the U.S." *European Economic Review*, 86, 4–23.
   - WP: [NBER w21776](https://www.nber.org/papers/w21776)
   - Status: verified as NBER WP 21776; journal volume/pages taken from the IWH listing. Confirm the journal DOI before citing.
3. **Decker, R., Haltiwanger, J., Jarmin, R., & Miranda, J. (2020).** "Changing Business Dynamism and Productivity: Shocks versus Responsiveness." *American Economic Review*, 110(12), 3952–90.
   - DOI: [10.1257/aer.20190680](https://doi.org/10.1257/aer.20190680)
   - WP: [NBER w24236](https://www.nber.org/papers/w24236)
   - Status: verified
4. **Akcigit, U., & Ates, S. T. (2021).** "Ten Facts on Declining Business Dynamism and Lessons from Endogenous Growth Theory." *American Economic Journal: Macroeconomics*, 13(1), 257–98.
   - DOI: [10.1257/mac.20180449](https://doi.org/10.1257/mac.20180449)
   - WP: [NBER w25755](https://www.nber.org/papers/w25755)
   - Status: verified
5. **Karahan, F., Pugsley, B., & Şahin, A. (2024).** "Demographic Origins of the Start-up Deficit." *American Economic Review*, 114(7), 1986–2023.
   - DOI: [10.1257/aer.20210362](https://doi.org/10.1257/aer.20210362)
   - WP: [NBER w25874](https://www.nber.org/papers/w25874)
   - Replication: [openICPSR 188261](https://openicpsr.org/openicpsr/project/188261/version/V1/view)
   - Status: verified
6. **Pugsley, B., & Şahin, A. (2019).** "Grown-up Business Cycles." *Review of Financial Studies*, 32(3), 1102–47.
   - Status: unverified
7. **Hopenhayn, H., Neira, J., & Singhania, R. (2022).** "From Population Growth to Firm Demographics: Implications for Concentration, Entrepreneurship and the Labor Share." *Econometrica*, 90(4), 1879–1914.
   - Status: unverified
8. **Calvino, F., Criscuolo, C., & Verlhac, R. (2020).** "Declining Business Dynamism: Structural and Policy Determinants." *OECD Science, Technology and Industry Policy Papers*, No. 94.
   - URL: [OECD publication page](https://www.oecd.org/en/publications/2020/11/declining-business-dynamism_111d20a3.html)
   - Status: verified

### B. Job creation by firm size vs. firm age

9. **Haltiwanger, J., Jarmin, R., & Miranda, J. (2013).** "Who Creates Jobs? Small versus Large versus Young." *Review of Economics and Statistics*, 95(2), 347–61.
   - WP: [NBER w16300](https://www.nber.org/papers/w16300)
   - Status: verified
10. **Criscuolo, C., Gal, P. N., & Menon, C. (2014).** "The Dynamics of Employment Growth: New Evidence from 18 Countries." *OECD Science, Technology and Industry Policy Papers*, No. 14. Also CEP Discussion Paper 1274.
    - URL: [LSE eprint 60286](https://eprints.lse.ac.uk/60286/)
    - Status: verified

### C. Cloud computing: causal and micro evidence

11. **Ewens, M., Nanda, R., & Rhodes-Kropf, M. (2018).** "Cost of Experimentation and the Evolution of Venture Capital." *Journal of Financial Economics*, 128(3), 422–42.
    - DOI: [10.1016/j.jfineco.2018.03.001](https://doi.org/10.1016/j.jfineco.2018.03.001)
    - WP: [NBER w24523](https://www.nber.org/papers/w24523)
    - Status: verified. Page range is 422–442 in most listings and 422–438 in one; confirm against the journal.
12. **DeStefano, T., Kneller, R., & Timmis, J. (2023).** "Cloud Computing and Firm Growth." *Review of Economics and Statistics*, published online 29 Nov 2023.
    - DOI: [10.1162/rest_a_01393](https://doi.org/10.1162/rest_a_01393)
    - WP: [CESifo WP 8306](https://www.cesifo.org/DocDL/cesifo1_wp8306_0.pdf)
    - Status: verified. Check the final print volume/issue.
13. **Jin, W., & McElheran, K. (2017/2018).** "Economies before Scale: Survival and Performance of Young Plants in the Age of Cloud Computing." Working paper (SSRN; NBER Summer Institute 2018).
    - URL: [NBER SI 2018 PDF](https://www.nber.org/conferences/2006/Jin_McElheran_EBS_SI_Submission_2018.pdf)
    - Status: verified as a working paper. Check for a later journal version.
14. **Koning, R., Hasan, S., & Chatterji, A. (2022).** "Experimentation and Start-up Performance: Evidence from A/B Testing." *Management Science*, 68(9), 6434–53.
    - DOI: [10.1287/mnsc.2021.4209](https://doi.org/10.1287/mnsc.2021.4209)
    - WP: [NBER w26278](https://www.nber.org/papers/w26278)
    - Status: verified
15. **Zolas, N., Kroff, Z., Brynjolfsson, E., McElheran, K., Beede, D., Buffington, C., Goldschlag, N., Foster, L., & Dinlersoz, E. (2020).** "Advanced Technologies Adoption and Use by U.S. Firms: Evidence from the Annual Business Survey." NBER Working Paper 28290.
    - URL: [NBER w28290](https://www.nber.org/papers/w28290)
    - Status: verified (WP number and lead authors). Check the full author list.
16. **Bloom, N., & Pierri, N. (2018).** "Cloud Computing Is Helping Smaller, Newer Firms Compete." *Harvard Business Review*, 31 Aug 2018.
    - Status: unverified (title and date confirmed via a BU TPRI listing; authors and data not confirmed)

### D. Counterforces: IT, scale and concentration

17. **Bessen, J. (2020).** "Industry Concentration and Information Technology." *Journal of Law and Economics*, 63(3), 531–55.
    - DOI: [10.1086/708936](https://doi.org/10.1086/708936)
    - SSRN: [3044730](https://papers.ssrn.com/abstract=3044730)
    - Status: verified
18. **Autor, D., Dorn, D., Katz, L., Patterson, C., & Van Reenen, J. (2020).** "The Fall of the Labor Share and the Rise of Superstar Firms." *Quarterly Journal of Economics*, 135(2), 645–709.
    - Status: unverified

### E. Measuring business formation

19. **Bayard, K., Dinlersoz, E., Dunne, T., Haltiwanger, J., Miranda, J., & Stevens, J. (2018).** "Early-Stage Business Formation: An Analysis of Applications for Employer Identification Numbers." NBER Working Paper 24364.
    - DOI: [10.3386/w24364](https://doi.org/10.3386/w24364)
    - Also Census CES WP 18-52; FEDS 2018-015
    - Status: verified
20. **Guzman, J., & Stern, S. (2020).** "The State of American Entrepreneurship: New Estimates of the Quantity and Quality of Entrepreneurship for 32 US States, 1988–2014." *American Economic Journal: Economic Policy*, 12(4), 212–43.
    - DOI: [10.1257/pol.20170498](https://doi.org/10.1257/pol.20170498)
    - WP: [NBER w22095](https://www.nber.org/papers/w22095)
    - Status: verified

**Count:** 20 academic references, 15 with bibliographic details verified this pass. Five are flagged unverified: Pugsley & Şahin 2019, Hopenhayn et al. 2022, Bloom & Pierri 2018, Autor et al. 2020, and the EER volume/pages for Decker et al. 2016.

---

## 3. Cloud launch-date sources (timeline §1.1)

- AWS S3 (2006-03-14) and EC2 beta (2006-08-25): [Wikipedia, Timeline of Amazon Web Services](https://en.wikipedia.org/wiki/Timeline_of_Amazon_Web_Services); [TechCrunch, 2021-08-28, EC2 history](https://techcrunch.com/2021/08/28/how-amazon-ec2-grew-from-a-notion-into-a-foundational-element-of-cloud-computing). Prefer AWS press releases for a formal citation.
- Google App Engine preview (2008-04-07/08): [Google Developers Blog, "Google App Engine at Campfire One"](https://developers.googleblog.com/en/google-app-engine-at-campfire-one)
- Windows Azure GA (2010-02-01): [Microsoft Learn archive, "Commercial Availability of Windows Azure Platform"](https://learn.microsoft.com/en-us/archive/blogs/usisvde/commercial-availability-of-windows-azure-platform); [InfoWorld](https://www.infoworld.com/article/2300071/microsoft-windows-azure-cloud-reaches-general-availability-stage-2.html)
- Google Compute Engine GA (2013-12-02): [HPCwire, 2013-12-05](https://www.hpcwire.com/2013/12/05/google-compute-engine-enters-general-availability/); [InfoQ](https://www.infoq.com/news/2013/12/gcega/)
- Complementary-layer dates in baseline §1.2 (Heroku, GitHub, Stripe, Lambda, etc.) were **not re-verified**.

---

## 4. Reproducing the computed numbers

Every [C] figure in the baseline comes from the public files above using simple ratios:

| Measure | Formula |
|---|---|
| Startup rate | `firms[fage='a) 0'] / firms[total]` (bds2023_fa / bds2023) |
| Young share | sum over `fage` a)–f) (ages 0–5) ÷ total |
| Size shares | `emp` by `fsize` class ÷ sum over classes (bds2023_fz) |
| Net job creation by size | sum of `net_job_creation` by `fsize` over BDS years |
| Sector startup rate | `firms[sector, fage='a) 0'] / firms[sector]` (bds2023_sec_fa / bds2023_sec) |
| BFS annual figures | sum of the 12 unadjusted monthly values (`sa=U`, `geo=US`) |
| EU size shares | `V16110[size] / V16110[TOTAL]` for `nace_r2=B-N_S95_X_K` |

The analysis scripts were scratch files and were not kept. Re-deriving takes a few lines of Python over the CSV and JSON listed here.

---

## 5. AI-era official data sources (for `ai_adoption_evidence.md`)

#### Census Business Trends and Outlook Survey (BTOS): used

- **What it is:** biweekly survey of about 1.2M businesses (about 20k responses per wave). AI questions run from September 2023.
- **Landing page:** [Census BTOS](https://www.census.gov/hfp/btos)
- **Files used** (downloaded 2026-10-29, latest wave 2026-10-05 → 10-18):
  - [Employment Size Class.xlsx](https://www.census.gov/hfp/btos/downloads/Employment%20Size%20Class.xlsx)
  - [National.xlsx](https://www.census.gov/hfp/btos/downloads/National.xlsx)
- **Items used:**
  - Question 7: current AI use, last two weeks.
  - Question 24: expected use in the next six months.
  - Size codes: A 1–4, B 5–9, C 10–19, D 20–49, E 50–99, F 100–249, G 250+.
- **Caveats:**
  - The wording changed in November 2025, from "producing goods or services" to "any of its business functions". The file holds only the new-wording series (24 waves from 202524).
  - In the 2026 file, the item text reads "Super Intelligence or SI (formerly referred to as Artificial Intelligence or AI)". Confirm in the technical notes that this is a relabel only.
  - Estimates are firm-weighted. Biweekly noise is large for the 250+ class.

#### Census Annual Business Survey (ABS) technology modules: referenced

- **Modules:**
  - 2018 and 2021: digital technology, including ML, machine vision, NLP and voice recognition.
  - 2019 and 2023: automation, including AI, robotics and cloud, with effects on employment.
- [Census ABS](https://www.census.gov/programs-surveys/abs.html)
- Overview slides: Dinlersoz, E. (2024-12-13), "Measuring AI Use by Businesses", BEA FESAC meeting. [PDF](https://apps.bea.gov/fesac/meetings/2024-12-13/Dinlersoz.pdf). Status: verified (read).

#### Census Business Formation Statistics (BFS): used again

- Same `bfs_monthly.csv` as §1.1, re-pulled 2026-10-29 with data through September 2026.
- Additional series used: `BA_CBA` (corporate applications).
- **Caveat:** formation series (`BF_BF4Q`, `BF_BF8Q`) currently end at application-year 2022.

#### Eurostat ICT usage in enterprises: AI: used

- **Dataset:** `isoc_eb_ai`, by size class, 2021/2023/2024/2025. [Data browser](https://ec.europa.eu/eurostat/databrowser/view/isoc_eb_ai/default/table)
  - Indicators used: `E_AI_TANY` (any AI technology), `E_AI_TNLG` (generating language or code), `E_AI_BCST` (not used: costs), `E_AI_BLE` (not used: lack of expertise).
  - `unit=PC_ENT`; `geo=EU27_2020`; `nace_r2=C10-S951_X_K`.
  - Covers enterprises with 10+ persons; micro enterprises are not covered.
- **By NACE:** `isoc_eb_ain2`.
- **Explainer:** [Statistics Explained: Use of artificial intelligence in enterprises](https://ec.europa.eu/eurostat/statistics-explained/index.php?title=Use_of_artificial_intelligence_in_enterprises) (data extracted Dec 2025). Status: verified (read).

#### Official notes and statistical releases

- **Grundy, A., Breaux, C., & Khatiwoda, D. (2026-05-26).** "Large Firms With at Least 20 Employees Biggest AI Users." U.S. Census Bureau, America Counts story.
  - [census.gov story](https://census.gov/library/stories/2026/05/ai-use-businesses.html)
  - Status: verified (read)
- **Allen, J. S. (2026-04-03).** "Monitoring AI Adoption in the U.S. Economy." *FEDS Notes*, Board of Governors of the Federal Reserve System.
  - [federalreserve.gov](https://www.federalreserve.gov/econres/notes/feds-notes/monitoring-ai-adoption-in-the-u-s-economy-20260403.html)
  - Status: verified (read)

---

## 6. Academic papers: AI era

### F. Measuring AI adoption

21. **McElheran, K., Li, J. F., Brynjolfsson, E., Kroff, Z., Dinlersoz, E., Foster, L., & Zolas, N. (2024).** "AI Adoption in America: Who, What, and Where." *Journal of Economics & Management Strategy*, 33(2), 375–415.
    - DOI: [10.1111/jems.12576](https://doi.org/10.1111/jems.12576)
    - WP: [NBER w31788](https://www.nber.org/papers/w31788)
    - Status: verified
22. **Bonney, K., Breaux, C., Buffington, C., Dinlersoz, E., Foster, L., Goldschlag, N., Haltiwanger, J., Kroff, Z., & Savage, K. (2024).** "Tracking Firm Use of AI in Real Time: A Snapshot from the Business Trends and Outlook Survey." NBER Working Paper 32319; Census CES WP 24-16.
    - URL: [NBER w32319](https://www.nber.org/papers/w32319)
    - Status: verified
23. **Bonney, K., Breaux, C., Buffington, C., Dinlersoz, E., Foster, L., Goldschlag, N., Haltiwanger, J., Kroff, Z., & Savage, K. (2024).** "The Impact of AI on the Workforce: Tasks versus Jobs?" *Economics Letters*, 244.
    - URL: [IDEAS listing](https://ideas.repec.org/a/eee/ecolet/v244y2024ics0165176524004555.html)
    - Status: verified (journal and volume). Check the article number/DOI and the author list against the journal page.
24. **Bonney, K., Breaux, C. L., Dinlersoz, E., Foster, L. S., Haltiwanger, J. C., & Pande, A. A. (2026).** "The Microstructure of AI Diffusion: Evidence from Firms, Business Functions, and Worker Tasks." NBER Working Paper 35141; Census CES WP 26-25.
    - URL: [NBER w35141](https://www.nber.org/papers/w35141)
    - URL: [Census CES-WP-26-25](https://www.census.gov/library/working-papers/2026/adrm/CES-WP-26-25.html)
    - Status: verified (abstract read)

### G. AI and employment at adopting firms

25. **Babina, T., Fedyk, A., He, A., & Hodson, J. (2024).** "Artificial Intelligence, Firm Growth, and Product Innovation." *Journal of Financial Economics*, 151, 103745.
    - DOI: [10.1016/j.jfineco.2023.103745](https://doi.org/10.1016/j.jfineco.2023.103745)
    - Status: verified (bibliographic and abstract). Regression magnitudes not extracted.
26. **Babina, T., Fedyk, A., He, A., & Hodson, J. (2023).** "Firm Investments in Artificial Intelligence Technologies and Changes in Workforce Composition." NBER Working Paper 31325. Also a chapter in *Technology, Productivity, and Economic Growth* (NBER/University of Chicago Press).
    - URL: [NBER w31325](https://www.nber.org/papers/w31325)
    - Status: verified (WP). The 7.3% non-college-share figure comes from Columbia Business School press coverage.
27. **Aghion, P., Bunel, S., Jaravel, X., Mikaelsen, T., Roulet, A., & Søgaard, J. (2025).** "How Different Uses of AI Shape Labor Demand: Evidence from France." *AEA Papers and Proceedings*, 115, 62–67.
    - DOI: [10.1257/pandp.20251047](https://doi.org/10.1257/pandp.20251047)
    - Replication: [openICPSR E215601](https://doi.org/10.3886/E215601)
    - Status: verified
28. **Hampole, M., Papanikolaou, D., Schmidt, L. D. W., & Seegmiller, B. (2025).** "Artificial Intelligence and the Labor Market." NBER Working Paper 33509 (rev. Sep 2025).
    - URL: [NBER w33509](https://www.nber.org/papers/w33509)
    - Status: verified
29. **Acemoglu, D., Autor, D., Hazell, J., & Restrepo, P. (2022).** "Artificial Intelligence and Jobs: Evidence from Online Vacancies." *Journal of Labor Economics*, 40(S1), S293–S340.
    - DOI: [10.1086/718327](https://doi.org/10.1086/718327)
    - WP: NBER w28257
    - Status: verified
30. **Humlum, A., & Vestergaard, E. (2025).** "Large Language Models, Small Labor Market Effects." NBER Working Paper 33777; BFI WP 2025-56.
    - URL: [NBER w33777 (IDEAS)](https://ideas.repec.org/p/nbr/nberwo/33777.html)
    - URL: [BFI](https://bfi.uchicago.edu/working-papers/large-language-models-small-labor-market-effects)
    - Status: verified. Versions differ: the bound is 1% in the May 2025 version and 2% in the NBER version. Cite the latest.
31. **Stevens, R. (2026).** "Payrolls to Prompts: Firm-Level Evidence on the Substitution of Labor for AI." arXiv:2602.00139.
    - DOI: [10.48550/arXiv.2602.00139](https://doi.org/10.48550/arXiv.2602.00139)
    - Status: verified (abstract)
32. **Acemoglu, D., Anderson, G., Beede, D., Buffington, C., Childress, E., Dinlersoz, E., Foster, L., Goldschlag, N., Haltiwanger, J., Kroff, Z., Restrepo, P., & Zolas, N. (2022).** "Automation and the Workforce: A Firm-Level View from the 2019 Annual Business Survey." NBER Working Paper 30659; chapter in *Technology, Productivity, and Economic Growth*.
    - Status: unverified (title confirmed in Census slides; WP number and author list from domain knowledge)

### H. Workers, occupations and exposure

33. **Brynjolfsson, E., Chandar, B., & Chen, R. (2025, rev. 2026).** "Canaries in the Coal Mine? Six Facts about the Recent Employment Effects of Artificial Intelligence." Stanford Digital Economy Lab working paper.
    - URL: [Aug 2026 version (PDF)](https://digitaleconomy.stanford.edu/app/uploads/2026/08/Canaries_August2026.pdf)
    - URL: [Nov 2025 version (PDF)](https://digitaleconomy.stanford.edu/app/uploads/2025/11/CanariesintheCoalMine_Nov25.pdf)
    - Status: verified (URLs). Headline figures (13%, 16%, 19%) taken from secondary summaries of each version.
34. **Brynjolfsson, E., Li, D., & Raymond, L. (2025).** "Generative AI at Work." *Quarterly Journal of Economics*, 140(2), 889–942.
    - DOI: [10.1093/qje/qjae044](https://doi.org/10.1093/qje/qjae044)
    - Status: verified. The page range ends at 942 or 944 depending on the source.
35. **Eloundou, T., Manning, S., Mishkin, P., & Rock, D. (2024).** "GPTs are GPTs: Labor Market Impact Potential of LLMs." *Science*.
    - DOI: [10.1126/science.adj0998](https://doi.org/10.1126/science.adj0998)
    - Status: verified (DOI and authors). The 80%/19% exposure figures are unverified this pass.
36. **Acemoglu, D. (2025).** "The Simple Macroeconomics of AI." *Economic Policy*.
    - WP: [NBER w32487](https://www.nber.org/papers/w32487)
    - Repository: [MIT DSpace](https://dspace.mit.edu/handle/1721.1/166327)
    - Status: verified (0.66% upper bound). Journal DOI not checked. Drafts differ on the adjusted figure (0.53% vs 0.55%).
37. **Felten, E., Raj, M., & Seamans, R. (2021).** "Occupational, Industry, and Geographic Exposure to Artificial Intelligence: A Novel Dataset and Its Potential Uses." *Strategic Management Journal*, 42(12), 2195–2217.
    - DOI: 10.1002/smj.3286
    - Status: unverified
38. **Webb, M. (2020).** "The Impact of Artificial Intelligence on the Labor Market." Working paper, SSRN 3482150.
    - Status: unverified
39. **Noy, S., & Zhang, W. (2023).** "Experimental Evidence on the Productivity Effects of Generative Artificial Intelligence." *Science*, 381(6654), 187–192.
    - DOI: 10.1126/science.adh2586
    - Status: unverified

### I. Robots and automation (prior technology)

40. **Acemoglu, D., Lelarge, C., & Restrepo, P. (2020).** "Competing with Robots: Firm-Level Evidence from France." *AEA Papers and Proceedings*, 110, 383–388.
    - WP: [NBER w26738](https://www.nber.org/papers/w26738)
    - Status: verified (venue, volume, pages, finding). DOI not checked.
41. **Koch, M., Manuylov, I., & Smolka, M. (2021).** "Robots and Firms." *Economic Journal*, 131(638), 2553–2584.
    - Status: unverified (venue confirmed only via citing papers)
42. **Acemoglu, D., & Restrepo, P. (2020).** "Robots and Jobs: Evidence from US Labor Markets." *Journal of Political Economy*, 128(6), 2188–2244.
    - DOI: 10.1086/705716
    - Status: unverified
43. **Graetz, G., & Michaels, G. (2018).** "Robots at Work." *Review of Economics and Statistics*, 100(5), 753–768.
    - DOI: 10.1162/rest_a_00754
    - Status: unverified

### J. Elasticity of substitution

44. **Gechert, S., Havranek, T., Irsova, Z., & Kolcunova, D. (2022).** "Measuring Capital-Labor Substitution: The Importance of Method Choices and Publication Bias." *Review of Economic Dynamics*, 45, 55–82.
    - WP: [CEPR DP15687 (PDF)](https://repec.cepr.org/repec/cpr/ceprdp/DP15687.pdf)
    - Status: verified (venue, volume, pages, 0.9 → 0.3 result). Journal DOI not checked.
45. **Oberfield, E., & Raval, D. (2021).** "Micro Data and Macro Technology." *Econometrica*, 89(2), 703–732.
    - DOI: [10.3982/ECTA12807](https://doi.org/10.3982/ECTA12807)
    - WP: [NBER w20452](https://www.nber.org/papers/w20452)
    - Status: verified
46. **Karabarbounis, L., & Neiman, B. (2014).** "The Global Decline of the Labor Share." *Quarterly Journal of Economics*, 129(1), 61–103.
    - DOI: [10.1093/qje/qjt032](https://doi.org/10.1093/qje/qjt032)
    - Status: verified (bibliographic). The σ ≈ 1.25 estimate is not in the abstract; check the body.
47. **Krusell, P., Ohanian, L., Ríos-Rull, J.-V., & Violante, G. (2000).** "Capital-Skill Complementarity and Inequality: A Macroeconomic Analysis." *Econometrica*, 68(5), 1029–1053.
    - DOI: [10.1111/1468-0262.00150](https://doi.org/10.1111/1468-0262.00150)
    - Status: verified (bibliographic). The σ values 1.67 and 0.67 are unverified this pass.
48. **DeCanio, S. J. (2016).** "Robots and Humans – Complements or Substitutes?" *Journal of Macroeconomics*, 49, 280–291.
    - DOI: [10.1016/j.jmacro.2016.08.003](https://doi.org/10.1016/j.jmacro.2016.08.003)
    - Status: verified (about 1.9 threshold)
49. **Luduvice, A. V. D., & Pinheiro, R. (2026).** "AI-Augmented Capital-Skill Complementarity." Federal Reserve Bank of Cleveland Working Paper 26-22.
    - DOI: [10.26509/frbc-wp-202622](https://doi.org/10.26509/frbc-wp-202622)
    - Status: verified (read). Estimates: σ(AI, high-skill × equipment) ≈ 0.89; σ(high-skill, equipment) ≈ 0.24; σ(high, low composites) ≈ 2.7.
50. **Whitfill, P., & Wu, C. (2025).** "Will Compute Bottlenecks Prevent an Intelligence Explosion?" arXiv:2507.23181.
    - URL: [arXiv 2507.23181](https://arxiv.org/abs/2507.23181)
    - Status: verified (URL). Author names from search summary.

### K. AI-era startups

51. **Dinlersoz, E., Dogan, C., & Zolas, N. (2024).** "Starting Up AI." U.S. Census Bureau, CES Working Paper 24-09.
    - URL: [Census CES-WP-24-09](https://census.gov/library/working-papers/2024/adrm/CES-WP-24-09.html)
    - Status: verified (abstract)
52. **Kim, H., & Koning, R. (2026).** "AI-Native Firms." Harvard Business School Working Paper 26-090.
    - URL: [HBS item 69077](https://www.hbs.edu/faculty/Pages/item.aspx?num=69077)
    - Summary: [HBS AI Institute](https://aiinstitute.hbs.edu/less-headcount-more-valuation-how-ai-native-firms-change-the-game/)
    - Status: verified (WP number and headline 25%/12%). The 13-vs-42 average headcount comes from press coverage.

**Count, §6:** 32 new academic references (21–52). 25 are verified this pass at least at the bibliographic level; 7 are unverified (32, 37, 38, 39, 41, 42, 43).

---

## 7. Industry and secondary sources (context only; not for calibration)

- **Carta (2025).** *Solo Founders Report 2025*. Solo-founder share 23.7% (2019) → 36.3% (H1 2025). [Carta](https://carta.com/data/solo-founders-report/). Status: verified (secondary summary).
- **Carta (2025).** *State of Startup Compensation, H2 2025*. Series D headcount −29% from the 2023 peak; about 40% of dollars to AI companies. [Carta](https://carta.com/sg/en/data/startup-compensation-h2-2025/). Status: verified (secondary summary).
- **Crunchbase News (Jan 2026).** Year-end 2025 global funding: $425B total, AI about $212B (about 50%), up from 34% in 2024. [Crunchbase News: AI section](https://news.crunchbase.com/sections/ai/). Status: unverified. Figures come via secondary summaries; locate the specific year-end article before citing.
- **Gusto (Apr 2026).** "Leaner Startups, More Founders: How AI Is Reshaping the Economics of Starting a Business." [Gusto](https://gusto.com/resources/gusto-insights/how-ai-is-reshaping-small-business-formation). Status: unverified (page returned HTTP 403; figure from search snippet).
- **Y Combinator batch composition.** S25 is 88% AI-native per [Extruct analysis](https://www.extruct.ai/research/ycs25/). Status: unverified (third-party classification).
- **McKinsey & Company.** *The State of AI* (Mar 2025; Nov 2025). [McKinsey](https://www.mckinsey.com/capabilities/quantumblack/our-insights/the-state-of-ai). Status: unverified this pass.

---

## 8. Reproducing the AI-era computed numbers

See `data/ai_adoption_evidence.md` §7 for exact files, filters and formulas: BTOS size-class rates, Eurostat `isoc_eb_ai` by size, and BFS 2018–2026 annual and Jan–Sep sums and ratios.
