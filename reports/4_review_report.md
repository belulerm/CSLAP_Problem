# STAGE 4 — CODE REVIEW VERDICT

## VERDICT: **PASS** (with documented deviations accepted, two MAJOR science-not-code flags forwarded to Stage 5)

No CRITICAL defect found. No data leakage. Equations (2),(6)–(11),(13) are faithfully implemented. The k=1 identity and arm-comparability hold at the experiment level. The HiGHS-backend and U7a–c deviations are honestly documented and do not invalidate the reported (non-degenerate) rows.

---

## 1. Math-to-Code Compliance Matrix

| Eq | Object | Location | Verdict | Note |
|---|---|---|---|---|
| (1) | Û_k uncertainty set (implicit via Q\*,Π\*) | not materialized in code (conceptual) | PASS | Correctly left implicit; only generators Q(o),P̄_o are built. |
| (2) | Q(o), closure P̄_o | `pk_instance_robust.compute_closures` L147-168 | PASS | `if q & support: closure |= q` — exact union over hit patterns. |
| (6) | master min Π | `_solve_master_lp`/`_solve_master_integer` c[0]=1 | PASS | Π at var index 0, minimized. |
| (7) | cover =1 (exact) / ≥1 (cover) | `_build_master_matrices` L548-556; `_solve_master_integer` L661-664 | PASS | exact→equality `(rhs,rhs)`; cover→`(rhs,∞)`. LP variant uses vstack(-A_cover). |
| (8) | overlap ≤ Π over DISTINCT supports | `_build_master_matrices` L538-546; `A_sample` rows = `len(distinct_supports)` | PASS | Built over `distinct_supports` only; `-Pi + Σx ≤ 0`. |
| (9) | pricing (obj, 1≤Σz≤k, w_o≥z_p, ε=1e-6) | `_HighsPricing` L294-384; accept `>COLUMN_EPS` L809 | PASS | size row `1≤Σz≤k`; linking `w_o−z_p≥0`; binary; milp negates for max. β sign normalized. |
| (10) | T̄_s = ⌈1.10·(Σ L̄_p/V_s)/|S|⌉ | `transform_instance` L250-260 | PASS | `int(math.ceil(slack*load/n_stations))`, slack=1.10, V_s divisor, per-station loop. Verified pkk2 T_s=7906. |
| (11) | V(a,O^te) with dom(a) restrict + κ | `evaluate_layout` L83-155 | PASS | visits over `p in domain` only; κ=covered/total lines; unseen excluded + reported. |
| (12) | oracle regret RR | **ABSENT** | NOTE | Not implemented; not run in smoke. Method report listed it as a metric; coder did not wire an oracle arm. Acceptable for smoke; flag for full run. |
| (13) | PoR(k), G(k) | `run_experiment` L457-472 | PASS | Recomputed from eval CSV for 4 sampled rows — exact match. |
| (4) | Zhang orders-only shift | `zhang_shift_orders` L64-165 | PASS | Frozen universe/products/stations; orders regenerated; ρ-resampling of itemset pool. |

---

## 2. Findings (caveman-review, severity-tagged)

**[MAJOR — science, forward to Stage 5, NOT a code bug]**
- `run_robustness_experiment.py` L157 (RR/eq.12): oracle regret metric never implemented or run. Method Report E.1.3 specifies it. Full run should add a test-reoptimized oracle arm or Stage 5 must drop the metric explicitly.
- `pk_instance_robust` closure log: k=4 syn_50sku mean|closure|=9.06 < k=2's 15.52. Closure size is non-monotone in k (coarser partition → order hits fewer but larger patterns). Not a bug (consistent with Π\* decreasing in k, Method Report D), but it breaks the "bias monotone in k" narrative; Stage 5 must address.

**[MINOR]**
- `pk_instance_robust.transform_instance` L250-260: transformed L̄_p collapses within-order duplicate product rows (closure is a set). Original `read_data` counts duplicate rows: syn_50sku has 2461 duplicate (ORDER,PRODUCT) rows, so the **k=1 transform's** L_p (21162) ≠ original L_p (23623), and pkk1 T_s=4656 vs original 5198. **This is benign in the experiment** because the harness k=1 arm uses the ORIGINAL prefix (`train_instances[1]=instance`, L391-392), bypassing the transform — verified. But the self_test "identity" (L304) checks supports only, not L_p; the docstring claim "T=id at k=1" is true on supports, not on the full instance. Tighten the docstring wording.
- `run_experiment` L459/L463-464: PoR/G guards use truthiness (`if nk and base_nom`); a legitimate 0 would yield None. Visits never 0 in practice → harmless.
- `results_robustness_eval.csv` L2: orphan `syn_20sku_TRIVIAL`/`trivial` row from an ad-hoc test, not in the summary and not in any grid. Cosmetic; recommend pruning before the writer ingests the eval CSV.
- `_solve_master_integer` U7b fallback L676-695: emits WARN to stderr but does NOT stamp a `degenerate` flag into the output meta/CSV. Reported runs never triggered it (log: 0 U7b warnings, all Π\*>1), so no degenerate row leaked — but a future full run relying on CSV inspection alone could miss a silent degeneration. Recommend writing a `singleton_fallback` boolean into the transform meta.

**[INFO — verified clean]**
- Baseline files all mtime 2026-06-11 17:00:52, unmodified; Stage-3 files post-date. No baseline touched.
- GA/SA return 7-tuples; harness reads result[0]/[1] correctly; GA chromosome→dict at L329; SA state is dict. Adapter arity correct.
- Hexaly adapter kwargs (`time_limit`, `scenario_name`) match `run_milp_hexaly`/`column_generation_hexaly` signatures.
- Layout JSON = clean `{PROD_x:int}`, full 50-product domain.
- Pattern validity / Π independent recompute: `check_partition_and_pi` recomputes cover/Π from scratch (no solver trust).

---

## 3. Leakage Audit Outcome: **CLEAN — NO LEAKAGE**

Traced full data flow:
- Construction `obtain_cover`/`run_pk_cover` reads only `{train_prefix}_*` via `read_supports_from_instance`. Never touches test prefixes.
- Transform `transform_instance` reads only training CSVs; writes `{prefix}_pkk{k}_*`.
- Every solver arm runs on `train_instances[k]` (training-derived only). Nominal cost N(a_k) evaluated on the **original training orders** (`instance`, split=`nominal_train`), NOT on closures — verified L432-439.
- Test orders read exclusively by `evaluate_layout_robust` on `shift_test` cells.
- Seed disjointness asserted (`assert train_seed not in test_seeds`, L351) and logged ("LEAKAGE GUARD OK: train_seed=42 disjoint from [43,44,45,46,47]").
- Zhang shift wrapper freezes universe/products/stations (copied verbatim from training) and regenerates **orders only** — does not overwrite training files (distinct `_te_*` out_prefix). Verified.
- TIME_CAPACITY recalibration (eq.10) computed from L̄_p over training closures only — no test data.
- U7 subsample affects only the cover-driver support set fed to constraint (8); closures (eq.2) computed over ALL training orders (verified: pkk2 has all 2336 orders preserved). No leakage path.

---

## 4. Deviations U2 / U7a–c: **ACCEPTABLE AS DOCUMENTED**

- **U2 (Gurobi→HiGHS):** gurobipy import genuinely fails in env; HiGHS gives exact LP duals; formulation (6)–(9) preserved. Accepted. Consequence: acceptance test Π\*=6 not reproduced — honestly logged as a failure-to-reproduce, not a silent pass. Substitute validation (non-degenerate Π\*>1, mean closure > mean order size) is reasonable.
- **U7 (subsample):** fixed-seed (12345), applied to distinct supports only, closures over all orders. Documented and threaded through CLI. Accepted.
- **U7a (combo-column cap):** singletons + size-k chunks always kept → feasibility preserved; only initial pool bounded. Accepted.
- **U7b (singleton fallback):** correct (singleton partition always feasible); WARN emitted; **not triggered in any reported row** (0 warnings in log). Accepted, with the MINOR note that it should also stamp a CSV flag.
- **U7c (k=6 dropped):** justified (saturated/degenerate); no k=6 row in summary. Accepted.

---

## 5. Results Sanity: **PASS**

- PoR/G recomputed from eval CSV for syn_50sku{heuristic,ga,sa} and syn_500sku{ga} — exact match to stored summary (0 mismatch).
- Eval row counts consistent with grid: syn_50sku 3k×(1+45), syn_500sku 2k×(1+45), syn_20sku 2k×(1+4).
- No G>0 & PoR≈0 free-lunch anomaly in any k>1 row (every positive-G row carries a positive PoR; the few negative-PoR rows also have ≤0 or near-zero G).
- All reported transforms non-degenerate (Π\*∈{9,10,13,15}, mean|closure|>order size).

---

**Handoff:** Advance to **Stage 5 (Scientific Reviewer)**. The two MAJOR items (absent oracle/eq.12; non-monotone closure-vs-k) are science-design questions, not code defects, and are the Scientific Reviewer's domain. Recommend the coder (if a full run is later commissioned) add the eq.12 oracle arm, stamp a `singleton_fallback` flag into transform meta, prune the orphan `TRIVIAL` eval row, and tighten the k=1 "identity" docstring to "identity on supports."
