# Literature Review: AI, Employment, and Firm Dynamics

**Created:** 2026-10-29  
**Purpose:** Position our paper in the existing literature and identify the specific gap we fill.

---

## Executive Summary: What's Been Written and What Hasn't

### The Gap Our Paper Fills

**Nobody has written this exact paper.** The existing literature studies:
1. AI's effect on employment *within* firms (productivity, displacement)
2. AI's effect on task composition and wages
3. Firm dynamics and entry in general
4. Cloud computing's effect on startup formation

**What's missing:** A model that combines (1) labor-saving effects at incumbents with (2) lower entry costs for new firms, asking whether the second channel can *offset* the first. We bring these strands together using cloud computing as an empirical analogue.

---

## 1. Core Literature We Must Cite

### 1.1 AI and Automation Effects on Labor (Within-Firm)

| Paper | Key Finding | Relevance to Us |
|-------|-------------|-----------------|
| **Acemoglu & Restrepo (2018, 2019)** | Task-based framework: automation displaces labor in existing tasks, but new tasks can reinstate it | Our theoretical foundation. We extend this to ask: what if new tasks come via *new firms*? |
| **Acemoglu (2024) "Simple Macroeconomics of AI"** | AI's GDP effects are modest (0.53-0.66% TFP over 10 years) because task-level gains don't aggregate dramatically | Skeptical baseline. He doesn't consider entry margin. |
| **Brynjolfsson, Li & Raymond (2023/2025)** | AI at customer support firm: +14% productivity, +34% for novices | Micro evidence of augmentation. Our Anthropic S-1 data extends this to a firm that *produces* AI. |
| **Noy & Zhang (2023)** | Experimental: AI raises productivity 30-40% in writing tasks | Task-level evidence we cite |
| **Eloundou et al. (2024) "GPTs are GPTs"** | 80% of US workers in occupations with 10%+ task exposure; 19% with 50%+ | Breadth measure. We use their exposure scores. |
| **Graetz & Michaels (2018)** | Industrial robots: productivity up, employment down, but small aggregate effects | Earlier automation precedent |

### 1.2 Firm Dynamics and Entry

| Paper | Key Finding | Relevance to Us |
|-------|-------------|-----------------|
| **Hopenhayn (1992)** | Canonical model of firm entry/exit with endogenous size distribution | Our model's foundation |
| **Luttmer (2007)** | Selection on productivity explains Pareto firm size distribution | We extend with AI-enhanced productivity |
| **Haltiwanger, Jarmin & Miranda (2013)** | Job creation is about *age*, not size: young firms drive net growth | Critical for our "graduation" analysis. AI labs are young. |
| **Decker et al. (2014, 2016, 2020)** | Declining business dynamism in US since 2000 | The secular trend we must control for |
| **Akcigit & Ates (2021)** | 10 facts on declining dynamism; knowledge diffusion matters | Context for why AI *might* reverse the trend |

### 1.3 Cloud Computing and Startup Formation

| Paper | Key Finding | Relevance to Us |
|-------|-------------|-----------------|
| **Ewens, Nanda & Rhodes-Kropf (2018)** | Cloud lowered experimentation costs → more "spray and pray" VC | Our empirical analogue for entry-cost reduction |
| **Jin & McElheran (2017)** | Cloud improved survival and performance of young plants | Entry margin evidence |

### 1.4 AI and Firm-Level Outcomes

| Paper | Key Finding | Relevance to Us |
|-------|-------------|-----------------|
| **Babina et al. (2024)** | AI investment correlates with firm growth and product innovation | Firm-level evidence, but doesn't address entry |
| **Felten, Raj & Seamans (2021)** | AI exposure measure by occupation/industry | We use this for sector heterogeneity |

---

## 2. Papers That Come Close But Don't Fill Our Gap

### 2.1 Chandar & Klein Teeselink (2026) "How Does AI Change Labor Demand?"

From the Google Scholar results: "Evidence from 41 countries... can offset labor saving, so employment could grow even for groups whose tasks are partially displaced."

**How it differs:** Cross-country empirical, not a firm dynamics model. Doesn't model the *mechanism* of offset through entry.

### 2.2 Vivarelli & Arenas Díaz (2026) "New Technologies and Employment: State of the Art"

"Are job losses due to the advent of robots and AI structural... companies can offset the displacement effects."

**How it differs:** Survey/synthesis paper, not original model or empirics.

### 2.3 IMF Staff Discussion Note (2024) "Gen-AI and the Future of Work"

Couldn't access full text, but from description: focuses on policy recommendations and aggregate scenarios, not firm dynamics.

### 2.4 OECD Employment Outlook (2024/2025)

Aggregate statistics and policy discussion. No firm-level model.

---

## 3. Literature We Should Add to References

### 3.1 Must-Add (core to our argument)

```bibtex
@article{acemoglu2020robots,
  author  = {Acemoglu, Daron and Restrepo, Pascual},
  title   = {Robots and Jobs: Evidence from {US} Labor Markets},
  journal = {Journal of Political Economy},
  year    = {2020},
  volume  = {128},
  number  = {6},
  pages   = {2188--2244}
}

@techreport{korinek2024scenarios,
  author      = {Korinek, Anton and Suh, Donghyun},
  title       = {Scenarios for the Transition to {AGI}},
  institution = {National Bureau of Economic Research},
  type        = {NBER Working Paper},
  number      = {32255},
  year        = {2024}
}

@article{autor2022new,
  author  = {Autor, David and Chin, Caroline and Salomons, Anna and Seegmiller, Bryan},
  title   = {New Frontiers: The Origins and Content of New Work, 1940--2018},
  journal = {Quarterly Journal of Economics},
  year    = {2022},
  volume  = {139},
  number  = {3},
  pages   = {1399--1465}
}

@article{webb2020impact,
  author  = {Webb, Michael},
  title   = {The Impact of Artificial Intelligence on the Labor Market},
  journal = {Working Paper},
  year    = {2020},
  note    = {Stanford University}
}
```

### 3.2 Should-Add (context and robustness)

```bibtex
@article{bessen2020automation,
  author  = {Bessen, James E.},
  title   = {Automation and Jobs: When Technology Boosts Employment},
  journal = {Economic Policy},
  year    = {2020},
  volume  = {34},
  number  = {100},
  pages   = {589--626}
}

@article{arntz2017risk,
  author  = {Arntz, Melanie and Gregory, Terry and Zierahn, Ulrich},
  title   = {Revisiting the Risk of Automation},
  journal = {Economics Letters},
  year    = {2017},
  volume  = {159},
  pages   = {157--160}
}

@article{frey2017future,
  author  = {Frey, Carl Benedikt and Osborne, Michael A.},
  title   = {The Future of Employment: How Susceptible Are Jobs to Computerisation?},
  journal = {Technological Forecasting and Social Change},
  year    = {2017},
  volume  = {114},
  pages   = {254--280}
}
```

### 3.3 For the Infrastructure vs Applications Discussion

```bibtex
@article{goldfarb2023could,
  author  = {Goldfarb, Avi and Teodoridis, Florenta},
  title   = {Could Machine Learning Be a General Purpose Technology? {A} Comparison of Emerging Technologies Using Data from Online Job Postings},
  journal = {Research Policy},
  year    = {2023},
  volume  = {52},
  number  = {1},
  pages   = {104653}
}
```

---

## 4. Our Unique Contribution (Positioning Statement)

**We are the first to:**

1. **Model both channels jointly.** Existing work studies displacement OR entry, not both in a unified framework with endogenous offset.

2. **Use cloud computing as a disciplined analogue.** Rather than speculating about AI's entry effects, we measure how a previous technology shock (cloud) affected entry in exposed sectors, and apply that response function to AI.

3. **Derive conditions for offset.** We don't just ask "will AI create or destroy jobs?" but "under what parameter values does creation offset destruction?" The threshold σ_ai ≈ 2.78 and the dominance of substitution elasticity (71% of variance) over entry costs (3%) are novel results.

4. **Distinguish infrastructure from application layers.** The discussion section's analysis of labs-as-hyperscalers vs. application companies like Cursor is new framing for the AI employment literature.

5. **Use primary S-1 data from an AI lab.** The Anthropic S-1 extract (90% of code written by Claude, 45× increase in code per engineer) is the first audited evidence on how AI labs view their own technology's labor effects.

---

## 5. Potential Competing Papers to Monitor

Based on the search results, watch for:

1. **Chandar & Klein Teeselink (2026)** — if they've modeled firm dynamics, they could be close
2. **Any Acemoglu follow-up to w32487** — he may extend to entry margin
3. **Stanford HAI 2026/2027 Index** — may synthesize firm-level evidence we need

---

## 6. Citation Strategy for the Paper

### Introduction (Section 1)
- Cite Noy & Zhang, Brynjolfsson et al. for productivity gains
- Cite Acemoglu (2024) for skeptical macro view
- Cite Eloundou for exposure breadth
- Cite Haltiwanger for age-vs-size finding
- Cite Decker for declining dynamism context

### Theory (Section 2)
- Cite Hopenhayn, Luttmer for model foundation
- Cite Acemoglu & Restrepo (2018, 2019) for task framework
- Cite Lucas (1978), Klette & Kortum for size distribution

### Cloud Parallel (Section 3)
- Cite Ewens, Nanda & Rhodes-Kropf for entry-cost evidence
- Cite Jin & McElheran for survival evidence
- Cite BDS/Census for data

### AI Model and Simulation (Sections 4-5)
- Cite Felten for exposure measure
- Cite Eloundou for task exposure

### Empirical Signatures (Section 6)
- Cite BTOS for adoption patterns
- Cite BFS for application data

### Discussion (Section 7)
- Cite Anthropic S-1 for productivity evidence
- Cite Brynjolfsson (2021) for J-curve/complementary investments
- Cite Autor (2020) for superstar firms

---

## 7. What We Should NOT Claim

1. **Don't claim we're first to study AI and employment** — huge literature exists
2. **Don't claim we prove offset will happen** — we show conditions, P(offset)=81.7% under our priors
3. **Don't claim cloud perfectly parallels AI** — we acknowledge the analogy's limits in Section 7
4. **Don't claim firm-level evidence** — our evidence is aggregate BDS/BFS, not matched employer-employee data
