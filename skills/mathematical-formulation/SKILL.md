---
name: mathematical-formulation
description: Formulate optimization problems with rigorous mathematical notation. Use when defining new models, writing problem formulations, or extending existing models (e.g., deterministic to stochastic). Ensures consistent notation across the thesis.
---

# Mathematical Formulation

## Purpose
Produce clean, consistent, and complete mathematical formulations for optimization problems throughout the thesis. Notation introduced in early chapters must remain consistent in later chapters.

## Core Notation Conventions

### Sets
| Symbol | Meaning | LaTeX |
|--------|---------|-------|
| $\mathcal{P}$ | Set of products | `\mathcal{P}` |
| $\mathcal{L}$ | Set of locations | `\mathcal{L}` |
| $\mathcal{G}$ | Set of groups / communities | `\mathcal{G}` |
| $\mathcal{S}$ | Set of scenarios (stochastic) | `\mathcal{S}` |
| $\mathcal{U}$ | Uncertainty set (robust) | `\mathcal{U}` |
| $\mathcal{T}$ | Time horizon | `\mathcal{T}` |

### Indices
| Symbol | Range | Meaning |
|--------|-------|---------|
| $p$ | $p \in \mathcal{P}$ | Product index |
| $\ell$ | $\ell \in \mathcal{L}$ | Location index |
| $g$ | $g \in \mathcal{G}$ | Group index |
| $s$ | $s \in \mathcal{S}$ | Scenario index |
| $t$ | $t \in \mathcal{T}$ | Time period |

### Parameters (deterministic)
| Symbol | Meaning |
|--------|---------|
| $f_p$ | Pick frequency of product $p$ |
| $d_p$ | Daily volume demand of product $p$ |
| $c_\ell$ | Picking cost coefficient of location $\ell$ |
| $V_\ell$ | Replenishment capacity of location $\ell$ |
| $\beta$ | Replenishment cost weight |
| $\gamma$ | Single-stop cost in monetary units |

### Parameters (stochastic/robust)
| Symbol | Meaning |
|--------|---------|
| $\tilde{d}_p$ | Random daily demand of product $p$ |
| $d_p^s$ | Demand in scenario $s$ |
| $\pi^s$ | Probability of scenario $s$ |
| $\bar{d}_p, \hat{d}_p$ | Nominal value and deviation (robust) |
| $\Gamma$ | Budget of uncertainty (Bertsimas–Sim) |

### Decision Variables
| Symbol | Meaning |
|--------|---------|
| $x_{p\ell}$ | $1$ if product $p$ is assigned to location $\ell$ |
| $y_g$ | $1$ if group $g$ is active |
| $z_p^s$ | Recourse variable for product $p$ in scenario $s$ |

## Standard LP/IP Template

```latex
\begin{align}
\min \quad & \sum_{p \in \mathcal{P}} \sum_{\ell \in \mathcal{L}} c_{p\ell} \, x_{p\ell} \label{eq:obj} \\
\text{s.t.} \quad & \sum_{\ell \in \mathcal{L}} x_{p\ell} = 1, & \forall p \in \mathcal{P} \label{eq:assign} \\
& \sum_{p \in \mathcal{P}} x_{p\ell} \leq 1, & \forall \ell \in \mathcal{L} \label{eq:capacity} \\
& x_{p\ell} \in \{0,1\}, & \forall p, \ell. \label{eq:bin}
\end{align}
```

**Always include**:
- Objective `(eq:obj)`
- Assignment / coverage constraints
- Capacity / resource constraints
- Variable domain definitions
- Equation labels for cross-referencing

## Cost Function Structures

### Deterministic SLAP Cost
$$c_{p\ell} = f_p \cdot c_\ell + \beta \cdot \frac{d_p}{0.8 \, V_\ell}$$

- First term: picking cost
- Second term: replenishment cost
- 0.8 factor: capacity utilization buffer (justify in chapter)

### Sustainability-Augmented Cost (MSLAP)
$$c_{p\ell}^{(\lambda)} = (1-\lambda) \cdot c_{p\ell}^{\text{econ}} + \lambda \cdot \Delta_{\text{CO2}} \cdot (e_{\text{pick}} \cdot f_p + e_{\text{repl}} \cdot d_p / V_\ell)$$

- $\lambda \in [0,1]$: policy weight
- $\Delta_{\text{CO2}}$: grid carbon intensity (kg CO2e per kWh)
- $e_{\text{pick}}, e_{\text{repl}}$: energy coefficients (kWh per unit)

### Stochastic Two-Stage Cost
$$\min_x \; c^\top x + \mathbb{E}_{s \sim \mathcal{S}}[Q(x, s)]$$

where $Q(x, s)$ is the second-stage recourse function.

### Robust Worst-Case Cost
$$\min_x \; \max_{u \in \mathcal{U}} \; c(u)^\top x$$

## Style Rules

1. **Define before use**: every new symbol must be introduced at first appearance.
2. **Consistency across chapters**: re-use symbols from earlier chapters; do not introduce $p$ as "product" in Chapter 2 and "period" in Chapter 4.
3. **Avoid notational overload**: if a symbol is used for multiple concepts, rename one.
4. **Match LaTeX rendering**: use `\bm{}` for bold vectors only if loaded; otherwise `\boldsymbol{}`.
5. **Number only referenced equations**: use `\[ ... \]` for unreferenced display math.
6. **Italicize text mode "such that"**: prefer `\text{s.t.}` inside `align` environments.

## Translating Between Models

When extending a deterministic model to stochastic/robust:
1. Identify which parameters become uncertain.
2. Preserve decision variable structure (same $x_{p\ell}$).
3. Add scenario index or uncertainty set.
4. Update objective to expected value, worst-case, or risk-averse functional.
5. Add recourse variables for second-stage decisions (stochastic) or robust counterpart constraints.

### Example: SLAP → Stochastic SLAP

Deterministic:
$$\min \sum_{p,\ell} (f_p c_\ell + \beta d_p / V_\ell) x_{p\ell}$$

Stochastic (two-stage):
$$\min \sum_{p,\ell} f_p c_\ell x_{p\ell} + \sum_{s} \pi^s \beta \sum_{p,\ell} d_p^s x_{p\ell} / V_\ell$$

Robust (budget $\Gamma$):
$$\min_x \max_{d \in \mathcal{U}(\Gamma)} \sum_{p,\ell} (f_p c_\ell + \beta d_p / V_\ell) x_{p\ell}$$

## Verification Checklist

Before publishing a formulation:

- [ ] All sets, indices, parameters, variables defined in a "Notation" table.
- [ ] Constraints fully capture the problem (no missing constraints).
- [ ] Objective function justified by operational reasoning.
- [ ] Units consistent throughout.
- [ ] Domain constraints (binary, integer, continuous) explicit.
- [ ] Equation labels for all referenced equations.
- [ ] LaTeX compiles cleanly.
- [ ] Notation matches prior chapters (or any deviation is justified).

## When to Invoke This Skill
- Defining a new optimization model
- Extending an existing model (deterministic → stochastic → robust)
- Standardizing notation across chapters
- Writing a methodology section requiring formal formulations
- Verifying consistency of mathematical notation in a chapter draft
