"""T5: search for parameter combinations that reproduce cloud-era concentration.

Empirical targets (data/cloud_era_baseline.md, Census BDS 2006 -> 2019):
  small-firm (<500) employment share  50.9% -> 47.0%  (-3.9 pp, -7.7% rel.)
  employer startup rate               10.3% ->  8.5%  (-1.8 pp, -17.5% rel.)
  young-firm (age 0-5) emp. share     13.4% -> 10.6%  (-2.8 pp, -20.9% rel.)

The model's "AI" shock is reinterpreted as the cloud/IT shock: channel (a)
entry cost, (b) entrant productivity, (c) a factor-augmenting technology with a
per-period adoption fixed cost (proprietary IT / cloud integration).

Each scenario runs the shocked arm and a frozen pre-shock arm from the same
burned-in economy with common random numbers. Effects are shocked minus frozen,
averaged over years 11-15 after the shock starts (centred on 2006 + 13 = 2019)
and over the long run (last 10 periods). Parameters listed in ``phased`` move
from their pre value to the given post value in step with diffusion S(t),
like entry_cost_post does natively (used for rising fixed costs and a shrinking
founder pool, which the model otherwise holds constant).

Run from the workspace root:
    .venv/bin/python scripts/cloud_replication.py            # single-lever sweep, 8 seeds
    .venv/bin/python scripts/cloud_replication.py grid       # 240-cell combination grid, 8 seeds
    .venv/bin/python scripts/cloud_replication.py confirm    # finalists + decomposition, 24 seeds
Writes data/cloud_replication_{results,grid,confirm}.csv. Write-up:
data/cloud_replication_scenarios.md.
"""

from __future__ import annotations

import sys
from multiprocessing import Pool
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from model.parameters import Parameters  # noqa: E402
from model.simulation import initialize_economy, simulate_period  # noqa: E402

SEEDS = tuple(range(42, 50))
WINDOW_13 = range(16, 21)  # ai_start_period 5 + years 11..15
WINDOW_LR = range(30, 40)
PRE = range(0, 5)

TARGETS = {"d_share_lt500_pp": -3.9, "d_entry_rate_pp": -1.8, "d_young_share_pp": -2.8}
TARGETS_REL = {"d_share_lt500_rel": -0.077, "d_entry_rate_rel": -0.175, "d_young_share_rel": -0.209}

# name -> (group, base-parameter overrides, phased {param: post value})
SCENARIOS = {
    "baseline": ("A baseline", {}, {}),
    # B: labour-augmenting technology (sigma below 1/(1-alpha) = 2.78)
    "sigma_2.5": ("B sigma", dict(sigma_ai=2.5), {}),
    "sigma_2.0": ("B sigma", dict(sigma_ai=2.0), {}),
    "sigma_1.5": ("B sigma", dict(sigma_ai=1.5), {}),
    # C: entry cost
    "ce_-10%": ("C entry cost", dict(entry_cost_post=18.0), {}),
    "ce_-5%": ("C entry cost", dict(entry_cost_post=19.0), {}),
    "ce_0%": ("C entry cost", dict(entry_cost_post=20.0), {}),
    "ce_+10%": ("C entry cost", dict(entry_cost_post=22.0), {}),
    "ce_+20%": ("C entry cost", dict(entry_cost_post=24.0), {}),
    # D: per-period fixed operating cost rising with diffusion (regressive)
    "fc_0.5->0.75": ("D fixed cost", {}, dict(fixed_cost=0.75)),
    "fc_0.5->1.0": ("D fixed cost", {}, dict(fixed_cost=1.0)),
    "fc_0.5->1.5": ("D fixed cost", {}, dict(fixed_cost=1.5)),
    "fc_static_1.0": ("D fixed cost", dict(fixed_cost=1.0), {}),
    # E: entrant quality declining
    "shift_0": ("E entrant quality", dict(ai_entrant_productivity_shift=0.0), {}),
    "shift_-0.05": ("E entrant quality", dict(ai_entrant_productivity_shift=-0.05), {}),
    "shift_-0.10": ("E entrant quality", dict(ai_entrant_productivity_shift=-0.10), {}),
    "shift_-0.20": ("E entrant quality", dict(ai_entrant_productivity_shift=-0.20), {}),
    # F: shrinking founder pool (Karahan-Pugsley-Sahin demographics; non-tech)
    "pool_-10%": ("F founder pool", {}, dict(potential_entrants=540.0)),
    "pool_-20%": ("F founder pool", {}, dict(potential_entrants=480.0)),
    # G: combinations
    "sig2.5_ce-5%": ("G combo", dict(sigma_ai=2.5, entry_cost_post=19.0), {}),
    "sig2.0_ce-5%": ("G combo", dict(sigma_ai=2.0, entry_cost_post=19.0), {}),
    "sig2.0_ce+10%": ("G combo", dict(sigma_ai=2.0, entry_cost_post=22.0), {}),
    "sig2.0_ce-5%_sh-0.10": (
        "G combo",
        dict(sigma_ai=2.0, entry_cost_post=19.0, ai_entrant_productivity_shift=-0.10),
        {},
    ),
    "sig2.0_ce-5%_fc1.0": ("G combo", dict(sigma_ai=2.0, entry_cost_post=19.0), dict(fixed_cost=1.0)),
    "sig2.0_ce-5%_pool-10%": ("G combo", dict(sigma_ai=2.0, entry_cost_post=19.0), dict(potential_entrants=540.0)),
    "sig2.0_ce-5%_Fai2.5": ("G combo", dict(sigma_ai=2.0, entry_cost_post=19.0, ai_adoption_fixed_cost=2.5), {}),
    "sig1.5_ce-5%_sh-0.05": (
        "G combo",
        dict(sigma_ai=1.5, entry_cost_post=19.0, ai_entrant_productivity_shift=-0.05),
        {},
    ),
    "sig2.5_ce+10%_sh-0.05": (
        "G combo",
        dict(sigma_ai=2.5, entry_cost_post=22.0, ai_entrant_productivity_shift=-0.05),
        {},
    ),
    "sig3.5_ce+10%_sh-0.10_fc1.0": (
        "G combo",
        dict(entry_cost_post=22.0, ai_entrant_productivity_shift=-0.10),
        dict(fixed_cost=1.0),
    ),
    # H: finite labour supply (wage clears the market)
    "eps1_baseline": ("H general eq.", dict(labor_supply_elasticity=1.0), {}),
    "eps1_sig2.0": ("H general eq.", dict(labor_supply_elasticity=1.0, sigma_ai=2.0), {}),
    "eps0.5_sig2.0": ("H general eq.", dict(labor_supply_elasticity=0.5, sigma_ai=2.0), {}),
    "eps0_sig2.0": ("H general eq.", dict(labor_supply_elasticity=0.0, sigma_ai=2.0), {}),
}


def _period_params(base: Parameters, phased: dict, t: int) -> Parameters:
    if not phased:
        return base
    s = base.ai_diffusion(t)
    return base.with_updates(**{k: getattr(base, k) + (v - getattr(base, k)) * s for k, v in phased.items()})


def _young_share(econ) -> float:
    emp = econ.size.sum()
    return float(econ.size[econ.age <= 5].sum() / emp) if emp > 0 else np.nan


def _run_arm(econ, base: Parameters, phased: dict, seed: int, shocked: bool) -> pd.DataFrame:
    rows = []
    for t in range(base.n_periods):
        p = _period_params(base, phased, t) if shocked else base
        econ.params = p
        rec = simulate_period(econ, t, p, seed, ai_enabled=shocked)
        emp = rec["aggregate_employment"]
        rec["share_lt500"] = 1.0 - rec["emp_500_plus"] / emp
        rec["emp_lt500"] = emp - rec["emp_500_plus"]
        rec["young_share"] = _young_share(econ)
        rows.append(rec)
    return pd.DataFrame(rows).set_index("period")


def run_pair(base: Parameters, phased: dict, seed: int):
    econ = initialize_economy(base, seed)
    shocked = _run_arm(econ.copy(), base, phased, seed, shocked=True)
    frozen = _run_arm(econ, base, phased, seed, shocked=False)
    return shocked, frozen


def effects(shocked: pd.DataFrame, frozen: pd.DataFrame, window) -> dict:
    a, c = shocked.loc[list(window)], frozen.loc[list(window)]
    emp_c = c["aggregate_employment"].mean()
    out = {}
    for col, key in (("share_lt500", "share_lt500"), ("entry_rate", "entry_rate"), ("young_share", "young_share")):
        d = a[col].mean() - c[col].mean()
        out[f"d_{key}_pp"] = 100 * d
        out[f"d_{key}_rel"] = d / c[col].mean()
    d_tot = a["aggregate_employment"].mean() - emp_c
    d_small = a["emp_lt500"].mean() - c["emp_lt500"].mean()
    d_large = a["emp_500_plus"].mean() - c["emp_500_plus"].mean()
    out.update(
        net_emp_pct=100 * d_tot / emp_c,
        d_emp_lt500_pct=100 * d_small / emp_c,
        d_emp_500plus_pct=100 * d_large / emp_c,
        large_capture=d_large / d_tot if abs(d_tot) > 1e-9 else np.nan,
        firm_count_pct=100 * (a["n_firms"].mean() / c["n_firms"].mean() - 1),
        adoption_rate=a["adoption_rate"].mean(),
        adopter_emp_share=a["adopter_employment_share"].mean(),
    )
    return out


def _task(args):
    name, seed = args
    group, overrides, phased = SCENARIOS[name]
    base = Parameters().with_updates(**overrides)
    shocked, frozen = run_pair(base, phased, seed)
    rows = []
    for label, win in (("y13", WINDOW_13), ("lr", WINDOW_LR)):
        rows.append(dict(scenario=name, group=group, seed=seed, window=label, **effects(shocked, frozen, win)))
    pre, post = shocked.loc[list(PRE)], shocked.loc[list(WINDOW_13)]
    for col in ("share_lt500", "entry_rate", "young_share"):
        rows[0][f"pre_{col}"] = pre[col].mean()
        rows[0][f"ba_{col}_pp"] = 100 * (post[col].mean() - pre[col].mean())  # before/after, shocked arm
    return rows


#: (sigma_ai, ai_cost_full). Rows after the first hold the share-weighted
#: adopter unit cost at full diffusion equal to the baseline's (0.868), so
#: sigma changes the labour response without enlarging the technology gain.
#: ("2.5raw" keeps ai_cost_full = 1.5, a bigger gain.)
TECH = {"3.5": (3.5, 1.5), "2.5raw": (2.5, 1.5), "2.5n": (2.5, 2.715), "2.25n": (2.25, 3.833), "2.0n": (2.0, 6.716)}
GRID_ENTRY_COST = (16.0, 20.0, 22.0, 24.0)
GRID_SHIFT = (0.05, 0.0, -0.10, -0.15)
GRID_POOL = (600.0, 540.0, 480.0)


def _grid_task(args):
    tech, ce, sh, pool, seed = args
    sig, acf = TECH[tech]
    base = Parameters().with_updates(
        sigma_ai=sig, ai_cost_full=acf, entry_cost_post=ce, ai_entrant_productivity_shift=sh
    )
    phased = {} if pool == base.potential_entrants else dict(potential_entrants=pool)
    shocked, frozen = run_pair(base, phased, seed)
    key = dict(tech=tech, entry_cost_post=ce, entrant_shift=sh, pool_post=pool, seed=seed)
    return [dict(key, window=lab, **effects(shocked, frozen, win)) for lab, win in (("y13", WINDOW_13), ("lr", WINDOW_LR))]


def _combo(tech, ce, sh, pool=None, extra=None, phased_extra=None):
    sig, acf = TECH[tech]
    over = dict(sigma_ai=sig, ai_cost_full=acf, entry_cost_post=ce, ai_entrant_productivity_shift=sh, **(extra or {}))
    phased = dict(phased_extra or {})
    if pool is not None and pool != 600.0:
        phased["potential_entrants"] = pool
    return over, phased


#: Finalists and a one-channel-at-a-time decomposition of the best fit (F2),
#: confirmed on SEEDS_CONFIRM.
SEEDS_CONFIRM = tuple(range(42, 66))
CONFIRM = {
    "F0_baseline": ("final",) + _combo("3.5", 16.0, 0.05),
    "F1_tech_only_sig2.0n": ("final",) + _combo("2.0n", 16.0, 0.05),
    "F2_best_fit": ("final",) + _combo("2.0n", 24.0, 0.0, 480.0),
    "F3_cloud_entry_cut": ("final",) + _combo("2.0n", 16.0, -0.10, 480.0),
    "F4_moderate_sig2.25n": ("final",) + _combo("2.25n", 22.0, -0.10, 540.0),
    "F5_raw_sig2.5": ("final",) + _combo("2.5raw", 24.0, 0.0, 480.0),
    "F6_displacing_all_headwinds": ("final",) + _combo("3.5", 24.0, -0.10, 480.0),
    "F2_ge_eps1": ("final",) + _combo("2.0n", 24.0, 0.0, 480.0, extra=dict(labor_supply_elasticity=1.0)),
    "F2_plus_fc1.0": ("final",) + _combo("2.0n", 24.0, 0.0, 480.0, phased_extra=dict(fixed_cost=1.0)),
    "F2_minus_tech(sig3.5)": ("decomp",) + _combo("3.5", 24.0, 0.0, 480.0),
    "F2_minus_entrycost(ce16)": ("decomp",) + _combo("2.0n", 16.0, 0.0, 480.0),
    "F2_minus_pool(600)": ("decomp",) + _combo("2.0n", 24.0, 0.0, 600.0),
    "F2_minus_quality(+0.05)": ("decomp",) + _combo("2.0n", 24.0, 0.05, 480.0),
    # Baseline AI (displacing, -20% entry cost) facing only cloud-era founder/quality headwinds
    "X_baseline_ai_with_headwinds": ("check",) + _combo("3.5", 16.0, 0.0, 480.0),
}
SWEEP = tuple(SCENARIOS)
SCENARIOS.update(CONFIRM)


def target_loss(df: pd.DataFrame) -> pd.Series:
    """Sum of squared proportional misses on the three pp targets."""
    return sum(((df[k] - v) / v) ** 2 for k, v in TARGETS.items())


def grid():
    tasks = [
        (t, ce, sh, pool, s)
        for t in TECH for ce in GRID_ENTRY_COST for sh in GRID_SHIFT for pool in GRID_POOL for s in SEEDS
    ]
    with Pool() as pool:
        rows = [r for rs in pool.map(_grid_task, tasks, chunksize=4) for r in rs]
    df = pd.DataFrame(rows)
    df.to_csv(ROOT / "data" / "cloud_replication_grid.csv", index=False)
    keys = ["window", "tech", "entry_cost_post", "entrant_shift", "pool_post"]
    m = df.groupby(keys)[list(TARGETS) + ["net_emp_pct", "d_emp_500plus_pct", "d_emp_lt500_pct"]].mean()
    m["loss"] = target_loss(m)
    m["all_neg"] = (m[list(TARGETS)] < 0).all(axis=1)
    with pd.option_context("display.width", 200, "display.max_rows", 200):
        print(m.loc["y13"].sort_values("loss").head(25).round(2))
    return df


def main(names=None, seeds=SEEDS, out_name="cloud_replication_results.csv"):
    names = list(names or SWEEP)
    with Pool() as pool:
        rows = [r for rs in pool.map(_task, [(n, s) for n in names for s in seeds]) for r in rs]
    df = pd.DataFrame(rows)
    out = ROOT / "data" / out_name
    df.to_csv(out, index=False)
    cols = ["d_share_lt500_pp", "d_entry_rate_pp", "d_young_share_pp", "net_emp_pct",
            "d_emp_lt500_pct", "d_emp_500plus_pct", "firm_count_pct", "adoption_rate"]
    summary = df.groupby(["window", "scenario"], sort=False)[cols].mean().round(2)
    sd = df[df.window == "y13"].groupby("scenario", sort=False)["d_share_lt500_pp"].std().round(2)
    with pd.option_context("display.width", 200, "display.max_rows", 200):
        print(summary.loc["y13"].assign(sd_lt500=sd))
        print(summary.loc["lr"])
    return df


if __name__ == "__main__":
    if sys.argv[1:] == ["grid"]:
        grid()
    elif sys.argv[1:] == ["confirm"]:
        main(list(CONFIRM), SEEDS_CONFIRM, "cloud_replication_confirm.csv")
    else:
        main(sys.argv[1:] or None)
