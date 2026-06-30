# Memory Index

- [Placement solver: Hexaly only](placement-solver-hexaly-only.md) — assignment MILP runs only via milp_synthetic.py, not Gurobi/CPLEX/GA/SA
- [CPLEX phase overview](plan-cplex-phase-overview.md) — H1 revalidation state: two venvs, ISCF facts, Phase A/B done (Pi*=6), scale caveats
- [ISCF K-fold result](iscf-kfold-result.md) — PRIMARY finding: i.i.d. K-fold cleanly falsifies H1 at k=2 (PoR +6.8%, G −6.8%, both CIs exclude 0, feasible)
- [Temporal split preferred](temporal-split-preferred.md) — use ONLY temporal cut (order by ORDER_ID, hide latest IDs as test), not random K-fold
- [iscf10k subsample](iscf10k-subsample.md) — 10k-order down-sample (all 4328 products) via iscf_subsample.py for tractable temporal higher-k runs
- [ISCF data is stationary](iscf-data-is-stationary.md) — full data early/late pair-cosine 0.85: no real shift → explains G≤0; data unsuitable for showing robustness benefit; need injected shift or BERNER
- [Injected-shift result](injected-shift-result.md) — curveball shift confirms mechanism but net gain = break-even, OBJECTIVE-INVARIANT (min-sum==min-max); remaining lever = demand-shift
- [iscfco dataset](iscfco-dataset.md) — co-occurrence-rich testbed (1600 SKUs, 15k orders, 20% singletons, median co-occ 13) for the demand-shift round
- [Why robustness fails (data)](why-robustness-fails-data.md) — data realistic (Pareto Gini 0.77) but WRONG regime: sparse+stationary affinity (lift~1), demand-insensitive objective; path = coherent affinity drift
- [Affinity boundary result](affinity-boundary-result.md) — planted-affinity-drift boundary test, win-region EMPTY; rigged data FOR method, still lost; enlargement redundant vs direct min-visits clustering
- [BERNER decomposition result](berner-decomposition-result.md) — FINAL confound closed: v2 BERNER "win" was the capacity side-channel (G(D) cap-only +8%), NOT outer-approximation (G(B) preproc-only ≤0); both real instances now clean-negative
