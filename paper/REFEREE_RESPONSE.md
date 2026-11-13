# Response to the referee, round 1 (first tranche)

This tranche makes the paper honest about what the model shows and folds in the results that already exist. It does **not** contain the rebuild the report asks for. The following are **not done**: equilibrium closure, SMM calibration, cohort (pre-shock size) classification of the offset ratio, a multi-seed Monte Carlo, the cloud-era exposure estimation, and continuous-exposure empirics. Section 7.3 ("Limitations and ongoing work") lists each one.

Every number in the revised text comes from a repo file. New scripts and their outputs:

| script | output | purpose |
|---|---|---|
| `scripts/baseline_moments.py` | `data/baseline_moments.md` | pre-AI model moments vs. data, 5 seeds (concern 4) |
| `scripts/threshold_table.py` | `data/threshold_table.md` | alpha -> threshold -> share of U(2,5) below it (concern 2) |
| `scripts/normalization_cost_saving.py` | `data/normalization_cost_saving.md` | cost saving and headcount ratio by sigma under both normalizations (concern 3) |
| `scripts/bfs_revision_numbers.py` | `data/bfs_revision_numbers.md` | every BFS figure quoted from the new vintage that the existing CSVs don't already contain (concern 7) |

The paper builds with tectonic and has no undefined references or citations. The PDF is at `paper/main.pdf`. New appendix files: `paper/sections/A1-company-evidence.tex` and `paper/sections/A2-europe.tex`.

## Major concerns

**1. No equilibrium.** *Done (text only).* The abstract, introduction (P4), Section 2.4 (retitled "The fixed-wage stationary distribution"), Section 5.2 and the conclusion now say that wages are fixed, that outcomes are labor demand, and that the labor market is not closed. The free-entry condition is now described as something the fixed-wage model cannot use (Section 2.3), and every sentence implying equilibrium employment has been removed. Section 7.3 adds a "No equilibrium closure (ongoing)" item covering a finite labor-supply elasticity, downward-sloping product demand and business stealing (citing acemoglu2020competing and koch2021robots). The same two papers are also cited after Proposition 1 and in the related literature. *Remaining:* closing the model.

**2. Threshold depends on alpha.** *Done.* Proposition 1 (Section 4.2) is now stated for a general scale elasticity eta. The text derives the Hicks–Marshall decomposition d ln n / d ln r = s_a(sigma − eta), cites hamermesh1993labor, and gives eta for span of control (1/(1−alpha)), for monopolistic competition with CES demand (epsilon), and for the two combined. The proposition is presented as an application of a textbook result. Every mention of 2.78 now says "at alpha = 0.64". The new Table 2 (`tab:alpha-threshold`) gives thresholds of 2.50, 2.78, 3.33, 4.00, 5.00 and 6.67, with shares of the prior below them of 17%, 26%, 44%, 67%, 100% and 100%. Each value is checked by arithmetic in `data/threshold_table.md`, and all of them match the referee's table. atkeson2005modeling and restuccia2008policy are cited for returns to scale near 0.85, both in the introduction and in Section 4.2.

**3. sigma confounded with shock size.** *Done.* New Section 5.3, "Substitutability versus shock size: normalizing the CES", covers:
- the normalization problem (klump2000growth, leonledesma2010identifying);
- the `cost_saving` rule, equation (16), which reproduces the original specification at sigma = 3.5;
- the size of the confound: with the price fixed, the unit-cost saving is 69.7% at sigma = 1.5, 11.65% at 3.5 and 4.4% at 5 (`data/normalization_cost_saving.md`).

The normalized regime map (`paper/figures/regime_map.pdf`) is now Figure 1, the central result, and Result 1 was rewritten around it. The text states that the original plateau (−6.8%, −7.2% and −7.1% at sigma = 4, 4.5 and 5 with no entrant shift) was an artifact of the fixed price. Results from `data/monte_carlo_normalized_results.md` are in Table 5 and Section 5.4: the sigma variance share falls from 0.714 to 0.618, the entrant-shift share rises from 0.187 to 0.250, and the share of draws above zero in [4.5, 5) falls from 68% to 15%. Section 2.5 now cites luduvice2026ai (an elasticity of about 0.89 between AI capital and a high-skill labor/equipment composite, with computer investment as the AI proxy) and says that the prior support excludes complementarity by construction. *Remaining:* the AI-price and prior-reweighting checks have not been rerun under the normalization, and the paper says so.

**4. Not calibrated.** *Done.* All claims of calibration to BDS moments have been removed. Section 5.1 now begins "The model is not calibrated." `scripts/baseline_moments.py` (5 seeds, `model.calibration.simulated_moments`) feeds the new Table 4 (`tab:moments`), with model vs. data as follows:

| moment | model | data |
|---|---|---|
| entry rate | 7.3% | 8.5% |
| 500+ employment share | 25.2% | 53.0% |
| share of firms under 20 | 73.5% | 87.9% |
| mean firm size | 31.4 | 24.7 |
| Pareto exponent, 100+ | 1.28 | not sourced |
| exit rate | 7.3% | not sourced |

Data values are BDS 2019 figures from `data/cloud_era_baseline.md`. The exit-rate and tail targets are marked unsourced: the `model/calibration.py` placeholders are flagged unverified, and Axtell's exponent is fitted to the whole distribution rather than to firms with 100+ employees. Table 3 (`tab:calibration`) now lists every parameter, including the ones previously missing: exogenous exit 5%, entrant distribution N(0.75, 0.60²) against incumbents' mean 0.95, pool elasticity 0.3, potential entrants 600, sector shares and exposures, the logistic diffusion curve, the reference AI price, and kappa_f = 1. *Remaining:* SMM calibration (`calibrate()` is still a stub).

**5. Prior-predictive shares are not probabilities.** *Done.* The abstract has three numbers (0.64, 2.78, 0.29) and contains none of the old shares. The introduction, results and conclusion no longer contain 59.2%, 81.7%, 44.5% or 69.7%, and there are no confidence intervals on shares of draws. Shares appear only in the robustness subsection (5.4) and in Appendix B, labelled "share of draws under the assumed prior". The headline is now the regime map: offset fails when substitution is high and entrants are no better. The old sigma-threshold and offset-heatmap figures, which plotted "probability of offset", have been dropped from the paper. Their files remain in `paper/figures/`.

**6. Cloud analogue.** *Done.* Section 3 is retitled "Motivation" and contains facts only. The text says that the best-fitting configuration raises the employer entry cost by 20%, the opposite sign of the cloud cost cut, and that a cloud-like cut moves the startup rate by only −0.33 pp against −1.8 in the data (`data/cloud_replication_scenarios.md`, section 5). The replication is not used to set any AI prior. The section cites destefano2023cloud, karahan2024demographic and hopenhayn2022population. The unsupported claim that European concentration followed cloud adoption "with a comparable delay" has been deleted. *Remaining:* the cloud event-study estimation (Section 3.5 now labels it as not done).

**7. Thin empirics.** *Done, descriptive only.* Section 6.1 was rewritten on the November 12, 2026 vintage:
- **Headline:** event coefficient 0.296 (s.e. 0.058); permutation gap 0.288, rank 10 of 171, p = 0.058; pre-2022 ranks never above 41st; pooled DiD 0.07 with p = 0.29; monthly gap above 0.05 from March 2025, reaching 0.44 in October 2026.
- **Composition:** high-propensity applications 0.105 (s.e. 0.120), rank 46. Information alone is now about zero (0.005) rather than negative, and the text says so.
- **Growth figures:** Jan–Oct +10.9% applications, −16.5% planned-wage, +3.6% high-propensity; planned-wage share 6.8% (Information 4.7%); Jan–Sep revised to +15.0% and −15.4%; 2006–2019 +33.8% and −48.1%.

New paragraphs cover:
- **Bena et al. and Gupta et al.:** explicit positioning against bena2026prompted and gupta2026generative.
- **Rival reading:** displaced workers registering as contractors.
- **Finance:** 2026 gap −0.078 (s.e. 0.062). Adding Finance roughly halves the estimate: the 51+52+54 gap is 0.160, 0.55 times the two-sector gap, rank 121 of 969 triples, p = 0.125, computed with the existing permutation machinery extended to triples.
- **Management of companies (55):** all 9 pairs ranked above 51+54 include 55. Dropping 55, the exposed pair ranks 1 of 153, which is reported as a post hoc check.
- **Weighting:** the equal-weighted gap is 0.30 against 0.32 application-weighted.
- **Retail placebo:** 0.24 in 2025 and 0.16 in 2026, more than half of the exposed coefficient.
- **The 2020 jump:** 0.08, monthly peak 0.16 in April 2020.

Citations added: dinlersoz2024starting, decker2023surging, brynjolfsson2025canaries. All causal language has been removed. *Remaining:* continuous exposure, employer-entry outcomes. `data/bfs_causal_analysis.md` (prose) has not been regenerated, and the paper no longer cites it for numbers.

**8. Section 7 commentary.** *Done.* Section 7 is now about two pages (pp. 20–22 of the build): employment-light application firms, more firms but not more employers, limitations and ongoing work, and policy. It adds that revenue is not value added and uses kim2026ainative as the systematic evidence. The company table has moved to Appendix A, without the OpenAI row and with the Anthropic revenue labelled as derived. The Europe comparison has moved to Appendix B. It reports the share of draws with a positive effect among draws with a large-firm decline: US 61.0% and Europe 43.6% (all channels), as in `data/europe_comparison.md`. A footnote says the US run there used 1,000 draws against 2,000 in the main run.

**9. Literature.** *Done.* New subsection 1.1, "Related literature", engages hubmer2021typical, deridder2024market, aghion2023falling, decker2023surging, dinlersoz2024starting, humlum2025large, brynjolfsson2025canaries, bena2026prompted, gupta2026generative, acemoglu2020competing and koch2021robots. The claim that firm-dynamics models "have not been used" is softened to "have been used much less ... we are not aware of one that does so for AI".

## Minor comments

The brief summarizes twelve items. Item 2 is split into its three objects below, giving 14.

1. **Size classes:** one set throughout (<20, 20–499, 500+), matching the simulation (Sections 2.4, 4.4, 5.2, and Prediction 4). The 5,000 cutoff has been dropped, and the reason is stated: the model has 0–3 firms above 5,000.
2. **Task share phi:** kept as an illustration in Section 4.1 and marked as not used in any simulation.
3. **kappa_f:** marked as not used and held at 1 (after Assumption 1, and in Table 3).
4. **omega:** removed from the CES bundle. The note in Section 4.2 explains that the code uses the unweighted form.
5. **Define sigma in the cloud section:** done in Section 3.4.
6. **First-order indices sum below one:** Section 5.4 gives the sums (0.946 and 0.920) and explains that interactions decide the sign of the binary outcome.
7. **BDS label vs. years:** the text and table notes now say the BDS figures come from the 1978–2023 release, cited as bds2021. The bib entry itself was not edited, per the brief.
8. **Anthropic revenue:** labelled as derived (rev/employee × headcount) in the Appendix A table and its notes.
9. **Retail placebo:** discussed in Section 6.1 ("Placebos and the 2020 jump") and shown in Table 7.
10. **2020 jump in the BFS gap figure** (now Figure 2): discussed in the text and noted in the caption.
11. **Table 1 notes layout:** the notes are now in a parbox under the cloud table.
12. **Seminar thanks:** removed. The disclosure line has been added and the LLM-assistance note kept.
13. **Abstract number count:** three numbers.
14. **Policy opening sentence:** now opens with the finding that entry costs explain little (about 4% of variance, from Table 5).

## Discrepancy with the brief

- The brief gives the Finance (52) 2026 gap as −0.068 on Jan–Oct data against the 14 controls. I could not reproduce that figure. The paper uses what the data give:
  - −0.078 with the standard annual outcome;
  - −0.090 using Jan–Oct months in every year;

  Both are recorded in `data/bfs_revision_numbers.md`. Other variants I tried (different control sets, unadjusted counts, application weighting) did not give −0.068 either.
- All other figures in the brief were reproduced exactly.
