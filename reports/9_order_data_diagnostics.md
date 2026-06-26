# Report 9 — Order-data diagnostics: is the data realistic, and why does robustness fail?

**Date:** 2026-06-22. **Tool:** `Baselines/analyze_order_distributions.py` (read-only).
Universe (products) and station layout are **identical** across every scenario, so any explanation
of the robustness result must live in the **order distribution**. Figures in `reports/figures/`.

## 1. The data IS a realistic warehouse demand process

| dataset | orders | mean size | singleton % | Gini (demand) | median lift | % pairs lift>2 | % pairs lift>5 |
|---|---|---|---|---|---|---|---|
| **baseline `iscf`** | 418,849 | 2.38 | 55% | **0.771** | 0.64 | 24% | 9% |
| `iscf10kt` | 10,000 | 2.58 | 49% | 0.662 | (sample-biased) | 12% | 9% |
| `iscfco` | 15,000 | 3.44 | 20% | 0.644 | (sample-biased) | 21% | 11% |

- **Order size** (`fig1`): right-skewed, ~55% singletons, exponential-like tail — the classic
  warehouse shape. `iscfco` is the de-singletonised version (20%) we built for co-occurrence signal.
- **Product popularity** (`fig2`, `fig4`): heavy-tailed / **Pareto**, Gini **0.77** on the baseline —
  a few SKUs carry most demand, exactly the 80/20 concentration of real warehouses. The Lorenz curve
  (`fig4`) is deeply bowed. This is realistic and **well generalized** (the subsamples keep Gini ~0.65).

So on **marginal** distributions (size, popularity) the data is a faithful, realistic warehouse
process. Nothing pathological there.

## 2. The decisive diagnostic: co-occurrence is mostly a POPULARITY artifact (`fig3`)

For the 300 most-popular SKUs we computed, for every pair, the **lift** =
observed co-occurrence / expected-under-independence (`freq_a·freq_b/N`). lift≫1 ⇒ genuine product
affinity the layout can exploit; lift≈1 ⇒ the pair co-occurs only because both are popular (no real
correlation). On the baseline (the unbiased, full-data measurement):

- the lift distribution is **centered at lift≈1** (log10≈0) — the *bulk* of popular-SKU co-occurrence
  is explained by popularity alone, not affinity;
- genuine affinity is a **minority tail**: only **24%** of pairs have lift>2 and **9%** have lift>5.

(The subsample curves in `fig3` sit further right only because, over a 10–15k sample, the *observed*
top-SKU pairs are survivorship-biased toward high lift; the baseline is authoritative. `iscfco`
faithfully preserves the affinity tail — 21% lift>2, 11% lift>5.)

**This is a core reason CSLAP/covering has a weak signal here:** the "correlation structure" the
method is built to exploit is *sparse* — most of the co-occurrence a layout sees is just popular SKUs
appearing together by chance, which co-location can do little about.

## 3. Why our robustness theory does not pay off — the full critical picture

Three independent properties of the order data each suppress the robustness benefit, and together
they explain the exhaustive break-even:

1. **Affinity is sparse and weak** (§2): only ~1 in 4–10 popular pairs is genuinely affine. The
   covering enlargement groups affine products, but with a weak affinity signal there is little to
   group beyond what popularity already dictates, so the enlargement adds small value.
2. **The structure is stationary** (`reports/8`): full-data early-vs-late pair-cosine **0.85**,
   popularity Pearson **0.93**. The (sparse) affinity that exists does **not drift** between train and
   test, so the direct (k=1) layout already captures it — there is no generalization gap for the
   robust layout to close. Our injected co-occurrence shift *manufactures* novelty but **randomly**
   (curveball swaps), i.e. it moves test pairs *off* the train affinity manifold rather than
   recombining *within* it, so the closures cannot anticipate it; and it **saturates** by ρ≈2.
3. **The visit objective is demand-insensitive**: an order's visit count depends on the *co-location*
   of its products, not on how often the order arrives. So the **demand-changing shift** barely moves
   `G` (the robust layout's conservatism is a fixed cost regardless of which orders surge) — confirmed
   empirically (`iscfco`: min-sum G −13.8%→−10.6% across the whole demand-ρ range, never positive).

In short: **the data is realistic, but it is the *wrong regime* for this robustness method.** The
covering enlargement pays off only when a *stable, learnable affinity structure is under-sampled by
train and recombined within by test*. ISCF has a weak, stationary affinity and a demand-insensitive
objective — so the price of robustness consistently meets or exceeds the benefit.

## 4. What kind of data WOULD make it pay (the path, if we continue)

The missing ingredient is **coherent affinity drift** — not random co-occurrence noise, but a test
period where the *community structure itself changes*: products that were affine in the past fade and
*new* affinities emerge (e.g. seasonal market baskets — summer vs winter assortments). A robust layout
fitted to a coarse, multi-season view of affinity would then beat a layout overfit to one season,
while the direct layout would generalize worse. To test the theory in its intended regime we would
generate train/test from **two (or more) different affinity-community structures** with a controlled
overlap, rather than perturbing a single stationary structure. That is a fundamentally different
synthetic-data design from anything tested so far, and is the only remaining lever with a sound
mechanism for a *positive* result.

Figures: `reports/figures/fig1_order_size.png`, `fig2_popularity_zipf.png`,
`fig3_cooccurrence_lift.png`, `fig4_demand_lorenz.png`.
