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

## The faithful robust arm (C′/D′) + real-world feasibility (`berner_decompose_cprime.py`)

A review note observed that arm C above is a hybrid: closures objective but the *real* workload
signal under a loose cap, so the constraint went artificially slack and C behaved like D. The
faithful "solve the transformed instance" arm feeds the closure-derived workload `bar_L` AND the
loose cap together: **C′** = closures + `bar_L` workload + loose `T_s`; **D′** = nominal + `bar_L`
workload + loose `T_s`. Every C′/D′ layout is also rechecked against the **real** `L_p`/`T_s` (the
old `cap_broken=0` was a station-id type artifact; real feasibility is computed explicitly here).

| k | c̄ | G(C′) | G(D′) | C′−D′ | real `wl_broken` C′/D′ (of 24) | worst overload |
|---|---|---|---|---|---|---|
| 2 | 1.49 | −7.32% | −5.25% | −2.07% | 7 / 6 | 5.49× |
| 3 | 1.82 | −8.25% | −5.47% | −2.77% | 7 / 7 | 4.20× |
| 4 | 2.07 | −6.44% | −4.60% | −1.84% | 8 / 7 | 6.33× |
| 6 | 2.43 | −7.33% | −4.60% | −2.73% | 9 / 6 | 3.68× |
| 10 | 3.02 | −5.68% | −4.03% | −1.66% | 7 / 9 | 3.14× |

This strengthens the verdict three ways. (a) The faithful robust arm **loses 5.7–8.3% out of sample**
at every k — making the closure world self-consistent does not recover break-even, it goes firmly
negative. (b) `C′−D′ ≤ 0` everywhere — a **third** independent isolation of the enlargement's own
effect (after `B−A` and `oldC−oldD`), all three showing the enlargement *costs* ~2–3.5% in any
workload regime. (c) The C′/D′ layouts **violate the real workload limit** on 6–9 of 24 stations by up
to 5.5×, so they are not deployable. By the same construction the only positive arm, `oldG(D)`, was
optimized under the loose cap and likewise violates the real `T_s`: the apparent gain was a layout the
warehouse cannot run. **The only arms that respect the real `T_s` are A and B, where `G(B) ≤ 0`.**

## Fair per-station 120% caps + bigger k (`berner_clean_comparison.py`)

Two fairness objections were then settled in one table. (i) `A`/`B` used a real **per-station 120%**
cap while the inflated arms used eq. 10's **flat 110% of the mean** — unfair, since the BERNER
warehouse is highly non-flat (real `T_s` ranges 7 to 148). So the inflated arms were rebuilt at the
**per-station 120%** cap `T_s^fair = ⌈1.20·Σ_{p:a₀(p)=s} bar_L_p/V_s⌉` (A's exact calibration on the
inflated lines, using the saved pinning `a₀`). (ii) `G(B)` was extended past k=10 to **k=15, 20**
(c̄ up to 4.17). All arms at 120%, single temporal split:

| k | c̄ | **G(B) real (deployable)** | G(C″) fair | G(D″) fair | **C″−D″** | G(oldD) slack | deployable B / C″ / D″ |
|---|---|---|---|---|---|---|---|
| 2 | 1.49 | −3.33% (ok) | −4.58% | +0.23% | −4.81% | +0.45% | ok / no(5) / no(5) |
| 3 | 1.82 | −3.24% (ok) | −2.38% | −0.92% | −1.46% | +3.33% | ok / no(4) / no(5) |
| 4 | 2.07 | −2.18% (ok) | −1.72% | +0.26% | −1.98% | +5.60% | ok / no(7) / no(8) |
| 6 | 2.43 | −0.94% (ok) | −2.35% | +1.92% | −4.27% | +5.32% | ok / no(6) / no(8) |
| 10 | 3.02 | +0.02% (ok) | −2.52% | +1.87% | −4.39% | +7.92% | ok / no(6) / no(7) |
| 15 | 3.62 | −2.80% (ok) | −1.34% | +1.19% | −2.52% | +7.22% | ok / no(7) / no(5) |
| 20 | 4.17 | −0.57% (ok) | −0.58% | +1.54% | −2.12% | +8.51% | ok / no(8) / no(6) |

(`reports/figures/fig8_berner_fair_kcurve.png`.) Conclusions, each addressing an objection:
- **Bigger k does not rescue robustness.** `G(B)` — the *only* fully real-feasible (deployable)
  robustness arm — never goes meaningfully positive: it peaks at **+0.02% at k=10** (noise) and is
  **negative again at k=15 (−2.80%) and k=20 (−0.57%)**. The apparent k=2→10 rise was a fluctuation,
  not a climb; `PoR(B)` stays positive (B is worse on train too, not collapsing to A).
- **Fairness was not the issue.** Under the fair per-station 120% inflated cap, the within-pair
  robustness `C″−D″` is **negative at every k** (−1.5% to −4.8%) — a **fourth** independent isolation
  of the enlargement effect, all negative.
- **Not a scaling artifact, and the gains are non-deployable.** The only positive columns are `oldD`
  (loose-cap slack) and the `D″` *control* — both **real-infeasible** (5–10 of 24 stations
  overloaded). Even the fair per-station scaling does not deflate cleanly (the proven `a₀`-vs-`a*`
  non-uniform-inflation misalignment), so `C″`/`D″` remain non-deployable. The deployable robustness
  arm `B` is `≤ 0` at every k.

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
