# Sector-Specific AI Scenarios (T8): Is Offset Sector-Dependent?

Compiled 2026-10-29. All numbers come from `python -m model.sector_analysis` (200 seeds × 3 labour-market regimes × 7 scenarios, common random numbers against a no-AI counterfactual). Full generated tables: `data/sector_analysis_tables.md`. Machine-readable output: `data/sector_analysis_results.csv` (by sector) and `data/sector_analysis_totals.csv` (economy-wide). Parameters are the uncalibrated placeholders in `model/parameters.py`, so treat magnitudes as illustrative and signs and rankings as the result.

## 0. Headline answers

1. **Offset depends on the sector, and exposure decides it.** Within a sector, net employment rises where exposure is low and falls where it is high. At baseline exposures under partial equilibrium (PE), 25–34 years after AI arrives: goods +12.0%, trade/transport +9.0%, professional services +0.5% (±0.6, break-even), information/finance **−5.2%** (±0.8). Information/finance never fully offsets, in any regime or at any horizon tested (−5% to −10%). At exposure 2.0 it loses 15–20%.
2. **Offset fails in high-exposure sectors because new firms adopt AI too.** In information/finance, AI-era entrant cohorts employ *fewer* workers than counterfactual entrants (ΔN_entrants = −308 under PE in the long run; −883 at 10–19 years), even though there are 12% more firms. Exposure ≥ 1.2 makes adoption pay from 14–23 employees, so the **5–499 band itself is where displacement happens**. The paper's Ω (band gains ÷ losses at pre-shock large firms) is then negative. In information/finance, P(Ω ≥ 1) is 1.5% (medium window) to 16% (long window).
3. **Low-exposure sectors do not concentrate.** They grow across the whole size distribution. Their 500+ employment share does not move by more than the noise (goods +0.06 pp ± 0.47). Employment concentration falls sharply in high-exposure sectors: the 500+ share drops 3–4 pp at baseline and 4.6–5.5 pp at exposure 2.0, because adopters shed labour. Output concentration (top-1% output share) rises about 1 pp wherever firms adopt. Headcount and output measures move in **opposite directions**.
4. **Labour moves from high- to low-exposure sectors, but only under general equilibrium (GE).** Under PE the sectors do not interact. Under GE, AI in professional services and information/finance raises employment in the *unexposed* sectors by **6.6–8.0 pp** beyond the entry channel, because displacement holds the wage about 2 pp below its entry-only path. With a fixed labour force, about 1.9 pp (baseline) to 3.5 pp (exposure 2.0) of total employment moves out of information/finance. At the economy level, offset comes from **cross-sector reallocation**, not from firm formation inside the exposed sectors.
5. **The model does NOT reproduce the cloud-era pattern** (Information's startup rate recovered above its 2006 level while other sectors stayed below). At baseline exposures, AI raises the startup rate by the same ~0.5 pp in every sector: the Information-minus-others difference is +0.01 pp, against +2.3 pp in the BDS. The reason is structural. In this model, exposure only scales the *displacement* channel, while the entry-cost cut and the entrant-productivity shift apply to the whole economy. The cloud pattern is the signature of a *sector-specific entry-cost* shock. Only at exposure 2.0 does a small exposure gradient in startups appear (+0.29 pp).

---

## 1. Setup

**What changes.** Only `sector_ai_exposure`, which scales AI efficiency (channel c): the price of AI services is `ai_cost_full / (S × exposure_s)`. Channels (a), the entry-cost cut from 20 to 16, and (b), the +0.05 log-point entrant-productivity shift, are **economy-wide** in the current model. Apart from exposure and entrant share, the four sectors have identical primitives. So differences *across sectors* within a scenario are caused by exposure, and differences across sectors in the `entry_only` run are pure simulation noise.

| Scenario | goods | trade_transport | professional_services | information_finance |
|---|---|---|---|---|
| baseline | 0.5 | 0.8 | 1.2 | 1.5 |
| uniform (control) | 1.0 | 1.0 | 1.0 | 1.0 |
| high_only | 0 | 0 | 1.2 | 1.5 |
| low_only | 0.5 | 0.8 | 0 | 0 |
| extreme_gradient | 0.2 | 0.8 | 1.4 | 2.0 |
| displacement_only | baseline exposure; entry cost and entrant shift switched off | | | |
| entry_only | exposure 0 everywhere; only channels (a)+(b) | | | |

**Regimes.** PE: wage fixed at 1, perfectly elastic labour supply. GE ε = 0.5: upward-sloping labour supply. GE fixed L: ε = 0, aggregate employment pinned.

**Windows.** *Medium*: years 10–19 after AI starts (diffusion S ≈ 0.73 → 1.0). *Long*: years 25–34 (S ≈ 1).

**Offset measures** (all AI minus counterfactual, averaged over the window):
- *Net*: sector employment effect ≥ 0.
- *Ω (paper, def:offset)*: ΔN^B / −ΔN^L. L = firms with 500+ employees at the last pre-AI period. B = firms with 5–499 employees then, plus post-shock entrants currently in the band. The model has very few 5,000+ firms, so the paper's 5–4,999 band is truncated at the model's large-firm threshold of 500.
- *Ω_ent*: ΔN_entrants / −ΔN_incumbents. Entrants are firms born after AI arrives; incumbents are all firms alive before.

**Why exposure matters so much.** These are closed-form results at full diffusion with σ_ai = 3.5, so the displacement condition σ > 1/(1−α) ≈ 2.78 holds. "Smallest adopter" is the non-adopter size above which the AI profit gain covers the fixed cost F_ai = 5.

| exposure | AI price r | adopter headcount ratio (c/w)^(σ−θ) | operating-profit gain | smallest adopter (employees) |
|---|---|---|---|---|
| 0.2 | 7.50 | 0.998 | +0.5% | ~1,900 |
| 0.5 | 3.00 | 0.982 | +4.5% | ~200 |
| 0.8 | 1.88 | 0.947 | +14% | ~62 |
| 1.0 | 1.50 | 0.914 | +25% | ~36 |
| 1.2 | 1.25 | 0.877 | +38% | ~23 |
| 1.5 | 1.00 | 0.819 | +64% | ~14 |
| 2.0 | 0.75 | 0.724 | +121% | ~7 |

Raising exposure does two things at once. It deepens the headcount cut at each adopter, and it pushes adoption down into the small-firm band. Displacement is therefore strongly convex in exposure.

---

## 2. Does offset occur in high-exposure sectors?

### 2.1 Net sector employment effect, baseline exposures (AI vs. no-AI, %)

| sector (exposure) | adopt % (PE, long) | PE medium | PE long | GE ε=0.5 medium | GE ε=0.5 long | fixed L medium | fixed L long |
|---|---|---|---|---|---|---|---|
| goods (0.5) | 2.5 | +3.8 | +12.0 | +6.2 | +9.6 | +5.8 | +9.2 |
| trade_transport (0.8) | 9.4 | +1.3 | +9.0 | +3.4 | +5.0 | +4.1 | +4.5 |
| professional_services (1.2) | 23.4 | −4.3 | +0.5 | −2.2 | −2.2 | −1.5 | −2.5 |
| information_finance (1.5) | 34.3 | **−10.2** | **−5.2** | −7.7 | −8.3 | −7.9 | −9.5 |

Standard errors across seeds: 0.3–0.5 pp in the medium window, 0.5–1.0 pp in the long window.

### 2.2 Extreme gradient (0.2 / 0.8 / 1.4 / 2.0)

| sector (exposure) | adopt % (PE, long) | PE medium | PE long | GE ε=0.5 medium | GE ε=0.5 long | fixed L medium | fixed L long |
|---|---|---|---|---|---|---|---|
| goods (0.2) | 0.1 | +4.6 | +13.7 | +9.5 | +12.5 | +9.6 | +13.0 |
| trade_transport (0.8) | 9.5 | +1.3 | +9.1 | +6.2 | +8.6 | +7.2 | +8.7 |
| professional_services (1.4) | 30.8 | −7.9 | −4.1 | −3.3 | −3.3 | −1.9 | −3.1 |
| information_finance (2.0) | 50.9 | **−19.7** | **−16.1** | −15.0 | −16.3 | −14.8 | −17.6 |

### 2.3 Treating one group of sectors only

PE / GE ε=0.5, %; sectors with exposure set to 0 are marked (0).

| scenario | window | goods | trade_transport | professional_services | information_finance |
|---|---|---|---|---|---|
| high_only | medium | +4.4 / +6.0 (0) | +4.2 / +5.5 (0) | −4.3 / −3.0 | −10.2 / −8.6 |
| high_only | long | +12.9 / +9.4 (0) | +12.9 / +7.9 (0) | +0.5 / −3.1 | −5.2 / −9.9 |
| low_only | medium | +3.7 / +0.9 | +1.3 / −1.6 | +4.4 / +1.5 (0) | +4.2 / +1.8 (0) |
| low_only | long | +11.8 / +1.9 | +8.7 / −0.7 | +11.8 / +3.1 (0) | +13.2 / +2.2 (0) |

Under PE, a treated sector's result is the same whether or not the other sectors are treated, because the sectors do not interact. Under GE, the untreated sectors in `high_only` gain from the lower wage (§4).

### 2.4 Channel decomposition (PE, %)

| sector (exposure) | displacement only, medium | entry only, medium | both, medium | displacement only, long | entry only, long | both, long | interaction, long |
|---|---|---|---|---|---|---|---|
| goods (0.5) | −0.6 | +4.3 | +3.8 | −0.8 | +12.7 | +12.0 | +0.1 |
| trade_transport (0.8) | −2.8 | +4.2 | +1.3 | −3.2 | +12.7 | +9.0 | −0.5 |
| professional_services (1.2) | −8.5 | +4.4 | −4.3 | −10.2 | +11.8 | +0.5 | −1.1 |
| information_finance (1.5) | −13.8 | +4.2 | −10.2 | −15.8 | +13.2 | −5.2 | −2.6 |

- **The entry channel is the same in every sector** (+4% medium, +12–13% long). Displacement scales with exposure. Offset is sector-dependent because one side of the balance is flat and the other is steep.
- **Break-even exposure** (net effect = 0): about 0.9 at 10–19 years and about 1.2 at 25–34 years under PE; about 1.0–1.1 under GE ε = 0.5. The entry stock builds slowly, while displacement arrives with diffusion, so the break-even rises with the horizon.
- **The interaction is negative and grows with exposure.** In exposed sectors, the extra entrants grow into adopters and shed labour themselves. So the entry channel offsets *less* than the entry-only run suggests: −2.6 pp in information/finance.

### 2.5 Offset ratios (PE, baseline exposures)

| sector | ΔN^L medium | ΔN^B medium | Ω medium | P(Ω≥1) medium | ΔN_inc long | ΔN_ent long | Ω_ent long |
|---|---|---|---|---|---|---|---|
| goods | −15 | +837 | 55 | 89% | −73 | +3,241 | 44 |
| trade_transport | −100 | +948 | 9.5 | 82% | −549 | +5,184 | 9.4 |
| professional_services | −264 | **−1,813** | −6.9 | 4% | −1,735 | +2,050 | 1.18 |
| information_finance | −239 | **−2,567** | −10.7 | 1.5% | −1,515 | **−308** | −0.20 |

- In the exposed sectors the **band loses about 7–11× more employment than the pre-shock large cohort**. Under this model, Ω's assumption that large firms lose and the band gains does not hold in high-exposure sectors.
- In low-exposure sectors Ω is huge only because ΔN^L is tiny. Ω is badly behaved whenever displacement at large firms is small, so read it together with the net effect.
- **Small-firm counts mislead in exposed sectors.** In information/finance, firms with fewer than 20 employees rise 18.0% while all firms rise 12.2% (PE, long). At exposure 2.0 the figures are 22.5% vs. 13.0%. Under displacement only, small firms still rise 4–5.5% with *zero* change in firm count: these are adopters shrinking below 20 employees, not new formation. Low-exposure sectors show no such gap (goods: small +11.8%, all +11.9%).

### 2.6 Economy-wide

| scenario | PE medium | PE long | GE ε=0.5 medium | GE ε=0.5 long | wage, GE ε=0.5 long |
|---|---|---|---|---|---|
| baseline | −2.56% | +3.60% | −0.34% | +0.56% | +1.11% |
| uniform (exposure 1.0) | −1.19% | +5.19% | −0.14% | +0.74% | +1.49% |
| extreme_gradient | −5.60% | +0.09% | −0.80% | +0.08% | +0.15% |
| displacement_only | −6.61% | −7.81% | −0.98% | −1.11% | −2.21% |
| entry_only | +4.32% | +12.48% | +0.69% | +1.80% | +3.63% |

**Dispersion in exposure costs jobs in aggregate.** Baseline and uniform have almost the same employment-weighted mean exposure (1.04 vs. 1.00). Yet baseline employment is 1.4 pp lower in the medium window and 1.6 pp lower in the long window, because displacement is convex in exposure. A sector-blind exposure index therefore understates aggregate displacement.

---

## 3. Do low-exposure sectors see concentration?

**No.** Changes are in pp, AI minus counterfactual, long window (s.e.).

| sector | 500+ emp. share, PE baseline | 500+ emp. share, PE extreme | 500+ emp. share, PE entry-only (noise check) | top-1% output share, PE baseline | top-1% output share, PE extreme |
|---|---|---|---|---|---|
| goods | +0.06 (0.47) | +0.84 (0.54) | +0.34 (0.46) | +0.97 (0.35) | +0.46 (0.39) |
| trade_transport | −1.29 (0.40) | −1.52 (0.41) | −0.22 (0.38) | +1.16 (0.30) | +1.04 (0.30) |
| professional_services | **−3.45** (0.39) | **−4.18** (0.37) | −0.79 (0.37) | +0.69 (0.30) | +0.56 (0.29) |
| information_finance | **−3.03** (0.55) | **−4.58** (0.51) | +0.66 (0.55) | +1.60 (0.42) | +1.27 (0.39) |

- **Low-exposure sectors grow at every size.** Firm counts rise about 12%, employment rises 9–14% under PE (5–13% under GE), and the 500+ share does not move by more than the noise. This holds even with exposure 0.2 in goods (`extreme_gradient`) or 0 (`high_only`: goods +0.56 ± 0.47, trade +0.02 ± 0.40).
- **High-exposure sectors deconcentrate in headcount.** Large adopters shed labour, so the 500+ share falls 3–5 pp. The same holds in GE: −3.1 to −5.5 pp.
- **Output concentrates wherever firms adopt.** The top-1% output share rises about 1 pp under baseline and displacement-only, but not under entry-only. Concentration measured by headcount and by output point in opposite directions in exposed sectors. Firm-size distributions measured by headcount (the BDS) would show *deconcentration* in exactly the sectors where output is concentrating.
- **The only route to concentration in a low-exposure sector is a GE wage spillover with no entry boost.** Under `displacement_only` with a fixed labour force, goods' 500+ share rises +1.24 pp (±0.41) as the wage falls 2.6%. With the entry channel on, entry-driven deconcentration more than cancels it. In GE ε = 0.5 `high_only`, goods gets +0.16 (±0.50) and trade −0.47 (±0.39), against −1.64 and −1.76 under entry only. So displacement elsewhere *slows* deconcentration in low-exposure sectors but does not reverse it.

---

## 4. Is there labour reallocation across sectors?

**Under PE, no.** The wage is fixed and each sector's entry decision depends only on its own AI price, so the sectors are independent. As a check, zero-exposure sectors in `high_only` differ from `entry_only` by +0.2 pp (s.e. ≈ 0.9). Employment shares still shift mechanically: information/finance −1.70 pp (±0.15), professional services −1.02, goods +1.22, trade +1.49. But displaced workers leave for the outside option, not for another sector.

**Under GE, yes, from high- to low-exposure sectors.**

*Spillover into zero-exposure sectors, long window.* The spillover is a sector's employment effect minus its effect under entry only.

| scenario | regime | sector | emp. effect | entry-only effect | **spillover** | wage effect |
|---|---|---|---|---|---|---|
| high_only | GE ε=0.5 | goods | +9.35% | +1.86% | **+7.50 pp** | +1.48% |
| high_only | GE ε=0.5 | trade_transport | +7.94% | +1.36% | **+6.58 pp** | +1.48% |
| high_only | fixed L | goods | +8.80% | +0.84% | **+7.97 pp** | +1.68% |
| high_only | fixed L | trade_transport | +6.96% | −0.06% | **+7.02 pp** | +1.68% |
| low_only | GE ε=0.5 | professional_services | +3.10% | +2.14% | +0.96 pp | +3.19% |
| low_only | GE ε=0.5 | information_finance | +2.16% | +1.81% | +0.35 pp | +3.19% |

*Employment shares under a fixed labour force* (pp, long window): baseline information/finance −1.88, professional services −0.86, goods +1.39, trade +1.35. Extreme gradient: −3.49, −1.08, +1.97, +2.60.

Mechanism: in exposed sectors, displacement lowers labour demand and holds the economy-wide wage about 2.1 pp below its entry-only path (+1.48% vs. +3.63%). Unexposed incumbents and entrants hire the released workers. Under GE the aggregate offset is close to complete (Ω_ent = 1.20 economy-wide at ε = 0.5 in the long window), but it is built in goods and trade/transport, while information/finance stays 8–10% below its counterfactual. The reverse spillover (`low_only`) is small, because low exposure displaces little.

---

## 5. Cloud-era comparison

Evidence (`data/cloud_era_baseline.md` §2.4, BDS, startup-rate change 2006 → 2019): Information (51) **+0.7 pp**; professional services (54) −1.9; retail (44–45) −2.2; manufacturing (31–33) −0.8. Information minus the mean of the others: **+2.3 pp**. The model's sectors map roughly onto these (information_finance ≈ 51+52, professional_services ≈ 54, trade_transport ≈ 44–45 + 48–49, goods ≈ 31–33).

| | goods | trade_transport | professional_services | information_finance | info − others |
|---|---|---|---|---|---|
| BDS 2019 vs. 2006 (pp) | −0.8 (mfg) | −2.2 (retail) | −1.9 | **+0.7** | **+2.3** |
| Model, baseline, PE, AI−CF long (pp) | 0.51 | 0.49 | 0.48 | 0.50 | **+0.01** |
| Model, extreme, PE, AI−CF long (pp) | 0.50 | 0.49 | 0.48 | 0.78 | +0.29 |
| Model, extreme, GE ε=0.5 (pp) | 0.45 | 0.46 | 0.45 | 0.71 | +0.26 |
| Model, displacement only, PE (pp) | 0.00 | 0.01 | −0.01 | 0.02 | +0.02 |
| Model, baseline, peak transition gap (pp, yr 12–15) | 0.96 | 0.97 | 0.97 | 0.97 | 0.00 |

Standard errors on the model startup gaps are 0.01–0.02 pp.

**The model does not reproduce the pattern.**
- *Levels*: every model sector ends above its pre-AI startup rate (7.39–7.40% → 7.86–7.91%). In the cloud data only Information did. The model has no common headwind (2007–09 recession, secular decline in dynamism), so it cannot produce "others stayed below".
- *Cross-section*: the startup response is flat across sectors at baseline exposures. Exposure feeds into entry only through the expected value of later adopting AI, which matters for marginal entrants only once adoption pays at very small sizes (exposure ≈ 2, threshold about 7 employees). Even then the gap (+0.29 pp) is about an eighth of the BDS gap.
- *Why*: in the model, exposure is a **displacement** parameter: it substitutes AI for labour inside firms. The cloud-era sector evidence is the footprint of an **entry-cost** shock concentrated where IT was the main input. That is the channel Ewens, Nanda & Rhodes-Kropf (2018) identify. The model's entry-cost cut is economy-wide. As specified, the model predicts *uniform entry, concentrated displacement*. The cloud era looked like *concentrated entry*.
- *Implication*: if AI's entry-cost reduction is also concentrated in exposed sectors, as the cloud analogy suggests, offset *within* professional services and information/finance would be stronger than reported here, and weaker in goods and trade. The sector results in §2 are a lower bound on within-sector offset in exposed sectors, and an upper bound in unexposed ones.

---

## 6. Implications for the paper

1. **Report offset by sector, not just economy-wide.** The aggregate result (PE long +3.6%) sums sectors that move in opposite directions (+12% vs. −5%). A single Ω hides that information/finance never offsets.
2. **Re-specify Ω for exposed sectors.** When exposure is 1.2 or more, adoption starts at 14–23 employees, so the 5–499 band is where displacement happens (ΔN^B < 0). Use an adopter vs. non-adopter split or an entry-cohort split (Ω_ent) alongside the size-class definition.
3. **Empirical signatures (§6 of the paper): avoid size-class counts in exposed sectors.** In information/finance, small-firm counts rise about 6 pp faster than firm counts because adopters shrink into the small class. Firm age or entry cohort identifies formation; size class does not. Output-based size measures move the opposite way from headcount-based ones.
4. **Add a sector-indexed entry-cost channel** before running the cloud-era replication, e.g. `entry_cost_post_s = entry_cost_pre × (1 − κ × exposure_s)`. Calibrate κ to the BDS information-minus-others startup difference (+2.3 pp). The uniform 20% cut used here moves startup rates by only about 0.5 pp in the long run (about 1 pp at the peak), so matching the BDS gap needs a much larger sector-specific cut or a more elastic entry margin (`entry_pool_elasticity`).
5. **GE matters for the sector story.** Cross-sector reallocation through the wage is what makes the aggregate GE offset near-complete. That makes the labour-supply elasticity a first-order parameter for *where* jobs land, not just *how many* there are.

## 7. Caveats

- Parameters are uncalibrated placeholders. σ_ai = 3.5 sits on the displacement side of the threshold (θ ≈ 2.78). With σ_ai < θ, adopters grow and the exposure ranking of employment effects reverses.
- Common random numbers hold for incumbents but break for entrants: entrant counts differ between runs, firm ids shift, and so do their later shocks. This is why the noise is non-trivial, why 200 seeds were used, and why standard errors are reported. The `entry_only` cross-sector spread (500+ share ±0.8 pp) gives the noise floor for share measures.
- The pre-shock 500+ cohort is small (4–16 firms per sector) and decays over 25–34 years through 5% exogenous exit and mean reversion. Ω is therefore read in the medium window, and the net effect and Ω_ent are preferred in the long window.
- Entrants assume today's prices persist, and the entry value takes the adoption max at the expected productivity path (`firm_dynamics.entry_value`). Both understate the value of later adoption, which is the channel that would create an exposure gradient in startups.

## 8. Reproduction

```bash
cd ~/.kiro/crew/workspace-member-playecon
PYTHONPATH=. .venv/bin/python -m model.sector_analysis   # ~6 min on 6 workers; writes data/sector_analysis_{results,totals}.csv and _tables.md
.venv/bin/python -m pytest tests/test_sector_analysis.py -q
```

Code: `model/sector_analysis.py` (scenario definitions in `EXPOSURE_SCENARIOS` / `CHANNEL_SCENARIOS`, regimes in `LABOR_REGIMES`). Only `sector_ai_exposure` and, for the decomposition, `entry_cost_post` / `ai_entrant_productivity_shift` are changed, all via `Parameters.with_updates()`. The core model files are unchanged.
