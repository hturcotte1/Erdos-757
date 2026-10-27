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

Conjecture T (finiteness of tight graphs) [REFUTED for Delta <= 4 on 2026-10-27: cell(21,18,9,4) has 12 classes, degree-4 gluings of tight pieces; the Delta <= 3 version, Conjecture T', is open and is all the induction needs]. Every connected member of C with slack 0 AND maximum degree <= 3 has at most 17 vertices.
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

## Addendum 2026-10-27 02:55 UTC: the Henning-Yeo deficiency template and a Hall lemma [derived-here]

Source read: Henning-Yeo, arXiv:1802.01825, Section 7 (saved by the scout in kb/literature/sources/henning_yeo/;
text extract in the scratchpad). Their key theorem has the form A tau <= B n + C m + def(H), where def(H) is the
maximum over families X of vertex-disjoint 'special' subhypergraphs of sum of weights minus C per edge of E*(X)
(edges meeting X from outside); the proof is a minimal counterexample on n + m with Claim B (if a minimum X-transversal
covers E*(X), induct on H - V(X)), then Hall's theorem on the bipartite graph (X versus E*(X)) and a choice of X
minimising |E*(X)| - |X| gives |E*(X)| >= |X| + 2; the rest is a long local case analysis. The weights make the
induction exact for the special pieces. For I11 on class C the analogue is cleaner because (conjecturally) nothing
violates the plain inequality, so no weights are needed; what remains is the Hall argument, which we can state for
arbitrary low-slack blocks:

Lemma U'' (non-universality from slack) [derived-here]. Let F in C satisfy I11 on all its proper induced subgraphs
(e.g. F a proper induced subgraph of a minimal counterexample). If x is a vertex with d_F(x) >= 1 and
slack(F) < 3 + 2 d_F(x) (in particular whenever slack(F) <= 4), then tau(F - x) = tau(F) - 1, i.e. x lies in a minimum
transversal of F. Proof: otherwise slack(F - x) = slack(F) - 3 - 2 d_F(x) < 0. Two vertices x, y lie in a common
minimum transversal whenever slack(F) < 5 + 2(d_F(x) + d_F(y) - [x,y share an edge]) fails to allow tau(F - x - y) = tau(F) - 1:
precisely, if tau(F - x - y) >= tau(F) - 1 then slack(F - x - y) = slack(F) + 5 - 2(d_x + d_y - s_xy) must be >= 0.

Lemma H (Hall reduction) [derived-here]. Let H be a minimal counterexample to I11 and X = {F_1, ..., F_r} a nonempty
family of vertex-disjoint PROPER induced subgraphs of H, each with slack(F_i) <= 4 and no isolated vertex. Let E*(X)
be the edges of H meeting V(X) that lie in no F_i. If the bipartite graph between E*(X) and X (e adjacent to F_i when
e meets V(F_i)) has a matching saturating E*(X), then I11 holds for H. Proof: for each matched pair (e, F_i) pick
x_e in e meeting V(F_i); by Lemma U'' there is a minimum transversal T_i of F_i containing x_e (for unmatched F_i any
minimum transversal); T = union of the T_i covers every edge meeting V(X); tau(H) <= |T| + tau(H - V(X)) and I11 for
H - V(X) and for the F_i give 11 tau(H) <= 3n + 2m - sum slack(F_i) - 2|E*(X)| <= 3n + 2m.
Consequences for a minimal counterexample H (connected, Delta <= 3, slack s <= -1):
(H1) every edge has degree sum >= 5 (X = {e}: |E*| = degsum - 3 must be >= 2); with Lemma R(b) the only pattern
with a degree-1 vertex is (1,2,2).
(H2) For a vertex v of degree 3: tau(H - v) = tau(H) - 1 and slack(H - v) = s + 2 in {0, 1} (so s in {-1, -2}); H - v has
no isolated vertex (an isolated vertex has slack 3 > 1), hence all six neighbours of v have degree >= 2; the components
F_1..F_r of H - v have slacks >= 0 summing to s + 2, so all are tight except at most one of slack 1; and Hall must FAIL
for X = {F_i} with E*(X) = the three edges at v. Hence r <= 3 and exactly one of: (a) r = 1 (H - v connected, slack <= 1,
and no minimum transversal of H - v meets all three pairs {a,b}, {c,d}, {e,f} of v's co-vertices); (b) r = 2 and every
edge at v has one co-vertex in each component; (c) r = 2, two edges at v have all four co-vertices in F_1 and the third
edge meets F_2; (d) r = 3, two edges inside F_1 and the third edge bridging F_2 and F_3. In (c), (d) no minimum
transversal of F_1 meets both pairs; in (b) no minimum transversal of F_1 contains two of x_1, x_2, x_3 and likewise F_2.
(H3) For a vertex v of degree 2: slack(H - v) = s + 4 in {2, 3}; Hall with the two edges at v must fail: H - v has exactly
one non-trivial component meeting both edges (or an edge at v meets no block, which needs two degree-1 co-vertices,
excluded by (H1)).
(H4) If Delta(H) <= 2 then Lemma M (to be proved) applies; otherwise H has a degree-3 vertex and (H2) holds.
Open: turning (H2) into a contradiction needs knowledge of the low-slack graphs F (tight and slack-1): the 'pair/triple
transversal' properties. This is where the Henning-Yeo case analysis would start.
