---
name: iscf10k-subsample
description: iscf10k = 10k-order down-sample of full ISCF (all 4328 products), for tractable temporal higher-k experiments
metadata:
  type: project
---

`Baselines/iscf_subsample.py` produces **`iscf10k`** (`iscf_instances/iscf10k_*.csv`): a
coverage-guaranteed, distribution-preserving down-sample of the full ISCF order stream to
**10,000 orders** that still contains **all 4,328 products** (full universe), keeping real
ORDER_IDs (so temporal split works) and the 8×541 κ-invariant layout.

Method: greedy coverage skeleton (rare products first, orders capped at the 95th-pctile size to
avoid mean inflation) + size-stratified fill. Fidelity vs full ISCF: mean order size 2.58 vs 2.38,
size-share histogram within a few %, popularity Spearman rank-corr 0.83, FULL universe covered.
Only **4,411 distinct multi-item supports** (vs 108,820 full) → covers at k=3/4/6 are ~25× smaller
and far more tractable, though the partition is still over all 4,328 products.

**`iscf10kt` (USE THIS for the temporal test) = `iscf_subsample.py --front-load-coverage`.** Same
10k/4328 instance but the ORDER column is renumbered so the coverage skeleton (~1476 real orders
covering all products) gets the earliest temporal ranks; the fill keeps real ORDER_ID order. Result:
**every cut 50/50..90/10 has all 4328 products in train (0 missing)**, and the test is dominated by
**unseen product COMBINATIONS** (82.6% novel multi-item test orders at 50/50 -> 66.6% at 90/10). No
fabrication, no leakage (each order once; skeleton orders are real with real co-occurrence).

**Why (user, 2026-06-20):** the robustness question is unseen *combinations* of *known* products
(train {A,B},{B,C} -> test {A,C}), NOT new-SKU arrival. The natural temporal split left 958 products
missing from the 50% train cut, contaminating the test with product-novelty; front-load-coverage
removes that. (Key argument: a leakage-free synthetic order for a future-only product can only be a
SINGLETON — any multi-item synthetic order either copies a real future combo or fabricates fake
co-occurrence — so using real front-loaded orders is strictly cleaner than fabricating.)

**Pipeline (temporal only, see [[temporal-split-preferred]]):** make-folds(--mode temporal) ->
build-covers(CPLEX, train-only, k=2,3,4,6) -> place(Hexaly) -> evaluate. Use prefix **iscf10kt** and
dirs `iscf10kt_*_temporal/`. See [[iscf-kfold-result]], [[plan-cplex-phase-overview]].
