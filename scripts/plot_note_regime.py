"""Note figure: simulated net labor-demand effect, normalized CES only.

Reads data/regime_map.csv (scripts/regime_map.py) and writes
paper/figures/note_regime_sim.{pdf,png}: mean net labor-demand effect of AI
vs. the no-AI twin, 10 seeds per cell, with the reference cost saving held
fixed across sigma_ai. Illustrative; the model is not calibrated.

Usage
    .venv/bin/python scripts/plot_note_regime.py
"""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "data" / "regime_map.csv"
OUT = ROOT / "paper" / "figures" / "note_regime_sim"
THETA = 1 / (1 - 0.64)


def main() -> None:
    t = pd.read_csv(SRC)
    t = t[t.normalization == "cost_saving"]
    m = t.pivot(index="entrant_shift", columns="sigma_ai", values="net_mean")
    se = t.pivot(index="entrant_shift", columns="sigma_ai", values="net_se")
    sig = list(m.columns)
    fig, ax = plt.subplots(figsize=(6.4, 3.4), dpi=150)
    im = ax.imshow(m.to_numpy(), origin="lower", aspect="auto", cmap="RdBu", vmin=-0.4, vmax=0.4)
    for i in range(m.shape[0]):
        for j in range(m.shape[1]):
            v = m.iat[i, j]
            ax.text(j, i, f"{v:+.0%}\n±{se.iat[i, j]:.0%}", ha="center", va="center", fontsize=7,
                    color="white" if abs(v) > 0.25 else "black")
    ax.set_xticks(range(len(sig)))
    ax.set_xticklabels([f"{s:g}" for s in sig], fontsize=8)
    ax.set_yticks(range(m.shape[0]))
    ax.set_yticklabels([f"{d:.2f}" for d in m.index], fontsize=8)
    ax.axvline(np.interp(THETA, sig, range(len(sig))), color="black", ls="--", lw=0.8)
    ax.set_xlabel(r"Labor-AI elasticity $\sigma$ ($\theta = 2.78$ dashed)", fontsize=9)
    ax.set_ylabel(r"Entrant shift $\Delta$", fontsize=9)
    cb = fig.colorbar(im, ax=ax, fraction=0.04, pad=0.02)
    cb.ax.yaxis.set_major_formatter(matplotlib.ticker.PercentFormatter(1.0, decimals=0))
    cb.ax.tick_params(labelsize=7)
    fig.tight_layout()
    fig.savefig(OUT.with_suffix(".pdf"))
    fig.savefig(OUT.with_suffix(".png"))
    print(f"wrote {OUT}.pdf")


if __name__ == "__main__":
    main()
