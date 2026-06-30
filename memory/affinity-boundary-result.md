---
name: affinity-boundary-result
description: Affinity-drift boundary stress-test — win-region is EMPTY; covering enlargement never pays off even on data rigged to favor it
metadata:
  type: project
---

The final lever (planted-affinity-drift boundary test, `reports/10_affinity_boundary.md`, 2026-06-25)
confirms the project's negative rigorously. Tools: `Baselines/iscf_affinity_gen.py` (planted 80
communities of 10, flat 8x100, Gini~0.73; train=sparse within-community fragments; test drift modes
`combine` [orders grow within communities = realize the closures] and `reassign` [SKUs switch
communities], alpha sweep, R=3) + `analyze_affinity_boundary.py` (total-cost-over-horizon metric).

**Metric (reviewer-demanded):** slot once on regime A, operate fraction tau under A (price
dN=n_rob-n_nom), break to B for the rest (saving dV=v_nom-v_rob). Net(alpha,tau)=(1-tau)*dV - tau*dN;
robust wins iff tau < tau*=dV/(dV+dN), needs dV>0.

**Result: win-region EMPTY.** dV is NEVER significantly positive; price dN~+0.13-0.15/order always
paid. combine: dV~-0.11 (robust WORSE — enlargement spreads the layout, hurts large orders). reassign:
dV marginal +0.007/+0.035 at alpha 0.5/1.0 but CI spans 0 (not sig). tau* <0 (combine) or ~0.03-0.12
non-sig (reassign). So Net<0 over essentially the whole (alpha,tau) plane.

**Two points that STRENGTHEN the negative:** (1) we rigged the data FOR the method (strong planted
affinity + combine drift = future exactly realizes the closures) and it STILL lost -> opposite of
circular; the theoretically-favorable regime is empirically unfavorable. (2) the mechanism is
REDUNDANT not just weak: direct min-visits already does the transitive correlation clustering the
cover provides, so the enlargement adds conservatism (real price) without adding placement info.

**FINAL project verdict:** the covering construction is provably a robust counterpart of the TRAINING
objective (Prop.1), but offers NO out-of-sample advantage over the direct solver for the CSLAP visit
objective, across every lever tried (k/K, min-max/min-sum cover, co-occurrence/demand/affinity-drift
shift, train density, data density, total-cost-over-horizon) — because the direct min-visits layout
already captures the stable correlation structure the enlargement re-encodes, at extra cost. Clean,
mechanistically-explained, publishable negative. Natural stopping point for the empirical arc.
See [[why-robustness-fails-data]], [[injected-shift-result]], [[iscf-data-is-stationary]].
