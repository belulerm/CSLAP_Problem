---
name: plan-cplex-phase-overview
description: State + key facts for the CSLAP H1 CPLEX-revalidation phase (plan.md); what's done and the scale constraints
metadata:
  type: project
---

Re-validating hypothesis **H1** (P–K covering enlargement = data-driven robust counterpart of CSLAP)
on an exact solver + clean ISCF data, per `plan.md`. H1 was previously ACCEPTED as conditional.
Goal: remove first-run biases (G1–G7) — exact solver, full cover (no subsample), kappa-invariant
capacity, repeated K-fold CIs, enforced feasibility. Count visits on REAL orders always.

**Two venvs (no single interpreter has both solvers)** — see [[placement-solver-hexaly-only]]:
cover = CPLEX venv; placement = Hexaly venv. So the harness must be **staged**: Stage 1 (CPLEX)
builds folds + enlarged instances; Stage 2 (Hexaly) runs placement + eval. Fold splits are seeded so
both stages agree.

**ISCF instance** (built by `Baselines/iscf_adapter.py` -> `iscf_instances/iscf_*.csv`):
4328 products, 418,849 orders, 997,198 lines, 8 stations x 541 slots (=|P|, balanced, kappa-invariant
capacity). products.csv carries extra cols REAL_LINES/VOLUME/FREQUENCY (kappa-invariant; read_data
ignores them). **54.9% of orders are size-1** (229,860) -> drop from placement (constant 1 visit) and
from cover constraints (touch 1 pattern). Distinct supports: 112,943 total, 108,820 of size>=2.

**Done:** Phase A (CPLEX + Hexaly runtimes verified; adapter built+validated). Phase B: `--backend
cplex` added to `pk_cover_construction.py` (docplex master LP duals + pricing MIP + integer master);
scipy imports made lazy so it loads in CPLEX venv. **Pi*=6 acceptance REPRODUCED** at k=6 on
`filtered_dataset.csv` (valid partition, checker pi=6) -> `logs/pk_cover_filtered_k6_cplex.json`.

**Scale caveat:** the CPLEX master rebuilds per CG iteration; with the ~20k step-(c) combo-seed flood
the LP took 242s/220 iters even on the 400-order acceptance case. For full ISCF use size>=2 supports +
`--cooccurrence-pairs` (suppresses the combo flood) and/or make the master incremental. Pi_true is
computed over ALL supports via `check_partition_and_pi` regardless of what the master optimized over.

**Placement via Hexaly:** harness imports `milp_synthetic.run_milp_hexaly` and passes kappa-invariant
REAL_LINES as `prod_lines` (param, no baseline edit). milp_synthetic objective is unweighted per-order
-> aggregate by distinct support (multiplicity handling is the open design point for Phase D).
