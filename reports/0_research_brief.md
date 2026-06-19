# Research Brief — CSLAP Robustness via Covering Constructions (Pipeline Canonical Reference)

This file is the canonical brief for all pipeline agents. Do not deviate from it.

## 0. Existing context (ground truth — do not re-derive)

The project folder contains the full current work on the Correlated Storage Location Assignment Problem (CSLAP), solved on deterministic input data. Orders are sets of products: each order ID maps to a set of products. Placement is optimized so that correlated products (frequently co-ordered) are stored close together.

Key assets (paths relative to repo root `c:\Users\ebelul\My Savoye project\CSLAP_Problem`):

* Filtered industrial order dataset (order → product list):
  `Different_Solution_Approaches/Full_Package_Code_With_All_Approaches/CSLAP-Synthetic/filtered_dataset.csv`
* Main full industrial dataset (order lines, Sep–Dec window):
  `Different_Solution_Approaches/Full_Package_Code_With_All_Approaches/CSLAP-Synthetic/Heuristic_Connex_Set_Project/data/BERNER_ORDER_LINES_09-12.csv`
  — We have exactly ONE dataset of orders. Sizeable but static; no second dataset and no externally
  given temporal split unless one is constructed from this data.
* Synthetic data generator (Zhang et al. 2019 common-itemset scheme):
  `Different_Solution_Approaches/Full_Package_Code_With_All_Approaches/CSLAP-Synthetic/Data_Generators/synthetic_data_zhang.py`
  Generated datasets: `Different_Solution_Approaches/Full_Package_Code_With_All_Approaches/CSLAP-Synthetic/synthetic_datasets/`
  (sizes: 20, 30, 50, 500, 1000, 2000, 5000 SKUs; schema: `*_orders.csv`, `*_stations.csv`, `*_products.csv`, sep=";")
* Existing solution approaches (ALL must be used for evaluation — the new method is an instance
  transformation, not a new isolated solver):
  `Different_Solution_Approaches/Full_Package_Code_With_All_Approaches/CSLAP-Synthetic/Baselines/`
  - `milp_gurobi_synthetic.py` (Gurobi MILP), `milp_synthetic.py` (Hexaly MILP)
  - `cg_gurobi_synthetic.py` / `cg_synthetic.py` (Column Generation, Gurobi/Hexaly)
  - `cg_gurobi_homogeneous.py`, `cg_hexaly_homogeneous.py`
  - `heuristic_synthetic.py` (clustering heuristics), `ga_baseline.py` (GA), `sa_correlated.py` (SA)
* Existing manuscript (notation + register to match):
  `LaTeX_Articles_We_Have_Drafted/Computers_and_Operations_Research_manuscript.tex`
* Existing P–K Set Cover implementation (MUST be reused, not reimplemented):
  `Different_Solution_Approaches/Topology_referal_from_another_problem/P-K Set Cover/p-k-set-cover/`
  (notebooks: `min_sum_p_exact.ipynb`, `new_alban_version.ipynb`, `new_alban_version_exact.ipynb`; see its `README.md`)

## 1. Research objective (HYPOTHESIS, not conclusion)

**Hypothesis H1.** Constructing larger product-sets from the observed orders via a covering / hitting-set construction, and optimizing placement over these enlarged sets, yields a layout that is more robust to future shifts in the order distribution than a layout optimized directly on the observed orders — at the cost of some degradation in nominal (observed-order) performance.

The pipeline's job is to formalize, implement, and test H1 — and to report honestly if it is false or only conditionally true. Do not assume the conclusion. A negative or partial result is an acceptable and valuable outcome.

## 2. Definitional tasks that MUST be resolved before coding (blocking)

The Method Selector cannot proceed until each has a committed answer.

1. **Approximation of WHAT?** Define the precise mathematical object the enlarged sets approximate (e.g., the empirical order/co-occurrence distribution, the product-correlation structure, or a set of plausible future demand scenarios). "Inner vs outer approximation" is undefined until this object is fixed.
2. **Inner vs outer — decide and prove.** Only after (1), determine whether the construction is an inner or outer approximation of that object, and state the mathematical sense (set inclusion, bound direction on an objective, containment of a feasible/uncertainty region). If neither label applies cleanly, say so and propose the correct terminology rather than forcing the fit.
3. **Minimality vs redundancy.** Standard set cover / hitting set optimize for a minimum cover. Robustness intuition favors coverage/redundancy. Justify which variant (minimal, maximal, redundant, weighted) actually serves H1, or document the mismatch explicitly.
4. **Uncertainty / perturbation model.** Commit to one: (a) a temporal split of the existing orders (train-early / test-late), and/or (b) an explicit perturbation model that generates plausible future order distributions from the observed one. This model IS the de facto uncertainty set; name it as such.
5. **Connection to a formal framework.** Locate H1 relative to stochastic programming, robust optimization, distributionally robust optimization, sample-average approximation. State which (if any) it instantiates, or argue precisely why it is a distinct heuristic. Do not claim it "handles uncertainty" without anchoring that claim to a formal definition.

## 3. Per-stage mandate

### Stage 1 — Researcher → Research report on uncertainty methods
* Deep literature review on: hitting set / set cover duality, set partitioning, covering formulations in OR; and optimization under uncertainty (robust opt, DRO, two-stage/multi-stage stochastic programming, scenario generation, SAA). Explicitly map each to the SLAP / warehouse-assignment setting where prior art exists.
* Do not fabricate references. Cite only sources that can be verified (DOI, venue, authors). If a claimed result cannot be located in its source, flag it. Distinguish "verified from source" from "plausible but unverified."
* Deliver a clear verdict on whether the proposed construction corresponds to any established named method, or is a novel hybrid. State uncertainty honestly.

### Stage 2 — Method Selector → Method selection + math formulation sketch
* Resolve all five blocking definitional tasks in §2 with committed answers.
* Produce a formal formulation: define the universe, the sets, the construction operator, the resulting enlarged instance, and how it feeds the existing solvers.
* State the bias–variance tradeoff explicitly as part of the formulation: what is gained, what is lost.
* Output the precise robustness metric(s) and the uncertainty/perturbation model to be used downstream.

### Stage 3 — Coder → Python implementation
* Reuse the existing P–K Set Cover code; do not reimplement from scratch.
* Implement: (a) the set-construction step, (b) the enlarged-instance generator, (c) the pipeline that runs the enlarged instance through each existing solution approach, (d) the perturbation/temporal-split harness from §2.4.
* Keep the deterministic baseline runnable for direct comparison.
* Follow `.claude/rules/code-standards.md` (CLI args --prefix/--dir/--time, type hints, LaTeX-math docstrings, standard return tuple, semicolon-CSV schema).

### Stage 4 — Code Reviewer → Bug report + math compliance
* Verify the implementation matches the Stage 2 formulation exactly (flag any divergence referencing the formulation's equation numbers).
* Confirm the perturbation harness does not leak test information into training.
* PASS / FAIL gate; on FAIL, return to Stage 3.

### Stage 5 — Scientific Reviewer → Accept / Revise
* Assess whether the experiments actually test H1 and whether the robustness claim is supported, including the nominal-performance loss, not only the upside.
* Check that "inner/outer approximation" is used in its committed mathematical sense, not loosely.
* Route: REVISE_METHOD (→ Stage 2) if the framework is unsound; REVISE_CODE or MORE_TESTING (→ Stage 3) otherwise; ACCEPTED → Stage 6.
* If H1 is not supported, say so plainly. A falsified hypothesis is a valid result.

### Stage 6 — Academic Writer → Humanized academic prose
* Write only what the experiments support. No overclaiming robustness.
* Match the manuscript's existing register and notation; flag any notation inconsistencies with the existing article.

## 4. Experimental requirements

* Compare, on every existing solution approach:
  (i) layout optimized on observed orders (nominal baseline),
  (ii) layout optimized on the enlarged/covering instance.
* Evaluate both on: (a) observed orders (nominal cost — expect (ii) to be worse), and (b) perturbed/future-order distributions from §2.4 (robustness — H1 predicts (ii) better).
* Report the tradeoff curve, not a single number. Robustness with no nominal cost is implausible; if observed, suspect a leak or a bug.

## 5. Standing constraints for all stages

* Prioritize truth over confirmation. Flag weak reasoning, unsupported steps, and any place the result depends on an unverified assumption.
* Never fabricate citations, statistics, or results.
* State uncertainty explicitly; mark unverified figures as such.
