# Scientific Audit Report — Stage 5, Iteration 2 (CSLAP Robustness via P–K Covering)

**Auditor:** Scientific Reviewer (loop iteration 2/5). **Inputs:** iteration-1 audit (`reports/5_scientific_report.md` §7 INSTRUCTIONS 1–5 + §8 BERNER addendum), method report (`reports/2_method_report.md`, eqs. 1–13, P1–P3, Prop. 1/2), coder log iteration-2 section (`reports/3_coder_log.md` §10–14), and the data files. **All statistics below were computed by the reviewer** (read-only scripts in `c:\tmp\`; no repo file modified): `stage5_iter2.py` (pooled cross-seed paired stats), `stage5_por.py` (PoR/c_bar), `berner_freelunch.py` (independent BERNER recomputation), and oracle/leakage probes. The independent recomputation **reproduced the coder's BERNER N and V_te numbers exactly**, so the result CSVs are trustworthy.

---

## A. Instruction-compliance check

| # | Iter-1 instruction | Status | Evidence |
|---|---|---|---|
| 1 | Guards: `c_bar`, `degenerate` flag, prune TRIVIAL, cite actual build | **SATISFIED** | Summary CSV carries `c_bar`+`degenerate`; 0 TRIVIAL rows remain in eval; k=4 rows flagged `degenerate=True` and excluded from genuine analysis; per-arm `c_bar` stamped (k2≈1.71–1.76, k3≈2.18–2.23). |
| 2 | Fix k=4 or substitute k=3 | **SATISFIED** | k=4 stays degenerate under HiGHS (`c_bar=1.0`, `frac_strict=0.0`) and is correctly retired; **k=3 substituted and genuinely non-degenerate** on all 3 seeds (`c_bar≈2.18–2.23`, `frac_strict≈1.0`). A second genuine k-level now exists. |
| 3 | Three train seeds {42,142,242} + pkk1 (1T) control | **SATISFIED** | `syn_50sku`, `_s142`, `_s242` each with 45 test cells; the `1T` T_s-recalibration control is present (184 eval rows, 3 summary rows on seed 42). |
| 4 | Oracle RR (eq. 12) | **SATISFIED (as a 2-cell probe)** | `results_oracle_rr.csv` present, RR computed at θ′=0.7, ρ∈{0,1.0}, seed 43, for k1/k2, all three solvers; correctly labeled "test data seen by design as normalizer only." Scope is a 4–6 cell probe, not the full grid — acknowledged by the coder. |
| 5 | Per-(seed,solver,k) paired rows for cross-seed pooling | **SATISFIED** | Eval CSV has per-cell rows enabling the pooled analysis below. (Minor: seed-42 k=1 rows are duplicated 2–3× in the eval CSV — harmless; deduplicated on (θ′,ρ,seed) before pairing.) |
| §8 | **BERNER mandatory arm**, temporal split, train seeds disjoint from {43..47} | **SATISFIED** | `berner_10w3w` arm run (k∈{1,2,3}), temporal split with disjoint train/test order IDs (verified, overlap=0, clean cut train.max<test.min), Π reconciliation performed, degeneracy guards active, GA/SA scalability honestly reported. Synthetic train seeds {42,142,242} disjoint from test range. |

**All six instructions satisfied.** The coder did the requested work and surfaced negative results rather than hiding them.

---

## B. Pooled cross-seed synthetic stats — the core of this iteration

Paired design verified: every k>1 arm shares the identical 45 (θ′,ρ,seed) test cells with its seed's k=1 arm. Gain G>0 = robust layout better on test. Per-seed Wilcoxon; pooled across the 3 seeds (135 paired diffs); Stouffer combination of per-seed signed-Wilcoxon z; binomial sign test on the 18 per-(seed,solver,k) cell means.

**Per-seed paired gain (mean G%, Wilcoxon p):**

| solver | k | s42 | s142 | s242 | sign pattern |
|---|---|---|---|---|---|
| heuristic | 2 | **+0.54** (p=0.034) | **−0.69** (p=0.030) | +0.23 (ns) | + / − / + |
| heuristic | 3 | −0.24 (ns) | −0.34 (ns) | +0.04 (ns) | − / − / + |
| sa | 2 | **+0.85** (p=0.0002) | −0.89 (p=0.064) | −0.04 (ns) | + / − / − |
| sa | 3 | +0.17 (ns) | +0.14 (ns) | **+0.43** (p=0.049) | + / + / + |
| ga | 2 | **+1.48** (p<0.0001) | +0.04 (ns) | +0.21 (ns) | + / + / + |
| ga | 3 | +0.21 (p=0.059) | −0.53 (p=0.054) | −0.79 (p=0.060) | + / − / − |

**Pooled (135 diffs) + combined tests:**

| solver | k | mean G% | 95% CI | sign(42/142/242) | pooled Wilcoxon | Stouffer z (p) |
|---|---|---|---|---|---|---|
| heuristic | 2 | +0.03 | [−0.29, +0.35] | + / − / + | 0.479 | +0.58 (0.565) |
| heuristic | 3 | −0.18 | [−0.46, +0.10] | − / − / + | 0.186 | −0.70 (0.484) |
| sa | 2 | −0.03 | [−0.38, +0.33] | + / − / − | 0.144 | +0.70 (0.486) |
| sa | 3 | +0.25 | [−0.15, +0.64] | + / + / + | 0.238 | +1.36 (0.173) |
| **ga** | **2** | **+0.58** | **[+0.18, +0.98]** | **+ / + / +** | **0.0030** | **+2.98 (0.003)** |
| ga | 3 | −0.37 | [−0.75, +0.01] | + / − / − | 0.117 | −1.10 (0.270) |

Binomial sign test on 18 cells: 11/18 positive, **p=0.48 (no global directional signal)**.

**KEY QUESTION — does the iter-1 k=2 signal replicate? VERDICT: NO, with one exception.** The iter-1 finding rested entirely on seed 42, where all three solvers showed significant positive G at k=2 (h +0.54, sa +0.85, ga +1.48). On the two new seeds the effect **largely collapses or flips**: heuristic k=2 goes significantly *negative* on s142 (−0.69, p=0.03); sa k=2 is negative on s142 and s242. Pooled across seeds, **only GA at k=2 survives** — sign-stable +/+/+ across all three seeds, pooled Wilcoxon p=0.003, Stouffer p=0.003, CI excluding zero. **The seed-42 across-solver result was substantially a single-draw artifact; GA-k2 is the one finding that genuinely replicates.** The price side (PoR) is, by contrast, **rock-solid: 18/18 genuine cells have PoR>0** (range +0.05% to +6.96%), roughly monotone in k — the nominal price of robustness is real and stable; only the test-side payoff is unstable.

---

## C. k=3 arm and the tradeoff-curve shape

k=3 is now genuinely non-degenerate (`c_bar≈2.18–2.23` vs k=2's ≈1.75), so for the first time a two-point curve in realized enlargement exists.

- **P1 (PoR increasing in k):** Directionally supported on the price axis: PoR generally rises k2→k3 (heuristic s42 +0.16%→+3.02%; sa all seeds rise; ga mixed). The "bias monotone in closure size" prediction (method §D) is **consistent with the data** now that a second genuine k exists.
- **D's U-shape (G increasing then decreasing in k):** **No support.** k2→k3 does *not* improve G; in most cells G is flat or worsens (pooled: h +0.03→−0.18; ga +0.58→−0.37). k=3 is past the useful point — more conservatism, no extra out-of-sample payoff. The U-shape's *right arm* (over-conservatism hurting) is weakly visible; the *left arm* (a genuine interior optimum beating k=1) is not established because k=2 itself is unstable.
- **Net:** a real two-point curve (PoR↑, G→flat/down), a publishable shape statement — "increasing nominal price with no commensurate out-of-sample gain beyond k=2 on synthetics" — but it does **not** confirm the predicted interior optimum.

---

## D. Oracle regret (eq. 12)

RR = (V_te(layout) − V_te(oracle))/V_te(oracle), oracle = test-reoptimized layout. Regret modest throughout (RR ∈ −0.03…+0.24). k=2 vs k=1:

| | ρ=0 (sampling noise only) | ρ=1.0 (full correlation replacement) |
|---|---|---|
| k=2 beats k=1 | 1 of 3 solvers (sa only) | 2 of 3 solvers (heuristic, sa) |

**Interpretation:** consistent with the H1 *mechanism* — the robust layout's advantage over k=1 (relative to the achievable oracle) emerges preferentially at the *maximum* shift ρ=1.0 (heuristic flips from worse at ρ=0 to better at ρ=1.0; sa better at both, more so at ρ=1.0). GA is worse at both cells here (single-seed 2-cell probe, partly contradicts GA's pooled multi-cell win — underpowered). The oracle probe **weakly corroborates "gain concentrated under large shift"** but cannot carry weight: 4–6 cells, one test seed, no replication.

---

## E. BERNER industrial adjudication

### E.1 Free-lunch signature — VERDICT: BENIGN ARTIFACT OF HEURISTIC SUBOPTIMALITY, **not** a leak or bug.

Summary BERNER heuristic: k=2 PoR=−0.92%, G=+0.32%; k=3 PoR=−2.45%, G=+1.98% — negative PoR with positive G, the classic free-lunch signature the brief flags. Discriminating checks confirm it is **benign.**

Independent recomputation of every heuristic layout on every relevant order set:

| layout | real_train (=N, the PoR base) | pkk2 objective | pkk3 objective | test (=V_te) |
|---|---|---|---|---|
| k1 (nominal) | 578111 | 684550 | 760992 | 164140 |
| k2 (robust) | **572765** | **597776** | 715591 | **163607** |
| k3 (robust) | **563947** | 625271 | **586900** | **160888** |

Recomputed real_train and test columns **match the CSV to the unit** — no fabrication.

Mechanism, precisely:
1. **The robust layouts genuinely minimize their own enlarged objective** (pkk2: k1=684550 → k2=597776; pkk3: k1=760992 → k3=586900). The transform did its job.
2. **The k1 nominal layout is NOT the true CSLAP optimum.** It is a greedy-clustering heuristic solution — provably suboptimal. The enlarged instance gives the same greedy a denser co-occurrence signal, steering it to a layout better on the *real* objective too (572765 < 578111).
3. **No contradiction with Prop. 1's PoR≥0.** Eqs. (3)/(5) guarantee N(a_k) ≥ N(a_0) **only at optimality**. The heuristic is not an optimizer; a better-guided suboptimal a_k can beat a worse-guided suboptimal a_0 on the real objective. This is exactly the "enlargement guiding a suboptimal solver" case the method report anticipated (§A.3 point 4).

**Leak ruled out independently:** train/test order-ID sets disjoint (overlap=0), clean temporal cut (train max 8076655551 < test min 8076655553), construction draws from exactly the 219121 train orders and zero test orders, products/stations frozen from train, κ identical (0.9891) across arms. **Not a leak. Not a bug. Benign.**

### E.2 Π reconciliation — VERDICT: DOCUMENTABLE LIMITATION, **not** REVISE_METHOD.

Stored `pi_star`=34 (k2) was the bottleneck over the *subsampled* support set the CG master saw (U7); true global bottleneck over all 142,241 distinct train supports is **Π_true=369** (k2) / 360 (k3). The coder relabeled it `pi_constrained`, recomputed Π_true, re-verified the partition is valid on the full stream, patched the meta JSONs.

- **Core formulation intact.** Prop. 1 (robust-counterpart *identity*, eq. 5) depends only on monotonicity of v(a,·) and closures over all orders — both hold (max|closure|=429 ≤ Π_true·k=738). Transform, enlargement, partition all valid.
- **Only Prop. 2's optimality claim weakens.** "min-max-Π minimizes the *global* worst-case bottleneck" is now true only over the subsample. Realized global bound is v(a,u)≤369, not ≤34. The construction is a **valid but not provably min-max-optimal** cover.
- **Limitation, not broken framework.** H1's empirical content (does enlargement buy out-of-sample robustness?) is unaffected. **Not REVISE_METHOD.** Writer must report Π_true alongside Π_constrained and state Prop. 2's bound is conditional on full-stream Π.

### E.3 Single test cell, GA degenerate, SA unscalable — the evidence is narrow.

- **n_test_cells=1.** One real late temporal window. **No CI, no significance** for BERNER G. +0.32%/+1.98% are point estimates on a single split.
- **GA degenerate:** byte-identical layout across all three arms (md5 `8ea2c967f423`), GA reaches only generation ~2 in 120s. **Zero arm differentiation.**
- **SA unscalable:** completed only k=1 (~1 cooling step, 1219s); k2/k3 skipped (~19 min/temp-step). **No SA signal on enlarged arms.**
- **Consequence:** BERNER's entire H1 signal rests on **one solver (heuristic) on one temporal split.** Heuristic layouts *are* genuinely distinct (12341/13363 of 21316 products relocated) — signal is real but a single point.
- **κ=0.989** (3844 unseen test lines of 353,999) is **acceptable** — unseen SKUs excluded identically across layouts; wl_broken=1, cap_broken=0 identical across arms (no hidden feasibility price).

---

## F. Honesty / overclaim ruling

Coder's iteration-2 verdict: *"H1 holds on industrial data, more cleanly than on the synthetics … Pareto-dominates the nominal layout."*

**Ruling: OVERCLAIM as headline framing, though every individual number is honestly reported.**
1. "Pareto-dominates" is true for the heuristic on one split; generalizing to "holds on industrial data" overweights n=1 cell, one solver, GA showing nothing, SA absent on enlarged arms.
2. "More cleanly than the synthetics" inverts the epistemics: synthetics have multi-cell replication across 3 seeds and show k=2 is unstable; BERNER looks cleaner *precisely because it has no dispersion to expose instability*. A single point with no error bar is not "cleaner" than a replicated study.
3. The negative-PoR Pareto improvement is real but is a property of *heuristic suboptimality* (E.1), not the robust method dominating in general.

To the coder's credit, §14 *does* carry all three caveats; only the headline sentence is too strong.

**Strongest honest claim BERNER supports:** *On a single real industrial temporal hold-out (BERNER, 219k train / 66k test orders, 21k SKUs), the P–K enlarged covering layout produced by the greedy clustering heuristic (the only solver that scaled and differentiated) reduced both training visits and out-of-sample test visits relative to the nominal heuristic layout (k=2: −0.9% train, +0.3% test; k=3: −2.5% train, +2.0% test). Because the heuristic is not an optimizer, the simultaneous nominal improvement is consistent with the enlarged objective guiding the greedy to a better real-objective layout (no contradiction with Prop. 1, which guarantees a nominal price only at optimality), and is not a free lunch in the leakage sense — leakage is ruled out (disjoint temporal split, construction touches train only). This is a single uncorroborated cell with no confidence interval; SA did not scale and GA did not differentiate at this scale.*

---

## G. Overall verdict and the writable envelope

The framework is sound (no REVISE_METHOD: Π-subsampling weakens only Prop. 2's *optimality* claim — documentable; Prop. 1's identity and the transform are intact). The code did everything instructed and surfaced its negative results. The evidence is **rich enough to write an honest, hedged, conditional paper** — a falsified-as-headline-but-conditionally-supported result is publishable when reported as such:

- **A genuine, replicated positive:** GA-k2 gain, sign-stable across 3 seeds, pooled p=0.003.
- **A clean negative-results story:** seed-42 cross-solver k=2 signal does NOT replicate; no global directional effect (11/18, p=0.48); predicted U-shape absent.
- **A stable price axis:** PoR>0 in 18/18 cells.
- **A narrow but mechanistically-explained industrial result:** BERNER heuristic Pareto improvement, free-lunch diagnosed as benign suboptimality, leakage excluded.
- **Documented limitations:** Π_constrained vs Π_true (Prop. 2 conditional); single BERNER cell, no CI; SA unscalable, GA degenerate at scale; HiGHS construction ceiling; T_s side-channel (1T control shows recalibration alone moves heuristic nominal cost −3.16%).

A third coder loop is **not justified**: the instability is a property of the data/method at this scale, not a fixable bug; the honest finding is complete and writable. Forcing a cleaner result would risk manufacturing one. Advance to the Writer with a strict honesty envelope.

```yaml
STATUS: ACCEPTED
ITERATION: 2
REASON: All iter-1 instructions + BERNER addendum satisfied; framework sound (Pi-subsampling weakens only Prop.2 optimality, documentable); evidence supports an honestly-hedged, partly-falsified, conditionally-supported finding that is publishable as-is. BERNER free-lunch proven benign (heuristic suboptimality, leakage excluded by independent recomputation).
INSTRUCTIONS: >
  Advance to Stage 6 (Academic Writer), MANDATORY processing through skills/humanizer-writer/SKILL.md.
  WRITABLE CLAIMS (do not exceed):
  (1) Frame H1 as CONDITIONALLY SUPPORTED / SOLVER- AND SEED-DEPENDENT, not confirmed. The price of robustness (PoR>0) is stable (18/18 synthetic cells); the out-of-sample gain G is NOT.
  (2) The ONLY replicated synthetic positive is GA at k=2: sign-stable across seeds {42,142,242}, pooled Wilcoxon p=0.003, Stouffer p=0.003, mean G=+0.58% [+0.18,+0.98]. Report it as the one robust synthetic effect.
  (3) Report the NEGATIVE RESULT explicitly and as a contribution: the iter-1 seed-42 cross-solver k=2 gain did NOT replicate (heuristic flips to -0.69% p=0.03 on s142; sa flips negative); no global directional effect (11/18 cells positive, sign-test p=0.48); the predicted U-shape in k is absent (k=3 adds nominal price with no commensurate gain).
  (4) BERNER: report ONLY the heuristic result, as a single uncorroborated temporal cell with NO confidence interval. State plainly that SA did not scale (skipped on enlarged arms) and GA returned a byte-identical non-differentiating layout, so the industrial signal is one-solver/one-cell. Use the strongest-honest-claim wording from audit section F.
  (5) The BERNER negative-PoR Pareto improvement MUST be explained as benign heuristic suboptimality (enlarged objective guides the greedy to a better real-objective layout), explicitly reconciled with Prop. 1 (nominal price guaranteed only at optimality), and accompanied by the leakage-exclusion evidence (disjoint temporal order-ID split, construction touches train only). Do NOT present it as the method dominating "for free."
  MANDATORY LIMITATIONS SECTION must include: (a) Pi_constrained (34/23) vs Pi_true_full_stream (369/360) — Prop. 2's worst-case bound is conditional on full-stream Pi and the subsampled construction does NOT certify global min-max optimality; (b) no exact solver ran (Gurobi absent, HiGHS construction ceiling, Pi*=6 acceptance not reproduced); (c) the T_s recalibration side-channel confound — cite the 1T control (heuristic PoR=-3.16%, G=-0.30% from recalibration ALONE), so PoR/G mix enlargement with capacity recalibration; (d) single BERNER cell, SA unscalable, GA degenerate; (e) oracle RR is a 2-cell probe only. Parameterize tradeoff figures by realized c_bar (k2~1.75, k3~2.2), not nominal k.
```
