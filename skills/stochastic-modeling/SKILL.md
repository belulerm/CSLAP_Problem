---
name: stochastic-modeling
description: Build stochastic optimization models for warehouse problems under demand/parameter uncertainty. Use when formulating two-stage or multi-stage stochastic programs, designing scenario generation, applying SAA, or selecting decomposition methods. Specialized for SLAP-family problems with probabilistic uncertainty.
---

# Stochastic Modeling

## Purpose
Produce rigorous stochastic optimization formulations for warehouse problems where uncertainty (demand, picking frequency, replenishment lead time) follows a probability distribution. Cover model formulation, scenario generation, solution methods, and quality assessment.

## Scope
This skill applies to:
- Two-stage stochastic programs (here-and-now decisions + recourse)
- Multi-stage stochastic programs (sequential decisions over time)
- Sample Average Approximation (SAA) for tractability
- Risk-averse extensions (CVaR, mean-variance)
- Stochastic SLAP, CSLAP, and MSLAP variants

**Out of scope**: parameter uncertainty without probabilistic structure (use `robust-modeling` instead); ML forecasting integration (use future `ml-forecasting-integration`).

## Foundational Distinctions

### Decision Timing
- **Here-and-now ($x$)**: decisions made *before* uncertainty realizes (e.g., physical slot assignment).
- **Wait-and-see / recourse ($y(s)$)**: decisions made *after* observing scenario $s$ (e.g., picker routing).
- A well-defined stochastic model is explicit about which decisions are first-stage vs. recourse.

### Risk Attitudes
- **Risk-neutral**: minimize expected cost $\mathbb{E}[c(x, \tilde{\xi})]$.
- **Risk-averse**: penalize high-cost tails (CVaR, mean-variance).
- **Robust** (separate skill): minimize worst-case, no probabilistic structure required.

### Information Structure
- **Static**: all uncertainty resolves simultaneously.
- **Dynamic / multi-stage**: uncertainty resolves sequentially with adaptive decisions.

## Standard Formulations

### Two-Stage Stochastic Program (General Form)

$$\min_{x \in \mathcal{X}} \; c^\top x + \mathbb{E}_{\tilde{\xi}}\left[Q(x, \tilde{\xi})\right]$$

where the recourse function is
$$Q(x, \xi) = \min_{y \in \mathcal{Y}(x, \xi)} q(\xi)^\top y.$$

- $x$: first-stage decision (e.g., product-to-location assignment).
- $\tilde{\xi}$: random parameter vector (demand, frequency, etc.).
- $y$: second-stage recourse (e.g., overflow handling, reassignment).
- $\mathcal{Y}(x, \xi)$: feasibility set given first-stage decision and scenario.

### Two-Stage Stochastic SLAP

**First stage**: assign products to locations.
**Second stage**: handle demand realization (overflow, additional picks).

$$\min_{x} \; \underbrace{\sum_{p,\ell} f_p \, c_\ell \, x_{p\ell}}_{\text{picking cost (deterministic)}} + \sum_{s \in \mathcal{S}} \pi^s \, Q^s(x)$$

subject to assignment constraints, with recourse:

$$Q^s(x) = \min_{y^s, z^s} \beta \sum_{p,\ell} \frac{d_p^s}{V_\ell} x_{p\ell} + M \sum_p z_p^s$$

where $z_p^s$ is a penalty for demand $d_p^s$ that exceeds the capacity of the assigned location.

### Multi-Stage Formulation (Demand Evolves Over Time)

For $t = 1, \ldots, T$:

$$\min \mathbb{E}\left[\sum_{t=1}^T c_t^\top x_t(\xi_{[1:t]})\right]$$

with non-anticipativity: $x_t$ depends only on $\xi_{[1:t]}$ (history observed up to $t$).

### CVaR-Augmented Objective

For tail-risk control with confidence level $\alpha \in (0,1)$:

$$\min_x \; (1-\rho) \, \mathbb{E}[c(x, \tilde{\xi})] + \rho \cdot \text{CVaR}_\alpha[c(x, \tilde{\xi})]$$

CVaR linearization (sample-based):
$$\text{CVaR}_\alpha = \min_{\eta} \; \eta + \frac{1}{(1-\alpha) |\mathcal{S}|} \sum_{s} [c(x, \xi^s) - \eta]^+$$

introducing auxiliary variables $w^s \geq c(x, \xi^s) - \eta$, $w^s \geq 0$.

## Scenario Generation

### Quality Criteria
Scenarios must:
1. Cover the support of $\tilde{\xi}$ (no important regions missed).
2. Preserve relevant statistics (mean, variance, correlation structure).
3. Be computationally tractable (small enough $|\mathcal{S}|$).
4. Yield stable solutions (low in-sample vs. out-of-sample gap).

### Generation Methods

#### A. Monte Carlo / Random Sampling
- Sample i.i.d. from estimated distribution.
- Simple, asymptotically valid (SAA convergence).
- May require large $|\mathcal{S}|$ for stability.

#### B. Quasi-Monte Carlo
- Low-discrepancy sequences (Sobol, Halton).
- Faster convergence than crude Monte Carlo for moderate dimension.

#### C. Scenario Reduction
- Start with large scenario set, reduce via clustering (k-means on $\xi^s$).
- Preserve probability mass (reduced scenarios inherit weights of merged ones).
- Algorithms: Heitsch–Römisch, fast forward selection.

#### D. Historical Bootstrapping
- Use historical demand data directly as scenarios.
- Captures empirical correlations.
- Requires careful handling of temporal dependence.

#### E. Moment-Matching
- Generate scenarios that match specified moments (mean, variance, skewness, correlation).
- Useful when distribution is parametrically specified.

### Reporting Scenario Generation
In the thesis, document:
- Source data (historical / synthetic / hybrid).
- Sample size $|\mathcal{S}|$ and justification.
- Generation method.
- Validation (in-sample stability, out-of-sample test).

## Solution Methods

### Sample Average Approximation (SAA)

1. Generate $|\mathcal{S}|$ scenarios.
2. Solve the deterministic equivalent (DEM):

$$\min_x \; c^\top x + \frac{1}{|\mathcal{S}|} \sum_{s=1}^{|\mathcal{S}|} Q(x, \xi^s)$$

3. Repeat with independent batches $M$ times → confidence interval on optimal value.

**Convergence**: As $|\mathcal{S}| \to \infty$, SAA solution converges to true stochastic optimum (with probability 1).

**Diagnostics**:
- **Optimality gap**: difference between upper bound (best SAA solution) and lower bound (mean of SAA objectives across batches).
- **In-sample vs. out-of-sample cost**: evaluate the chosen $x$ on a held-out scenario set.

### L-Shaped / Benders Decomposition

Decompose by stages:
- **Master problem**: first-stage variables + cuts approximating $\mathcal{Q}(x) := \mathbb{E}[Q(x, \tilde{\xi})]$.
- **Subproblems**: one per scenario, generates optimality / feasibility cuts.

**When to use**: large $|\mathcal{S}|$ makes DEM intractable; subproblems are easy LPs.

### Progressive Hedging

Iterative augmented Lagrangian on scenario-decomposable problem:
1. Solve scenario subproblems independently → $\bar{x}^s$.
2. Average across scenarios → $\hat{x}$.
3. Add penalty term for deviation from $\hat{x}$.
4. Repeat until non-anticipativity is enforced.

**When to use**: multi-stage problems with strong scenario structure; mixed-integer first-stage.

### Stochastic Decomposition (for Continuous Recourse)
- Generates cuts on-the-fly via subgradient sampling.
- Avoids enumerating all scenarios.
- Useful for very large or continuous uncertainty.

## Quality Metrics for Stochastic Solutions

### Value of Stochastic Solution (VSS)
$$\text{VSS} = \text{EEV} - \text{RP}$$
- **EEV** (Expected value of Expected-value solution): cost of solving with mean parameters, then evaluating against scenarios.
- **RP** (Recourse Problem optimum): cost of the true stochastic optimum.

Large VSS → ignoring uncertainty is costly; stochastic modeling is worthwhile.

### Expected Value of Perfect Information (EVPI)
$$\text{EVPI} = \text{RP} - \text{WS}$$
- **WS** (Wait-and-See): cost if uncertainty were known before deciding.

Large EVPI → forecasting effort would be valuable.

### Out-of-Sample Performance
- Train on scenarios $\mathcal{S}_{\text{train}}$, solve.
- Evaluate the chosen $x$ on independent scenarios $\mathcal{S}_{\text{test}}$.
- Report mean, std, percentiles, worst-case.
- A solution that performs well in-sample but poorly out-of-sample is overfit to scenarios.

## Notation Conventions (Aligned with `mathematical-formulation`)

| Symbol | Meaning |
|--------|---------|
| $\tilde{\xi}$ | Generic random parameter vector |
| $\xi^s$ | Realization in scenario $s$ |
| $\pi^s$ | Probability of scenario $s$, $\sum_s \pi^s = 1$ |
| $\mathcal{S}$ | Scenario set |
| $\tilde{d}_p$, $d_p^s$ | Random demand, scenario-specific demand |
| $Q(x, \xi)$ | Recourse function |
| $\mathcal{Q}(x)$ | Expected recourse $\mathbb{E}[Q(x, \tilde{\xi})]$ |
| $y$ or $y(\xi)$ | Recourse decision |
| $z^s$ | Slack / penalty variable in scenario $s$ |
| $\alpha$ | CVaR confidence level |
| $\rho$ | Risk aversion weight |

## Application to Warehouse Problems

### Stochastic SLAP (Demand Uncertainty)
- **First-stage**: $x_{p\ell}$ — physical assignment (hard to change).
- **Recourse**: $z_p^s$ — overflow / additional handling cost when realized demand exceeds capacity.
- **Cost**: deterministic picking + expected replenishment + expected overflow penalty.

### Stochastic CSLAP (Order Correlation Uncertainty)
- Co-location decision under uncertain product correlation patterns.
- Scenarios reflect alternative correlation matrices estimated from order data.

### Stochastic MSLAP (Multi-Source Demand)
- Source assignments with uncertain demand across origins.
- Recourse: source-switching when local capacity is exceeded.

## Common Pitfalls

- ❌ Treating `\mathbb{E}` as if linear over non-linear cost (jensen's inequality concerns).
- ❌ Generating scenarios that ignore temporal correlation in demand.
- ❌ Using same scenarios for training and evaluation (over-fitting illusion).
- ❌ Reporting only expected cost without out-of-sample variance.
- ❌ Conflating risk-aversion with robustness (CVaR ≠ worst-case).
- ❌ Solving DEM with thousands of scenarios when decomposition is needed.
- ❌ Forgetting non-anticipativity in multi-stage models.
- ❌ Comparing stochastic solution to deterministic on the *same nominal scenario* (use multiple scenarios for fair comparison).

## Reporting Checklist (Stochastic Section)

- [ ] Decision structure (first-stage vs. recourse) explicit.
- [ ] Random variables clearly defined with notation $\tilde{\xi}$.
- [ ] Scenario generation method documented.
- [ ] Sample size $|\mathcal{S}|$ justified (stability analysis).
- [ ] Solution method specified (SAA / Benders / Progressive Hedging).
- [ ] VSS or EVPI computed where meaningful.
- [ ] Out-of-sample evaluation on independent scenarios.
- [ ] Risk attitude (neutral / averse) and parameters ($\alpha$, $\rho$) stated.
- [ ] Comparison against deterministic baseline (using mean parameters).
- [ ] Computational performance: solve time as a function of $|\mathcal{S}|$.

## Cross-References to Other Skills

- Use `mathematical-formulation` for notation consistency with deterministic chapters.
- Use `algorithm-documentation` to describe SAA, Benders, progressive hedging.
- Use `experimental-results-presentation` for out-of-sample analysis and VSS reporting.
- Use `sparring-partner-review` to test the validity of distributional assumptions.
- Use `literature-review-citation` for foundational works:
  - Birge & Louveaux (Introduction to Stochastic Programming)
  - Shapiro, Dentcheva & Ruszczyński (Lectures on Stochastic Programming)
  - Rockafellar & Uryasev (CVaR)
  - Higle & Sen (Stochastic Decomposition)

## When to Invoke This Skill
- Drafting Chapter 4 (Stochastic Optimization) or related sections.
- Extending a deterministic model to incorporate demand uncertainty.
- Designing scenario generation experiments.
- Selecting between SAA, decomposition, or progressive hedging.
- Computing VSS / EVPI for a warehouse case study.
- Reviewing claims about stochastic performance for rigor.
