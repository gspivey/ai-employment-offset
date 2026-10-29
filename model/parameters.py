"""Model parameters with documented defaults.

Units: one period is one year; all costs are in units of the pre-AI annual
wage of one worker (``wage0 = 1``). Defaults are *placeholders* chosen to give
a plausible pre-AI steady state (entry/exit rates of roughly 7%, mean
firm size ~30, a right-skewed size distribution); they are not yet calibrated -- see
``model/calibration.py`` for the empirical targets.

The AI shock enters through three channels, all scaled by a diffusion index
``S(t)`` in [0, 1] (see :meth:`Parameters.ai_diffusion`):

(a) entry cost falls linearly from ``entry_cost_pre`` to ``entry_cost_post``;
(b) the entrant productivity distribution shifts up by
    ``ai_entrant_productivity_shift`` (log points) -- "AI-native" startups;
(c) the effective price of AI services falls as ``ai_cost_full / S``, so firms
    that pay the adoption fixed cost substitute AI for labour, changing their
    optimal scale and headcount (see ``firm_dynamics`` for the algebra).
"""

from __future__ import annotations

import math
from dataclasses import asdict, dataclass, replace
from typing import Optional, Tuple


@dataclass(frozen=True)
class Parameters:
    # --- Technology / labour ------------------------------------------------
    #: Output elasticity of the labour(+AI) input bundle, y = z * X**alpha.
    #: Lucas span-of-control / decreasing returns. 0.64 as in Hopenhayn &
    #: Rogerson (1993). Labour demand elasticity w.r.t. the wage is
    #: 1/(1-alpha) for non-adopters.
    alpha: float = 0.64
    #: Elasticity of substitution between labour and AI services inside an
    #: adopting firm. AI *reduces* an adopter's headcount iff
    #: sigma_ai > 1/(1-alpha) (~2.78 at the default alpha); below that the
    #: scale effect dominates and adopters hire. This is the key uncertain
    #: parameter -- the Monte Carlo default draws it on both sides.
    sigma_ai: float = 3.5
    #: Pre-AI wage (numeraire).
    wage0: float = 1.0
    #: Aggregate labour-supply elasticity, L_s = L_bar * (w/wage0)**eps.
    #: ``inf`` = perfectly elastic supply at wage0 (partial equilibrium);
    #: ``0`` = fixed labour force (employment pinned, wages adjust).
    labor_supply_elasticity: float = math.inf
    #: Per-period fixed operating cost c_f (worker-years). With the defaults a
    #: non-adopting firm exits below roughly one employee.
    fixed_cost: float = 0.5

    # --- Productivity process ----------------------------------------------
    #: Persistence of log productivity, log z' = rho log z + (1-rho) mu + sd e.
    #: rho = 1 gives Luttmer (2007)-style random growth.
    prod_persistence: float = 0.97
    #: Std. dev. of annual innovations to log productivity.
    prod_shock_sd: float = 0.18
    #: Long-run mean of incumbents' log productivity.
    prod_mean: float = 0.95
    #: Mean of entrants' log productivity draw (below prod_mean => firms grow
    #: with age, as in the data).
    entrant_prod_mean: float = 0.75
    #: Std. dev. of entrants' log productivity draw.
    entrant_prod_sd: float = 0.60

    # --- Entry --------------------------------------------------------------
    #: Sunk entry cost before AI (worker-years). Set so ~70% of potential
    #: entrants' draws clear the entry cutoff pre-AI.
    entry_cost_pre: float = 20.0
    #: Sunk entry cost at full AI diffusion (AI cheapens legal, software,
    #: marketing and back-office set-up). Default: a 20% reduction.
    entry_cost_post: float = 16.0
    #: Mean number of potential entrants per period at entry_cost_pre.
    potential_entrants: float = 600.0
    #: Elasticity of the potential-entrant pool w.r.t. the entry cost:
    #: M = potential_entrants * (entry_cost_pre / c_e)**eta. Captures would-be
    #: founders who never draw a productivity because the barrier deters them.
    entry_pool_elasticity: float = 0.3
    #: Annual discount factor used to value entry.
    discount: float = 0.96
    #: Horizon (years) of the expected-profit sum in the entry value.
    value_horizon: int = 40

    # --- Exit ---------------------------------------------------------------
    #: Exogenous exit probability per period (delta).
    exog_exit_rate: float = 0.05
    #: Endogenous exit threshold: an incumbent exits when its best available
    #: per-period net profit (after fixed and AI costs) falls below this
    #: value. 0 = exit as soon as the firm loses money.
    exit_profit_threshold: float = 0.0

    # --- AI adoption / diffusion schedule -----------------------------------
    #: First period in which AI is available (S(t) = 0 before).
    ai_start_period: int = 5
    #: Logistic diffusion speed (per year).
    ai_diffusion_speed: float = 0.5
    #: Years after ai_start_period at which diffusion reaches its inflection.
    ai_diffusion_midpoint: float = 8.0
    #: Long-run ceiling of the diffusion index.
    ai_diffusion_ceiling: float = 1.0
    #: Optional explicit schedule S(ai_start_period + k), k = 0, 1, ...;
    #: overrides the logistic curve, last value held thereafter.
    ai_schedule: Optional[Tuple[float, ...]] = None
    #: Effective price of one efficiency unit of AI services at full
    #: diffusion in an exposure-1 sector (wage0 units). Price at diffusion S in
    #: sector s is ai_cost_full / (S * exposure_s).
    ai_cost_full: float = 1.5
    #: Per-period fixed cost of operating AI (integration, data, compute
    #: contracts). Makes adoption selective on size.
    ai_adoption_fixed_cost: float = 5.0
    #: Shift (log points) in entrants' productivity mean at full diffusion.
    ai_entrant_productivity_shift: float = 0.05

    # --- Sectors ------------------------------------------------------------
    sector_names: Tuple[str, ...] = (
        "goods",
        "trade_transport",
        "professional_services",
        "information_finance",
    )
    #: Share of potential entrants drawn into each sector.
    sector_shares: Tuple[float, ...] = (0.15, 0.30, 0.35, 0.20)
    #: Relative AI exposure (multiplies AI efficiency). Placeholder ordering
    #: in line with occupational-exposure indices (Felten et al. 2021;
    #: Eloundou et al. 2023): information/finance and professional services
    #: most exposed, goods least.
    sector_ai_exposure: Tuple[float, ...] = (0.5, 0.8, 1.2, 1.5)

    # --- Reporting ----------------------------------------------------------
    #: Firm-size bucket edges (employees), half-open [lo, hi). BDS-style.
    size_bucket_edges: Tuple[float, ...] = (0, 5, 10, 20, 100, 500, math.inf)
    #: Firms below this size count as "small" in summary outcomes.
    small_firm_max: float = 20
    #: Firms at or above this size count as "large".
    large_firm_min: float = 500

    # --- Simulation ---------------------------------------------------------
    #: Firms seeded (from the entrant distribution) before burn-in.
    initial_firms: int = 1000
    #: Pre-AI periods simulated to reach the stationary distribution.
    burn_in: int = 150
    #: Recorded periods per simulation (AI starts at ai_start_period).
    n_periods: int = 40

    def __post_init__(self) -> None:
        def check(cond: bool, msg: str) -> None:
            if not cond:
                raise ValueError(f"Invalid parameter: {msg}")

        check(0.0 < self.alpha < 1.0, "alpha must be in (0, 1)")
        check(self.sigma_ai > 1.0, "sigma_ai must exceed 1 (AI substitutes for labour)")
        check(self.wage0 > 0.0, "wage0 must be positive")
        check(self.labor_supply_elasticity >= 0.0, "labor_supply_elasticity must be >= 0")
        check(self.fixed_cost >= 0.0, "fixed_cost must be >= 0")
        check(0.0 <= self.prod_persistence <= 1.0, "prod_persistence must be in [0, 1]")
        check(self.prod_shock_sd >= 0.0, "prod_shock_sd must be >= 0")
        check(self.entrant_prod_sd >= 0.0, "entrant_prod_sd must be >= 0")
        check(self.entry_cost_pre > 0.0, "entry_cost_pre must be positive")
        check(self.entry_cost_post > 0.0, "entry_cost_post must be positive")
        check(self.potential_entrants >= 0.0, "potential_entrants must be >= 0")
        check(self.entry_pool_elasticity >= 0.0, "entry_pool_elasticity must be >= 0")
        check(0.0 < self.discount < 1.0, "discount must be in (0, 1)")
        check(self.value_horizon >= 1, "value_horizon must be >= 1")
        check(0.0 <= self.exog_exit_rate < 1.0, "exog_exit_rate must be in [0, 1)")
        check(self.ai_start_period >= 0, "ai_start_period must be >= 0")
        check(self.ai_diffusion_speed > 0.0, "ai_diffusion_speed must be positive")
        check(0.0 <= self.ai_diffusion_ceiling <= 1.0, "ai_diffusion_ceiling must be in [0, 1]")
        if self.ai_schedule is not None:
            check(len(self.ai_schedule) > 0, "ai_schedule must be non-empty")
            check(all(0.0 <= s <= 1.0 for s in self.ai_schedule), "ai_schedule values must be in [0, 1]")
        check(self.ai_cost_full > 0.0, "ai_cost_full must be positive")
        check(self.ai_adoption_fixed_cost >= 0.0, "ai_adoption_fixed_cost must be >= 0")
        n_sec = len(self.sector_names)
        check(n_sec >= 1, "need at least one sector")
        check(len(self.sector_shares) == n_sec, "sector_shares length must match sector_names")
        check(len(self.sector_ai_exposure) == n_sec, "sector_ai_exposure length must match sector_names")
        check(abs(sum(self.sector_shares) - 1.0) < 1e-8, "sector_shares must sum to 1")
        check(all(s >= 0.0 for s in self.sector_shares), "sector_shares must be >= 0")
        check(all(e >= 0.0 for e in self.sector_ai_exposure), "sector_ai_exposure must be >= 0")
        edges = self.size_bucket_edges
        check(len(edges) >= 2, "size_bucket_edges needs at least two edges")
        check(edges[0] == 0 and math.isinf(edges[-1]), "size_bucket_edges must start at 0 and end at inf")
        check(all(a < b for a, b in zip(edges, edges[1:])), "size_bucket_edges must be increasing")
        check(self.initial_firms >= 0, "initial_firms must be >= 0")
        check(self.burn_in >= 0, "burn_in must be >= 0")
        check(self.n_periods >= 1, "n_periods must be >= 1")

    # --- Derived quantities -------------------------------------------------
    @property
    def theta(self) -> float:
        """Curvature 1/(1-alpha): employment is proportional to z**theta."""
        return 1.0 / (1.0 - self.alpha)

    @property
    def displacement_threshold(self) -> float:
        """sigma_ai above which AI adoption lowers a firm's headcount."""
        return self.theta

    @property
    def n_sectors(self) -> int:
        return len(self.sector_names)

    def size_bucket_labels(self) -> Tuple[str, ...]:
        """Labels like ``0_4``, ``5_9``, ..., ``500_plus`` for the size buckets."""
        labels = []
        for lo, hi in zip(self.size_bucket_edges, self.size_bucket_edges[1:]):
            lo_s = f"{lo:g}"
            labels.append(f"{lo_s}_plus" if math.isinf(hi) else f"{lo_s}_{hi - 1:g}")
        return tuple(labels)

    def ai_diffusion(self, t: int) -> float:
        """AI diffusion index S(t) in [0, ceiling]; 0 before ai_start_period.

        Logistic in years since start, renormalised so S(start) = 0 and
        S -> ai_diffusion_ceiling as t -> inf.
        """
        if t < self.ai_start_period:
            return 0.0
        k = t - self.ai_start_period
        if self.ai_schedule is not None:
            return float(self.ai_schedule[min(k, len(self.ai_schedule) - 1)])

        def logistic(x: float) -> float:
            return 1.0 / (1.0 + math.exp(-self.ai_diffusion_speed * (x - self.ai_diffusion_midpoint)))

        l0 = logistic(0.0)
        return self.ai_diffusion_ceiling * (logistic(k) - l0) / (1.0 - l0)

    def with_updates(self, **changes) -> "Parameters":
        """Return a validated copy with some fields replaced."""
        return replace(self, **changes)

    def to_dict(self) -> dict:
        return asdict(self)
