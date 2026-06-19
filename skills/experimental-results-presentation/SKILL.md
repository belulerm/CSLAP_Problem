---
name: experimental-results-presentation
description: Present experimental results with rigorous statistics, clear figures, and complete tables. Use when reporting optimization benchmarks, comparing solvers, or analyzing computational experiments in the thesis. Ensures reproducibility and statistical validity.
---

# Experimental Results Presentation

## Purpose
Produce rigorous experimental sections that meet doctoral standards: statistically valid, reproducible, fairly comparing methods, and visually clear. Apply to all experimental chapters (SLAP, CSLAP, MSLAP, stochastic, robust, ML).

## Experimental Design Principles

### 1. Reproducibility
Document everything needed to replicate the experiments:
- **Hardware**: CPU model, RAM, OS, threading configuration.
- **Software**: Solver versions (Hexaly X.Y, Gurobi X.Y, CPLEX X.Y, OR-Tools X.Y), Python version, library versions.
- **Random seeds**: Fixed seeds for stochastic algorithms.
- **Data**: Source (real / synthetic), size, distribution, preprocessing.
- **Parameters**: All hyperparameters, time limits, tolerances.

### 2. Fair Comparison
- Same time budget across all methods.
- Same hardware for all runs.
- Same problem instances (don't compare on cherry-picked ones).
- Identical tuning effort for proposed method and baselines.
- Document baselines clearly: published version (with citation) or your reimplementation.

### 3. Statistical Validity
- Multiple runs per instance with different seeds (≥30 for statistical tests, ≥5 for averaged metrics).
- Report mean and standard deviation (or median and IQR).
- Use paired statistical tests (Wilcoxon signed-rank) for comparing methods.
- Report effect size (not just p-values).
- Confidence intervals (95%) for headline numbers.

## Structure of an Experimental Section

```latex
\section{Experimental Evaluation}

\subsection{Setup}
% Hardware, software, parameter values, instance generation.

\subsection{Instances}
% Real / synthetic, sizes, characteristics.

\subsection{Methods Compared}
% Proposed method + baselines, each cited.

\subsection{Metrics}
% Cost, runtime, optimality gap, etc.

\subsection{Results}
% Tables and figures.

\subsection{Analysis}
% What do the results mean? Why does the method work?

\subsection{Limitations}
% Where does the method underperform?
```

## Tables

### Standard Comparison Table
```latex
\begin{table}[h]
\centering
\caption{Performance comparison on benchmark instances. Best results in bold; second-best underlined.}
\label{tab:slap-comparison}
\begin{tabular}{lrrrrr}
\toprule
Instance & $|\mathcal{P}|$ & $|\mathcal{L}|$ & Gurobi & Heuristic & Hexaly \\
\midrule
Small-1  & 50   & 100   & \textbf{124.3} & 126.7 & \underline{125.1} \\
Small-2  & 80   & 150   & \textbf{198.5} & 203.2 & \underline{199.8} \\
Medium-1 & 500  & 1000  & 1245.7 & \textbf{1198.4} & \underline{1210.3} \\
Medium-2 & 800  & 1500  & TLE    & \textbf{1876.2} & 1923.8 \\
Large-1  & 5000 & 10000 & TLE    & \textbf{12453.1} & 12891.4 \\
\bottomrule
\end{tabular}
\end{table}
```

**Conventions**:
- `booktabs` for clean horizontal rules; no vertical rules.
- Bold for best, underline for second-best (define in caption).
- `TLE` (Time Limit Exceeded) for runs that don't terminate.
- `NA` for not applicable.
- Numeric alignment via `\siunitx` `S` columns for decimal alignment.

### Detailed Statistics Table
```latex
\begin{table}[h]
\centering
\caption{Mean cost over 30 runs (95\% CI in parentheses). p-value from Wilcoxon signed-rank test vs. proposed method.}
\begin{tabular}{lrr}
\toprule
Method & Mean Cost (CI) & p-value \\
\midrule
Baseline-A & 1245.7 (1230.2, 1261.2) & 0.003 \\
Baseline-B & 1238.5 (1224.1, 1252.9) & 0.012 \\
Proposed   & \textbf{1198.4} (1185.7, 1211.1) & --- \\
\bottomrule
\end{tabular}
\end{table}
```

## Figures

### Cost Evolution Plot
- X-axis: time (or iteration).
- Y-axis: cost (lower is better) or improvement %.
- Lines: one per method, with confidence bands.
- Legend: method names matching the table.
- Use vector graphics (PDF or EPS).

### Pareto Frontier (Multi-Objective)
- X-axis: economic cost.
- Y-axis: environmental impact (CO2e).
- Points: solutions at different $\lambda$ values.
- Connect with a line to show frontier.
- Mark the chosen operating point.

### Scaling Plot
- X-axis: instance size ($|\mathcal{P}|$).
- Y-axis: solve time (log scale).
- Lines: methods, with theoretical bounds if applicable.
- Show empirical complexity scaling.

### Best Practices
- Avoid 3D charts unless data genuinely has 3 dimensions.
- Use color-blind-friendly palettes (avoid red/green only).
- Label axes with units (s, kWh, %, etc.).
- Title should describe the experiment, not just the y-axis label.
- Caption explains the takeaway, not just what the figure shows.

## Metrics for SLAP-Family Problems

### Primary Metrics
- **Total cost**: weighted sum of picking and replenishment.
- **Picking cost**: $\sum_p f_p \cdot c_{\sigma(p)}$.
- **Replenishment cost**: $\sum_p \beta \cdot d_p / V_{\sigma(p)}$.
- **Number of stations traversed** (CSLAP).
- **Carbon footprint** (kg CO2e) for sustainability extensions.

### Algorithmic Metrics
- **Solve time** (seconds).
- **Optimality gap**: $(z - z^*) / z^* \cdot 100\%$ where $z^*$ is best known (LP bound or exact solver).
- **Iterations to convergence** (heuristics).
- **Number of variables / constraints** (model size).
- **Memory usage** (MB).

### Quality Metrics (Stochastic / Robust)
- **In-sample cost**: cost on training scenarios.
- **Out-of-sample cost**: cost on held-out scenarios (CRITICAL).
- **Worst-case cost** (robust): $\max_{u \in \mathcal{U}} c(u)$.
- **Value of Stochastic Solution (VSS)**: benefit over deterministic solution.
- **Price of Robustness**: cost of conservatism.

## Analysis Section

For each result, address:
1. **What does the table/figure show?** Describe the pattern.
2. **Why does this pattern appear?** Connect to the algorithm's design.
3. **What is the practical implication?** When should one use this method?
4. **What is the limitation?** When does the method underperform?

### Example Analysis Paragraph
> Table~\ref{tab:slap-comparison} shows that the proposed heuristic outperforms Gurobi on instances with $|\mathcal{P}| > 500$ within the 1-hour time budget. This is consistent with the heuristic's $O(I \cdot K \cdot n)$ scaling versus Gurobi's exponential worst-case behavior on integer programs. The advantage diminishes on small instances where Gurobi achieves optimality within seconds. The practical takeaway: for warehouse instances exceeding a few hundred products, the heuristic offers a favorable trade-off between solution quality and runtime.

## Anti-Patterns to Avoid

- ❌ Reporting only best-case results (omit failures).
- ❌ Comparing against weak baselines (strawmen).
- ❌ Time-limited runs without disclosure of limit.
- ❌ Different hyperparameter tuning effort for proposed vs. baseline.
- ❌ "Significantly better" without statistical test.
- ❌ p-values without effect size or magnitude.
- ❌ Figures with unlabeled axes or missing legends.
- ❌ Tables that don't fit in the page width.
- ❌ Conclusions stronger than the data supports.

## Reporting Checklist

Before finalizing experimental section:

- [ ] Hardware and software fully specified.
- [ ] All hyperparameters reported.
- [ ] Random seeds disclosed.
- [ ] Baselines competitive (state-of-the-art, recently published).
- [ ] Statistical tests applied where relevant.
- [ ] Confidence intervals or standard deviations reported.
- [ ] Figures have axis labels, legends, captions.
- [ ] Tables use `booktabs` style, clear notation.
- [ ] Analysis explains *why*, not just *what*.
- [ ] Limitations honestly acknowledged.
- [ ] Data and code accessible (if open-sourced) — provide repository link.

## When to Invoke This Skill
- Writing an experimental section of a chapter.
- Designing benchmark experiments.
- Preparing tables and figures from raw experimental data.
- Defining metrics for a new optimization problem.
- Conducting statistical comparisons between solvers.
- Reviewing experimental rigor of a draft chapter.
