# Conjecture I11: 11 tau <= 3n + 2m for the AP hypergraph of every (4,5)-set [conjecture]

Written 2026-10-17 06:12 UTC. Statement, evidence, what is proved, and what a proof would need.

**Statement.** Let A be a (4,5)-set with n points, m three-term APs and h(A) = n - tau (tau = transversal number of the
AP hypergraph H(A)). Then 11 tau <= 3 n + 2 m. Equivalently, with slack s(H) = 3n + 2m - 11 tau: s >= 0.

**Why it matters.** Henning-Yeo [published] gives 17 tau <= 5n + 3m for all linear F7-free 3-graphs, hence
h >= (9n + 6)/17 and c* >= 9/17. I11 is strictly stronger for saturated sets (m = n - 2): tau <= (5n - 4)/11, so
h >= (6n + 4)/11 and c* >= 6/11 = 0.5454... > 9/17 = 0.5294... (goal clause B would follow from a proof of I11 in
general). Within the proved range n <= 26 (see 'What is proved' below) it gives f(16) >= 10, f(18) >= 11, f(20) >= 12, f(22) >= 13, i.e. no record set at n = 16, 18, 20, 22 [verified-here, L007-L011];
the first size where I11 allows a record is n = 23 (h = 13 >= (138+4)/11 = 12.9); that cell is closed by other means: degree >= 5 by the slack arithmetic of L012 Step 1, degree 4 by exact non-realizability (L012/K56), and degree 3 by the class-level computation of L014/K58, so f(23) = 14 [verified-here, L012 and L014 each ACCEPTED x3]. The first size at which a record is not excluded by these results is therefore n = 25 (cell (25,23,11), I11 slack 0).

**Evidence [verified-here, experiments/falsify/i11-inequality].** 0 violations on: every subset of the seven stored
record sets and of all 2,910 saturated extremal 14-point classes and all 54,243 extremal 12-point classes; the
1,333,217-row realizable (n, m, tau) dataset; Fibonacci prefixes to n = 25; gluings; 2,028,719 one-point extensions;
the abstract censuses (12,10) and (14,12). Equality cases: (3,1,1) (one AP), (10,7,4), (12,4,4), (13,8,5), (14,12,6) = A_base,
and disjoint unions of these (gluing A_base with itself: (28,24,12), slack 0). The LP polygon of valid bounds
tau <= a n + b m over the data known on 2026-10-17 has vertices (0,1), (3/11, 2/11) = I11, (3/7, 0). Since 2026-10-20 the vertex (3/7, 0), i.e. the bound tau <= 3n/7, is invalid [refuted]: the 65-point set C003 (K59; a community construction, an anonymous reader's, Erdos Problem a Day, 19 Oct 2026, verified here, not discovered here) has (n, m, tau) = (65, 63, 28) and 7 tau = 196 > 195 = 3n. I11 holds on C003 with slack 3*65 + 2*63 - 11*28 = 13, and on the whole community family S_K (n = 11 + 9K, m = n - 2, tau = 4 + 4K; K60, L015) with slack 7 + K (L015, Sanity checks) [derived-here].

**What is proved.** On the class C of linear F7-free 3-graphs with e(S) <= |S| - 2 on every vertex subset (which contains
every AP hypergraph of a (4,5)-set, K3-K7), I11 holds for all n <= 27: certificates L007 (n <= 14), L008 (n = 15, 16),
L009 (n = 17, 18), L010 (n = 19, 20), L011 (n = 21, 22), L013 (n = 23, 24, 25, 26) and L016 (n = 27), all ACCEPTED by three referees (K51-K55, K57, K61).
Consequences: f(16) = 10, f(18) = 11, f(20) = 12, f(22) = 13; no (4,5)-set with at most 22 points beats 4/7. The method is inductive: I11 at n - 1 bounds
the degrees in a hypothetical violator at n, which makes the remaining enumeration finite and small. The method does not decide the record at n = 23: the record cell (23,21,10) has slack +1, so I11 holds there and there is nothing to
refute. The induction itself continues to n = 26 (L013, K57, ACCEPTED x3; first found by the worker runs experiments/20261017-1645-i11-n23-n24 and
experiments/20261017-1720-i11-n26), and it cannot pass n = 27 without the complete lists cell(22,18,9,3) and cell(23,21,10,3) (both now computed and certified by L014, ACCEPTED x3, K58; worker run
experiments/20261017-1925-q14-decide): the violator cell (27,25,12) forces a degree-3 vertex whose
deletion leaves (26,22) with slack 1, and [(23,21,10), AP] is one of its three decompositions; the first I11-allowed record cells are (23,21,10), (25,23,11), (30,27,13), (30,28,13), (32,29,14), (32,30,14),
(34,32,15). At (23,21,10) the degree-4 case is excluded by realizability (L012, ACCEPTED x3, K56) and the degree-3 case is empty in C (L014, ACCEPTED x3, K58; Q14 closed), so f(23) = 14 and the first size where a record is not excluded is n = 25.

**What a proof must use.** Both hypotheses of C are essential: a connected linear F7-free 3-graph with (9,8,4) has slack -1
(it has m > n - 2, so it violates e(S) <= |S| - 2), and a linear (14,11,6) graph containing F7 has slack -2
(experiments/falsify/i11-inequality/f7free_nonO_violation_9_8_4.json, f7_containing_violation.json). For n <= 13 and
m <= n - 2 the only connected linear 3-graph violating I11 is F7 itself (L007 referee rounds 1 and 3). A general proof
would be a Henning-Yeo-style discharging/induction argument on C; the equality cases above show what the extremal
structures must look like (A_base-type components and disjoint APs).

**Status tags.** The inequality in general: [conjecture]. For n <= 27 on C: [verified-here] (L007-L011, L013, L016).
The implication c* >= 6/11: conditional on the conjecture.

## Status 2026-10-27: minimal-counterexample theory, conjectures T, T', T'', RU, C1, P2

All statements below are tagged; "as a computation" means an exact or exhaustive computation that no referee has re-run. Notation: a cell (n,m,tau,Delta) is the set of connected members of C with n vertices, m edges, transversal number tau and maximum degree Delta; slack = 3n + 2m - 11 tau (so I11 says slack >= 0; "tight" means slack 0). Evidence is in journal/LOG.md entries dated 2026-10-27.

**L017: structure of a minimal counterexample (results/proofs/L017-i11-minimal-counterexample-structure.md).** [verified-here: referee ACCEPT x2, 2026-10-27; Theorem 7 [published, re-proved here]] (K64, K65; round 1 editorial fixes only, round 2 two referees ACCEPT; Corollary 13.3/13.5 computations below remain unrefereed)
- A minimal counterexample H to I11 on C (minimal in n, then m) is connected, has Delta = 3 and n >= 28, and has slack s in {-1,-2}.
- Every vertex of H lies in a minimum transversal, and tau(H - v) = tau(H) - 1 for every vertex v.
- Deleting a vertex v of degree d gives slack(H - v) = s + 8 - 2 d(v) (Lemma D).
- Lemma U'' (every non-isolated vertex of a graph in C with slack <= 4 lies in a minimum transversal, given I11 below n), the pair and k-vertex forms of Lemmas R and R+, and the Hall lemma (Lemma H, reduction for families of disjoint low-slack blocks; modelled on Henning-Yeo arXiv:1802.01825 Section 7; only proper induced subgraphs are used, so there is no circularity).
- For a degree-3 vertex v, H - v has at most 3 components: tight pieces plus at most one slack-1 piece; there are exactly seven Hall-deficient attachment patterns, each with an exact equivalent condition (Theorem 4 of L017). L018 Theorem 6(b') [verified-here, K67] sharpens this to at most 2 components (supersedes L017 Theorem 4(iii)).
- Degree-1 and degree-2 vertices: a degree-1 vertex forces s = -1; see Theorem 5 of L017 and L018.
- Caveat stated in L017: Theorems 1-5 use only linearity and I11 below n, so F7 and the (9,8,4) graphs satisfy them; a full proof must use F7-freeness and the hereditary condition e(S) <= |S| - 2.
- Theorem 7 (I11 for Delta <= 2, Lemma M): [published, re-proved here]. Henning-Yeo EJC 24(2) (2017) P2.50, Prop. 9 + Thm 14 at k = 3, or Chvatal-Hanson 1976 (|E| <= 3 nu + floor(nu/2) for subcubic graphs); L017 proves it via tau = m - nu(dual graph) and Tutte-Berge, equality only for matchings. Scout verdict NOVELTY: KNOWN for this theorem; Theorems 1-6 are the new content.

**The reduction (L017 Corollary 13.3).** [verified-here as a computation, not refereed]
- For a minimal counterexample H and a degree-3 vertex v, some component of H - v has >= 27 vertices or is a tight graph in cell (25,23,11).
- Hence I11 on C follows from Conjecture T'' (below) together with the emptiness of cell(25,23,11,3). **UPDATE 06:20 UTC: T'' is REFUTED [refuted; K69, two referees]: L020 Theorem 1 (results/proofs/L020-joint-induction-i11.md) exhibits 45 connected members of C with (29,23,12), Delta = 3, slack 1 (verified by two independent programs). The reduction 'I11 <= T''' is therefore vacuous; L020 Corollary 5 replaces it by 'I11 <= cell(25,23,11,3) empty [computed] + C1-big + R-big' (coverage conjectures for connected slack <= 1 Delta <= 3 graphs with >= 27 vertices).**

**Conjecture T (every connected tight member of C has <= 17 vertices).** [refuted] in this form. cell(21,18,9,4) has 12 classes, all with Delta = 4 (experiments/20261027-0300-tight-cells-d4; also experiments/falsify/i11-structure-lemmas/REPORT.md). Tight graphs with a degree-4 vertex are degree-4 gluings of unions of tight pieces and form an unbounded family (slack 0 + 3 + 8 - 11 = 0). Also three Delta = 4 tight classes in (25,23,11) (experiments/falsify/i11-structure-lemmas, non-exhaustive; search exhaustive only for the shape A u (3,1,1)). [verified-here as computations]

**Conjecture T' (Delta <= 3 version: a connected tight member of C with Delta <= 3 has n <= 17).** [conjecture]. Holds for n <= 27: the cells (20,14,8,3), (21,18,9,3), (24,19,10,3), (27,20,11,3) are empty and (17,13,7,3) is the L014 list of 6 classes (experiments/20261027-0300-tight-cells-d4; stored refereed lists). [verified-here as computations: stored cells]

**Conjecture T'' (connected, Delta <= 3, slack <= 1 implies n <= 26).** [conjecture]
- Evidence: the stress test experiments/falsify/i11-n28-40 (2.6M random growth graphs, 713k gluings, 3.16M edge extensions, exact beam, hub unions; HOLDS-ON-DATA for I11). Every connected slack <= 1 graph found with n >= 19 has Delta = 4; with Delta <= 3 the only connected slack <= 1 graphs found have n <= 17 (low_graphs.jsonl.gz there). [heuristic]
- Slack-1 cells with Delta <= 3 and n <= 26: (8,5,3), (12,10,5), (15,11,6), (19,16,8), (22,17,9), (26,22,11) with 2, 149, 19, 227, 37, 36 classes (470 in total, from the stored refereed lists; L017 C4). [verified-here as computations]

**Conjecture RU ((Red)-universality).** [conjecture]. Every connected Delta <= 3 member of C with n >= 4 has a proper nonempty Z and a cover T of the edges meeting Z with 11|T| <= 3|Z| + 2e(Z). RU would imply I11 for all n (a minimal counterexample is connected, Delta <= 3 and (Red)-free; the only (Red)-free graph is the single edge, which satisfies I11).
- Verified for n <= 14 by the census experiments/20261027-0230-red-config (2,704,610 connected classes; only the single edge is (Red)-free). [verified-here as a computation]
- L018 (results/proofs/L018-red-universality.md, PARTIAL certificate) proves RU is NON-LOCAL (Theorem 4: for any R there are class-C graphs whose every (Red) pair has |Z| > R), so no bounded-radius discharging proof exists. L018 proved parts [verified-here, K67] (fable ACCEPT x2, opus ACCEPT after four editorial rounds); RU itself and I11 remain [conjecture]. Theorem 6(b') of L018 supersedes L017 Theorem 4(iii): H - v has at most 2 components.
- The n = 15 dense census (experiments/20261027-0400-red-config-n15) is not complete; nothing is claimed beyond n = 14.

**Conjecture C1 (triple coverage).** [conjecture]. In a connected slack <= 1 member F of C with m <= n - 4, every admissible degree-3 attachment (three disjoint vertex pairs whose addition keeps the graph in C) is met by some minimum transversal.
- 102,260,107 admissible triples checked in cells (17,13,7), (15,11,6), (22,17,9), (26,22,11), 0 failures; it fails at slack 2 (56 uncoverable admissible triples in (20,15,8)) (experiments/20261027-0300-transversal-richness). [verified-here as a computation]
- L019 (results/proofs/L019-triple-coverage-C1.md) proved parts [verified-here, K68]; C1 open (GAP 1: s(F) = 1; GAP 2: s(F) = 0 closes under T3). Its folding lemma (Theorem 5) is a new exact slack-raising operation: deleting a degree-2 vertex and identifying two non-adjacent neighbours from its two edges changes (n, m, tau) by (-2, -2, -1), raising the I11 slack by exactly 1 (graph case: Chen-Kanj-Jia 2001 [published]; 3-uniform form with the class-C criterion new) [verified-here, K68].

**Conjecture P2 (tight graphs have at most one degree-1 vertex).** [conjecture]. Verified on all stored tight cells for n <= 27 (L018 Theorem 5; experiments/20261027-0300-tight-cells-d4). [verified-here as a computation] If true, no minimal counterexample has a degree-1 vertex (L018 Theorem 5).

**Exact realizability of the tight (21,18,9) classes.** [verified-here as a computation, unrefereed]. experiments/20261027-0400-realize-21-18-9 (rexact.py, exact incremental RREF over Q, DFS over midpoint labellings): none of the 12 tight (21,18,9) classes is realizable (each contains a non-realizable sub-configuration of 9-12 edges; positive controls (17,13,7), (14,12,6), (10,7,4) are realizable). f(21) = 12: class 43 of cell(21,19,9,4) is realizable (C006, K66).

**I11 at n = 28 by computation.** [verified-here as a computation, unrefereed]. Every violator cell at n = 28 is empty: (28,17,11,2), (28,18,11,3), (28,23,12,3), (28,19,11,3) in experiments/20261027-0340-induction-n28-n29-f25/progress.tsv, and (27,20,11,3) = 0 in experiments/20261027-0300-tight-cells-d4; this relies on the refereed lists up to n = 27 and on the L017 reductions (Corollary 13.3, Lemma D), which are themselves not yet refereed in full. n = 29 is in progress (no claim). Not certified: no L-number exists for n = 28.
