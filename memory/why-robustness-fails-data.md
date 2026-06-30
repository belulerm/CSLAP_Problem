---
name: why-robustness-fails-data
description: Root-cause of the robustness break-even — the ISCF order data is realistic but the WRONG regime (sparse+stationary affinity, demand-insensitive objective)
metadata:
  type: project
---

`Baselines/analyze_order_distributions.py` (+ `reports/9_order_data_diagnostics.md`, figures in
`reports/figures/`) explains WHY the covering-enlargement robustness never beats break-even. Universe
and layout are identical across all scenarios, so the cause is the ORDER distribution.

**The data IS realistic** (good generalized warehouse demand): order size right-skewed (~55% singletons
baseline), product popularity heavy-tailed Pareto/Zipf (demand **Gini 0.771**, clean power-law on
log-log fig2), Lorenz deeply bowed. Nothing pathological in the marginals.

**Decisive diagnostic — co-occurrence is mostly a POPULARITY artifact, not affinity.** Lift =
observed_cooccurrence / (freq_a*freq_b/N) over the top-300 SKUs: baseline lift distribution is
**centered at lift≈1** (independence); genuine affinity is a minority tail — only **24% of pairs
lift>2, 9% lift>5**. So the "correlation structure" CSLAP/covering is built to exploit is SPARSE.

**Three reasons robustness fails (all from the data):**
1. Affinity is sparse+weak (only ~1 in 4-10 popular pairs is affine) -> little for the enlargement to
   group beyond what popularity already dictates.
2. The structure is STATIONARY (full-data early/late pair-cosine 0.85, popularity Pearson 0.93;
   [[iscf-data-is-stationary]]) -> nominal k=1 already captures the stable sparse affinity, no
   generalization gap to close. Our curveball shifts manufacture novelty RANDOMLY (off the affinity
   manifold), so closures can't anticipate it, and it saturates by rho~2.
3. The visit objective is DEMAND-INSENSITIVE (visits = co-location, not frequency) -> demand-shift
   barely moves G ([[injected-shift-result]]).

**Path to a positive result (only remaining sound lever):** COHERENT AFFINITY DRIFT — generate
train/test from two+ DIFFERENT affinity-community structures with controlled overlap (e.g. seasonal
market baskets that change), not random perturbation of one stationary structure. A robust layout fit
to the multi-regime affinity would beat one overfit to a single regime. This is a fundamentally new
synthetic-data design (NOT yet built). See [[iscfco-dataset]], [[temporal-split-preferred]].
