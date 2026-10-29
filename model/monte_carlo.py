"""Monte Carlo engine: replications over parameter draws and shock histories.

Each replication draws a parameter vector from :class:`ParameterUncertainty`,
burns in one pre-AI economy, then runs the AI scenario and a no-AI
counterfactual from copies of it with the same seed. Outcomes are
AI-vs-counterfactual differences averaged over the final ``eval_window``
periods (see :func:`model.simulation.employment_effects`), so both parameter
uncertainty and simulation noise feed the reported distribution.
"""

from __future__ import annotations

from concurrent.futures import ProcessPoolExecutor
from dataclasses import dataclass, field
from typing import Any, Dict, Optional, Sequence

import numpy as np
import pandas as pd
from scipy import stats

from .parameters import Parameters
from .simulation import compare_scenarios, employment_effects

DEFAULT_PERCENTILES = (5, 25, 50, 75, 95)


@dataclass
class ParameterUncertainty:
    """Independent priors over a subset of :class:`Parameters` fields.

    ``distributions`` maps field name -> frozen ``scipy.stats`` distribution.
    Fields not listed keep their base values.
    """

    distributions: Dict[str, Any] = field(default_factory=dict)

    def draw(self, rng: np.random.Generator) -> Dict[str, float]:
        return {name: float(dist.rvs(random_state=rng)) for name, dist in self.distributions.items()}

    def apply(self, base: Parameters, rng: np.random.Generator) -> Parameters:
        return base.with_updates(**self.draw(rng))


def default_uncertainty() -> ParameterUncertainty:
    """Placeholder priors; ranges are deliberately wide pending calibration.

    sigma_ai straddles the displacement threshold 1/(1-alpha) ~ 2.78, so the
    sign of the adopter headcount response is itself uncertain.
    """
    return ParameterUncertainty(
        {
            "sigma_ai": stats.uniform(loc=2.0, scale=3.0),  # U[2, 5]
            "ai_cost_full": stats.lognorm(s=0.4, scale=1.5),  # median 1.5
            "ai_adoption_fixed_cost": stats.uniform(loc=2.0, scale=8.0),  # U[2, 10]
            "entry_cost_post": stats.uniform(loc=10.0, scale=10.0),  # U[10, 20]: 0-50% cut from 20
            "entry_pool_elasticity": stats.uniform(loc=0.0, scale=0.6),  # U[0, 0.6]
            "ai_entrant_productivity_shift": stats.uniform(loc=0.0, scale=0.1),  # U[0, 0.1]
        }
    )


@dataclass
class MonteCarloResult:
    """Per-replication draws/outcomes and (optionally) trajectories."""

    draws: pd.DataFrame  # one row per replication: drawn params + outcomes
    trajectories: Optional[pd.DataFrame]  # long format: replication, period, scenario-specific columns
    outcome_columns: Sequence[str]

    def summary(self, percentiles: Sequence[float] = DEFAULT_PERCENTILES) -> pd.DataFrame:
        """Mean, std, percentiles and P(<0) of each outcome across replications."""
        out = self.draws[list(self.outcome_columns)]
        table = pd.DataFrame({"mean": out.mean(), "std": out.std(ddof=1)})
        for p in percentiles:
            table[f"p{p:g}"] = out.quantile(p / 100.0)
        table["prob_negative"] = (out < 0).mean()
        table["n"] = out.notna().sum()
        return table

    def net_employment_effect(self, percentiles: Sequence[float] = DEFAULT_PERCENTILES) -> pd.Series:
        return self.summary(percentiles).loc["net_employment_effect"]

    def trajectory_bands(self, column: str = "employment_effect", percentiles: Sequence[float] = DEFAULT_PERCENTILES) -> pd.DataFrame:
        """Per-period mean and percentile bands of a trajectory column."""
        if self.trajectories is None:
            raise ValueError("run_monte_carlo(..., keep_trajectories=False) dropped trajectories")
        g = self.trajectories.groupby("period")[column]
        bands = pd.DataFrame({"mean": g.mean()})
        for p in percentiles:
            bands[f"p{p:g}"] = g.quantile(p / 100.0)
        return bands


def _run_replication(task) -> tuple:
    rep, params, seed, n_periods, eval_window, keep_trajectories = task
    ai, cf = compare_scenarios(params, seed=int(seed), n_periods=n_periods)
    outcomes = employment_effects(ai, cf, params, window=eval_window)
    traj = None
    if keep_trajectories:
        traj = pd.DataFrame(
            {
                "replication": rep,
                "period": ai.index,
                "ai_diffusion": ai["ai_diffusion"].to_numpy(),
                "employment_ai": ai["aggregate_employment"].to_numpy(),
                "employment_cf": cf["aggregate_employment"].to_numpy(),
                "firms_ai": ai["n_firms"].to_numpy(),
                "firms_cf": cf["n_firms"].to_numpy(),
                "adoption_rate": ai["adoption_rate"].to_numpy(),
            }
        )
        traj["employment_effect"] = traj["employment_ai"] / traj["employment_cf"] - 1.0
        traj["firm_count_effect"] = traj["firms_ai"] / traj["firms_cf"] - 1.0
    return outcomes, traj


def run_monte_carlo(
    n_replications: int = 100,
    base_params: Optional[Parameters] = None,
    uncertainty: Optional[ParameterUncertainty] = None,
    seed: int = 0,
    n_periods: Optional[int] = None,
    eval_window: int = 10,
    n_jobs: int = 1,
    keep_trajectories: bool = True,
) -> MonteCarloResult:
    """Run ``n_replications`` AI-vs-counterfactual simulations with parameter draws.

    ``uncertainty=None`` uses :func:`default_uncertainty`; pass
    ``ParameterUncertainty()`` to hold parameters fixed and isolate
    simulation noise. ``n_jobs > 1`` runs replications in worker processes;
    results are identical to ``n_jobs=1`` for the same seed.
    """
    base = base_params or Parameters()
    unc = default_uncertainty() if uncertainty is None else uncertainty
    T = base.n_periods if n_periods is None else int(n_periods)
    if eval_window > T:
        raise ValueError("eval_window cannot exceed n_periods")

    param_rng = np.random.default_rng(np.random.SeedSequence(seed).spawn(1)[0])
    sim_seeds = np.random.SeedSequence(seed).generate_state(n_replications, dtype=np.uint32)
    drawn = [unc.draw(param_rng) for _ in range(n_replications)]
    tasks = [
        (rep, base.with_updates(**d), sim_seeds[rep], T, eval_window, keep_trajectories)
        for rep, d in enumerate(drawn)
    ]

    if n_jobs > 1:
        with ProcessPoolExecutor(max_workers=n_jobs) as pool:
            results = list(pool.map(_run_replication, tasks))
    else:
        results = [_run_replication(t) for t in tasks]

    outcomes = [r[0] for r in results]
    outcome_cols = list(outcomes[0].keys()) if outcomes else []
    draws = pd.concat(
        [pd.DataFrame(drawn, index=range(n_replications)), pd.DataFrame(outcomes, index=range(n_replications))],
        axis=1,
    )
    draws.index.name = "replication"
    draws.insert(0, "seed", sim_seeds)
    traj = pd.concat([r[1] for r in results], ignore_index=True) if keep_trajectories and results else None
    return MonteCarloResult(draws=draws, trajectories=traj, outcome_columns=outcome_cols)
