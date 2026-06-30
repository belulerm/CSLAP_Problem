---
name: placement-solver-hexaly-only
description: Placement/assignment MILP must run ONLY through Hexaly milp_synthetic.py — not Gurobi, not CPLEX, not GA/SA
metadata:
  type: feedback
---

For the CSLAP robustness (CPLEX) phase, the **product→station placement/assignment** must be
solved **only** through the Hexaly MILP `Baselines/milp_synthetic.py`. Do NOT run the Gurobi MILP
(`milp_gurobi_synthetic.py`), do NOT write/run a new CPLEX placement MILP, and do NOT run the GA
(`ga_baseline.py`) or SA (`sa_correlated.py`) baselines for placement.

**Why:** User directive (2026-06-19), overriding plan.md Phase D (which had said write `milp_cplex.py`
for exact placement) and CLAUDE.md (which named CPLEX for the placement MILP). CPLEX/`docplex` is
still used for the **cover construction** (`pk_cover_construction.py --backend cplex`, Phase B) and
the Pi*=6 acceptance test — only the placement solver is constrained to Hexaly.

**How to apply:** In `run_robustness_experiment.py`, the a_0 / a_kappa layouts are produced by the
Hexaly runner in `milp_synthetic.py` only. Skip the milp_cplex.py artifact from plan.md §5 Phase D.
Note the caveat: Hexaly is a metaheuristic (no global optimality guarantee), so plan.md G3's
"PoR>=0 holds at optimality" does not strictly apply — report the price-of-robustness empirically.

**TWO separate virtual environments (this machine), each for one job:**
- **CPLEX** (cover construction, `pk_cover_construction.py --backend cplex`):
  `C:\ermal\Virtual_Environment_CPLEX_1\Scripts\python.exe` — has docplex 2.29 / cplex 22.1.1, pandas,
  numpy; NO scipy, NO hexaly, NO gurobipy.
- **Hexaly/LocalSolver** (placement, `milp_synthetic.py`):
  `C:\ermal\Virtual_Environment_LocalSolver_3\Scripts\python.exe` — has hexaly.
Run each step with the matching interpreter. `prod_lines` is a parameter of `run_milp_hexaly`, so the
harness passes the kappa-invariant REAL_LINES (from the ISCF products file) instead of the recomputed
closure line counts — no baseline edit needed. See [[plan-cplex-phase-overview]].
