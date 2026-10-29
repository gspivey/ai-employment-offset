# Claim Registry

Tracks empirical claims in the paper, their sources, and verification status.

**Legend:**
- ✓ = Verified against primary source
- ✗ = Needs primary source verification  
- ⚠ = Secondary source only (news, estimates)

---

## Big Tech Layoffs (Section 2)

| Claim | Value | Source | Status | Notes |
|-------|-------|--------|--------|-------|
| Meta layoffs 2022-2024 | 21,000 | SEC 10-K filings | ✓ | Verified by subagent |
| Google layoffs 2023-2024 | 12,000 | News reports | ⚠ | Need 10-K |
| Amazon layoffs 2023 | 27,000 | News reports | ⚠ | Need 10-K |
| Microsoft layoffs 2023 | 10,000 | News reports | ⚠ | Need 10-K |
| Total Big-5 workforce | ~9,000 net reduction | Calculation | ✓ | Corrected from 4.8k |

## Hyperscaler CapEx (Section 7)

| Claim | Value | Source | Status | Notes |
|-------|-------|--------|--------|-------|
| Big-4 cloud 2024 CapEx | $175B | 10-K filings | ✓ | MS+GOOG+AMZN+META |
| Microsoft 2024 CapEx | $44.5B | 10-K | ✓ | |
| Google 2024 CapEx | $52.5B | 10-K | ✓ | |
| Amazon 2024 CapEx | $48B | 10-K | ✓ | |
| Meta 2024 CapEx | $30B | 10-K | ✓ | |

## AI Application Companies (Section 3/7)

| Claim | Value | Source | Status | Notes |
|-------|-------|--------|--------|-------|
| Cursor valuation | $9B (Jan 2025) | TechCrunch | ⚠ | Secondary |
| Cursor ARR | $100M+ (2024) | Forbes | ⚠ | May be outdated |
| Cursor employees | ~100 | Estimates | ✗ | Need primary |
| Lovable valuation | $750M | TechCrunch | ⚠ | Secondary |
| Lovable employees | ~50 | Estimates | ✗ | Need primary |
| CoreWeave valuation | $35B | News | ⚠ | S-1 filed |
| CoreWeave debt financing | $12.9B | S-1 filing | ✓ | |

## BLS/BFS Data (Section 4)

| Claim | Value | Source | Status | Notes |
|-------|-------|--------|--------|-------|
| Establishment births 2024 | ~430,000/quarter | BLS BFS | ✓ | Primary data |
| Birth rate inflection | March 2025 | BLS BFS | ✓ | Corrected from 2023 |
| Small firm employment share | 47% | BLS | ✓ | |

## Model Parameters (Section 5)

| Claim | Value | Source | Status | Notes |
|-------|-------|--------|--------|-------|
| σ_ai threshold | 1/(1-α) ≈ 2.78 | Derived | ✓ | CES derivation |
| P(offset) US | 81.7% | Monte Carlo | ✓ | 10,000 runs |
| P(offset) Europe | ~70% | Monte Carlo | ✓ | Higher frictions |

## Literature Claims

| Claim | Source | Status | Notes |
|-------|--------|--------|-------|
| Acemoglu-Restrepo automation framework | AER 2018, 2019, 2020 | ✓ | DOIs verified |
| Webb 2020 AI exposure | Brookings | ✓ | DOI verified |
| Autor 2024 new work creation | NBER | ✓ | Working paper |
| Haltiwanger entry/exit dynamics | Multiple papers | ✓ | DOIs verified |

---

## Action Items

1. **HIGH**: Get primary sources for Cursor/Lovable employee counts
2. **MEDIUM**: Verify Google/Amazon/Microsoft layoffs against 10-K filings
3. **LOW**: Track down CoreWeave employee count from S-1

Last updated: 2025-01-15
