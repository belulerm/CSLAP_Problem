# PLAN.md — Unbiased validation of the P–K covering robustness pre-process (CPLEX phase)

**Status:** the first end-to-end run is COMPLETE and ACCEPTED as a *conditional / partial* result.
This plan defines the next phase: re-test the hypothesis on an **exact solver (CPLEX)** and on
**clean, well-distributed data (`ISCF Data/`)** to remove the biases that made the first result
only conditional. New machine has a working CPLEX runtime; use it.

> Read first, in order: `reports/0_research_brief.md` (the hypothesis and rules),
> `reports/2_method_report.md` (the formulation, eqs. 1–13, Prop. 1/2),
> `reports/5_scientific_report_iter2.md` (the ACCEPTED verdict + the exact limitations to close),
> `reports/3_coder_log.md` (what actually ran the first time and how),
> then this file.

---

## 0. The hypothesis (unchanged)

**H1.** A layout optimized on a covering-**enlarged** demand object (each order replaced by its
pattern-closure) is more robust to future order-distribution shift than a layout optimized on the
raw observed orders, at a bounded nominal-cost price. H1 is tested, never assumed. A falsified or
partial H1 is a valid result. See `reports/0_research_brief.md`.

The construction = a data-driven **outer approximation** of the observed demand; optimizing on it is
*exactly* a robust counterpart of CSLAP (Prop. 1, `reports/2_method_report.md`). κ is the
conservatism knob (κ=1 → identity → the direct/nominal method; larger κ → bigger closures → more
conservative).

---

## 1. What changed since the first run — READ BEFORE CODING

1. **Synthetic Zhang datasets are GONE.** Do **not** use `synthetic_datasets/` or
   `Data_Generators/synthetic_data_zhang.py` for testing. The Zhang shift family is retired as the
   test infrastructure (it confounded "shift" with "regeneration noise").
2. **New PRIMARY test infrastructure = `ISCF Data/`** (clean, well-distributed; see §2). All
   small/medium controlled tests run here now.
3. **Industrial validation = BERNER** order lines (still used; see §2). Rebuild its instances from raw
   (the previously generated `berner_10w3w_*` files lived in the deleted `synthetic_datasets/`).
4. **Exact solver available = CPLEX (`docplex`).** Use it for BOTH the cover construction and the
   placement MILP. This is the single biggest change: the first run had no exact solver
   (`gurobipy` absent, fell back to HiGHS), which caused most of the biases below.

---

## 2. The data

### 2.1 `ISCF Data/` (new primary)
- `Products_data_ISCF.csv` (comma-separated, 997,198 order-lines): columns
  `,ID_Product,Product_FREQUENCY,Average_Volume/Day,ORDER_ID,Volume_Product,Number_Lines`.
  Each row is one (order, product) line. **Orders = group by `ORDER_ID`** → the set of `ID_Product`.
  - 4,328 distinct products; 418,849 distinct orders; mean order size 2.38 (min 1, max 132).
  - `Product_FREQUENCY` and `Volume_Product` are **per-product, fixed** (do not depend on κ).
- `Location_data_ISCF.csv` (4,328 locations): columns `,CODE_BARRE,COUT_EMPL,ID_GARE,Volume_Location`.
  - 8 stations (`ID_GARE` = GARE4..GARE11), **541 locations each** (8×541 = 4,328 = #products).
  - Capacity sums exactly to |P|: a balanced, uniform layout — this is the "well-distributed" input.
  - `COUT_EMPL` = location cost; `Volume_Location` = location capacity.

**Why ISCF removes a confound (important).** In the BERNER run, station time-capacity was a
*frequency-based workload* that the transform **recomputed from the enlarged orders**, so enlargement
inflated it (the "recalibration side-channel", limitation (c)). On ISCF, capacity is **slot count
(541) and/or product volume**, both **independent of κ** (a product's volume and its slot are fixed;
enlargement only reshapes the visit objective, not the capacity). Keep it that way: if a workload
constraint is used at all, compute it from the **real per-product** `Product_FREQUENCY`/volume,
**never** from closure line counts. This makes the κ=1 vs κ≥2 comparison clean by construction.

### 2.2 BERNER (industrial validation)
- Raw: `Different_Solution_Approaches/Full_Package_Code_With_All_Approaches/CSLAP-Synthetic/Heuristic_Connex_Set_Project/data/BERNER_ORDER_LINES_09-12.csv`
  (`PRODUCT;ORDER;QTY;STATION`, ~1.67M lines, 21,316 SKUs).
- Rebuild train/test instances from raw with `Baselines/build_berner_instance.py` (temporal
  early/late split by `ORDER_ID` rank; no date column → documented assumption U1). Use **multiple
  cuts** this time (e.g. 10w/3w, 8w/5w, and at least one more) to attach dispersion.

---

## 3. Biases in the first run to eliminate (the gap list) — each with its fix

| # | Bias / gap (first run) | Fix in this phase |
|---|---|---|
| G1 | No exact solver; HiGHS fell back, weak on the integer master. | Use **CPLEX** for the cover and the placement MILP. |
| G2 | Cover ran on a **subsampled** support set → reported Π (34) ≠ true Π (369); Prop. 2 bound only conditional; acceptance Π*=6 never reproduced. | Run the **full** cover (no subsample) and **certify Π_true**. Reproduce the **Π*=6 acceptance test** on `filtered_dataset.csv`. |
| G3 | Metaheuristic suboptimality produced a "benign free lunch" (robust layout cheaper on train too). | Exact MILP makes the price-of-robustness inequality **hold at optimality** (PoR ≥ 0). Any negative PoR with exact solver is then a real signal, not solver noise. |
| G4 | T_s recalibration side-channel confounded PoR/G. | Use **κ-invariant capacity** (slot/volume; workload from real per-product frequency). Confound removed by construction. Keep a recalibration-only control arm **only if** a workload cap is used. |
| G5 | Single train seed (synthetic) / single temporal cell (BERNER) → no CIs. | **Repeated K-fold random train/test splits** on ISCF (→ confidence intervals) + **multiple temporal cuts** on BERNER. |
| G6 | Workload feasibility not guaranteed; heuristic overloaded station 1 ~16×, and κ=2 worsened the peak. The BERNER win was visits-only. | Exact MILP **enforces** capacity (and any workload constraint), so layouts are feasible by construction. Report the **per-station** feasibility check for both arms regardless. |
| G7 | (Already correct, keep.) Count discipline. | Optimize on **enlarged** orders; **count visits on REAL orders**; score nominal and robust layouts on the **same** real held-out orders. The closures never enter any reported count. |

---

## 4. The unbiased experimental protocol

**Objective (unchanged):** minimize total station visits, $\sum_o |\{a(p):p\in P_o\}|$, per the
manuscript model (objective + capacity constraints). Counting is always on **real** orders.

**Comparison (apples-to-apples):** for each train/test split,
- $a_0$ = layout optimized on the **raw training orders** (κ=1, the direct method),
- $a_\kappa$ = layout optimized on the **enlarged training orders** (κ ≥ 2),
- both solved by **exact CPLEX** under an identical time budget,
- both scored on the **same real held-out orders**.
Then $\mathrm{PoR}(\kappa)$ and $G(\kappa)$ (eq. 13). Headline output = the **tradeoff curve**
$\{(\mathrm{PoR},G)\}$ indexed by realized enlargement $\bar c$, with **mean ± 95% CI across folds**.

**Uncertainty / out-of-sample model (replaces the Zhang generator):**
1. **Repeated random K-fold on orders** (primary): partition the ~419k ISCF orders into K folds
   (e.g. K=5 or 10), repeated R times with different seeds. Train on the in-fold orders, test on the
   held-out fold. This gives a clean, assumption-free generalization test **with dispersion** and no
   synthetic shift generator. Folds = the replication that fixes G5.
2. **Order-ID-rank temporal split** (secondary realism check): rank by `ORDER_ID`, train early / test
   late. Label the time-monotonicity as an assumption (no date column). Mirrors the BERNER protocol.
3. **(Optional) explicit perturbation** only if a referee wants a controlled shift: resample the order
   stream by reweighting product popularity; keep it documented and secondary. Do **not** reintroduce
   the Zhang generator.

**κ grid:** {1, 2, 3, 4, …} swept until enlargement saturates, to actually map the tradeoff curve and
test the predicted interior optimum (the first run could not — it had only one genuine κ). Stamp the
**realized** enlargement $\bar c = \text{mean}|\bar P_o|/\text{mean}|P_o|$ and a degeneracy flag per arm.

**Statistics:** paired design (same test fold for both arms); Wilcoxon signed-rank on paired
differences; mean ± 95% CI and effect sizes across folds; never report a single number.

**Pre-registered falsification (state before running):** H1 is **not supported** if $G \le 0$ across
folds for all κ>1. With an exact solver, expect $\mathrm{PoR} \ge 0$ always; a $G>0$ with
$\mathrm{PoR} \le 0$ now would be a real anomaly to investigate (leak/bug), not solver noise.

---

## 5. Step-by-step tasks for the agent

**Phase A — environment + adapter.**
- Confirm `import docplex` and a working CPLEX solve (trivial 2-var model). Log it.
- Write `Baselines/iscf_adapter.py`: read `ISCF Data/*.csv`, emit a standard CSLAP instance
  (orders grouped by `ORDER_ID`; universe = `ID_Product`; 8 stations from `ID_GARE`, 541 slots each;
  capacity = slots primary, product volume secondary). Drop nothing silently; log sizes. Keep the
  existing semicolon-CSV schema so the downstream code reads it unchanged.

**Phase B — exact cover (CPLEX).**
- Add `--backend cplex` to `Baselines/pk_cover_construction.py` using `docplex` (the original P–K
  notebooks were docplex/CPLEX; duals via the LP solution). Mirror the existing HiGHS backend API.
- Validate: reproduce **Π*=6** at k=6 on `…/P-K Set Cover/p-k-set-cover/filtered_dataset.csv`
  (the notebook's known result). This is the acceptance test the HiGHS run failed.
- Run the **full** cover on ISCF (no `--cover-max-supports` subsample) and on BERNER; record
  **Π_true** and assert partition validity (use `check_partition_and_pi`).

**Phase C — clean instance transform.**
- Use `Baselines/pk_instance_robust.py` to build the enlarged instances. **Disable / bypass the
  frequency-based TIME_CAPACITY recalibration** for ISCF (capacity is κ-invariant here); if any
  workload cap is kept, base it on real per-product frequency only. Verify κ=1 reproduces the raw
  instance exactly (identity self-test).

**Phase D — fold harness + exact placement.**
- Write a CPLEX placement MILP `Baselines/milp_cplex.py` (port of `milp_gurobi_synthetic.py` to
  docplex; same standard return tuple, same constraints incl. capacity). For tractability: drop
  size-1 orders from the optimization (each is a constant 1 visit), and **aggregate orders by distinct
  support with multiplicity weights**.
- Extend / replace `Baselines/run_robustness_experiment.py` to: build K-fold splits on ISCF, run
  $a_0$ and $a_\kappa$ with the exact solver under equal budgets, persist layouts, and enforce the
  no-leakage assertions (construction + solve see TRAIN only; test only in the evaluator).

**Phase E — metrics + feasibility.**
- `evaluate_layout_robust.py` (eq. 11) scores on **real** held-out orders. Compute PoR, G, oracle
  relative-regret, and the **per-station** slot/volume(/workload) feasibility for both arms (the
  station-1 overload check from the BERNER analysis — now expected clean under the exact solver).
- Aggregate across folds: mean ± 95% CI, paired Wilcoxon, tradeoff curve in $\bar c$.

**Phase F — industrial validation (BERNER).**
- Rebuild BERNER instances (multiple temporal cuts) with `build_berner_instance.py`. Run the same
  exact cover + exact (or, if 21k SKUs is too large for exact placement, the best available) solve.
  Report per-cut PoR/G with the per-station feasibility table.

**Phase G — write-up.**
- Re-run the pipeline's Scientific-Reviewer audit on the new exact results, then update
  `LaTeX_Articles_We_Have_Drafted/CSLAP_Robust_Covering_draft.tex` via the Academic-Writer
  (humanizer filter mandatory). Replace the conditional/limitation language with whatever the **exact,
  multi-fold** evidence now supports — upgrade or retract claims honestly. Update `reports/`.

---

## 6. Standing honesty rules (unchanged)

Prioritize truth over confirmation. Never fabricate citations, numbers, or results. Count on real
orders. Report dispersion (CIs), not single numbers. Report negative results as findings. State every
unverified assumption (e.g., BERNER temporal monotonicity). Pre-register the falsification criterion.
A clean negative result on ISCF is publishable and valuable.

---

## 7. Artifacts to produce this phase

- `Baselines/iscf_adapter.py`, `Baselines/milp_cplex.py`, `--backend cplex` in `pk_cover_construction.py`.
- Exact-cover logs with **Π_true** for ISCF and BERNER; the Π*=6 acceptance proof.
- `results_robustness_iscf_folds.csv` (per fold/arm/κ, with $\bar c$ + degeneracy flag), per-station
  feasibility tables, oracle-regret CSV.
- Updated `reports/` and a refreshed `CSLAP_Robust_Covering_draft.tex`.

## 8. File pointers

- Pipeline reports: `reports/0_…6_…md` (brief, SotA, method, coder log, code review, two science audits, writer report).
- Robustness modules: `Baselines/{pk_cover_construction,pk_instance_robust,evaluate_layout_robust,run_robustness_experiment,build_berner_instance}.py`.
- Reference P–K notebooks: `Different_Solution_Approaches/Topology_referal_from_another_problem/P-K Set Cover/p-k-set-cover/`.
- Draft paper: `LaTeX_Articles_We_Have_Drafted/CSLAP_Robust_Covering_draft.tex`.
- New data: `ISCF Data/` (primary) + BERNER raw (industrial).
- Agent pipeline protocol + standards: `.claude/rules/`.
