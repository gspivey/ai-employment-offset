# AI Adoption and Labor-Market Evidence (2017–2026)

Research notes for calibrating the AI block of the model (T7): `sigma_ai`, `ai_adoption_fixed_cost`, the diffusion schedule, and the entry channel (`entry_cost_post`, `ai_entrant_productivity_shift`). Companion to `data/cloud_era_baseline.md`.

Compiled 2026-10-29. Full references with URLs/DOIs: `data/sources.md` §5–§8.

**Provenance tags** (same scheme as the cloud baseline)

| Tag | Meaning |
|---|---|
| **[C]** | Computed by us from official public files: Census BTOS `Employment Size Class.xlsx` / `National.xlsx` (downloaded 2026-10-29, latest period 2026-10-05→10-18), Eurostat `isoc_eb_ai` via API, Census BFS `bfs_monthly.csv` (through Sep 2026). Reproducible; see §7. |
| **[P]** | Paper finding as stated in the published abstract/summary; bibliographic data verified. |
| **[V]** | Bibliographic details verified this pass; finding taken from a secondary description or slides. Read the paper before quoting. |
| **[U]** | Not re-verified this pass (domain knowledge). Check before citing. |

---

## 0. Headline findings

1. **Large firms adopt AI more, and the gap in percentage points is widening.** [C] In the current-wording Census BTOS series, 43.6% of firms with 250+ employees used AI in early Oct 2026, against 22.6–26.0% for every class below 50 employees. Averaged over the last six biweekly waves, the ratio of the 250+ class to the 1–4 class is **1.74**, almost exactly the 1.72 of the first six waves (Nov 2025–Feb 2026). The absolute gap widened from 12.8 pp to 17.3 pp. In the EU (enterprises with 10+ persons), 55.0% of large enterprises used AI in 2025 against 17.0% of small ones. That ratio fell from 4.6 (2021) to 3.2 (2025) while the gap rose from 22 pp to 38 pp.
2. **Diffusion is fast and still in its early phase.** [C] BTOS national use rose from 17.3% (Nov 2025) to 24.6% (Oct 2026) on the new wording. The older "producing goods or services" wording ran 3.7% (Sep 2023) → 5.4% (Feb 2024) → about 10% (2025). Eurostat: 7.7% (2021) → 8.1% (2023) → 13.5% (2024) → 20.0% (2025).
3. **Adopting firms have not shed workers on net so far.** [P] AI-investing US firms grew faster in sales *and employment*, concentrated among the largest firms (Babina et al. 2024). French AI adopters raised employment and sales after adoption (Aghion et al. 2025). In BTOS, only about 5% of AI users reported any employment change in 2024 (increases more common than decreases), and only **2%** reported AI-related employment reductions in the 2026 supplement. Robot adopters also expanded, at competitors' expense (Acemoglu, Lelarge & Restrepo 2020).
4. **The displacement shows up in tasks, occupations and young workers, not in adopter headcount.** [P] AI-exposed establishments cut non-AI hiring (Acemoglu et al. 2022). Within firms, demand falls for exposed occupations, while firm-level productivity gains offset it in aggregate (Hampole et al. 2025). Employment of 22–25-year-olds in the most exposed occupations is 13–19% below trend, mostly through reduced hiring (Brynjolfsson, Chandar & Chen, 2025–26 revisions). Danish LLM adoption shows precise nulls on earnings and hours (Humlum & Vestergaard 2025).
5. **Startup formation rose but became more employment-light.** [C] Business applications reached 5.67M in 2025, **+62% vs 2019**. High-propensity applications rose only +30%, and applications with planned wages only +5%. Planned-wage applications fell to **6.8%** of all applications in Jan–Sep 2026, against 13.7% in 2019, and are down 15% year on year. This repeats the cloud-era pattern: more formation at the nonemployer margin, not at the employer margin. [V] AI-native startups are 12–25% smaller in headcount than comparable firms (Kim & Koning 2026). The solo-founder share of new startups on Carta rose from 23.7% (2019) to 36.3% (H1 2025).
6. **The empirical σ literature sits mostly below the model's displacement threshold.** The model's adopter headcount falls iff `sigma_ai > 1/(1−α) ≈ 2.78`. Capital–labor estimates run from 0.3 (bias-corrected meta-analysis) to about 1.25. Equipment vs unskilled labor is about 1.67 (KORV). The one aggregate AI-specific estimate (Luduvice & Pinheiro 2026) finds AI *complementary* to the high-skill–equipment composite (σ ≈ 0.89). No published firm-level AI–labor CES elasticity exists yet. The behavioral evidence in (3) is consistent with an effective σ below 2.78 at current adoption intensity.

**Implication for the model:** On present evidence, the "adopters shed labor" region (`sigma_ai > 2.78`) is a tail scenario, not the central case. The data do support three features the model already has: (a) adoption selective on size; (b) a large rise in formation concentrated among employment-light entrants; (c) displacement acting through *hiring* (entrant and young-worker headcount) rather than separations at incumbents. See §6 for concrete parameter recommendations.

---

## 1. AI adoption by firm size

### 1.1 United States: Census BTOS, current wording (Nov 2025 →) [C]

Question 7 (from the Nov 2025 redesign): did the business use AI "in any of its business functions" in the last two weeks. Firm-weighted shares answering "Yes". Source: `Employment Size Class.xlsx`, sheet *Response Estimates*.

| Employment size | First wave (17–30 Nov 2025) | Latest wave (5–18 Oct 2026) | Mean, first 6 waves | Mean, last 6 waves (27 Jul–18 Oct 2026) | Expect to use in next 6 months (latest) |
|---|---|---|---|---|---|
| 1–4 | 17.0 | 24.3 | 17.7 | 23.3 | 28.1 |
| 5–9 | 15.5 | 22.6 | 17.1 | 21.1 | 26.7 |
| 10–19 | 17.8 | 24.6 | 17.2 | 22.1 | 28.9 |
| 20–49 | 18.7 | 26.0 | 18.5 | 23.8 | 30.1 |
| 50–99 | 20.7 | 29.0 | 21.3 | 27.9 | 34.5 |
| 100–249 | 23.7 | 35.3 | 25.4 | 33.5 | 41.1 |
| **250+** | **30.5** | **43.6** | **30.5** | **40.6** | **51.4** |
| All firms (`National.xlsx`) | 17.3 | 24.6 | — | — | — |

Reading the table:
- Adoption is **flat below 50 employees** (about 21–24%) and then rises steeply. In the model, a fixed adoption cost produces a threshold in size, and this is the shape it should generate.
- Ratio of the 250+ class to the 1–4 class: 1.72 at the start, 1.74 at the end. The proportional gap is stable; the pp gap widens as everyone adopts.
- Biweekly estimates for 250+ are noisy (36.5–44.0% across the last six waves). Use multi-wave means as calibration moments.
- **Wording caveat.** In the downloaded file, questions 7 and 24 are worded "Super Intelligence or SI (formerly referred to as Artificial Intelligence or AI)". This looks like a relabelling of the same item. Check the BTOS technical notes before relying on continuity across the relabel.

Corroboration:
- [P] Census story (Grundy, Breaux & Khatiwoda, 26 May 2026) reports 37% for 250+ and 32% for 100–249 at the wave ending 3 May 2026. It also reports no significant change below 20 employees over Dec 2025–May 2026, and a national rate of 19.8%.
- [P] Bonney et al. (2026, NBER w35141), from the 2026 BTOS AI supplement (Nov 2025–Jan 2026): **18% of firms, but 32% employment-weighted**, used AI in at least one function. That puts the employment-weighted rate at about 1.8× the firm-weighted rate. Use reaches 50–60% (60–70% employment-weighted) among very large firms in Information, Professional Services and Finance.

### 1.2 United States: earlier measures

| Source | Period | Firm-weighted use | Size pattern | Tag |
|---|---|---|---|---|
| ABS 2018 technology module (McElheran et al. 2024; Zolas et al. 2020) | 2017 | **< 6%** used any of five AI-related technologies | Employment-weighted about 18%; most very large firms report some use. Use is also concentrated in young, VC-backed, innovating firms and superstar cities. | [P] |
| BTOS legacy wording ("producing goods or services"); Bonney et al. 2024 | Sep 2023 → Feb 2024 | 3.7% → 5.4% | Higher in large firms but **non-monotonic**: U-shaped, with 1–4 employee firms high | [P] |
| BTOS legacy wording; Fed note (Allen 2026) | Q3 2025 | about 10% (+68% y/y) | U-shaped across seven size groups | [P] |
| BTOS new wording; Fed note | end-2025 | about 18% | U-shape replaced by a monotone-from-20 pattern; smallest firms comparable to other <20 classes | [P] |
| Atlanta Fed SBU (Fed note) | Nov 2025 | 69.4% equal-weighted, **78% employment-weighted**; LLMs 46%/54% | Largest firms highest | [P] |

Takeaways for calibration:
- Firm-weighted adoption depends heavily on wording: "producing goods/services" gives about 10%, "any business function" about 18–25%. Executive surveys (SBU) give about 70%. **Pick one definition and keep it.** BTOS new wording is the closest to the model's "pays fixed cost and substitutes AI for labor" concept, and it is the only one with a public size breakdown.
- The legacy U-shape (micro firms high) vanished under the new wording. This suggests some 1–4-employee "use" in the legacy series was light-touch, which supports modelling micro-firm use as a low-fixed-cost tier rather than full adoption.

### 1.3 European Union: Eurostat ICT usage in enterprises, `isoc_eb_ai` [C]

Indicator `E_AI_TANY` (uses at least one of the AI technologies). Enterprises with 10+ persons employed, NACE `C10-S951_X_K`, EU27_2020, % of enterprises. Micro enterprises are not covered.

| Size class | 2021 | 2023 | 2024 | 2025 |
|---|---|---|---|---|
| 10–49 | 6.1 | 6.4 | 11.2 | 17.0 |
| 50–249 | 12.6 | 13.1 | 21.0 | 30.4 |
| 250+ | 28.4 | 30.5 | 41.2 | 55.0 |
| All 10+ | 7.7 | 8.1 | 13.5 | 20.0 |
| Ratio 250+ / 10–49 | 4.6 | 4.8 | 3.7 | 3.2 |
| Gap 250+ − 10–49 (pp) | 22.3 | 24.1 | 30.0 | 38.0 |

Generative-type use (`E_AI_TNLG`, generating language or code), 2025: 7.0% / 14.8% / 31.7% for small / medium / large. In 2023 it was 1.8% / 2.8% / 7.7%. The GenAI wave scaled with size: the large-firm rate quadrupled.

By sector, 2025 (Statistics Explained, `isoc_eb_ain2`) [P]:
- Information and communication: 62.5%
- Professional, scientific and technical: 40.4%
- Real estate: 24.8%
- Construction: 10.8% (lowest)

Barriers, 2025:
- Among enterprises that considered AI [P]: lack of expertise 70.9%, unclear legal consequences 52.5%, data protection 48.8%.
- As a share of all enterprises [C]: "costs too high" is cited by 4.0% of small enterprises and 5.5–5.7% of medium and large ones. "Lack of expertise" is cited by 7.2% (small) and 10.3–10.5% (medium and large).
- Neither cost nor skills shortage, as stated, is concentrated among small firms. That argues for modelling the adoption fixed cost as **integration/organizational** (scale-invariant in level, so lighter per worker at large firms) rather than as a pure cash price.

### 1.4 Private surveys (secondary, use only as context) [U]

- McKinsey *State of AI* (Mar 2025 and Nov 2025 editions): 78% and then 88% of respondent organizations use AI in at least one function. The sample is skewed to large firms, and large-revenue firms are further along in scaling. Not comparable to BTOS; this is an upper-bound-style series like the SBU.

### 1.5 Size gap: answer to research question 1

Yes. Large firms adopt faster in every official source, and the size premium is steepest above 50–100 employees.

| Measure | Value | Source |
|---|---|---|
| US current ratio, 250+ vs <20 | about 1.8× | BTOS |
| US employment-weighted vs firm-weighted rate | about 1.8× | BTOS supplement |
| EU ratio, 250+ vs 10–49 | 3.2× (2025), down from 4.6× (2021) | Eurostat |

The *relative* gap is stable (US) or narrowing (EU) as diffusion proceeds. The *absolute* gap is widening in both. The ABS-2017 → BTOS-2026 sequence shows the same ordering throughout.

---

## 2. AI and employment at adopting firms

### 2.1 Firm-level evidence

| Study | Data / design | Finding on adopter employment | Tag |
|---|---|---|---|
| **Babina, Fedyk, He & Hodson (2024)**, *JFE* | US public firms 2010–2018. AI investment measured from résumés (Cognism) and postings (Burning Glass). IV: firm exposure to universities' AI graduate supply. | AI-investing firms grow faster in **sales, employment** and valuation, through product innovation. Growth **concentrates among larger firms** and is associated with **higher industry concentration**. | [P]; magnitudes [U] |
| Babina, Fedyk, He & Hodson (2023/2025), NBER w31325, workforce composition | Same data | AI investors shift to more educated, STEM-heavy staff. The hierarchy flattens (more juniors, fewer middle and senior managers). The non-college share falls about 7.3%. Total employment does not fall. | [V] |
| **Aghion, Bunel, Jaravel, Mikaelsen, Roulet & Søgaard (2025)**, *AEA P&P* | French firm data 2017–2020, difference-in-differences on adoption timing | Employment and sales **rise** after AI adoption. Even occupations classed as AI-substitutable expand. Effects are heterogeneous by use: positive for ICT security, negative for administrative-process uses. Adopters are larger, more productive and more skill-intensive. | [P] |
| **Hampole, Papanikolaou, Schmidt & Seegmiller (2025)**, NBER w33509 | Task-level AI exposure by firm × occupation × year, 2010–2023. IV from historical university hiring networks. | Demand falls for tasks and occupations with high mean exposure. Concentrated exposure lets workers reallocate effort. **Net employment effects are modest**: productivity-driven growth at adopters offsets the decline in exposed occupations. | [P] |
| **Acemoglu, Autor, Hazell & Restrepo (2022)**, *JOLE* | Near-universe of US online vacancies 2010–2018, establishment level | AI-exposed establishments **reduce non-AI hiring** as they expand AI hiring, and change skill requirements. No detectable effect at the occupation or industry level yet. | [P] |
| **Bonney et al. (2024)**, *Economics Letters* (BTOS AI supplement, Dec 2023–Feb 2024) | Firm survey | 27% of AI users replace worker tasks, but **only about 5% report any employment change**, with increases more common than decreases. Expected rises: 35% (tasks) and 12% (employment). 87% of task-replacers replace only a few tasks. | [P] (slides [V]) |
| **Bonney et al. (2026)**, NBER w35141 (2026 BTOS AI supplement) | Firm survey, Nov 2025–Jan 2026 | 66% of users augment tasks; **employment reductions in 2% of firms**. Performance rises with breadth of AI integration. Functional deployment and operational AI investment are associated with employment *declines*; worker-task use is not, once those are controlled for. | [P] |
| **Humlum & Vestergaard (2025)**, NBER w33777 | Denmark: 25k workers, 7k workplaces, 11 exposed occupations, linked employer–employee data, 2023–2024 | Precise **null** on earnings and recorded hours, at worker and workplace level. Rules out effects above 2% two years after. Some task restructuring and occupational switching. | [P] |
| **Stevens (2026)**, arXiv 2602.00139 | Expense-platform payments, Q3 2021–Q3 2025. DiD on ChatGPT release, by pre-shock share of spending on online-labor platforms. | Most-exposed firms cut spending on freelance platforms. Each $1 less of online-labor spend comes with about **$0.03** more AI spend. Spending substitution, not headcount. | [P] |

### 2.2 Worker- and occupation-level evidence

- **Brynjolfsson, Chandar & Chen** ("Canaries in the Coal Mine", ADP payroll data). [V] This is descriptive, not causal, and the estimate has grown across revisions:

  | Version | Relative employment decline, ages 22–25 in most-exposed occupations | Notes |
  |---|---|---|
  | Aug 2025 | 13% | |
  | Nov 2025 | 16% | |
  | Aug 2026 (data to June 2026) | 19% | Effect works through **reduced hiring, not separations**. No economy-wide displacement. |

- **Productivity in field experiments:**
  - Brynjolfsson, Li & Raymond (2025, *QJE*): +15% issues resolved per hour for customer-support agents with GenAI, concentrated among less-experienced agents. [P]
  - Noy & Zhang (2023, *Science*): writing tasks completed faster and at higher quality. [U]
- **Exposure indices** (for `sector_ai_exposure` and the task share φ):
  - Eloundou et al. (2024, *Science*): about 80% of US workers have ≥10% of tasks exposed to LLMs; about 19% have ≥50% exposed. [P] metadata; numbers [U]
  - Felten, Raj & Seamans (2021, *SMJ*) AIOE index. [U]
  - Webb (2020) patent-overlap exposure. [U]
- **Macro-task accounting:** Acemoglu (2025, *Economic Policy*). [P]
  - Only about 4.6% of GDP is in tasks both exposed and profitably automatable within 10 years (about 20% exposed × about 23% cost-effective).
  - That implies TFP gains of at most **0.66% over 10 years**, and below 0.53% once hard-to-learn tasks are accounted for.
  - In the paper's task-based specification (§4.1), this is the natural anchor for φ in the near term.

### 2.3 Robots and automation: the closest prior technology

| Study | Finding | Tag |
|---|---|---|
| Acemoglu, Lelarge & Restrepo (2020), *AEA P&P*, France 2010–2015 | 598 robot adopters (about 20% of manufacturing employment). Adopters' hours **+10.9%**, but at competitors' expense. A 20 pp rise in industry robot adoption gives **−3.2% industry employment**. | [P] |
| Koch, Manuylov & Smolka (2021), *EJ*, Spain | Robot adopters raise output and employment; non-adopters lose. | [U] |
| Acemoglu & Restrepo (2020), *JPE*, US commuting zones | One more robot per 1,000 workers lowers the employment/population ratio by about 0.2 pp and wages by about 0.42%. | [U] |
| Graetz & Michaels (2018), *ReStat*, 17 countries | Robots raise labor productivity. No significant effect on total hours; the low-skill share falls. | [U] |
| Acemoglu et al. (2022), 2019 ABS automation module | Adoption concentrated in large firms. Few adopters report employment declines. | [V] |

**Pattern across all of 2.1–2.3:** adopters grow and their competitors or exposed occupations shrink. That is the model's **reallocation-toward-adopters** channel, not within-adopter displacement. Because adopters are larger, the evidence points toward a **rising large-firm employment share**, matching Babina et al.'s concentration result and the cloud-era baseline (`cloud_era_baseline.md` §0.1).

---

## 3. Startup formation, 2020–2026

### 3.1 Census BFS: business applications (US, unadjusted annual sums) [C]

| Year | All applications (BA) | High-propensity (HBA) | With planned wages (WBA) | Corporate (CBA) | HBA/BA % | WBA/BA % |
|---|---|---|---|---|---|---|
| 2018 | 3,486,829 | 1,330,929 | 503,783 | 553,409 | 38.2 | 14.4 |
| 2019 | 3,498,990 | 1,316,191 | 478,640 | 520,532 | 37.6 | 13.7 |
| 2020 | 4,356,498 | 1,518,956 | 524,651 | 532,635 | 34.9 | 12.0 |
| 2021 | 5,390,816 | 1,841,954 | 638,140 | 594,441 | 34.2 | 11.8 |
| 2022 | 5,062,563 | 1,722,399 | 578,669 | 559,165 | 34.0 | 11.4 |
| 2023 | 5,469,302 | 1,848,540 | 613,708 | 561,122 | 33.8 | 11.2 |
| 2024 | 5,224,176 | 1,715,458 | 550,423 | 541,315 | 32.8 | 10.5 |
| 2025 | 5,671,836 | 1,708,842 | 501,223 | 525,860 | 30.1 | 8.8 |
| 2026 Jan–Sep | 4,927,840 | 1,386,358 | 336,905 | — | 28.1 | 6.8 |

Changes:
- **2019 → 2025:** BA +62%, HBA +30%, WBA +5%, CBA +1%.
- **Jan–Sep 2026 vs Jan–Sep 2025:** BA +15%, HBA +5%, **WBA −15%**. WBA is also below Jan–Sep 2019 (−11%).

Sectors, BA:
- Information (NAICS 51): 73k (2019) → 110k (2025). Jan–Sep 2026 is +40% y/y, while HBA is flat to down.
- Professional services (NAICS 54): 457k → 764k (+67%). Jan–Sep 2026 is +30% y/y.

Formations (BF4Q, employer within 4 quarters):
- 280k (2019), 315k (2021), 297k (2022).
- **The current file has no formation series after application-year 2022**, so 2023+ conversion cannot be computed yet.
- BF4Q/BA fell from 8.0% (2019) to 5.9% (2021–2022).

Interpretation:
- The post-2020 surge in applications sits overwhelmingly at the **non-employer / low-propensity** margin, as in 2006–2019.
- The share that plans to hire has fallen every year since 2018, and fell faster in 2025–2026, the years of rapid AI diffusion.
- This is consistent with AI lowering the cost of *starting* without raising, and possibly lowering, the headcount *needed* at start.
- Caveat: application counts can be inflated by non-genuine EIN filings and by changes in filing behaviour. Do not treat BA levels as firm entry. Use HBA, WBA and, once released, BF4Q/BF8Q.

### 3.2 AI-specific formation and startup size

- **Dinlersoz, Dogan & Zolas (2024), "Starting Up AI"** (Census CES WP 24-09). [P]
  - Applications are text-classified as AI-related from the EIN form.
  - The flow was flat from 2004–2011, rose from 2012 and again from 2016, and made a **large discrete jump in 2023** (post-ChatGPT).
  - AI-related applications are **more likely to become employer startups**.
  - The resulting firms have higher revenue, average wage and labor share, similar labor productivity, and **lower survival**.
- **Kim & Koning (2026), "AI-Native Firms"** (HBS WP 26-090; about 2,900 YC companies 2020–2024 matched to Revelio workforce data). [V]
  - AI-native startups are **about 25% smaller** in the YC sample and **about 12% smaller** in the broader PitchBook sample (industry × cohort controls). Average YC AI startup about 13 workers vs 42.
  - Per-employee valuation is higher. Staff mix: more engineers, about 15% fewer entry-level workers and managers, flatter hierarchy.
  - The headcount gap is largest in services-delivery industries.
- **Carta.** [V]
  - The solo-founder share of new startups rose from 23.7% (2019) to about 30% (2024) and 36.3% (H1 2025).
  - Solo-led firms received only 14.7% of priced-round cash in 2024.
  - Average Series D headcount is down 29% from the 2023 peak (to 131, 2025).
  - About 40% of 2025 startup dollars on Carta went to AI companies.
- **Gusto (Apr 2026).** 2024 cohorts have about 6% lower headcount at 12 months than earlier cohorts. [U]: page returned 403; secondary citation only.

### 3.3 Funding and accelerator composition

| Indicator | Value | Tag |
|---|---|---|
| Crunchbase global venture funding, 2025 | $425B (+30% y/y), of which **AI about $212B, about 50%** (34% in 2024) | [V] |
| Y Combinator Summer 2025 batch | 88–90% AI-native or AI-focused (secondary counts disagree on batch size and definition) | [U] |
| YC Spring 2025 | About 47% building AI agents or agent tooling | [U] |

The capital-allocation picture matches the cloud era (Ewens, Nanda & Rhodes-Kropf 2018). Cheaper experimentation shows up as more, smaller and leaner bets, while dollars concentrate in a few capital-intensive AI labs. The funding share is a statement about *where VC goes*, not about the population of new firms.

### 3.4 Answer to research question 3

The AI era has changed the *composition* of startups more than the *rate* of employer formation:
- Applications are at record levels.
- High-propensity applications are about 30% above 2019 but flat since 2021.
- Planned-wage applications are now **below** 2019.
- AI-related applications jumped in 2023, and convert to employers at higher rates.
- AI-native startups launch with 12–25% fewer workers.

In the model this calls for a **larger entry-pool response** (`entry_pool_elasticity`, `entry_cost_post`) together with a **smaller headcount per entrant**. Raising `ai_entrant_productivity_shift` alone would imply more employment per entrant, which the data do not show.

---

## 4. Elasticity of substitution: empirical guidance on `sigma_ai`

### 4.1 What the model needs

`model/parameters.py`: within an adopter, labor and AI services combine CES with elasticity `sigma_ai`, nested in y = z·X^α with α = 0.64. Adopter headcount falls iff **σ > 1/(1−α) = 2.78**. The default is 3.5, i.e. *above* the threshold.

Note: the paper's §4 (`paper/sections/04-ai-model.tex`) instead uses a task-based Cobb–Douglas aggregate, which is unit elasticity across tasks plus a displacement share φ. The two parameterisations are not the same object. The evidence below maps to σ in the code and to φ in the paper.

### 4.2 Estimates

| Estimate | Object | Value | Tag |
|---|---|---|---|
| Gechert, Havranek, Irsova & Kolcunova (2022), *RED* | Capital–labor σ, meta-analysis of 3,186 estimates in 121 studies | Raw mean about 0.9. **Corrected for publication bias and method: about 0.3** (range 0–0.6). | [P] |
| Oberfield & Raval (2021), *Econometrica* | Aggregate capital–labor σ, US manufacturing, built up from plant level | **0.5–0.7**, slightly declining since 1970 | [P] |
| Karabarbounis & Neiman (2014), *QJE* | Capital–labor σ from cross-country labor-share and investment-price trends | About 1.25 (in body, not abstract) | [U] number; DOI [V] |
| Krusell, Ohanian, Ríos-Rull & Violante (2000), *Econometrica* | Equipment vs unskilled labor; equipment vs skilled labor | About **1.67** and about **0.67** | [U] numbers; DOI [V] |
| **Luduvice & Pinheiro (2026)**, Cleveland Fed WP 26-22 | AI capital vs (high-skill labor × equipment) composite in a nested KORV-type CES, GMM on US aggregates | **σ ≈ 0.89** (complements). AI weight in production about 2.4%. Inner high-skill–equipment σ ≈ 0.24. High-skill vs low-skill composites σ ≈ 2.7. | [P] |
| DeCanio (2016), *J. Macroeconomics* | Human–robot σ above which robot growth lowers aggregate wages (Houthakker method) | Threshold **about 1.9**, lower for manufacturing workers. A threshold, not an estimate. | [P] |
| Stevens (2026) | Firm-level spending substitution, freelance labor → AI APIs | $1 of labor spend replaced with about $0.03 of AI spend. Implies very high cost savings on substitutable tasks, but not a CES σ. | [P] |
| Whitfill & Wu (2025), arXiv | Compute vs research labor at frontier labs | Sign depends on specification (substitutes in the baseline, complements in "frontier experiments") | [V] |

No published firm-level CES elasticity between AI services and labor exists as of Oct 2026.

### 4.3 Indirect inference from adopter behaviour

Under the model's algebra, a firm that adopts and then *expands* employment reveals σ < 1/(1−α) at its relevant margin. The evidence in §2.1–2.3 points the same way:
- Babina et al.: employment up.
- Aghion et al.: employment up, even in substitutable occupations.
- BTOS: increases more common than decreases; reductions in 2% of firms.
- Acemoglu–Lelarge–Restrepo: robot adopters' hours +10.9%.
- Humlum–Vestergaard: no hours effect.

All of these imply an effective σ **below 2.78** at current adoption intensity, with two caveats:
1. **Selection.** Adopters are faster-growing firms (Babina, Aghion, McElheran). IV and DiD designs address this partly.
2. **Early phase.** Hampole et al. and Bonney et al. (2026) find employment declines where AI is *deployed in functions* or backed by *operational investment*, i.e. at higher intensity. The young-worker hiring decline (Brynjolfsson et al.) shows displacement on the hiring margin that firm-level net headcount does not reveal.

---

## 5. Calibration map: model parameter ↔ evidence

| Model parameter / target | Current value | Evidence | Recommendation |
|---|---|---|---|
| `sigma_ai` | 3.5 | §4. Capital–labor σ 0.3–1.67; AI-specific aggregate 0.89; firm behaviour implies < 2.78. | Make **below-threshold the central case**: median about 1.8–2.0. Keep a right tail above 2.78 for "agentic AI" scenarios, with P(σ > 2.78) about 0.2. Report results conditional on the side of the threshold. Treat 3.5 as a stress scenario. |
| `AI_TARGETS.adoption_rate` | 0.09, "BTOS 2025" | §1.1–1.2. 0.09 matches the *legacy* wording in mid-2025. | Replace with a dated, wording-consistent target: e.g. **0.173 (17–30 Nov 2025)** and **0.246 (5–18 Oct 2026)**, firm-weighted BTOS new wording. Add **employment-weighted 0.32** (Nov 2025–Jan 2026, Bonney et al. 2026). |
| New targets: adoption by size | — | §1.1 table | Add moments `adopt_rate_<20` ≈ 0.22, `adopt_rate_50_249` ≈ 0.31, `adopt_rate_250plus` ≈ 0.41 (last-6-wave means, 2026). Or target the ratio 250+/(<20) ≈ 1.8. Identifies `ai_adoption_fixed_cost`. |
| `ai_diffusion_speed`, `ai_diffusion_midpoint` | 0.5, 8.0 | BTOS: +7.3 pp in about 11 months (new wording). Legacy: 3.7% (Sep 2023) → about 10% (2025). EU: 8.1% (2023) → 20.0% (2025). | With ceiling 1, late-2026 adoption of about 0.25 sits on the steep lower part of a logistic. If `ai_start_period` is Nov 2022, the current 0.5/8 schedule gives S(4) ≈ 0.10, which is too slow against the new-wording series and about right against the legacy one. Choose the wording first. |
| `sector_ai_exposure` ordering | goods 0.5 < trade 0.8 < prof. 1.2 < info/fin 1.5 | US BTOS: Information 39.7%, Finance 33.9%, Prof. services about 33%, Retail about 14%, Accommodation/food 8% (2026). EU: ICT 62.5%, Prof. 40.4%, Construction 10.8%. | Ordering confirmed. Ratio info/fin to retail/trade about 2.5–3, a bit steeper than the current 1.5/0.8. |
| `entry_cost_post` / `entry_pool_elasticity` | 16 (−20%) / 0.3 | BA +62% and HBA +30% vs 2019, but WBA flat to falling. AI-related applications jumped in 2023. | Entry-pool response is large at the low-propensity margin. Calibrate to **HBA** (+30%) or **WBA** (≈0%), not to BA. |
| Entrant headcount | via φ / σ | Kim & Koning: AI-native startups 12–25% smaller. WBA/BA share 13.7% → 6.8%. | Use −12% to −25% employment per entrant at given productivity as an **untargeted validation moment**. |
| Concentration | emp_share_large | Babina et al. 2024: AI growth concentrated in large firms, raising concentration. Cloud baseline: large-firm share rose 2006–2019. | Use as the sign test in the empirical-signatures section: a rising 500+ share is the prior, not the null. |

---

## 6. Open gaps

1. **Firm-level σ.** No direct CES estimate exists. The best route is BTOS supplement microdata (FSRDC) linked to LBD employment, or the Stevens-type payments data with headcount.
2. **Formations after 2022.** BF4Q/BF8Q for 2023+ applications are absent from the current BFS file. Re-pull when released to test whether the 2023 AI jump converted to employers.
3. **BDS for 2024–2025.** The BDS 2023 release ends in March 2023. Firm-size employment shares for the AI era are not yet observable in BDS. SUSB 2022 is the latest size snapshot.
4. **Wording break.** BTOS legacy vs new wording (Nov 2025) and the "SI" relabel in the 2026 file need a crosswalk before any long diffusion series is fit.
5. **Magnitudes from Babina et al. (2024)** need extraction from the full text (the abstract gives signs only).

---

## 7. Reproducing the [C] numbers

| Item | File / call | Computation |
|---|---|---|
| BTOS by size | `https://www.census.gov/hfp/btos/downloads/Employment%20Size%20Class.xlsx`, sheet *Response Estimates* | Rows `Question ID = 7` (current use) and `24` (expected), `Answer ID = 1` (Yes). Size codes: A 1–4, B 5–9, C 10–19, D 20–49, E 50–99, F 100–249, G 250+. Period codes `YYYYCC` map to dates in sheet *Collection and Reference Dates* (`Smpdt` column), e.g. 202524 = 17–30 Nov 2025, 202621 = 5–18 Oct 2026. |
| BTOS national | `https://www.census.gov/hfp/btos/downloads/National.xlsx` | Same question and answer IDs |
| Eurostat | `https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/isoc_eb_ai?format=JSON&geo=EU27_2020&unit=PC_ENT&lang=EN` | `indic_is = E_AI_TANY / E_AI_TNLG / E_AI_BCST / E_AI_BLE`; `size_emp = 10-49, 50-249, GE250, GE10` |
| BFS | `https://www.census.gov/econ/bfs/csv/bfs_monthly.csv` | `sa=U`, `geo=US`, `naics_sector=TOTAL` (or `NAICS51`, `NAICS54`). Annual = sum of 12 months; Jan–Sep = first 9. Series `BA_BA, BA_HBA, BA_WBA, BA_CBA, BF_BF4Q`. |

Scripts were scratch files and were not kept. Each figure is a few lines of Python over the files above.
