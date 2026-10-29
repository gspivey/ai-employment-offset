"""T6: Monte Carlo uncertainty quantification of the AI employment offset.

Draws the four AI-shock parameters below independently, runs the AI scenario
and the no-AI counterfactual for each draw (common random numbers, see
``model.simulation``), and records AI-vs-counterfactual effects over the last
``eval_window`` periods. Other parameters stay at ``Parameters()`` defaults
(partial equilibrium: perfectly elastic labour supply, so wages do not move).

Priors
    sigma_ai                       U(2, 5)
    entry_cost_post                entry_cost_pre * U(0.7, 1.0)   (0-30% cut)
    ai_entrant_productivity_shift  U(0, 0.15)
    ai_adoption_fixed_cost         U(2, 10)

Outputs
    data/monte_carlo_raw.csv     one row per replication (draws + outcomes)
    data/monte_carlo_noise.csv   fixed-parameter replications (simulation noise)
    data/monte_carlo_results.md  summary, probabilities, sensitivity

Usage
    .venv/bin/python scripts/monte_carlo_t6.py [--n 2000] [--jobs 6] [--seed 2026]
    .venv/bin/python scripts/monte_carlo_t6.py --analyze-only
"""

from __future__ import annotations

import argparse
import math
import sys
import time
from concurrent.futures import ProcessPoolExecutor
from itertools import combinations_with_replacement
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from model import ParameterUncertainty, Parameters, compare_scenarios, employment_effects  # noqa: E402
from model.simulation import size_class_columns  # noqa: E402

DATA = ROOT / "data"
RAW_CSV = DATA / "monte_carlo_raw.csv"
NOISE_CSV = DATA / "monte_carlo_noise.csv"
REPORT_MD = DATA / "monte_carlo_results.md"

PARAMS = ["sigma_ai", "entry_cost_reduction", "ai_entrant_productivity_shift", "ai_adoption_fixed_cost"]
PARAM_LABELS = {
    "sigma_ai": "sigma_ai (labour-AI substitution)",
    "entry_cost_reduction": "entry-cost reduction (1 - post/pre)",
    "ai_entrant_productivity_shift": "AI entrant productivity shift",
    "ai_adoption_fixed_cost": "AI adoption fixed cost",
}
OUTCOMES = [
    "net_employment_effect",
    "small_firm_employment_effect",
    "mid_firm_employment_effect",
    "large_firm_employment_effect",
    "firm_count_effect",
    "small_firm_count_effect",
    "mean_firm_size_effect",
    "output_effect",
    "entry_rate_change",
    "adoption_rate",
    "adopter_employment_share",
    "offset_ratio_proxy",
]
STRONG_OFFSET = 0.05
EVAL_WINDOW = 10


def study_uncertainty(base: Parameters) -> ParameterUncertainty:
    pre = base.entry_cost_pre
    return ParameterUncertainty(
        {
            "sigma_ai": stats.uniform(loc=2.0, scale=3.0),
            "entry_cost_post": stats.uniform(loc=0.7 * pre, scale=0.3 * pre),
            "ai_entrant_productivity_shift": stats.uniform(loc=0.0, scale=0.15),
            "ai_adoption_fixed_cost": stats.uniform(loc=2.0, scale=8.0),
        }
    )


# ---------------------------------------------------------------------------
# Simulation
# ---------------------------------------------------------------------------


def replicate(task) -> dict:
    rep, params, seed, window = task
    ai, cf = compare_scenarios(params, seed=int(seed))
    out = employment_effects(ai, cf, params, window=window)
    a, c = ai.iloc[-window:], cf.iloc[-window:]
    small, large = size_class_columns(params)
    mid = [lab for lab in params.size_bucket_labels() if lab not in small and lab not in large]

    def level(df, labels):
        return float(df[[f"emp_{lab}" for lab in labels]].sum(axis=1).mean())

    for name, labels in (("small", small), ("mid", mid), ("large", large)):
        out[f"emp_{name}_ai"] = level(a, labels)
        out[f"emp_{name}_cf"] = level(c, labels)
    out["employment_ai"] = float(a["aggregate_employment"].mean())
    out["employment_cf"] = float(c["aggregate_employment"].mean())
    out["mid_firm_employment_effect"] = out["emp_mid_ai"] / out["emp_mid_cf"] - 1.0
    # Size-bucket proxy for the paper's Omega: employment change in firms
    # currently < 500 over the loss in firms currently >= 500 (not cohort-based).
    d_large = out["emp_large_ai"] - out["emp_large_cf"]
    d_band = (out["emp_small_ai"] + out["emp_mid_ai"]) - (out["emp_small_cf"] + out["emp_mid_cf"])
    out["offset_ratio_proxy"] = d_band / -d_large if d_large < 0 else np.nan
    out["replication"] = rep
    return out


def run(draws: list, base: Parameters, seeds: np.ndarray, jobs: int, label: str) -> pd.DataFrame:
    tasks = [(i, base.with_updates(**d), seeds[i], EVAL_WINDOW) for i, d in enumerate(draws)]
    t0 = time.time()
    rows = []
    with ProcessPoolExecutor(max_workers=jobs) as pool:
        for k, r in enumerate(pool.map(replicate, tasks, chunksize=4), 1):
            rows.append(r)
            if k % 250 == 0 or k == len(tasks):
                print(f"[{label}] {k}/{len(tasks)} done, {time.time() - t0:.0f}s", flush=True)
    out = pd.DataFrame(rows).set_index("replication").sort_index()
    inputs = pd.DataFrame(draws, index=out.index)
    out = pd.concat([inputs, out], axis=1)
    out.insert(0, "seed", seeds[: len(draws)])
    return out


def simulate(n: int, noise_n: int, seed: int, jobs: int) -> tuple:
    base = Parameters()
    unc = study_uncertainty(base)
    param_rng = np.random.default_rng(np.random.SeedSequence(seed).spawn(1)[0])
    sim_seeds = np.random.SeedSequence(seed).generate_state(n, dtype=np.uint32)
    draws = [unc.draw(param_rng) for _ in range(n)]
    df = run(draws, base, sim_seeds, jobs, "main")
    df.insert(df.columns.get_loc("entry_cost_post") + 1, "entry_cost_reduction", 1.0 - df["entry_cost_post"] / base.entry_cost_pre)
    df["offset"] = df["net_employment_effect"] > 0
    df["strong_offset"] = df["net_employment_effect"] > STRONG_OFFSET
    df["concentration"] = df["small_firm_employment_effect"] < 0

    noise_seeds = np.random.SeedSequence([seed, 1]).generate_state(noise_n, dtype=np.uint32)
    noise = run([{} for _ in range(noise_n)], base, noise_seeds, jobs, "noise")
    return df, noise


# ---------------------------------------------------------------------------
# Analysis
# ---------------------------------------------------------------------------


def wilson(k: int, n: int, z: float = 1.96) -> tuple:
    p = k / n
    d = 1 + z**2 / n
    centre = (p + z**2 / (2 * n)) / d
    half = z * math.sqrt(p * (1 - p) / n + z**2 / (4 * n**2)) / d
    return centre - half, centre + half


def derive(df: pd.DataFrame) -> pd.DataFrame:
    """Add regime and share-based columns computed from the stored levels."""
    df = df.copy()
    df["large_share_change"] = df["emp_large_ai"] / df["employment_ai"] - df["emp_large_cf"] / df["employment_cf"]
    df["share_concentration"] = df["large_share_change"] > 0
    df["displacement"] = df["large_firm_employment_effect"] < 0
    df["regime"] = np.select(
        [~df["displacement"], df["offset"]],
        ["no large-firm displacement", "displacement, offset"],
        "displacement, no offset",
    )
    return df


def prob_table(df: pd.DataFrame) -> pd.DataFrame:
    events = {
        "P(offset): net employment effect > 0": df["offset"],
        f"P(strong offset): net employment effect > {STRONG_OFFSET:.0%}": df["strong_offset"],
        "P(concentration): small-firm (<20) employment effect < 0": df["concentration"],
        "P(share concentration): 500+ share of employment rises": df["share_concentration"],
        "P(net employment effect < -5%)": df["net_employment_effect"] < -0.05,
        "P(large-firm (500+) employment falls)": df["displacement"],
        "P(offset | large-firm employment falls)": df.loc[df["displacement"], "offset"],
        "P(mid-size (20-499) employment rises)": df["mid_firm_employment_effect"] > 0,
        "P(more firms): firm count effect > 0": df["firm_count_effect"] > 0,
    }
    rows = []
    for name, mask in events.items():
        n = len(mask)
        k = int(mask.sum())
        p = k / n
        lo, hi = wilson(k, n)
        rows.append({"event": name, "probability": p, "mc_se": math.sqrt(p * (1 - p) / n), "ci95_lo": lo, "ci95_hi": hi, "n": n})
    return pd.DataFrame(rows).set_index("event")


def summary_table(df: pd.DataFrame) -> pd.DataFrame:
    out = df[OUTCOMES]
    t = pd.DataFrame({"mean": out.mean(), "mc_se_mean": out.std(ddof=1) / np.sqrt(out.notna().sum()), "sd": out.std(ddof=1)})
    for p in (5, 25, 50, 75, 95):
        t[f"p{p}"] = out.quantile(p / 100)
    t["n"] = out.notna().sum()
    return t


def first_order_index(x: np.ndarray, y: np.ndarray, bins: int = 20) -> float:
    """Bias-adjusted correlation ratio (epsilon^2) of y on quantile bins of x.

    Estimates the first-order Sobol index Var(E[y|x]) / Var(y).
    """
    q = pd.qcut(x, bins, labels=False, duplicates="drop")
    g = pd.Series(y).groupby(q)
    k = g.ngroups
    n = len(y)
    ss_tot = ((y - y.mean()) ** 2).sum()
    ss_between = (g.count() * (g.mean() - y.mean()) ** 2).sum()
    ms_within = (ss_tot - ss_between) / (n - k)
    return float((ss_between - (k - 1) * ms_within) / ss_tot)


def ols_r2(X: np.ndarray, y: np.ndarray) -> tuple:
    X1 = np.column_stack([np.ones(len(y)), X])
    beta, *_ = np.linalg.lstsq(X1, y, rcond=None)
    resid = y - X1 @ beta
    return beta, 1.0 - resid.var() / y.var()


def smoothed_offset(df: pd.DataFrame, degree: int = 4) -> tuple:
    """P(offset) with simulation noise smoothed out by a polynomial response surface.

    Fits the net effect on all monomials of the standardised parameters up to
    ``degree``; returns (share of fitted values > 0, R^2, residual SD).
    """
    Z = ((df[PARAMS] - df[PARAMS].mean()) / df[PARAMS].std()).to_numpy()
    y = df["net_employment_effect"].to_numpy()
    cols = [np.prod(Z[:, list(c)], axis=1) for k in range(1, degree + 1) for c in combinations_with_replacement(range(Z.shape[1]), k)]
    X = np.column_stack([np.ones(len(y))] + cols)
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    fit = X @ beta
    return float((fit > 0).mean()), 1.0 - (y - fit).var() / y.var(), float((y - fit).std())


def sensitivity(df: pd.DataFrame, outcome: str) -> tuple:
    d = df[PARAMS + [outcome]].dropna()
    y = d[outcome].to_numpy()
    Z = ((d[PARAMS] - d[PARAMS].mean()) / d[PARAMS].std(ddof=0)).to_numpy()
    beta, r2_lin = ols_r2(Z, y / y.std())
    # full quadratic (squares + pairwise interactions) response surface
    cols = [Z] + [Z[:, [i]] * Z[:, [j]] for i in range(Z.shape[1]) for j in range(i, Z.shape[1])]
    _, r2_quad = ols_r2(np.hstack(cols), y)
    rows = []
    for i, p in enumerate(PARAMS):
        rows.append(
            {
                "parameter": PARAM_LABELS[p],
                "spearman_rho": stats.spearmanr(d[p], y).statistic,
                "src": beta[i + 1],
                "src_sq": beta[i + 1] ** 2,
                "first_order_S1": first_order_index(d[p].to_numpy(), y),
            }
        )
    t = pd.DataFrame(rows).set_index("parameter").sort_values("first_order_S1", ascending=False)
    return t, r2_lin, r2_quad


def sigma_bins(df: pd.DataFrame, width: float = 0.25) -> pd.DataFrame:
    edges = np.round(np.arange(2.0, 5.0 + width / 2, width), 4)
    b = pd.cut(df["sigma_ai"], edges, include_lowest=True)
    g = df.groupby(b, observed=True)
    t = pd.DataFrame(
        {
            "n": g.size(),
            "net_mean": g["net_employment_effect"].mean(),
            "net_p5": g["net_employment_effect"].quantile(0.05),
            "net_p50": g["net_employment_effect"].median(),
            "net_p95": g["net_employment_effect"].quantile(0.95),
            "P_offset": g["offset"].mean(),
            "P_strong": g["strong_offset"].mean(),
            "P_concentration": g["concentration"].mean(),
            "P_share_conc": g["share_concentration"].mean(),
            "P_large_falls": g["displacement"].mean(),
            "small_mean": g["small_firm_employment_effect"].mean(),
            "large_mean": g["large_firm_employment_effect"].mean(),
            "adoption": g["adoption_rate"].mean(),
        }
    )
    t.index = [f"[{iv.left:.2f}, {iv.right:.2f}]" for iv in t.index]
    t["mid"] = [(iv.left + iv.right) / 2 for iv in g.size().index]
    return t


def crossing(x: np.ndarray, y: np.ndarray, level: float) -> float:
    """First x at which the piecewise-linear y crosses ``level`` (nan if none)."""
    for i in range(len(x) - 1):
        if (y[i] - level) * (y[i + 1] - level) <= 0 and y[i] != y[i + 1]:
            return float(x[i] + (level - y[i]) * (x[i + 1] - x[i]) / (y[i + 1] - y[i]))
    return float("nan")


def two_way(df: pd.DataFrame, other: str, event: str = "offset") -> pd.DataFrame:
    sb = pd.cut(df["sigma_ai"], np.arange(2.0, 5.01, 0.5), include_lowest=True)
    ob = pd.qcut(df[other], 3)
    t = df.groupby([sb, ob], observed=True)[event].mean().unstack()
    t.index = [f"sigma [{iv.left:.1f}, {iv.right:.1f}]" for iv in t.index]
    fmt = (lambda v: f"{v:.0%}") if other == "entry_cost_reduction" else (lambda v: f"{v:.3f}" if abs(v) < 1 else f"{v:.1f}")
    t.columns = [f"{other} {fmt(max(iv.left, df[other].min()))}-{fmt(iv.right)}" for iv in t.columns]
    return t


# ---------------------------------------------------------------------------
# Report
# ---------------------------------------------------------------------------


def md_table(t: pd.DataFrame, fmt: dict | None = None, index_name: str = "") -> str:
    fmt = fmt or {}
    cols = list(t.columns)
    lines = ["| " + " | ".join([index_name] + cols) + " |", "|" + "---|" * (len(cols) + 1)]
    for idx, row in t.iterrows():
        cells = []
        for c in cols:
            v = row[c]
            f = fmt.get(c, "{:.4f}")
            cells.append("n/a" if isinstance(v, float) and not np.isfinite(v) else (f(v) if callable(f) else f.format(v)))
        lines.append("| " + " | ".join([str(idx).replace("|", "\\|")] + cells) + " |")
    return "\n".join(lines)


pct = "{:+.2%}".format
pct0 = "{:.1%}".format


def s1(v: float) -> str:
    """First-order index as text; bias adjustment can push ~0 slightly negative."""
    return "<1%" if v < 0.005 else f"{v:.0%}"


def report(df: pd.DataFrame, noise: pd.DataFrame, seed: int, runtime: float | None) -> str:
    base = Parameters()
    df = derive(df)
    n = len(df)
    probs = prob_table(df)
    summ = summary_table(df)
    sens = {o: sensitivity(df, o) for o in ("net_employment_effect", "small_firm_employment_effect", "large_firm_employment_effect")}
    sb = sigma_bins(df)
    sig0_mean = crossing(sb["mid"].to_numpy(), sb["net_mean"].to_numpy(), 0.0)
    sig0_p50 = crossing(sb["mid"].to_numpy(), sb["P_offset"].to_numpy(), 0.5)

    net = df["net_employment_effect"]
    var_total = net.var()
    var_noise = noise["net_employment_effect"].var()
    s_net, r2_lin, r2_quad = sens["net_employment_effect"]
    top, second = s_net.index[0], s_net.index[1]
    second_key = {v: k for k, v in PARAM_LABELS.items()}[second]

    joint = pd.crosstab(
        df["offset"].map({True: "offset (net > 0)", False: "no offset (net <= 0)"}),
        df["concentration"].map({True: "concentration (small < 0)", False: "small-firm growth (small >= 0)"}),
        normalize=True,
    )

    conv = pd.DataFrame(
        {
            "N": [m for m in (250, 500, 1000, n) if m <= n],
        }
    )
    conv["P(offset)"] = [df["offset"].iloc[:m].mean() for m in conv["N"]]
    conv["P(strong)"] = [df["strong_offset"].iloc[:m].mean() for m in conv["N"]]
    conv["P(concentration)"] = [df["concentration"].iloc[:m].mean() for m in conv["N"]]
    conv["mean net"] = [net.iloc[:m].mean() for m in conv["N"]]
    conv = conv.drop_duplicates("N").set_index("N")

    inputs = df[PARAMS + ["entry_cost_post"]].describe().T[["min", "mean", "max"]]

    lo_sig = df[df["sigma_ai"] < base.displacement_threshold]
    hi_sig = df[df["sigma_ai"] >= base.displacement_threshold]

    L = []
    L.append("# T6: Monte Carlo Uncertainty Quantification -- AI Offset vs Concentration\n")
    L.append(
        f"Generated by `scripts/monte_carlo_t6.py` (seed {seed}). Every number below is computed from "
        "`data/monte_carlo_raw.csv`; rerun with `--analyze-only` to regenerate this file without re-simulating.\n"
    )
    L.append("## Design\n")
    L.append(
        f"- **Replications:** N = {n:,} parameter draws, each an AI run and a no-AI counterfactual from the same "
        f"burned-in economy and seed (common random numbers). {len(noise)} extra replications at fixed default "
        "parameters measure pure simulation noise."
        + (f" Wall time {runtime / 60:.1f} min." if runtime else "")
    )
    L.append(
        f"- **Outcomes:** AI-vs-counterfactual proportional differences averaged over the last {EVAL_WINDOW} of "
        f"{base.n_periods} periods (AI starts at period {base.ai_start_period}; diffusion S > 0.99 throughout the window)."
    )
    L.append(
        "- **Priors (independent):** sigma_ai ~ U(2, 5); entry_cost_post = entry_cost_pre x U(0.7, 1.0) "
        f"(entry_cost_pre = {base.entry_cost_pre:g}, so a 0-30% cut); ai_entrant_productivity_shift ~ U(0, 0.15); "
        "ai_adoption_fixed_cost ~ U(2, 10)."
    )
    L.append(
        f"- **Held fixed at `Parameters()` defaults:** alpha = {base.alpha} (displacement threshold "
        f"1/(1-alpha) = {base.displacement_threshold:.3f}), ai_cost_full = {base.ai_cost_full}, "
        f"entry_pool_elasticity = {base.entry_pool_elasticity}, sector exposures {base.sector_ai_exposure}. "
        "Labour supply is perfectly elastic (partial equilibrium), so `wage_effect` is 0 by construction."
    )
    L.append(
        "- **Definitions:** offset = net_employment_effect > 0; strong offset = net > 5%; concentration = "
        "employment in firms with < 20 employees falls (small_firm_employment_effect < 0). Size classes use *current* "
        "size buckets (small < 20, mid 20-499, large 500+), not pre-shock cohorts.\n"
    )
    L.append("Realised draws:\n")
    L.append(md_table(inputs, {"min": "{:.3f}", "mean": "{:.3f}", "max": "{:.3f}"}, "parameter"))
    L.append("")

    p_off = probs.iloc[0]
    p_str = probs.iloc[1]
    p_con = probs.iloc[2]
    p_share = probs.iloc[3]
    p_off_disp = probs.loc["P(offset | large-firm employment falls)"]
    p_smooth, r2_smooth, resid_sd = smoothed_offset(df)
    regimes = df["regime"].value_counts(normalize=True)
    s_small = sens["small_firm_employment_effect"][0]
    low_band = df[df["sigma_ai"] <= 2.5]
    plateau = sb[sb["mid"] >= 3.25]
    hi_region = df[df["sigma_ai"] >= 3.25]
    corner = df[(df["sigma_ai"] > 3.5) & (df["ai_entrant_productivity_shift"] < 0.05)]
    good_entry = df[df["ai_entrant_productivity_shift"] >= 0.10]

    L.append("## Key findings\n")
    L.append(
        f"1. **P(offset) = {pct0(p_off.probability)}** (95% CI {pct0(p_off.ci95_lo)}-{pct0(p_off.ci95_hi)}). "
        f"Median net employment effect {pct(net.median())}, mean {pct(net.mean())}, 90% interval "
        f"[{pct(net.quantile(0.05))}, {pct(net.quantile(0.95))}]. Smoothing out simulation noise with a quartic "
        f"response surface (R^2 = {r2_smooth:.2f}, residual SD {resid_sd:.1%} vs pure-noise SD {math.sqrt(var_noise):.1%}) "
        f"gives P(offset) = {pct0(p_smooth)}, so the headline is not a noise artefact."
    )
    L.append(
        f"2. **P(strong offset, net > 5%) = {pct0(p_str.probability)}** (95% CI {pct0(p_str.ci95_lo)}-{pct0(p_str.ci95_hi)})."
    )
    L.append(
        f"3. **Most offset is absence of displacement, not compensation for it.** Large-firm (500+) employment falls "
        f"in only {pct0(regimes.get('displacement, offset', 0) + regimes.get('displacement, no offset', 0))} of draws. "
        f"Regimes: no large-firm displacement {pct0(regimes.get('no large-firm displacement', 0))}; displacement fully "
        f"offset {pct0(regimes.get('displacement, offset', 0))}; displacement not offset "
        f"{pct0(regimes.get('displacement, no offset', 0))}. Conditional on large-firm employment falling, "
        f"P(offset) = {pct0(p_off_disp.probability)} (95% CI {pct0(p_off_disp.ci95_lo)}-{pct0(p_off_disp.ci95_hi)}); "
        f"median offset-ratio proxy among those draws = {df['offset_ratio_proxy'].median():.2f}."
    )
    L.append(
        f"4. **P(concentration) = {pct0(p_con.probability)}** (95% CI {pct0(p_con.ci95_lo)}-{pct0(p_con.ci95_hi)}), "
        f"and it never coincides with job loss: P(no offset and concentration) = "
        f"{pct0(((~df['offset']) & df['concentration']).mean())}. It occurs at low sigma_ai, where AI is a large "
        f"cost advantage and adopters scale up (sigma_ai <= 2.5: adoption {pct0(low_band['adoption_rate'].mean())}, "
        f"500+ employment {pct(low_band['large_firm_employment_effect'].mean())}, P(concentration) "
        f"{pct0(low_band['concentration'].mean())}). This is concentration through growth: firms climb out of the "
        f"<20 bucket. Share-based concentration (500+ share of employment rises) is more common, "
        f"{pct0(p_share.probability)} overall, {pct0(lo_sig['share_concentration'].mean())} for sigma_ai < "
        f"{base.displacement_threshold:.2f} vs {pct0(hi_sig['share_concentration'].mean())} above. Small-firm (<20) "
        f"employment rises in {pct0(1 - p_con.probability)} of draws (median {pct(df['small_firm_employment_effect'].median())})."
    )
    L.append(
        f"5. **{top} dominates the net effect.** First-order index S1 = {s1(s_net.iloc[0].first_order_S1)} "
        f"(Spearman rho = {s_net.iloc[0].spearman_rho:+.2f}). Next is {second} (S1 = {s1(s_net.iloc[1].first_order_S1)}), "
        f"then {s_net.index[2]} (S1 = {s1(s_net.iloc[2].first_order_S1)}) and {s_net.index[3]} "
        f"(S1 = {s1(s_net.iloc[3].first_order_S1)}). The four parameters explain {r2_lin:.0%} of variance linearly and "
        f"{r2_quad:.0%} with a quadratic surface; pure simulation noise is {var_noise / var_total:.1%} of the total. "
        f"For small-firm employment the entry-side channels matter about as much as sigma_ai: "
        + ", ".join(f"{p} S1 = {s1(r.first_order_S1)}" for p, r in s_small.iterrows())
        + "."
    )
    zero_txt = (
        f"crosses zero at sigma_ai ~ {sig0_mean:.2f}"
        if np.isfinite(sig0_mean)
        else "never crosses zero on [2, 5]"
    )
    p50_txt = (
        f"P(offset) crosses 50% at sigma_ai ~ {sig0_p50:.2f}"
        if np.isfinite(sig0_p50)
        else f"P(offset) never falls below {pct0(sb['P_offset'].min())}"
    )
    L.append(
        f"6. **No sigma_ai tipping point inside the prior.** The binned mean net effect {zero_txt}: it falls from "
        f"{pct(sb['net_mean'].iloc[0])} at sigma_ai in {sb.index[0]} to {pct(plateau['net_mean'].min())}-"
        f"{pct(plateau['net_mean'].max())} for sigma_ai >= 3.25, and {p50_txt}. Higher sigma_ai displaces more labour "
        f"per adopter but also shrinks AI's cost advantage, so adoption falls from {pct0(sb['adoption'].iloc[0])} to "
        f"{pct0(sb['adoption'].iloc[-1])} across the range (with ai_cost_full = {base.ai_cost_full} the AI price is at "
        f"or above the wage in every sector). Below the single-firm threshold 1/(1-alpha) = "
        f"{base.displacement_threshold:.2f}: P(offset) = {pct0(lo_sig['offset'].mean())} (n = {len(lo_sig)}); "
        f"above it: {pct0(hi_sig['offset'].mean())} (n = {len(hi_sig)})."
    )
    L.append(
        f"7. **Offset fails mainly when high substitution meets weak AI-native entry.** sigma_ai > 3.5 and entrant "
        f"shift < 0.05 (n = {len(corner)}): P(offset) = {pct0(corner['offset'].mean())}, mean net "
        f"{pct(corner['net_employment_effect'].mean())}. Entrant shift >= 0.10 (n = {len(good_entry)}): P(offset) = "
        f"{pct0(good_entry['offset'].mean())}. Above the threshold, entrant quality decides offset; the size of the "
        f"entry-cost cut matters far less (S1 = {s1(s_net.loc[PARAM_LABELS['entry_cost_reduction'], 'first_order_S1'])})."
    )
    L.append("")
    L.append("### Caveats\n")
    L.append(
        f"- **Simulation noise is material where the effect is small.** For sigma_ai >= 3.25 the net effect has SD "
        f"{hi_region['net_employment_effect'].std():.1%}, of which pure noise (SD {math.sqrt(var_noise):.1%}) is "
        f"{var_noise / hi_region['net_employment_effect'].var():.0%} of the variance. The model economy has about "
        f"{df['employment_cf'].mean() / 1000:.0f}k workers, and the 500+ bucket ({(df['emp_large_cf'] / df['employment_cf']).mean():.0%} "
        "of employment) holds few firms, so shock histories move it. P(offset) in that region mixes parameter "
        "uncertainty with finite-economy luck."
    )
    L.append(
        f"- **Partial equilibrium.** Wages are fixed at wage0. A finite labour-supply elasticity would damp both gains "
        "and losses."
    )
    L.append(
        f"- **ai_cost_full is fixed at {base.ai_cost_full}.** It sets how cheap AI is relative to labour and drives the "
        "adoption decline that flattens the sigma_ai profile. `default_uncertainty()` already carries a lognormal prior "
        "for it, and it is the obvious next parameter to add."
    )
    L.append(
        "- **Size classes are current-size buckets, not pre-shock cohorts.** `offset_ratio_proxy` is "
        "(change in <500 employment) / (loss in 500+ employment), so it only approximates the paper's cohort-based "
        "Omega. Firms that grow across a bucket edge count as gains in one class and losses in another."
    )
    L.append("")
    L.append("### Joint outcome probabilities (offset x concentration)\n")
    L.append(md_table(joint, {c: pct0 for c in joint.columns}, ""))
    L.append("")
    L.append("### Regimes by sigma_ai\n")
    reg = pd.crosstab(pd.cut(df["sigma_ai"], np.arange(2.0, 5.01, 0.5), include_lowest=True), df["regime"], normalize="index")
    reg = reg.reindex(columns=["no large-firm displacement", "displacement, offset", "displacement, no offset"], fill_value=0.0)
    reg.index = [f"[{iv.left:.1f}, {iv.right:.1f}]" for iv in reg.index]
    reg["P(offset)"] = df.groupby(pd.cut(df["sigma_ai"], np.arange(2.0, 5.01, 0.5), include_lowest=True), observed=True)["offset"].mean().to_numpy()
    L.append(md_table(reg, {c: pct0 for c in reg.columns}, "sigma_ai"))
    L.append("")

    L.append("## Probability table (Monte Carlo SE and Wilson 95% CI)\n")
    L.append(md_table(probs, {"probability": pct0, "mc_se": pct0, "ci95_lo": pct0, "ci95_hi": pct0, "n": "{:.0f}"}, "event"))
    L.append("")

    L.append("## Summary statistics of outcomes\n")
    L.append(
        "Proportional AI-vs-counterfactual differences (rates for `entry_rate_change`, `adoption_rate`, "
        "`adopter_employment_share`; `offset_ratio_proxy` is defined only when large-firm employment falls).\n"
    )
    f4 = {c: "{:+.4f}" for c in summ.columns}
    f4["n"] = "{:.0f}"
    f4["sd"] = "{:.4f}"
    f4["mc_se_mean"] = "{:.4f}"
    L.append(md_table(summ, f4, "outcome"))
    L.append("")

    L.append("## Sensitivity: which parameter drives variance\n")
    L.append(
        "S1 = bias-adjusted first-order index Var(E[Y|X_i])/Var(Y) from 20 quantile bins (model-free; captures "
        "non-linear main effects). SRC = standardised regression coefficient (linear, additive); SRC^2 sums to the "
        "linear R^2. Rows sorted by S1.\n"
    )
    sfmt = {"spearman_rho": "{:+.3f}", "src": "{:+.3f}", "src_sq": "{:.3f}", "first_order_S1": "{:.3f}"}
    for o, (t, r2l, r2q) in sens.items():
        L.append(f"### {o}\n")
        L.append(md_table(t, sfmt, "parameter"))
        L.append(
            f"\nLinear R^2 = {r2l:.3f}; quadratic (squares + interactions) R^2 = {r2q:.3f}; sum of S1 = "
            f"{t['first_order_S1'].sum():.3f}.\n"
        )

    L.append(f"### P(offset) by sigma_ai and {second}\n")
    L.append(md_table(two_way(df, second_key), {c: pct0 for c in two_way(df, second_key).columns}, ""))
    L.append("")

    L.append("## Scatter data: sigma_ai vs net employment effect\n")
    L.append(
        "Binned (width 0.25) conditional distribution of the net employment effect. Raw points: columns `sigma_ai` "
        "and `net_employment_effect` of `data/monte_carlo_raw.csv`.\n"
    )
    bfmt = {
        "n": "{:.0f}",
        "net_mean": pct,
        "net_p5": pct,
        "net_p50": pct,
        "net_p95": pct,
        "P_offset": pct0,
        "P_strong": pct0,
        "P_concentration": pct0,
        "P_share_conc": pct0,
        "P_large_falls": pct0,
        "small_mean": pct,
        "large_mean": pct,
        "adoption": pct0,
    }
    L.append(md_table(sb.drop(columns="mid"), bfmt, "sigma_ai bin"))
    L.append("")
    L.append("Sample of raw points (every 40th replication):\n")
    pts = df.iloc[::40][["sigma_ai", "net_employment_effect", "small_firm_employment_effect", "large_firm_employment_effect"]]
    L.append(md_table(pts, {"sigma_ai": "{:.3f}", "net_employment_effect": pct, "small_firm_employment_effect": pct, "large_firm_employment_effect": pct}, "rep"))
    L.append("")

    L.append("## Convergence and simulation noise\n")
    L.append(md_table(conv, {"P(offset)": pct0, "P(strong)": pct0, "P(concentration)": pct0, "mean net": pct}, "N"))
    L.append(
        f"\nFixed-parameter noise run (defaults: sigma_ai = {base.sigma_ai}, entry_cost_post = {base.entry_cost_post}, "
        f"shift = {base.ai_entrant_productivity_shift}, F_ai = {base.ai_adoption_fixed_cost}; n = {len(noise)}): "
        f"net effect mean {pct(noise['net_employment_effect'].mean())}, SD {noise['net_employment_effect'].std():.2%}; "
        f"small-firm effect mean {pct(noise['small_firm_employment_effect'].mean())}, "
        f"SD {noise['small_firm_employment_effect'].std():.2%}.\n"
    )

    L.append("## Raw data\n")
    L.append(
        "`data/monte_carlo_raw.csv`: one row per replication -- `seed`, the four drawn parameters "
        "(`entry_cost_post` plus derived `entry_cost_reduction`), all `employment_effects` outputs, employment levels "
        "by size class in each scenario (`emp_{small,mid,large}_{ai,cf}`, `employment_{ai,cf}`), "
        "`offset_ratio_proxy`, and boolean `offset`, `strong_offset`, `concentration`. "
        "`data/monte_carlo_noise.csv`: the fixed-parameter replications."
    )
    return "\n".join(L) + "\n"


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--n", type=int, default=2000)
    ap.add_argument("--noise-n", type=int, default=60)
    ap.add_argument("--jobs", type=int, default=6)
    ap.add_argument("--seed", type=int, default=2026)
    ap.add_argument("--analyze-only", action="store_true")
    args = ap.parse_args()

    runtime = None
    if args.analyze_only:
        df = pd.read_csv(RAW_CSV, index_col="replication")
        noise = pd.read_csv(NOISE_CSV, index_col="replication")
    else:
        t0 = time.time()
        df, noise = simulate(args.n, args.noise_n, args.seed, args.jobs)
        runtime = time.time() - t0
        df.to_csv(RAW_CSV)
        noise.to_csv(NOISE_CSV)
        print(f"wrote {RAW_CSV} ({len(df)} rows), {NOISE_CSV}; {runtime:.0f}s")
    REPORT_MD.write_text(report(df, noise, args.seed, runtime))
    print(f"wrote {REPORT_MD}")


if __name__ == "__main__":
    main()
