"""Firm dynamics primitives: production, AI adoption, entry and exit.

Framework: Hopenhayn (1992) industry dynamics -- heterogeneous firms draw
persistent productivity, enter if the expected value exceeds a sunk entry
cost, and exit when profits fall below a threshold -- with Luttmer (2007)
random growth as the rho = 1 special case.

Production
----------
A firm with productivity ``z`` produces ``y = z * X**alpha`` (alpha < 1,
span of control). A non-adopter uses labour only, ``X = n``. A firm that pays
the per-period AI fixed cost ``F_ai`` uses a CES bundle of labour and AI
services (elasticity ``sigma > 1``), so the unit cost of ``X`` is

    c = w                                              (non-adopter)
    c = (w**(1-sigma) + r**(1-sigma))**(1/(1-sigma))   (adopter; c < w)

where ``r`` is the effective price of AI per efficiency unit. Then

    X*   = (alpha z / c)**theta,          theta = 1/(1-alpha)
    n    = (c/w)**sigma * X*
    pi   = (1-alpha) * (alpha/c)**(alpha*theta) * z**theta   (operating profit)

and for the same firm, adopting vs not,

    n_ai / n_no_ai = (c/w)**(sigma - theta).

AI is factor-augmenting (it raises the efficiency of the non-labour input).
Cheaper ``X`` makes the firm want to be bigger (scale effect) while
substitution pushes labour out (displacement). Displacement dominates --
optimal headcount falls -- iff ``sigma > theta``. Because the adoption gain is
proportional to ``z**theta`` and adoption has a fixed cost, only large firms
adopt: the downward shift in optimal headcount is concentrated at the top of
the size distribution, while lower entry costs and better entrant draws let
small firms proliferate.
"""

from __future__ import annotations

import copy
import math
from dataclasses import dataclass
from typing import Iterable, List, Optional

import numpy as np
import pandas as pd
from scipy import optimize, stats

from .parameters import Parameters

# ---------------------------------------------------------------------------
# Containers
# ---------------------------------------------------------------------------


@dataclass
class Firm:
    """A single firm. ``Economy`` stores firms as arrays; this is the row view."""

    size: float  # employment (headcount)
    productivity: float  # z, in levels
    age: int = 0
    sector: int = 0  # index into Parameters.sector_names
    ai_adopter: bool = False
    firm_id: int = -1


@dataclass(frozen=True)
class FirmChoices:
    """Optimal static choices for a vector of firms at given prices."""

    employment: np.ndarray
    adopt: np.ndarray
    unit_cost: np.ndarray
    operating_profit: np.ndarray
    net_profit: np.ndarray
    output: np.ndarray


@dataclass(frozen=True)
class AIState:
    """The three AI channels implied by a diffusion level S in [0, 1]."""

    diffusion: float
    ai_cost: np.ndarray  # (a/c) effective AI price per efficiency unit, by sector
    entry_cost: float  # (a) sunk entry cost
    entrant_productivity_shift: float  # (b) shift in entrants' log-z mean


class Economy:
    """A collection of firms plus the current wage.

    Firm attributes are held as parallel numpy arrays so that a period of
    dynamics is fully vectorised; :attr:`firms` materialises
    :class:`Firm` objects on demand.
    """

    def __init__(self, params: Optional[Parameters] = None) -> None:
        self.params = params or Parameters()
        self.productivity = np.empty(0, dtype=float)
        self.size = np.empty(0, dtype=float)
        self.age = np.empty(0, dtype=np.int64)
        self.sector = np.empty(0, dtype=np.int64)
        self.ai_adopter = np.empty(0, dtype=bool)
        self.firm_id = np.empty(0, dtype=np.int64)
        self.output = np.empty(0, dtype=float)
        self.wage = self.params.wage0
        #: L_bar in the labour-supply curve; set at the end of burn-in.
        self.labor_supply_scale: Optional[float] = None
        self._next_id = 0

    # --- construction ------------------------------------------------------
    @classmethod
    def from_firms(cls, firms: Iterable[Firm], params: Optional[Parameters] = None) -> "Economy":
        econ = cls(params)
        for f in firms:
            econ.add_firm(f)
        return econ

    def add_firm(self, firm: Firm) -> int:
        fid = self.add_firms([firm.productivity], [firm.sector], age=[firm.age])[0]
        self.size[-1] = firm.size
        self.ai_adopter[-1] = firm.ai_adopter
        return int(fid)

    def add_firms(self, productivity, sector, age=None) -> np.ndarray:
        """Append firms (size 0 until :meth:`update_choices`). Returns new ids."""
        productivity = np.asarray(productivity, dtype=float)
        k = productivity.size
        sector = np.broadcast_to(np.asarray(sector, dtype=np.int64), (k,))
        age = np.zeros(k, dtype=np.int64) if age is None else np.broadcast_to(np.asarray(age, dtype=np.int64), (k,))
        ids = np.arange(self._next_id, self._next_id + k, dtype=np.int64)
        self._next_id += k
        self.productivity = np.concatenate([self.productivity, productivity])
        self.sector = np.concatenate([self.sector, sector])
        self.age = np.concatenate([self.age, age])
        self.size = np.concatenate([self.size, np.zeros(k)])
        self.ai_adopter = np.concatenate([self.ai_adopter, np.zeros(k, dtype=bool)])
        self.output = np.concatenate([self.output, np.zeros(k)])
        self.firm_id = np.concatenate([self.firm_id, ids])
        return ids

    def keep(self, mask: np.ndarray) -> None:
        """Retain only firms where ``mask`` is True (i.e. drop exiters)."""
        for name in ("productivity", "size", "age", "sector", "ai_adopter", "firm_id", "output"):
            setattr(self, name, getattr(self, name)[mask])

    def copy(self) -> "Economy":
        return copy.deepcopy(self)

    # --- views -------------------------------------------------------------
    @property
    def n_firms(self) -> int:
        return int(self.productivity.size)

    @property
    def aggregate_employment(self) -> float:
        return float(self.size.sum())

    @property
    def firms(self) -> List[Firm]:
        return [
            Firm(float(n), float(z), int(a), int(s), bool(ai), int(i))
            for n, z, a, s, ai, i in zip(
                self.size, self.productivity, self.age, self.sector, self.ai_adopter, self.firm_id
            )
        ]

    def to_frame(self) -> pd.DataFrame:
        return pd.DataFrame(
            {
                "firm_id": self.firm_id,
                "size": self.size,
                "productivity": self.productivity,
                "age": self.age,
                "sector": self.sector,
                "ai_adopter": self.ai_adopter,
            }
        )

    def size_bucket_index(self) -> np.ndarray:
        edges = np.asarray(self.params.size_bucket_edges, dtype=float)
        return np.searchsorted(edges, self.size, side="right") - 1

    def size_distribution(self) -> pd.DataFrame:
        """Firm-size distribution: firms, employment and shares by size bucket."""
        labels = self.params.size_bucket_labels()
        idx = self.size_bucket_index()
        nb = len(labels)
        firms = np.bincount(idx, minlength=nb)[:nb]
        emp = np.bincount(idx, weights=self.size, minlength=nb)[:nb]
        adopters = np.bincount(idx, weights=self.ai_adopter.astype(float), minlength=nb)[:nb]
        df = pd.DataFrame({"firms": firms, "employment": emp}, index=pd.Index(labels, name="size_bucket"))
        df["firm_share"] = df["firms"] / max(self.n_firms, 1)
        df["employment_share"] = df["employment"] / max(self.aggregate_employment, 1e-12)
        with np.errstate(invalid="ignore", divide="ignore"):
            df["adoption_rate"] = np.where(firms > 0, adopters / firms, np.nan)
        return df

    # --- behaviour ---------------------------------------------------------
    def update_choices(self, wage: float, ai_cost: np.ndarray) -> FirmChoices:
        """Set the wage, then each firm's optimal adoption and employment."""
        self.wage = float(wage)
        ch = firm_choices(self.productivity, self.sector, self.wage, ai_cost, self.params)
        self.size = ch.employment
        self.ai_adopter = ch.adopt
        self.output = ch.output
        return ch


# ---------------------------------------------------------------------------
# Production and the AI shock
# ---------------------------------------------------------------------------


def ces_unit_cost(wage, ai_cost, sigma: float):
    """Unit cost of the labour/AI bundle; equals ``wage`` when AI is unavailable (inf)."""
    e = 1.0 - sigma
    wage = np.asarray(wage, dtype=float)
    ai_cost = np.asarray(ai_cost, dtype=float)
    with np.errstate(divide="ignore", over="ignore"):
        return (wage**e + ai_cost**e) ** (1.0 / e)


def optimal_input(z, unit_cost, alpha: float):
    """Profit-maximising input bundle X* = (alpha z / c)**(1/(1-alpha))."""
    return (alpha * np.asarray(z, dtype=float) / unit_cost) ** (1.0 / (1.0 - alpha))


def operating_profit(z, unit_cost, alpha: float):
    """Revenue minus variable input cost at the optimum, (1-alpha)/alpha * c X*."""
    return (1.0 - alpha) / alpha * unit_cost * optimal_input(z, unit_cost, alpha)


def profit_coefficient(unit_cost, alpha: float):
    """K(c) such that operating profit = K(c) * z**theta."""
    return (1.0 - alpha) * (alpha / np.asarray(unit_cost, dtype=float)) ** (alpha / (1.0 - alpha))


def labor_demand(z, wage, unit_cost, alpha: float, sigma: float):
    """Headcount n = (c/w)**sigma * X*. For a non-adopter (c = w), n = X*."""
    return (unit_cost / wage) ** sigma * optimal_input(z, unit_cost, alpha)


def ai_headcount_ratio(wage, ai_cost, params: Parameters):
    """Optimal headcount with AI relative to without, (c/w)**(sigma - theta).

    Independent of z: < 1 (AI shrinks the firm's workforce) iff
    sigma_ai > 1/(1-alpha).
    """
    c = ces_unit_cost(wage, ai_cost, params.sigma_ai)
    return (c / wage) ** (params.sigma_ai - params.theta)


def ai_productivity_shock(diffusion: float, params: Parameters) -> AIState:
    """Map AI diffusion S in [0, 1] into the model's three AI channels.

    (a) entry cost: linear from entry_cost_pre (S=0) to entry_cost_post (S=1);
    (b) entrant log-productivity mean shifts by S * ai_entrant_productivity_shift;
    (c) AI efficiency in sector s is proportional to S * exposure_s, so the
        effective AI price is ai_cost_full / (S * exposure_s) (inf when 0).
        Adopters' unit cost falls and, with sigma_ai > theta, their optimal
        headcount shifts down (see :func:`ai_headcount_ratio`).
    """
    s = float(np.clip(diffusion, 0.0, 1.0))
    efficiency = s * np.asarray(params.sector_ai_exposure, dtype=float)
    with np.errstate(divide="ignore"):
        ai_cost = np.where(efficiency > 0, params.ai_cost_full / efficiency, np.inf)
    entry_cost = params.entry_cost_pre + (params.entry_cost_post - params.entry_cost_pre) * s
    return AIState(
        diffusion=s,
        ai_cost=ai_cost,
        entry_cost=entry_cost,
        entrant_productivity_shift=params.ai_entrant_productivity_shift * s,
    )


def firm_choices(productivity, sector, wage: float, ai_cost, params: Parameters) -> FirmChoices:
    """Static optimum for each firm: adopt AI iff the profit gain exceeds F_ai."""
    z = np.asarray(productivity, dtype=float)
    alpha = params.alpha
    r = np.asarray(ai_cost, dtype=float)[np.asarray(sector, dtype=np.int64)]
    c_ai = ces_unit_cost(wage, r, params.sigma_ai)
    pi_no = operating_profit(z, wage, alpha)
    pi_ai = operating_profit(z, c_ai, alpha) - params.ai_adoption_fixed_cost
    adopt = pi_ai > pi_no
    c = np.where(adopt, c_ai, wage)
    x = optimal_input(z, c, alpha)
    n = (c / wage) ** params.sigma_ai * x
    pi = np.where(adopt, pi_ai, pi_no)
    return FirmChoices(
        employment=n,
        adopt=adopt,
        unit_cost=c,
        operating_profit=pi,
        net_profit=pi - params.fixed_cost,
        output=z * x**alpha,
    )


def solve_wage(productivity, sector, ai_cost, params: Parameters, labor_supply_scale: Optional[float]) -> float:
    """Market-clearing wage: sum_i n_i(w) = L_bar * (w / wage0)**eps.

    Returns wage0 under perfectly elastic supply (eps = inf), before L_bar has
    been set (burn-in), or with no firms.
    """
    eps = params.labor_supply_elasticity
    z = np.asarray(productivity, dtype=float)
    if math.isinf(eps) or labor_supply_scale is None or z.size == 0:
        return params.wage0
    w0 = params.wage0

    def excess(log_w: float) -> float:
        w = math.exp(log_w)
        demand = firm_choices(z, sector, w, ai_cost, params).employment.sum()
        return math.log(max(demand, 1e-300)) - math.log(labor_supply_scale) - eps * (log_w - math.log(w0))

    return math.exp(optimize.brentq(excess, math.log(w0) - 5.0, math.log(w0) + 5.0, xtol=1e-10))


# ---------------------------------------------------------------------------
# Productivity process
# ---------------------------------------------------------------------------


def evolve_productivity(
    productivity,
    params: Parameters,
    rng: Optional[np.random.Generator] = None,
    shocks: Optional[np.ndarray] = None,
) -> np.ndarray:
    """One-year AR(1) step in logs: log z' = rho log z + (1-rho) mu + sd * eps.

    Pass standard-normal ``shocks`` directly (e.g. keyed by firm id) or an ``rng``.
    """
    log_z = np.log(np.asarray(productivity, dtype=float))
    if shocks is None:
        if rng is None:
            raise ValueError("evolve_productivity needs rng or shocks")
        shocks = rng.standard_normal(log_z.size)
    rho = params.prod_persistence
    log_z = rho * log_z + (1.0 - rho) * params.prod_mean + params.prod_shock_sd * np.asarray(shocks)
    return np.exp(log_z)


def _log_z_moments(log_z0: np.ndarray, horizon: int, params: Parameters):
    """Conditional mean and variance of log z_t, t = 0..horizon-1."""
    t = np.arange(horizon, dtype=float)
    rho, mu, sd = params.prod_persistence, params.prod_mean, params.prod_shock_sd
    mean = mu + rho**t * (log_z0[:, None] - mu)
    if rho < 1.0:
        var = sd**2 * (1.0 - rho ** (2.0 * t)) / (1.0 - rho**2)
    else:
        var = sd**2 * t
    return mean, var


# ---------------------------------------------------------------------------
# Entry
# ---------------------------------------------------------------------------


def potential_entrant_mass(entry_cost: float, params: Parameters) -> float:
    """Expected pool of would-be entrants: M0 * (c_e,pre / c_e)**eta."""
    return params.potential_entrants * (params.entry_cost_pre / entry_cost) ** params.entry_pool_elasticity


def draw_potential_entrants(
    n: int,
    params: Parameters,
    rng: np.random.Generator,
    productivity_shift: float = 0.0,
    sector_rng: Optional[np.random.Generator] = None,
):
    """Productivity and sector draws for ``n`` potential entrants.

    A separate ``sector_rng`` keeps the i-th entrant's draws independent of ``n``.
    """
    log_z = rng.normal(params.entrant_prod_mean + productivity_shift, params.entrant_prod_sd, size=n)
    sector = (sector_rng or rng).choice(params.n_sectors, size=n, p=np.asarray(params.sector_shares, dtype=float))
    return np.exp(log_z), sector


def entry_value(productivity, sector, wage: float, ai_cost, params: Parameters) -> np.ndarray:
    """Expected discounted net profit of a firm starting at productivity z.

    V(z) = sum_t (beta (1-delta))**t * [max(K_0 m_t, K_ai m_t - F_ai) - c_f],
    m_t = E[z_t**theta | z_0 = z] (closed form under the log-AR(1)). Evaluating
    the adoption max at the expectation and ignoring the exit option are
    approximations (both understate V slightly). Entrants assume today's wage
    and AI prices persist.
    """
    z = np.atleast_1d(np.asarray(productivity, dtype=float))
    sector = np.broadcast_to(np.asarray(sector, dtype=np.int64), z.shape)
    theta = params.theta
    mean, var = _log_z_moments(np.log(z), params.value_horizon, params)
    m = np.exp(theta * mean + 0.5 * theta**2 * var)
    k_no = profit_coefficient(wage, params.alpha)
    r = np.asarray(ai_cost, dtype=float)[sector]
    k_ai = profit_coefficient(ces_unit_cost(wage, r, params.sigma_ai), params.alpha)
    flow = np.maximum(k_no * m, k_ai[:, None] * m - params.ai_adoption_fixed_cost) - params.fixed_cost
    disc = (params.discount * (1.0 - params.exog_exit_rate)) ** np.arange(params.value_horizon)
    return flow @ disc


def entry_cutoff(entry_cost: float, wage: float, ai_cost, params: Parameters) -> np.ndarray:
    """Per-sector log-productivity cutoff above which entry is profitable, V = c_e."""
    cut = np.empty(params.n_sectors)
    for s in range(params.n_sectors):
        f = lambda lz: entry_value(math.exp(lz), s, wage, ai_cost, params)[0] - entry_cost  # noqa: E731
        cut[s] = optimize.brentq(f, -10.0, 10.0, xtol=1e-10)
    return cut


def entry_probability(entry_cost: float, wage: float, ai_cost, params: Parameters, productivity_shift: float = 0.0) -> float:
    """Probability a potential entrant's draw clears the entry cutoff."""
    cut = entry_cutoff(entry_cost, wage, ai_cost, params)
    mu = params.entrant_prod_mean + productivity_shift
    sd = max(params.entrant_prod_sd, 1e-12)
    p = stats.norm.sf((cut - mu) / sd)
    return float(np.dot(params.sector_shares, p))


def expected_entry(entry_cost: float, wage: float, ai_cost, params: Parameters, productivity_shift: float = 0.0) -> float:
    """Expected entrants per period as a function of the entry barrier:
    pool size(c_e) x probability the draw clears the cutoff(c_e)."""
    return potential_entrant_mass(entry_cost, params) * entry_probability(
        entry_cost, wage, ai_cost, params, productivity_shift
    )


# ---------------------------------------------------------------------------
# Exit
# ---------------------------------------------------------------------------


def exit_productivity_cutoff(wage: float, params: Parameters) -> float:
    """z below which a non-adopter's net profit falls under the exit threshold.

    Solves K(w) z**theta - c_f = exit_profit_threshold. (Firms near the cutoff
    are far too small to adopt AI, so the non-adopter profit is the relevant one.)
    """
    target = params.fixed_cost + params.exit_profit_threshold
    if target <= 0.0:
        return 0.0
    return float((target / profit_coefficient(wage, params.alpha)) ** (1.0 - params.alpha))


def exit_probability(productivity, wage: float, params: Parameters) -> np.ndarray:
    """Probability each firm exits before producing next period:
    delta + (1 - delta) * P(z' < cutoff | z)."""
    z = np.asarray(productivity, dtype=float)
    cutoff = exit_productivity_cutoff(wage, params)
    delta = params.exog_exit_rate
    if cutoff <= 0.0:
        return np.full(z.shape, delta)
    rho = params.prod_persistence
    mean = rho * np.log(z) + (1.0 - rho) * params.prod_mean
    if params.prod_shock_sd > 0:
        p_endo = stats.norm.cdf((math.log(cutoff) - mean) / params.prod_shock_sd)
    else:
        p_endo = (mean < math.log(cutoff)).astype(float)
    return delta + (1.0 - delta) * p_endo


def exit_rate(productivity, wage: float, params: Parameters) -> float:
    """Expected exit rate of a population of firms."""
    z = np.asarray(productivity, dtype=float)
    return float(exit_probability(z, wage, params).mean()) if z.size else 0.0
