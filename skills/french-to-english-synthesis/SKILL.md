---
name: french-to-english-synthesis
description: Synthesize French-language source materials (papers, notes, proposals, regulations) into rigorous English for the thesis manuscript. Use when the source language is French but output must be in English. Preserves technical precision while adapting to academic English conventions.
---

# French to English Synthesis

## Purpose
Translate and synthesize French-language source materials into English suitable for a UTC doctoral thesis. The output must be in formal academic English while preserving the technical precision, references, and intellectual content of the original.

## Operating Principle
**The thesis manuscript and ALL conversational output must be in English**, regardless of the language of source materials. French sources are common at UTC (literature, proposals, regulations); they must be ingested and re-expressed in English.

## Translation Approach

### Not Word-for-Word Translation
- Do not produce literal French-to-English conversions.
- Do not preserve French sentence structures (which can feel verbose in English).
- Synthesize: read the French passage, understand its argument, write the equivalent in idiomatic academic English.

### Preserve What Matters
- Technical terms (translate accurately; check glossaries).
- Mathematical content (notation is language-independent).
- Citations (preserve BibTeX keys; if author/title appears in prose, translate the prose but keep the cited work's metadata).
- Logical structure of arguments (premises, evidence, conclusions).

### Adapt What Doesn't Travel
- Academic register: French academic writing tends to be more formal and elaborate; English thesis writing favors precision and concision.
- Sentence length: split long French sentences into multiple English ones for clarity.
- Voice: French prefers passive/impersonal ("Il est nécessaire de..."); English often allows active voice ("We must...").
- Connectors: French uses many connectives (en effet, ainsi, par ailleurs); English uses fewer and prefers structural clarity.

## Glossary: Technical Vocabulary (French → English)

| French | English | Notes |
|--------|---------|-------|
| Logistique | Logistics | |
| Intralogistique | Intralogistics | |
| Entrepôt | Warehouse | |
| Casier | Locker / cubby / bin | Context-dependent; "locker" for robotic, "bin" for storage |
| Emplacement | Location / slot | "Location" preferred in thesis |
| Article / Produit | Article / Product | "Product" preferred for SLAP context |
| Préparation de commandes | Order picking | |
| Réapprovisionnement | Replenishment | |
| Affectation | Assignment | |
| Ordonnancement | Scheduling | |
| Optimisation combinatoire | Combinatorial optimization | |
| Incertitude | Uncertainty | |
| Robustesse | Robustness | |
| Algorithme d'optimisation | Optimization algorithm | |
| Heuristique | Heuristic | |
| Métaheuristique | Metaheuristic | |
| Programmation linéaire | Linear programming | |
| Programmation linéaire en nombres entiers (PLNE) | Integer linear programming (ILP) | |
| Variable de décision | Decision variable | |
| Contrainte | Constraint | |
| Fonction objectif | Objective function | |
| Recherche locale | Local search | |
| Recuit simulé | Simulated annealing | |
| Algorithme génétique | Genetic algorithm | |
| Recherche tabou | Tabu search | |
| Borne inférieure / supérieure | Lower / upper bound | |
| Convergence | Convergence | |
| Cadence | Throughput / rate | Context-dependent |
| Démarche | Approach / methodology | "Approach" preferred |
| État de l'art | State of the art | |
| Cahier des charges | Specifications / requirements | |
| Mémoire de thèse | Thesis manuscript | |
| Soutenance | Defense | |

## Tone Adjustments

### French Academic Style (typical)
> "Il convient de souligner que l'approche proposée permet de tenir compte de manière particulièrement efficace de l'ensemble des contraintes du système de préparation de commandes considéré."

### English Academic Style (preferred)
> "The proposed approach efficiently incorporates all constraints of the order-picking system."

**Changes**:
- Removed introductory throat-clearing ("Il convient de souligner que").
- Active voice with concrete subject ("The proposed approach").
- Concise without losing meaning.

## Handling Specific Source Types

### 1. French Papers / Articles
- Read the abstract and conclusion first to grasp the argument.
- Translate technical content, not stylistic flourishes.
- Cite the original paper (in French) in BibTeX; the prose around it is in English.
- Example: "Erschler and Lopez \cite{erschler1990} introduced energetic reasoning to detect infeasibilities in cumulative scheduling..."

### 2. UTC Internal Documents / Proposals
- May contain administrative language; focus on technical content.
- Synthesize: do not include institutional boilerplate.
- Quote sparingly; paraphrase to fit thesis flow.

### 3. French Code Comments / Documentation
- Translate inline if integrating code into the thesis.
- Update variable names if they were French (e.g., `coût_total` → `total_cost`).

### 4. Industry Documents (Savoye, partners)
- Anonymize sensitive details if required.
- Translate technical specifications precisely.
- Cite as "industrial collaboration with Savoye" or with a specific report number.

## Output Format Guidelines

When producing English output from French sources:

1. **Read the entire passage first** before translating any of it.
2. **Identify the core claim** the passage makes.
3. **Restructure if needed**: a French paragraph may become 2 English paragraphs (or vice versa) for clarity.
4. **Cross-check terminology** against the glossary and earlier chapters.
5. **Preserve citations and equation references** exactly.
6. **Add footnotes** if translating a term whose nuance is lost.

## Common Pitfalls

### False Cognates
- "Sensible" (Fr) = "sensitive" (En), not "sensible"
- "Actuel" (Fr) = "current" (En), not "actual"
- "Eventuellement" (Fr) = "possibly" (En), not "eventually"
- "Important" (Fr) = often "significant" (En), not always "important"

### Over-Translation
- Don't translate proper nouns (Université de Technologie de Compiègne stays UTC).
- Don't translate French names of institutions, labs, projects.
- Don't translate journal/conference titles in citations.

### Under-Translation
- Don't leave French phrases untranslated in the thesis body. If a French phrase is essential, italicize and translate in parentheses: *"par exemple"* (for example).

## Self-Review Checklist

After translating a passage:

- [ ] No French words remain in the English body (except italicized necessary terms).
- [ ] Technical terms use the glossary's preferred English forms.
- [ ] Sentence lengths are reasonable for English academic writing.
- [ ] Active voice is used where appropriate.
- [ ] Citations and references are intact.
- [ ] The argument is preserved (no nuance lost).
- [ ] No false-cognate errors.

## When to Invoke This Skill
- Reading French literature for the thesis literature review
- Synthesizing French proposal documents
- Translating internal UTC notes or meeting summaries
- Adapting French code documentation to English thesis
- Reviewing English thesis text drafted from French sources for fidelity
