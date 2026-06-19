---
name: literature-review-citation
description: Manage citations and BibTeX entries when drafting literature reviews or referencing prior work in the thesis. Use when inserting citations, building related-work sections, or integrating external sources. Ensures proper LaTeX referencing and BibTeX consistency.
---

# Literature Review & Citation Management

## Purpose
Ensure that every citation in the thesis manuscript is grounded in a verified BibTeX entry, that referencing conventions are uniform, and that the literature integration reflects scholarly rigor.

## Core Rules

### 1. Citation Source of Truth
- **Primary BibTeX file**: `bibl_these_utc_ro.bib` (in the thesis directory).
- Only use citation keys that **already exist** in this file.
- Before inserting any `\cite{key}`, verify the key is present.

### 2. Adding Missing References
If a required paper is not in `bibl_these_utc_ro.bib`:
1. Identify the paper type:
   - `@article{...}` — journal papers
   - `@inproceedings{...}` — conference papers
   - `@book{...}` — books and monographs
   - `@incollection{...}` — book chapters
   - `@phdthesis{...}` — doctoral dissertations
   - `@techreport{...}` — technical reports
2. Construct a complete BibTeX entry with these fields:
   - `author`, `title`, `year` (mandatory)
   - `journal`/`booktitle`/`publisher` (type-specific)
   - `volume`, `number`, `pages`, `doi`, `url` (when available)
3. Use a stable, lowercase citation key based on first author + year + topic (e.g., `belul2024slap`, `erschler1990energetic`).
4. Append the entry to `bibl_these_utc_ro.bib` (do not modify existing entries).
5. Verify the entry compiles correctly with `biber`.

### 3. Citation Style & Grouping
- **Multiple citations together**: `\cite{key1, key2, key3}` — order alphabetically or chronologically.
- **Page references**: `\cite[p.~42]{key}` for specific pages.
- **Author-prominent citations**: `\textcite{key}` if using `biblatex` author-year style.
- **Footnote citations**: avoid; integrate into running text.

### 4. Topical Distinction — Uncertainty Types
When citing work on uncertainty, maintain clear distinctions between:
- **Stochastic uncertainty**: probabilistic distributions known (e.g., demand follows a known distribution).
- **Robust/parametric uncertainty**: bounded parameter ranges without distributions (uncertainty sets).
- **Machine learning forecasting**: data-driven prediction with confidence intervals.
- **Fuzzy uncertainty**: linguistic/imprecise information.

Do not conflate these in the same paragraph without explicit explanation. Each citation should be situated in the correct uncertainty framework.

## Workflow

### Before Drafting a Section
1. Read the relevant chapter of the thesis to understand the argument structure.
2. Scan `bibl_these_utc_ro.bib` for available citation keys on the topic.
3. Identify gaps — papers that should be cited but are missing.
4. Add missing entries before drafting (avoid disruption later).

### While Writing
- Cite at the end of claims, not at the start of sentences.
- Use 1–3 citations per claim; more suggests survey writing, fewer suggests undersupport.
- For seminal works, cite the original (e.g., Erschler & Lopez 1990 for Energetic Reasoning).
- For state-of-the-art comparisons, cite the most recent peer-reviewed source.

### After Writing
1. Run `biber main` and check for unresolved citations.
2. Verify all citation keys in the chapter exist in the .bib file.
3. Check formatting in the compiled PDF — author names, journal abbreviations, page ranges.

## Anti-Patterns to Avoid

- ❌ Inventing citation keys without verifying their existence
- ❌ Citing papers you haven't read (use only verified sources)
- ❌ Citation dumping (`\cite{a, b, c, d, e, f, g, h}` without justification)
- ❌ Mixing uncertainty types without clear framing
- ❌ Modifying existing BibTeX entries (append new ones instead)
- ❌ Using inconsistent citation key formats (e.g., `Belul2024` and `belul_2024_slap` in the same .bib)

## When to Invoke This Skill
- Drafting a literature review chapter or section
- Adding references to a methodology section
- Building a "Related Work" comparison table
- Synthesizing French-language papers into English citations (combine with `french-to-english-synthesis` skill)
- Compiling the final bibliography before submission
