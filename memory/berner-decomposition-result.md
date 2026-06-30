---
name: berner-decomposition-result
description: BERNER preprocess-vs-capacity decomposition — the v2 BERNER "win" was the capacity side-channel, NOT the outer-approximation
metadata:
  type: project
---

The last open confound, closed (`reports/11_berner_decomposition.md`, 2026-06-25). BERNER (Company B)
was the ONLY instance where a positive out-of-sample gain ever appeared (v2: heuristic G=+0.3%@k2,
+2.0%@k3), but it changed two things at once: covering enlargement (closures) AND a looser time-cap
(robust arm rebuilt T_s from inflated closure line counts, eq.10 of pk_instance_robust).

**Tools:** `Baselines/berner_adapter.py` (rebuild BERNER as clean kappa-invariant top-2000 instance:
175419 train / 49748 test, real 24-station layout, REAL_LINES workload, manifest); min-sum CPLEX
covers k=2,3,4,6,10 (all optimal, c_bar 1.49->3.02); `Baselines/berner_decompose.py` (4-arm 2x2:
{nominal|closures} x {real cap|recal cap}, SAME Hexaly placement, visits on SAME real test orders;
recalibration uses partition fast-path bar_L_p = pattern popularity). Raw CSV path is
`../Heuristic_Connex_Set_Project/data/BERNER_ORDER_LINES_09-12.csv` (relative to Baselines).

**Result (G vs baseline A, all arms feasible cap/wl_broken=0):**
- A=nominal/realcap, B=closures/realcap (PREPROCESS-ONLY), C=closures/loosecap (v2 arm), D=nominal/loosecap (CAP-ONLY).
- G(B) preproc-only: -3.41,-3.65,-2.15,-0.93,+0.13 % (k=2..10) -> NEGATIVE to break-even; preprocess alone HURTS.
- G(D) cap-only (zero enlargement): +0.09,+3.37,+4.79,+5.41,+7.97 % -> the WHOLE gain, and MORE than G(C).
- G(C) v2-full: -3.11,-0.28,+2.05,+3.17,+4.56 % -> reproduces v2 positive but G(C)<G(D): closures DRAG ~3%.
- PoR(D)<0 (D cheaper on train too: -0.78..-8.54): original cap T_s=7 was BINDING; recalibration just
  RELAXED a binding constraint (T_s 7->32..65) -> a constraint relaxation, not robustness.

**Faithful robust arm (C'/D', `berner_decompose_cprime.py`, 2026-06-28):** reviewer flagged old arm C
(closures + REAL workload + loose cap) as a hybrid that went artificially slack ~ D. Faithful arm
C'=closures + bar_L (closure) workload + loose cap (=solve transformed instance self-consistently);
D'=nominal + bar_L + loose cap. Result: G(C') STRONGLY NEGATIVE every k (-5.7 to -8.3%); G(D') also neg
(-4 to -5.5%); C'-D' <=0 every k (-1.7 to -2.8%) = THIRD independent isolation showing enlargement
costs ~2-3.5% in ANY workload regime (after B-A and oldC-oldD). REAL-feasibility (vs real L_p/T_s):
C'/D' layouts overload 6-9 of 24 stations by up to 5.5x -> NON-DEPLOYABLE. By construction old G(D)
"+8%" layout (loose cap) also violates real T_s (old cap_broken=0 was a station-id TYPE BUG). Only A
and B respect real T_s, and there G(B)<=0. So the only positive arm was real-demand-under-a-cap-sized-
for-fictional-demand (free headroom), non-deployable; self-consistent honest version goes negative.

**Fair per-station 120% caps + bigger k (`berner_clean_comparison.py`, 2026-06-29):** addressed two
fairness objections. (i) A/B used per-station 120% but inflated arms used eq.10 flat-110%-of-mean
(BERNER very non-flat, real T_s 7..148); rebuilt inflated arms at per-station fair cap T_s^fair =
ceil(1.20*sum_{p pinned to s} bar_L_p/V_s) using saved a0 (PINNED_STATION col added to berner_adapter).
(ii) extended G(B) to k=15,20 (c_bar to 4.17). Result table (G vs A, all 120%): G(B) deployable
robustness = -3.33,-3.24,-2.18,-0.94,+0.02,-2.80,-0.57% (k=2..20) -> NEVER meaningfully positive; the
k=10 +0.02% is noise, k=15/20 negative again (the earlier "monotonic rise to k=10" was a fluctuation,
not a climb; PoR(B)>0 so B not collapsing to A). Fair within-pair robustness C"-D" NEGATIVE every k
(-1.5 to -4.8%) = 4th independent isolation. Only positives = oldD slack + D" control, BOTH
real-infeasible (5-10 of 24 stations overloaded): even fair per-station scaling does not deflate
cleanly (proven a0-vs-a* non-uniform-inflation misalignment). B is the ONLY deployable robustness arm
and it's <=0 at every k. Fig: reports/figures/fig8_berner_fair_kcurve.png.

**Verdict:** BERNER "win" = workload-capacity side-channel (free headroom, non-deployable), NOT the
set-cover outer-approximation. Enlargement's own out-of-sample effect is NEGATIVE in all FOUR regimes
(real/real, real/loose, inflated/loose, inflated/fair-120%) and at every k up to 20. Deployable
robustness (arm B) never positive. Escalation rule (re-run full 21k iff G(B)>0) NOT met; no escalation.
Now both real industrial instances (ISCF + BERNER) give a clean negative under kappa-invariant
capacity. Project's last confound closed; empirical arc COMPLETE. Confirms user's exact suspicion.
See [[affinity-boundary-result]], [[why-robustness-fails-data]], [[iscf-kfold-result]],
[[placement-solver-hexaly-only]].
