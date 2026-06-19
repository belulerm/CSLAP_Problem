---
name: robust-modeling
description: Build robust optimization models for warehouse problems under set-based (non-probabilistic) uncertainty. Use when formulating worst-case formulations, defining uncertainty sets, deriving robust counterparts, or applying column-and-constraint generation. Specialized for SLAP-family problems with bounded parametric uncertainty.
---

# Robust Modeling

## Purpose
Produce rigorous robust optimization formulations for warehouse problems where uncertainty is described by **a set** (interval, ellipsoid, polyhedron, budgeted set) rather than a probability distribution. Cover uncertainty set design, robust counterpart derivation, tractable reformulations, solution methods, and quality assessment.

## Scope
This skill applies to:
- Static (single-stage) robust optimization with linear/conic constraints
- Two-stage adjustable (adaptive) robust optimization
- Affine decision rules (ADR) for tractability
- Bertsimas–Sim budgeted uncertainty
- Column-and-constraint generation (C&CG) for two-stage problems
- Robust SLAP, CSLAP, and MSLAP variants

**Out of scope**: probabilistic uncertainty (use `stochastic-modeling` instead); distributionally robust optimization (a hybrid — touch lightly, deeper treatment in a future skill); ML forecasting integration.

## Foundational Distinctions

### Robust vs. Stochastic vs. Distributionally Robust
- **Stochastic** (`stochastic-modeling`): distribution known; minimize expectation or risk measure.
- **Robust**: distribution *unknown* or unreliable; uncertainty described by a set $\mathcal{U}$; minimize worst-case.
- **Distributionally robust**: distribution belongs to an *ambiguity set*; minimize worst-case expectation.

When to choose robust over stochastic:
- Insufficient data to estimate a reliable distribution.
- Decision-maker is risk-averse to tail events without probabilistic structure.
- Constraints must hold under *all* realizations (hard guarantees).
- Industry/regulatory requirements demand worst-case safety.

### Static vs. Adjustable Robust
- **Static**: all decisions made *before* uncertainty realizes; no recourse.
- **Adjustable** (two-stage robust): first-stage $x$ before uncertainty, recourse $y(u)$ after observing $u$.
- Adjustable models are less conservative but harder to solve; affine decision rules (ADR) provide a tractable approximation.

### Constraint-Wise vs. Global Robustness
- **Constraint-wise**: each uncertain constraint must hold for *every* $u \in \mathcal{U}$.
- **Global**: solution must satisfy *all* constraints jointly for *every* $u$.
- Often equivalent when uncertainty enters constraints independently; differ when uncertain parameters are coupled across constraints.

## Uncertainty Sets

### 1. Box (Interval) Uncertainty
$$\mathcal{U}^{\text{box}} = \{u \in \mathbb{R}^n : \bar{u}_i - \hat{u}_i \le u_i \le \bar{u}_i + \hat{u}_i, \, \forall i\}$$

- $\bar{u}_i$: nominal value, $\hat{u}_i$: maximum deviation.
- Simplest model; often **too conservative** (assumes all parameters reach worst at once).
- Reformulation: LP (linear in $x$).

### 2. Ellipsoidal Uncertainty
$$\mathcal{U}^{\text{ell}} = \{u : (u - \bar{u})^\top \Sigma^{-1} (u - \bar{u}) \le \Omega^2\}$$

- Captures correlation structure via $\Sigma$.
- $\Omega$ controls size (often interpreted via $\chi^2$ quantile).
- Reformulation: SOCP (second-order cone program).

### 3. Polyhedral Uncertainty
$$\mathcal{U}^{\text{poly}} = \{u : Du \le e\}$$

- Most flexible linear set; box, simplex, budget are special cases.
- Reformulation: LP via duality.

### 4. Budget of Uncertainty (Bertsimas–Sim)
$$\mathcal{U}^{\Gamma} = \left\{u : u_i = \bar{u}_i + \hat{u}_i \zeta_i, \; |\zeta_i| \le 1, \; \sum_i |\zeta_i| \le \Gamma\right\}$$

- $\Gamma \in [0, n]$: at most $\lfloor \Gamma \rfloor$ parameters deviate fully; one partially.
- $\Gamma = 0$: deterministic; $\Gamma = n$: full box.
- **Most popular in practice** — controls conservatism with a single parameter.
- Reformulation: LP via duality (Bertsimas–Sim 2004).

### 5. Data-Driven Uncertainty Sets
- **Scenario hulls**: $\mathcal{U} = \text{conv}\{\xi^1, \ldots, \xi^N\}$ (convex hull of observations).
- **Wasserstein balls**: $\mathcal{U} = \{F : W_p(F, \hat{F}_N) \le \varepsilon\}$ (distributional, technically DRO).
- **PCA-based ellipsoids**: shape from empirical covariance.
- **Kernel-based sets**: support of an empirical kernel density.
- Selection should be justified by data; do not pick an arbitrary set "for tractability."

### Choosing Uncertainty Set Size
- **Probabilistic guarantees**: for budget $\Gamma$, constraint violation probability $\le \exp(-\Gamma^2 / 2n)$ under i.i.d. symmetric perturbations (Bertsimas–Sim).
- **Cross-validation**: pick set size that balances in-sample feasibility vs. out-of-sample worst-case.
- **Decision-maker risk preference**: larger set ↔ more conservative ↔ higher cost.

## Standard Formulations

### Generic Robust Counterpart
For a problem with uncertain parameters $u \in \mathcal{U}$:
$$\min_{x \in \mathcal{X}} \; \max_{u \in \mathcal{U}} \; c(u)^\top x \quad \text{s.t.} \quad A(u) x \le b(u), \, \forall u \in \mathcal{U}$$

The **robust counterpart** replaces the constrained max problem with its tractable reformulation derived via duality (for $\mathcal{U}$ polyhedral) or conic duality (for $\mathcal{U}$ ellipsoidal).

### Static Robust SLAP with Budgeted Demand

Let $\tilde{d}_p = \bar{d}_p + \hat{d}_p \zeta_p$, $|\zeta_p| \le 1$, $\sum_p |\zeta_p| \le \Gamma$.

Robust SLAP:
$$\min_{x} \max_{\zeta \in \mathcal{Z}^\Gamma} \sum_{p,\ell} \left(f_p c_\ell + \beta \frac{\bar{d}_p + \hat{d}_p \zeta_p}{V_\ell}\right) x_{p\ell}$$

**Robust counterpart** (Bertsimas–Sim reformulation):
$$\min_{x, y, \pi, \pi_0} \; \sum_{p,\ell} \left(f_p c_\ell + \beta \frac{\bar{d}_p}{V_\ell}\right) x_{p\ell} + \Gamma \pi_0 + \sum_p \pi_p$$

subject to:
$$\pi_0 + \pi_p \ge \frac{\beta \hat{d}_p}{V_\ell} x_{p\ell}, \; \forall p, \ell \in \mathcal{L}_p, \quad \pi_0, \pi_p \ge 0$$

plus the original assignment constraints.

### Two-Stage Adjustable Robust SLAP

**First stage**: $x_{p\ell}$ (assignment, made before observing demand).
**Adversary**: chooses $u \in \mathcal{U}$.
**Second stage**: $y(u)$ — overflow / reassignment recourse.

$$\min_{x \in \mathcal{X}} \; \max_{u \in \mathcal{U}} \; \min_{y \in \mathcal{Y}(x, u)} \; c^\top x + q^\top y$$

Generally **NP-hard** even for polyhedral $\mathcal{U}$; tractable approximations needed.

### Affine Decision Rule (ADR) Approximation

Restrict recourse to affine functions of uncertainty:
$$y(u) = y^0 + Y u$$

Substitute into the model, derive robust counterpart for the affine policy. Yields a tractable LP/SOCP. Loses some optimality but bounds the true adjustable optimum.

## Reformulation Techniques

### Bertsimas–Sim for Budgeted Uncertainty
For constraint $\sum_i (\bar{a}_i + \hat{a}_i \zeta_i) x_i \le b$ with $\sum_i |\zeta_i| \le \Gamma$, $|\zeta_i| \le 1$:

The constraint holds for all $\zeta$ iff:
$$\sum_i \bar{a}_i x_i + \max_{|S| \le \Gamma} \sum_{i \in S} \hat{a}_i |x_i| \le b$$

Linearizing via duality introduces auxiliary variables (one per constraint, one per uncertain parameter):
$$\sum_i \bar{a}_i x_i + \Gamma z_0 + \sum_i z_i \le b, \quad z_0 + z_i \ge \hat{a}_i |x_i|, \quad z_0, z_i \ge 0$$

(Linearize $|x_i|$ if $x$ is signed.)

### Conic Duality for Ellipsoidal Uncertainty
For constraint $(\bar{a} + \Sigma^{1/2} \zeta)^\top x \le b$ with $\|\zeta\|_2 \le \Omega$:
$$\bar{a}^\top x + \Omega \|\Sigma^{1/2} x\|_2 \le b$$

Yields an SOCP constraint.

### LP Duality for Polyhedral Uncertainty
For $\mathcal{U} = \{u : Du \le e\}$, the worst-case becomes a dual LP. Solve:
$$\max_u \{u^\top a : Du \le e\} = \min_\nu \{e^\top \nu : D^\top \nu = a, \nu \ge 0\}$$

and substitute the dual into the robust constraint.

## Solution Methods

### Direct Reformulation
When the robust counterpart admits closed-form reformulation (LP, SOCP), solve directly with a commercial solver (Gurobi, CPLEX, Hexaly for LP; Mosek for SOCP).

### Column-and-Constraint Generation (C&CG)
For two-stage adjustable robust problems too large for direct reformulation:

1. **Master**: first-stage problem + finite set of scenarios from $\mathcal{U}$.
2. **Subproblem**: find worst-case $u^* \in \mathcal{U}$ for current first-stage solution.
3. **Cut generation**: add $u^*$ and associated recourse variables to the master.
4. Iterate until master and subproblem objectives converge.

**Advantages**: handles complex $\mathcal{U}$ and recourse structure.
**Reference**: Zeng & Zhao 2013 (Operations Research Letters).

### Benders-Style Cutting Planes
Alternative decomposition: separate first-stage and worst-case recourse via cutting planes.

### Iterative Scenario Enumeration
For finite or sampled $\mathcal{U}$:
1. Start with small scenario set.
2. Solve robust problem.
3. Check feasibility against all $u \in \mathcal{U}$ (or against a held-out sample).
4. Add violating scenarios; resolve.

## Quality Metrics

### Price of Robustness (PoR)
$$\text{PoR} = \frac{z^{\text{robust}} - z^{\text{nominal}}}{z^{\text{nominal}}} \cdot 100\%$$

- $z^{\text{nominal}}$: optimal cost with nominal parameters.
- $z^{\text{robust}}$: optimal cost of robust solution.

Reports the *cost of conservatism*. Typically a curve vs. $\Gamma$ or $\Omega$.

### Probability of Constraint Violation
Evaluate the robust solution against random samples drawn from a presumed (possibly different) distribution:
- Empirical violation rate.
- Compare to theoretical bound (Bertsimas–Sim guarantee).
- A robust solution should have *very low* violation rate.

### Worst-Case Performance
Evaluate cost at the realized worst-case $u^*$. For two-stage robust, this is the master's converged value.

### Robustness–Performance Trade-Off
Plot:
- X-axis: $\Gamma$ (or $\Omega$).
- Y-axis: cost, with two lines:
  - Nominal cost of the robust solution evaluated at $\bar{u}$.
  - Worst-case cost.
- Decision-maker picks the operating point that balances expected cost and worst-case protection.

### Comparison Against Stochastic Solution
If a stochastic counterpart is available:
- Evaluate both on adversarial scenarios (favors robust).
- Evaluate both on average/random scenarios (often favors stochastic).
- Report which method dominates under which evaluation regime.

## Notation Conventions (Aligned with `mathematical-formulation`)

| Symbol | Meaning |
|--------|---------|
| $u$ | Uncertain parameter vector |
| $\mathcal{U}$ | Uncertainty set |
| $\bar{u}_i$, $\hat{u}_i$ | Nominal value, maximum deviation |
| $\zeta$ | Normalized perturbation, $u = \bar{u} + \hat{u} \zeta$ |
| $\Gamma$ | Budget of uncertainty (Bertsimas–Sim) |
| $\Omega$ | Radius of ellipsoidal uncertainty |
| $\Sigma$ | Covariance / shape matrix of ellipsoid |
| $y(u)$ | Adjustable recourse decision |
| $Y$, $y^0$ | Affine decision rule coefficients |
| $z^{\text{robust}}$, $z^{\text{nominal}}$ | Robust and nominal optimal costs |

## Application to Warehouse Problems

### Robust SLAP (Bounded Demand)
- Demand $\tilde{d}_p \in [\bar{d}_p - \hat{d}_p, \bar{d}_p + \hat{d}_p]$.
- Choose $\Gamma$ based on operational risk tolerance.
- Robust counterpart: LP via Bertsimas–Sim reformulation.
- Solve with Gurobi/CPLEX/Hexaly.

### Robust CSLAP (Uncertain Correlation)
- Order correlation matrix elements uncertain within bounds.
- Polyhedral uncertainty on correlation values; uncertainty set may need to enforce positive semi-definiteness (SDP constraints).

### Robust MSLAP (Capacity Uncertainty)
- Location capacities $V_\ell$ vary within $[V_\ell - \Delta_\ell, V_\ell + \Delta_\ell]$.
- Affects replenishment cost via $d_p / V_\ell$ — non-linear; requires reformulation or linearization.

### Adjustable Robust MSLAP (Source Switching)
- First-stage: physical assignment of products to locations and source groups.
- Recourse: when demand realizes, switch source assignment within feasibility.
- Use ADR or C&CG.

## Common Pitfalls

- ❌ Choosing $\mathcal{U}$ without data justification (arbitrary $\hat{u}_i$ values).
- ❌ Setting $\Gamma$ too large → trivially infeasible or absurdly conservative solutions.
- ❌ Confusing robust with risk-averse stochastic — robust has no probability measure.
- ❌ Using static robust where two-stage adjustable would yield big gains.
- ❌ Applying Bertsimas–Sim to non-linear or non-affine uncertainty without reformulation justification.
- ❌ Reporting only worst-case cost without comparison to nominal (PoR is informative).
- ❌ Ignoring SDP constraints when uncertainty is over covariance matrices (requires positive semi-definite cone).
- ❌ Using ADR without verifying that the affine restriction is justified (could lose much optimality).
- ❌ Not validating $\Gamma$ choice via cross-validation or domain knowledge.

## Reporting Checklist (Robust Section)

- [ ] Uncertainty set $\mathcal{U}$ clearly specified (type, parameters, data source).
- [ ] Justification for set size ($\Gamma$, $\Omega$) — data-driven or risk-based.
- [ ] Robust counterpart derivation included (or cited if standard).
- [ ] Reformulation type (LP / SOCP / SDP) stated explicitly.
- [ ] Solution method (direct, C&CG, ADR) justified by problem structure.
- [ ] Price of Robustness reported as a function of $\Gamma$.
- [ ] Probability of constraint violation evaluated empirically.
- [ ] Comparison against deterministic baseline (nominal solution).
- [ ] Comparison against stochastic solution (when available) on both adversarial and random scenarios.
- [ ] Computational performance documented.
- [ ] For two-stage models: static vs. adjustable comparison; ADR optimality gap if applicable.

## Cross-References to Other Skills

- Use `mathematical-formulation` for consistent notation with deterministic and stochastic chapters.
- Use `algorithm-documentation` to describe C&CG, Benders, ADR.
- Use `experimental-results-presentation` for PoR curves and constraint violation tables.
- Use `sparring-partner-review` to test uncertainty set justification and conservatism level.
- Use `stochastic-modeling` for comparison and to identify when one paradigm is preferable.
- Use `literature-review-citation` for foundational works:
  - Ben-Tal, El Ghaoui & Nemirovski (Robust Optimization, 2009)
  - Bertsimas & Sim (The Price of Robustness, 2004)
  - Bertsimas, Brown & Caramanis (Theory and Applications of Robust Optimization, 2011)
  - Zeng & Zhao (Solving two-stage robust optimization problems by C&CG, 2013)
  - Yanıkoğlu, Gorissen & den Hertog (A survey of adjustable robust optimization, 2019)

## When to Invoke This Skill
- Drafting Chapter 5 (Robust Optimization) or related sections.
- Extending a deterministic model to incorporate bounded parameter uncertainty.
- Designing or justifying an uncertainty set $\mathcal{U}$.
- Selecting between static, adjustable, and ADR formulations.
- Deriving a tractable robust counterpart (LP, SOCP, SDP).
- Implementing column-and-constraint generation for two-stage robust problems.
- Comparing robust vs. stochastic vs. deterministic solutions in experiments.
- Reviewing robust claims for over-conservatism or under-specification of $\mathcal{U}$.
