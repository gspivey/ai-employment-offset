"""Pre-trend, placebo and permutation tests on Census BFS business applications.

Question: did business applications in AI-exposed sectors (Information, NAICS 51;
Professional/scientific/technical, NAICS 54) diverge from other sectors only
after the late-2022 generative-AI shock, and do low-exposure sectors
(Construction, NAICS 23; Retail, NAICS 44-45) show the same pattern?

Data: Census BFS ``bfs_monthly.csv`` (seasonally adjusted, ``sa=A``, ``geo=US``),
19 NAICS sectors (TOTAL and NONAICS dropped). The annual outcome is the log of
the mean monthly SA count; 2026 uses Jan-Sep, the latest months available.

Specifications (sector and year fixed effects throughout; SEs clustered by
sector, CR1; small-cluster inference by permutation across sector pairs):
  1. Event study: y_st = a_s + g_t + sum_{k != 2022} b_k D_s 1[t=k] + e_st
  2. Pre-trend slope on 2010-2022: y_st = a_s + g_t + c D_s (t - 2022) + e_st
  3. Pooled DiD: post = 2023-2026 vs pre = 2015-2022 (and excluding 2020-21)
  4. Placebo sectors: D = {23, RET}, controls exclude 51/54
  5. Placebo timing: fake shock in 2016 on 2010-2019 (pre-COVID)
  6. Permutation: pooled DiD and pre-trend slope for all 171 sector pairs

Run from the workspace root:
    .venv/bin/python scripts/bfs_causal_analysis.py data/bfs_raw/bfs_monthly.csv
Writes data/bfs_causal_results.csv, data/bfs_event_study.csv and
paper/figures/bfs_{event_study,indices}.pdf. Write-up:
data/bfs_causal_analysis.md.
"""

from __future__ import annotations

import itertools
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
MONTHS = ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"]
TREATED = ["NAICS51", "NAICS54"]
PLACEBO = ["NAICS23", "NAICSRET"]
BASE_YEAR = 2022
YEARS = range(2010, 2027)
LABELS = {
    "NAICS11": "Agriculture", "NAICS21": "Mining", "NAICS22": "Utilities",
    "NAICS23": "Construction", "NAICSMNF": "Manufacturing", "NAICS42": "Wholesale",
    "NAICSRET": "Retail", "NAICSTW": "Transport/warehousing", "NAICS51": "Information",
    "NAICS52": "Finance/insurance", "NAICS53": "Real estate", "NAICS54": "Professional services",
    "NAICS55": "Management of companies", "NAICS56": "Admin/support", "NAICS61": "Education",
    "NAICS62": "Health care", "NAICS71": "Arts/recreation", "NAICS72": "Accommodation/food",
    "NAICS81": "Other services",
}


def load(path: Path, series: str, months: list[str] | None = None) -> pd.DataFrame:
    """Long panel (sector, year, y=log mean monthly SA applications)."""
    d = pd.read_csv(path, dtype=str)
    d = d[(d.geo == "US") & (d.sa == "A") & (d.series == series) & d.naics_sector.isin(LABELS)]
    x = d.set_index(["naics_sector", d.year.astype(int)])[months or MONTHS]
    x = x.apply(pd.to_numeric, errors="coerce")
    lvl = x.mean(axis=1).rename("level").reset_index()
    lvl.columns = ["sector", "year", "level"]
    lvl = lvl[lvl.year.isin(YEARS)]
    lvl["y"] = np.log(lvl.level)
    return lvl


def ols_cluster(y: np.ndarray, X: np.ndarray, groups: np.ndarray):
    """OLS with CR1 cluster-robust covariance."""
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    u = y - X @ beta
    bread = np.linalg.pinv(X.T @ X)
    meat = np.zeros((X.shape[1], X.shape[1]))
    ids = np.unique(groups)
    for g in ids:
        s = X[groups == g].T @ u[groups == g]
        meat += np.outer(s, s)
    n, k, G = X.shape[0], np.linalg.matrix_rank(X), len(ids)
    V = bread @ meat @ bread * (G / (G - 1)) * ((n - 1) / (n - k))
    return beta, V


def fe_design(df: pd.DataFrame, extra: pd.DataFrame) -> np.ndarray:
    """Columns of interest first, then sector and year dummies (one dropped)."""
    s = pd.get_dummies(df.sector, drop_first=True, dtype=float)
    t = pd.get_dummies(df.year, prefix="y", drop_first=True, dtype=float)
    return np.column_stack([extra.to_numpy(float), s, t, np.ones(len(df))])


def sample(df: pd.DataFrame, treated: list[str], exclude: list[str]) -> pd.DataFrame:
    out = df[~df.sector.isin([s for s in exclude if s not in treated])].copy()
    out["D"] = out.sector.isin(treated).astype(float)
    return out


def event_study(df: pd.DataFrame, base: int = BASE_YEAR) -> pd.DataFrame:
    years = [k for k in sorted(df.year.unique()) if k != base]
    extra = pd.DataFrame({k: df.D * (df.year == k) for k in years})
    b, V = ols_cluster(df.y.to_numpy(), fe_design(df, extra), df.sector.to_numpy())
    se = np.sqrt(np.diag(V))[: len(years)]
    es = pd.DataFrame({"year": years, "coef": b[: len(years)], "se": se})
    return pd.concat([es, pd.DataFrame({"year": [base], "coef": [0.0], "se": [0.0]})]).sort_values("year")


def pre_wald(df: pd.DataFrame, pre_years: list[int], base: int = BASE_YEAR) -> tuple[float, int]:
    """Cluster-robust Wald stat for H0: all pre-period event coefficients = 0."""
    years = [k for k in sorted(df.year.unique()) if k != base]
    extra = pd.DataFrame({k: df.D * (df.year == k) for k in years})
    b, V = ols_cluster(df.y.to_numpy(), fe_design(df, extra), df.sector.to_numpy())
    idx = [years.index(k) for k in pre_years]
    bb, VV = b[idx], V[np.ix_(idx, idx)]
    return float(bb @ np.linalg.pinv(VV) @ bb), len(idx)


def pre_slope(df: pd.DataFrame, lo: int = 2010, hi: int = BASE_YEAR) -> tuple[float, float]:
    """Differential linear trend of treated vs control over [lo, hi]."""
    d = df[df.year.between(lo, hi)]
    extra = pd.DataFrame({"trend": d.D * (d.year - hi)})
    b, V = ols_cluster(d.y.to_numpy(), fe_design(d, extra), d.sector.to_numpy())
    return float(b[0]), float(np.sqrt(V[0, 0]))


def did(df: pd.DataFrame, pre: list[int], post: list[int]) -> tuple[float, float]:
    d = df[df.year.isin(pre + post)]
    extra = pd.DataFrame({"post": d.D * d.year.isin(post)})
    b, V = ols_cluster(d.y.to_numpy(), fe_design(d, extra), d.sector.to_numpy())
    return float(b[0]), float(np.sqrt(V[0, 0]))


def did_fast(wide: pd.DataFrame, treated: list[str], pre: list[int], post: list[int]) -> float:
    """Balanced-panel DiD in means (identical to the FE regression point estimate)."""
    gap = wide.loc[treated].mean() - wide.drop(index=treated).mean()
    return float(gap[post].mean() - gap[pre].mean())


def slope_fast(wide: pd.DataFrame, treated: list[str], lo: int = 2010, hi: int = BASE_YEAR) -> float:
    gap = wide.loc[treated].mean() - wide.drop(index=treated).mean()
    yrs = np.arange(lo, hi + 1)
    return float(np.polyfit(yrs, gap[list(yrs)].to_numpy(), 1)[0])


def main(path: Path) -> None:
    pre_full = list(range(2015, 2023))
    pre_nocovid = [2015, 2016, 2017, 2018, 2019, 2022]
    post = [2023, 2024, 2025, 2026]
    rows, es_all = [], []

    for series in ["BA_BA", "BA_HBA"]:
        panel = load(path, series)
        designs = {
            "AI-exposed (51+54)": (TREATED, PLACEBO),
            "Information (51)": (["NAICS51"], PLACEBO + ["NAICS54"]),
            "Professional (54)": (["NAICS54"], PLACEBO + ["NAICS51"]),
            "Placebo: Construction+Retail": (PLACEBO, TREATED),
            "Placebo: Construction (23)": (["NAICS23"], TREATED + ["NAICSRET"]),
            "Placebo: Retail (44-45)": (["NAICSRET"], TREATED + ["NAICS23"]),
        }
        for name, (tr, ex) in designs.items():
            df = sample(panel, tr, ex)
            es = event_study(df).assign(design=name, series=series)
            es_all.append(es)
            w, k = pre_wald(df, list(range(2015, 2022)))
            sl, sl_se = pre_slope(df)
            d1, d1_se = did(df, pre_full, post)
            d2, d2_se = did(df, pre_nocovid, post)
            # placebo timing: fake 2016 shock, pre-COVID window
            dft = df[df.year <= 2019]
            d3, d3_se = did(dft, list(range(2010, 2016)), list(range(2016, 2020)))
            rows.append(dict(series=series, design=name, n_treated=len(tr), n_control=df[df.D == 0].sector.nunique(),
                             pretrend_slope=sl, pretrend_slope_se=sl_se, pre_wald_2015_2021=w, pre_wald_df=k,
                             did_post=d1, did_post_se=d1_se, did_post_nocovid=d2, did_post_nocovid_se=d2_se,
                             did_fake2016=d3, did_fake2016_se=d3_se))

        # permutation across all sector pairs (controls = all other sectors)
        wide = panel.pivot(index="sector", columns="year", values="y")
        perm = []
        for pair in itertools.combinations(wide.index, 2):
            perm.append(dict(pair="+".join(pair), did=did_fast(wide, list(pair), pre_full, post),
                             slope=slope_fast(wide, list(pair))))
        perm = pd.DataFrame(perm)
        perm.to_csv(ROOT / f"data/bfs_permutation_{series}.csv", index=False)

        # year-by-year permutation: rank of each design's event coefficient among all 171 pairs
        pairs = list(itertools.combinations(wide.index, 2))
        gaps = pd.DataFrame({"+".join(p): (wide.loc[list(p)].mean() - wide.drop(index=list(p)).mean()) for p in pairs}).T
        gaps = gaps.sub(gaps[BASE_YEAR], axis=0)
        yr = []
        for name, tr in [("AI-exposed (51+54)", TREATED), ("Placebo: Construction+Retail", PLACEBO)]:
            key = "+".join(sorted(tr, key=list(wide.index).index))
            for k in [y for y in YEARS if y >= 2015]:
                obs = gaps.loc[key, k]
                yr.append(dict(series=series, design=name, year=k, gap=obs,
                               rank_from_top=int((gaps[k] >= obs - 1e-12).sum()), n=len(gaps),
                               p_upper=float((gaps[k] >= obs - 1e-12).mean())))
        pd.DataFrame(yr).to_csv(ROOT / f"data/bfs_perm_by_year_{series}.csv", index=False)
        for name, tr in [("AI-exposed (51+54)", TREATED), ("Placebo: Construction+Retail", PLACEBO)]:
            obs = did_fast(wide, tr, pre_full, post)
            obs_sl = slope_fast(wide, tr)
            rows.append(dict(series=series, design=name + " [permutation, all controls]",
                             did_post=obs, perm_rank=int((perm.did >= obs - 1e-12).sum()), perm_n=len(perm),
                             perm_p=float((perm.did >= obs - 1e-12).mean()),
                             perm_p_twosided=float((perm.did.abs() >= abs(obs) - 1e-12).mean()),
                             pretrend_slope=obs_sl,
                             perm_p_slope_twosided=float((perm.slope.abs() >= abs(obs_sl) - 1e-12).mean())))

        # single-sector league table
        league = []
        for s in wide.index:
            league.append(dict(series=series, sector=s, label=LABELS[s],
                               did_post=did_fast(wide, [s], pre_full, post), pre_slope=slope_fast(wide, [s]),
                               growth_2022_2026=float(np.exp(wide.loc[s, 2026] - wide.loc[s, 2022]) - 1)))
        pd.DataFrame(league).sort_values("did_post", ascending=False).to_csv(
            ROOT / f"data/bfs_sector_league_{series}.csv", index=False)

        # Jan-Sep-only robustness (same months every year)
        js = load(path, series, MONTHS[:9])
        for name, (tr, ex) in [("AI-exposed (51+54) [Jan-Sep only]", (TREATED, PLACEBO)),
                               ("Placebo: Construction+Retail [Jan-Sep only]", (PLACEBO, TREATED))]:
            df = sample(js, tr, ex)
            sl, sl_se = pre_slope(df)
            d1, d1_se = did(df, pre_full, post)
            rows.append(dict(series=series, design=name, pretrend_slope=sl, pretrend_slope_se=sl_se,
                             did_post=d1, did_post_se=d1_se))

    res = pd.DataFrame(rows)
    res.to_csv(ROOT / "data/bfs_causal_results.csv", index=False)
    es_all = pd.concat(es_all)
    es_all.to_csv(ROOT / "data/bfs_event_study.csv", index=False)
    pd.set_option("display.width", 250, "display.max_columns", 30)
    print(res.round(4).to_string())

    # Figure 1: event study, treated vs placebo, total applications
    fig, axes = plt.subplots(1, 2, figsize=(10, 3.6), sharey=True)
    for ax, series, title in zip(axes, ["BA_BA", "BA_HBA"], ["All applications", "High-propensity applications"]):
        for name, color, off in [("AI-exposed (51+54)", "#2b6cb0", -0.12), ("Placebo: Construction+Retail", "#c05621", 0.12)]:
            e = es_all[(es_all.design == name) & (es_all.series == series)]
            ax.errorbar(e.year + off, e.coef, yerr=1.96 * e.se, fmt="o", ms=3.5, color=color, capsize=2,
                        lw=1, label=name.replace("Placebo: ", "Placebo: "))
        ax.axhline(0, color="0.5", lw=0.8)
        ax.axvline(2022.5, color="0.3", lw=0.8, ls="--")
        ax.set_title(title, fontsize=10)
        ax.set_xlabel("Year (base = 2022)")
        ax.grid(alpha=0.25)
    axes[0].set_ylabel("Log difference vs. other sectors")
    axes[0].legend(fontsize=8, loc="upper left", frameon=False)
    fig.tight_layout()
    fig.savefig(ROOT / "paper/figures/bfs_event_study.pdf")
    fig.savefig(ROOT / "data/bfs_event_study.png", dpi=150)

    # Monthly gap (log SA applications, treated-group mean minus other-15 mean), 2022 mean = 0
    d = pd.read_csv(path, dtype=str)
    d = d[(d.geo == "US") & (d.sa == "A") & (d.series == "BA_BA") & d.naics_sector.isin(LABELS)]
    m = d.melt(id_vars=["naics_sector", "year"], value_vars=MONTHS, var_name="month", value_name="v")
    m["v"] = pd.to_numeric(m.v, errors="coerce")
    m = m.dropna()
    m["date"] = pd.to_datetime(m.year + "-" + m.month, format="%Y-%b")
    mw = np.log(m.pivot(index="naics_sector", columns="date", values="v"))
    mw = mw.loc[:, mw.columns >= "2019-01-01"]
    others_m = mw.drop(index=TREATED + PLACEBO).mean()
    monthly = pd.DataFrame({
        "AI-exposed (51+54)": mw.loc[TREATED].mean() - others_m,
        "Information (51)": mw.loc["NAICS51"] - others_m,
        "Professional (54)": mw.loc["NAICS54"] - others_m,
        "Construction (23)": mw.loc["NAICS23"] - others_m,
        "Retail (44-45)": mw.loc["NAICSRET"] - others_m,
    })
    monthly = monthly - monthly[monthly.index.year == BASE_YEAR].mean()
    monthly.to_csv(ROOT / "data/bfs_monthly_gap.csv")

    fig, ax = plt.subplots(figsize=(6.5, 3.4))
    for col, c, lw in [("AI-exposed (51+54)", "#2b6cb0", 2.0), ("Construction (23)", "#c05621", 1.4),
                       ("Retail (44-45)", "#ed8936", 1.0)]:
        ax.plot(monthly.index, monthly[col], color=c, lw=lw, label=col)
    ax.axvline(pd.Timestamp("2022-12-01"), color="0.3", lw=0.8, ls="--")
    ax.axhline(0, color="0.5", lw=0.8)
    ax.set_ylabel("Log gap vs. other 15 sectors\n(2022 mean = 0)")
    ax.grid(alpha=0.25)
    ax.legend(fontsize=8, frameon=False, loc="upper left")
    fig.tight_layout()
    fig.savefig(ROOT / "paper/figures/bfs_monthly_gap.pdf")
    fig.savefig(ROOT / "data/bfs_monthly_gap.png", dpi=150)

    # Figure 2: log indices relative to 2022
    panel = load(path, "BA_BA")
    wide = panel.pivot(index="sector", columns="year", values="y")
    idx = wide.sub(wide[BASE_YEAR], axis=0)
    others = idx.drop(index=TREATED + PLACEBO).mean()
    fig, ax = plt.subplots(figsize=(6.5, 3.6))
    for s, c in [("NAICS51", "#2b6cb0"), ("NAICS54", "#63b3ed"), ("NAICS23", "#c05621"), ("NAICSRET", "#ed8936")]:
        ax.plot(idx.columns, idx.loc[s], color=c, lw=1.6, label=LABELS[s])
    ax.plot(others.index, others, color="0.2", lw=1.6, ls="--", label="Other 15 sectors (mean)")
    ax.axvline(2022.5, color="0.3", lw=0.8, ls="--")
    ax.axhline(0, color="0.5", lw=0.8)
    ax.set_ylabel("Log applications, 2022 = 0")
    ax.grid(alpha=0.25)
    ax.legend(fontsize=8, frameon=False)
    fig.tight_layout()
    fig.savefig(ROOT / "paper/figures/bfs_indices.pdf")
    fig.savefig(ROOT / "data/bfs_indices.png", dpi=150)


if __name__ == "__main__":
    main(Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "data/bfs_raw/bfs_monthly.csv")
