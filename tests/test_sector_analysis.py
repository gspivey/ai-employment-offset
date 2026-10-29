"""Tests for the sector-level scenario runner (model/sector_analysis.py)."""

import numpy as np
import pandas as pd
import pytest

from model import Parameters
from model.sector_analysis import aggregate, run_seed, summarize, windows

FAST = dict(initial_firms=300, potential_entrants=150.0, burn_in=60, n_periods=25, ai_start_period=3)
NO_AI = {"sector_ai_exposure": (0.0, 0.0, 0.0, 0.0), "entry_cost_post": 20.0, "ai_entrant_productivity_shift": 0.0}


@pytest.fixture(scope="module")
def base():
    return Parameters(**FAST)


@pytest.fixture(scope="module")
def panel(base):
    scen = {"null": NO_AI, "high_only": {"sector_ai_exposure": (0.0, 0.0, 1.2, 1.5)}}
    return run_seed(3, scen, float("inf"), base).assign(regime="PE")


def test_sector_rows_partition_the_economy(panel, base):
    per = panel.groupby(["scenario", "period"])
    assert (per.size() == base.n_sectors).all()
    np.testing.assert_allclose(per["emp_share_of_economy"].sum(), 1.0)
    cohorts = panel[["emp_cohort_L", "emp_cohort_B", "emp_cohort_small", "emp_entrants"]].sum(axis=1)
    np.testing.assert_allclose(cohorts, panel["employment"])


def test_zero_exposure_sector_never_adopts(panel):
    hi = panel[panel["scenario"] == "high_only"]
    assert (hi.loc[hi["sector"].isin(["goods", "trade_transport"]), "adoption_rate"] == 0).all()


def test_null_shock_reproduces_counterfactual(panel, base):
    lo, hi = windows(base)["long"]
    s = summarize(panel, lo, hi)
    null = s[s["scenario"] == "null"]
    for c in ("dN_L", "dN_B", "dN_incumbents", "dN_entrants", "startup_gap"):
        np.testing.assert_allclose(null[c], 0.0, atol=1e-9)


def test_offset_ratio_from_mean_changes():
    df = pd.DataFrame(
        {
            "window": "long", "regime": "PE", "scenario": "s", "sector": "x", "seed": [0, 1],
            "dN_L": [-10.0, -30.0], "dN_B": [5.0, 45.0], "dN_incumbents": [-20.0, -20.0], "dN_entrants": [10.0, 30.0],
            "emp_effect": [0.0, 0.0], "startup_gap": [0.0, 0.0],
        }
    )
    a = aggregate(df).iloc[0]
    assert a["omega"] == pytest.approx(25.0 / 20.0)
    assert a["omega_entry"] == pytest.approx(1.0)
    assert a["p_omega_ge1"] == pytest.approx(0.5)
