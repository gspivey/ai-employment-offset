"""Blog figure: new business applications vs. applications planning to pay wages.

Annual US totals (not seasonally adjusted) from the Census Business Formation
Statistics file in data/bfs_raw/bfs_monthly.csv, full years 2005-2025.
Writes paper/figures/blog_applications.png. Sized and lettered for phones.

Usage
    .venv/bin/python scripts/plot_blog_applications.py
"""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import pandas as pd  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "bfs_raw" / "bfs_monthly.csv"
OUT = ROOT / "paper" / "figures" / "blog_applications.png"
MONTHS = ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"]


def main() -> None:
    df = pd.read_csv(RAW, dtype=str)
    d = df[(df.sa == "U") & (df.naics_sector == "TOTAL") & (df.geo == "US") & df.series.isin(["BA_BA", "BA_WBA"])].copy()
    for c in MONTHS:
        d[c] = pd.to_numeric(d[c].str.replace(",", ""), errors="coerce")
    d["year"] = d["year"].astype(int)
    d["total"] = d[MONTHS].sum(axis=1, min_count=12)  # full years only
    p = d.pivot(index="year", columns="series", values="total").dropna().loc[2005:2025] / 1e6

    fig, ax = plt.subplots(figsize=(8, 6.4), dpi=150)
    ax.plot(p.index, p["BA_BA"], color="#2a9d8f", lw=4)
    ax.plot(p.index, p["BA_WBA"], color="#e76f51", lw=4)
    last = p.index.max()
    ax.text(2005.2, 4.6, "All new business applications", fontsize=15, color="#2a9d8f", fontweight="bold")
    ax.annotate(f"{p['BA_BA'].iloc[-1]:.1f}M", (last, p["BA_BA"].iloc[-1]), xytext=(0, 10), textcoords="offset points",
                ha="center", fontsize=15, color="#2a9d8f", fontweight="bold")
    ax.annotate(f"Planning to pay wages\n{p['BA_WBA'].iloc[-1] * 1000:.0f}K", (last, p["BA_WBA"].iloc[-1]),
                xytext=(-10, 14), textcoords="offset points", ha="right", va="bottom", fontsize=15, color="#e76f51", fontweight="bold")
    ax.annotate(f"{p['BA_BA'].loc[2006]:.1f}M", (2006, p["BA_BA"].loc[2006]), xytext=(0, 10), textcoords="offset points",
                ha="center", fontsize=13, color="#2a9d8f")
    ax.annotate(f"{p['BA_WBA'].loc[2006] * 1000:.0f}K", (2006, p["BA_WBA"].loc[2006]), xytext=(0, 10), textcoords="offset points",
                ha="center", fontsize=13, color="#e76f51")
    ax.set_ylim(0, 6.2)
    ax.set_xlim(2004.5, 2025.8)
    ax.set_xticks(range(2005, 2026, 5))
    ax.set_ylabel("Applications per year (millions)", fontsize=14)
    ax.tick_params(labelsize=13)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.grid(axis="y", color="#dddddd")
    ax.set_title("More new businesses, fewer new employers", fontsize=19, fontweight="bold", loc="left", pad=14)
    fig.text(0.01, 0.01, "Source: Census Business Formation Statistics, US totals, not seasonally adjusted.", fontsize=11, color="#666666")
    fig.tight_layout(rect=(0, 0.03, 1, 1))
    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT)
    print(p.round(3).to_string())
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
