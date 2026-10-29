# BFS causal analysis: pre-trends, placebos and permutation inference

Companion to `data/ai_era_startups_2023_2026.md` §3 and paper Section 6 (`paper/sections/06-empirical-signatures.tex`).
All numbers are **[C]**: computed by us from the official Census file. Reproducible with:

```
.venv/bin/python scripts/bfs_causal_analysis.py data/bfs_raw/bfs_monthly.csv
```

- **Source:** Census Business Formation Statistics, [bfs_monthly.csv](https://www.census.gov/econ/bfs/csv/bfs_monthly.csv), downloaded 2026-10-29 to `data/bfs_raw/bfs_monthly.csv`. Data run through September 2026.
- **Filters:** `geo=US`, `sa=A` (seasonally adjusted), 19 NAICS sectors. `TOTAL` and `NONAICS` are dropped.
- **Outcomes:** `BA_BA` (all business applications) and `BA_HBA` (high-propensity applications, i.e. likely employers).
- **Annual outcome:** log of the mean monthly SA count. 2026 = Jan–Sep. A Jan–Sep-only robustness check for every year gives the same results (Table 2).
- **Treated:** Information (NAICS 51) and Professional, scientific & technical services (NAICS 54). These are the two high-exposure sectors where AI-native firms register (`ai_era_startups_2023_2026.md` §3.3).
- **Placebo:** Construction (23) and Retail (44–45). These are low-exposure sectors (exposure 0.28 in Section 6).
- **Controls:** the other 15 sectors (51, 54, 23 and Retail are excluded from controls in every design).
- **Outputs:** `data/bfs_causal_results.csv`, `data/bfs_event_study.csv`, `data/bfs_perm_by_year_{BA_BA,BA_HBA}.csv`, `data/bfs_permutation_*.csv`, `data/bfs_sector_league_*.csv`, `data/bfs_monthly_gap.csv`. Figures are in `paper/figures/bfs_{event_study,monthly_gap,indices}.pdf`, with PNG copies in `data/`.

## Headline

1. **Pre-trends pass.** From 2010 to 2022, applications in 51+54 tracked the other 15 sectors.
   - The differential linear trend is **−0.26% per year** (SE 0.010), so it is not distinguishable from zero.
   - Every 2015–2021 event coefficient lies in [−0.01, +0.085] log points.
   - In each pre-year, the 51+54 gap ranks between 40th and 80th of the 171 possible sector pairs, which is mid-distribution.
   - A fake shock in 2016, estimated on pre-COVID data from 2010–2019, gives **−0.001** (SE 0.053).
2. **The divergence is real but late.** Nothing happens in 2023 (−0.03) or 2024 (+0.00).
   - The 51+54 gap opens in **March 2025** and rises almost monotonically to **+0.34 log points (≈ +41%) by September 2026**.
   - The 2026 event coefficient is **+0.29** (cluster SE 0.059). It ranks **10th of 171** sector pairs, a one-sided permutation p of 0.058.
3. **The Construction placebo is clean.** Its event coefficients for 2023–2026 are −0.006, −0.004, −0.008 and +0.005. Its monthly gap stays within ±0.04 throughout 2025–26.
4. **Retail is not a clean placebo.** It has a strong upward pre-trend (+3.8% per year relative to controls, driven by the 2020–21 e-commerce wave). After 2024 it also shows large, erratic one-month spikes (+0.51 in Sep 2025 and Jul 2026, back to −0.06 in Feb 2026). It is a noisy series with a different mechanism, not a smooth diffusion path. Pooling Retail with Construction makes the combined "placebo" DiD positive. The paper should use Construction alone as the placebo and report Retail transparently.
5. **The surge is in low-propensity applications.** On high-propensity (likely-employer) applications, 51+54 has a 2026 event coefficient of only +0.12 (SE 0.12; permutation gap +0.10, rank 48/171), and Information alone is *negative* (−0.157 pooled DiD). The AI-sector entry response is concentrated among applicants unlikely to hire. That fits Prediction 3 (entrant size falls) and the nonemployer-margin story in `cloud_era_baseline.md`. It does not yet show employer entry.
6. **A pooled 2023–2026 DiD is not significant** (+0.063, SE 0.070; permutation p = 0.32). This is because 2023–24 show no effect. Any claim must be framed around the 2025–26 onset, and that timing was observed, not pre-registered (see caveats).

## Table 1. Event study, log SA business applications (all), relative to 2022

Two-way FE (sector, year). SEs are clustered by sector (CR1, 17 clusters). Coefficient = treated − control log gap, normalised to 2022.

| Year | 51+54 | (SE) | Information 51 | Professional 54 | Construction 23 | Retail 44–45 |
|---|---|---|---|---|---|---|
| 2015 | 0.020 | (0.072) | −0.009 | 0.048 | −0.068 | −0.346 |
| 2016 | 0.039 | (0.067) | 0.017 | 0.061 | −0.024 | −0.289 |
| 2017 | 0.059 | (0.067) | 0.088 | 0.030 | 0.012 | −0.273 |
| 2018 | 0.018 | (0.063) | 0.018 | 0.018 | 0.007 | −0.287 |
| 2019 | 0.033 | (0.049) | 0.032 | 0.035 | 0.055 | −0.192 |
| 2020 | 0.085 | (0.055) | 0.132 | 0.038 | −0.024 | 0.132 |
| 2021 | 0.020 | (0.045) | 0.068 | −0.029 | −0.031 | 0.086 |
| 2022 | 0 | — | 0 | 0 | 0 | 0 |
| 2023 | −0.032 | (0.044) | −0.067 | 0.003 | −0.006 | 0.019 |
| 2024 | 0.003 | (0.052) | −0.034 | 0.040 | −0.004 | 0.022 |
| 2025 | 0.126 | (0.065) | 0.071 | 0.180 | −0.008 | 0.256 |
| **2026** | **0.292** | **(0.059)** | **0.279** | **0.305** | **0.005** | 0.187 |

Single-sector columns use the same 15-sector control group. With one treated cluster, CR1 SEs are unreliable (Conley & Taber 2011), so inference for single sectors relies on the permutation ranks below.

## Table 2. Summary tests

| Design | Pre-trend slope, 2010–22 (per yr) | Pooled DiD 2023–26 vs 2015–22 | Excl. 2020–21 from pre | Fake 2016 shock (2010–19) |
|---|---|---|---|---|
| **All applications (BA_BA)** | | | | |
| 51+54 | −0.0026 (0.010) | 0.063 (0.070) | 0.069 (0.072) | −0.001 (0.053) |
| 51+54, Jan–Sep only | −0.0031 (0.010) | 0.061 (0.072) | — | — |
| Information (51) | 0.0020 | 0.019 | 0.038 | 0.024 |
| Professional (54) | −0.0072 | 0.107 | 0.100 | −0.026 |
| Placebo: Construction (23) | 0.0226 | **0.006** | 0.000 | 0.189 |
| Placebo: Retail (44–45) | 0.0381 | 0.267 | 0.352 | 0.093 |
| Placebo: 23+Retail | 0.0304 (0.011) | 0.137 (0.119) | 0.176 (0.155) | 0.141 (0.063) |
| **High-propensity applications (BA_HBA)** | | | | |
| 51+54 | −0.0021 (0.010) | −0.037 (0.113) | −0.038 (0.120) | 0.020 (0.058) |
| Information (51) | −0.0016 | −0.135 | −0.138 | 0.057 |
| Professional (54) | −0.0025 | 0.062 | 0.062 | −0.018 |
| Placebo: 23+Retail | 0.0293 (0.012) | 0.170 (0.083) | 0.205 (0.095) | 0.122 (0.119) |

The placebo sectors' positive pre-trend (+2–4% per year) reflects Construction's and Retail's post-GFC and e-commerce recoveries. Their fake-2016 DiD is positive for the same reason. On every pre-trend test, 51+54 is the *cleaner* comparison.

## Table 3. Permutation inference: rank of each year's gap among all 171 sector pairs (all applications)

Each of the C(19,2) = 171 sector pairs is treated in turn against the other 17 sectors. Rank 1 = largest positive gap relative to 2022.

| Year | 51+54 gap | Rank /171 | 23+Retail gap | Rank /171 |
|---|---|---|---|---|
| 2015 | 0.044 | 67 | −0.209 | 154 |
| 2017 | 0.075 | 56 | −0.138 | 136 |
| 2019 | 0.042 | 71 | −0.072 | 127 |
| 2020 | 0.079 | 40 | 0.044 | 59 |
| 2021 | 0.016 | 80 | 0.025 | 62 |
| 2023 | −0.033 | 119 | 0.011 | 53 |
| 2024 | 0.002 | 76 | 0.008 | 71 |
| 2025 | 0.111 | 29 | 0.109 | 33 |
| **2026** | **0.280** | **10** (p = 0.058) | 0.062 | 55 |

- **Pooled 2023–26 DiD:** 51+54 ranks 55/171 (p = 0.32). The two-sided permutation p for the 51+54 pre-trend slope is 0.72.
- **Top single sectors by pooled DiD:** Management of companies (55) and Utilities (22). These are the two smallest series (≈ 0.6k–6k applications per month) and the noisiest. Professional services (54) ranks 4th of 19 by pooled DiD, behind those two and Retail.

## Table 4. Monthly gap, 51+54 vs other 15 sectors (log, 2022 mean = 0)

| | Mar | Jun | Sep | Dec |
|---|---|---|---|---|
| 2023 | 0.019 | −0.036 | −0.041 | −0.102 |
| 2024 | −0.025 | 0.025 | 0.063 | 0.016 |
| 2025 | 0.067 | 0.125 | 0.136 | 0.261 |
| 2026 | 0.271 | 0.334 | 0.344 | — |

Construction over the same months stays within [−0.04, +0.04] in 2025–26. Full series: `data/bfs_monthly_gap.csv`. Figure: `paper/figures/bfs_monthly_gap.pdf`.

## Interpretation for the paper

- **What this supports.**
  - Pre-trends for the AI-exposed sectors are flat for over a decade. That rules out the most common objection, that 51/54 were already on a faster entry trajectory.
  - The 2025–26 divergence is large (+0.29 to +0.34 log points), smooth, and growing. It is absent in the cleanest low-exposure placebo (Construction).
  - It ranks in the top 6% of all sector-pair gaps for 2026.
- **What this does not support.**
  1. **A response to the late-2022 ChatGPT release itself.** The data show no differential entry in 2023–24. If the shock is dated to the arrival of capable AI coding and agent tools in 2025, the timing fits a diffusion lag. But that dating was chosen after seeing the data, so it is not a pre-registered test.
  2. **Employer entry.** High-propensity applications do not diverge significantly. The response sits on the low-propensity, likely-nonemployer margin.
  3. **A clean exposure gradient.** Finance (NAICS 52, exposure 0.78) has a *negative* pooled DiD (−0.165). Exposure alone does not predict entry; sectors where a solo founder can ship a software or service product appear to drive the effect.
- **Caveats.**
  - Only two treated sectors and 17 controls; cluster-robust SEs with few treated clusters over-reject, so the permutation ranks are the preferred inference.
  - The 2026 figures are Jan–Sep.
  - BFS sector codes are self-reported on the SS-4.
  - Applications are not firms: BF4Q/BF8Q conversions for 2023+ cohorts are not yet released.
