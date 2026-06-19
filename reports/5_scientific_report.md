# Scientific Audit Report — Stage 5 (CSLAP Robustness via P–K Covering, Smoke Run)

**Auditor:** Scientific Reviewer (loop iteration 1/5). **Inputs:** brief `0_research_brief.md`, method report `2_method_report.md` (eqs. 1–13, P1–P3, U1–U7), coder log `3_coder_log.md`, code review `4_review_report.md` (PASS + 2 MAJOR science flags), `results_robustness_eval.csv` (712 rows), `results_robustness_summary.csv` (19 rows), harness log, transformed instance CSVs. All statistics below computed by the reviewer from the per-cell eval CSV (script: `c:\tmp\stage5_analysis.py`; no repo file modified).

---

## 0. NEW CRITICAL FINDING (missed by Stages 3 and 4): the k=4 arm is a degenerate identity transform

Direct comparison of `syn_50sku_pkk4_orders.csv` against `syn_50sku_orders.csv`:

* **2336 / 2336 orders have closure exactly equal to the original support. Zero strict supersets.** Closure size distribution is bit-identical to the original order-size distribution (mean 9.06, std 2.78, max 15).
* Π\*(k=4) = 15 = the maximum order size — the exact signature of a **singleton partition** (every pattern hitting an order must be contained in it for closure = support to hold for all 2336 orders; with non-trivially co-occurring Zhang data this forces effective singletons).
* No U7b warning fired because the integer master legitimately returned a singleton-equivalent incumbent — the degeneracy guard only catches *no incumbent*, not a *degenerate* incumbent.
* The k=4 arm therefore differs from the k=1 arm **only** through the side effects of the transform: recalibrated `TIME_CAPACITY` (4656 vs original 5198, due to the duplicate-row collapse Stage 4 flagged as MINOR) and QTY-collapsed rows. Every k=4 "effect" in the summary — including heuristic's PoR = −3.16% and GA's G = +0.52% — is solver response to a tighter time-capacity constraint on a robustness-identical instance. **Scientifically void as a robustness arm.**

This refutes specific written claims in the record:

**Line-level issues (caveman-review format):**
- `reports/3_coder_log.md` §5 chunk 1 / §7: "substitute validation = non-degenerate cover at k=2/k=4 with Π\* > 1 and mean closure > mean order size" — FALSE for k=4. Mean closure 9.06 = mean order size 9.06 exactly. Π\*>1 is not a degeneracy test when Π\* = max|P_o|.
- `reports/4_review_report.md` §5: "All reported transforms non-degenerate (Π\*∈{9,10,13,15}, mean|closure|>order size)" — FALSE for the Π\*=15 row.
- `reports/4_review_report.md` §5: "every positive-G row carries a positive PoR" — FALSE: syn_50sku ga k=4 has G=+0.52%, PoR=−0.42%. (Moot once the arm is voided, but the sanity claim was wrong as stated.)
- `run_robustness_experiment.py` (transform step, ~L380–400): no post-transform degeneracy assertion (closure-vs-support comparison). Must be added.
- `logs/robustness_harness.log` L25 vs L31: two k=2 builds, mean|closure| 15.52 then 15.38 under the same fixed subsample seed — construction is not run-to-run reproducible (time-budget-dependent CG column pool). Results used the 15.38 build; coder log cites 15.52. MINOR, but log/report should cite the build that produced the data.
- `ga_baseline.py` L176: `np.random.shuffle(indices)` uses the unseeded global RNG while L228 seeds a local `RandomState(42)` — GA is not fully deterministic. MINOR (single run per arm, but undermines "solver seeds fixed and logged" in Method Report E.4).
- `results_robustness_eval.csv` L2: orphan `TRIVIAL` row (already flagged by Stage 4; excluded from all statistics here).

**Consequences:** the effective knob grid is **k ∈ {2} everywhere** (20/50/500 sku). The Stage-4 "closure non-monotone in k" puzzle dissolves (§4 below). The k=4 rows must be removed or relabeled "degenerate control" before any writing.

---

## 1. Statistical analysis (computed, paired, identical test cells)

Pairing verified: every k>1 arm shares exactly the same 45 (θ′, ρ, seed) test cells with its k=1 arm (45/45 intersection; 4/4 at 20sku). Positive values = robust arm better on test. Wilcoxon signed-rank, two-sided; 95% t-CI on the paired relative difference; Holm within (instance, solver) family as run.

### A1 — Primary paired test, k>1 vs k=1

| instance | solver | k | n pairs | mean rel. gain % | 95% CI % | frac. pairs > 0 | Wilcoxon p | Holm p (as run) |
|---|---|---|---|---|---|---|---|---|
| syn_50sku | ga | 2 | 45 | **+1.48** | [+0.85, +2.11] | 0.80 | <0.0001 | <0.0001 |
| syn_50sku | sa | 2 | 45 | **+0.85** | [+0.44, +1.27] | 0.76 | 0.0002 | 0.0004 |
| syn_50sku | heuristic | 2 | 45 | **+0.54** | [+0.11, +0.97] | 0.62 | 0.0339 | 0.0678 |
| syn_50sku | ga | 4† | 45 | +0.59 | [+0.03, +1.14] | 0.62 | 0.0339 | 0.0339 |
| syn_50sku | heuristic | 4† | 45 | −0.24 | [−0.68, +0.20] | 0.47 | 0.509 | 0.509 |
| syn_50sku | sa | 4† | 45 | +0.06 | [−0.57, +0.70] | 0.49 | 0.746 | 0.746 |
| syn_500sku | ga | 2 | 45 | **+0.21** | [+0.03, +0.40] | 0.69 | 0.0223 | 0.0223 |
| syn_500sku | heuristic | 2 | 45 | −0.06 | [−0.35, +0.22] | 0.53 | 0.744 | 0.744 |
| syn_500sku | sa | 2 | 45 | **−0.18** | [−0.36, −0.00] | 0.36 | 0.0276 | 0.0276 |
| syn_20sku | heuristic | 2 | 4 | −0.58 | [−8.6, +7.5] | 0.50 | 1.0 | — |
| syn_20sku | sa | 2 | 4 | +1.87 | [−10.7, +14.5] | 0.75 | 0.625 | — |

† degenerate arm (§0) — rows void, shown only for the record. With k=4 excluded, each 50sku family contains one test and the raw p stands: **heuristic k=2 p = 0.0339 is then significant at α=0.05** (the Holm 0.0678 above was inflated only by pairing it with a void test). syn_20sku: n=4 pairs — essentially zero power, descriptive only.

Nominal price (single point per arm — no CI is possible; one train instance, one solver run): PoR(2) = +0.90% / +0.29% / +1.11% (50sku h/sa/ga), +1.97% / −0.26% / +0.37% (500sku h/sa/ga).

### A2 — Gain by shift level ρ (paired, n=15 per cell)

Mean paired relative gain %, genuine k=2 arms:

| instance | solver | ρ=0 | ρ=0.5 | ρ=1.0 | Spearman r(ρ, gain) | paired-slope of gain vs ρ (p) |
|---|---|---|---|---|---|---|
| syn_50sku | ga | +0.83 | +2.16* | +1.44 | 0.03 (ns) | +0.025 (0.46) |
| syn_50sku | sa | +0.44* | +0.20 | **+1.92*** | **0.41 (p=0.005)** | **+0.065 (p=0.002)** |
| syn_50sku | heuristic | +0.25 | +0.54 | +0.84 | 0.12 (ns) | +0.025 (0.27) |
| syn_500sku | ga | +0.13 | +0.12 | +0.40 | 0.16 (ns) | +0.012 (0.23) |
| syn_500sku | heuristic | −0.40 | −0.31 | **+0.51*** (p=0.0035) | **0.42 (p=0.004)** | **+0.039 (p=0.007)** |
| syn_500sku | sa | −0.17* | −0.30 | −0.07 | 0.01 (ns) | +0.004 (0.65) |

\* per-cell Wilcoxon p<0.05. Notable: 500sku heuristic is flat-to-negative overall but **significantly positive at the maximum shift ρ=1.0** — gain emerging only under large shift, exactly the H1 mechanism. Secondary axis θ′: gain increases monotonically with θ′ for ga/sa at 50sku and ga at 500sku; decreases for sa at 500sku (consistent with its overall negative result).

### A3 — Degradation slopes (OLS, mean visits/order vs ρ; P3)

Slope difference (robust − nominal); negative = robust arm flatter:

| instance | solver | k | slope k=1 | slope k | diff | z-test p |
|---|---|---|---|---|---|---|
| syn_500sku | heuristic | 2 | +0.0123 | −0.0266 | **−0.0389** | **0.0013** |
| syn_50sku | sa | 2 | +0.0079 | −0.0568 | **−0.0647** | **0.0169** |
| syn_50sku | ga | 2 | −0.0006 | −0.0258 | −0.0252 | 0.53 |
| syn_50sku | heuristic | 2 | +0.0652 | +0.0398 | −0.0254 | 0.41 |
| syn_500sku | ga | 2 | −0.0073 | −0.0189 | −0.0116 | 0.18 |
| syn_500sku | sa | 2 | +0.0127 | +0.0084 | −0.0043 | 0.60 |

All six genuine k=2 comparisons have the robust slope flatter (sign consistent 6/6; binomial sign test p=0.03 if treated as independent draws, which they only partly are); individually significant for 2/6. The more powerful paired version (per-cell gain regressed on ρ) gives a positive slope-of-gain in all 6 genuine arms, significant for sa@50sku (p=0.002) and heuristic@500sku (p=0.007).

Sanity: coverage κ=1.0 in every test cell (frozen universe — as designed); cap_broken=0 everywhere; wl_broken comparable across arms (e.g., 500sku 3.74 vs 3.79 mean) — no hidden feasibility price on the robust side.

---

## 2. Design audit — does the smoke design test H1?

**What is sound:**
1. Pairing is real and verified (identical cells across arms); the paired analysis is the correct design and is what rescues sub-percent effects from seed noise.
2. Leakage: Stage 4's trace is corroborated by the data — every positive-G genuine arm carries positive PoR; the single "free lunch" row (ga k=4) is fully explained by the degenerate arm (§0), not by leakage. No G>0 ∧ PoR≈0 signature among genuine arms.
3. Nominal-loss side is measured and reported (brief §4 satisfied in structure): PoR > 0 in 5/6 genuine k=2 cells.
4. The shift family (eq. 4) is implemented as committed (frozen universe, orders-only regeneration; ρ-grid {0, 0.5, 1.0} is a documented shrink of the committed {0, 0.25, 0.5, 1.0}; M=5 seeds vs committed 10).

**What limits the evidence:**
1. **One train instance per N** (contract E.3 mandated ≥3 train seeds for N∈{50,500}). Every p-value above is conditional on one fixed pair of layouts from one training draw. The inference is "layout a₂ beats layout a₀ on this shift family," not "the method produces more robust layouts." Method-level claims are **not licensed** by this design.
2. **Effective k grid = {2}.** With k=4 void and k=6 dropped, the "tradeoff curve in k" (E.1.6), the U-shape prediction (D), and P1/P2's "increasing in k" clauses are all **untestable** from this data. The headline deliverable of brief §4 — a curve — is currently a single point per solver.
3. **No exact-solver arm** (Gurobi absent, Hexaly not invoked). The majorant argument (eq. 3) guarantees PoR ≥ 0 only at optimality; with metaheuristics, PoR point estimates carry solver-path noise of the same order as the effect (the void k=4 arm proves this concretely: a robustness-identical instance moved heuristic's nominal cost by −3.16% through the T_s side-channel alone). PoR has no replication and no CI anywhere.
4. **Eq. 12 oracle regret absent** (Stage-4 MAJOR confirmed). Without the test-reoptimized normalizer, G cannot be placed on an achievability scale — we cannot say how much of the available robustness headroom k=2 captures.
5. **Acceptance test Π\*=6 not reproduced** (HiGHS ceiling, honestly logged), and the substitute non-degeneracy validation demonstrably failed once (§0). Construction QA is the weakest link in the chain.
6. syn_20sku: n=4 cells — no power; should be labeled pilot-only and excluded from claims.
7. The T_s side-channel: transformed arms run under recalibrated time capacities (eq. 10) that differ from the original even when closures don't (duplicate-row collapse). For genuine arms this is a declared bias (U6), but it means PoR/G mix "enlargement effect" with "capacity-recalibration effect." A clean decomposition needs the k=1-transform control (pkk1 instance) as a third arm — it exists on disk but was not run as an arm.

---

## 3. Predictions verdict

* **P1 (PoR > 0, increasing in k): INCONCLUSIVE.** PoR > 0 in 5/6 genuine k=2 cells (range +0.29% to +1.97%), consistent with the prediction's direction; sa@500sku is −0.26% (within solver noise; no replication to test). "Increasing in k" untestable — only one genuine k. The theoretical guarantee applies only to exact solvers, none of which ran.
* **P2 (G > 0 for some k, increasing in shift): CONDITIONALLY SUPPORTED at 50 SKUs; MIXED at 500.** G > 0 with paired significance for all three solvers at syn_50sku k=2 (ga p<0.0001, sa p=0.0002, heuristic p=0.034). "Increasing in shift" supported with significance for sa@50sku and heuristic@500sku, directionally positive in 6/6 genuine arms; at 500sku the overall effect is positive only for ga, **significantly negative for sa**. Conditional on solver and scale.
* **P3 (flatter degradation slope): DIRECTIONALLY SUPPORTED.** Robust slope flatter in 6/6 genuine arms, individually significant in 2/6 (heuristic@500 p=0.0013, sa@50 p=0.017). Consistent but mostly underpowered.
* **H1 overall: conditionally supported at smoke scale.** The falsification criterion (P2 fails for all k>1 at all shift levels) is **not** met. But neither is the evidence sufficient for a method-level claim (one train seed, one genuine k, no exact solver, no oracle).

---

## 4. Closure-monotonicity resolution (Stage-4 MAJOR (b))

**Resolved — but not the way Stage 4 framed it.** The k=4 closure mean of 9.06 is not a "coarser-partition-hits-fewer-patterns" phenomenon requiring a revised bias narrative; it is the original order-size distribution, because the k=4 construction collapsed to an effective singleton partition (§0). The Method Report's bias story (D) survives **in theory** unmodified; what failed is the construction's delivery of a genuine k=4 enlargement under the HiGHS + 150-support-subsample regime. Two directives follow:

1. The k=4 rows are removed from the evidence base, and the bias-monotonicity narrative is simply untested above k=2 — not contradicted.
2. For the article, the reported tradeoff must be **parameterized by the realized enlargement ratio** $\bar{c} = \text{mean}|\bar{P}_o| / \text{mean}|P_o|$ (50sku k=2: 15.38/9.06 = 1.70; 500sku k=2: 18.23/9.89 = 1.84; degenerate arm: 1.00) rather than by nominal k alone. k sets an upper bound on pattern size; the achieved partition decides conservatism. $\bar{c}$ must be stamped into the summary CSV per arm, with $\bar{c} \approx 1$ auto-flagged degenerate.

---

## 5. Honesty checks

* **Free-lunch signature:** one row (ga, 50sku, k=4: G=+0.52%, PoR=−0.42%) — explained as degenerate-arm solver noise, not leakage; voided. Genuine arms: none.
* **Negative results present and must be reported:** sa@500sku k=2 is significantly *worse* under shift (mean −0.18%, CI excludes 0, p=0.028) while marginally cheaper nominally — for SA at 500 SKUs under a 60s budget, the transform delivered anti-robustness. Plausible mechanism: at 500 SKUs / 60s the metaheuristics are far from convergence and the enlarged instance (more lines per order) is harder to search; this is a real deployment caveat, not noise to suppress.
* **"Outer approximation" usage: COMPLIANT.** The method report uses it strictly in the three committed senses (per-order inclusion, support inclusion, objective majorization — A.2) with proof sketches and an explicit honest boundary (no probabilistic containment claim; U5). Code docstrings say only "robust counterpart." No loose usage found anywhere in the Stage-3 deliverables.

---

## 6. What may honestly be claimed vs. not

**May be claimed (with stated limitations):**
* On one synthetic training instance at 50 SKUs, the k=2 P–K enlargement (realized enlargement ratio 1.70) produced layouts that, under a 45-cell parametric shift grid, beat the nominal layouts of all three metaheuristic solvers in paired comparison (gains +0.5% to +1.5%, each p<0.05), at a nominal price of +0.3% to +1.1% — a genuine price-of-robustness tradeoff with no free lunch.
* The gain grows with shift magnitude in all genuine arms (significantly for 2/6), and degradation slopes are uniformly flatter for the robust arms (significantly for 2/6) — the qualitative H1 mechanism.
* At 500 SKUs the effect is solver-dependent: positive for GA (p=0.022), null for the clustering heuristic overall (but significantly positive at maximum shift), significantly negative for SA.

**May NOT be claimed:**
* Any method-level generalization (one train seed; contract required ≥3).
* Anything about the shape of the tradeoff in k (one genuine k; U-shape, monotonicity, and the E.1.6 curve are all untested).
* Anything about exact solvers, PoR magnitudes with confidence bounds, or oracle-relative regret (eq. 12 unimplemented).
* Anything about real (BERNER temporal) shift — only the parametric Zhang family was exercised.

---

## 7. Verdict

The framework is sound (no REVISE_METHOD: Prop. 1/eq. 5 identity is correct, outer-approximation usage is disciplined, the negative results are coherent with the theory's own caveats). The code is structurally correct, but the evidence base is contaminated by one undetected degenerate arm and is one genuine k-level and one train seed short of supporting even a hedged smoke-scale finding about a *tradeoff curve*. A scoped increment — not the full 50–100× grid — closes the gap. This is iteration 1 of 5; budget exists for exactly one such loop before writing.

```yaml
STATUS: MORE_TESTING
ITERATION: 1
REASON: k=4 arm proven degenerate (closure==support for 2336/2336 orders, missed by Stages 3-4), leaving one genuine k-level and one train seed - insufficient for the committed tradeoff-curve claim; framework itself sound, k=2 signal real.
INSTRUCTIONS: Return to Coder (Stage 3) for one scoped re-run, then direct to Stage 5 (skip full Stage-4 re-review; delta review of items 1-2 only). (1) GUARDS: add post-transform degeneracy check (fraction of orders with closure strictly containing support; if <5% mark arm DEGENERATE, exclude from summary, log loudly); stamp realized enlargement ratio c=mean|closure|/mean|P_o| and a degenerate flag into transform meta and summary CSV; prune the TRIVIAL eval row; cite the actual build (closure 15.38) in the log. (2) FIX k=4 CONSTRUCTION at syn_50sku so it yields genuine enlargement (acceptance: >=50% orders with strict closure growth AND c>=1.2): raise --cover-max-supports to 300-400, seed the column pool with greedy co-occurrence merges of sizes 2..k, and/or extend integer-master budget; if k=4 still saturates, substitute k=3 and document. (3) RUN: syn_50sku with 3 train seeds, k in {1,2,4-fixed}, solvers heuristic+sa+ga, full 45-cell test grid per seed, --time 60 unchanged; ALSO run the pkk1 arm as a control on one seed to decompose the T_s-recalibration side-channel from the enlargement effect. syn_500sku: keep existing k=2 rows; add nothing unless budget remains. (4) ORACLE (eq. 12): at syn_50sku seed 42 only, reoptimize each solver directly on test cells (theta'=0.7, rho in {0,1.0}, test seed 43) under the same 60s budget and report RR for k=1 and k=2 layouts. (5) Report per-(train-seed, solver, k) paired stats rows in the eval CSV exactly as now so Stage 5 can pool across train seeds (sign consistency across 3 seeds + per-seed Wilcoxon). Estimated cost ~4-5x the 50sku smoke chunk, not the full grid. Defer BERNER and Hexaly arms to a post-acceptance full run.
```

---

## 8. ADDENDUM — Human supervisor directive (overrides INSTRUCTIONS item on BERNER deferral)

The human supervisor has directed (2026-06-12): **the BERNER industrial arm may NOT be deferred past this loop.** Before any ACCEPTED verdict and advance to the Academic Writer, the same tests must also run on the full industrial dataset `Heuristic_Connex_Set_Project/data/BERNER_ORDER_LINES_09-12.csv` (temporal train-early/test-late split per Method Report A.4(a)), so the evidence is not exclusively from small synthetic data. The Stage-3 re-run scope is therefore: reviewer items (1)–(5) PLUS the BERNER temporal arm (metaheuristic solvers at industrial scale; construction with documented U7 mitigations; degeneracy guard mandatory). Seed-collision correction by the orchestrator: train seeds for item (3) must be disjoint from the test-seed range {43..47} — use {42, 142, 242}.
