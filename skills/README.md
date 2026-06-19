# PhD Thesis Skills

This directory contains skills that Claude Code can invoke to support specific tasks in the PhD thesis workflow. Each skill is a self-contained, focused capability defined by a `SKILL.md` file.

## Available Skills

### Drafting & Writing
| Skill | Purpose |
|-------|---------|
| [`thesis-chapter-drafting`](./thesis-chapter-drafting/SKILL.md) | Draft a complete thesis chapter following UTC standards |
| [`mathematical-formulation`](./mathematical-formulation/SKILL.md) | Formulate optimization problems with rigorous notation |
| [`algorithm-documentation`](./algorithm-documentation/SKILL.md) | Document algorithms with pseudocode and complexity analysis |
| [`experimental-results-presentation`](./experimental-results-presentation/SKILL.md) | Present experimental results with rigorous statistics |

### Uncertainty Modeling
| Skill | Purpose |
|-------|---------|
| [`stochastic-modeling`](./stochastic-modeling/SKILL.md) | Build stochastic optimization models (two-stage, SAA, CVaR) for probabilistic uncertainty |
| [`robust-modeling`](./robust-modeling/SKILL.md) | Build robust optimization models (uncertainty sets, robust counterparts, C&CG) for set-based uncertainty |

### Sources & Citations
| Skill | Purpose |
|-------|---------|
| [`literature-review-citation`](./literature-review-citation/SKILL.md) | Manage citations and BibTeX entries |
| [`french-to-english-synthesis`](./french-to-english-synthesis/SKILL.md) | Synthesize French sources into English |

### Review & Critique
| Skill | Purpose |
|-------|---------|
| [`sparring-partner-review`](./sparring-partner-review/SKILL.md) | Critically review thesis content with intellectual rigor |

### Build & Maintenance
| Skill | Purpose |
|-------|---------|
| [`latex-thesis-build`](./latex-thesis-build/SKILL.md) | Compile and debug the LaTeX manuscript |

### Project Navigation
| Skill | Purpose |
|-------|---------|
| [`graphify`](./graphify/SKILL.md) | Build a persistent knowledge graph of the project for token-efficient agent navigation |

## Composing Skills into Workflows

Skills are designed to compose. Below are common multi-skill workflows.

### Workflow 1: Drafting a New Chapter
```
1. thesis-chapter-drafting    → produce chapter skeleton and structure
2. mathematical-formulation   → add formal problem definitions
3. literature-review-citation → integrate prior work with verified citations
4. algorithm-documentation    → describe algorithms with pseudocode
5. experimental-results-presentation → add tables/figures from data
6. sparring-partner-review    → critical review before finalizing
7. latex-thesis-build         → compile and verify the chapter
```

### Workflow 2: Integrating a French Paper
```
1. french-to-english-synthesis → translate and synthesize the paper
2. literature-review-citation  → add BibTeX entry and cite properly
3. thesis-chapter-drafting     → integrate into the relevant chapter
4. sparring-partner-review     → check that the integration is rigorous
```

### Workflow 3: Adding a New Algorithm Chapter
```
1. mathematical-formulation   → define the problem
2. algorithm-documentation    → write pseudocode and complexity
3. experimental-results-presentation → benchmark experiments
4. thesis-chapter-drafting    → assemble into chapter format
5. sparring-partner-review    → critique methodology and claims
6. latex-thesis-build         → verify compilation
```

### Workflow 4: Pre-Submission Review
```
1. sparring-partner-review    → critique every chapter
2. literature-review-citation → verify all citations resolve
3. latex-thesis-build         → clean build and pre-submission verification
```

### Workflow 5: Drafting an Uncertainty Chapter (Stochastic or Robust)
```
1. mathematical-formulation                → define notation extending the deterministic model
2. stochastic-modeling OR robust-modeling  → build the uncertainty formulation
3. algorithm-documentation                 → describe SAA/Benders (stochastic) or C&CG/ADR (robust)
4. experimental-results-presentation       → compare against deterministic and across uncertainty paradigms
5. literature-review-citation              → cite foundational works (Birge-Louveaux, Ben-Tal-Nemirovski, etc.)
6. sparring-partner-review                 → test distributional/uncertainty-set assumptions for rigor
7. latex-thesis-build                      → compile and verify
```

### Workflow 6: Cross-Paradigm Comparison (Stochastic vs. Robust)
```
1. stochastic-modeling                     → formulate stochastic version
2. robust-modeling                         → formulate robust version
3. experimental-results-presentation       → evaluate both on adversarial and random scenarios
4. sparring-partner-review                 → critique which paradigm is appropriate for the warehouse setting
```

## Invoking Skills

In Claude Code, skills are invoked via the Skill tool:
```
Skill(skill="thesis-chapter-drafting", args="draft chapter 4 on stochastic optimization")
```

Or by referencing them in conversation:
> "Use the `mathematical-formulation` skill to define the robust SLAP."

## Adding New Skills

To create a new skill:
1. Create a subdirectory under `.claude/skills/<skill-name>/`.
2. Add a `SKILL.md` file with YAML frontmatter (name, description) and Markdown body.
3. Update this README's index table.
4. Reference the skill in `CLAUDE.md` if it's core to the workflow.

### Skill File Template
```markdown
---
name: <kebab-case-name>
description: <one-sentence description of when to use this skill>
---

# Skill Title

## Purpose
<what this skill achieves>

## Core Principles / Approach
<the key operating rules>

## Workflow
<step-by-step usage>

## When to Invoke This Skill
- <trigger 1>
- <trigger 2>
```

## Relationship to CLAUDE.md

- `CLAUDE.md` (in the project root) sets the **overall context, constraints, and architecture**.
- Skills (here) provide **task-specific operational guidance**.
- Skills assume CLAUDE.md context is already loaded; they don't re-state it.

## Future Skills (To Be Created)

These skills may be added as the thesis progresses:
- `defense-preparation` — prepare for the thesis defense
- `journal-paper-extraction` — extract a journal paper from a chapter
- `ml-forecasting-integration` — integrate ML predictions into optimization models
- `data-preprocessing` — clean and prepare warehouse data
- `solver-benchmarking` — run head-to-head solver comparisons
- `distributionally-robust-modeling` — hybrid stochastic/robust with ambiguity sets
