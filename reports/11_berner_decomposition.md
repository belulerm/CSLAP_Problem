# Report 11 — BERNER preprocess-vs-capacity decomposition (closing the last confound)

**Date:** 2026-06-25. **Tools:** `Baselines/berner_adapter.py` (rebuild BERNER as a clean
κ-invariant top-2000 instance), `run_robustness_iscf.py build-covers --objective minsum` (CPLEX),
`Baselines/berner_decompose.py` (4-arm 2×2, unchanged Hexaly placement + `evaluate_layout_robust`).
Figure: `reports/figures/fig7_berner_decomposition.png`.

## Why this experiment

BERNER (Company B) was the **only** instance where a positive out-of-sample gain ever appeared
(`reports/7` / draft Table `rc-berner`: heuristic `G=+0.3%` at κ=2, `+2.0%` at κ=3). But that run
changed **two** things at once and never separated them: the covering **enlargement** (closures) and
a **time-capacity recalibration** — the robust arm rebuilt each station's workload cap `T_s` from the
*inflated* closure line counts (eq. 10 of `pk_instance_robust`), making it **looser** → more
placement freedom → fewer visits *on its own*. The open question: did the BERNER value come from the
set-cover preprocess (the outer-approximation) or from the workload-capacity increase?

## Design — a clean 2×2

Rebuilt BERNER in the harness format on the real 24-station layout/speeds, restricted to the top-2000
SKUs (175,419 train / 49,748 test orders, κ_sku=1.0, 64% train-line coverage). Min-sum CPLEX covers
at k∈{2,3,4,6,10} (all certified optimal; c̄ from 1.49 to 3.02). Every arm placed with the **same**
unmodified Hexaly model; visits counted on the **same** real test orders; the real per-product
pick-lines are the κ-invariant workload in every arm — **only `T_s` differs** between B and C:

| arm | orders | capacity | isolates |
|---|---|---|---|
| A | nominal | real | baseline (k=1) |
| **B** | closures | **real (κ-invariant)** | **the outer-approximation alone** |
| C | closures | recalibrated (loose) | the v2 robust arm |
| D | nominal | recalibrated (loose) | the capacity loosening alone |

## Result — the gain is capacity, not the preprocess

| k | c̄ | T_s (real→recal) | **G(B) preproc** | G(C) v2-full | G(D) cap-only | PoR(D) |
|---|---|---|---|---|---|---|
| 2 | 1.49 | 7→32 | **−3.41%** | −3.11% | +0.09% | −0.78% |
| 3 | 1.82 | 7→39 | **−3.65%** | −0.28% | +3.37% | −3.39% |
| 4 | 2.07 | 7→44 | **−2.15%** | +2.05% | +4.79% | −5.23% |
| 6 | 2.43 | 7→52 | **−0.93%** | +3.17% | +5.41% | −5.88% |
| 10 | 3.02 | 7→65 | **+0.13%** | +4.56% | +7.97% | −8.54% |

All arms feasible (`cap_broken=wl_broken=0`). Three conclusions:

1. **The outer-approximation alone gives no out-of-sample gain.** `G(B)` (closures, *real* capacity)
   is **negative for k=2,3,4,6** and only reaches break-even (+0.13%) at k=10 — and only with a
   massive c̄=3.0 enlargement. On its own the preprocess *hurts*, exactly as on the clean ISCF
   instance (`reports/7`, G=−6.8%).
2. **The entire v2 "win" was the capacity loosening.** `G(D)` (nominal orders, loose cap, **zero
   enlargement**) is positive and growing (+0.1→+8.0%) — it delivers the whole gain, and *more* of it
   than the full v2 arm. `PoR(D)<0` shows D is cheaper on **train** too: the original cap `T_s=7` was
   **binding**, and recalibration simply **relaxed a binding constraint** — a constraint relaxation,
   not robustness, and one that would help the nominal layout just as much.
3. **The closures are counterproductive.** `G(C) < G(D)` at every k — adding the enlargement to the
   loose-cap arm *costs* ~3% out-of-sample consistently. The v2 positive was the side-channel masking
   a preprocess that drags.

## Verdict

The BERNER apparent "win" was the **workload-capacity side-channel, not the set-cover
outer-approximation**. With capacity held κ-invariant (the real workload), the preprocess returns
negative-to-break-even out-of-sample on BERNER's own co-occurrence structure — the same clean
negative found on ISCF. The escalation criterion (re-run at full 21k iff `G(B)>0`) is **not met**, so
the question is settled at this scale; full-scale escalation is unnecessary.

This closes the project's last open confound. The covering construction is provably a robust
counterpart of the *training* objective (Prop. 1), but offers **no out-of-sample advantage** over the
direct solver on **either** real industrial instance once the capacity confound is removed —
consistent with the affinity boundary test (`reports/10`, win-region empty) and the order-data
diagnostics (`reports/9`, wrong regime). The empirical arc is complete; the honest finding is a clean,
mechanistically-explained negative for H1.
