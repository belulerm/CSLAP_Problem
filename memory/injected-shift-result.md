---
name: injected-shift-result
description: Under injected co-occurrence shift, the robustness MECHANISM is confirmed (robust layouts degrade slower); net gain reaches break-even at low k, not a significant win
metadata:
  type: project
---

Because ISCF is stationary ([[iscf-data-is-stationary]]), we inject controlled co-occurrence shift via
`Baselines/iscf_shift_inject.py` — **degree-preserving (curveball) swaps** that conserve every
product's demand L_p and every order's size (so the flat layout/workload stays valid; cap_broken=0,
wl_broken flat throughout — no workload confound). Two modes: **structured** (swaps within affinity
communities detected from train; H1's fair regime) and **unstructured** (global). Knob rho = swaps /
test-incidences. Eval via `run_robustness_iscf.py evaluate-shift` on the existing iscf10kt layouts.

**Result (2026-06-21):** the robustness MECHANISM is confirmed. Test-visit degradation from rho=0→2
falls monotonically with k (k=1 +29%, k=2 +27%, k=4 +23%, k=6 +16%) — more enlargement = more stable
under shift. Gain G(k,rho) improves monotonically toward 0 as rho rises, in BOTH modes:
- k=2: G goes -1.7% (rho0) → ~-0.4% structured / +0.5% unstructured (rho2) — break-even, CI incl 0.
- k=3: -3.2%* → ~-0.3%/-0.2%. k=4: -6.5%* → -1.9%/-0.1%. k=6: -15%* → -4.7%*/-1.8%* (still neg).
(* CI excludes 0.) PoR fixed (train): k2 +3%, k3 +3.2%, k4 +6.9%, k6 +12.8%.

**Reading:** the enlargement genuinely protects against co-occurrence shift (robust degrades slower),
and the benefit scales with shift severity — but on this DENSE-train data the benefit only MATCHES the
price (break-even at low k=2; never a statistically significant positive gain). Stronger enlargement
(k=6) is over-conservative (price too high). The interior optimum is at LOW k, now visible. Honest
status: NOT a flat negative anymore — "mechanism works, margin ~zero here."

**Sparse-train sweep (DONE 2026-06-21) — hypothesis REFUTED.** Tested train caps {500,1000,2000} vs
dense(5-9k) via `make-folds --train-cap` + same shift sweep (`run_robustness_iscf.py evaluate-shift`,
reusing the shift sets since test is identical across caps). Sparse train did NOT make robust win; it
made it WORSE and noisier. G at rho=2 (structured), k=3: dense −0.3%, cap2000 +0.07%, cap1000 −1.3%,
cap500 −3.1% — best is dense/2000 (≈break-even), degrading as train shrinks. Reason: sparse train
also starves the COVER (closures shrink, c_bar→~1.1) so robust≈nominal, plus high variance (wide CIs).
**No configuration anywhere (4 caps × k{2,3,4,6} × 2 modes × rho grid) gives a statistically
significant POSITIVE G** — every cell is ns(~0) except the significant-NEGATIVE dense k=6
(over-conservative). (Sparse-train side note: wl_broken jumps to ~38/40 because T_s from sparse train
is too tight for the full test — slots fine cap_broken=0, equal across arms, visit comparison valid.)

**Cover-objective redesign (min-sum vs min-max, DONE 2026-06-22).** Added `--objective {minmax,minsum}`
to `pk_cover_construction.py` (min-sum minimises total pattern-order hits via column obj-coef c_q,
drops the Pi bottleneck rows, reuses the pricing with beta=-1; cplex only). Validated: min-sum gives
fewer, LARGER sets and lower total-hits, and crucially scales to big closures where min-max degenerates
(full-train iscf10kt K=10: min-sum c_bar~3.07 with size-10 sets, vs min-max c_bar~1.0 mostly singletons).
Cover composition (num_patterns + pattern-size histogram) now saved per cover JSON + `cover_composition.csv`.
**Head-to-head G (full-train 50/50..90/10 temporal, structured+unstructured shift to rho=4):** NEITHER
objective crosses to a significant positive G. Both reach ~break-even at high shift (unstructured rho=4:
min-sum K6 G=-0.01% [-2.7,+2.7], min-max K6 -0.68%; structured rho=4 both ~-2 to -4%, mostly ns). min-sum
is NOT better than min-max; differences are within noise. **The break-even is OBJECTIVE-INVARIANT.**

**Demand-shift round (DONE 2026-06-22, on iscfco dense data [[iscfco-dataset]]).** Built
`iscf_demand_shift.py` (popularity drift = weight-proportional resample of test orders toward a
log-normal per-product drift; order compositions stay real, L_p shifts) + the user's flat-workload
safeguard (dummy LPT assignment -> set all stations T_s = ceil(slack*max-station-workload)).
`evaluate-shift --mode demand` now reads the shift-set stations (safeguard T_s). Verified drift:
L_p Pearson 0.997 (rho0) -> 0.54-0.79 (rho2); safeguard kept feasibility (wl_broken bounded,
cap_broken=0). **Result: demand shift does NOT help.** min-sum k10 (c_bar 3.34) G stays strongly
negative (-13.8% rho0 -> -10.6% rho2, CI excludes 0); min-max k10 degenerate (~nominal) G~-3% ns.
Demand shift barely moves G because the CSLAP VISIT objective depends on co-location of co-occurring
products, not on demand frequency -- resampling order *frequencies* doesn't change the co-occurrence
structure the layout must handle, so the robust layout's conservatism is a fixed cost regardless.

Also note: at K=10 on dense iscfco, **min-max DEGENERATES** (4/5 folds c_bar~1.0, can't minimise the
big bottleneck Pi~118 in time) while **min-sum builds c_bar~3.34 certified-optimal** -- min-sum is the
only construction that scales to large covers. But bigger enlargement = bigger price (+14% PoR) and
bigger loss on the (stationary) natural test (-13.8%).

**FINAL verdict of the whole arc:** the covering-enlargement robustness MECHANISM is real and
confirmed (robust layouts degrade slower under injected shift; G improves monotonically with rho), but
on this flat-layout ISCF data the benefit only ever reaches **break-even** and is NEVER a statistically
significant net gain, robust across EVERY lever tried: k/K grid, min-max vs min-sum cover objective,
structured vs unstructured shift, shift magnitude rho<=4, and train density. The price of robustness ≈
the benefit here. Remaining untried lever (user's deferred round): **demand-changing shift** (curveball
swaps preserved demand; the natural demand drift is modest-but-real per `reports/8_drift_characteristics.md`)
with the dummy-assignment flat-workload safeguard. Also untried: redundant-cover (>=1) variant.
Artifacts: `iscf10kt_results_{mm,ms}/summary_shift_*.csv`, `iscf10kt_covers_{mm,ms}/cover_composition.csv`,
`reports/8_drift_characteristics.md`. See [[temporal-split-preferred]], [[iscf-data-is-stationary]].
