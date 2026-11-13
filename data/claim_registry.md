# Claim Registry

Tracks the quantitative claims in the current paper (`paper/`) and its summary post, where each comes from, and whether it has been checked against a primary source. Rows from earlier drafts that the paper no longer makes have been removed (see git history).

**Legend:**
- ✓ = Verified against a primary source (filing, official data, or the cited paper itself)
- ⚠ = Secondary source only (press, reprint of a blocked primary, or a single unnamed source)
- ✗ = No primary source found; the paper must hedge or drop it
- = = Computed by code in this repository

Detailed evidence, quotes and URLs: `data/claim_sources_2026-11.md` (AI firms, cloud-era firms, acquisitions, BTOS), `data/hyperscaler_verification.md` (Microsoft and hyperscaler capex), `data/bfs_causal_analysis.md` (Census BFS tests), `data/monte_carlo_results.md` and `data/monte_carlo_aicost_results.md` (simulation).

---

## Model and simulation (Sections 4–5)

| Claim | Value | Source | Status |
|---|---|---|---|
Shares below are shares of Monte Carlo draws under assumed priors. They are not probabilities about the world and
must not be quoted as odds (referee round 1, rule 1). The original runs hold the AI price fixed, which confounds
sigma_ai with the size of the shock; prefer the normalized results.

| Claim | Value | Source | Status |
|---|---|---|---|
| Single-firm displacement threshold | σ_ai < θ, the scale elasticity; θ = 1/(1−α) = 2.78 only at α = 0.64 | Proposition 1 (Hicks–Marshall application) | ✓ |
| Industry offset condition; entrant quality vs entry cost | Propositions 2–3 of the note | `note/note.tex`, `data/note_numbers.md` | ✓ (derived) |
| Normalized regime map | net labor-demand effect by σ_ai × entrant shift, 10 seeds per cell | `data/regime_map.md` | = |
| Normalized Monte Carlo variance shares (σ_ai / entrant shift / entry cost) | 0.62 / 0.25 / 0.04 (original: 0.71 / 0.19 / 0.04) | `data/monte_carlo_normalized_results.md` | = |
| Original Monte Carlo replications | 2,000 draws + 60 noise runs, seed 2026 | `scripts/monte_carlo_t6.py` | = (superseded framing) |
| Share of draws with offset given large-firm employment falls, AI price fixed | 59.2% | `monte_carlo_results.md` | = (do not quote as odds) |
| Same, AI price drawn | 44.5% | `monte_carlo_aicost_results.md` | = (do not quote as odds) |
| Same, alternative σ_ai priors | 55.7–63.3% | `prior_sensitivity.md` | = (do not quote as odds) |
| Unconditional share of draws with offset | 81.7% (fixed price), 74.7% (drawn) | as above | = (do not quote as odds) |
| Mean output effect, original | +61% (median +48%); an upper bound, wages and prices fixed | `monte_carlo_results.md` | = |
| Europe vs US shares of draws | 69.7% vs 81.7% (all draws); 43.6% vs 61.0% (given large-firm decline) | `europe_comparison.md` | = (do not quote as odds) |

## Census data (Sections 3, 6, 7)

| Claim | Value | Source | Status |
|---|---|---|---|
| Business applications, Jan–Sep 2026 vs 2025 | +15.3% | Census BFS (`bfs_raw/`) | ✓ |
| Applications with planned wages, same window | −15.3% | Census BFS | ✓ |
| High-propensity applications, same window | +4.7% | Census BFS | ✓ |
| AI-exposed sectors (51+54) gap onset | March 2025; ≈ +41% (0.34 log pts) by Sep 2026 | `bfs_causal_analysis.md` | = |
| 2026 gap rank among sector pairs | 10th of 171 (one-sided permutation p = 0.058) | `bfs_causal_analysis.md` | = |
| AI-using firms reporting AI-driven employment cuts / increases | 2.0% / 2.3% firm-weighted (2.4% / 3.7% employment-weighted); denominator is AI-using firms | Bonney et al. (2026), NBER w35141, Table 4 | ✓ |

## AI and cloud-era firms (Section 7)

| Claim | Value | Source | Status |
|---|---|---|---|
| CoreWeave employees / revenue, 2025 | 2,189 / $5.13B | FY2025 10-K | ✓ |
| CoreWeave debt, June 2026 | ≈ $35.1B (sum of four balance-sheet lines) | Q2 2026 10-Q | ✓ (by summation) |
| Microsoft share of CoreWeave revenue | 67% of 2025 revenue | FY2025 10-K | ✓ |
| Cursor ARR | $3B, late April 2026 | Bloomberg (via reprint) | ⚠ |
| Cursor headcount | ≈ 800, May 2026 | Business Insider (via reprint) | ⚠ |
| Cursor acquisition | $60.0B implied equity value, closed 14 Aug 2026 | SpaceX 8-Ks | ✓ |
| Lovable ARR / headcount | $400M / 146, Feb 2026 | TechCrunch | ⚠ |
| Lovable valuation | $13.3B, Aug 2026 | Company blog, TechCrunch | ✓ |
| Vercel valuation / run-rate / headcount | $9.3B (Sep 2025) / $340M (Feb 2026) / 550 (Jan 2025) | Company blog / TechCrunch citing Forbes / Fortune | ⚠ (dates mismatch) |
| Snowflake revenue / employees, FY to Jan 2021 | $592.0M / 2,495 | 10-K | ✓ |
| Snowflake valuation | $33.3B at IPO price (>$70B first-day close) | CNBC, Bloomberg | ⚠ |
| Databricks valuation / ARR, 2021 | $38B / >$800M ARR at end-2021 | Press release / TechCrunch | ✓ / ⚠ |
| Databricks 2021 headcount | — | none found | ✗ (removed from table) |
| xAI value in SpaceX merger | $250B | Reuters, one unnamed source | ⚠ |
| AI-native startups smaller in headcount | 12–25% | Kim & Koning (2026), HBS WP 26-090 | ✓ |
| OpenAI and CoreWeave valuations in `tab:ai-vs-cloud` | $840B / $27B | press estimates | ⚠ |
| GenAI exposure broader than cloud | — | no direct comparison found; paper now says it is a conjecture | ✗ |

## Hyperscalers (Section 7)

See `data/hyperscaler_verification.md` (verified 2026-10-29): Microsoft's ~60,000-employee voluntary exit offer (eligibility, not exits), ~9,000 layoffs from July 2025, ~$175B calendar-2026 capex guidance.

---

## Open items

1. **MEDIUM**: Open the Bloomberg (Cursor ARR) and Business Insider (Cursor headcount) originals; current quotes come from reprints.
2. **MEDIUM**: Find a primary 2021 Databricks headcount if the table should show its revenue per employee.
3. **LOW**: Primary sources for the OpenAI and CoreWeave valuations in `tab:ai-vs-cloud`.

Last updated: 2026-11-07
