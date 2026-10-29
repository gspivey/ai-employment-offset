# Cloud-Era Replication Scenarios (T5)

Can the firm-dynamics model reproduce the **concentration** of 2006–2019, when the baseline AI shock produces **offset** (small-firm expansion, net employment +4–5%)?

Compiled 2026-10-29. Code: `scripts/cloud_replication.py`. Raw results: `data/cloud_replication_results.csv` (single-lever sweep, 8 seeds), `data/cloud_replication_grid.csv` (240-cell grid, 8 seeds), `data/cloud_replication_confirm.csv` (finalists and decomposition, 24 seeds). Empirical targets: `data/cloud_era_baseline.md` §2.1, §3.

---

## 0. Headline findings

1. **Only one parameter changes the sign of the size-share response: `sigma_ai` below the displacement threshold 1/(1−α) ≈ 2.78.** No entry-cost, fixed-cost, entrant-quality or founder-pool setting on its own turns the baseline's deconcentration into concentration. The single-lever sweep never pushes the <500 share below +0.5 pp when σ = 3.5. In the 240-cell grid, the only σ = 3.5 cell where all three moments fall reaches just −0.23 pp on the share. It gets there by shrinking small firms (total employment −12.7%), not by growing large ones.
2. **Concentration alone is not the cloud era.** A labour-complementary technology by itself (F1) moves employment to 500+ firms but *raises* the startup rate and the young-firm share. To match all three cloud-era moments, it must be paired with **entry headwinds**: a smaller founder pool, a higher employer entry cost, and no "cloud-native" quality gain for entrants.
3. **Best fit (F2):** σ = 2.0 at the baseline unit-cost gain, employer entry cost 20 → 24 (+20%), entrant productivity shift 0, founder pool 600 → 480 (−20%). Years 11–15 after the shock:

   | Moment | Model F2 | Cloud era | Model, relative | Cloud era, relative |
   |---|---|---|---|---|
   | <500 employment share | **−2.28 pp** | −3.9 pp | 500+ share **+9.1%** | 500+ share +7.9% |
   | Startup rate | **−1.57 pp** | −1.8 pp | **−21%** | −17.5% |
   | Young (0–5) employment share | **−3.11 pp** | −2.8 pp | **−17%** | −21% |
   | Net employment change landing in 500+ firms | **>100%** (+3.1% vs −0.3% of total) | ~90% | | |

4. **The parts separate cleanly.** Technology (σ) drives the size distribution; entry-side parameters drive dynamism (see the F2 decomposition in §5). Switching σ back to 3.5 removes all of the concentration and leaves the startup decline unchanged. Removing the founder-pool decline removes 79% of the young-share decline.
5. **For the AI paper:** the baseline offset rests on two legs, displacement at large adopters (σ > θ) and an intact entry pipeline. Give the baseline AI shock cloud-era founder headwinds and keep its 20% entry-cost cut. The <500 share still rises (+1.5 pp), but net employment goes to **−8.7% at year 13 and −15.4% long-run** instead of +4%. Displacement continues; absorption does not.

---

## 1. Setup

**Mapping.** The model's "AI" shock stands in for the cloud/IT shock. Its three channels become:

- (a) the employer entry cost `entry_cost_pre → entry_cost_post`;
- (b) the entrant log-productivity shift;
- (c) a factor-augmenting technology with a per-period adoption fixed cost (`ai_adoption_fixed_cost = 5`). This plays the role of proprietary IT / cloud integration, which only large firms find worth paying for.

The diffusion schedule is unchanged. AI starts in period 5, and years 11–15 after the start are periods 16–20, with S = 0.81–0.97. This window is centred on 2006 + 13 = 2019.

**Measurement.** Each scenario runs a shocked arm and a frozen pre-shock arm from the same burned-in economy, using common random numbers. Effects are shocked − frozen, averaged over the window. Long-run (LR) effects average the last 10 periods. A before/after comparison inside the shocked arm (2006 → 2019 style) gives the same answer to within 0.1 pp: for F2 it is −2.24 / −1.59 / −3.31 against −2.28 / −1.57 / −3.11, because the frozen arm has no trend.

**Extensions in the runner (no model code changed).**

- Young-firm employment share = employment at firms aged ≤ 5 ÷ total, read from `Economy.age`.
- `fixed_cost` and `potential_entrants` can move with diffusion (`pre + (post − pre)·S(t)`), the same way `entry_cost_post` does natively.
- `ai_cost_full` can be re-solved per σ (below).
- The runner reproduces `compare_scenarios` bit-for-bit when nothing is phased.

**Cost-neutral σ.** In the CES bundle, lowering σ at a fixed AI price also enlarges the productivity gain. At the default `ai_cost_full = 1.5`, σ = 2.0 cuts adopters' unit cost by 25–50% and employment rises +50% (`sigma_2.0` in §3). That is a different shock, not a different labour response. The "n" variants re-solve `ai_cost_full` so that the share-weighted unit cost of adopters at S = 1 equals the baseline's 0.868:

| σ | ai_cost_full | Adopter headcount at same z vs non-adoption, by sector |
|---|---|---|
| 3.5 (baseline) | 1.5 | 0.98–0.82 (displacement) |
| 2.5n | 2.715 | 1.01–1.07 |
| 2.25n | 3.833 | 1.03–1.12 |
| 2.0n | 6.716 | 1.06–1.17 |

**Levels are not calibrated.** Pre-shock, the model's <500 share is 74.9% (data 50.9%), the startup rate is 7.4% (10.3%), and the young-firm share is 19.0% (13.4%). Fit is therefore judged on pp changes and on relative changes. The empirical targets also include non-tech forces (recession, demographics), which the scenarios model explicitly where they are used.

---

## 2. Why the baseline offsets: the mechanism that has to fail

Baseline (σ = 3.5, c_e 20 → 16, entrant shift +0.05), 24 seeds, years 11–15:

| Measure | Value |
|---|---|
| <500 share | **+2.23 pp** |
| Startup rate | **+0.92 pp** |
| Young share | **+2.31 pp** |
| 500+ employment | −2.9% of total |
| <500 employment | −0.0% of total |
| Firm count | +5.1% |
| Net employment, years 11–15 | −2.9% |
| Net employment, LR | **+4.0%** (the brief's +5.05% is seed 42 alone) |

How the offset works:

1. **Displacement at the top.** Adopters are the ~15% of firms that clear `F_ai`, and they hold ~66% of employment. Because σ > θ, they cut headcount by (c/w)^(σ−θ) ≈ 0.82–0.98.
2. **Absorption at the bottom.** A cheaper entry cost, better entrant draws and the technology's option value raise entry. Small and young firms take up the slack over time.

Both legs push the <500 share *up*. Concentration needs a scenario in which large firms grow (leg 1 reversed). Falling dynamism needs entry to fall (leg 2 reversed).

---

## 3. Single-lever sweep (task items 2a–2e), 8 seeds, years 11–15

The standard error of the share column is about 0.3–0.8 pp. "Firms" is the firm-count change. Rows are grouped by the lever being varied.

**Baseline**

| Scenario | <500 share pp | Startup pp | Young pp | Net emp % | Firms % |
|---|---|---|---|---|---|
| Baseline | +2.01 | +0.94 | +2.20 | −2.5 | +4.9 |

**(a) σ < 2.78, raw AI price**

| Scenario | <500 share pp | Startup pp | Young pp | Net emp % | Firms % |
|---|---|---|---|---|---|
| σ = 2.5 | **−1.33** | +1.01 | +2.15 | +11.7 | +5.1 |
| σ = 2.0 | **−6.53** | +1.41 | +1.91 | +49.7 | +5.9 |
| σ = 1.5 | **−27.95** | +2.86 | +1.79 | +361 | +8.8 |

**(b) Smaller entry-cost cut**

| Scenario | <500 share pp | Startup pp | Young pp | Net emp % | Firms % |
|---|---|---|---|---|---|
| c_e −10% (→18) | +2.19 | +0.54 | +2.21 | −3.8 | +3.1 |
| c_e −5% (→19) | +1.53 | +0.35 | +2.29 | −2.8 | +2.2 |
| c_e 0% (→20) | +1.62 | +0.18 | +1.96 | −3.4 | +1.5 |

**(c) Rising entry cost**

| Scenario | <500 share pp | Startup pp | Young pp | Net emp % | Firms % |
|---|---|---|---|---|---|
| c_e +10% (→22) | +1.46 | −0.13 | +1.65 | −4.0 | −0.1 |
| c_e +20% (→24) | +1.49 | −0.45 | +1.25 | −4.4 | −1.6 |

**(d) Higher fixed operating cost (rises with diffusion)**

| Scenario | <500 share pp | Startup pp | Young pp | Net emp % | Firms % |
|---|---|---|---|---|---|
| fc 0.5 → 0.75 | +2.03 | +1.21 | +2.57 | −3.4 | −3.8 |
| fc 0.5 → 1.0 | +0.92 | +1.47 | +2.41 | −2.7 | −11.2 |
| fc 0.5 → 1.5 | +1.03 | +1.86 | +1.96 | −5.0 | −22.9 |
| fc 1.0 throughout | +2.19 | +1.17 | +2.45 | −2.4 | +6.0 |

**(e) Lower entrant productivity**

| Scenario | <500 share pp | Startup pp | Young pp | Net emp % | Firms % |
|---|---|---|---|---|---|
| shift 0 | +1.47 | +0.77 | +1.07 | −4.1 | +3.5 |
| shift −0.05 | +1.33 | +0.60 | −0.19 | −6.3 | +2.0 |
| shift −0.10 | +1.23 | +0.41 | −1.88 | −8.4 | +0.5 |
| shift −0.20 | +0.51 | −0.02 | **−4.18** | −11.3 | −2.7 |

**(extra) Founder pool shrinks**

| Scenario | <500 share pp | Startup pp | Young pp | Net emp % | Firms % |
|---|---|---|---|---|---|
| pool −10% | +1.97 | +0.40 | +1.31 | −5.1 | +1.4 |
| pool −20% | +1.20 | −0.18 | −0.10 | −5.9 | −2.0 |

**(extra) General equilibrium (finite labour supply ε)**

| Scenario | <500 share pp | Startup pp | Young pp | Net emp % | Firms % |
|---|---|---|---|---|---|
| ε = 1, baseline | +2.23 | +0.97 | +1.90 | −1.1 | +5.6 |
| ε = 1, σ = 2.0 raw | −2.20 | +1.28 | +1.57 | +12.1 | +1.4 |
| ε = 0.5, σ = 2.0 raw | −1.10 | +1.27 | +2.04 | +6.8 | +0.6 |
| ε = 0, σ = 2.0 raw | −0.23 | +1.23 | +1.50 | 0.0 | −0.6 |

### Why each lever fails to replicate the cloud era on its own

- **(a) σ < θ.** This is the only lever that concentrates, and it does so for the right reason: adopters *expand* headcount, and because `F_ai` limits adoption to large firms, the gains land in 500+. The displacement leg disappears, so there is nothing for small firms to absorb.
  - Two things go wrong. The startup rate and young share still *rise*, because the technology raises the option value of entering. And at the default AI price, σ ≤ 2.0 is a productivity explosion (+50% to +361% employment).
  - A finite labour supply chokes the raw-σ boom off (ε = 0 leaves −0.23 pp). Under the cost-neutral calibration it instead *amplifies* concentration (§4, F2-GE). Rising wages hit non-adopters, whose unit cost is the full wage, harder than adopters, whose CES cost is partly shielded.
- **(b)/(c) Entry cost.** It moves the startup rate by about 0.35 pp per 10% change in c_e. It barely touches size shares (all +1.5 to +2.2 pp), because entrants hold ~2% of employment and the large-firm displacement leg is untouched. Entry cost governs **dynamism, not concentration**. Even +20% leaves the <500 share rising.
- **(d) Fixed cost.** Raising c_f kills marginal small firms (firm count −11% to −23%), but the startup *rate* rises (+1.5 to +1.9 pp) and the young share rises. With fewer incumbents and an unchanged founder pool, entrants per incumbent go up, and exiting old firms are replaced by young ones. That is **more churn**, the opposite of the cloud era (reallocation fell from 27.6% to 22.3%, and employer firm count was +1.4%). Survivors are larger, but the <500 share still rises. The fixed cost is uniform across firms, so "higher for small firms" is captured only through its larger share of small firms' profit. A size-dependent fixed cost would need a model change.
- **(e) Entrant quality.** This is the strongest lever on the young-firm share (a shift of ≈ −0.14 hits the −2.8 pp target on its own). It leaves the startup rate near zero and the <500 share still rising. Entrants' log-normal draws (sd 0.6, so log-employment sd ≈ 1.7) feed *both* tails: some entrants land directly in 500+. Weaker entry therefore removes employment from small and large firms alike, and the share barely moves.
- **Founder pool (demographics).** It lowers both dynamism moments, and per unit it is the most efficient lever on the young share, but it leaves the share rising, for the same reason as (e).

---

## 4. Combinations that produce concentration

### 4.1 Grid search

240 cells × 8 seeds. Each cell sets technology {σ = 3.5, 2.5 raw, 2.5n, 2.25n, 2.0n}, `entry_cost_post` {16, 20, 22, 24}, entrant shift {+0.05, 0, −0.10, −0.15} and founder pool {600, 540, 480}.

- **145 of 240 cells** give all three moments falling. 144 of them have σ < θ. The lone σ = 3.5 cell is the attrition case in §0.
- Average across the grid, by lever:

| Lever | Setting | <500 share pp | Startup pp | Young pp |
|---|---|---|---|---|
| Technology | σ = 3.5 | +1.05 | −0.74 | −2.03 |
| Technology | 2.5n | −1.40 | −0.74 | −2.38 |
| Technology | 2.25n | −2.13 | −0.74 | −2.48 |
| Technology | 2.0n | −2.88 | −0.74 | −2.57 |
| Entry cost | 16 → 24 | −1.36 → −1.68 | +0.07 → −1.28 | −1.75 → −2.87 |
| Founder pool | 600 → 480 | −1.23 → −1.74 | −0.24 → −1.21 | −1.34 → −3.48 |
| Entrant shift | +0.05 → −0.15 | −1.14 → −1.89 | −0.35 → −1.11 | +0.23 → −4.92 |

### 4.2 Finalists, 24 seeds, years 11–15

"Neg." is the share of seeds with a negative Δ<500. The standard error is about 0.3 pp on the share, about 0.01 pp on startup and about 0.15 pp on young.

| ID | Parameters (changes from baseline) | Δ<500 pp | Δ startup pp | Δ young pp | Net emp % | Δemp <500 (% of total) | Δemp 500+ (% of total) | Firms % | LR Δ<500 pp | Neg. |
|---|---|---|---|---|---|---|---|---|---|---|
| F0 | baseline | +2.23 | +0.92 | +2.31 | −2.9 | −0.04 | −2.89 | +5.1 | +2.24 | 4% |
| F1 | σ 2.0n only | −1.70 | **+0.92** | **+1.74** | +12.0 | +7.11 | +4.92 | +5.0 | −2.07 | 96% |
| **F2** | **σ 2.0n; c_e → 24; shift 0; pool → 480** | **−2.28** | **−1.57** | **−3.11** | +2.8 | −0.31 | +3.08 | −8.9 | −3.22 | 96% |
| F3 | σ 2.0n; c_e → 16 (cloud cut kept); shift −0.10; pool → 480 | −3.08 | −0.64 | −4.31 | +1.9 | −1.82 | +3.68 | −5.9 | −2.42 | 100% |
| F4 | σ 2.25n; c_e → 22; shift −0.10; pool → 540 | −2.05 | −1.22 | −4.12 | −1.1 | −2.89 | +1.80 | −7.4 | −2.47 | 92% |
| F5 | σ 2.5 raw; c_e → 24; shift 0; pool → 480 | −1.47 | −1.45 | −2.87 | +1.6 | −0.33 | +1.93 | −8.6 | −2.32 | 83% |
| F2-GE | F2 with ε = 1 | −2.82 | −1.60 | −3.29 | +1.2 | −1.98 | +3.14 | −9.4 | **−5.19** | 96% |
| F2+fc | F2 with fc 0.5 → 1.0 | −3.17 | −1.25 | −3.14 | +2.1 | −1.69 | +3.83 | **−22.5** | −4.14 | 100% |
| F6 | σ 3.5; c_e → 24; shift −0.10; pool → 480 | +0.78 | −1.96 | −4.92 | **−13.8** | −9.68 | −4.06 | −11.5 | +1.63 | 42% |
| X | σ 3.5; c_e → 16; shift 0; pool → 480 | +1.54 | −0.33 | −1.19 | **−8.7** | −5.16 | −3.57 | −3.2 | +1.87 | — |

Relative fit, as Δ500+ share / Δ startup / Δ young:

| Scenario | Δ500+ share | Δ startup | Δ young |
|---|---|---|---|
| Data | +7.9% | −17.5% | −20.9% |
| F2 | +9.1% | −21.4% | −16.6% |
| F3 | +12.3% | −8.7% | −22.9% |
| F4 | +8.2% | −16.6% | −21.8% |
| F5 | +5.9% | −19.8% | −15.3% |
| F2-GE | +11.2% | −21.8% | −17.2% |

**Why the offset fails in each concentrating case:**

- **F1.** There is no displacement to offset. Adopters grow (+4.9% of total in 500+), and small-firm growth (+7.1%) is too slow to hold the share. Dynamism rises, so F1 gives concentration *without* the startup deficit and does not fit the cloud era.
- **F2 / F4 / F5.** Leg 1 is reversed (adopters expand) and leg 2 is cut (fewer founders, a costlier employer entry, no quality gain). Small-firm employment is flat or falling while 500+ employment rises by 2–4% of the total. The 500+ class captures more than 100% of net job growth, close to the ~90% in the data.
- **F3.** This keeps the cloud's measured 20% entry-cost cut (Ewens et al. 2018) and still concentrates hard (−3.1 pp). Only the startup decline falls short (−0.64 vs −1.8 pp). A cheaper entry cost is not enough to offset when the technology favours adopters and the founder pool shrinks.
- **F2-GE.** A finite labour supply makes concentration worse, especially in the long run (−5.2 pp). The adopters' wage bids squeeze non-adopting small firms.
- **F2+fc.** Concentration is stronger, but the firm count collapses (−22.5%) and churn rises. This conflicts with the data (firm count flat, reallocation down).
- **F6 / X (σ = 3.5 with headwinds).** The share still rises because large adopters keep shedding labour. With the entry pipeline weakened, though, the offset collapses into net job loss (−8.7% to −13.8%).

---

## 5. Decomposition of the best fit (F2), 24 seeds, years 11–15

| Variant | Δ<500 pp | Δ startup pp | Δ young pp | Net emp % |
|---|---|---|---|---|
| **F2** | **−2.28** | **−1.57** | **−3.11** | +2.8 |
| σ → 3.5 (displacing technology) | +1.68 | −1.57 | −2.61 | −11.1 |
| c_e → 16 (cloud entry-cost cut) | −2.51 | −0.33 | −1.72 | +5.4 |
| pool → 600 (no demographic headwind) | −2.57 | −0.64 | −0.65 | +7.4 |
| shift → +0.05 (cloud-native entrants) | −2.81 | −1.39 | −1.76 | +5.7 |

Contribution of each ingredient (F2 minus the variant without it):

| Ingredient | <500 share | Startup rate | Young share | Comment |
|---|---|---|---|---|
| σ 2.0n (vs 3.5) | **−3.96 pp** (>100%) | 0.00 | −0.50 | All of the concentration; none of the startup decline |
| Entry cost +20% (vs −20%) | +0.23 | **−1.24** (79%) | −1.39 | Main startup-rate driver |
| Founder pool −20% | +0.29 | −0.93 (59%) | **−2.46** (79%) | Main young-share driver |
| Entrant shift 0 (vs +0.05) | +0.53 | −0.18 | −1.35 | Secondary |

Contributions are non-additive because the model is nonlinear. Entry-side headwinds slightly *raise* the <500 share in F2 for the reason given under (e) in §3: entrants feed both tails.

---

## 6. Which parameters most plausibly explain the cloud era

1. **`sigma_ai` ≈ 2.0–2.25 at a moderate productivity gain. Necessary; most plausible.** It is the only mechanism that reproduces the stock shift *through large-firm growth*. That is what the data show: 500+ employment +19.4% versus <500 +2.0%, with ~90% of net growth in 500+. It fits two pieces of evidence:
   - Cloud and IT mostly replaced IT capital and a narrow set of IT roles, so they complemented rather than substituted labour at adopters (§6.4 of the baseline notes).
   - Proprietary IT raised returns to scale (Bessen 2020).

   **Caveat:** DeStefano et al. (2023) find that cloud adoption *itself* gave incumbents no scale effect. The σ channel is better read as scale-biased IT and software investment broadly (proprietary systems), not as cloud rental specifically. Raw σ ≤ 2.0 at the baseline AI price implies a productivity gain far larger than anything seen in 2006–2019 and is rejected.
2. **Founder pool −10% to −20%. Plausible, and not caused by technology.** It drives most of the young-share decline and about 60% of the startup decline. This is consistent with Karahan, Pugsley & Şahin (2024), where labour-supply growth explains about half the startup decline, and with Hopenhayn, Neira & Singhania (2022). It should be read as the demographic backdrop rather than a cloud effect.
3. **Employer entry cost +10% to +20%. Plausible as a *net employer* barrier, but in tension with the cloud story.** Cloud cut the capital needed to *try* (first VC rounds about 20% smaller; nonemployer firms +30%; applications +34%). The BFS shows the cost of becoming an *employer* rose: wage-planning applications −48%, and 8-quarter employer conversion fell from 17.3% to 10.2%.

   The model's c_e is the sunk cost of becoming an employer firm, so a rise is defensible. Even so, F3 shows that concentration survives with the cloud's 20% cut kept. That cut affects only the size of the startup decline, not whether it happens.
4. **No entrant-quality gain, or a modest decline (shift 0 to −0.10). Secondary and contested.** It helps the young share. It is consistent with the fall in high-growth young firms (Decker et al. 2016) and with high-propensity applications −15%. Guzman & Stern (2020) find quality-adjusted entrepreneurship cyclical rather than declining, so do not lean on this one.
5. **Finite labour supply. Supporting.** It strengthens concentration (F2-GE), which is consistent with slow labour-force growth in the period.
6. **Higher fixed operating costs. Implausible.** They produce more churn and a collapsing firm count, both contradicted by the data.

**Most plausible cloud-era configuration:** F2 or F4. That is a scale-biased, labour-complementary technology at large adopters, plus a demographic decline in the founder pool, plus a higher net employer entry barrier. The technology accounts for the concentration; demographics and the employer barrier account for the dynamism decline.

---

## 7. Implications for the AI paper

- **The baseline's offset is conditional on σ > θ.** If AI at large firms behaves like cloud-era IT (complementing labour and scaling with size), the model predicts cloud-like concentration: about −2 to −3 pp of the <500 share over 13 years. This holds even with a 20% cut in entry cost (F1, F3). The sign of the headcount response at adopting large firms is the decisive empirical parameter. It should anchor the Monte Carlo prior on `sigma_ai`, which is currently U[2, 5], symmetric around 2.78.
- **The offset also needs the entry pipeline.** Run the baseline AI shock with cloud-era founder headwinds while keeping its own −20% entry cost (X). The share still rises, but net employment is −8.7% at year 13 and −15.4% long-run, instead of +4%. The paper's offset result should be shown conditional on the founder pool and the employer-conversion rate, not only on entry cost.
- **What the cloud-era model fit says to watch in AI-era data:**
  - adopter headcount at 500+ firms (sign of σ − θ);
  - BFS employer conversion (BF8Q ÷ BA) and wage-planning applications (employer entry barrier);
  - young-firm employment share.

  Applications and nonemployer counts are the wrong indicators. They rose in the cloud era while employer dynamism fell.

---

## 8. Caveats

- **Uncalibrated levels.** The model's 500+ share (25%) is half the data's (49%), so pp and relative fits differ. F2 hits the relative 500+ share change (+9.1% vs +7.9%) but only 58% of the pp change.
- **Firm count.** F2's firm count is −8.9% against a frozen counterfactual, while the actual count was +1.4%. The model has no labour-force growth, so the frozen arm is flat where the real counterfactual was growing. Firm count is an untargeted moment.
- **No product-market interaction.** With ε = ∞, firms do not compete. Concentration here comes only from adopter scale, not from business-stealing or superstar markups (Autor et al. 2020). The GE runs add wage competition only.
- **Recession.** 2006–2010 is dominated by the Great Recession, which the model does not have. The targets therefore overstate what a technology-plus-structural model should explain. The startup rate's trough-to-2019 recovery is +0.9 pp, and the model has no cycle.
- **Definitions.**
  - Startup rate = entrants ÷ incumbents at the start of the period. BDS uses age-0 firms ÷ all firms.
  - Young = age ≤ 5 at the time of recording.
  - Window = years 11–15 after the shock (S ≈ 0.81–0.97).
- **Noise.** Across-seed standard error on the <500 share is about 0.3 pp with 24 seeds and about 0.5 pp with 8 seeds. Single-lever share responses within about ±0.7 pp of each other (§3) are not reliably ranked.
