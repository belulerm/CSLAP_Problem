# CSLAP Multi-Agent Research Project Constitution

## 1. Project Context
This repository contains research and implementation for the **Correlated Storage Location Assignment Problem (CSLAP)** in automated pick-and-pass warehouses.
* **Core Goal**: Minimize total station visits for order completion while balancing workload across picking stations.
* **Current Research Frontier**: Incorporating and addressing **uncertainty in warehouse data** (specifically demand data, processing speeds, capacities, and order arrival patterns).
* **Current Status**: A comprehensive set of baseline solvers exists in Python. Draft articles have been written in LaTeX. The robustness hypothesis **H1** (a covering-based **outer approximation** of orders that recasts CSLAP as a data-driven robust counterpart) has been taken end-to-end through the agent pipeline once and **ACCEPTED as a conditional / partial result**. **Next phase (READ `plan.md` FIRST): re-validate H1 on an exact solver (CPLEX) and on the clean `ISCF Data/` instance to remove the first-run biases.** See §7 below.

## 2. Technology Stack
* **Optimization & Modeling**: Python 3.10+, **CPLEX (`docplex`) — the exact solver for the current phase (cover construction + placement MILP)**, Gurobi (`gurobipy`, may be absent on a given machine — verify before relying on it), Hexaly (formerly LocalSolver; metaheuristic, no LP duals, cannot drive the cover's column generation).
* **Data Science & Analytics**: `pandas`, `numpy`, `scipy` (HiGHS via `scipy.optimize` was the first-run fallback; it is weak on the integer master and forced support subsampling — prefer CPLEX now).
* **Academic Publishing**: LaTeX (`elsarticle` document class), Tectonic engine for local compiles

## 3. Codebase Map
* **Solver Baselines**: Located in [Baselines](file:///c:/Users/ebelul/My%20Savoye%20project/CSLAP_Problem/Different_Solution_Approaches/Full_Package_Code_With_All_Approaches/CSLAP-Synthetic/Baselines/)
  - [milp_gurobi_synthetic.py](file:///c:/Users/ebelul/My%20Savoye%20project/CSLAP_Problem/Different_Solution_Approaches/Full_Package_Code_With_All_Approaches/CSLAP-Synthetic/Baselines/milp_gurobi_synthetic.py): Gurobi MILP model
  - [milp_synthetic.py](file:///c:/Users/ebelul/My%20Savoye%20project/CSLAP_Problem/Different_Solution_Approaches/Full_Package_Code_With_All_Approaches/CSLAP-Synthetic/Baselines/milp_synthetic.py): Hexaly MILP model
  - [cg_gurobi_synthetic.py](file:///c:/Users/ebelul/My%20Savoye%20project/CSLAP_Problem/Different_Solution_Approaches/Full_Package_Code_With_All_Approaches/CSLAP-Synthetic/Baselines/cg_gurobi_synthetic.py): Column Generation using Gurobi
  - [cg_synthetic.py](file:///c:/Users/ebelul/My%20Savoye%20project/CSLAP_Problem/Different_Solution_Approaches/Full_Package_Code_With_All_Approaches/CSLAP-Synthetic/Baselines/cg_synthetic.py): Column Generation using Hexaly
  - [heuristic_synthetic.py](file:///c:/Users/ebelul/My%20Savoye%20project/CSLAP_Problem/Different_Solution_Approaches/Full_Package_Code_With_All_Approaches/CSLAP-Synthetic/Baselines/heuristic_synthetic.py): Clustering heuristics
  - [ga_baseline.py](file:///c:/Users/ebelul/My%20Savoye%20project/CSLAP_Problem/Different_Solution_Approaches/Full_Package_Code_With_All_Approaches/CSLAP-Synthetic/Baselines/ga_baseline.py): Genetic Algorithm baseline
  - [sa_correlated.py](file:///c:/Users/ebelul/My%20Savoye%20project/CSLAP_Problem/Different_Solution_Approaches/Full_Package_Code_With_All_Approaches/CSLAP-Synthetic/Baselines/sa_correlated.py): Simulated Annealing baseline
* **Robustness pre-process (P–K covering, H1)**: in the same `Baselines/` directory —
  - `pk_cover_construction.py`: the column-generation cover (min–max Π partition; eqs. 6–9 of `reports/2_method_report.md`). Add a `--backend cplex` path this phase.
  - `pk_instance_robust.py`: the transform that replaces each order by its pattern-closure (the enlarged instance).
  - `evaluate_layout_robust.py`: fixed-layout evaluator (counts visits on **real** orders).
  - `run_robustness_experiment.py`: the experiment harness (folds, leakage guards, metrics).
  - `build_berner_instance.py`: rebuilds BERNER train/test instances from the raw order-lines.
* **LaTex Articles**: Located in [LaTeX_Articles_We_Have_Drafted](file:///c:/Users/ebelul/My%20Savoye%20project/CSLAP_Problem/LaTeX_Articles_We_Have_Drafted/) — current draft: `CSLAP_Robust_Covering_draft.tex`.
* **Pipeline reports**: `reports/0_research_brief.md` … `reports/6_writer_report.md` (brief, SotA, method, coder log, code review, two scientific audits, writer report).
* **Data**:
  - `ISCF Data/` — **PRIMARY clean test instance** (4,328 SKUs; 8 uniform stations × 541 slots; ~419k orders; comma-CSV; capacity is κ-invariant). Build instances via a new `Baselines/iscf_adapter.py`.
  - BERNER raw order-lines: `Different_Solution_Approaches/Full_Package_Code_With_All_Approaches/CSLAP-Synthetic/Heuristic_Connex_Set_Project/data/BERNER_ORDER_LINES_09-12.csv` — **industrial validation**.
  - The previously generated synthetic Zhang datasets (`synthetic_datasets/`) and the generator (`Data_Generators/synthetic_data_zhang.py`) have been **removed / retired for testing — do not use them**.
* **Agent Skills**: Pre-packaged capabilities reside in [skills](file:///c:/Users/ebelul/My%20Savoye%20project/CSLAP_Problem/skills/)

## 4. Multi-Agent Swarm & Co-Work Rules
1. **Pipeline Execution**: You operate as part of a multi-agent pipeline: Researcher → Method Selector → Optimization Coder → Code Reviewer → Scientific Reviewer → Academic Writer. Follow the protocol in [.claude/rules/agent-pipeline-protocol.md](file:///c:/Users/ebelul/My%20Savoye%20project/CSLAP_Problem/.claude/rules/agent-pipeline-protocol.md).
2. **Context Compaction & Sub-Agents**: Avoid loading large datasets (CSV, logs, etc.) into the main session. Delegate heavy read/analysis tasks to ephemeral sub-agents, and only request high-level summaries.
3. **No direct vscode/IDE configurations**: All workspace-specific config must exist within `.claude/`. Do not commit `.vscode` files or other IDE-specific files in the project root.
4. **Token Efficiency (Caveman Mode)**: Speak in caveman style (drop filler, pleasantries, hedging, and articles) in all intermediate chat logs and reasoning steps to optimize token utilization. (Ref: [skills/caveman/SKILL.md](file:///c:/Users/ebelul/My%20Savoye%20project/CSLAP_Problem/skills/caveman/SKILL.md)).


## 5. Documentation Routing Matrix
* **Sub-Agent Profiles**: Defined in [.claude/agents/](file:///c:/Users/ebelul/My%20Savoye%20project/CSLAP_Problem/.claude/agents/)
* **Development Standards**: Detailed in [.claude/rules/](file:///c:/Users/ebelul/My%20Savoye%20project/CSLAP_Problem/.claude/rules/)
* **Workspace Settings**: Specified in [.claude/settings.json](file:///c:/Users/ebelul/My%20Savoye%20project/CSLAP_Problem/.claude/settings.json)
* **Custom Skills**: Available in [skills/](file:///c:/Users/ebelul/My%20Savoye%20project/CSLAP_Problem/skills/)

## 6. Project Knowledge Graph (graphify)
* **Skill**: [`graphify`](file:///c:/Users/ebelul/My%20Savoye%20project/CSLAP_Problem/skills/graphify/SKILL.md) — builds a persistent knowledge graph of the entire project (code, LaTeX, skills, agent defs).
* **Trigger**: `/graphify`
* **Purpose**: Navigate the CSLAP codebase without reading every file. Query the graph for entities, relationships, and cross-module connections at ~70× fewer tokens than raw file reads.
* **First-run (one-time)**: `/graphify .` to build `graphify-out/graph.json` + `GRAPH_REPORT.md`.
* **Incremental update**: `/graphify . --update --no-viz` after new files are added or modified.
* **Query pattern**: `/graphify query "<concept>"` replaces broad Glob/Grep sweeps across unknown directories.
* **Cost rule**: Agents MUST query the graph before doing `Glob`/`Grep` sweeps across unknown directories. Only do direct file reads after graph query returns insufficient detail.

## 7. Current Research State & Next Phase (READ FIRST)

**The full plan lives in [`plan.md`](file:///c:/Users/ebelul/My%20Savoye%20project/CSLAP_Problem/plan.md). Read it before doing anything in this phase.**

**Where we are.** Hypothesis **H1** — enlarge each order to its covering pattern-closure (a data-driven **outer approximation** of demand), then optimize placement on the enlarged instance — was taken once through the pipeline. Theory is sound: optimizing on the enlarged orders is *identically* a robust counterpart of CSLAP (Prop. 1 in `reports/2_method_report.md`); κ is the conservatism knob. Empirically the result was **conditional**: the price of robustness was stable, the out-of-sample gain was not.

**Why we re-test now (this machine has CPLEX).** The first run's weaknesses were tooling/data, not theory:
1. No exact solver (HiGHS fallback) → weak integer master → **forced support subsampling** → the reported bottleneck Π=34 was not the true Π=369; the Π*=6 acceptance test was never reproduced.
2. Metaheuristic suboptimality produced a "benign free lunch" (robust layout cheaper on train too) — explainable, but it muddies the price-of-robustness reading.
3. A frequency-based time-capacity **recalibration confound** mixed enlargement with capacity loosening.
4. Single train seed / single industrial cell → no confidence intervals.
5. Workload feasibility was not enforced (the clustering heuristic overloaded one station ~16×; κ=2 worsened the peak) — the industrial "win" was visits-only.

**Next steps (summary; full detail in `plan.md`).**
- Use **CPLEX** (`docplex`) for the cover construction (full, no subsample → certify Π_true; reproduce Π*=6) AND for an exact placement MILP (enforces feasibility, makes PoR ≥ 0 hold at optimality).
- Test on the clean **`ISCF Data/`** instance, whose **κ-invariant capacity removes the recalibration confound by construction**. Use **repeated K-fold random train/test splits** for confidence intervals (the Zhang synthetic generator is retired).
- Always **count visits on the REAL orders**; the closures only shape placement.
- Re-validate on **BERNER** with multiple temporal cuts; report per-station feasibility.
- Then refresh `reports/` and `CSLAP_Robust_Covering_draft.tex` to whatever the exact, multi-fold evidence supports — upgrade or retract claims honestly.
