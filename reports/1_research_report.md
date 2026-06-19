# State-of-the-Art Report — CSLAP Robustness via Covering Constructions

**Pipeline Stage 1 (Academic Researcher). Prepared for the Method Selector (Stage 2).**
**Date: 2026-06-11. AI-assisted research disclosure: this report was compiled with an AI research agent; every load-bearing reference was independently verified in-session via web search/fetch (authors, venue, year, DOI). Verification status is marked per reference.**

## Executive Summary

The brief's Hypothesis **H1** proposes building enlarged product-sets from observed orders via a covering/hitting-set construction (the existing P–K Set Cover: partition the SKU universe `I` into patterns of size ≤ k, minimizing `P` = the max number of selected patterns intersecting any observed order), then optimizing CSLAP placement over those enlarged sets, with the claim that the resulting layout is more robust to order-distribution shift than one optimized directly on the observed orders.

The literature supports the following findings, stated with the honesty the brief demands:

1. **The components of H1 are individually well-established; the specific combination is not.** Set covering/partitioning, min-max objectives, and column-generation over patterns are textbook OR (Balas & Padberg 1976; Karp 1972). Correlated/affinity slotting and zone-visit minimization are mature SLAP sub-fields (Mantel et al. 2007; Xiao & Zheng 2012; Zhang et al. 2019). Optimization under uncertainty (RO, DRO, two-stage SP, SAA, scenario aggregation) is a fully formalized toolbox (Ben-Tal & Nemirovski 1999; Bertsimas & Sim 2004; Delage & Ye 2010; Mohajerin Esfahani & Kuhn 2018; Rockafellar & Wets 1991; Kleywegt et al. 2002).

2. **I could NOT locate any published work that does what H1 proposes**: replacing the observed demand sets with an optimized cover/partition of them and optimizing placement over that cover, as a deliberate robustification device. This is the report's central honest finding. The closest published relatives are (a) *scenario/policy aggregation* (Rockafellar & Wets 1991), (b) *data-driven uncertainty-set construction* (Bertsimas, Gupta & Kallus 2018), and (c) *correlated storage assignment* with co-occurrence aggregation (Xiao & Zheng 2012). H1 resembles each in spirit but matches none in mechanism.

3. **Verdict (Section 4): H1 is a novel hybrid heuristic, NOT an instance of an established named method.** It is best described as a *combinatorial demand-aggregation / instance-transformation* heuristic. It is **not** a robust counterpart, **not** SAA, **not** DRO, and **not** scenario aggregation in their formal senses. The robustness claim is currently a conjecture without a formal uncertainty object behind it — exactly what the brief's §2 blocking tasks must fix before coding.

4. **A critical warning for the Method Selector:** the min-max-`P` covering objective optimizes *minimality* (fewest patterns, tightest cover), whereas robustness intuition favors *redundancy/coverage*. This is a genuine objective mismatch (brief §2.3) and the literature gives no free pass on it.

---

## Section 1 — Covering formulations in OR

**Set covering, set partitioning, hitting set, and their duality.** The three canonical 0–1 models are *set covering* (`Σ_{p∋i} x_p ≥ 1`), *set partitioning* (`= 1`), and *set packing* (`≤ 1`). The set-partitioning/equality-constrained set-covering problem and its polyhedral structure and algorithms are surveyed comprehensively by **Balas & Padberg (1976)** [VERIFIED: SIAM Review 18(4):710–760, DOI 10.1137/1018115]. Set covering is one of Karp's original 21 NP-complete problems **(Karp 1972)** [VERIFIED: in *Complexity of Computer Computations*, Plenum Press, pp. 85–103, DOI 10.1007/978-1-4684-2001-2_9]. The *hitting set* problem is the standard dual/transpose of set cover (a hitting set picks elements meeting every set; a cover picks sets meeting every element); they are equivalent under interchange of the roles of elements and sets, and both are equivalent to the minimum transversal of a hypergraph. The brief's P–K master is an **exact-cover (partition) variant** in its `Σ_{p∋i} x_p = 1` constraint, placing it squarely in the Balas–Padberg set-partitioning family.

**Column generation over patterns.** Selecting subsets ("patterns", "columns") from an exponential family by a master LP plus a pricing subproblem is the standard branch-and-price machinery for set-covering/packing/partitioning masters. This is precisely the architecture of the project's existing CG solvers and of the P–K Set Cover pricing step ("pricing maximizes α·z + β·w subject to |p| ≤ k"). The numerical-stability advantage of covering (`≥`) masters over partitioning (`=`) masters in the LP relaxation is a known practical point in this literature (multiple CG references in the search corpus).

**Min-max cover-size objectives.** The P–K objective — minimize the maximum number of selected patterns intersecting any observed order — is a **min-max load/overlap objective layered on a partition**. This is structurally a *bottleneck* objective over a partition, related to balanced/bottleneck partitioning and to **hypergraph partitioning with a max-degree/max-load objective**. I did **not** find this exact object ("min over partitions of the max number of parts hit by any hyperedge") established under a single standard name in the warehousing or OR-covering literature; it is most naturally read as a min-max hitting/overlap criterion on a hypergraph whose hyperedges are the observed orders. [Honest gap: marked as not-located rather than non-existent.]

**"Optimize over a cover/partition of the demand sets instead of the demand sets themselves."** The closest *established* idea is **instance/data aggregation** — replacing many constraints/scenarios by aggregated surrogates. In the warehouse domain specifically, **Xiao & Zheng (2012)** [VERIFIED: Int. J. Adv. Manuf. Technol. 61:797–807, DOI 10.1007/s00170-011-3740-5] aggregate demand into *itemsets/clusters* (from BOM/co-occurrence) and then **minimize total zone visits** under picking capacity — conceptually the nearest published cousin to "form enlarged sets, then optimize visits over them." However, their itemsets are correlation clusters, not the output of a min-max cover optimization, and the aggregation is a modeling convenience, not a robustification operator. **Conclusion for §1:** the building blocks (partition, min-max, CG pricing) are standard; the *use of a covering/partition as a substitute demand object for placement* has a near-cousin in correlated-clustering SLAP but the specific min-max-`P` cover-as-surrogate has not been located as a named, prior construction.

---

## Section 2 — Optimization under uncertainty

For each framework: the formal uncertainty object and known guarantees.

**Robust optimization (RO).** *Uncertainty object:* a deterministic set `U` containing all admissible parameter realizations; one optimizes against the worst case in `U`. **Ben-Tal & Nemirovski (1999)** [VERIFIED: Operations Research Letters 25(1):1–13, DOI 10.1016/S0167-6377(99)00016-4] established the robust-counterpart methodology and showed the robust counterpart of an LP under an ellipsoidal `U` is a tractable conic-quadratic program. *Guarantee:* feasibility for **every** realization in `U` (a hard, worst-case guarantee), at the cost of conservatism. The field is surveyed by **Bertsimas, Brown & Caramanis (2011)** [VERIFIED: SIAM Review 53(3):464–501, DOI 10.1137/080734510].

**Budgeted / cardinality-constrained RO.** *Uncertainty object:* a polyhedral set parameterized by a budget `Γ` bounding how many coefficients deviate simultaneously. **Bertsimas & Sim (2004)** [VERIFIED: Operations Research 52(1):35–53, DOI 10.1287/opre.1030.0065]. *Guarantee:* the robust counterpart stays an LP (preserves problem class, extends tractably to discrete optimization), with **probabilistic bounds on constraint violation** as an explicit function of `Γ` — letting the modeler tune conservatism. This is the most likely RO home if H1 were to be cast as RO: the analog would be bounding how many SKUs of an order migrate across patterns.

**Distributionally robust optimization (DRO).** *Uncertainty object:* an *ambiguity set* `D` of probability distributions; one optimizes worst-case **expected** cost over `D`.
- *Moment ambiguity:* **Delage & Ye (2010)** [VERIFIED: Operations Research 58(3):595–612, DOI 10.1287/opre.1090.0741] — `D` constrained by (estimated) mean and covariance; tractable reformulations and finite-sample confidence-region guarantees from data.
- *Wasserstein ambiguity:* **Mohajerin Esfahani & Kuhn (2018)** [VERIFIED: Mathematical Programming 171(1–2):115–166, DOI 10.1007/s10107-017-1141-8] — `D` is a Wasserstein ball around the empirical distribution; tractable convex reformulations and finite-sample **performance guarantees** (out-of-sample cost bounded by the in-sample worst case with high probability). DRO is the framework whose *goal* most closely matches H1's stated aim ("robust to distribution shift"), but its mechanism (a ball of distributions, not a cover of sets) is different.

**Data-driven uncertainty-set construction.** **Bertsimas, Gupta & Kallus (2018)** [VERIFIED: Mathematical Programming 167(2):235–292, DOI 10.1007/s10107-017-1125-8] design RO uncertainty sets *directly from data* via hypothesis tests, yielding finite-sample probabilistic guarantees. *This is the most relevant conceptual template for reinterpreting H1:* if the enlarged sets are to be an uncertainty object, the rigorous question is which data-driven set they implicitly define and whether any guarantee attaches.

**Two-stage / multi-stage stochastic programming (SP).** *Uncertainty object:* a known (or sampled) distribution over scenarios; first-stage "here-and-now" decisions precede scenario realization, second-stage "recourse" adapts. Canonical text: **Birge & Louveaux (2011, 2nd ed.)** [VERIFIED: Introduction to Stochastic Programming, Springer, DOI 10.1007/978-1-4614-0237-4, ISBN 9781461402367]. *Guarantee:* optimizes **expected** cost over the modeled distribution (risk-neutral by default). For CSLAP, placement is naturally a first-stage decision and future order realizations the scenarios.

**Sample Average Approximation (SAA).** *Uncertainty object:* a Monte-Carlo sample approximating the true expectation. **Kleywegt, Shapiro & Homem-de-Mello (2002)** [VERIFIED: SIAM Journal on Optimization 12(2):479–502, DOI 10.1137/S1052623499363220]. *Guarantee:* consistency and exponential convergence of the SAA optimal solution/value to the true ones as sample size grows; stopping rules and complexity bounds. SAA is the natural bridge if H1's "perturbation model" (brief §2.4) generates sampled future-order scenarios.

**Scenario generation / reduction and scenario aggregation.** *Scenario reduction:* **Heitsch & Römisch (2003)** [VERIFIED: Computational Optimization and Applications 24(2–3):187–206, DOI 10.1023/A:1021805924152] — choose a small scenario subset minimizing a probability-metric distance to the full distribution; forward/backward selection algorithms. *Scenario (policy) aggregation:* **Rockafellar & Wets (1991)** [VERIFIED: Mathematics of Operations Research 16(1):119–147, DOI 10.1287/moor.16.1.119] — the progressive-hedging foundation; bundles scenarios and enforces non-anticipativity to produce a single implementable policy from many scenarios. **This is the named method most likely to be confused with H1 (both "aggregate" demand), so Section 4 separates them carefully.**

---

## Section 3 — Prior art at the intersection (uncertainty × SLAP)

**SLAP and its surveys.** The SLAP is NP-hard and is reviewed broadly in **de Koster, Le-Duc & Roodbergen (2007)** [VERIFIED: European Journal of Operational Research 182(2):481–501, DOI 10.1016/j.ejor.2006.07.009] and specifically in **Reyes, Solano-Charris & Montoya-Torres (2019)** [VERIFIED: International Journal of Industrial Engineering Computations 10(2):199–224, DOI 10.5267/j.ijiec.2018.8.001]. The SLAP review notes most work is deterministic and flags demand uncertainty as a comparatively under-addressed dimension.

**Correlated / affinity-based slotting (the deterministic backbone of CSLAP).**
- **Mantel, Schuur & Heragu (2007)** [VERIFIED: European Journal of Industrial Engineering 1(3):301–316, DOI 10.1504/EJIE.2007.014689] — Order-Oriented Slotting (OOS): store SKUs that co-occur in orders close together; the conceptual root of correlation-based slotting.
- **Xiao & Zheng (2012)** [VERIFIED: Int. J. Adv. Manuf. Technol. 61:797–807, DOI 10.1007/s00170-011-3740-5] — correlated storage assignment to **minimize zone visits** under picking capacity; the closest published objective to the project's "minimize station visits."
- **Zhang, Wang & Pan (2019)** [VERIFIED: Computers & Industrial Engineering 129:210–219, DOI 10.1016/j.cie.2019.01.027] — Demand Correlation Pattern (DCP) SLAP model. (This is the "Zhang et al. 2019" whose common-itemset scheme the project's synthetic generator follows.)

**Order batching as set partitioning (the methodological cousin of the master problem).** **Gademann & van de Velde (2005)** [VERIFIED: IIE Transactions 37(1):63–75, DOI 10.1080/07408170590516917] model order batching as a (generalized) set-partitioning problem solved by branch-and-price. This confirms that *partitioning orders/patterns by column generation* is established practice in warehousing — exactly the master used by the project — but applied to batching, not to robustification of placement.

**SLAP under demand uncertainty / dynamics (the H1-adjacent intersection).**
- **Kofler, Beham, Wagner & Affenzeller (2014)** [VERIFIED via Springer + Semantic Scholar metadata: chapter "Affinity Based Slotting in Warehouses with Dynamic Order Patterns", in *Advanced Methods and Applications in Computational Intelligence*, Topics in Intelligent Engineering and Informatics vol. 6, Springer, DOI 10.1007/978-3-319-01436-4_7] — extends SLAP to a **multi-period M-SLAP** and tests how affinity-based slotting performs under **changing order patterns**. This is the single most on-point prior work for H1's robustness-to-shift question: it asks whether correlation-based layouts degrade when demand patterns change. It does *not*, however, use a covering/hitting-set construction; the layout is built from affinity directly. [Note: chapter metadata verified; full text behind paywall — used as a directional pointer, not for any quantitative claim.]
- **A two-stage storage-assignment model** ("Two-stage storage assignment to minimize travel time and congestion for warehouse order picking", *Computers & Operations Research*, 2020, ScienceDirect ID S0360835219305984) appeared in search and is on-topic (two-stage + storage assignment + congestion). [UNVERIFIED: full bibliographic record could not be confirmed in-session — ScienceDirect returned HTTP 403. Listed for the Method Selector to verify; NOT used as a load-bearing claim.]

**Mapping each uncertainty paradigm onto SLAP — where prior art exists vs. where it does not:**

| Paradigm (Section 2) | Published SLAP/warehouse instantiation? | Evidence |
|---|---|---|
| Two-stage stochastic SP | Yes, emerging (travel-time/congestion two-stage SLAP) | S0360835219305984 [UNVERIFIED record]; general SP text Birge & Louveaux 2011 [VERIFIED] |
| SAA | Indirectly (SAA used in warehouse/relocation SP per search corpus) | General method Kleywegt et al. 2002 [VERIFIED]; warehouse use not pinned to a single verified paper |
| Robust optimization (set-based) | **Sparse** for CSLAP specifically; "robust storage assignment in unit-load warehouses" exists in gray/working-paper form | Not verified to a peer-reviewed record in-session — flagged as a gap |
| Budgeted RO (Bertsimas–Sim) | **Not located** applied to correlated SLAP | — (honest gap) |
| DRO (moment / Wasserstein) | **Not located** applied to SLAP/slotting | — (honest gap) |
| Scenario reduction / aggregation | **Not located** applied to SLAP slotting | — (honest gap) |
| Multi-period / dynamic SLAP (demand shift) | Yes | Kofler et al. 2014 [VERIFIED metadata] |
| Correlation/co-occurrence aggregation for visits | Yes | Xiao & Zheng 2012, Zhang et al. 2019, Mantel et al. 2007 [all VERIFIED] |

**Honest gap statement:** I found no peer-reviewed paper, verifiable in this session, that applies budgeted RO, DRO, or scenario reduction/aggregation to the *correlated* SLAP / station-visit-minimization setting. The intersection of formal distribution-shift robustness with correlated slotting is genuinely thin — Kofler et al. (2014) is the principal exception, and it is empirical/dynamic rather than RO/DRO-formal.

---

## Section 4 — Verdict: established named method, or novel hybrid?

**Claim:** H1's construction is a **novel hybrid heuristic** — a *combinatorial demand-aggregation / instance-transformation* operator — and does **not** correspond, in its mechanism, to any single established named method (scenario aggregation, robust counterpart, SAA, DRO, or standard instance aggregation). I argue this by elimination against the closest relatives.

**Closest relative 1 — Scenario / policy aggregation (Rockafellar & Wets 1991) [VERIFIED].** Both "aggregate demand." But scenario aggregation operates on a *probability-weighted set of scenarios* and produces an implementable policy via non-anticipativity; its object is a distribution over futures. H1's covering operates on the *support sets themselves* (SKU subsets), produces *enlarged deterministic sets*, and carries no probability weights or non-anticipativity structure. **Different object (sets vs. weighted scenarios), different mechanism (cover optimization vs. proximal aggregation).** Not an instance of it.

**Closest relative 2 — Robust counterpart / data-driven uncertainty set (Ben-Tal & Nemirovski 1999; Bertsimas & Sim 2004; Bertsimas, Gupta & Kallus 2018) [all VERIFIED].** A robust counterpart requires an explicit uncertainty set `U` and a worst-case optimization over it. H1 as currently stated has **no declared `U`** and does **no** worst-case optimization — it transforms the *instance* (the demand sets) and then runs the *nominal* CSLAP solvers on the transformed instance. It *could* be reinterpreted as implicitly defining a `U` (the set of orders "explained" by the enlarged patterns), and Bertsimas–Gupta–Kallus is the right template for making that rigorous — but that reinterpretation is *work the Method Selector must do*, not a property the construction already has. As written, it is **not** a robust counterpart.

**Closest relative 3 — SAA / two-stage SP (Kleywegt et al. 2002; Birge & Louveaux 2011) [VERIFIED].** These require a sampling/expectation structure over future demand. H1's covering uses *no sampling and optimizes no expectation*; it is a deterministic combinatorial transform of the observed support. **Not SAA, not SP.**

**Closest relative 4 — Instance/constraint aggregation & correlated-clustering SLAP (Xiao & Zheng 2012) [VERIFIED].** This is the *nearest* relative in mechanism: aggregate demand into supersets/itemsets, then optimize visits. The distinction is *purpose and construction*: Xiao–Zheng aggregate by *correlation clustering* as a tractability/modeling device with no robustness claim; H1 aggregates by a *min-max-`P` optimal cover* and asserts the aggregation itself *confers robustness*. The robustness rationale and the min-max-cover construction are the novel elements.

**Therefore:** H1 is best named a **covering-based demand-set enlargement (instance-transformation) heuristic**. Its intellectual neighbors are correlated-clustering SLAP (for the warehouse mechanism) and data-driven uncertainty-set design (for the would-be robustness semantics). The honest status of the robustness claim is **conjectural**: no formal guarantee attaches until the Method Selector fixes the uncertainty object (brief §2.1) and shows the construction is an inner/outer approximation of it (§2.2).

**Load-bearing caution for Stage 2 (objective-mismatch, brief §2.3):** the min-max-`P` cover is a **minimal/tight** construction (fewest, smallest patterns covering each SKU once). Robustness to distribution shift typically calls for **redundant/over-covering** structure (a SKU plausibly belonging to several future co-occurrence groups). There is a real tension between what set-covering minimizes and what robustness wants. The Method Selector must either (a) justify why min-max-`P` minimality serves robustness, or (b) switch to a redundant/weighted/maximal covering variant — and the literature (Bertsimas–Sim's tunable `Γ`; DRO's tunable ambiguity radius) suggests robustness usually comes from a *tunable conservatism knob*, which the current parameter `k`/`P` may or may not provide.

---

## Section 5 — Literature's answers to the five definitional questions (brief §2)

What each framework would say the enlarged sets *approximate*, and in what sense (inner/outer). These are *candidate framings* the literature makes available; the Method Selector must commit to one.

**Q1 — Approximation of WHAT?** Three literature-supported candidate objects:
- *(a) The support of the future order distribution* — under DRO/SP framing, the enlarged sets approximate the set of order-patterns that may appear (Mohajerin Esfahani & Kuhn 2018; Birge & Louveaux 2011).
- *(b) The product co-occurrence/correlation structure* — under correlated-SLAP framing, the patterns approximate the latent affinity graph/itemset structure (Mantel et al. 2007; Xiao & Zheng 2012; Zhang et al. 2019).
- *(c) A data-driven uncertainty set of plausible orders* — under data-driven RO framing, the union/closure of enlarged patterns approximates `U`, the set of orders the layout must serve (Bertsimas, Gupta & Kallus 2018).
The literature does **not** decide this for you; it offers (a)/(b)/(c) as mutually exclusive commitments. *Recommendation: (c) is the framing under which "robustness" has a formal meaning and a guarantee template exists.*

**Q2 — Inner vs. outer.** Only definable after Q1. Literature-grounded readings:
- If the object is *uncertainty set `U`* (framing c): enlarging observed orders into bigger patterns yields a **superset** of the observed support → an **outer approximation** of plausible future demand (you optimize against more order-patterns than you saw). Outer approximation of `U` is the conservative, robustness-conferring direction in RO (Ben-Tal & Nemirovski 1999; Bertsimas, Gupta & Kallus 2018). This is the cleanest fit and the most defensible robustness story.
- If the object is the *true future distribution* (framing a): the enlarged deterministic sets are neither inner nor outer in a distributional sense — they are a *support relaxation*, not a distribution bound. The "inner/outer" vocabulary applies awkwardly here; the honest move (per brief §2.2) is to say so rather than force it.
- If the object is the *correlation structure* (framing b): "inner/outer" does not naturally apply (it is structure estimation, not region containment). Again, say so.
*Recommendation: adopt framing (c) and argue the construction is an **outer approximation of the demand uncertainty set**; this is the only reading under which inner/outer is both well-defined and aligned with the robustness claim.*

**Q3 — Minimality vs. redundancy.** Literature verdict: robustness comes from **redundancy/coverage with a tunable conservatism level** (Bertsimas & Sim 2004's budget `Γ`; DRO's ambiguity radius). The P–K min-max-`P` cover is **minimal**, which is in *tension* with this. The Method Selector must explicitly resolve this (per §2.3): either reinterpret `k`/`P` as the conservatism knob (larger `k` → larger patterns → larger outer approximation → more robust, more nominal loss) or move to a redundant/weighted covering variant. **Do not paper over this.**

**Q4 — Uncertainty / perturbation model.** Literature offers two implementable, citable options matching the brief's §2.4:
- *Temporal split (train-early/test-late):* already used in the project's own manuscript (§5 temporal hold-out, §sec:temporal_validation) and consistent with out-of-sample robustness practice in storage assignment. This **is** the de facto empirical uncertainty set and should be named as such.
- *Explicit perturbation model:* generate plausible future order distributions from the observed one (bootstrap/resampling → SAA-style scenarios per Kleywegt et al. 2002; or a Wasserstein ball around the empirical order distribution per Mohajerin Esfahani & Kuhn 2018). Scenario reduction (Heitsch & Römisch 2003) keeps the scenario count tractable.

**Q5 — Connection to a formal framework.** Per Section 4: H1 instantiates **none** of SP/RO/DRO/SAA as written. The most rigorous *anchoring* available is to recast it, under framing Q1(c)+Q2-outer, as a **data-driven, set-based outer approximation of a demand uncertainty set** in the spirit of Bertsimas, Gupta & Kallus (2018) — and then to test the robustness claim empirically against the §2.4 perturbation model. Absent that recast, the claim "handles uncertainty" is **not anchored to any formal definition** and should not be made.

---

## Limitations of this report

- **Paywalled/blocked records:** ResearchGate and ScienceDirect blocked direct fetch (HTTP 403); affected items were verified via publisher/aggregator metadata (Springer, IDEAS/RePEc, Semantic Scholar, Inderscience) or are explicitly marked [UNVERIFIED] and kept out of load-bearing claims. The two-stage storage-assignment paper (S0360835219305984) is the one on-topic item I could not fully verify in-session.
- **Negative findings are "not located," not "non-existent":** the gaps in Section 3's table (no verified DRO/budgeted-RO/scenario-aggregation applied to correlated SLAP) reflect what I could confirm in this session, not a proof of absence. The Method Selector should treat them as a likely (but not certain) novelty opening.
- **No claim is made that H1 is *true*.** Per the brief, robustness is a hypothesis to be tested; this report only locates H1 in the literature and flags the objective-mismatch and missing-formalism risks.

## Verified reference list (18 load-bearing references)

1. Balas, E. & Padberg, M.W. (1976). Set Partitioning: A Survey. *SIAM Review* 18(4), 710–760. DOI 10.1137/1018115. [VERIFIED: SIAM]
2. Karp, R.M. (1972). Reducibility Among Combinatorial Problems. In *Complexity of Computer Computations*, Plenum Press, 85–103. DOI 10.1007/978-1-4684-2001-2_9. [VERIFIED: Springer/Wikipedia corpus]
3. Ben-Tal, A. & Nemirovski, A. (1999). Robust solutions of uncertain linear programs. *Operations Research Letters* 25(1), 1–13. DOI 10.1016/S0167-6377(99)00016-4. [VERIFIED: ScienceDirect listing]
4. Bertsimas, D. & Sim, M. (2004). The Price of Robustness. *Operations Research* 52(1), 35–53. DOI 10.1287/opre.1030.0065. [VERIFIED: INFORMS]
5. Bertsimas, D., Brown, D.B. & Caramanis, C. (2011). Theory and Applications of Robust Optimization. *SIAM Review* 53(3), 464–501. DOI 10.1137/080734510. [VERIFIED: SIAM/MIT]
6. Delage, E. & Ye, Y. (2010). Distributionally Robust Optimization Under Moment Uncertainty with Application to Data-Driven Problems. *Operations Research* 58(3), 595–612. DOI 10.1287/opre.1090.0741. [VERIFIED: INFORMS]
7. Mohajerin Esfahani, P. & Kuhn, D. (2018). Data-driven distributionally robust optimization using the Wasserstein metric. *Mathematical Programming* 171(1–2), 115–166. DOI 10.1007/s10107-017-1141-8. [VERIFIED: Math. Program.]
8. Bertsimas, D., Gupta, V. & Kallus, N. (2018). Data-Driven Robust Optimization. *Mathematical Programming* 167(2), 235–292. DOI 10.1007/s10107-017-1125-8. [VERIFIED: Math. Program. (arXiv:1401.0212)]
9. Birge, J.R. & Louveaux, F. (2011). *Introduction to Stochastic Programming*, 2nd ed. Springer. DOI 10.1007/978-1-4614-0237-4. ISBN 9781461402367. [VERIFIED: Springer]
10. Kleywegt, A.J., Shapiro, A. & Homem-de-Mello, T. (2002). The Sample Average Approximation Method for Stochastic Discrete Optimization. *SIAM Journal on Optimization* 12(2), 479–502. DOI 10.1137/S1052623499363220. [VERIFIED: SIAM]
11. Heitsch, H. & Römisch, W. (2003). Scenario Reduction Algorithms in Stochastic Programming. *Computational Optimization and Applications* 24(2–3), 187–206. DOI 10.1023/A:1021805924152. [VERIFIED: Springer]
12. Rockafellar, R.T. & Wets, R.J.-B. (1991). Scenarios and Policy Aggregation in Optimization Under Uncertainty. *Mathematics of Operations Research* 16(1), 119–147. DOI 10.1287/moor.16.1.119. [VERIFIED: INFORMS]
13. de Koster, R., Le-Duc, T. & Roodbergen, K.J. (2007). Design and control of warehouse order picking: A literature review. *European Journal of Operational Research* 182(2), 481–501. DOI 10.1016/j.ejor.2006.07.009. [VERIFIED: EJOR/IDEAS]
14. Reyes, J.J.R., Solano-Charris, E.L. & Montoya-Torres, J.R. (2019). The storage location assignment problem: A literature review. *International Journal of Industrial Engineering Computations* 10(2), 199–224. DOI 10.5267/j.ijiec.2018.8.001. [VERIFIED: Growing Science]
15. Mantel, R.J., Schuur, P.C. & Heragu, S.S. (2007). Order oriented slotting: a new assignment strategy for warehouses. *European Journal of Industrial Engineering* 1(3), 301–316. DOI 10.1504/EJIE.2007.014689. [VERIFIED: Inderscience/IDEAS]
16. Xiao, J. & Zheng, L. (2012). Correlated storage assignment to minimize zone visits for BOM picking. *International Journal of Advanced Manufacturing Technology* 61(5–8), 797–807. DOI 10.1007/s00170-011-3740-5. [VERIFIED: Springer]
17. Zhang, R.-Q., Wang, M. & Pan, X. (2019). New model of the storage location assignment problem considering demand correlation pattern. *Computers & Industrial Engineering* 129, 210–219. DOI 10.1016/j.cie.2019.01.027. [VERIFIED: CIE/ScienceDirect listing]
18. Gademann, N. & van de Velde, S. (2005). Order batching to minimize total travel time in a parallel-aisle warehouse. *IIE Transactions* 37(1), 63–75. DOI 10.1080/07408170590516917. [VERIFIED: IIE Transactions/TU Eindhoven]

**Directional pointer (verified metadata, paywalled full text):** Kofler, M., Beham, A., Wagner, S. & Affenzeller, M. (2014). Affinity Based Slotting in Warehouses with Dynamic Order Patterns. In *Advanced Methods and Applications in Computational Intelligence*, Topics in Intelligent Engineering and Informatics vol. 6, Springer, 123–143. DOI 10.1007/978-3-319-01436-4_7. [VERIFIED: metadata only — most on-point prior work for the demand-shift robustness question.]

**Flagged for Stage-2 verification (NOT load-bearing):** "Two-stage storage assignment to minimize travel time and congestion for warehouse order picking operations," *Computers & Operations Research* (2020), ScienceDirect S0360835219305984. [UNVERIFIED: full record blocked in-session.]
