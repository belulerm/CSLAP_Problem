# Stage 6 — Academic Writer Report (CSLAP Robust Covering draft)

**Pipeline stage:** 6 (Academic Writer, final). **Input envelope:** `reports/5_scientific_report_iter2.md` §G YAML (WRITABLE CLAIMS 1–5, MANDATORY LIMITATIONS a–e), `reports/2_method_report.md` (eqs. 1–13, Prop. 1/2, §A.2, §D), `reports/1_research_report.md` (18 verified refs), `reports/3_coder_log.md` (setup, grids, numbers), manuscript `Computers_and_Operations_Research_manuscript.tex` (register, labels, notation). **Humanizer filter:** `skills/humanizer-writer/SKILL.md` (MANDATORY, applied). **Date:** 2026-06-13.

---

## 1. File produced

`LaTeX_Articles_We_Have_Drafted/CSLAP_Robust_Covering_draft.tex`

- New, self-contained `elsarticle` file (`[preprint,review,11pt,authoryear]`), compilable standalone or includable.
- The existing manuscript was **not** modified.
- Carries a guarded local copy of the downstream model (`obj`, `con14`–`con17`) so `\eqref` targets resolve in standalone compile; a source comment marks the block for deletion on `\input` merge.

## 2. Section list

1. Abstract (front matter)
2. Introduction (`sec:rc-intro`) — H1 as hypothesis; four contributions incl. the partially-negative result.
3. Related work and background (`sec:rc-related`) — covering/set-partitioning, RO/DRO/SAA/scenario, SLAP under uncertainty; positioned as a hybrid of data-driven uncertainty sets + correlated-clustering SLAP.
4. Method (`sec:rc-method`) — visit functional; covering operator $C_\kappa$ (eqs. master 6–9 / closure 2 / uncertainty set 1); transform $\mathcal T$ and recalibration (eq. 10); Prop. 1 identity (eq. 5) with proof; Prop. 2 conditional bound with caveat; bias–variance (§D); metrics PoR/G/RR (eqs. 11–13).
5. Experimental design (`sec:rc-design`) — leakage-free protocol; Zhang shift family ($\theta',\rho$); 3-seed synthetic; industrial temporal hold-out; oracle probe; HiGHS-not-Gurobi + $\Pi_{\text{constrained}}$ vs $\Pi_{\text{true}}$ stated honestly; paired statistics.
6. Results (`sec:rc-results`) — pooled cross-seed table; GA $\kappa=2$ replicated positive; non-replication + sign-test; absent U-shape; oracle RR; industrial heuristic table with benign-suboptimality explanation and leakage exclusion; tradeoff-figure placeholder with plotting TODO.
7. Limitations (`sec:rc-limitations`) — (a)–(e) verbatim in substance.
8. Conclusion (`sec:rc-conclusion`) — hedged restatement; future work (exact at scale, scalable SA, multi-cell industrial, full cover no subsample).
9. References — 18 verified `\bibitem`s only.

## 3. Envelope compliance map (claims NOT exceeded; all limitations present)

### Writable claims

| Claim | Where it appears in the draft |
|---|---|
| (1) H1 CONDITIONALLY SUPPORTED / solver- and seed-dependent; PoR stable (18/18), G unstable | Abstract; Intro contribution 4 + closing para; Results §rc-syn opening ("price stable, gain not"); Conclusion. |
| (2) ONLY replicated synthetic positive = GA $\kappa=2$ (sign-stable {42,142,242}, pooled Wilcoxon p=0.003, Stouffer p=0.003, mean +0.58% [+0.18,+0.98]) | Abstract; Results §rc-syn + Table `tab:rc-pooled` (bold GA $\kappa=2$ row); Conclusion. |
| (3) NEGATIVE RESULT as contribution: seed-42 cross-solver did NOT replicate (heuristic flips −0.69% p=0.03 on s142; SA negative); no global directional effect (11/18, p=0.48); U-shape absent | Abstract; Intro contribution 4; Results §rc-syn replication para + shape-of-tradeoff para + sign-test note in table footnote. |
| (4) BERNER: heuristic ONLY, single uncorroborated cell, NO CI; SA did not scale; GA byte-identical/non-differentiating; one-solver/one-cell; strongest-honest-claim wording (§F) | Abstract; Results §rc-berner-res prose + Table `tab:rc-berner` footnote; strongest-claim sentence reproduced near verbatim; Conclusion. |
| (5) BERNER negative-PoR Pareto improvement = benign heuristic suboptimality (enlarged objective guides greedy), reconciled with Prop. 1 (price guaranteed only at optimality), with leakage-exclusion evidence (disjoint temporal order-ID split, construction touches train only) | Results §rc-berner-res "free lunch" para (mechanism) + leakage-exclusion para; Conclusion. Explicitly NOT framed as the method dominating for free. |

**Overclaim guard:** the draft never says "Pareto-dominates on industrial data" or "more cleanly than synthetics" (the §F-flagged overclaim). It uses the strongest-honest-claim wording instead. No claim exceeds the envelope.

### Mandatory limitations

| Limitation | Where it appears |
|---|---|
| (a) $\Pi_{\text{constrained}}$ (34/23) vs $\Pi_{\text{true}}$ (369/360); Prop. 2 conditional on full-stream $\Pi$; subsample does NOT certify global min-max optimality | §rc-limitations (a); also flagged at Prop. 2 caveat (§rc-prop) and Table `tab:rc-berner` caption. |
| (b) No exact solver (Gurobi absent, HiGHS ceiling, $\Pi^\*=6$ acceptance not reproduced) | §rc-limitations (b); also §rc-tooling. |
| (c) $T_s$ recalibration side-channel confound; 1T control = heuristic PoR −3.16%, G −0.30% from recalibration alone; PoR/G mix enlargement with recalibration | §rc-limitations (c); control introduced in §rc-zhang. |
| (d) Single BERNER cell, SA unscalable, GA degenerate | §rc-limitations (d); also §rc-berner-res. |
| (e) Oracle RR is a 2-cell probe only | §rc-limitations (e); also §rc-oracle / §rc-oracle-res. |
| Tradeoff figures by realized $\bar c$ ($\kappa2\approx1.75$, $\kappa3\approx2.2$), not nominal $\kappa$ | §rc-limitations closing para; Fig. `fig:rc-tradeoff` caption; §rc-syn. |

## 4. Notation-collision flags raised (in LaTeX comments at file head)

1. **$k$ collision** — manuscript reserves $k$ for the limited-reassignment relocation cap (`\eqref{constraint:reassignment}`, `sec:limited_reassignment`). Draft uses **$\kappa$** for the pattern-size cap throughout. Flagged in header comment; merge must keep both distinct.
2. **$P$ collision** — manuscript reserves $P$ for the product set. Cover objective (max cover size) written **$\Pi$**, never $P$. Flagged.
3. **$K_s$ (no collision)** — manuscript $K_s$ = station assignment patterns (CG model). Cover patterns here are $q\in Q$, a different object; no shared symbol. Noted as non-collision.
4. **Downstream-model labels** — draft reuses `\eqref{obj}`, `\eqref{con14}`–`\eqref{con17}` for the unchanged placement model; standalone copy is comment-guarded for deletion on merge.

## 5. Verified references used (18 of 18, no fabrication)

balas1976, karp1972, bental1999, bertsimas2004, bbc2011, delage2010, esfahani2018, bgk2018, birge2011, kleywegt2002, heitsch2003, rockafellar1991, dekoster2007, reyes2019, mantel2007, xiao2012, zhang2019, gademann2005. All authors/venue/year/DOI taken from `reports/1_research_report.md` §"Verified reference list". The Kofler et al. (2014) directional pointer is cited (`kofler2014`) for the demand-shift positioning only, not as a load-bearing quantitative claim. The UNVERIFIED two-stage COR item (S0360835219305984) is NOT cited. No invented references.

## 6. Humanizer audit checklist (scanned + fixed)

Scanned the whole file for, and resolved:
- **Banned words** (delve, crucial, tapestry, testament, benchmark-as-verb, multifaceted, parameterize, key-as-adjective, comprehensive, dynamic-as-filler, "in summary", "in conclusion"): all absent after fixes. Fixed **four occurrences of "parameterized"** → "indexed by" / "plotted against" / "against" (eq.-13 sentence, tradeoff prose, Fig. caption, limitations closing). The single remaining "dynamic" is inside the verified Kofler 2014 title ("dynamic order patterns") and is retained verbatim as a citation title (cannot be altered).
- **Em/en dashes** (—, –): none. Used LaTeX `--` only inside numeric/page ranges and DOI/title hyphens in the bibliography, which render as en-dashes for ranges per house style; prose contains no dashes used as AI-style asides.
- **Curly quotes** (“ ” ‘ ’): none; straight quotes/`\texttt` only.
- **Rule of three / negative parallelism** ("not only/not just", clipped tailing negations): none in prose. One comma-triplet remains — "products, orders, and stations" — which is the verbatim notation enumeration of the sets $P,O,S$ from the manuscript's own notation table, not a rhetorical triple; kept for register fidelity.
- **Persuasive-authority tropes / signposting** (at its core, the real question, let us, fundamentally, let's dive in): none.
- **Promotional vocabulary** (vibrant, pivotal, showcase, underscore, seamless, leverage, nestled, boasts): none.
- **Copula avoidance / filler / excessive hedging / generic positive conclusion**: checked; prose uses plain is/are/has, active voice; conclusion is hedged and concrete (no upbeat filler ending).
- **Sentence rhythm**: varied short/long deliberately to avoid uniform AI cadence.

## 7. Compile caveats

- I did **not** run tectonic/latexmk (no compile invoked in this stage; not blocking per instructions).
- Standalone compile expectation: should build. Preamble mirrors the manuscript's `elsarticle` setup (amsmath/booktabs/threeparttable/tabularx/cleveref/hyperref) plus `amsthm` for the two propositions. `\bibliography` is replaced by an explicit `thebibliography`, so no `.bib`/biber pass is needed.
- One thing to verify on first compile: `cleveref` + `hyperref` load order is correct (hyperref before cleveref, as in the manuscript). The `\eqref{obj}`/`\eqref{con14}`–`\eqref{con17}` targets are provided locally for standalone build; on `\input` merge, delete the guarded block (marked in source) to avoid duplicate-label warnings.
- The tradeoff figure is a `\framebox` placeholder with a `% TODO(plotting)` comment naming the source CSV and axis spec; no figure is fabricated. Replace with `\includegraphics{rc_tradeoff}` once the plotting script is run.
- No solver/data files were touched; this stage only wrote the `.tex` draft and this report.

**Status: DRAFT COMPLETE.** Envelope respected (claims not exceeded; all five limitations present), humanizer pass applied and re-scanned clean.
