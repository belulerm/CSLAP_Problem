---
name: caveman-review
description: Ultra-compressed code review comments. Cuts noise from PR feedback while preserving the actionable signal. Each comment is one line: location, problem, fix. Use when user says "review this PR", "code review", "review the diff", "/review", or invokes /caveman-review.
---

# Caveman Review

## Purpose
Write code review comments terse and actionable. One line per finding. Location, problem, fix. No conversational preamble.

## Activation
Triggered when user says "review this PR", "code review", "review the diff", "/review", or invokes `/caveman-review`. Auto-triggers during the code-review pipeline step.

## Rules
* **Format**: `L<line>: <problem>. <fix>.` — or `<file>:L<line>: ...` when reviewing multi-file diffs.
* **Severity Prefix**:
  - `🔴 bug:` — broken behavior, will cause incident/failure.
  - `🟡 risk:` — works but fragile (race condition, missing null check, swallowed error).
  - `🔵 nit:` — style, naming, micro-optimization. Author can choose to ignore.
  - `❓ q:` — genuine question, not a suggestion.
* **Drop**:
  - "I noticed that...", "It seems like...", "You might want to consider..."
  - "Great work!", "Looks good overall but..." — state it once at the top, not per comment.
  - Hedging ("perhaps", "maybe", "I think"). If unsure, use `❓ q:`.
* **Keep**:
  - Exact line numbers.
  - Exact symbol/function/variable names in backticks.
  - Concrete fixes, not vague suggestions like "consider refactoring".

## Examples
* **Yes**: `L102: 🔴 bug: Division by zero possible when speed is 0. Add guard: if speed == 0: return.`
* **Yes**: `cg_synthetic.py:L45: 🔵 nit: Unused import `time`. Remove.`
