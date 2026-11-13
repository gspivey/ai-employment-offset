"""Regime map: net labor-demand effect of AI by sigma_ai x entrant productivity shift.

For each cell of a sigma_ai x Delta-mu_e grid, runs the AI scenario and its
no-AI twin for several seeds (common random numbers) and records the mean
net employment effect, its seed standard error, and the mean large-firm
(500+) effect. Other AI parameters are held at fixed central values, so the
map is a comparative-statics picture, not a probability statement.

Runs both CES normalizations so the effect of fixing the cost saving
is visible:
    none         AI price fixed at ai_cost_full (original model)
    cost_saving  AI price rescaled so the reference unit-cost saving is the
                 same for every sigma_ai

Outputs
    data/regime_map.csv
    data/regime_map.md
    paper/figures/regime_map.{pdf,png}

Usage
    .venv/bin/python scripts/regime_map.py [--seeds 10] [--jobs 6]
"""
from __future__ import annotations

import argparse
import sys
import time
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

from model import Parameters  # noqa: E402
import monte_carlo_t6 as t6  # noqa: E402

SIGMAS = (1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0)
SHIFTS = (0.0, 0.05, 0.10, 0.15)
FIXED = dict(entry_cost_post=0.85 * Parameters().entry_cost_pre, ai_adoption_fixed_cost=6.0)
OUT_CSV = ROOT / "data" / "regime_map.csv"
OUT_MD = ROOT / "data" / "regime_map.md"
OUT_FIG = ROOT / "paper" / "figures" / "regime_map"


def tasks(n_seeds: int, base_seed: int):
    seeds = np.random.SeedSequence(base_seed).generate_state(n_seeds, dtype=np.uint32)
    out, i = [], 0
    for norm in ("none", "cost_saving"):
        for s in SIGMAS:
            for d in SHIFTS:
                p = Parameters().with_updates(sigma_ai=s, ai_entrant_productivity_shift=d, ces_normalization=norm, **FIXED)
                for k, sd in enumerate(seeds):  # same seeds in every cell (common random numbers)
                    out.append(((norm, s, d, k), p, int(sd)))
                    i += 1
    return out


def run_one(task):
    key, p, seed = task
    r = t6.replicate((0, p, seed, t6.EVAL_WINDOW))
    return key, r["net_employment_effect"], r["large_firm_employment_effect"], r["adoption_rate"]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", type=int, default=10)
    ap.add_argument("--jobs", type=int, default=6)
    ap.add_argument("--seed", type=int, default=2028)
    a = ap.parse_args()
    ts = tasks(a.seeds, a.seed)
    t0 = time.time()
    rows = []
    with ProcessPoolExecutor(max_workers=a.jobs) as pool:
        for k, res in enumerate(pool.map(run_one, ts, chunksize=4), 1):
            (norm, s, d, seed_i), net, large, adopt = res
            rows.append(dict(normalization=norm, sigma_ai=s, entrant_shift=d, seed=seed_i,
                             net=net, large=large, adoption=adopt))
            if k % 100 == 0 or k == len(ts):
                print(f"{k}/{len(ts)} {time.time() - t0:.0f}s", flush=True)
    df = pd.DataFrame(rows)
    g = df.groupby(["normalization", "sigma_ai", "entrant_shift"])
    tab = g.agg(net_mean=("net", "mean"), net_se=("net", lambda x: x.std(ddof=1) / np.sqrt(len(x))),
                large_mean=("large", "mean"), adoption_mean=("adoption", "mean"), n=("net", "size")).reset_index()
    tab.to_csv(OUT_CSV, index=False)

    theta = Parameters().theta
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.6), dpi=150, sharey=True)
    vmax = 0.4
    for ax, norm, title in zip(axes, ("none", "cost_saving"), ("AI price fixed (original)", "Cost saving fixed (normalized)")):
        t = tab[tab.normalization == norm].pivot(index="entrant_shift", columns="sigma_ai", values="net_mean")
        se = tab[tab.normalization == norm].pivot(index="entrant_shift", columns="sigma_ai", values="net_se")
        im = ax.imshow(t.to_numpy(), origin="lower", aspect="auto", cmap="RdBu", vmin=-vmax, vmax=vmax)
        for i in range(t.shape[0]):
            for j in range(t.shape[1]):
                v, e = t.iat[i, j], se.iat[i, j]
                ax.text(j, i, f"{v:+.0%}\n±{e:.0%}", ha="center", va="center", fontsize=7,
                        color="white" if abs(v) > 0.25 else "black")
        ax.set_xticks(range(len(SIGMAS)))
        ax.set_xticklabels([f"{s:g}" for s in SIGMAS], fontsize=8)
        ax.set_yticks(range(len(SHIFTS)))
        ax.set_yticklabels([f"{d:.2f}" for d in SHIFTS], fontsize=8)
        ax.axvline(np.interp(theta, SIGMAS, range(len(SIGMAS))), color="black", ls="--", lw=0.8)
        ax.set_xlabel(r"Labor-AI substitution elasticity $\sigma_{\mathrm{ai}}$", fontsize=9)
        ax.set_title(title, fontsize=10)
    axes[0].set_ylabel(r"Entrant productivity shift $\Delta\mu_e$", fontsize=9)
    cb = fig.colorbar(im, ax=axes, fraction=0.025, pad=0.02)
    cb.ax.yaxis.set_major_formatter(matplotlib.ticker.PercentFormatter(1.0, decimals=0))
    cb.set_label("Mean net labor-demand effect vs. no-AI twin", fontsize=8)
    OUT_FIG.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT_FIG.with_suffix(".pdf"), bbox_inches="tight")
    fig.savefig(OUT_FIG.with_suffix(".png"), bbox_inches="tight")

    L = ["# Regime map: net labor-demand effect by sigma_ai and entrant shift", "",
         f"Generated by `scripts/regime_map.py` ({a.seeds} seeds per cell, seed {a.seed}, wall {time.time() - t0:.0f}s).",
         f"Fixed: entry-cost cut 15%, AI adoption fixed cost 6, alpha 0.64 (theta = {theta:.3f}), wages fixed.",
         "Cells: mean net employment effect vs. the no-AI twin, with seed standard error. Not probabilities.", ""]
    for norm in ("none", "cost_saving"):
        L += [f"## normalization = {norm}", "", "| entrant shift \\ sigma | " + " | ".join(f"{s:g}" for s in SIGMAS) + " |",
              "|---|" + "---|" * len(SIGMAS)]
        for d in SHIFTS:
            cells = []
            for s in SIGMAS:
                r = tab[(tab.normalization == norm) & (tab.sigma_ai == s) & (tab.entrant_shift == d)].iloc[0]
                cells.append(f"{r.net_mean:+.1%} (±{r.net_se:.1%})")
            L.append(f"| {d:.2f} | " + " | ".join(cells) + " |")
        L.append("")
    OUT_MD.write_text("\n".join(L) + "\n")
    print(OUT_MD.read_text())


if __name__ == "__main__":
    main()
