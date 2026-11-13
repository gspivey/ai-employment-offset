"""Normalized CES and the firm-level threshold (Proposition 1)."""

import numpy as np
import pytest

from model import Parameters
from model.firm_dynamics import ai_headcount_ratio, ai_productivity_shock, ces_unit_cost, reference_ai_price


@pytest.mark.parametrize("target", [0.05, 0.117, 0.30])
def test_cost_saving_is_the_same_for_every_sigma(target):
    """Under cost_saving, the reference unit-cost saving does not move with sigma_ai."""
    savings = []
    for sigma in (1.5, 2.0, 2.78, 3.5, 5.0, 8.0):
        p = Parameters(sigma_ai=sigma, ces_normalization="cost_saving", ai_cost_saving_target=target)
        c = ces_unit_cost(p.wage0, reference_ai_price(p), sigma)
        savings.append(1.0 - c / p.wage0)
    assert np.allclose(savings, target, atol=1e-10)


def test_unnormalized_saving_shrinks_with_sigma():
    """Without normalization, a lower sigma_ai is a bigger cost shock (the confound)."""
    saving = [1.0 - ces_unit_cost(1.0, 1.5, s) for s in (2.0, 3.5, 5.0)]
    assert saving[0] > saving[1] > saving[2]


def test_default_target_reproduces_unnormalized_model_at_sigma_3_5():
    p_none = Parameters(sigma_ai=3.5)
    p_norm = Parameters(sigma_ai=3.5, ces_normalization="cost_saving")
    assert reference_ai_price(p_norm) == pytest.approx(reference_ai_price(p_none), rel=1e-2)


def test_normalization_keeps_relative_prices_across_sectors_and_diffusion():
    p = Parameters(sigma_ai=2.5, ces_normalization="cost_saving")
    ai = ai_productivity_shock(0.5, p)
    expected = reference_ai_price(p) / (0.5 * np.asarray(p.sector_ai_exposure))
    assert np.allclose(ai.ai_cost, expected)


@pytest.mark.parametrize("alpha", [0.6, 0.64, 0.75, 0.85])
@pytest.mark.parametrize("normalization", ["none", "cost_saving"])
def test_headcount_response_flips_sign_at_threshold(alpha, normalization):
    """Adopter headcount rises iff sigma_ai < theta = 1/(1-alpha), for any alpha."""
    theta = 1.0 / (1.0 - alpha)
    for sigma, rises in ((theta * 0.8, True), (theta * 1.25, False)):
        sigma = max(sigma, 1.05)
        if sigma >= theta and rises:
            continue
        p = Parameters(alpha=alpha, sigma_ai=sigma, ces_normalization=normalization)
        ratio = float(ai_headcount_ratio(p.wage0, reference_ai_price(p), p))
        assert (ratio > 1.0) == rises, (alpha, sigma, ratio)
