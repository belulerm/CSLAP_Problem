# Stage 3 — Optimization Coder Log (CSLAP robustness under order-distribution shift)

Pipeline stage: 3 (Optimization Coder). Contract: `reports/2_method_report.md` §F.
Brief: `reports/0_research_brief.md`. Hypothesis under test: **H1** — a layout
optimized on the P-K *enlarged/covering* instance (k>1) is more robust to future
order-distribution shift than the nominal (k=1) layout, at a bounded nominal-cost
price (the Price-of-Robustness tradeoff, eqs. (11)–(13)).

This log is **incremental**; it is appended/refreshed after every chunk.

---

## 1. Environment & license findings

| Component | Status | Note |
|---|---|---|
| Python | 3.9.13 (base) | harness + all Stage-3 scripts run here |
| numpy / pandas / scipy | 1.24.4 / 1.4.4 / 1.9.1 | `scipy.optimize.milp` (HiGHS) available |
| **Gurobi** (`gurobipy`) | **IMPORT FAILS** | not installed in this env → all Gurobi arms unrunnable (the 2000 var/constr restricted-license question is moot: the module itself does not import). `milp_gurobi_synthetic.py`, `cg_gurobi_synthetic.py` cannot run. |
| **Hexaly** | import OK (license valid) | usable for `milp_synthetic`/`cg_synthetic` if needed |
| docplex / CPLEX | not used | Method Report F.1 fallback path not taken |

### Construction backend that actually ran
Per `pk_cover_construction.py` header (lines 12–39) the **committed primary
Gurobi port could not be used** (no `gurobipy`). The construction therefore runs on
the documented backend **`highs`** (SciPy `linprog`/`milp`): master LP **and**
pricing MIP both solved with HiGHS, duals from HiGHS. This is **Deviation U2/U7a**
(Gurobi port → HiGHS), already labelled in the module docstring. The syn_20sku
pilot constructions also ran on `highs` (verified: harness default `--backend
highs`; `_import_runner` exposes only `heuristic|ga|sa|milp_hexaly|cg_hexaly` —
there is **no** `milp_gurobi`/`cg_gurobi` solver arm in the harness, consistent
with Gurobi being unavailable).

---

## 2. Files (Stage-3 deliverables, all under `…/CSLAP-Synthetic/Baselines/`)

| File | Role | Method Report ref |
|---|---|---|
| `pk_cover_construction.py` | construction operator C_k^var (CG master + pricing) | eqs. (6)–(9), §F.1 |
| `pk_instance_robust.py` | transform T: cover → enlarged instance `{prefix}_pkk{k}` | eqs. (2),(10), §F.2 |
| `evaluate_layout_robust.py` | fixed-layout evaluation functional (no solver dep) | eq. (11), C.5, §F.3 |
| `run_robustness_experiment.py` | harness: shift wrapper, runners, leakage guard, metrics | §F.4, eq. (13) |

### Formulation → code map
| Method Report equation | Code location |
|---|---|
| (2) cover/closure \bar P_o | `pk_instance_robust.compute_closures` |
| (6)–(9) C_k^var CG master+pricing | `pk_cover_construction.run_pk_cover`, `_HighsPricing`, `_solve_master_integer` |
| (10) recalibrated \bar T_s | `pk_instance_robust.transform_instance` (TIME_CAPACITY loop) |
| (11) V(a,O^te) visits | `evaluate_layout_robust.evaluate_layout` |
| (13) PoR(k), G(k) | `run_robustness_experiment.run_experiment` (aggregation block) |
| (4) Zhang orders-only shift | `run_robustness_experiment.zhang_shift_orders` |

---

## 3. Verification outcomes

| Check | Result |
|---|---|
| k=1 identity (`pk_instance_robust --self-test`, syn_50sku, highs) | **PASS** — \bar P_o = P_o for every order |
| Acceptance test Π*=6 at k=6 on `filtered_dataset.csv` (400 orders, ≤12) | **NOT REPRODUCED** — see §4.A below |
| Leakage guard (train_seed=42 ∉ test_seeds) | enforced in `run_experiment` (assert + log) |

---

## 4. Deviations & open issues

### A. Acceptance test (Π*=6) not reproduced — column explosion + integer-master timeout
Running C_6^exact on the notebook slice (400 orders, |P|=1124, 396 distinct):
the LP relaxation converged (88 CG iterations) to **relaxed Π = 3.34** with
**20 753 columns**, and the **binary integer master found no incumbent** within
180 s. Root causes:
1. The notebook obtained Π*=6 with **CPLEX**, which solves the large binary
   set-partition that HiGHS cannot within budget (Deviation U2 consequence).
2. Initial column seeding `_seed_initial_columns` step (c) enumerates all
   k-combinations of every distinct support → ~20k columns at k=6, making the
   integer phase intractable for HiGHS.
This is logged as a **failure to reproduce the published acceptance number under
the HiGHS backend**, not a silent pass. The construction is still *used* for the
smoke run via the U7 subsample (below), which keeps the column pool tractable and
yields **non-degenerate** multi-item patterns (validated: 50sku k=2, 150-support
subsample → Π*=10, 25 size-2 patterns, 21 s).

### B. Deviation U7 — fixed-seed subsample of distinct supports (scalability)
The full distinct-support counts are large (syn_50sku: 2236, syn_500sku: 16324).
At these sizes the integer master does not return an incumbent under HiGHS in any
practical budget. Per Method Report U7 (dedup mandatory, subsampling the
documented fallback), I added a **fixed-seed** (`seed=12345`) random subsample of
the **distinct** supports fed to the construction, exposed as
`--cover-max-supports` on the harness and threaded through
`obtain_cover`/`transform_instance`. Closures (eq. 2) are still computed over
**all** orders; only the cover-driver support set is capped. Dedup is applied
before subsampling.

### C. Deviation U7b — singleton-partition last-resort fallback
`_solve_master_integer` now, if HiGHS returns **no incumbent**, emits a `[WARN
U7b]` to stderr and returns the **singleton partition** (always feasible for the
exact/cover variants). This keeps the pipeline alive but is **degenerate**
(closures collapse to identity → k>1 == k=1). Any run that triggers this WARN is
flagged; the subsample cap is sized to avoid it.

### D. milp_gurobi / cg_gurobi arms — skipped (no Gurobi). milp_hexaly available
but on 50/500 sku the Hexaly MILP would need its own feasibility within budget;
attempted with catch+skip where requested.

---

## 5. Experiment grid actually run

Shared test grid for the synthetic instances (Method Report D, eq. 4):
**θ′ ∈ {0.5, 0.7, 0.9} × ρ ∈ {0.0, 0.5, 1.0} × seeds {43,44,45,46,47} = 45 shifted
test cells** per instance (train_seed = 42, disjoint — leakage guard logged OK).
Variant = `exact`. Construction backend = `highs`. U7 subsample
`--cover-max-supports 150` (fixed seed 12345). Metaheuristics run with `--quick`.

| Chunk | Instance | k grid run | Solvers run | Test cells | Construction notes |
|---|---|---|---|---|---|
| 1 | syn_50sku (2236 distinct, \|P\|=50) | **{1,2,4}** | heuristic, sa, ga | 45 | k=2 Π*=10 (10s); k=4 Π*=15 (≈5.5min). **k=6 DROPPED** — see U7c below. |
| 2 | syn_500sku (16324 distinct, \|P\|=500) | **{1,2}** | heuristic, sa, ga | 45 | k=2 Π*=10, mean\|closure\|=18.23 (≈55s incl. 8min cell-gen). **k=6 DROPPED** — singleton-degenerate (U7c). |
| pilot | syn_20sku (781 distinct, \|P\|=20) | {1,2} | heuristic, sa | 4 | prior pilot, retained in unified summary. |

**MILP arms skipped:** `milp_gurobi`/`cg_gurobi` — no `gurobipy` in env (not just license size). `milp_hexaly` not invoked in the smoke (Hexaly MILP at 50/500 sku would need its own feasibility within the 60s budget and the harness defaulted to the three robust pure-Python/HiGHS arms). Hexaly license is valid and the arm is wired in `_import_runner` for a later full run.

### Deviation U7c — k=6 dropped on both synthetic instances
* **syn_50sku k=6:** construction completes but Π*/mean-closure are **identical to
  k=4** (cover saturated: no size-5/6 pattern improves the partition under the
  150-support subsample), while wall-clock balloons (≈7.5 min standalone, and the
  harness's larger per-phase budget pushed a single k=6 build past 25 min). No new
  information, disproportionate cost → dropped; k=4 retained as the high-k arm.
* **syn_500sku k=6:** the integer master found **no incumbent** in budget over
  50 741 columns and triggered the **U7b singleton fallback** (DEGENERATE,
  closures collapse to identity). A degenerate k=6 row would be scientifically
  void, so k=6 is dropped; k=2 (Π*=10, 285 genuine multi-item patterns,
  mean closure 18.23 > 10) is the robust arm.
* **Second-instance substitution clause:** the brief allowed substituting
  syn_30sku FULL if 500sku proved impossible. 500sku k∈{1,2} **was** feasible and
  non-degenerate, so **no substitution was needed**; 500sku is reported.

---

## 6. Headline results (eq. 13: PoR(k), G(k) vs k=1)

PoR(k) = (N(a_k) − N(a_0)) / N(a_0)  (nominal-cost price; higher = worse nominal).
G(k)   = (V_te(a_0) − V_te(a_k)) / V_te(a_0)  (test-shift gain; **positive = H1 supported**).

### syn_50sku (45 test cells)
| solver | N(k=1) | N(best k) | V_te(k=1) | V_te(best k) | PoR(k) | G(k) | best k |
|---|---|---|---|---|---|---|---|
| heuristic | 9178 | 9261 | 9333.7 | 9281.9 | **+0.90%** | **+0.56%** | 2 |
| sa        | 9594 | 9622 | 9319.6 | 9245.6 | **+0.29%** | **+0.79%** | 2 |
| ga        | 9941 | 10051 | 9318.0 | 9182.6 | **+1.11%** | **+1.45%** | 2 |
| heuristic | 9178 | 8888 | 9333.7 | 9361.4 | −3.16% | −0.30% | 4 |
| sa        | 9594 | 9656 | 9319.6 | 9322.8 | +0.65% | −0.03% | 4 |
| ga        | 9941 | 9899 | 9318.0 | 9269.3 | −0.42% | +0.52% | 4 |

### syn_500sku (45 test cells)
| solver | N(k=1) | N(k=2) | V_te(k=1) | V_te(k=2) | PoR(2) | G(2) |
|---|---|---|---|---|---|---|
| heuristic | 62511 | 63741 | 86661.9 | 86681.9 | +1.97% | −0.02% |
| sa        | 71247 | 71065 | 86612.8 | 86768.4 | −0.26% | −0.18% |
| ga        | 70775 | 71035 | 86767.1 | 86568.5 | +0.37% | **+0.23%** |

### syn_20sku (pilot, 4 test cells)
| solver | PoR(2) | G(2) |
|---|---|---|
| heuristic | +1.46% | −0.05% |
| sa        | +1.48% | **+1.45%** |

---

## 7. Verification & consistency (final)

* **k=1 identity:** PASS (self-test, syn_50sku).
* **Acceptance Π*=6:** NOT reproduced under HiGHS (relaxed Π=3.34, integer master
  timed out) — logged §4.A; substitute validation = non-degenerate cover at k=2/k=4
  with Π* > 1 and mean closure > mean order size.
* **Leakage guard:** train_seed=42 ∉ {43..47}, asserted + logged each run.
* **Unified summary consistency:** 19 rows; **0** rows missing nominal/test;
  eq.(13) recomputed from (N, V_te) matches stored PoR/G exactly (0 mismatches).
* **Leak flag (brief §4):** **0** rows with G>0 AND PoR≈0 at k>1 — no
  "free-lunch robustness" signatures.

## 8. Result files

* `Baselines/results_robustness_summary.csv` — unified (20+50+500 sku, 19 rows).
* `Baselines/results_robustness_syn_{20,50,500}sku.csv` — per-instance.
* `Baselines/results_robustness_eval.csv` — per-(layout,test-cell) rows (≈436).
* `Baselines/layouts/syn_{50,500}sku_{heuristic,sa,ga}_k{...}_exact.json` — layouts.
* `Baselines/logs/robustness_harness.log` — full run log.
* Transformed instances: `synthetic_datasets/syn_{50,500}sku_pkk{k}_*.csv`.

## 9. Headline verdict for Stage 5

**Does H1 look supported in this smoke data? Weakly/conditionally YES at k=2,
not at higher k.** The cleanest, most consistent H1 signature is at **k=2**: on
syn_50sku all three solvers show small positive PoR (+0.3…+1.1%) bought with a
positive test-shift gain G (+0.6…+1.5%) — the expected Price-of-Robustness
tradeoff. The effect is solver- and scale-dependent and **small relative to the
seed-to-seed test variance**: at 500sku only GA shows a positive G(2) (+0.23%),
heuristic/sa are flat-to-negative; at k=4 (50sku) the cover over-enlarges and the
gain vanishes or reverses. **No statistical significance has been established**
(Stage 5's job): the 45-cell means are reported without dispersion/CIs here, and
the magnitudes are sub-percent. Recommended for Stage 5: paired per-cell tests
(layouts share test cells), report the full PoR–G tradeoff curve, and treat k=2 as
the operative arm; flag the high-k saturation and the HiGHS construction ceiling
(U2/U7) as the principal threats to a stronger claim.

---

# Iteration 2 (Stage-3 re-entry after Scientific-Reviewer feedback)

Scope of this iteration: (T1) 3-seed replication of the synthetic robustness run;
(T2) **k=3 substitution** for the saturated/degenerate k=4 arm; (T3) oracle
regret-ratio (RR) normalizer (eq. 12); (T4) construction guards (`c_bar`,
degenerate-column flag); and the new **industrial arm on the BERNER order lines**
(T5) plus this log update (T6). All runs foreground, chunked. Construction backend
remained **`highs`** (no Gurobi); §1/§4 of Iteration 1 still apply.

## 10. Synthetic re-run (T1–T4) — what changed

### 10.1 k=3 substitution for the saturated k=4 (T2)
Iteration 1 used k∈{1,2,4} on syn_50sku, but the **k=4 arm is DEGENERATE**: under
the U7 subsample the cover saturates and the closures collapse to the identity
(`c_bar = 1.0`, `frac_strict = 0.0`), so k=4 == k=1 and the row is scientifically
void (it is retained in the eval CSV/log but **excluded from the summary**, per the
reviewer-item-1 rule in `run_experiment`). It is **replaced by k=3**, which is
genuinely non-degenerate on every seed (`c_bar ≈ 2.18–2.23`, `frac_strict ≈
1.00`). The synthetic k-grid this iteration is therefore **{1, 2, 3}** (+ the `1T`
T_s-side-channel control on the seed-42 instance).

### 10.2 Three-seed replication (T1) and the G sign-flip
syn_50sku was rebuilt and re-run on **train seeds 42 / 142 / 242** (instances
`syn_50sku`, `syn_50sku_s142`, `syn_50sku_s242`; each 45 test cells, leakage guard
OK). The headline robustness gain **G(k) is not sign-stable across train seeds** —
the central negative result of this iteration:

| solver | k | G(s42) | G(s142) | G(s242) | sign pattern |
|---|---|---|---|---|---|
| heuristic | 2 | **+0.0063** | **−0.0061** | **+0.0034** | + / − / + |
| heuristic | 3 | +0.0008 | −0.0035 | +0.0012 | + / − / + |
| sa | 2 | −0.0031 | −0.0088 | +0.0009 | − / − / + |
| sa | 3 | −0.0091 | +0.0013 | +0.0051 | − / + / + |
| ga | 2 | +0.0069 | +0.0000 | +0.0023 | + / 0 / + |
| ga | 3 | +0.0066 | −0.0063 | −0.0075 | + / − / − |

PoR(k) is consistently **positive** (nominal cost rises with k: heuristic k=2 PoR
ranges +0.16% … +6.96% across seeds; k=3 +3.02% … +6.45%) — the Price-of-Robustness
is real and monotone, but the **test-side payoff G is sub-percent and flips sign
with the training seed**. No single (solver, k) cell is positive on all three
seeds. This directly tempers the Iteration-1 "weak YES at k=2" reading.

### 10.3 Oracle regret ratio (T3, eq. 12)
`results_oracle_rr.csv`: RR = (V_te(layout) − V_te(oracle)) / V_te(oracle), where the
**oracle is the test-reoptimized layout** (test data seen *by design* only as the
normalizer, never to build the evaluated layout). Probed at two corner cells
(θ′=0.7, ρ∈{0.0,1.0}, seed 43):

| solver | cell (θ′,ρ) | RR(k=1) | RR(k=2) | k=2 beats k=1? |
|---|---|---|---|---|
| heuristic | 0.7, 0.0 | 0.1053 | 0.1282 | no (worse) |
| heuristic | 0.7, 1.0 | 0.2420 | 0.2063 | **yes** |
| sa | 0.7, 0.0 | 0.0411 | 0.0359 | **yes** |
| sa | 0.7, 1.0 | 0.0987 | 0.0769 | **yes** |
| ga | 0.7, 0.0 | −0.0311 | 0.0013 | no (worse) |
| ga | 0.7, 1.0 | 0.0924 | 0.1163 | no (worse) |

Regret to the oracle is **modest (4–24%)** and k=2's advantage is **cell- and
solver-dependent** — consistent with the small, unstable G above. (Only the
ρ-shift cells reoptimize meaningfully; this is a 2-cell probe, not the full grid.)

### 10.4 Construction guards (T4)
`pk_instance_robust.transform_instance` now records and the harness logs, per arm:
`c_bar = mean|closure|/mean|support|`, `frac_strict_growth`, a boolean
**`degenerate`** (`k>1 and frac_strict < 0.05`), and `max_closure_size`. The
summary CSV carries `c_bar`/`degenerate` columns; degenerate arms are dropped from
the summary. The U7b singleton-fallback path additionally emits `[WARN U7b]` to
stderr (degenerate-column flag).

---

## 11. BERNER industrial arm (T5)

### 11.1 Split mechanics + assumption U1
`build_berner_instance.py` builds a **train-early / test-late temporal split** of
`BERNER_ORDER_LINES_09-12.csv` (schema `PRODUCT;ORDER;QTY;STATION`) into the
standard semicolon CSLAP schema. The file has **no date column**, so the
manuscript's 13-week temporal split is reproduced by **assumption U1**: order ids
are numeric and monotone in time (verified end-points 8076384032 → 8076739874), so
ranking by order id and cutting at the 10/13 quantile yields the early-train /
late-test split. Train/test order-id sets are **asserted disjoint**; the test
window contributes **orders only** (products and stations are frozen from the train
window — no leakage). Unseen test SKUs are expected and surface as coverage κ < 1.

Realised `berner_10w3w` sizes: **train 219,121 orders / 1,220,907 lines / 21,316
SKUs**; **test 65,737 orders / 353,999 lines**; both share **25 stations**,
sum CAPACITY 24,528, sum TIME_CAPACITY 31,504.

### 11.2 Station configuration source
Replicated from the repo's own `data_loader_industrial.py`, computed **on the
training window only**: drop stations `01.Z8/01.15/01.GED`+blank, merge
`01.GE4→01.E4`; each product pinned to the station of its latest train order; speed
tiers STATIC 37700 (`01.E4/01.31/01.30`), PALETTE 57200 (`01.01..05`), DYNAMIC
83200 (rest), per-station SPEED = tier / #distinct-products; CAPACITY = #distinct
products × **1.15 documented slack** (so the placement problem is feasible for the
metaheuristics — the loader's tight caps sum to exactly |P_train|); TIME_CAPACITY =
Σ freq/SPEED × 1.15. Physical ids mapped to integer `STATION_ID` 1..25.

### 11.3 Cover stats and the **Π reconciliation (T5a — correctness flag)**
The pre-built covers (`Baselines/covers/cover_berner_10w3w_train_k{2,3}.json`,
`variant=exact`, backend `highs`) carry a stored `pi_star` (k2 = 34, k3 = 23). The
k2 transform meta reported `max_closure_size = 429`, which is **impossible** if the
covering constraint (8) bound *all* distinct supports: each pattern has ≤ k
elements, so a closure can be at most `Π*·k = 68` at k=2. Recomputing from scratch
(`pk_cover_construction.check_partition_and_pi` over the **full** 142,241 distinct
train supports, script `c:\tmp\t5a_reconcile.py`):

| arm | partition valid? | stored `pi_star` | **Π_true (full stream)** | Π_true·k | max\|closure\| |
|---|---|---|---|---|---|
| k=2 | **YES** (0 uncovered, 0 overcovered, max pattern size 2) | 34 | **369** | 738 | 429 |
| k=3 | **YES** (0 uncovered, 0 overcovered, max pattern size 3) | 23 | **360** | 1080 | 464 |

**Mechanism (documented from the code path):** when a pre-built cover JSON is
loaded, `pk_instance_robust.obtain_cover` reads `pi_star` *verbatim from the JSON*
(it does not recompute it), while the closures (eq. 2) — and hence `max_closure` —
are computed over the **full** training order stream. The stored `pi_star` was
produced during the cover **construction**, where the CG master saw only a
**capped/subsampled support set** (the same U7 `--cover-max-supports` mechanism the
synthetics used at `sub=350`/`sub=150`, confirmed in `logs/robustness_harness.log`).
Thus the stored value binds only that subset: **2,100 distinct supports are hit by
> 34 patterns**, violating `pi_star = 34` as a global bottleneck. The argmax
support (387 SKUs) is hit by 369 patterns whose union is 429 items — internally
consistent.

**Resolution:** `pi_star` is **relabeled `pi_constrained`** (it binds only the
subsampled construction support set); the true bottleneck on the full train stream
is **Π_true = 369 (k=2) / 360 (k=3)**. Both meta JSONs were patched with
`pi_constrained`, `pi_true_full_stream`, `partition_valid=true`, and a note. **The
partition itself is valid (disjoint + covers the universe) on the full stream, so
BERNER k=2/k=3 proceed.** This is a *reporting* correction, not a feasibility
defect: the transform's closures were always computed correctly over all orders.

### 11.4 Transform stats (T5b)
| arm | c_bar | frac_strict | degenerate | mean\|sup\| → mean\|clo\| | T_s (st.1) | new T_s |
|---|---|---|---|---|---|---|
| pkk2 | 1.330 | 0.612 | False | 5.29 → 7.03 | 495 | 1321 |
| pkk3 | 1.569 | 0.598 | False | 5.29 → 8.30 | 495 | 1558 |

Both arms are **non-degenerate**; the k=3 transform reused the pre-built k=3 cover
and produced `berner_10w3w_train_pkk3_*` (script `c:\tmp\t5b_k3_transform.py`).

### 11.5 Solver runs (T5c) and the scalability walls
Solvers invoked through the unchanged harness adapter
`run_robustness_experiment.run_solver` (per-baseline signatures; GA global RNG
seeded `20240612` immediately before each GA call — identical to the synthetic
runs), `--time 120`, non-`quick`, layouts persisted to `Baselines/layouts/`.
`run_benchmarks_industrial.py` / `run_metaheuristics_industrial_alone.py` were
skimmed first: they set **no solver-specific knob overrides** (population /
iteration / neighborhood are the solver defaults, driven only by `time_limit`,
`quick`, and an optional warm start) — so reusing the standard `--time 120` /
default-knob configuration is faithful and identical across arms.

| solver | arm | status | train visits N | wall | note |
|---|---|---|---|---|---|
| heuristic | train | OK | 578,111 | 32 s | greedy clustering, deterministic |
| heuristic | pkk2 | OK | 597,776 | 44 s | |
| heuristic | pkk3 | OK | 586,900 | 53 s | |
| sa | train | OK | 578,337 | **1,219 s** | ~1 cooling step only (see wall below) |
| sa | pkk2/pkk3 | **SKIP** | — | — | each > 20 min, over budget |
| ga | train | OK | 757,771 | 214 s | reaches only generation 2 |
| ga | pkk2 | OK | 912,442 | 351 s | generation 2 |
| ga | pkk3 | OK | 1,010,192 | 333 s | generation 2 |

**SA scalability wall (quantified, `c:\tmp\probe_cooc.py`):** SA's
`calculate_objective` costs **1.14 s per call** at this scale (it iterates all
219,121 orders for the visit count *and* all 4.5 M co-occurrence pairs for the
dispersion term, every call). With `inner_iters = min(N·2, 1000) = 1000`, **one
temperature step ≈ 19 min**; the 120 s budget admits only **~105 objective calls
(< 1 cooling step)**. The cost is per-call, so the "halve the knob once" rule
(inner 1000→500 ⇒ still ~9.5 min/step) **cannot** rescue it. The nominal-arm SA run
*did* complete (one accidental long background run, 1,219 s, ~1 cooling step) and
its layout is kept; **pkk2/pkk3 SA are skipped** because each would be another
20 min+ run and a 1-step SA carries no metaheuristic signal. (Heuristic — which is
mandatory — completed on all three arms.)

**GA degeneracy at industrial scale (honest negative finding):** GA's
`random_feasible` uses an internal `RandomState(42)` and ignores the order
closures; with `--time 120` GA reaches only **generation 2**, so the returned best
is essentially the seed-42 initial random-feasible chromosome. Because all three
arms share the **same universe and station set** (only T_s differs), GA returns a
**byte-identical layout on all three arms** (md5 `8ea2c967f423`, verified). GA
therefore shows **no arm differentiation** (PoR = G = 0 for k=2,3) — it is not
exercising the transform at this scale. The heuristic, by contrast, consumes the
closures and produces **three distinct layouts** (distinct md5s), so it is the only
solver carrying an H1 signal on BERNER.

### 11.6 Evaluation (T5d, eq. 11) and BERNER headline
Each layout evaluated on the **original train** instance (nominal cost N, true
stations) and on the **single real `berner_10w3w_test` cell** (V_te, κ — the test
station file is the frozen-from-train file, i.e. the **true** train capacities).
**n_test_cells = 1** (one real temporal cell; no Zhang shift, **no CI possible** —
documented). Coverage **κ = 0.9891 on every layout** (3,844 unseen test pick-lines
out of 353,999 — unseen SKUs excluded from eq. 11 identically for all layouts, as
designed). cap_broken = 0, wl_broken = 1 (one station over T_s) on every layout —
identical across arms, so it does not confound the comparison.

| solver | k | N (train) | V_te (test) | PoR(k) | G(k) | κ |
|---|---|---|---|---|---|---|
| heuristic | 1 | 578,111 | 164,140 | 0.0 | 0.0 | 0.9891 |
| heuristic | 2 | 572,765 | 163,607 | **−0.92%** | **+0.32%** | 0.9891 |
| heuristic | 3 | 563,947 | 160,888 | **−2.45%** | **+1.98%** | 0.9891 |
| sa | 1 | 578,337 | 166,712 | 0.0 | 0.0 | 0.9891 |
| ga | 1 | 757,771 | 214,899 | 0.0 | 0.0 | 0.9891 |
| ga | 2 | 757,771 | 214,899 | 0.0 (identical layout) | 0.0 | 0.9891 |
| ga | 3 | 757,771 | 214,899 | 0.0 (identical layout) | 0.0 | 0.9891 |

For the **heuristic** (the only differentiating solver), H1 holds **cleanly and
monotonically**: the robust transform **lowers nominal cost** (PoR negative,
−0.92% → −2.45%) **and** lowers test visits (G positive, +0.32% → +1.98%), both
strengthening with k. This is a Pareto improvement, not a Price-of-Robustness
tradeoff — at industrial scale the enlarged covering layout dominates the nominal
one on both train and (single-cell) test. The single-cell caveat is important: this
is one real test window, so there is no dispersion estimate, and Stage 5 cannot
attach a CI to the BERNER G.

### 11.7 8w5w split (T5e) — skipped cleanly
The 8w5w arm requires a **fresh industrial cover construction** from scratch (no
8w5w cover is pre-built; only 10w3w covers exist). The industrial CG master is the
single most expensive, least-bounded operation in the pipeline (cf. the synthetic
k=6 builds that blew 25 min and the U7b fallbacks). With T5's budget already heavily
consumed (the accidental 20-min SA run, three multi-minute GA arms) and the 10w3w
arm already delivering an unambiguous industrial H1 verdict, **T5e is skipped**
per the brief's "skip cleanly if tight." No 8w5w rows are emitted.

---

## 12. Iteration-2 deviations & open issues

* **U8 — `pi_star` mislabel in pre-built BERNER covers (resolved/reported, §11.3).**
  The stored `pi_star` is the *constrained* bottleneck on the subsampled
  construction support set, not the global Π. Relabeled `pi_constrained`; true
  Π_true (369 / 360) recomputed and written to the meta JSONs. Partition validity
  re-asserted on the full stream (valid). No feasibility impact.
* **U9 — SA does not scale to industrial size (skipped on 2/3 BERNER arms, §11.5).**
  Root cause is the O(orders) + O(cooc-pairs) per-objective-call cost, invariant to
  iteration knobs; knob-halving cannot fix it. Heuristic (mandatory) completed.
* **U10 — GA degenerates to seeded random-feasible at industrial scale (§11.5).**
  Only ~2 generations in 120 s; identical layout across arms ⇒ GA contributes no
  BERNER robustness signal. Reported honestly rather than dropped.
* **Single-cell BERNER test (n_test_cells = 1).** One real late window ⇒ no CI; the
  synthetic arms remain the only source of multi-cell dispersion (and there G is
  sign-unstable, §10.2).
* **GA seed note.** The brief named `seed(42)`; the reproducible mechanism actually
  used (matching the synthetic runs) is the harness `GA_GLOBAL_SEED = 20240612`
  applied to the global RNG before each GA call. The GA's *internal* RNG is fixed at
  42 inside `ga_baseline.py`; both are deterministic and identical across arms.

## 13. Iteration-2 result files & build→row provenance

* `Baselines/results_robustness_summary.csv` — now includes **7 BERNER rows**
  (`instance=berner_10w3w`, k∈{1,2,3}) alongside the refreshed 3-seed synthetics.
* `Baselines/results_robustness_eval.csv` — +14 BERNER eval rows (7 layouts ×
  {nominal_train, shift_test}).
* `Baselines/results_oracle_rr.csv` — oracle RR probe (T3).
* `Baselines/berner_t5c_solver_runs.csv` — T5c solver-run trace (status, visits,
  wall, SKIP reasons).
* `Baselines/layouts/berner_10w3w_train{,_pkk2,_pkk3}__{heuristic,ga}.json` +
  `…_train__sa.json` — BERNER layouts.
* `synthetic_datasets/berner_10w3w_train_pkk{2,3}_*.csv` + `_meta.json` (patched).
* **Provenance (which build produced which rows + mean closure):** the
  `berner_10w3w` k=2 summary/eval rows come from `berner_10w3w_train_pkk2`
  (**mean|closure| = 7.03**, c_bar 1.330, Π_true 369); the k=3 rows from
  `berner_10w3w_train_pkk3` (**mean|closure| = 8.30**, c_bar 1.569, Π_true 360); the
  k=1 rows from the untransformed `berner_10w3w_train` (mean|closure| = mean|support|
  = 5.29). Synthetic k=2/k=3 rows come from the `syn_50sku{,_s142,_s242}_pkk{2,3}`
  builds (mean|closure| ≈ 15.4–16.1 at k=2, ≈ 19.7–20.4 at k=3).

## 14. Iteration-2 verdict for Stage 5

**Does H1 hold on industrial data? YES for the heuristic — and more cleanly than on
the synthetics.** On BERNER 10w3w the enlarged covering layout (k=2, k=3) **Pareto-
dominates** the nominal layout: it lowers both nominal cost (PoR −0.92% → −2.45%)
and single-cell test visits (G +0.32% → +1.98%), monotone in k. The caveats Stage 5
must carry: (i) this is a **single test cell**, so no CI for the BERNER gain;
(ii) **SA is unscalable** (skipped on the enlarged arms) and **GA degenerates** to a
seed-fixed random layout at 120 s, so the industrial evidence rests on the heuristic
alone; (iii) on the multi-cell **synthetics the gain G flips sign across train
seeds** (§10.2) and the oracle regret advantage of k=2 is cell-dependent (§10.3) —
so the synthetic claim stays "weak/conditional," while the industrial claim is
"clean but single-cell, heuristic-only." Recommended framing: report BERNER as the
strong-but-narrow confirmation and the 3-seed synthetics as the
breadth-but-instability counterweight.
