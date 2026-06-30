---
name: iscfco-dataset
description: iscfco = co-occurrence-rich ISCF-derived testbed (1600 SKUs, 15k orders, 20% singletons) for the demand-shift robustness round
metadata:
  type: project
---

`Baselines/iscf_cooc_builder.py` produces **`iscfco`** (`iscf_instances/iscfco_*.csv`): a
co-occurrence-RICH instance derived from the real ISCF orders, built to fix the singleton problem
(raw ISCF is 54.9% singletons = zero co-occurrence value) for the demand-shift robustness round.

**Config (user-chosen 2026-06-22):** 1600 SKUs (8x200 flat layout), 15,000 orders, **20% singletons**
(under the user's 30% ceiling). Method: keep the top-1600 SKUs by *multi-item* order frequency
(dense universe — trims the rare tail), restrict orders to them, sample 80% multi-item (preserving
real co-occurrence + size dist) + 20% singletons, greedy coverage skeleton front-loaded to earliest
ORDER ids so every 50/50..90/10 temporal cut has the full universe in train (0 missing). REAL_LINES +
flat kappa-invariant TIME_CAPACITY recomputed.

**Achieved stats:** mean order size 3.44 (vs raw 2.38), singleton frac exactly 20%, full coverage,
**per-product co-occurrence median 13 / mean 32** (vs sparse raw), 8,571 distinct multi-supports,
size hist {1:3000, 2:4650, 3:2581, 4:1492, 5:923, 6:647, 7:492, 8:298,...}. Standard semicolon schema,
products file carries REAL_LINES/VOLUME/FREQUENCY.

**Why:** the cover-objective round showed break-even is objective-invariant ([[injected-shift-result]]);
remaining lever is the **demand-changing shift** on a dataset with real co-occurrence signal. iscfco is
that dataset. NEXT (not yet built): a demand-shift injector (change product L_p, not just co-occurrence)
with the user's dummy-assignment flat-workload safeguard (dummy assign products->stations, set all
stations' T_s = max-station workload), then cover(minmax+minsum) -> place(Hexaly) -> evaluate-shift on
iscfco temporal cuts. See [[temporal-split-preferred]], [[iscf10k-subsample]], [[iscf-data-is-stationary]].
