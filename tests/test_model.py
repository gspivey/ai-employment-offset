"""Smoke and sanity tests for the firm-dynamics model."""

import math

import numpy as np
import pandas as pd
import pytest

from model import (
    Economy,
    Firm,
    Parameters,
    ParameterUncertainty,
    ai_headcount_ratio,
    ai_productivity_shock,
    compare_scenarios,
    employment_effects,
    exit_probability,
    exit_productivity_cutoff,
    expected_entry,
    firm_choices,
    run_monte_carlo,
    run_simulation,
    solve_wage,
)
from model.calibration import BASELINE_TARGETS, moment_distance, pareto_tail_exponent, simulated_moments
from model.firm_dynamics import ces_unit_cost, optimal_input

# Small, fast economy for tests.
FAST = dict(initial_firms=300, potential_entrants=150.0, burn_in=60, n_periods=25, ai_start_period=3)


@pytest.fixture(scope="module")
def fast_params():
    return Parameters(**FAST)


@pytest.fixture(scope="module")
def scenario_pair(fast_params):
    return compare_scenarios(fast_params, seed=11)


# --- parameters -------------------------------------------------------------


def test_default_parameters_valid():
    p = Parameters()
    assert p.theta == pytest.approx(1 / (1 - p.alpha))
    assert p.sigma_ai > p.displacement_threshold  # default: AI shrinks adopters' headcount
    assert len(p.size_bucket_labels()) == len(p.size_bucket_edges) - 1
    assert p.size_bucket_labels()[-1] == "500_plus"


@pytest.mark.parametrize(
    "bad",
    [dict(alpha=1.2), dict(sigma_ai=0.8), dict(sector_shares=(0.5, 0.5, 0.5, 0.5)), dict(entry_cost_post=0.0)],
)
def test_parameter_validation(bad):
    with pytest.raises(ValueError):
        Parameters(**bad)


def test_ai_diffusion_schedule():
    p = Parameters(ai_start_period=5)
    s = [p.ai_diffusion(t) for t in range(60)]
    assert all(v == 0.0 for v in s[:6])
    assert all(b >= a for a, b in zip(s, s[1:]))
    assert s[-1] == pytest.approx(p.ai_diffusion_ceiling, abs=1e-6)
    explicit = Parameters(ai_start_period=2, ai_schedule=(0.1, 0.5))
    assert [explicit.ai_diffusion(t) for t in range(5)] == [0.0, 0.0, 0.1, 0.5, 0.5]


# --- firm problem -----------------------------------------------------------


def test_non_adopter_foc():
    """Marginal product of labour equals the wage at the optimum."""
    p = Parameters()
    z, w = np.array([1.5, 2.5, 4.0]), 1.3
    n = optimal_input(z, w, p.alpha)
    mpl = p.alpha * z * n ** (p.alpha - 1)
    np.testing.assert_allclose(mpl, w)


def test_ai_unavailable_means_no_adoption():
    p = Parameters()
    off = ai_productivity_shock(0.0, p)
    assert np.all(np.isinf(off.ai_cost))
    ch = firm_choices(np.array([1.0, 5.0, 50.0]), np.array([0, 1, 3]), 1.0, off.ai_cost, p)
    assert not ch.adopt.any()
    np.testing.assert_allclose(ces_unit_cost(1.0, np.inf, p.sigma_ai), 1.0)


def test_large_firms_adopt_and_shrink():
    p = Parameters()
    on = ai_productivity_shock(1.0, p)
    z = np.exp(np.linspace(0.5, 4.0, 200))
    sector = np.full(z.size, 3)
    with_ai = firm_choices(z, sector, 1.0, on.ai_cost, p)
    no_ai = firm_choices(z, sector, 1.0, np.full(p.n_sectors, np.inf), p)
    assert with_ai.adopt.any() and not with_ai.adopt.all()
    # adoption is monotone in productivity: a single size cutoff
    first = np.argmax(with_ai.adopt)
    assert with_ai.adopt[first:].all() and not with_ai.adopt[:first].any()
    ratio = with_ai.employment[with_ai.adopt] / no_ai.employment[with_ai.adopt]
    np.testing.assert_allclose(ratio, ai_headcount_ratio(1.0, on.ai_cost[3], p))
    assert np.all(ratio < 1.0)
    assert np.all(with_ai.output >= no_ai.output - 1e-12)


def test_low_substitutability_means_adopters_grow():
    p = Parameters(sigma_ai=2.0)  # below 1/(1-alpha) ~ 2.78: scale effect dominates
    on = ai_productivity_shock(1.0, p)
    assert np.all(ai_headcount_ratio(1.0, on.ai_cost[np.isfinite(on.ai_cost)], p) > 1.0)


def test_entry_increases_as_barriers_fall():
    p = Parameters()
    off = ai_productivity_shock(0.0, p).ai_cost
    e_hi = expected_entry(p.entry_cost_pre, 1.0, off, p)
    e_lo = expected_entry(p.entry_cost_post, 1.0, off, p)
    assert e_lo > e_hi > 0


def test_exit_threshold():
    p = Parameters()
    cut = exit_productivity_cutoff(1.0, p)
    off = ai_productivity_shock(0.0, p).ai_cost
    ch = firm_choices(np.array([cut * 0.99, cut * 1.01]), np.array([0, 0]), 1.0, off, p)
    assert ch.net_profit[0] < 0 < ch.net_profit[1]
    probs = exit_probability(np.array([cut * 0.5, cut, cut * 5]), 1.0, p)
    assert np.all(np.diff(probs) < 0)
    assert probs[-1] >= p.exog_exit_rate


def test_wage_clears_labor_market():
    p = Parameters(labor_supply_elasticity=0.5)
    rng = np.random.default_rng(0)
    z = np.exp(rng.normal(1.0, 0.7, 500))
    sector = rng.integers(0, p.n_sectors, 500)
    on = ai_productivity_shock(1.0, p).ai_cost
    L_bar = 4000.0
    w = solve_wage(z, sector, on, p, L_bar)
    demand = firm_choices(z, sector, w, on, p).employment.sum()
    supply = L_bar * (w / p.wage0) ** p.labor_supply_elasticity
    assert demand == pytest.approx(supply, rel=1e-3)
    assert solve_wage(z, sector, on, Parameters(), L_bar) == 1.0  # PE default


# --- economy container ------------------------------------------------------


def test_economy_roundtrip_and_distribution():
    p = Parameters()
    firms = [Firm(size=3, productivity=1.2, age=1, sector=0), Firm(size=700, productivity=9.0, age=20, sector=2)]
    econ = Economy.from_firms(firms, p)
    assert econ.n_firms == 2 and econ.aggregate_employment == 703
    back = econ.firms
    assert back[1].size == 700 and back[1].sector == 2 and back[0].firm_id == 0
    dist = econ.size_distribution()
    assert dist.loc["0_4", "firms"] == 1 and dist.loc["500_plus", "employment"] == 700
    assert dist["employment_share"].sum() == pytest.approx(1.0)


# --- simulation -------------------------------------------------------------


def test_run_simulation_returns_trajectories(fast_params):
    df = run_simulation(fast_params, seed=3)
    assert isinstance(df, pd.DataFrame)
    assert len(df) == fast_params.n_periods
    labels = fast_params.size_bucket_labels()
    for col in ["aggregate_employment", "entrants", "exits", "n_firms", "wage", "adoption_rate"]:
        assert col in df.columns
    emp_cols = [f"emp_{b}" for b in labels]
    assert set(emp_cols) <= set(df.columns)
    assert not df[emp_cols + ["aggregate_employment", "n_firms"]].isna().any().any()
    np.testing.assert_allclose(df[emp_cols].sum(axis=1), df["aggregate_employment"])
    assert (df["aggregate_employment"] > 0).all()
    assert df["entry_rate"].between(0.0, 0.5).all() and df["exit_rate"].between(0.0, 0.5).all()
    assert df["ai_diffusion"].iloc[0] == 0.0 and df["ai_diffusion"].iloc[-1] > 0.5


def test_simulation_is_reproducible(fast_params):
    a = run_simulation(fast_params, seed=5)
    b = run_simulation(fast_params, seed=5)
    pd.testing.assert_frame_equal(a, b)


def test_scenarios_identical_before_ai(scenario_pair, fast_params):
    ai, cf = scenario_pair
    pre = slice(0, fast_params.ai_start_period)
    pd.testing.assert_frame_equal(ai.loc[pre], cf.loc[pre])
    assert (cf["adoption_rate"] == 0).all()


def test_ai_scenario_direction(scenario_pair, fast_params):
    """Default calibration: more firms, more small-firm employment, smaller average firm."""
    ai, cf = scenario_pair
    eff = employment_effects(ai, cf, fast_params, window=8)
    assert eff["firm_count_effect"] > 0
    assert eff["small_firm_employment_effect"] > 0
    assert eff["mean_firm_size_effect"] < 0
    assert eff["adoption_rate"] > 0
    assert math.isfinite(eff["net_employment_effect"])


def test_general_equilibrium_run(fast_params):
    p = fast_params.with_updates(labor_supply_elasticity=0.5)
    ai, cf = compare_scenarios(p, seed=2)
    # L_bar is set at the end of burn-in, so wages start at ~wage0 and then
    # fluctuate with the firm population.
    assert cf["wage"].iloc[0] == pytest.approx(p.wage0, rel=0.05)
    assert cf["wage"].between(0.8, 1.25).all()
    assert ai["wage"].nunique() > 1
    assert not np.allclose(ai["wage"].iloc[-5:], cf["wage"].iloc[-5:])


# --- monte carlo ------------------------------------------------------------


def test_monte_carlo_summary(fast_params):
    mc = run_monte_carlo(n_replications=4, base_params=fast_params, seed=1, eval_window=5)
    assert len(mc.draws) == 4
    summ = mc.summary()
    for col in ["mean", "std", "p5", "p50", "p95", "prob_negative"]:
        assert col in summ.columns
    row = mc.net_employment_effect()
    assert np.isfinite(row["mean"]) and row["p5"] <= row["p50"] <= row["p95"]
    assert mc.draws["sigma_ai"].between(2.0, 5.0).all()
    bands = mc.trajectory_bands()
    assert len(bands) == fast_params.n_periods


def test_monte_carlo_reproducible_and_fixed_params(fast_params):
    a = run_monte_carlo(n_replications=2, base_params=fast_params, uncertainty=ParameterUncertainty(), seed=9, eval_window=5)
    b = run_monte_carlo(n_replications=2, base_params=fast_params, uncertainty=ParameterUncertainty(), seed=9, eval_window=5)
    pd.testing.assert_frame_equal(a.draws, b.draws)


# --- calibration ------------------------------------------------------------


def test_calibration_moments(fast_params):
    from model.simulation import initialize_economy

    econ = initialize_economy(fast_params, seed=4)
    hist = run_simulation(fast_params, seed=4, ai_enabled=False, economy=econ)
    m = simulated_moments(hist, fast_params, economy=econ)
    assert 0 < m["entry_rate"] < 0.5 and 0 < m["firm_share_small"] <= 1
    assert np.isfinite(moment_distance(m, BASELINE_TARGETS))
    rng = np.random.default_rng(0)
    sizes = 100 * (1 + rng.pareto(1.1, 20000))
    assert pareto_tail_exponent(sizes, 100) == pytest.approx(1.1, rel=0.05)
