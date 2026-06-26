# Report 10 — Affinity-drift boundary stress-test (does the insurance ever pay off?)

**Date:** 2026-06-25. **Tools:** `Baselines/iscf_affinity_gen.py` (planted-affinity generator),
`run_robustness_iscf.py` (build-covers `--objective minsum --k 10`, place, evaluate),
`Baselines/analyze_affinity_boundary.py`. Figures in `reports/figures/`.

## Why this experiment

After exhaustive empirical break-even, we pivoted to **boundary testing**: build controlled data
with explicit, *strong* affinity communities and a tunable, unforeseeable structural break, and find
the parameterized conditions (if any) under which the covering enlargement's "insurance" pays off
**over the operating horizon** — not merely survives the shift. Per external review, we (1)
parameterize the break (`alpha`) and map the threshold rather than asserting "it works", (2) frame
the break as an unpredictable structural change, and (3) use a **total-cost-over-horizon** metric.

**Setup.** 800 SKUs in 80 planted communities of 10 (flat 8×100 layout, demand Gini≈0.73, Zipf
popularity). Train (regime A) = sparse within-community fragments. Test (regime B), two drift modes ×
`alpha ∈ {0,0.5,1}` × 3 replicates: `combine` (future orders *grow within the same communities* —
realizing the closures of the train fragments; the regime *theoretically most favorable* to the
method) and `reassign` (a fraction `alpha` of SKUs switch communities — the contrast). Robust =
min-sum cover, K=10 (c̄≈4.0), placed by the unchanged Hexaly model; nominal = direct k=1.

## The total-cost-over-horizon metric

Slot once on regime A, operate for a fraction `tau` under A (price `dN = n_rob−n_nom`), then break to
B for the rest (saving `dV = v_nom−v_rob`). `Net(alpha,tau) = (1−tau)·dV − tau·dN`; robust pays off
iff `tau < tau*(alpha) = dV/(dV+dN)` (needs `dV>0`).

## Result — the win-region is empty

| mode | alpha | price dN/order | **saving dV/order [95% CI]** | tau*(alpha) | robust wins? |
|---|---|---|---|---|---|
| combine | 0.0 | +0.131 | **−0.110** [−0.358,+0.139] | <0 | no |
| combine | 0.5 | +0.135 | **−0.105** [−0.339,+0.129] | <0 | no |
| combine | 1.0 | +0.152 | **−0.111** [−0.356,+0.134] | <0 | no |
| reassign | 0.0 | +0.155 | −0.120 [−0.379,+0.138] | <0 | no |
| reassign | 0.5 | +0.154 | +0.007 [−0.026,+0.040] | 0.03 | not sig. |
| reassign | 1.0 | +0.152 | +0.035 [−0.092,+0.162] | 0.12 | not sig. |

(`fig5_affinity_dV.png`, `fig6_winregion_combine.png`, `fig6_winregion_reassign.png`.)

**The out-of-sample saving `dV` is never significantly positive**, while the price `dN ≈ +0.13–0.15`
per order is always paid. So `Net(alpha,tau) < 0` for essentially the whole `(alpha, tau)` plane (the
win-region heatmaps are red): over any operating horizon with `tau>0`, the robust layout's insurance
**does not pay off**. `tau*` is negative under `combine` and a non-significant ~0.03–0.12 under
`reassign`.

## Two findings that strengthen, not weaken, the negative

1. **We rigged the data *for* the method and it still lost — the opposite of circular.** The
   `combine` regime is the textbook best case (strong planted affinity + future orders that *exactly
   realize the closures* the construction builds). Yet `dV<0` there — robust is actually **worse** on
   the combined future. The reason: the enlargement makes the layout *more spread* (broader groups
   distributed across stations), which is penalised precisely when future orders grow large. So the
   theoretically-favorable regime is empirically *unfavorable*.
2. **The mechanism is redundant, not just weak.** Both layouts optimise visits on the same fragments,
   and direct min-visits already performs the transitive correlation clustering the cover provides —
   so the enlargement adds conservatism (a real price) without adding placement information. This is
   why the result is break-even-or-worse across *every* lever tried in the whole project.

## Verdict

Under a rigorous, parameterized, total-cost-over-horizon test — on data deliberately constructed to
favour the method — the covering-enlargement robust counterpart **does not pay off out of sample for
the CSLAP visit objective**. The win-region is empty. Combined with `reports/9` (the real data is the
wrong regime) this is a complete, mechanistically-explained result: *the construction is provably a
robust counterpart of the **training** objective, but offers no out-of-sample advantage over the
direct solver, because the direct min-visits layout already captures the stable correlation structure
that the enlargement re-encodes — at extra cost.* This is a clean, publishable boundary/negative
finding, and the natural stopping point for the empirical arc.
