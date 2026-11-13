# Fewer Giants, More Firms?

**Artificial Intelligence, Entry Costs, and the Firm Size Distribution**

*Gerard Spivey (gs@gspivey.com)*

---

## Overview

Can firms created thanks to AI make up for the jobs that large incumbents shed as they adopt it? This repository
holds the model, data and LaTeX sources for three related outputs, each making a different claim:

| Output | Claim | Status | Source | PDF |
|---|---|---|---|---|
| **Short model note** | An analytical condition for when entry offsets displacement at adopters, and why entrant quality outweighs entry cost | Draft | `note/note.tex` | [`note/note.pdf`](note/note.pdf) |
| **Quantitative macro paper** | Magnitudes for employment, wages and the labor share in an equilibrium model whose entry channel is disciplined by data | In revision (see Current status below) | `paper/` | [`paper/main.pdf`](paper/main.pdf) |
| **Plain-language summary** | Offset is possible, but only under conditions we can name and watch | Mirrors the blog post | `layman-summary/summary.tex` | [`layman-summary/summary.pdf`](layman-summary/summary.pdf) |

**What the model shows.** New firms make up for jobs lost at adopting incumbents under some conditions and not
others. Entry offsets displacement when adopting firms grow rather than shrink (the labor-AI elasticity of
substitution is below the firm's scale elasticity), or when AI-native entrants are much more productive than the
entrants they replace. It fails when AI substitutes easily for labor and entrants are no better. Cheaper entry
matters much less than entrant quality unless the pool of potential founders is very elastic.

**What it does not show.** All results are labor demand at a fixed wage; the simulated economy is not calibrated;
Monte Carlo shares summarize assumed priors and are not probabilities about the world; the business-application
evidence is descriptive. The October 2026 draft of the paper is superseded and should not be cited.

<!-- TODO before sharing: update this link to the published post's URL (it will include the date, e.g. /posts/2026-11-12-ai-jobs-offset-summary/). -->
📝 **[Read the blog post](https://www.gspivey.com/posts/ai-jobs-offset-summary/)**

---

## Current status

| Area | Status |
|---|---|
| Substitutability vs. shock size | **Done.** Normalized CES (`ces_normalization="cost_saving"` in `model/parameters.py`); regime map (`scripts/regime_map.py`) and Monte Carlo (`scripts/monte_carlo_normalized.py`) re-run. The high-sigma "plateau" in the original runs was an artifact of the normalization. |
| Dependence of the threshold on returns to scale | **Done in the text and the note.** Stated for a general scale elasticity; the note's boundary figure varies alpha. Not yet in the uncertainty analysis with recalibration. |
| Presentation of Monte Carlo results | **Done.** Results shown as a regime map; shares of draws are not presented as probabilities. |
| Equilibrium closure (wages, product demand, business stealing) | **Not done.** Stated as a limitation; next workstream. |
| Calibration | **Partly.** Model-versus-data table added; simulated method of moments not done. |
| Cloud-era evidence | **Partly.** Used as motivation only; a cloud-era estimation is not done. |
| Business-application evidence | **Partly.** On the November 12, 2026 Census vintage, positioned against recent entry studies, with sensitivity to sector definitions; continuous-exposure study not done. |

---

## Repository structure

```
├── model/                       # Simulation model (firm dynamics, entry/exit, AI adoption)
│   ├── firm_dynamics.py         #   production, CES labor-AI bundle, normalization, entry and exit
│   ├── parameters.py            #   parameters and placeholders (incl. ces_normalization)
│   ├── simulation.py            #   one economy over time, AI run vs. no-AI twin
│   ├── calibration.py           #   moment targets (simulated method of moments is a stub)
│   └── monte_carlo.py           #   prior draws
├── note/                        # Short model note (LaTeX, bibliography, PDF)
├── paper/                       # Macro paper (LaTeX sections, figures, PDF)
├── layman-summary/              # Plain-language summary (LaTeX, PDF)
├── scripts/
│   ├── monte_carlo_t6.py            # original 2,000-draw Monte Carlo (AI price fixed)
│   ├── monte_carlo_normalized.py    # same draws, normalized CES
│   ├── monte_carlo_ai_cost.py       # sensitivity with the AI price drawn
│   ├── prior_sensitivity.py         # reweighting under alternative sigma priors
│   ├── regime_map.py                # sigma x entrant-shift map, 10 seeds per cell, both normalizations
│   ├── note_regime_boundary.py      # analytic numbers and figure for the note
│   ├── plot_note_regime.py          # simulated regime map for the note
│   ├── bfs_causal_analysis.py       # Census business-application event study and permutations
│   ├── plot_blog_bfs_gap.py         # summary chart: AI-exposed sectors vs. Construction
│   ├── baseline_moments.py, threshold_table.py, normalization_cost_saving.py, bfs_revision_numbers.py
│   └── europe_comparison.py, cloud_replication.py
├── data/
│   ├── bfs_raw/bfs_monthly.csv           # Census BFS, November 12, 2026 release
│   ├── bfs_raw/bfs_monthly_vintage-2026-10.csv  # earlier vintage used by the October draft
│   ├── regime_map.md, monte_carlo_*_results.md, note_numbers.md, prior_sensitivity.md
│   ├── sources.md                        # bibliography for the cloud-era and AI-era data notes
│   └── ...                               # cloud-era, Europe and S-1 data notes cited by the paper
└── tests/                       # unit tests (normalization, threshold sign flip, model invariants)
```

---

## Reproducing the results

```bash
python -m venv .venv && .venv/bin/pip install -r requirements.txt
.venv/bin/python -m pytest -q                                   # tests

.venv/bin/python scripts/regime_map.py --seeds 10                # regime map (about 1-2 min on 6 cores)
.venv/bin/python scripts/monte_carlo_normalized.py               # normalized Monte Carlo (about 4 min)
.venv/bin/python scripts/monte_carlo_t6.py                       # original Monte Carlo
.venv/bin/python scripts/note_regime_boundary.py                 # note numbers and boundary figure
.venv/bin/python scripts/plot_note_regime.py
.venv/bin/python scripts/bfs_causal_analysis.py                  # Census event study (uses data/bfs_raw)
```

The Census file is the public `bfs_monthly.csv` from the
[Business Formation Statistics](https://www.census.gov/econ/bfs/) page. The PDFs build with any LaTeX
distribution (or [Tectonic](https://tectonic-typesetting.github.io/)): run it on `paper/main.tex`,
`note/note.tex` and `layman-summary/summary.tex` from their own directories.

---

## Data sources

- **Census Business Formation Statistics**: business applications, planned-wage and high-propensity applications,
  projected employer formations
- **Census Business Trends and Outlook Survey** (AI supplement, via Bonney et al. 2026): AI use and AI-related
  employment changes
- **Business Dynamics Statistics, OECD, Eurostat, Stanford HAI AI Index**: firm dynamics and European comparisons
- **Company filings and press** for the descriptive company comparisons (cited in the paper's bibliography)

---

## Citation

```bibtex
@unpublished{spivey2026fewer,
  author = {Spivey, Gerard},
  title  = {Fewer Giants, More Firms? {Artificial} Intelligence, Entry Costs, and the Firm Size Distribution},
  year   = {2026},
  note   = {Working paper in revision; cite the repository, not the superseded October 2026 draft},
  url    = {https://github.com/gspivey/ai-employment-offset}
}
```

The views expressed are the author's own and do not represent those of any employer.

---

## License

Code: MIT License
Paper and note: © 2026 Gerard Spivey. All rights reserved.

---

## Contact

Gerard Spivey
📧 gs@gspivey.com
🌐 [gspivey.com](https://www.gspivey.com)
