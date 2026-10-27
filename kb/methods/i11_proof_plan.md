# Proof plan for I11 (11 tau <= 3n + 2m on the class C): minimal-counterexample theory

Written 2026-10-27 02:45 UTC by the orchestrator. Tags: [derived-here] unless marked; every lemma below is
elementary and should be falsified on data and refereed before use (certificate L017 planned).

Setting. C = linear F7-free 3-uniform hypergraphs with e(S) <= |S| - 2 for all S with |S| >= 2 (hereditary under
induced subgraphs). slack(H) = 3n + 2m - 11 tau(H); slack is additive over components; an isolated vertex has slack 3,
a single edge (3,1,1) slack 0. I11 <=> slack >= 0. Known [verified-here]: I11 on C for n <= 27 (L007-L016).

Lemma R (reduction) [derived-here]. Let H in C, Z a nonempty proper vertex subset, e(Z) the number of edges meeting Z,
and T a vertex set such that every edge meeting Z contains a vertex of T. Then tau(H) <= tau(H - Z) + |T|, so if I11
holds for H - Z then slack(H) >= slack(H - Z) + 3|Z| + 2e(Z) - 11|T|. Consequently a MINIMAL counterexample H
(fewest vertices) satisfies, for every proper nonempty Z and every such T: 11|T| > 3|Z| + 2e(Z) + slack(H - Z) >= 3|Z| + 2e(Z).
Call this (Red)-free.
Special cases: (a) Z = T = {v}: 11 > 3 + 2d(v), so Delta(H) <= 3. (b) Z = {y, a}, T = {a}, d(y) = 1, y in an edge with a:
11 > 6 + 2d(a) forces d(a) <= 2: a degree-1 vertex never shares an edge with a degree-3 vertex. (c) Z = {y, a, b} the edge
of a degree-1 vertex y with T = {b}: 11 > 9 + 2d(b) is impossible, so... careful: T = {b} covers all edges meeting Z only if
the edges at a and y all contain b, i.e. d(a) = d(y) = 1: an edge has at most one degree-1 vertex. Combined: the edge
of a degree-1 vertex has degree pattern (1, 2, 2).
(d) Z = any proper induced block whose minimum transversal also covers all edges leaving Z: then |T| = tau(Z) and
11 tau(Z) = 3|Z| + 2 m_Z - slack(Z) <= 3|Z| + 2 e(Z), so (Red) holds. Hence in a minimal counterexample NO minimum
transversal of any proper induced subgraph H[Z] covers all edges leaving Z; more precisely 11 k' > slack(Z) + 2k where
k = edges leaving Z and k' = those not covered by the chosen minimum transversal of H[Z].

Lemma D (deletion of one vertex) [derived-here]. For a minimal counterexample H with slack s <= -1 and a vertex v of
degree d: tau(H - v) = tau(H) - 1 (if tau did not drop, slack(H - v) = s - 3 - 2d < 0, contradicting minimality), and
slack(H - v) = s + 8 - 2d. So: d = 3 gives slack(H - v) = s + 2 <= 1; d = 2 gives s + 4 <= 3; d = 1 gives s + 6 <= 5.
The components of H - v have slack >= 0 (minimality) summing to slack(H - v); each contains a neighbour of v
(H connected), so there are at most 2d of them.
Consequence: H minus any degree-3 vertex is a disjoint union of tight (slack 0) connected members of C with at most one
component of slack 1. H has a degree-3 vertex unless Delta <= 2 (Lemma M below).

Lemma U' (no universal vertex in tight graphs) [derived-here from I11 at n <= 27, needs the general I11 beyond].
If K1, K2 in C are connected with slack 0 and K is obtained by identifying a vertex x1 of K1 with x2 of K2, then K is in C
(linearity, F7-freeness and e(S) <= |S| - 2 are preserved: an F7 split by a cut vertex is impossible since F7 minus any
vertex has at most 2 components that are not both edge-sets of an F7 piece... check in the certificate), n = n1 + n2 - 1,
m = m1 + m2, and tau(K) in {tau1 + tau2 - 1, tau1 + tau2}; slack(K) = 8 if tau(K) = tau1 + tau2 - 1 and -3 otherwise.
So I11 for K (n <= 27, verified) forces tau(K) = tau1 + tau2 - 1: x1 lies in a minimum transversal of K1 and x2 in one of
K2, i.e. NO vertex of a tight connected graph with <= 14 vertices is universal (alpha(K - x) = alpha(K) for all x).
Falsify on the known tight graphs ((10,7,4): 5 classes, (14,12,6): 11 classes, (17,13,7): 6 classes).

Lemma M (maximum degree 2) [conjecture, to prove]. If H in C has Delta <= 2 then I11 holds. Sketch: the dual graph G
(vertices = edges of H, one G-edge per degree-2 vertex of H) is simple (linearity) with maximum degree 3; tau(H) =
m - nu(G) + (corrections for edges whose vertices all have degree 1), so slack = 11 nu(G) - 3 |E(G)| + corrections;
needs nu(G) >= 3|E(G)|/11 for subcubic G arising this way (true for cubic graphs: nu >= (4|V|-1)/9 gives nu >= 0.44|V|
against 3|E|/11 = 0.41|V|); the class-C structure must be used for the general subcubic case or a counterexample found.

Conjecture T (finiteness of tight graphs) [conjecture]. Every connected member of C with slack 0 has at most 17 vertices.
Known tight connected cells [verified-here]: (3,1,1): 1 class; (10,7,4): 5 classes (4 with Delta <= 3); (14,12,6): 11 classes
(2 with Delta <= 3); (17,13,7): 6 classes (Delta <= 3); empty: (20,14,8), (21,18,9), (24,19,10) (Delta <= 3). Open: (27,20,11),
(28,...), and all Delta = 4 cells beyond 14. Relevance: the record cells (25,23,11) and (32,29,14) have slack 0, so
Conjecture T (with Delta <= 4) would give f(25) = 15 and exclude records at 25 and 32 points.
A tight graph K with a degree-4 vertex v has K - v tight (slack 0 + 11 - 3 - 8 = 0): tight graphs with Delta = 4 are
degree-4 extensions of unions of smaller tight graphs (A_base = AP + (10,7,4) + its point 0). With Delta = 3,
K - v has slack 2.

Why the obvious closure fails. One would like P(n): 'I11 holds for n vertices and all connected graphs of slack <= 1 are
in a finite list L'. The step for a minimal counterexample works (H minus a degree-3 vertex is a union of L-members, so
finitely many candidates). The step for slack-1 graphs fails: deleting a degree-3 vertex from a slack-1 graph gives slack 3,
whose connected members are not in L (cell (25,19,10,3) alone has 35,645 classes). So the induction needs either
(i) a classification of slack <= 3 (or <= 5) graphs by structure rather than by list, or (ii) a different reduction for
degree-3 vertices (Henning-Yeo style deletion of larger sets with a cover argument), or (iii) a potential function other
than slack.

Plan. (1) Falsify Lemmas R(a-d), D, U' and Conjecture T on all stored data (censuses, cell lists of L007-L016, the
S_K family). (2) Compute the (Red)-free connected Delta <= 3 graphs for small n to see the local structure a minimal
counterexample must have (experiments/20261027-0230-red-config). (3) Obtain the Henning-Yeo proof text and adapt its
degree-3 reductions. (4) Write certificate L017 (the structure theorem for a minimal counterexample) for refereeing even if
the full proof is not reached.
