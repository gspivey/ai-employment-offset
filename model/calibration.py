"""Empirical calibration targets (placeholder).

Pre-AI moments for the baseline steady state and AI-era moments for the
diffusion schedule. Every target is ``verified=False``: values are
approximate recollections of the cited sources and MUST be checked against
the actual releases (and the vintage chosen) before being used for
estimation. The moment functions and loss are working; the estimator itself
(:func:`calibrate`) is a stub.

Planned approach: simulated method of moments over (prod_mean,
prod_shock_sd, entrant_prod_mean, entrant_prod_sd, entry_cost_pre,
potential_entrants, fixed_cost, exog_exit_rate) on the pre-AI targets,
then the AI block (ai_cost_full, ai_adoption_fixed_cost, schedule) on AI-use
targets by firm size.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, Optional

import numpy as np
import pandas as pd

from .firm_dynamics import Economy
from .parameters import Parameters


@dataclass(frozen=True)
class CalibrationTarget:
    name: str  # key into simulated_moments()
    value: float
    source: str
    weight: float = 1.0
    verified: bool = False
    note: str = ""


#: Pre-AI steady-state targets (US employer firms).
BASELINE_TARGETS = (
    CalibrationTarget("entry_rate", 0.08, "Census BDS, firm startup rate, 2010s average", note="approx; verify vintage"),
    CalibrationTarget("exit_rate", 0.08, "Census BDS, firm death rate, 2010s average", note="approx; verify vintage"),
    CalibrationTarget("mean_firm_size", 22.0, "Census SUSB, employment / employer firms", note="approx"),
    CalibrationTarget("emp_share_large", 0.53, "Census SUSB, employment share of firms with 500+ employees", note="approx"),
    CalibrationTarget("firm_share_small", 0.89, "Census SUSB, share of employer firms with <20 employees", note="approx"),
    CalibrationTarget("size_tail_exponent", 1.06, "Axtell (2001), Science 293:1818 -- Zipf exponent of US firm sizes"),
)

#: AI-era targets for the diffusion block.
AI_TARGETS = (
    CalibrationTarget(
        "adoption_rate",
        0.09,
        "Census Business Trends and Outlook Survey (BTOS), share of firms using AI to produce goods/services",
        note="approx for 2025; rising quickly -- pin to a specific wave and map to a model period",
    ),
)


def pareto_tail_exponent(sizes: np.ndarray, min_size: float = 100.0) -> float:
    """MLE (Hill) estimate of the Pareto exponent for firms with size >= min_size."""
    x = np.asarray(sizes, dtype=float)
    x = x[x >= min_size]
    if x.size < 10:
        return np.nan
    return float(x.size / np.log(x / min_size).sum())


def simulated_moments(
    history: pd.DataFrame,
    params: Parameters,
    economy: Optional[Economy] = None,
    periods: Optional[slice] = None,
) -> Dict[str, float]:
    """Model counterparts of the calibration targets.

    ``history`` is a :func:`model.simulation.run_simulation` frame; ``periods``
    selects the rows to average (default: all). The tail exponent needs the
    cross-section, so it is only reported when ``economy`` is given.
    """
    from .simulation import size_class_columns

    h = history if periods is None else history.loc[periods]
    small, large = size_class_columns(params)
    emp = h["aggregate_employment"]
    moments = {
        "entry_rate": float(h["entry_rate"].mean()),
        "exit_rate": float(h["exit_rate"].mean()),
        "mean_firm_size": float(h["mean_firm_size"].mean()),
        "emp_share_large": float((h[[f"emp_{b}" for b in large]].sum(axis=1) / emp).mean()) if large else np.nan,
        "firm_share_small": float((h[[f"firms_{b}" for b in small]].sum(axis=1) / h["n_firms"]).mean()) if small else np.nan,
        "adoption_rate": float(h["adoption_rate"].mean()),
    }
    if economy is not None:
        moments["size_tail_exponent"] = pareto_tail_exponent(economy.size)
    return moments


def moment_distance(moments: Dict[str, float], targets: Iterable[CalibrationTarget] = BASELINE_TARGETS) -> float:
    """Weighted sum of squared proportional deviations from targets (missing moments skipped)."""
    loss = 0.0
    for tgt in targets:
        m = moments.get(tgt.name, np.nan)
        if np.isfinite(m):
            loss += tgt.weight * ((m - tgt.value) / tgt.value) ** 2
    return float(loss)


def moment_table(moments: Dict[str, float], targets: Iterable[CalibrationTarget] = BASELINE_TARGETS) -> pd.DataFrame:
    """Side-by-side model vs target table."""
    rows = [
        {
            "moment": t.name,
            "model": moments.get(t.name, np.nan),
            "target": t.value,
            "verified": t.verified,
            "source": t.source,
        }
        for t in targets
    ]
    return pd.DataFrame(rows).set_index("moment")


def calibrate(*args, **kwargs):
    """Simulated method of moments estimation -- not yet implemented."""
    raise NotImplementedError(
        "SMM calibration is a placeholder: verify BASELINE_TARGETS/AI_TARGETS first, "
        "then minimise moment_distance() over the parameter block listed in the module docstring."
    )
