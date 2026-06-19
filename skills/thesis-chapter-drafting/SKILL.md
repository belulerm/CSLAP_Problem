---
name: thesis-chapter-drafting
description: Draft a complete PhD thesis chapter following UTC manuscript standards. Use when writing new chapters or substantial sections. Ensures proper structure, academic tone, and integration with template conventions from Templates_PhD_Thesis_Manuscripts_UTC.
---

# Thesis Chapter Drafting

## Purpose
Produce chapter-length thesis content (15–40 pages) that meets UTC doctoral standards: rigorous, comprehensive, well-structured, and integrated with the broader thesis narrative.

## Pre-Drafting Checklist

Before writing any prose:

1. **Identify chapter role** in the thesis arc:
   - Where does this chapter sit (foundation, methods, results, synthesis)?
   - What does the previous chapter establish?
   - What must this chapter set up for the next chapter?

2. **Review template structure**: 
   - Read corresponding chapter in `Templates_PhD_Thesis_Manuscripts_UTC/An_Extension_of_Energetic_Reasoning_..._RCPSP/`.
   - Note section hierarchy, pacing, use of figures/algorithms/theorems.

3. **Confirm scope**: Is this chapter about a single contribution or a unified theme covering multiple contributions?

4. **List required components**:
   - Problem definition / mathematical formulation
   - Literature positioning (related work)
   - Methodology / algorithm description
   - Theoretical analysis (proofs, complexity)
   - Experimental validation (data, results, comparisons)
   - Discussion / limitations
   - Bridge to next chapter

## Chapter Skeleton Template

```latex
\chapter{<Chapter Title>}
\minitoc  % chapter-level table of contents (UTC convention)

% Opening paragraph: contextualizes the chapter within the thesis
\textcolor{black}{This chapter [introduces/extends/analyzes] ... 
We first ..., then ..., and finally demonstrate that ...}

\section{Introduction}
% Establish the specific problem this chapter addresses.
% Connect to the prior chapter's results.
% State the chapter's contributions explicitly.

\section{Problem Formulation}
% Define notation, sets, variables, parameters.
% Present the formal mathematical model.
% Discuss assumptions and their justification.

\section{Related Work}
% Position contribution against state-of-the-art.
% Identify gaps that motivate this work.
% Use \cite{...} with verified BibTeX keys.

\section{Proposed Approach}
% Describe methodology in detail.
% Include pseudocode with \begin{algorithm} ... \end{algorithm}.
% Provide complexity analysis.

\section{Theoretical Properties}
% State and prove key theorems/lemmas.
% Discuss correctness, optimality, convergence.

\section{Experimental Evaluation}
% Describe instances, parameters, hardware.
% Present results in tables/figures.
% Compare against baselines.

\section{Discussion}
% Interpret results.
% Acknowledge limitations.
% Identify open questions.

\section{Conclusion}
% Summarize contributions.
% Bridge to next chapter.
```

## Writing Principles

### Tone
- **Formal, third-person, present tense** for definitions and results: "The model assigns each product to exactly one location."
- **Past tense** for experimental descriptions: "We evaluated the heuristic on 100 instances."
- **Active voice** preferred over passive when describing contributions: "We propose a hybrid heuristic" rather than "A hybrid heuristic is proposed."
- Avoid first-person singular ("I"); use first-person plural ("we") sparingly, only for novel contributions.

### Pacing
- Each section should advance the chapter's argument.
- Avoid micro-sections (less than half a page); merge if too granular.
- Avoid macro-sections (more than 10 pages); split if too large.
- One main idea per paragraph; one chapter per major contribution.

### Mathematical Rigor
- Define every symbol before use.
- Use `\mathcal{}` for sets, `\mathbf{}` or `\bm{}` for vectors, plain math italic for scalars.
- Number equations only if referenced (`\begin{equation}` vs. `\[ ... \]`).
- Proofs end with `\qed` or `\square`.

### Figures & Tables
- Caption above tables (UTC convention) or below figures.
- Reference every figure/table in the prose at least once.
- Use `booktabs` for tables (no vertical lines).
- TikZ for diagrams; vector graphics (PDF/EPS) for plots.

## Connecting to the Thesis Arc

### Bridges
At chapter transitions, explicitly link:
- Start: "Having established X in Chapter N, we now extend Y by introducing Z."
- End: "The results of this chapter motivate the consideration of W, which we develop in Chapter N+1."

### Avoiding Repetition
- Do not redefine terms already defined in earlier chapters; cite them: "Recall from Section 2.3 that..."
- Do not repeat literature review across chapters; centralize in Chapter 2.
- Do not re-derive results; reference and use.

## Self-Review Checklist

Before considering a chapter draft complete:

- [ ] Every claim is supported by proof, citation, or experimental evidence.
- [ ] Every theorem/lemma has a complete proof or a clear reference.
- [ ] Every algorithm has a complexity analysis.
- [ ] Every figure/table is referenced and explained.
- [ ] Every citation key exists in `bibl_these_utc_ro.bib`.
- [ ] Smooth bridge from previous chapter; setup for next chapter.
- [ ] Sparring partner review applied (see `sparring-partner-review` skill).
- [ ] No undefined symbols, broken references, or compilation errors.
- [ ] Word/page count appropriate (~15–40 pages of substantive content).

## When to Invoke This Skill
- Starting a new chapter from scratch
- Major revision of an existing chapter
- Restructuring chapter to match UTC template flow
- Integrating multiple research outputs into a single chapter
