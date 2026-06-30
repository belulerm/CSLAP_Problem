---
name: iscf-data-is-stationary
description: The ISCF order data is temporally STATIONARY (no train→test structural shift) — so it cannot show a robustness BENEFIT, only the price
metadata:
  type: project
---

**Decisive diagnostic (2026-06-21):** the ISCF order stream has **no genuine temporal/structural
shift**. On the full 419k data, real early-50% vs late-50% (by ORDER_ID): product-popularity
Pearson **0.93**, pairwise co-occurrence freq-weighted overlap **0.81**, pair cosine **0.85**. The
demand correlation structure the layout optimizes (popular products + frequent pairs) is essentially
identical past vs future — classic stationary synthetic data (fixed itemset/affinity pool).

**Implication for H1:** with train ≈ test there is no shift for the covering enlargement to defend
against, so the direct (k=1) layout is already optimal for the future and the enlargement only pays
its price (PoR>0, G≤0). This **explains the negative result** ([[iscf-kfold-result]], full κ curve on
iscf10kt: PoR rises +3%→+13%, G falls −1.7%→−15% k=2..6) — it is the expected behavior of the theory
on stationary data, NOT a flaw in the method or code.

**The data is therefore unsuitable for demonstrating a robustness BENEFIT.** Subsampling cannot fix
it (our iscf10k subsample had LOWER similarity than reality — cosine 0.68 vs 0.85 — i.e. sampling
noise made the test *more* generous than real, and H1 still failed). The per-fold check: the only
non-negative gain was the least-similar 50/50 cut (G(k2)=+0.24%), weakly consistent with
"less similarity → better G", but even max-shift here barely breaks even.

**To test H1's mechanism we need genuine shift.** Options: (A) build a controlled-shift testbed
(inject graded novel co-occurrences into test while keeping all products seen — the {A,B},{B,C}→{A,C}
scenario at the structural level; sweep shift magnitude rho), or (B) check whether the REAL BERNER
industrial data has natural temporal drift (it is real, not synthetic, Sep–Dec — may have seasonal
shift; 21k SKUs so needs the same down-sample treatment). Tool: `Baselines/analyze_train_test_similarity.py`
computes the similarity metrics for any fold set. See [[temporal-split-preferred]], [[iscf10k-subsample]].
