"""Blog figure: business applications in two AI-exposed sectors vs. the rest.

Reads data/bfs_monthly_gap.csv (written by scripts/bfs_causal_analysis.py):
monthly log gap of each group vs. the other 15 sectors, 2022 mean = 0.
Plots Information + Professional Services and the Construction placebo only,
sized and lettered for phones. Writes paper/figures/blog_bfs_gap.png.

Usage
    .venv/bin/python scripts/plot_blog_bfs_gap.py
"""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "data" / "bfs_monthly_gap.csv"
OUT = ROOT / "paper" / "figures" / "blog_bfs_gap.png"


def main() -> None:
    g = pd.read_csv(SRC, parse_dates=["date"]).set_index("date")
    # log points -> percent difference, so the axis reads in plain terms
    ai = (np.exp(g["AI-exposed (51+54)"]) - 1) * 100
    con = (np.exp(g["Construction (23)"]) - 1) * 100

    fig, ax = plt.subplots(figsize=(8, 6), dpi=150)
    ax.axhline(0, color="#999999", lw=1)
    ax.axvline(pd.Timestamp("2025-03-01"), color="#999999", lw=1, ls="--")
    ax.plot(ai.index, ai, color="#2a9d8f", lw=3.5)
    ax.plot(con.index, con, color="#9aa3b2", lw=2.5)
    ax.text(pd.Timestamp("2024-12-01"), 27, "Information +\nProfessional Services", ha="right", va="center",
            fontsize=14, color="#2a9d8f", fontweight="bold")
    ax.text(con.index[-1], -9, "Construction", ha="right", va="top", fontsize=14, color="#6b7385", fontweight="bold")
    ax.text(pd.Timestamp("2025-02-01"), 50, "March 2025", ha="right", fontsize=12, color="#666666")
    ax.text(pd.Timestamp("2020-06-01"), 21, "2020 pandemic surge", ha="left", fontsize=12, color="#666666")
    ax.set_ylabel("Applications vs. other sectors (%, 2022 = 0)", fontsize=13)
    ax.tick_params(labelsize=13)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.grid(axis="y", color="#e5e5e5")
    ax.set_title("Two AI-exposed sectors pulled ahead", fontsize=19, fontweight="bold", loc="left", pad=14)
    fig.text(0.01, 0.01, f"Source: Census Business Formation Statistics, monthly, through {ai.index[-1]:%b %Y}.",
             fontsize=11, color="#666666")
    fig.tight_layout(rect=(0, 0.03, 1, 1))
    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT)
    print(f"last: AI {ai.iloc[-1]:.0f}%  construction {con.iloc[-1]:.0f}%  ({ai.index[-1]:%Y-%m})")
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
