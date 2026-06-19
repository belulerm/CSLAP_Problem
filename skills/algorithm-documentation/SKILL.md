---
name: algorithm-documentation
description: Document algorithms with pseudocode, complexity analysis, and correctness arguments. Use when describing a heuristic, exact method, or hybrid algorithm in the thesis. Produces algorithm2e-compatible LaTeX with rigorous complexity discussion.
---

# Algorithm Documentation

## Purpose
Produce publication-quality algorithm descriptions that combine clear pseudocode, complexity analysis, and correctness/optimality discussion. All algorithms should be reproducible from the documentation alone.

## Pseudocode Standard (algorithm2e)

Use the `algorithm2e` package with `ruled, vlined, linesnumbered` options (already set in UTC template).

### Template

```latex
\begin{algorithm}[H]
\caption{Heuristic SLAP Solver with Local Search}
\label{alg:slap-heuristic}
\KwIn{Products $\mathcal{P}$, locations $\mathcal{L}$, frequencies $\{f_p\}$, costs $\{c_\ell\}$}
\KwOut{Assignment $\sigma: \mathcal{P} \to \mathcal{L}$}

$\sigma \leftarrow$ \texttt{HungarianAssign}($\mathcal{P}, \mathcal{L}$)\;
$\sigma^* \leftarrow \sigma$\;
\For{$\text{iter} = 1$ \KwTo $\text{MaxIter}$}{
    $\mathcal{S} \leftarrow$ \texttt{TopKCandidatePairs}($\sigma$, $K$)\;
    \ForEach{$(p_1, p_2) \in \mathcal{S}$}{
        $\sigma' \leftarrow \texttt{Swap}(\sigma, p_1, p_2)$\;
        \If{$\text{cost}(\sigma') < \text{cost}(\sigma)$}{
            $\sigma \leftarrow \sigma'$\;
        }
    }
    \If{$\text{cost}(\sigma) < \text{cost}(\sigma^*)$}{
        $\sigma^* \leftarrow \sigma$\;
    }
    \If{convergence criterion met}{
        \Return $\sigma^*$\;
    }
}
\Return $\sigma^*$\;
\end{algorithm}
```

### Conventions

- **Inputs/Outputs**: Use `\KwIn{...}` and `\KwOut{...}`.
- **Loops**: `\For`, `\While`, `\ForEach`.
- **Conditionals**: `\If`, `\ElseIf`, `\Else`.
- **Comments**: `\tcp{...}` (end-of-line) or `\tcc{...}` (comment line).
- **Functions**: Reference subroutines with `\texttt{FuncName}(...)`.
- **Return**: `\Return value\;`.
- **Mathematical assignment**: `$\leftarrow$` (not `=`).

## Complexity Analysis

Every algorithm must include a complexity section.

### Components

1. **Time complexity**: Big-O of the overall algorithm and key subroutines.
2. **Space complexity**: Memory required (especially for cost matrices, scenarios).
3. **Iteration count**: For iterative methods, bound the number of iterations.
4. **Per-iteration cost**: Cost of one outer loop pass.

### Example Statement

> **Theorem 3.4** (Complexity of Algorithm 3.1).
> Algorithm 3.1 runs in $O(I \cdot K \cdot (|\mathcal{P}| + |\mathcal{L}|))$ time, where $I$ is the maximum number of iterations and $K$ is the candidate pool size. Space complexity is $O(|\mathcal{P}| \cdot |\mathcal{L}|)$ for the cost matrix.

### Proof Sketch
> The initial Hungarian assignment costs $O(n^3)$ where $n = \min(|\mathcal{P}|, |\mathcal{L}|)$. Each iteration evaluates $K$ candidate swaps; each swap evaluation is $O(1)$ if the cost matrix is precomputed. Convergence is bounded by $I$ iterations. $\square$

## Correctness & Optimality Arguments

### For Exact Methods
- State the optimality result formally (theorem + proof).
- Demonstrate that all constraints are satisfied.
- Compare against known optimal value or LP relaxation bound.

### For Heuristics
- Describe what the heuristic guarantees (e.g., local optimality, feasibility).
- Acknowledge what it does *not* guarantee (global optimality).
- Provide empirical evidence of quality (gap to LP bound, comparison to exact solver on small instances).

### For Hybrid Methods
- Identify the exact components (e.g., MIP solver on subproblem).
- Identify the heuristic components (e.g., neighborhood selection).
- Explain how they interact and what overall guarantees emerge.

## Algorithm Description Structure

For each algorithm in the thesis, include:

```latex
\subsection{Algorithm: [Name]}

\paragraph{Overview.}
% 2-3 sentences describing the high-level idea and motivation.

\paragraph{Notation.}
% Reference earlier-defined notation; introduce algorithm-specific symbols.

% Insert \begin{algorithm} ... \end{algorithm}

\paragraph{Description of key steps.}
% Walk through the pseudocode, explaining non-obvious lines.
% Reference line numbers: "In line 5, we ..."

\paragraph{Complexity.}
% Theorem + proof sketch.

\paragraph{Correctness / Optimality.}
% Formal guarantees, with proof or reference to proof.

\paragraph{Implementation notes.}
% Practical details: data structures, libraries, parallelization.
```

## Common Algorithms in This Thesis

### Deterministic
- **Hungarian Algorithm** (`scipy.optimize.linear_sum_assignment`): $O(n^3)$
- **Greedy Initial Assignment**: $O(|\mathcal{P}| \cdot |\mathcal{L}|)$
- **Local Search with Top-K Swaps**: heuristic, depends on $K$ and iteration count

### Combinatorial / Set-Based
- **Community Detection (CSLAP)**: graph-based, depends on graph size
- **MiniSLAP per Station**: small-scale assignment, $O(s^3)$ per station of size $s$

### Stochastic
- **Sample Average Approximation (SAA)**: $O(|\mathcal{S}| \cdot \text{deterministic cost})$
- **Progressive Hedging**: iterative, depends on scenario tree

### Robust
- **Bertsimas–Sim Robust Counterpart**: reformulation to LP/MIP
- **Column-and-Constraint Generation**: iterative master-subproblem

### Solvers Used
- **Hexaly** (commercial, license required)
- **Gurobi / CPLEX** (commercial)
- **OR-Tools** (open-source)
- **scipy.optimize** (open-source)

## Anti-Patterns to Avoid

- ❌ Pseudocode in plain prose ("First we do X, then Y") — use the algorithm environment.
- ❌ Vague complexity claims ("This is fast") — provide Big-O.
- ❌ Missing input/output specification.
- ❌ Implementation details disguised as algorithm steps (separate "Implementation notes").
- ❌ Magic constants in pseudocode without explanation (define and justify).

## When to Invoke This Skill
- Documenting a new algorithm in a chapter
- Standardizing pseudocode style across the thesis
- Writing a methodology section with multiple algorithms
- Preparing algorithm appendix with full pseudocode and proofs
- Reviewing an existing algorithm description for completeness
