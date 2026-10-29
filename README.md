# Fewer Giants, More Firms?

**Artificial Intelligence, Entry Costs, and the Firm Size Distribution**

*Gerard Spivey (gs@gspivey.com)*

---

## Overview

This repository contains the code and data for the working paper examining whether AI-induced firm formation can offset employment displacement at large incumbents.

**Key finding:** Under our priors, P(offset) = 81.7%, but this headline masks a threshold effect. Below σ_ai ≈ 2.78, offset is near-certain (99.8%); above it, the outcome depends on whether AI-native entrants are substantially more productive.

📄 **[Read the full paper (PDF)](https://www.gspivey.com/papers/ai-employment-offset-paper.pdf)**  
📝 **[Read the summary (blog post)](https://www.gspivey.com/posts/ai-jobs-offset-summary/)**

---

## Repository Structure

```
├── model/                  # Core simulation model
│   ├── firm_dynamics.py    # Hopenhayn-Luttmer firm dynamics
│   ├── parameters.py       # Calibration and priors
│   ├── simulation.py       # Single-run simulation
│   └── monte_carlo.py      # Monte Carlo analysis (2,000 draws)
│
├── paper/                  # LaTeX source
│   ├── main.tex            # Main document
│   ├── sections/           # Section files (01-08)
│   ├── figures/            # Generated figures
│   └── references.bib      # Bibliography (63 citations, 37 DOIs)
│
├── scripts/                # Analysis scripts
│   ├── bfs_causal_analysis.py    # BLS Business Formation Statistics
│   ├── europe_comparison.py      # US vs EU analysis
│   └── plot_sigma_threshold.py   # σ_ai threshold visualization
│
├── data/                   # Data and documentation
│   ├── claim_registry.md   # Verification status of empirical claims
│   ├── europe_evidence.md  # European data sources
│   ├── hyperscaler_verification.md  # Big Tech CapEx/layoffs verification
│   └── literature_review.md
│
├── companion/              # Study materials
│   └── math-companion.md   # Formula breakdowns and reading list
│
├── tests/                  # Unit tests
└── requirements.txt        # Python dependencies
```

---

## Key Model Components

### The Displacement Threshold

The paper's central result: AI adoption raises firm headcount if and only if:

$$\sigma_{ai} < \frac{1}{1-\alpha} \approx 2.78$$

where σ_ai is the labor-AI substitution elasticity and α = 0.64 is the span-of-control parameter.

### Monte Carlo Design

- **2,000 draws** from parameter priors
- **Common random numbers** for AI vs counterfactual comparison
- **Sobol sensitivity indices** to decompose variance

| Parameter | Prior | Sobol S₁ |
|-----------|-------|----------|
| σ_ai (substitution elasticity) | U(2, 5) | 0.71 |
| Δμ_e (entrant productivity shift) | U(0, 0.15) | 0.18 |
| κ_e (entry cost reduction) | U(0.7, 1.0) | 0.03 |

---

## Running the Model

```bash
# Install dependencies
pip install -r requirements.txt

# Run single simulation
python -m model.simulation

# Run Monte Carlo analysis (takes ~10 minutes)
python -m model.monte_carlo --draws 2000 --output data/monte_carlo_raw.csv

# Generate figures
python scripts/plot_sigma_threshold.py
```

---

## Data Sources

- **BLS Business Formation Statistics** — establishment births, employer vs non-employer applications
- **Census BTOS** — AI adoption and employment effects at establishments
- **SEC 10-K filings** — Big Tech CapEx and layoffs (verified in `data/hyperscaler_verification.md`)
- **OECD** — European business dynamics, employment protection indices
- **Stanford HAI AI Index** — AI investment by region

---

## Citation

```bibtex
@unpublished{spivey2026fewer,
  author = {Spivey, Gerard},
  title = {Fewer Giants, More Firms? {Artificial} Intelligence, Entry Costs, and the Firm Size Distribution},
  year = {2026},
  note = {Working paper},
  url = {https://www.gspivey.com/papers/ai-employment-offset-paper.pdf}
}
```

---

## License

Code: MIT License  
Paper: © 2026 Gerard Spivey. All rights reserved.

---

## Contact

Gerard Spivey  
📧 gs@gspivey.com  
🌐 [gspivey.com](https://www.gspivey.com)
