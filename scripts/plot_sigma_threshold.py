"""Figure: P(offset) as a function of sigma_ai, with the displacement threshold.

Reads data/monte_carlo_raw.csv (written by scripts/monte_carlo_t6.py) and writes
paper/figures/sigma_threshold.{pdf,png}. Every plotted number comes from the CSV.

Offset is the Monte Carlo definition, net_employment_effect > 0. When large-firm
employment falls this is the same event as Omega >= 1 (gains below 500 cover the
500+ loss); when it does not fall, there is no displacement and Omega is unbounded.

    python scripts/plot_sigma_threshold.py
"""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "monte_carlo_raw.csv"
OUT = ROOT / "paper" / "figures" / "sigma_threshold"

ALPHA = 0.64  # Parameters() default, held fixed in the Monte Carlo
THETA = 1.0 / (1.0 - ALPHA)
BIN_EDGES = np.arange(2.0, 5.0 + 1e-9, 0.25)  # same bins as monte_carlo_results.md
KERNEL_BW = 0.15  # Gaussian kernel bandwidth in sigma_ai units
Z95 = 1.959964


def wilson(k: np.ndarray, n: np.ndarray, z: float = Z95) -> tuple[np.ndarray, np.ndarray]:
    p = k / n
    denom = 1 + z**2 / n
    centre = (p + z**2 / (2 * n)) / denom
    half = z * np.sqrt(p * (1 - p) / n + z**2 / (4 * n**2)) / denom
    return centre - half, centre + half


def kernel_prob(x: np.ndarray, y: np.ndarray, grid: np.ndarray, bw: float):
    """Nadaraya-Watson estimate of P(y | x) with a Wilson band on the effective n."""
    w = np.exp(-0.5 * ((grid[:, None] - x[None, :]) / bw) ** 2)
    p = (w * y[None, :]).sum(1) / w.sum(1)
    n_eff = w.sum(1) ** 2 / (w**2).sum(1)
    lo, hi = wilson(p * n_eff, n_eff)
    return p, lo, hi


def main() -> None:
    df = pd.read_csv(RAW)
    sigma = df["sigma_ai"].to_numpy()
    offset = (df["net_employment_effect"] > 0).to_numpy(float)
    assert (offset == df["offset"].astype(bool).to_numpy()).all()

    # Binned estimates
    idx = np.clip(np.digitize(sigma, BIN_EDGES) - 1, 0, len(BIN_EDGES) - 2)
    mids = 0.5 * (BIN_EDGES[:-1] + BIN_EDGES[1:])
    n = np.bincount(idx, minlength=len(mids)).astype(float)
    k = np.bincount(idx, weights=offset, minlength=len(mids))
    p_bin = k / n
    lo_bin, hi_bin = wilson(k, n)

    grid = np.linspace(2.0, 5.0, 301)
    p_s, lo_s, hi_s = kernel_prob(sigma, offset, grid, KERNEL_BW)

    # Entrant-productivity terciles (same cut points as the results table)
    shift = df["ai_entrant_productivity_shift"].to_numpy()
    weak, strong = shift < 0.05, shift >= 0.10
    p_weak, *_ = kernel_prob(sigma[weak], offset[weak], grid, KERNEL_BW)
    p_strong, *_ = kernel_prob(sigma[strong], offset[strong], grid, KERNEL_BW)

    below = sigma < THETA
    p_below, p_above = offset[below].mean(), offset[~below].mean()

    plt.rcParams.update({
        "font.family": "serif",
        "font.size": 9,
        "mathtext.fontset": "cm",
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.linewidth": 0.6,
        "xtick.major.width": 0.6,
        "ytick.major.width": 0.6,
        "pdf.fonttype": 42,
    })
    fig, ax = plt.subplots(figsize=(6.0, 3.6))

    ax.axvspan(2.0, THETA, color="#d6e6f4", lw=0, zorder=0)
    ax.axvspan(THETA, 5.0, color="#f8e0cc", lw=0, zorder=0)
    ax.text(0.5 * (2.0 + THETA), 0.06, "Augmentation\n" r"($\sigma_{\mathrm{ai}} < \theta$)",
            ha="center", va="bottom", fontsize=8.5, color="#1f4e79")
    ax.text(0.5 * (THETA + 5.0), 0.06, "Displacement\n" r"($\sigma_{\mathrm{ai}} > \theta$)",
            ha="center", va="bottom", fontsize=8.5, color="#8a3b00")

    ax.axhline(0.5, color="0.6", lw=0.5, ls=":", zorder=1)
    ax.axvline(THETA, color="black", lw=1.0, ls="--", zorder=3)
    ax.text(THETA - 0.035, 0.55, r"$\theta = 1/(1-\alpha) \approx %.2f$" % THETA,
            ha="right", va="center", rotation=90, fontsize=8.5)

    ax.plot(grid, p_strong, color="#2b8a3e", lw=1.0, ls="-.", zorder=4,
            label=r"strong entrants ($\Delta\mu_e \geq 0.10$)")
    ax.plot(grid, p_weak, color="#b02418", lw=1.0, ls="-.", zorder=4,
            label=r"weak entrants ($\Delta\mu_e < 0.05$)")
    ax.fill_between(grid, lo_s, hi_s, color="0.15", alpha=0.15, lw=0, zorder=4)
    ax.plot(grid, p_s, color="0.1", lw=1.6, zorder=5, label="all draws (kernel smooth, 95% band)")
    ax.errorbar(mids, p_bin, yerr=[p_bin - lo_bin, hi_bin - p_bin], fmt="o", ms=3.5,
                color="0.1", mfc="white", mew=0.9, elinewidth=0.8, capsize=2, zorder=6,
                label=r"binned (width 0.25, Wilson 95% CI)")

    ax.text(2.06, 0.30, "P = %.1f%%\n(n = %d)" % (100 * p_below, below.sum()),
            fontsize=8, color="#1f4e79", va="bottom")
    ax.text(THETA + 0.06, 0.30, "P = %.1f%%\n(n = %d)" % (100 * p_above, (~below).sum()),
            fontsize=8, color="#8a3b00", va="bottom")

    ax.set_xlim(2.0, 5.0)
    ax.set_ylim(0.0, 1.02)
    ax.set_xlabel(r"Labor–AI substitution elasticity $\sigma_{\mathrm{ai}}$")
    ax.set_ylabel(r"Probability of offset, $\Pr[\Omega \geq 1]$")
    ax.yaxis.set_major_formatter(matplotlib.ticker.PercentFormatter(1.0, decimals=0))
    ax.legend(loc="upper right", bbox_to_anchor=(1.0, 0.56), fontsize=7, frameon=True,
              framealpha=0.9, edgecolor="none", borderpad=0.4)

    fig.tight_layout()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT.with_suffix(".pdf"))
    fig.savefig(OUT.with_suffix(".png"), dpi=300)

    print(f"theta = {THETA:.3f}; P(offset) below = {p_below:.3f} (n={below.sum()}), "
          f"above = {p_above:.3f} (n={(~below).sum()})")
    for m, nn, pp in zip(mids, n, p_bin):
        print(f"  bin {m:.3f}: n={int(nn):4d}  P={pp:.3f}")
    print(f"  kernel min P = {p_s.min():.3f} at sigma = {grid[p_s.argmin()]:.2f}")
    print(f"wrote {OUT.with_suffix('.pdf')} and .png")


if __name__ == "__main__":
    main()
