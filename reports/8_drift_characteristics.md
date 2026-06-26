# Report 8 — Train (history) vs Test (future) drift characteristics on ISCF

**Date:** 2026-06-21. **Tool:** `Baselines/analyze_train_test_similarity.py` (read-only).
**Instance:** `iscf10kt` (10,000 orders, all 4,328 SKUs, flat 8×541 layout), full-train temporal cuts
50/50 → 90/10 (`iscf10kt_folds_temporal`). All numbers below are computed, not estimated.

## 1. How much does the "future" (test) differ from the "past" (train)?

Mean across the 5 temporal cuts (full train, late test):

| Characteristic | Metric | Value | Reading |
|---|---|---|---|
| Order size | mean train → test | 2.64 → 2.55 | nearly unchanged |
| **Product demand** | per-product frequency Pearson | **0.86** | strongly correlated (same SKUs popular) |
| Product demand | top-50 SKU demand share train → test | **0.22 → 0.46** | demand **concentrates** in the future (see caveat) |
| Product demand | fraction of SKUs moving > 200 rank positions | **0.69** | large rank churn (see caveat) |
| **Co-occurrence** | pair overlap (freq-weighted) | **0.58** | majority of test co-occurrence already seen |
| Co-occurrence | pair cosine | **0.68** | structure substantially preserved |
| Co-occurrence | pair overlap (distinct, unweighted) | 0.31 | novelty lives in the rare tail |
| Orders | exact-order novelty | 0.76 | most full orders are novel **as sets** |
| Orders | recombination of seen pairs | 0.47 | but ~half are recombinations of seen pairs |

Per-cut trend (similarity rises as the train window grows / the test tail shrinks):

| cut | pair cosine | pair seen(w) | order-novel | demand top-50 (tr→te) | pop r |
|---|---|---|---|---|---|
| 50/50 | 0.76 | 0.48 | 0.83 | 0.20 → 0.35 | 0.92 |
| 60/40 | 0.75 | 0.51 | 0.80 | 0.21 → 0.37 | 0.90 |
| 70/30 | 0.68 | 0.57 | 0.77 | 0.22 → 0.41 | 0.86 |
| 80/20 | 0.62 | 0.63 | 0.73 | 0.23 → 0.49 | 0.83 |
| 90/10 | 0.57 | 0.72 | 0.67 | 0.24 → 0.67 | 0.80 |

## 2. Interpretation (and an important caveat)

- **Co-occurrence structure is largely stable** (pair cosine 0.68, weighted overlap 0.58, popularity
  Pearson 0.86). The "novelty" in full orders (76%) is **superficial** — ~47% are recombinations of
  *seen* pairs. This is the stationarity established in `reports/`-level analysis (full-data early/late
  pair-cosine **0.85**, popularity Pearson **0.93**) and is *why* the direct (k=1) layout is already
  well-matched to the future, leaving the covering enlargement at break-even.
- **Demand drift looks larger than it is.** The top-50 demand share appears to jump 0.22 → 0.46 and
  69% of SKUs move > 200 ranks, but this is **confounded by test size**: the late test windows are
  small (down to 1,000 orders at 90/10), so the top SKUs mechanically dominate and low-frequency
  ranks are noisy. The size-robust signal — per-product frequency Pearson **0.80–0.92** — shows the
  demand distribution is in fact fairly stable. Genuine demand drift exists but is modest.

## 3. Consequence for the injected-shift experiments

Because the real drift is mild and mostly co-occurrence-stable, the controlled **co-occurrence shift**
(`iscf_shift_inject.py`, demand-preserving curveball swaps) is the principal source of test novelty.
Realised injected novelty vs the real baseline (ρ=0):

| shift | pair-novelty vs train, ρ=0 (real) | ρ=1 | ρ=2 |
|---|---|---|---|
| structured (within-affinity) | 0.54–0.80 | 0.65–0.86 | 0.67–0.87 |
| unstructured (global) | 0.54–0.80 | 0.73–0.90 | 0.76–0.91 |

i.e. ρ=2 pushes co-occurrence novelty to ~0.86–0.91, well past the real ~0.76, and **saturates**
there. This is why the next levers are (a) a **cover redesign** (min-sum vs min-max, larger K) to
make closures that anticipate the recombinations the direct layout misses, and (b) a future
**demand-changing shift** round (the natural demand drift, though modest, is real and untested).
