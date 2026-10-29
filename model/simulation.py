"""Simulation harness: period-by-period firm dynamics with history tracking.

Timing within a period t:

1. exogenous exit (prob. delta);
2. incumbents draw new productivity and age one year;
3. endogenous exit: incumbents whose best net profit (at last period's wage
   and today's AI technology) is below the exit threshold leave;
4. entry: a Poisson(M(c_e)) pool of potential entrants draws productivity;
   those with V(z) >= c_e enter;
5. the wage clears the labour market (or stays at wage0 in partial equilibrium);
6. firms choose AI adoption and employment; the period is recorded.

Randomness is keyed on (seed, period, firm_id): every draw for period t comes
from generators seeded by ``SeedSequence([seed, phase, t, stream])`` and
firm-level shocks are indexed by firm id. Two scenarios run from the same
economy with the same seed therefore hit each surviving firm with the same
productivity and exit shocks (common random numbers), which removes most
simulation noise from AI-vs-counterfactual comparisons.
"""

from __future__ import annotations

from typing import Dict, NamedTuple, Optional, Tuple

import numpy as np
import pandas as pd

from .firm_dynamics import (
    Economy,
    ai_productivity_shock,
    draw_potential_entrants,
    entry_value,
    evolve_productivity,
    firm_choices,
    potential_entrant_mass,
    solve_wage,
)
from .parameters import Parameters


_RUN, _BURN_IN, _INIT = 0, 1, 2  # seed-key phases


class _Streams(NamedTuple):
    exit: np.random.Generator
    productivity: np.random.Generator
    entrant_count: np.random.Generator
    entrant_productivity: np.random.Generator
    entrant_sector: np.random.Generator


def _streams(seed: int, phase: int, t: int) -> _Streams:
    return _Streams(*(np.random.default_rng(s) for s in np.random.SeedSequence([seed, phase, t]).spawn(5)))


def resolve_seed(seed=None) -> int:
    """Non-negative integer seed; fresh OS entropy when ``seed`` is None."""
    return int(np.random.SeedSequence().entropy) if seed is None else int(seed)


def initialize_economy(params: Parameters, seed=None) -> Economy:
    """Seed firms from the entrant distribution and burn in to the pre-AI steady state.

    At the end of burn-in the labour-supply scale L_bar is set to current
    employment, so the labour market clears at wage0 in the pre-AI economy.
    """
    seed = resolve_seed(seed)
    econ = Economy(params)
    st = _streams(seed, _INIT, 0)
    z, sector = draw_potential_entrants(params.initial_firms, params, st.entrant_productivity)
    econ.add_firms(z, sector)
    econ.update_choices(params.wage0, ai_productivity_shock(0.0, params).ai_cost)
    for t in range(params.burn_in):
        simulate_period(econ, t, params, seed, ai_enabled=False, _phase=_BURN_IN)
    econ.labor_supply_scale = econ.aggregate_employment
    return econ


def simulate_period(
    economy: Economy,
    t: int,
    params: Parameters,
    seed: int,
    ai_enabled: bool = True,
    _phase: int = _RUN,
) -> Dict[str, float]:
    """Advance ``economy`` one period in place and return that period's record.

    ``seed`` is the run key; all randomness for period ``t`` is derived from
    (seed, t) and, for firm-level shocks, the firm id.
    """
    st = _streams(seed, _phase, t)
    ai = ai_productivity_shock(params.ai_diffusion(t) if ai_enabled else 0.0, params)
    n_start = economy.n_firms
    n_ids = economy._next_id

    # 1. exogenous exit
    survive = st.exit.random(n_ids)[economy.firm_id] >= params.exog_exit_rate
    exits_exog = int(n_start - survive.sum())
    economy.keep(survive)

    # 2. productivity shocks and ageing
    shocks = st.productivity.standard_normal(n_ids)[economy.firm_id]
    economy.productivity = evolve_productivity(economy.productivity, params, shocks=shocks)
    economy.age = economy.age + 1

    # 3. endogenous exit at last period's wage
    ch = firm_choices(economy.productivity, economy.sector, economy.wage, ai.ai_cost, params)
    stay = ch.net_profit >= params.exit_profit_threshold
    exits_endo = int((~stay).sum())
    economy.keep(stay)

    # 4. entry
    n_pot = int(st.entrant_count.poisson(potential_entrant_mass(ai.entry_cost, params)))
    z_new, sec_new = draw_potential_entrants(
        n_pot, params, st.entrant_productivity, ai.entrant_productivity_shift, sector_rng=st.entrant_sector
    )
    if n_pot:
        enter = entry_value(z_new, sec_new, economy.wage, ai.ai_cost, params) >= ai.entry_cost
        economy.add_firms(z_new[enter], sec_new[enter])
        entrants = int(enter.sum())
    else:
        entrants = 0

    # 5-6. wage and production choices
    wage = solve_wage(economy.productivity, economy.sector, ai.ai_cost, params, economy.labor_supply_scale)
    economy.update_choices(wage, ai.ai_cost)

    return _record(economy, t, params, ai.diffusion, ai.entry_cost, n_start, n_pot, entrants, exits_exog, exits_endo)


def _record(economy, t, params, diffusion, entry_cost, n_start, n_pot, entrants, exits_exog, exits_endo):
    emp = economy.aggregate_employment
    n = economy.n_firms
    exits = exits_exog + exits_endo
    rec = {
        "period": t,
        "ai_diffusion": diffusion,
        "entry_cost": entry_cost,
        "wage": economy.wage,
        "n_firms": n,
        "potential_entrants": n_pot,
        "entrants": entrants,
        "exits": exits,
        "exits_exogenous": exits_exog,
        "exits_endogenous": exits_endo,
        "entry_rate": entrants / n_start if n_start else np.nan,
        "exit_rate": exits / n_start if n_start else np.nan,
        "aggregate_employment": emp,
        "mean_firm_size": emp / n if n else np.nan,
        "output": float(economy.output.sum()),
        "adoption_rate": float(economy.ai_adopter.mean()) if n else 0.0,
        "adopter_employment_share": float(economy.size[economy.ai_adopter].sum() / emp) if emp > 0 else 0.0,
    }
    dist = economy.size_distribution()
    for label, row in dist.iterrows():
        rec[f"emp_{label}"] = float(row["employment"])
    for label, row in dist.iterrows():
        rec[f"firms_{label}"] = int(row["firms"])
    return rec


def run_simulation(
    params: Optional[Parameters] = None,
    n_periods: Optional[int] = None,
    seed=None,
    *,
    ai_enabled: bool = True,
    economy: Optional[Economy] = None,
) -> pd.DataFrame:
    """Simulate a full trajectory and return one row per period.

    Columns include ``aggregate_employment``, entry/exit counts and rates,
    ``wage``, AI ``adoption_rate`` and, for every size bucket, ``emp_<bucket>``
    and ``firms_<bucket>``.

    If ``economy`` is None a fresh one is initialised (and burned in) from
    ``seed``. A supplied economy is advanced in place. Shocks are keyed on
    (seed, period, firm id), so runs from copies of the same economy with the
    same seed share common random numbers firm by firm.
    """
    params = params or Parameters()
    T = params.n_periods if n_periods is None else int(n_periods)
    seed = resolve_seed(seed)
    if economy is None:
        economy = initialize_economy(params, seed)
    rows = [simulate_period(economy, t, params, seed, ai_enabled=ai_enabled) for t in range(T)]
    df = pd.DataFrame(rows).set_index("period")
    df.attrs.update(ai_enabled=ai_enabled, ai_start_period=params.ai_start_period, seed=seed)
    return df


def compare_scenarios(
    params: Optional[Parameters] = None,
    seed=None,
    n_periods: Optional[int] = None,
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Run AI and no-AI counterfactual from the same burned-in economy and seed."""
    params = params or Parameters()
    seed = resolve_seed(seed)
    base = initialize_economy(params, seed)
    ai = run_simulation(params, n_periods, seed, ai_enabled=True, economy=base.copy())
    cf = run_simulation(params, n_periods, seed, ai_enabled=False, economy=base)
    return ai, cf


def size_class_columns(params: Parameters) -> Tuple[list, list]:
    """Bucket labels classed as small (upper edge <= small_firm_max) and large
    (lower edge >= large_firm_min)."""
    edges = params.size_bucket_edges
    labels = params.size_bucket_labels()
    small = [lab for lab, hi in zip(labels, edges[1:]) if hi <= params.small_firm_max]
    large = [lab for lab, lo in zip(labels, edges[:-1]) if lo >= params.large_firm_min]
    return small, large


def employment_effects(ai: pd.DataFrame, cf: pd.DataFrame, params: Parameters, window: int = 10) -> Dict[str, float]:
    """AI-vs-counterfactual effects, averaged over the last ``window`` periods.

    Effects are proportional differences, e.g. net_employment_effect = -0.05
    means AI lowers aggregate employment by 5% relative to no AI.
    """
    a, c = ai.iloc[-window:], cf.iloc[-window:]
    small, large = size_class_columns(params)

    def pct(x_ai: float, x_cf: float) -> float:
        return x_ai / x_cf - 1.0 if x_cf > 0 else np.nan

    def total(df, prefix, labels):
        return float(df[[f"{prefix}_{lab}" for lab in labels]].sum(axis=1).mean()) if labels else 0.0

    return {
        "net_employment_effect": pct(a["aggregate_employment"].mean(), c["aggregate_employment"].mean()),
        "firm_count_effect": pct(a["n_firms"].mean(), c["n_firms"].mean()),
        "small_firm_count_effect": pct(total(a, "firms", small), total(c, "firms", small)),
        "small_firm_employment_effect": pct(total(a, "emp", small), total(c, "emp", small)),
        "large_firm_employment_effect": pct(total(a, "emp", large), total(c, "emp", large)),
        "mean_firm_size_effect": pct(a["mean_firm_size"].mean(), c["mean_firm_size"].mean()),
        "output_effect": pct(a["output"].mean(), c["output"].mean()),
        "wage_effect": pct(a["wage"].mean(), c["wage"].mean()),
        "entry_rate_change": float(a["entry_rate"].mean() - c["entry_rate"].mean()),
        "adoption_rate": float(a["adoption_rate"].mean()),
        "adopter_employment_share": float(a["adopter_employment_share"].mean()),
    }
