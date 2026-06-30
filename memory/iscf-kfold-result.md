---
name: iscf-kfold-result
description: Primary CPLEX-phase result — ISCF i.i.d. K-fold cleanly FALSIFIES H1 at k=2 (real price, no out-of-sample gain)
metadata:
  type: project
---

**Primary result of the CPLEX revalidation phase** (plan.md), on the clean iscf480 testbed
(480 most-frequent SKUs, 8x60 kappa-invariant layout, 308k orders), 5-fold random i.i.d. CV,
exact CPLEX k=2 cover (certified optimal Pi* in 4/5 folds, valid partitions, c_bar approx 1.63),
Hexaly placement on top-3000 frequent supports, visits counted on REAL orders:

- **PoR(k=2) = +6.8%** [95% CI 4.8%, 8.8%] — price of robustness positive, CI excludes 0. Stable.
- **G(k=2)  = -6.8%** [95% CI -9.0%, -4.7%] — out-of-sample GAIN is NEGATIVE, CI excludes 0.
- All 5 folds: V_te(nominal) < V_te(robust) (paired Wilcoxon p=0.0625 = the n=5 floor; sign-consistent).
- Feasibility clean: cap_broken=0, wl_broken=0 both arms, all folds; coverage kappa=1.0.

**Reading:** under i.i.d. resampling (NO distribution shift) the covering enlargement only pays a
price and gives no robustness benefit — a near-symmetric degradation (PoR ~ -G ~ 6.8%). This is a
**clean, honest negative for H1** at k=2 on this instance, and exactly what theory predicts when
there is no shift for conservatism to protect against. The kappa-invariant capacity removed the
first-run recalibration confound (G4), so unlike the BERNER first run there is NO free lunch here:
PoR>0 holds with the exact-ish setup.

**Caveats:** (1) single enlargement level k=2 — no PoR/G curve / interior optimum, because the
set-partition INTEGER master is intractable-to-optimality for k>=3 at this scale (k=3 incumbent
Pi=71 > k=2 optimal 49 = solver failure, not true monotonicity). (2) i.i.d. K-fold is a
generalization test, NOT a shift test; H1's potential benefit (if any) should be sought under
distribution SHIFT (temporal split / BERNER), still to run. (3) iscf480 is a scaled testbed: the
full 4328-SKU exact cover did not scale in-session (Pi_LP~73 for k2, 247s per LP solve). Placement
objective uses top-3000 supports (36.6% of multi-item order mass), evaluation uses ALL real orders.

**Temporal-shift variant (train-early/test-late by ORDER_ID rank, 5 expanding cuts, assumption U1):**
SAME direction, also a clean negative — PoR(k=2)=**+5.1%** [2.0%, 8.2%], G(k=2)=**-7.0%**
[-10.3%, -3.8%], both CIs exclude 0, all 5 folds G<0. So H1 fails under BOTH i.i.d. resampling AND
temporal shift on the exact/clean instance. Artifacts under `iscf_results_temporal/`,
`iscf_covers_temporal/`, `iscf_layouts_temporal/`, folds in `iscf_folds_temporal/`.

**Bottom line for write-up:** the exact + kappa-invariant setup REVERSES the first run's tentative
"weak positive (GA k=2)" — with no metaheuristic free-lunch and no recalibration confound, the
covering enlargement shows NO out-of-sample benefit at k=2, only a stable price. The first run's
positive was most consistent with metaheuristic suboptimality / seed noise. H1 is FALSIFIED at k=2
on the clean exact ISCF testbed (both shift models). Higher-kappa curve untested (integer master
intractable for k>=3 at scale). BERNER exact re-validation not run (21k SKUs >> ISCF cover scale
limit); first-run BERNER heuristic result stands as the only industrial datapoint, now contextualized.

Artifacts: `Baselines/iscf_results{,_temporal}/{per_fold,summary}.csv`, `iscf_covers*/`,
`iscf_layouts*/`, `logs/iscf480_*`. See [[plan-cplex-phase-overview]], [[placement-solver-hexaly-only]].
