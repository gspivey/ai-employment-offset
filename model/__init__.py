"""PlayEcon firm-dynamics model of AI productivity shocks.

Hopenhayn (1992) / Luttmer (2007) heterogeneous-firm dynamics with an AI
shock that (a) lowers entry costs, (b) shifts the entrant productivity
distribution and (c) lets adopting firms substitute AI for labour, shifting
optimal headcount down at the large firms that adopt. The question the model
is built to answer: does small-firm proliferation offset large-firm
headcount reduction in aggregate employment?
"""

from .firm_dynamics import (
    AIState,
    Economy,
    Firm,
    FirmChoices,
    ai_headcount_ratio,
    ai_productivity_shock,
    entry_probability,
    entry_value,
    exit_probability,
    exit_productivity_cutoff,
    exit_rate,
    expected_entry,
    firm_choices,
    labor_demand,
    potential_entrant_mass,
    solve_wage,
)
from .monte_carlo import MonteCarloResult, ParameterUncertainty, default_uncertainty, run_monte_carlo
from .parameters import Parameters
from .simulation import (
    compare_scenarios,
    employment_effects,
    initialize_economy,
    run_simulation,
    simulate_period,
)

__all__ = [
    "AIState",
    "Economy",
    "Firm",
    "FirmChoices",
    "MonteCarloResult",
    "ParameterUncertainty",
    "Parameters",
    "ai_headcount_ratio",
    "ai_productivity_shock",
    "compare_scenarios",
    "default_uncertainty",
    "employment_effects",
    "entry_probability",
    "entry_value",
    "exit_probability",
    "exit_productivity_cutoff",
    "exit_rate",
    "expected_entry",
    "firm_choices",
    "initialize_economy",
    "labor_demand",
    "potential_entrant_mass",
    "run_monte_carlo",
    "run_simulation",
    "simulate_period",
    "solve_wage",
]
