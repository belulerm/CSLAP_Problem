# Method Selection Report — CSLAP Robustness via P–K Covering Construction

**Pipeline Stage 2 (Method Selector). Input: `reports/0_research_brief.md`, `reports/1_research_report.md`, manuscript `Computers_and_Operations_Research_manuscript.tex`, P–K notebooks (ground truth), `milp_gurobi_synthetic.py`, `.claude/rules/code-standards.md`. Date: 2026-06-11.**

**Notation policy.** All symbols follow the manuscript's Table of Notations: $P, O, S$ (products, orders, stations), $P_o$ (product set of order $o$), $\zeta_s$ (slot capacity), $L_p$ (daily pick-lines), $V_s$ (speed), $T_s$ (time capacity), $x_{ps}, z_{os}$ (decision variables of eqs. \eqref{obj}, \eqref{con14}–\eqref{con17}). Because the manuscript reserves $P$ for the product set, the P–K code's objective value "P" (max cover size) is renamed $\Pi$ throughout; patterns are $q \in Q$ (the manuscript's $K_s$ denotes station-assignment patterns in the CG solver — a different object; no collision). The P–K code's $k$ (max pattern size) is kept as $k$; note the manuscript's §"Limited Product Reassignment" uses $k$ for a relocation cap — the Academic Writer must disambiguate (recommend renaming the relocation cap there, or using $\kappa$ for pattern size in the article).

---

## A. Committed answers to the five definitional tasks (binding)

### A.1 — What the enlarged sets approximate

**Commitment:** The enlarged sets approximate **the support of the future order distribution**, encoded as a **data-driven, combinatorial uncertainty set of order compositions** (Stage-1 framing (c), adopted). Precisely: let $\mathcal{O}^{tr} = \{P_o : o \in O^{tr}\}$ be the family of observed (training) order product-sets over universe $P$. The P–K construction selects a pattern family $Q^\* = \{q_1,\dots,q_m\}$, $q_j \subseteq P$, $|q_j| \le k$, partitioning $P$ (exact variant), with achieved overlap bound $\Pi^\* = \max_{o \in O^{tr}} |\{q \in Q^\* : q \cap P_o \neq \emptyset\}|$. The induced uncertainty set is

$$\widehat{\mathcal{U}}_{k} \;=\; \Big\{\, u \subseteq P \;:\; \exists\, R \subseteq Q^\*,\ |R| \le \Pi^\*,\ u \subseteq \textstyle\bigcup_{q \in R} q \,\Big\} \tag{1}$$

— the set of all order compositions expressible within at most $\Pi^\*$ patterns of the learned partition. The enlarged sets are its per-order generators: for each training order $o$, the **cover** and **pattern-closure** are

$$Q(o) = \{q \in Q^\* : q \cap P_o \neq \emptyset\}, \qquad \bar{P}_o = \bigcup_{q \in Q(o)} q. \tag{2}$$

**Justification.** This is the only one of the three Stage-1 candidate objects (support / correlation structure / uncertainty set) under which "approximation," "inner/outer," and "robustness" all acquire exact meanings (see A.2). The patterns are not estimates of a correlation matrix and carry no probability weights, so framings (a)-distributional and (b)-structural are formally inapplicable, as Stage 1 already argued.

### A.2 — Outer approximation: exact senses and proof sketch

**Commitment:** Under the object fixed in A.1, the construction is an **outer approximation**, in three exact and provable senses. It is **not** an approximation of a probability distribution in any inner/outer sense, and we will not claim that.

**(i) Per-order set inclusion.** For every training order $o$: $P_o \subseteq \bar{P}_o$.
*Proof.* $Q^\*$ covers $P$ (master constraint $\sum_{q \ni p} x_q = 1\ \forall p$), so every $p \in P_o$ lies in some $q \ni p$; that $q$ satisfies $q \cap P_o \supseteq \{p\} \neq \emptyset$, hence $q \in Q(o)$ and $p \in \bar{P}_o$. $\square$

**(ii) Support inclusion (region containment).** $\operatorname{supp}(\hat{\mathbb{P}}^{tr}) = \mathcal{O}^{tr} \subseteq \widehat{\mathcal{U}}_k$.
*Proof.* For $o \in O^{tr}$ take $R = Q(o)$ in (1): $|Q(o)| \le \Pi^\*$ by definition of $\Pi^\*$ (it is the max over training orders, enforced by the master constraint $\sum_{q:\, q\cap P_o \neq \emptyset} x_q \le \Pi$), and $P_o \subseteq \bar{P}_o$ by (i). $\square$ Thus the construction **encloses** the empirical support — the conservative, robustness-conferring direction in RO (Ben-Tal–Nemirovski; Bertsimas–Gupta–Kallus template per Stage 1).

**(iii) Bound direction on the objective (majorization).** Define the visit count of a fixed layout $a: P \to S$ on an order set $u$: $v(a, u) = |\{a(p) : p \in u\}|$. This function is monotone: $u \subseteq u' \Rightarrow v(a,u) \le v(a,u')$. Hence for every $u \subseteq \bar{P}_o$,

$$v(a, u) \;\le\; v(a, \bar{P}_o) \;=\; \max_{u \subseteq \bar{P}_o} v(a, u), \tag{3}$$

i.e., the transformed objective $\sum_o v(a,\bar{P}_o)$ is a **pointwise upper bound (majorant)** on the nominal objective evaluated at any realization dominated by the enlarged sets, with the maximum attained at $u = \bar{P}_o$. Minimizing the transformed objective is therefore minimization of a conservative surrogate — the defining bound direction of a robust counterpart.

**Honest boundary:** "outer approximation" here is of the *support* and of *per-order composition boxes* — it makes no statement about probabilities of future orders, and the guarantee that future orders actually fall inside $\widehat{\mathcal{U}}_k$ is **not proven**; it is exactly the empirical content of H1 to be tested (A.4, E).

### A.3 — Cover variant: the minimality–redundancy tension, resolved

**Commitment: the exact-cover (partition) variant is primary.** The Stage-1 warning conflated two different minimalities. The P–K objective does **not** minimize cover cardinality $\sum_q x_q$ (the classical "minimal cover"); it minimizes $\Pi$, the **worst-case number of patterns any order touches** — a min-max *bottleneck* objective. The resolution is:

1. **Partition is a feasibility requirement, not a robustness defect.** The downstream CSLAP assigns each product to exactly one station (manuscript constraint \eqref{con14}: $\sum_s x_{ps} = 1$). A redundant cover ($\ge 1$) places a SKU in several patterns; those patterns cannot all be realized as disjoint station contents by any physically feasible layout. The partition structure of the exact variant is the unique cover structure isomorphic to the physical decision space.
2. **Robustness in this construction comes from enlargement, not multiplicity of coverage.** The conservatism knob is **$k$** (and the resulting $\Pi^\*$), not redundancy: larger $k$ → coarser partition → larger closures $\bar{P}_o$ → larger $\widehat{\mathcal{U}}_k$ → more conservative. $k$ plays exactly the role of Bertsimas–Sim's $\Gamma$ or a DRO radius: $k=1$ gives singletons, $\bar{P}_o = P_o$, the identity transform (zero conservatism); $k \to |P|$ collapses all orders to $P$ (total conservatism, layout discrimination vanishes). The Stage-1 demand for "a tunable conservatism knob" is satisfied.
3. **Minimizing $\Pi$ directly serves the robustness target.** For any layout that keeps every pattern whole in a single station, every $u \in \widehat{\mathcal{U}}_k$ satisfies $v(a,u) \le \Pi^\*$ (Proposition 2, §C). So min-max-$\Pi$ *is* minimization of the uniform worst-case per-order visit bound over the uncertainty set — alignment, not mismatch.
4. **Documented residual mismatch (honesty):** the redundant ($\ge 1$) variant produces *strictly larger* closures, hence a larger $\widehat{\mathcal{U}}$ (more conservative outer approximation), at the price of voiding the pattern-wholeness guarantee in point 3 and the physical isomorphism in point 1. We retain it as a **sensitivity arm only** (the instance transform (2) remains well defined for it), not as the primary method. If experiments show the redundant variant dominating, that would indicate H1's mechanism is generic enlargement rather than partition structure — a finding to report, not suppress.

### A.4 — Committed uncertainty / perturbation model (the de facto uncertainty set)

**Commitment: both channels of brief §2.4, named as follows.**

**(a) Empirical temporal hold-out (primary, real shift) — "temporal uncertainty realization".** BERNER orders (Sep–Dec, 13 weeks, per manuscript §`sec:temporal_validation`) split train-early/test-late at the manuscript's own two split points: train = first 10 weeks / test = last 3 weeks, and train = first 8 weeks / test = last 5 weeks. This reuses the article's established protocol verbatim, ensuring register consistency. **Unverified assumption (flagged):** `BERNER_ORDER_LINES_09-12.csv` has columns `PRODUCT;ORDER;QTY;STATION;BOX_ID` and **no date column**; the manuscript's 13-week split implies temporal metadata was recoverable (order-ID monotonicity in time, or an external mapping). Stage 3 must verify how the manuscript's split was produced and reproduce it; the fallback is an order-ID-rank split at the 10/13 and 8/13 quantiles, explicitly labeled an assumption in all outputs.

**(b) Parametric itemset-shift family (controlled, graded shift) — "Zhang shift family".** Using `synthetic_data_zhang.py` mechanics with the SKU universe, stations file, and products file **frozen** to the training instance, regenerate **orders only** under perturbed parameters. The de facto uncertainty set is the parametric family of order distributions

$$\mathcal{D}_{shift} = \Big\{ \mathbb{P}_{\theta',\, \rho,\, \sigma} : \theta' \in \Theta,\ \rho \in [0,1],\ \sigma \in \text{seeds} \Big\}, \tag{4}$$

where $\theta'$ is the itemset-injection probability (train default $\theta = 0.7$), $\rho$ is the **fraction of the common-itemset pool resampled** (replaced by fresh random itemsets over the same universe — $\rho = 0$: pure sampling noise; $\rho = 1$: complete correlation-structure replacement), and $\sigma$ the RNG seed. Grids in §E. The current generator couples itemsets/orders/stations under one seed and writes all three files; the Stage-3 harness must wrap it to regenerate orders against a frozen universe (contract item F.4).

### A.5 — Formal framework H1 instantiates (committed recast)

Stage 1 correctly found that H1 *as written* instantiates nothing. **Our committed recast (construction (2) + replacement instance, §C) makes it exactly the following, by identity rather than analogy:**

**Proposition 1 (robust-counterpart identity).** Because $v(a,\cdot)$ is monotone with maximum attained at the full set (eq. 3), the nominal CSLAP solved on the transformed instance is **identically equal** to the static robust counterpart of the empirical CSLAP objective under order-wise, subset-closed uncertainty boxes $\mathcal{B}(o) = \{u : u \subseteq \bar{P}_o\}$:

$$\min_{a \in \mathcal{A}} \sum_{o \in O^{tr}} v(a, \bar{P}_o) \;=\; \min_{a \in \mathcal{A}} \sum_{o \in O^{tr}} \max_{u \in \mathcal{B}(o)} v(a, u), \tag{5}$$

where $\mathcal{A}$ is the feasible set of \eqref{con14}, \eqref{con15}, \eqref{con17}. Equivalently, since the adversary decouples across empirical atoms, (5) equals the distributionally robust program $\min_a \max_{\mathbb{Q} \in \mathcal{D}} |O^{tr}|\,\mathbb{E}_{\mathbb{Q}}[v(a,u)]$ with ambiguity set $\mathcal{D} = \{\frac{1}{|O^{tr}|}\sum_o \delta_{u_o} : u_o \in \mathcal{B}(o)\ \forall o\}$ — all distributions obtained by transporting each empirical atom anywhere within its pattern-closure box. *Proof sketch:* inner max in (5) is attained at $u_o = \bar{P}_o$ independently per atom (monotonicity); for the DRO form, the worst $\mathbb{Q}$ places each atom at its box's argmax. $\square$

**Therefore: H1 (recast) = a data-driven static robust counterpart of CSLAP — solved *exactly* by the unchanged nominal solvers because the inner maximization is trivial under monotonicity.** The uncertainty set is *learned from data* via the P–K partition, in the spirit of Bertsimas–Gupta–Kallus (2018), but **without** their statistical calibration: no finite-sample guarantee that future orders lie in $\widehat{\mathcal{U}}_k$ is claimed or available. What is structural (the identity (5)) versus what is conjectural (future orders ≈ within $\widehat{\mathcal{U}}_k$, hence out-of-sample benefit) must be kept separate in all downstream writing. It is **not** SAA (no sampling/expectation over generated scenarios), **not** scenario aggregation (no probability weights, no non-anticipativity), and only the objective is robustified — workload constraints \eqref{con17} stay nominal (see C.4; constraint robustness is explicitly out of scope).

---

## B. Candidate evaluation

Hard requirement from the brief: the method must be an **instance transformation** consumable by all existing solvers **unchanged**. Scoring 1–5 per criterion.

| Criterion | (i) P–K covering enlargement (order-closure replacement) | (ii) SAA over perturbed order samples | (iii) Budgeted robust counterpart (Γ on order composition) | (iv) Wasserstein DRO |
|---|---|---|---|---|
| Fidelity to H1 | **5** — is H1, recast with exact semantics (Prop. 1) | 2 — tests "more data," not the covering construction | 2 — robustness yes, covering no | 2 — same |
| Tractability | **4** — same solver class; instance grows ~3–4× in link constraints (closures ≤ $\Pi^\* k = 36$ vs median order 10) | 3 — instance grows linearly in scenario count | 1 — uncertainty is *combinatorial* (which SKUs are in an order), no LP-duality counterpart; needs C&CG | 1 — needs new conic/CG machinery |
| Reuse of solvers UNCHANGED (mandatory) | **5** — pure CSV transform | 5 — pure CSV transform (pooled sampled orders; placement has no recourse, so the SP collapses to nominal CSLAP on the pooled sample) | **0 — violates the constraint** (new model) | **0 — violates the constraint** |
| Implementability with P–K code | **5** — uses it as-is (port, F.5) | 1 — doesn't use it | 2 — could use patterns to define deviations | 1 |
| Testability of robustness claim | **5** — k-indexed tradeoff curve, falsifiable | 4 | 3 | 3 |

**Selection: candidate (i)**, the covering-based enlargement as a data-driven order-wise robust counterpart (instance transform). Candidates (iii) and (iv) are eliminated on the mandatory reuse constraint alone; (iii) is additionally intractable here because the uncertain object is the *set* $P_o$, not a coefficient vector — Bertsimas–Sim duality does not apply. Candidate (ii) is rejected as the primary method (low H1 fidelity) but **retained as an optional control arm** (bootstrap-augmentation layout): it isolates whether any observed robustness gain comes from the covering *structure* or merely from data smoothing — a cheap and scientifically valuable ablation if budget permits.

---

## C. Formal formulation

### C.1 Primitives

- **Universe:** the training product set $P$ (from `{prefix}_products.csv` of the training instance).
- **Observed order family:** $O^{tr}$ with product sets $P_o \subseteq P$, from `{prefix}_orders.csv` (training rows only; semicolon-separated, schema `ORDER;PRODUCT;QTY;STATION`).
- **Pick-lines:** $L_p = |\{(o,p) \text{ rows}\}|$, exactly as computed by `read_data` (`orders_df.groupby("PRODUCT").size()`).

### C.2 Construction operator $C_{k}^{var}(\cdot)$ — the verified P–K column generation

$C_k^{var}: \mathcal{O}^{tr} \mapsto (Q^\*, \Pi^\*)$, $var \in \{\text{exact}, \text{cover}\}$, implemented by the notebooks' CG, formulation frozen as follows (master, integer phase; $x_q \in \{0,1\}$ selects pattern $q$):

$$\min\ \Pi \tag{6}$$
$$\text{s.t.}\quad \sum_{q \ni p} x_q \;=\; 1 \quad \forall p \in P \qquad \text{(exact variant; } \ge 1 \text{ in the cover variant)} \tag{7}$$
$$\sum_{q :\, q \cap P_o \neq \emptyset} x_q \;\le\; \Pi \quad \forall o \in O^{tr}_{\neq} \tag{8}$$

over patterns $q \subseteq P$, $1 \le |q| \le k$, generated by the pricing problem (duals $\alpha_p$ from (7), $\beta_o \le 0$ from (8)):

$$\max_{z, w}\ \sum_{p \in P} \alpha_p z_p + \sum_{o} \beta_o w_o \quad \text{s.t.}\quad \sum_p z_p \le k,\ \ \sum_p z_p \ge 1,\ \ w_o \ge z_p\ \forall o,\ \forall p \in P_o,\ \ z, w \in \{0,1\}, \tag{9}$$

accepting a column iff score $> 10^{-6}$; LP phase then integer re-solve over deduplicated columns — **exactly the notebook logic** (`new_alban_version_exact.ipynb` / `new_alban_version.ipynb`). Defaults: $k = 6$, variant = exact. In (8), $O^{tr}_{\neq}$ denotes **distinct** order supports — duplicates yield identical constraints, so deduplication is exact for (6)–(9) (this is the scaling lever for full-size training sets; the notebook's caps of 400 orders and order size ≤ 12 are experiment artifacts, exposed as optional parameters, **not** part of the method — and the known result $\Pi^\* = 6$ at $k=6$ holds on that 400-order/≤12-item slice only).

### C.3 Enlarged-instance mapping $\mathcal{T}$ (the transform fed to unchanged solvers)

Given $(Q^\*, \Pi^\*)$ and the training instance, define per training order the cover $Q(o)$ and closure $\bar{P}_o$ by (2). The transformed instance $\mathcal{T}(\text{instance})$, written under prefix `{prefix}_pkk{k}` in the standard schema:

- **`*_orders.csv` (what replaces ORDER rows):** one pseudo-order per training order — **replacement, not augmentation**; ORDER id `CORD_{original}`; one row per $(o, p)$ with $p \in \bar{P}_o$; `QTY = 1`, `STATION = 1` (both ignored by `read_data`; schema placeholders, documented). Duplicate closures are **kept** (one pseudo-order per original order): row multiplicity is what carries the empirical frequency weighting into the objective. The `PROD_` prefixing convention of `read_data` must be respected (transform writes the same product tokens the products file induces).
- **`*_products.csv`:** carried over unchanged (same universe ⇒ identical file).
- **`*_stations.csv`:** `STATION_ID, CAPACITY, SPEED` carried over unchanged. `TIME_CAPACITY` is **recalibrated**, because the transform inflates line counts: in the transformed file, $\bar{L}_p = |\{o : q(p) \in Q(o)\}| \ge L_p$ (the popularity of $p$'s pattern). Recalibration rule (mirrors the generator's 10%-slack rule):

$$\bar{T}_s \;=\; \Big\lceil 1.10 \cdot \frac{\sum_{p} \bar{L}_p / V_s}{|S|} \Big\rceil \quad \forall s \in S \ \ (\text{homogeneous } V_s). \tag{10}$$

**Declared bias (do not hide):** the transformed workload signal $\bar{L}_p$ over-weights products in frequently-hit patterns; the workload constraint binds on this conservative proxy, and **true** feasibility of the resulting layout is verified post hoc on real $L_p, T_s$ by the evaluator (C.5) and reported via the standard `cap_broken` / `wl_broken` fields. Constraint robustness is not claimed (A.5).

### C.4 Downstream model (unchanged)

The solvers minimize the manuscript's objective \eqref{obj} subject to \eqref{con14}–\eqref{con17} on $\mathcal{T}(\text{instance})$ — i.e., they solve the left-hand side of identity (5), which equals the right-hand robust counterpart. No solver file is modified; every baseline (MILP, CG, heuristic, GA, SA) consumes the transformed CSVs through its existing `read_data`.

**Proposition 2 (worst-case visit guarantee, conditional).** If a layout $a$ assigns each $q \in Q^\*$ wholly to a single station, then $\sup_{u \in \widehat{\mathcal{U}}_k} v(a,u) \le \Pi^\*$. *Proof:* $u \subseteq \bigcup_{q \in R} q$, $|R| \le \Pi^\*$ ⇒ $a(u) \subseteq \{a(q): q \in R\}$. $\square$ **Caveat:** pattern-whole layouts need not exist (capacities $\zeta_s$ sum exactly to $|P|$, so a perfect packing of patterns into stations is required); the transformed objective merely *induces* wholeness, and the bound degrades gracefully to $v(a,u) \le \sum_{q \in R} |a(q)|$ when patterns split. State as conditional in the article.

### C.5 Evaluation functional (fixed layout, fresh orders — separate, cheap, no solver)

The existing solvers *optimize* layouts; evaluation of a **fixed** layout on test orders is a direct computation. For layout $a: P \to S$ (the `assignment` dict of the standard return tuple) and any fresh order family $O^{te}$:

$$\mathcal{V}(a, O^{te}) \;=\; \sum_{o \in O^{te}} \big|\{\, a(p) : p \in P_o \cap \operatorname{dom}(a) \,\}\big| \tag{11}$$

with companion statistics: coverage $\kappa = \sum_o |P_o \cap \operatorname{dom}(a)| \,/\, \sum_o |P_o|$ (fraction of test lines whose SKU exists in the training universe — unseen SKUs are **excluded from (11) and reported via $\kappa$**, identically for all compared layouts, so comparisons stay fair); and realized workloads $W_s = \sum_{p:\,a(p)=s} L_p^{te}/V_s$ checked against the true $T_s$ (violation counts reported). Complexity $O(\sum_o |P_o|)$ — pandas only.

---

## D. Bias–variance tradeoff (explicit)

- **What is lost (bias).** By (3) the training objective is a strict majorant of nominal visits whenever any $\bar{P}_o \supsetneq P_o$; the robust layout $a_k$ is therefore (weakly) suboptimal nominally: $\mathcal{V}(a_k, O^{tr}) \ge \mathcal{V}(a_0, O^{tr})$, where $a_0$ is the nominal-instance optimum. The bias is monotone in the closure size, hence driven by $k$: at $k=1$, $\mathcal{T} = \mathrm{id}$ and bias $= 0$; as $k$ grows, closures grow toward $P$ and the objective loses the ability to discriminate layouts (at the extreme every layout scores $|O^{tr}| \cdot v(a,P)$-ish — total bias, zero signal). Secondary bias source: the workload recalibration (10) (direction: spreads pattern-popular products, mildly opposing concentration).
- **What is gained (variance reduction).** The optimized layout depends on the data only through the pattern hypergraph $(Q^\*, \{Q(o)\})$ — a coarse-grained statistic of the order stream — rather than through exact order compositions. Resampling or shifting the order distribution within the same pattern structure leaves the transformed instance (nearly) invariant, so the layout's out-of-sample degradation (generalization gap) should shrink. Under H1, the out-of-sample cost $\mathcal{V}(a_k, O^{te})$ as a function of $k$ is predicted **U-shaped**: decreasing while variance reduction dominates, increasing once conservatism bias dominates.
- **Parameters trading them off.** $k$ (primary knob, $\Gamma$-analog): bias ↑ in $k$, variance ↓ in $k$. $\Pi^\*$ (achieved, not set): smaller $\Pi^\*$ ⇒ tighter worst-case bound (Prop. 2) and smaller closures ($|\bar{P}_o| \le \Pi^\* k$); $\Pi^\*$ decreases as $k$ increases (coarser patterns hit fewer per order). Exact vs. redundant cover: redundant ⇒ strictly larger closures ⇒ more bias, potentially more robustness, guarantee of Prop. 2 voided (A.3).
- **Predicted directions under H1** (falsifiable): (P1) nominal loss $\mathcal{V}(a_k,O^{tr}) - \mathcal{V}(a_0,O^{tr}) > 0$ and increasing in $k$; (P2) out-of-sample gain $\mathcal{V}(a_0,O^{te}) - \mathcal{V}(a_k,O^{te}) > 0$ for some intermediate $k$, increasing in shift magnitude $\rho$; (P3) degradation slope across shift magnitudes flatter for $a_k$ than for $a_0$. H1 is **falsified** if (P2) fails for all $k > 1$ at all shift levels; per the brief, a robustness gain with *no* nominal loss indicates a leak or bug, not success.

---

## E. Robustness metrics and experimental design

### E.1 Metric definitions (per train instance, solver $m$, knob $k$; $a_0^m$ = nominal layout, $a_k^m$ = robust layout, both produced by solver $m$ under identical time budget)

1. **Nominal cost:** $N(a) = \mathcal{V}(a, O^{tr})$; also reported per-order: $N(a)/|O^{tr}|$.
2. **Out-of-sample cost:** $V^{te}(a) = \mathcal{V}(a, O^{te})$ (per test set), with $\kappa$ and workload violations from C.5.
3. **Relative regret vs. test-reoptimized oracle:** $a^{or}$ = layout from the same solver, same time budget, optimized directly on $O^{te}$ (oracle uses test data **only** as a normalizer, clearly labeled):
$$\mathrm{RR}(a) = \frac{\mathcal{V}(a, O^{te}) - \mathcal{V}(a^{or}, O^{te})}{\mathcal{V}(a^{or}, O^{te})}. \tag{12}$$
4. **Price of robustness / robustness gain:**
$$\mathrm{PoR}(k) = \frac{N(a_k) - N(a_0)}{N(a_0)}, \qquad G(k) = \frac{V^{te}(a_0) - V^{te}(a_k)}{V^{te}(a_0)}. \tag{13}$$
5. **Degradation slope:** over the Zhang shift grid $\rho \in \{0, 0.25, 0.5, 1.0\}$, the OLS slope of mean $V^{te}_\rho(a)/|O^{te}|$ against $\rho$; compare slopes of $a_0$ vs $a_k$ (P3).
6. **Tradeoff curve (headline deliverable, brief §4):** the curve $\{(\mathrm{PoR}(k),\, G(k))\}_{k \in K}$ per solver and per shift level — never a single number.

### E.2 Train/test protocol — no leakage (binding)

- $C_k^{var}(\cdot)$ sees **only** $O^{tr}$. The transform $\mathcal{T}$ sees **only** the training instance. Every solver run that produces $a_0$ or $a_k$ sees **only** training-derived CSVs. Test orders are read **exclusively** by `evaluate_layout_robust.py` — with the single labeled exception of the oracle runs (12).
- Station and product files derive from the training universe; test evaluation restricts to $\operatorname{dom}(a)$ with $\kappa$ reported (C.5).
- The harness must assert disjointness (BERNER: train/test order-ID sets disjoint; Zhang: test seeds distinct from train seed) and log the assertion.

### E.3 Perturbation parameters

- **BERNER temporal:** splits 10w/3w and 8w/5w (A.4(a); split-mechanics verification duty flagged there). One industrial universe (~22k SKUs): only `heuristic_synthetic`, CG, GA, SA arms at this scale; MILP only if a reduced slice is defined and labeled as such.
- **Zhang shift simulation:** train instances $N \in \{50, 500, 1000\}$ ($2000$ optional), $\theta = 0.7$, train seed(s) $\{42, 43, 44\}$ (≥3 train instances mandatory for $N \in \{50, 500\}$). Test grids: $\theta' \in \{0.5, 0.7, 0.9\}$, $\rho \in \{0, 0.25, 0.5, 1.0\}$, $M = 10$ test seeds per cell, orders regenerated against the frozen universe.
- **Knob grid:** $k \in \{1, 2, 4, 6, 8\}$ ($k=1$ = identity transform — must reproduce nominal results exactly; built-in correctness check), variant = exact (primary), cover (sensitivity at $k = 6$ only).

### E.4 Statistical treatment

Paired design throughout: for a fixed train instance and solver, $a_0$ and $a_k$ are evaluated on **identical** test sets. Per cell: mean ± 95% t-CI over the $M = 10$ test seeds; Wilcoxon signed-rank test on paired differences $V^{te}(a_0) - V^{te}(a_k)$; Holm correction across the $k$-grid within each (solver, shift-cell) family. Report effect sizes (median paired relative difference), not just p-values. BERNER: two splits give point estimates only — supplement with per-week paired visit counts (3 and 5 paired points; report descriptively, no significance claims). Identical `--time` budgets across arms within a solver; solver seeds fixed and logged.

---

## F. Implementation contract for Stage 3

All files in `Different_Solution_Approaches/Full_Package_Code_With_All_Approaches/CSLAP-Synthetic/Baselines/`, all with `--prefix/--dir/--time` CLI per `code-standards.md`, type hints, LaTeX-math docstrings citing equations (1)–(13) of this report by number.

1. **`pk_cover_construction.py`** — the construction operator $C_k^{var}$, eqs. (6)–(9), as an importable module + CLI. Extra args: `--k` (default 6), `--variant {exact,cover}` (default exact), `--max-orders`/`--max-order-size` (default off; notebook-artifact reproduction only). Outputs: pattern list (JSON/CSV), $\Pi^\*$, CG log with timing breakdown mirroring the notebook's. **Porting decision (committed):** *primary path = port the CG master/pricing to `gurobipy`*, preserving (6)–(9) exactly — the project stack is Gurobi (CLAUDE.md), duals are available identically (`Constr.Pi`), and docplex/CPLEX availability in this environment is unverified. *Fallback path:* if Stage 3 verifies `import docplex` plus a working CPLEX runtime, it may instead wrap the notebooks' docplex logic behind the same module API. **Acceptance test for either path:** reproduce $\Pi^\* = 6$ at $k = 6$ on `filtered_dataset.csv` under the notebook's slice settings (≤12-item orders, first 400 retained). Mandatory scaling feature: constraint (8) built over distinct order supports (exactness argued in C.2).
2. **`pk_instance_robust.py`** — transform $\mathcal{T}$ (C.3): reads training CSVs, runs/loads the cover, writes `{prefix}_pkk{k}_orders.csv`, `..._stations.csv` (recalibrated $\bar{T}_s$, eq. 10), `..._products.csv` into `--dir`. Must be byte-compatible with `read_data` of `milp_gurobi_synthetic.py` (semicolon sep, `ORDER;PRODUCT;QTY;STATION` columns, `PROD_` token consistency). $k=1$ must regenerate the original orders' supports (identity check).
3. **`evaluate_layout_robust.py`** — eq. (11) + C.5 companions. Input: layout file (JSON `{product: station}` persisted by the harness from each runner's `assignment`), test instance prefix. No solver dependency. Outputs one row per (layout, test set) into `results_robustness_eval.csv`.
4. **`run_robustness_experiment.py`** — harness: (a) BERNER temporal splitter (writes standard-schema train/test instances; builds industrial station/product files — reuse the manuscript's industrial station configuration if present in the repo, else homogeneous stations by the Zhang rule, documented); (b) Zhang shift wrapper (frozen universe, orders-only regeneration per (4)); (c) runs each baseline on nominal and transformed instances by **importing runner functions** (to capture the `assignment` from the standard return tuple `(assignment, total_visits, elapsed_time, util_variance, max_util, cap_broken, wl_broken, best_bound)`), with thin adapters in the harness if GA/SA signatures differ — **no baseline file may be modified**; (d) persists layouts to `layouts/`, calls the evaluator, enforces and logs the E.2 leakage assertions; (e) writes `results_robustness_*.csv` aligned with the existing `results_syn_*.csv` conventions.
5. **Baselines to run:** `milp_gurobi_synthetic.py`, `cg_gurobi_synthetic.py`, `heuristic_synthetic.py`, `ga_baseline.py`, `sa_correlated.py`; Hexaly variants (`milp_synthetic.py`, `cg_synthetic.py`) **only if** a license is detected at runtime (try/except import + env probe, logged).
6. **Artifacts:** transformed instances (distinguishing prefix `_pkk{k}`), pattern/$\Pi^\*$ files, layout JSONs, results CSVs, per-run logs (solve start, config, objective, termination status per code-standards §5).

**Open items / unverified assumptions register (for Stages 3–5):** (U1) BERNER temporal split mechanics — no date column; verify against the manuscript's 13-week procedure or fall back to order-ID rank, labeled. (U2) docplex/CPLEX availability — Stage 3 verifies; Gurobi port is primary regardless. (U3) $\Pi^\* = 6$ holds on the 400-order slice only; full-train $\Pi^\*$ values unknown until run. (U4) Pattern-whole layouts may not exist (Prop. 2 is conditional). (U5) Future orders are **not** guaranteed to lie in $\widehat{\mathcal{U}}_k$ — this is precisely H1, to be tested, not assumed. (U6) Workload recalibration (10) is a declared modeling bias; true feasibility checked post hoc. (U7) Construction scalability on the full BERNER train set is unproven; distinct-support deduplication is the committed mitigation, subsampling the documented fallback.

---

**Status: METHOD COMMITTED.** Ready for Stage 3 (Optimization Coder) under the contract in §F.
