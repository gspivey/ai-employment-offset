"""Sector-level AI scenarios (T8): is offset sector-dependent?

Each scenario changes only ``sector_ai_exposure`` (plus, for the channel
decomposition, the economy-wide entry-cost and entrant-productivity channels)
and is compared with a no-AI counterfactual run from the same burned-in economy
and seed (common random numbers; see ``model.simulation``).

Per sector and period we record employment, firm counts, the startup rate
(age-0 firms / firms at the start of the period), adoption, concentration, and
the cohort pieces of the offset ratio (``paper/sections/04-ai-model.tex``,
def:offset). Firms are classified by size at the end of the last pre-AI period:

* L = large before the shock (size >= ``Parameters.large_firm_min``);
* B = the band, 5 <= size < large_firm_min before the shock, plus post-shock
  entrants currently in the band.

Omega_s = dN^B_s / -dN^L_s, where dN is the AI-minus-counterfactual difference
averaged over the evaluation window.

Run ``python -m model.sector_analysis`` to regenerate
``data/sector_analysis_results.csv`` and print the markdown tables used in
``data/sector_analysis.md``.
"""

from __future__ import annotations

import math
from pathlib import Path
from typing import Dict, List, Optional, Sequence

import numpy as np
import pandas as pd

from .parameters import Parameters
from .simulation import initialize_economy, simulate_period

#: Lower edge of the offset band B (employees); upper edge is large_firm_min.
BAND_MIN = 5.0

#: Exposure vectors (goods, trade_transport, professional_services, information_finance).
EXPOSURE_SCENARIOS: Dict[str, tuple] = {
    "baseline": (0.5, 0.8, 1.2, 1.5),
    "uniform": (1.0, 1.0, 1.0, 1.0),
    "high_only": (0.0, 0.0, 1.2, 1.5),
    "low_only": (0.5, 0.8, 0.0, 0.0),
    "extreme_gradient": (0.2, 0.8, 1.4, 2.0),
}

#: Channel decomposition at baseline exposure: (c) alone, or (a)+(b) alone.
CHANNEL_SCENARIOS: Dict[str, dict] = {
    "displacement_only": {"sector_ai_exposure": (0.5, 0.8, 1.2, 1.5), "entry_cost_post": 20.0, "ai_entrant_productivity_shift": 0.0},
    "entry_only": {"sector_ai_exposure": (0.0, 0.0, 0.0, 0.0)},
}

LABOR_REGIMES: Dict[str, float] = {
    "PE": math.inf,  # perfectly elastic labour supply at wage0
    "GE_eps0.5": 0.5,  # upward-sloping labour supply
    "GE_fixedL": 0.0,  # fixed labour force
}

_PRE, _ENTRANT = -1, 3  # cohort codes; 0 = pre-shock <5, 1 = band, 2 = large


def all_scenarios() -> Dict[str, dict]:
    out = {name: {"sector_ai_exposure": exp} for name, exp in EXPOSURE_SCENARIOS.items()}
    out.update(CHANNEL_SCENARIOS)
    return out


def _top_share(x: np.ndarray, frac: float = 0.01) -> float:
    if x.size == 0 or x.sum() <= 0:
        return np.nan
    k = max(1, int(math.ceil(frac * x.size)))
    return float(np.sort(x)[-k:].sum() / x.sum())


def sector_record(econ, t: int, n_start: np.ndarray, pre_class: np.ndarray, params: Parameters) -> List[dict]:
    """One row per sector describing ``econ`` at the end of period ``t``."""
    K, large = params.n_sectors, params.large_firm_min
    sec, size, out, ids = econ.sector, econ.size, econ.output, econ.firm_id
    cls = np.full(ids.size, _ENTRANT, dtype=np.int64)
    old = ids < pre_class.size
    cls[old] = pre_class[ids[old]]
    in_band = (size >= BAND_MIN) & (size < large)
    total_emp = float(size.sum())
    rows = []
    for s in range(K):
        m = sec == s
        sz, o, c = size[m], out[m], cls[m]
        emp = float(sz.sum())
        n = int(m.sum())
        entrants = int((econ.age[m] == 0).sum())
        rows.append(
            {
                "period": t,
                "sector": params.sector_names[s],
                "wage": econ.wage,
                "firms": n,
                "employment": emp,
                "emp_share_of_economy": emp / total_emp if total_emp > 0 else np.nan,
                "output": float(o.sum()),
                "startup_rate": entrants / n_start[s] if n_start[s] else np.nan,
                "exit_rate": (n_start[s] - (n - entrants)) / n_start[s] if n_start[s] else np.nan,
                "adoption_rate": float(econ.ai_adopter[m].mean()) if n else 0.0,
                "small_firms": int((sz < params.small_firm_max).sum()),
                "emp_small": float(sz[sz < params.small_firm_max].sum()),
                "emp_large_now": float(sz[sz >= large].sum()),
                "emp_share_large_now": float(sz[sz >= large].sum() / emp) if emp > 0 else np.nan,
                "output_share_top1pct": _top_share(o),
                "emp_share_top1pct": _top_share(sz),
                "mean_size": emp / n if n else np.nan,
                "emp_cohort_L": float(sz[c == 2].sum()),
                "emp_cohort_B": float(sz[c == 1].sum()),
                "emp_cohort_small": float(sz[c == 0].sum()),
                "emp_entrants": float(sz[c == _ENTRANT].sum()),
                "emp_entrants_in_band": float(sz[(c == _ENTRANT) & in_band[m]].sum()),
            }
        )
    return rows


def _classify(econ, params: Parameters) -> np.ndarray:
    """Pre-shock size class indexed by firm id (``_PRE`` for ids no longer alive)."""
    pre = np.full(econ._next_id, _PRE, dtype=np.int64)
    cls = np.where(econ.size >= params.large_firm_min, 2, np.where(econ.size >= BAND_MIN, 1, 0))
    pre[econ.firm_id] = cls
    return pre


def _run(econ, params: Parameters, seed: int, t0: int, t1: int, ai_enabled: bool, pre_class: np.ndarray) -> List[dict]:
    rows = []
    for t in range(t0, t1):
        n_start = np.bincount(econ.sector, minlength=params.n_sectors)
        simulate_period(econ, t, params, seed, ai_enabled=ai_enabled)
        rows.extend(sector_record(econ, t, n_start, pre_class, params))
    return rows


def run_seed(
    seed: int,
    scenarios: Dict[str, dict],
    labor_elasticity: float,
    base: Optional[Parameters] = None,
) -> pd.DataFrame:
    """All scenarios plus the no-AI counterfactual for one seed and labour regime.

    Burn-in and pre-AI periods do not depend on exposure (AI price is infinite
    at S = 0), so they are run once and shared.
    """
    base = (base or Parameters()).with_updates(labor_supply_elasticity=labor_elasticity)
    econ = initialize_economy(base, seed)
    start = base.ai_start_period
    pre_rows = _run(econ, base, seed, 0, start, False, np.empty(0, dtype=np.int64))
    pre_class = _classify(econ, base)
    frames = [pd.DataFrame(pre_rows).assign(scenario="pre_shock")]
    for name, changes in {"counterfactual": {}, **scenarios}.items():
        p = base.with_updates(**changes)
        e = econ.copy()
        e.params = p  # Economy.update_choices reads its own params
        rows = _run(e, p, seed, start, base.n_periods, name != "counterfactual", pre_class)
        frames.append(pd.DataFrame(rows).assign(scenario=name))
    return pd.concat(frames, ignore_index=True).assign(seed=seed)


LEVEL_COLS = ["employment", "firms", "small_firms", "output", "emp_cohort_L", "emp_cohort_B", "emp_cohort_small",
              "emp_entrants_in_band", "emp_entrants"]
RATE_COLS = ["startup_rate", "exit_rate", "adoption_rate", "emp_share_of_economy", "emp_share_large_now",
             "output_share_top1pct", "emp_share_top1pct", "mean_size", "wage"]
#: AI-minus-counterfactual differences kept per seed so their standard errors can be reported.
GAP_COLS = {"startup_rate": "startup_gap", "emp_share_of_economy": "emp_share_gap",
            "emp_share_large_now": "large_share_gap", "output_share_top1pct": "top1_output_gap"}


def windows(base: Optional[Parameters] = None) -> Dict[str, tuple]:
    """Evaluation windows (inclusive period ranges): 10-19 and 25-34 years after AI starts."""
    base = base or Parameters()
    s = base.ai_start_period
    return {"medium": (s + 10, s + 19), "long": (base.n_periods - 10, base.n_periods - 1)}


def summarize(panel: pd.DataFrame, lo: int, hi: int) -> pd.DataFrame:
    """Per regime x seed x scenario x sector window means, AI vs counterfactual, for periods lo..hi."""
    keys = ["regime", "seed", "sector"]
    w = panel[(panel["period"] >= lo) & (panel["period"] <= hi)]
    win = w.groupby(["scenario"] + keys)[LEVEL_COLS + RATE_COLS].mean()
    pre = panel[panel["scenario"] == "pre_shock"].groupby(keys)["startup_rate"].mean().rename("startup_rate_pre")
    cf = win.xs("counterfactual", level="scenario")
    rows = []
    for name in win.index.get_level_values("scenario").unique():
        if name == "counterfactual":
            continue
        ai = win.xs(name, level="scenario")
        d = pd.DataFrame(index=ai.index)
        d["scenario"] = name
        for c in ("employment", "firms", "small_firms", "output"):
            d[f"{c}_ai"], d[f"{c}_cf"] = ai[c], cf[c]
        d["dN_L"] = ai["emp_cohort_L"] - cf["emp_cohort_L"]
        d["dN_B"] = (ai["emp_cohort_B"] + ai["emp_entrants_in_band"]) - (cf["emp_cohort_B"] + cf["emp_entrants_in_band"])
        inc = ["emp_cohort_L", "emp_cohort_B", "emp_cohort_small"]
        d["dN_incumbents"] = ai[inc].sum(axis=1) - cf[inc].sum(axis=1)
        d["dN_entrants"] = ai["emp_entrants"] - cf["emp_entrants"]
        for c in RATE_COLS:
            d[f"{c}_ai"], d[f"{c}_cf"] = ai[c], cf[c]
        for c, gap in GAP_COLS.items():
            d[gap] = ai[c] - cf[c]
        d["emp_effect"] = ai["employment"] / cf["employment"] - 1
        rows.append(d.join(pre))
    return pd.concat(rows).reset_index()


def _work(task) -> tuple:
    regime, eps, seed, scenarios, base, wins = task
    panel = run_seed(seed, scenarios, eps, base).assign(regime=regime)
    per_seed = pd.concat([summarize(panel, lo, hi).assign(window=name) for name, (lo, hi) in wins.items()])
    path = panel[["regime", "scenario", "sector", "period", "startup_rate", "employment"]]
    return per_seed, path


def run_all(
    seeds: Sequence[int] = range(200),
    regimes: Optional[Dict[str, float]] = None,
    scenarios: Optional[Dict[str, dict]] = None,
    base: Optional[Parameters] = None,
    workers: int = 1,
) -> tuple:
    """(per-seed window summaries, period-level startup/employment paths) over regimes x seeds."""
    regimes = LABOR_REGIMES if regimes is None else regimes
    scenarios = all_scenarios() if scenarios is None else scenarios
    wins = windows(base)
    tasks = [(r, eps, s, scenarios, base, wins) for r, eps in regimes.items() for s in seeds]
    if workers > 1:
        from concurrent.futures import ProcessPoolExecutor

        with ProcessPoolExecutor(max_workers=workers) as ex:
            results = list(ex.map(_work, tasks, chunksize=4))
    else:
        results = [_work(t) for t in tasks]
    per_seed = pd.concat([r[0] for r in results], ignore_index=True)
    paths = pd.concat([r[1] for r in results], ignore_index=True)
    return per_seed, paths


def aggregate(per_seed: pd.DataFrame, by=("window", "regime", "scenario", "sector")) -> pd.DataFrame:
    """Seed means; level effects as ratios of means; offset ratios from mean dN."""
    by = list(by)
    g = per_seed.groupby(by, sort=False)
    m = g.mean(numeric_only=True).drop(columns="seed", errors="ignore")
    n = g.size()
    for c in ("employment", "firms", "small_firms", "output"):
        if f"{c}_ai" in m:
            m[f"{c}_effect"] = m[f"{c}_ai"] / m[f"{c}_cf"] - 1
    m["emp_effect_se"] = g["emp_effect"].std(ddof=1) / np.sqrt(n)
    for gap in GAP_COLS.values():
        if gap in per_seed:
            m[f"{gap}_se"] = g[gap].std(ddof=1) / np.sqrt(n)
    with np.errstate(divide="ignore", invalid="ignore"):
        m["omega"] = np.where(m["dN_L"] < 0, m["dN_B"] / -m["dN_L"], np.nan)
        m["omega_entry"] = np.where(m["dN_incumbents"] < 0, m["dN_entrants"] / -m["dN_incumbents"], np.nan)
    shed = per_seed[per_seed["dN_L"] < 0]
    m["p_omega_ge1"] = (shed["dN_B"] >= -shed["dN_L"]).groupby([shed[k] for k in by]).mean()
    m["n_seeds"] = n
    return m


def economy_totals(per_seed: pd.DataFrame) -> pd.DataFrame:
    """Economy-wide effects (sum over sectors per seed, then mean over seeds)."""
    k = ["window", "regime", "scenario", "seed"]
    lv = ["employment_ai", "employment_cf", "output_ai", "output_cf", "dN_L", "dN_B", "dN_incumbents", "dN_entrants"]
    tot = per_seed.groupby(k, sort=False)[lv].sum().join(per_seed.groupby(k, sort=False)[["wage_ai", "wage_cf"]].first())
    tot["emp_effect"] = tot["employment_ai"] / tot["employment_cf"] - 1
    a = aggregate(tot.reset_index().assign(sector="all", startup_gap=0.0), by=("window", "regime", "scenario"))
    a["wage_effect"] = a["wage_ai"] / a["wage_cf"] - 1
    return a


def spillover(agg: pd.DataFrame, window: str = "long") -> pd.DataFrame:
    """Employment change in sectors with ZERO exposure, net of the entry channel.

    In ``high_only`` (``low_only``) the zero-exposure sectors get only the
    economy-wide entry channel plus whatever reaches them through the wage.
    Subtracting the same sector's effect under ``entry_only`` isolates the
    cross-sector (wage) spillover of AI adoption elsewhere.
    """
    out = []
    for scen, zero in (("high_only", ("goods", "trade_transport")), ("low_only", ("professional_services", "information_finance"))):
        for regime in agg.index.get_level_values("regime").unique():
            for s in zero:
                a = agg.loc[(window, regime, scen, s)]
                b = agg.loc[(window, regime, "entry_only", s)]
                out.append({"scenario": scen, "regime": regime, "zero_exposure_sector": s,
                            "emp_effect": a["employment_effect"], "emp_effect_entry_only": b["employment_effect"],
                            "spillover_pp": a["employment_effect"] - b["employment_effect"],
                            "wage_effect": a["wage_ai"] / a["wage_cf"] - 1})
    return pd.DataFrame(out).set_index(["scenario", "regime", "zero_exposure_sector"])


def _fmt_table(df: pd.DataFrame, cols: Dict[str, str], pct: Sequence[str] = (), pp: Sequence[str] = (), dec: int = 1) -> str:
    names = [n or "index" for n in df.index.names]
    lines = ["| " + " | ".join(names + list(cols.values())) + " |", "|" + "---|" * (len(names) + len(cols))]
    for idx, r in df.iterrows():
        idx = idx if isinstance(idx, tuple) else (idx,)
        cells = []
        for c in cols:
            v = r[c]
            if pd.isna(v):
                cells.append("--")
            elif c in pct:
                cells.append(f"{100 * v:+.{dec}f}%")
            elif c in pp:
                cells.append(f"{100 * v:.{dec}f}")
            elif isinstance(v, (float, np.floating)):
                cells.append(f"{v:,.2f}" if abs(v) < 100 else f"{v:,.0f}")
            else:
                cells.append(str(v))
        lines.append("| " + " | ".join(map(str, idx)) + " | " + " | ".join(cells) + " |")
    return "\n".join(lines)


SECTOR_ORDER = ("goods", "trade_transport", "professional_services", "information_finance")
SCENARIO_ORDER = ("baseline", "uniform", "high_only", "low_only", "extreme_gradient", "displacement_only", "entry_only")


def _ordered(df: pd.DataFrame, sector: bool = True) -> pd.DataFrame:
    idx = df.index.to_frame(index=False)
    idx["_s"] = idx["scenario"].map({s: i for i, s in enumerate(SCENARIO_ORDER)})
    if sector:
        idx["_k"] = idx["sector"].map({s: i for i, s in enumerate(SECTOR_ORDER)})
    order = idx.sort_values([c for c in ("_s", "_k") if c in idx]).index
    return df.iloc[order]


def report(per_seed: pd.DataFrame, paths: pd.DataFrame) -> str:
    agg = aggregate(per_seed)
    tot = economy_totals(per_seed)
    out = []
    eff = {"employment_effect": "emp", "emp_effect_se": "s.e.", "firms_effect": "firms", "small_firms_effect": "small firms",
           "output_effect": "output", "adoption_rate_ai": "adopt %", "dN_L": "dN_L", "dN_B": "dN_B", "omega": "Omega",
           "p_omega_ge1": "P(Omega>=1) %", "dN_incumbents": "dN_inc", "dN_entrants": "dN_ent", "omega_entry": "Omega_ent"}
    pct = ("employment_effect", "emp_effect_se", "firms_effect", "small_firms_effect", "output_effect")
    for window in ("medium", "long"):
        t = _ordered(tot.xs(window, level="window").reorder_levels(["scenario", "regime"]), sector=False)
        out.append(f"### Economy-wide, {window} window\n")
        out.append(_fmt_table(t, {"employment_effect": "emp", "emp_effect_se": "s.e.", "output_effect": "output",
                                  "wage_effect": "wage", "dN_L": "dN_L", "dN_B": "dN_B", "omega": "Omega",
                                  "dN_incumbents": "dN_inc", "dN_entrants": "dN_ent", "omega_entry": "Omega_ent"},
                              pct=("employment_effect", "emp_effect_se", "output_effect", "wage_effect"), dec=2))
        for regime in LABOR_REGIMES:
            a = _ordered(agg.xs((window, regime), level=("window", "regime")))
            out.append(f"\n### {regime}, {window} window: employment and offset by sector\n")
            out.append(_fmt_table(a, eff, pct=pct, pp=("adoption_rate_ai", "p_omega_ge1")))
        out.append("")
    for regime in LABOR_REGIMES:
        a = _ordered(agg.xs(("long", regime), level=("window", "regime")))
        out.append(f"\n### {regime}, long window: startup rates, concentration, reallocation (all in %)\n")
        cols = {"startup_rate_pre": "startup pre", "startup_rate_cf": "startup CF", "startup_rate_ai": "startup AI",
                "startup_gap": "AI-CF", "startup_gap_se": "s.e.",
                "emp_share_of_economy_cf": "emp share CF", "emp_share_gap": "AI-CF", "emp_share_gap_se": "s.e.",
                "emp_share_large_now_cf": "500+ share CF", "large_share_gap": "AI-CF", "large_share_gap_se": "s.e.",
                "output_share_top1pct_cf": "top1% output CF", "top1_output_gap": "AI-CF", "top1_output_gap_se": "s.e."}
        out.append(_fmt_table(a, cols, pp=tuple(cols), dec=2))
    out.append("\n### Cross-sector spillover into zero-exposure sectors (long window)\n")
    out.append(_fmt_table(spillover(agg), {"emp_effect": "emp effect", "emp_effect_entry_only": "entry-only effect",
                                           "spillover_pp": "spillover", "wage_effect": "wage"},
                          pct=("emp_effect", "emp_effect_entry_only", "spillover_pp", "wage_effect"), dec=2))
    pe = paths[paths["regime"] == "PE"].groupby(["scenario", "sector", "period"])["startup_rate"].mean()
    cf = pe.xs("counterfactual", level="scenario")
    gap = (pe.drop(index=["pre_shock", "counterfactual"], level="scenario") - cf).dropna().unstack("period")
    start = Parameters().ai_start_period
    sel = {f"yr{k}": start + k for k in (0, 5, 8, 10, 15, 20, 34)}
    tr = pd.DataFrame({lab: gap[p] for lab, p in sel.items()})
    tr["peak"], tr["peak_yr"] = gap.max(axis=1), gap.idxmax(axis=1) - start
    out.append("\n### PE: startup-rate gap AI minus CF over the transition (pp; yrK = K years after AI start)\n")
    out.append(_fmt_table(_ordered(tr), {**{k: k for k in sel}, "peak": "peak", "peak_yr": "peak yr"}, pp=tuple(sel) + ("peak",), dec=2))
    return "\n".join(out)


def main(out_dir: Optional[Path] = None, n_seeds: int = 200, workers: int = 6) -> str:
    root = Path(__file__).resolve().parents[1]
    out_dir = out_dir or root / "data"
    per_seed, paths = run_all(range(n_seeds), workers=workers)
    aggregate(per_seed).to_csv(out_dir / "sector_analysis_results.csv")
    economy_totals(per_seed).to_csv(out_dir / "sector_analysis_totals.csv")
    text = report(per_seed, paths)
    (out_dir / "sector_analysis_tables.md").write_text(
        f"<!-- generated by `python -m model.sector_analysis` ({n_seeds} seeds); do not edit by hand -->\n\n{text}\n"
    )
    return text


if __name__ == "__main__":
    print(main())
