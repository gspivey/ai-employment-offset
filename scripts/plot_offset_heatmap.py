"""Figure: P(offset) by sigma_ai bin and AI-native entrant productivity shift.

Reads data/monte_carlo_raw.csv and writes paper/figures/offset_heatmap.{pdf,png}.
Rows are terciles of the entrant productivity shift (prior U(0, 0.15), so the
terciles are close to [0, 0.05), [0.05, 0.10), [0.10, 0.15]); columns are
0.5-wide sigma_ai bins. Each cell prints P(offset) and the number of draws.

Usage
    .venv/bin/python scripts/plot_offset_heatmap.py
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
OUT = ROOT / "paper" / "figures" / "offset_heatmap"
THETA = 1.0 / (1.0 - 0.64)


def main() -> None:
    df = pd.read_csv(RAW)
    df["offset"] = df["offset"].astype(bool)
    sig_edges = np.arange(2.0, 5.01, 0.5)
    df["sig_bin"] = pd.cut(df["sigma_ai"], sig_edges, right=False, include_lowest=True)
    df["mu_tercile"] = pd.qcut(df["ai_entrant_productivity_shift"], 3, labels=False)
    tercile_edges = df.groupby("mu_tercile")["ai_entrant_productivity_shift"].agg(["min", "max"])

    p = df.pivot_table(index="mu_tercile", columns="sig_bin", values="offset", aggfunc="mean", observed=False)
    n = df.pivot_table(index="mu_tercile", columns="sig_bin", values="offset", aggfunc="size", observed=False)

    fig, ax = plt.subplots(figsize=(6.5, 2.9), dpi=200)
    im = ax.imshow(p.to_numpy(), origin="lower", aspect="auto", cmap="RdBu", vmin=0.0, vmax=1.0)
    for i in range(p.shape[0]):
        for j in range(p.shape[1]):
            v = p.iat[i, j]
            ax.text(j, i, f"{v:.0%}\n(n={int(n.iat[i, j])})", ha="center", va="center", fontsize=7,
                    color="white" if v < 0.25 or v > 0.8 else "black")
    ax.set_xticks(range(len(sig_edges) - 1))
    ax.set_xticklabels([f"{a:.1f}–{b:.1f}" for a, b in zip(sig_edges[:-1], sig_edges[1:])], fontsize=7.5)
    ax.set_yticks(range(3))
    ax.set_yticklabels([f"{lo:.2f}–{hi:.2f}" for lo, hi in tercile_edges.to_numpy()], fontsize=7.5)
    ax.set_xlabel(r"Labor–AI substitution elasticity $\sigma_{\mathrm{ai}}$", fontsize=8.5)
    ax.set_ylabel(r"Entrant shift $\Delta\mu_e$ (tercile)", fontsize=8.5)
    # threshold at 2.78 sits inside the [2.5, 3.0) column: x = 1 + (2.78 - 2.5) / 0.5 - 0.5
    x_th = (THETA - 2.0) / 0.5 - 0.5
    ax.axvline(x_th, color="black", ls="--", lw=0.8)
    cb = fig.colorbar(im, ax=ax, fraction=0.04, pad=0.02)
    cb.ax.yaxis.set_major_formatter(matplotlib.ticker.PercentFormatter(1.0, decimals=0))
    cb.ax.tick_params(labelsize=7)
    cb.set_label("P(offset)", fontsize=8)
    fig.tight_layout()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT.with_suffix(".pdf"))
    fig.savefig(OUT.with_suffix(".png"))
    print(p.round(3).to_string())
    print(f"wrote {OUT}.pdf and .png")


if __name__ == "__main__":
    main()
