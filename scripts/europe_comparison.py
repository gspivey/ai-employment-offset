"""Stylized US-vs-Europe Monte Carlo for the transatlantic comparison (Section 7).

Runs the T6 design (``scripts/monte_carlo_t6.py``) under a US parameterisation
and under European variants that change one institutional channel at a time,
then all together. Common random numbers: every scenario uses the same
sigma_ai draws, the same uniform quantiles for the channel parameters, and the
same simulation seeds, so scenario differences reflect institutions only.

US priors are the T6 priors:
    sigma_ai                       U(2, 5)                     (shared)
    entry_cost_post                entry_cost_pre * (1 - 0.30 u1)
    ai_entrant_productivity_shift  0.15 u2
    ai_adoption_fixed_cost         2 + 8 u3
    potential_entrants             600

European channels (stylized mappings, documented in data/europe_comparison.md):
    pool     potential_entrants x 0.53 = EU-27 employer birth rate 2024
             (4.80%, Eurostat bd_size) / US startup rate 2023 (9.10%, BDS)
    ai_act   entry-cost cut capped at 20% (1 - 0.20 u1); adoption fixed cost
             3 + 9 u3 (AI Act provider/deployer obligations)
    finance  entrant shift 0.10 u2 (EU AI private investment ~1/9-1/14 of US)
    all      all three

Outputs: data/europe_comparison_raw.csv, data/europe_comparison.md.
Usage: python scripts/europe_comparison.py [--n 500] [--jobs 8] [--seed 2026]
"""

from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

from model import Parameters  # noqa: E402
from monte_carlo_t6 import STRONG_OFFSET, run, wilson  # noqa: E402

DATA = ROOT / "data"
RAW_CSV = DATA / "europe_comparison_raw.csv"
REPORT_MD = DATA / "europe_comparison.md"

POOL_RATIO = 4.80 / 9.10  # EU-27 employer birth rate 2024 / US BDS startup rate 2023

SCENARIOS = {
    "US": dict(pool=False, ai_act=False, finance=False),
    "EU: entry pool": dict(pool=True, ai_act=False, finance=False),
    "EU: AI Act costs": dict(pool=False, ai_act=True, finance=False),
    "EU: growth finance": dict(pool=False, ai_act=False, finance=True),
    "EU: all channels": dict(pool=True, ai_act=True, finance=True),
}


def scenario_draws(base: Parameters, u: np.ndarray, sigma: np.ndarray, pool: bool, ai_act: bool, finance: bool) -> list:
    pre = base.entry_cost_pre
    max_cut = 0.20 if ai_act else 0.30
    f_lo, f_span = (3.0, 9.0) if ai_act else (2.0, 8.0)
    shift_max = 0.10 if finance else 0.15
    entrants = base.potential_entrants * (POOL_RATIO if pool else 1.0)
    return [
        {
            "sigma_ai": float(sigma[i]),
            "entry_cost_post": float(pre * (1.0 - max_cut * u[i, 0])),
            "ai_entrant_productivity_shift": float(shift_max * u[i, 1]),
            "ai_adoption_fixed_cost": float(f_lo + f_span * u[i, 2]),
            "potential_entrants": float(entrants),
        }
        for i in range(len(sigma))
    ]


def summarise(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for name, g in df.groupby("scenario", sort=False):
        n = len(g)
        k = int(g["offset"].sum())
        lo, hi = wilson(k, n)
        above = g[g["sigma_ai"] > 2.78]
        disp = g[g["large_firm_employment_effect"] < 0]
        rows.append(
            {
                "scenario": name,
                "P(offset)": k / n,
                "95% CI": f"{lo:.1%}-{hi:.1%}",
                "P(strong offset)": (g["net_employment_effect"] > STRONG_OFFSET).mean(),
                "median net effect": g["net_employment_effect"].median(),
                "median small-firm effect": g["small_firm_employment_effect"].median(),
                "median large-firm effect": g["large_firm_employment_effect"].median(),
                "median entry-rate change": g["entry_rate_change"].median(),
                "P(offset | sigma>2.78)": above["offset"].mean(),
                "P(offset | displacement)": disp["offset"].mean() if len(disp) else np.nan,
                "n": n,
            }
        )
    return pd.DataFrame(rows).set_index("scenario")


def paired(df: pd.DataFrame) -> pd.DataFrame:
    us = df[df["scenario"] == "US"].set_index("replication")
    rows = []
    for name in list(SCENARIOS)[1:]:
        eu = df[df["scenario"] == name].set_index("replication")
        d = eu["net_employment_effect"] - us["net_employment_effect"]
        rows.append(
            {
                "scenario": name,
                "mean diff vs US (pp)": 100 * d.mean(),
                "SE (pp)": 100 * d.std(ddof=1) / np.sqrt(len(d)),
                "share of draws where EU < US": (d < 0).mean(),
                "offset flips (US yes, EU no)": (us["offset"] & ~eu["offset"]).mean(),
            }
        )
    return pd.DataFrame(rows).set_index("scenario")


def fmt_table(t: pd.DataFrame) -> str:
    def cell(v):
        if isinstance(v, (float, np.floating)):
            return f"{v:.3f}" if abs(v) < 10 else f"{v:.1f}"
        return str(v)

    cols = [t.index.name or ""] + list(t.columns)
    lines = ["| " + " | ".join(cols) + " |", "|" + "---|" * len(cols)]
    for idx, row in t.iterrows():
        lines.append("| " + " | ".join([str(idx)] + [cell(v) for v in row]) + " |")
    return "\n".join(lines)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=500)
    ap.add_argument("--jobs", type=int, default=8)
    ap.add_argument("--seed", type=int, default=2026)
    ap.add_argument("--analyze-only", action="store_true")
    args = ap.parse_args()

    if not args.analyze_only:
        base = Parameters()
        rng = np.random.default_rng(np.random.SeedSequence([args.seed, 77]))
        sigma = rng.uniform(2.0, 5.0, args.n)
        u = rng.uniform(0.0, 1.0, (args.n, 3))
        seeds = np.random.SeedSequence([args.seed, 78]).generate_state(args.n, dtype=np.uint32)
        frames = []
        t0 = time.time()
        for name, flags in SCENARIOS.items():
            out = run(scenario_draws(base, u, sigma, **flags), base, seeds, args.jobs, name)
            out["offset"] = out["net_employment_effect"] > 0
            out.insert(0, "scenario", name)
            frames.append(out.reset_index())
        df = pd.concat(frames, ignore_index=True)
        df.to_csv(RAW_CSV, index=False)
        print(f"simulated {len(df)} replications in {time.time() - t0:.0f}s")
    df = pd.read_csv(RAW_CSV)

    s, p = summarise(df), paired(df)
    md = [
        "# US vs Europe: stylized Monte Carlo comparison",
        "",
        "Generated by `scripts/europe_comparison.py`; every number is computed from `data/europe_comparison_raw.csv`.",
        f"N = {df['replication'].nunique()} draws per scenario, common random numbers across scenarios (same sigma_ai, "
        "channel quantiles and simulation seeds). Offset = net employment effect > 0, as in T6.",
        f"Entry-pool ratio = {POOL_RATIO:.3f} (EU-27 employer birth rate 2024 / US BDS startup rate 2023).",
        "",
        "## Scenario outcomes",
        "",
        fmt_table(s),
        "",
        "## Paired differences vs US (net employment effect)",
        "",
        fmt_table(p),
        "",
    ]
    REPORT_MD.write_text("\n".join(md))
    print("\n".join(md))


if __name__ == "__main__":
    main()
