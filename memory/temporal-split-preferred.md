---
name: temporal-split-preferred
description: For the ISCF robustness experiments use ONLY the temporal split (order by ORDER_ID, hide latest IDs as test), not random K-fold
metadata:
  type: feedback
---

Going forward, evaluate H1 on the ISCF data using **only the temporal cut**: order by `ORDER_ID`,
hold out the **last** slice of order IDs as the test set, train on the earlier IDs. Do **not** use
random i.i.d. K-fold for the headline (it has no real distribution shift, so it can't test robustness).

**Why:** User directive (2026-06-20). The temporal split is the only one of the two that injects a
genuine train→test drift, which is what H1 is supposed to defend against. Random K-fold was run as a
baseline but is not the protocol of interest.

**How to apply:** Use `run_robustness_iscf.py make-folds --mode temporal` (writes expanding-window
early-train/late-test cuts). Skip the random-mode runs unless explicitly asked. See
[[iscf-kfold-result]] for the numbers and [[plan-cplex-phase-overview]].
