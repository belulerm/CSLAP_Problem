---
name: latex-thesis-build
description: Compile, debug, and maintain the LaTeX thesis manuscript. Use when handling compilation errors, BibLaTeX/Biber issues, broken references, missing figures, or template configuration. Knows the UTC preamble conventions.
---

# LaTeX Thesis Build

## Purpose
Manage compilation, debugging, and maintenance of the multi-file LaTeX thesis manuscript. Ensure consistent, error-free output for review and final submission.

## Standard Build Workflow

### Full Compilation (with bibliography)
```bash
pdflatex main.tex
biber main
pdflatex main.tex
pdflatex main.tex
```

The four-pass workflow ensures:
1. First `pdflatex`: generates `.aux` with citation keys, builds initial structure.
2. `biber`: resolves citations against `references.bib` (or `bibl_these_utc_ro.bib`).
3. Second `pdflatex`: integrates bibliography, resolves `\cite{}`.
4. Third `pdflatex`: finalizes cross-references (`\ref{}`, page numbers, TOC).

### Quick Compilation (no bibliography changes)
```bash
pdflatex main.tex
```

Use when editing prose; skip `biber` if no new citations.

### Clean Build (remove auxiliary files)
```bash
rm -f *.aux *.bbl *.bcf *.blg *.log *.out *.toc *.lot *.lof *.run.xml *.synctex.gz
rm -f chapters/*.aux  # if chapters are in subdirectories
pdflatex main.tex
biber main
pdflatex main.tex
pdflatex main.tex
```

Use when:
- Switching between major template versions.
- Encountering inexplicable cross-reference errors.
- Preparing a fresh build for submission.

## Common Errors & Fixes

### 1. Citation `??` Appears in PDF
**Cause**: Citation key not resolved by Biber.

**Fix**:
- Verify the key exists in the .bib file.
- Run `biber main` after `pdflatex`.
- Check `main.log` for "missing entry" warnings.
- Ensure `.bib` file is in the path declared by `\addbibresource{...}`.

### 2. Reference `??` Appears in PDF
**Cause**: `\ref{label}` does not match any `\label{label}`.

**Fix**:
- Search the manuscript for the exact label.
- Check capitalization (labels are case-sensitive).
- Run `pdflatex` twice — references need a second pass to resolve.
- Check for stray characters in label names (avoid spaces, special chars).

### 3. Missing Figure: "File `X.pdf' not found"
**Cause**: Graphics path or filename mismatch.

**Fix**:
- Verify `\graphicspath{ {figures/} }` (or relevant path) in preamble.
- Confirm the figure file is in the declared directory.
- Check extension: `\includegraphics` defaults to PDF; explicit `\includegraphics{file.png}` if PNG.

### 4. Algorithm Environment Errors
**Cause**: `algorithm2e` package conflicts or syntax errors.

**Fix**:
- Ensure package loaded: `\usepackage[ruled,vlined,linesnumbered]{algorithm2e}`.
- Common syntax errors:
  - Missing `\;` at line ends inside algorithm.
  - Mismatched `\If` / `\End`.
  - `\KwIn{}` / `\KwOut{}` only at the top of the algorithm.

### 5. Overfull `\hbox` Warnings
**Cause**: Text exceeds line width.

**Fix**:
- Rephrase long words or split sentences.
- Use `\sloppy` for occasional problem paragraphs (sparingly).
- For tables: switch to `tabularx` or reduce font size.

### 6. Underfull `\hbox` Warnings
**Cause**: Bad line spacing, often around figures or equations.

**Fix**:
- Usually safe to ignore unless visible in PDF.
- Adjust paragraph breaks or float placement.

### 7. Biber Error: "Found BibTeX data source"
**Cause**: Biber and BibTeX collision; using wrong backend.

**Fix**:
- Ensure preamble has `\usepackage[backend=biber]{biblatex}`.
- Delete `*.bbl`, `*.bcf`, `*.blg` files.
- Use `biber main`, not `bibtex main`.

### 8. Encoding Errors (Special Characters)
**Cause**: Non-UTF-8 source or missing input encoding.

**Fix**:
- Preamble must include: `\usepackage[utf8]{inputenc}` and `\usepackage[T1]{fontenc}`.
- Save all `.tex` files as UTF-8.
- For Windows files, watch for BOM markers.

## Multi-File Structure

The thesis is split into multiple files for maintainability:

```
main.tex                  % entry point, preamble, \input{} or \include{}
chapters/
  intro.tex               % \chapter{Introduction}
  literature_review.tex   % \chapter{Literature Review}
  slap.tex                % \chapter{SLAP}
  cslap_mslap.tex         % \chapter{CSLAP and MSLAP}
  stochastic.tex          % \chapter{Stochastic Optimization}
  robust.tex              % \chapter{Robust Optimization}
  ml_forecasting.tex      % \chapter{ML Forecasting}
  integrated.tex          % \chapter{Integrated Framework}
  conclusion.tex          % \chapter{Conclusion}
appendices/
  proofs.tex
  experiments.tex
  algorithms.tex
figures/
  *.pdf, *.png, *.eps
references.bib            % or bibl_these_utc_ro.bib
classicthesis-config.tex  % UTC styling
```

### Inclusion Syntax
- `\input{chapters/intro}` — verbatim inclusion, no page break.
- `\include{chapters/intro}` — page break before, allows `\includeonly{}` for selective compilation.

### Selective Compilation
For faster iteration on one chapter:
```latex
\includeonly{chapters/slap}
```
Other chapters' `.aux` files are reused, references stay intact.

## UTC Template Specifics

### Required Packages (from template)
```latex
\documentclass[a4paper,12pt,twoside,english]{book}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage{babel}
\usepackage[a4paper,left=3cm,right=2.5cm,top=3cm,bottom=3cm,twoside]{geometry}
\usepackage{xcolor, stmaryrd, amssymb, amsmath, libertine}
\usepackage{hyperref}
\usepackage[backend=biber,style=numeric,sorting=none,maxbibnames=99,maxcitenames=1,doi=true,url=false]{biblatex}
\usepackage{graphicx, caption, subcaption, float}
\usepackage{multirow, array, tabularx, booktabs, longtable}
\usepackage{minitoc, tikz, fancyhdr}
\usepackage[strict]{changepage}
\usepackage{siunitx}
\usepackage[ruled,vlined,linesnumbered]{algorithm2e}
\usepackage{enumitem, epigraph}
```

### Language Switch
Note: the existing UTC template has `\selectlanguage{french}` — for an English thesis, change to:
```latex
\selectlanguage{english}
```
Or use the document class option `english` and remove the `\selectlanguage` call.

### Front Matter / Main Matter / Back Matter
```latex
\frontmatter   % Roman numerals, title page, abstract, TOC
\mainmatter    % Arabic numerals, chapters
\backmatter    % Bibliography, index, appendices
```

## Pre-Submission Build

Before submitting the final manuscript:

1. Clean build (remove all aux files).
2. Full 4-pass compilation.
3. Verify:
   - [ ] No `??` for citations or references.
   - [ ] All figures render correctly.
   - [ ] TOC, LOF, LOT are populated.
   - [ ] Page numbering correct (Roman for front, Arabic for main).
   - [ ] Bibliography is complete and formatted consistently.
   - [ ] No overfull/underfull warnings in critical sections.
4. Generate final PDF; check on multiple PDF readers.
5. Verify file size is reasonable (large PDFs may need image compression).

## Maintenance Tasks

### Updating the BibLaTeX Database
- Add new entries to `bibl_these_utc_ro.bib`.
- Run `biber main` to integrate.
- Verify no duplicate keys (Biber will warn).

### Updating Template Conventions
- Avoid altering `main.tex` preamble without authorization.
- For style changes, modify `classicthesis-config.tex` (UTC convention).
- Test changes on a single chapter before applying globally.

### Version Control
- Commit `.tex` files and `.bib` files.
- Ignore auxiliary files: add `*.aux *.bbl *.bcf *.blg *.log *.out *.toc *.lot *.lof *.run.xml *.synctex.gz` to `.gitignore`.
- Optionally commit final PDFs at major milestones (tag commits like `v0.5-draft`).

## When to Invoke This Skill
- LaTeX compilation fails or produces unexpected output.
- Citations or references appear as `??`.
- Figures, tables, or algorithms don't render correctly.
- Adding new chapters or restructuring the document.
- Preparing the manuscript for submission.
- Debugging encoding, font, or formatting issues.
