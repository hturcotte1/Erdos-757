# Two-point extensions and universal vertices [derived-here]

Written 2026-10-15 23:40 UTC while the sweep experiments/20261015-2340-ext14-all (2-point extensions of all 2,910
saturated extremal 14-point classes, the L001 case analysis applied to every class) was running. The sweep has since finished [verified-here]: all 4,970,208 (4,5) extension pairs with both new points in new 3-APs (case T1b), all 141,153 (4,5) single extensions (T1a) and all 122,220 one-edge lines (T2) of the 2,910 classes have h = 10, so no 16-point (4,5)-set with h <= 9 contains one of these classes (K46, certificate L005, referee ACCEPT x2 on 2026-10-16 01:37 UTC, scout CLEAR; see results/LEDGER.md). The structural census K47 [verified-here] also finds 0 universal vertices in all 2,910 classes, confirming Corollary U1 on the data. The lemmas below are
short consequences of published facts (K3-K6: in a (4,5)-set, Sidon subsets = 3-AP-free subsets, midpoints are injective
and never extreme; Henning-Yeo 17 tau <= 5n + 3m for linear F7-free 3-graphs). Re-check before relying on them.

Notation. A a (4,5)-set, H = H(A) its 3-AP hypergraph, h(A) = alpha(H) = n - tau(H), D(A) = 17h - 9n.
A vertex a is **universal** if it lies in every maximum Sidon subset of A (equivalently alpha(H - a) = alpha(H) - 1,
equivalently a lies in no minimum transversal).

**Lemma E (one-edge extension at an extreme point).** Let a be an extreme point of A (min or max). For all but
finitely many reals t, C = A ∪ {a - t, a + t} is a (4,5)-set whose AP hypergraph is H plus the single edge
{a - t, a, a + t}, and
  h(C) = h(A) + 1 if a is universal, h(C) = h(A) + 2 otherwise.
In the universal case D(C) = D(A) - 1 and the ratio improves: from (n, h) to (n + 2, h + 1).
*Proof.* Put x = a + t, y = a - t. For generic t the only linear relation among points of C that involves x or y is
x + y = 2a (any other relation, e.g. 2x = b + c, x + b = y + c, x + b = 2c, fixes t). A 4-subset of C containing x
and y has a coincidence of differences only through x - a = a - y (the pair {x, y, b, c} would need x + y = b + c,
i.e. 2a = b + c, impossible since a is extreme), so it has >= 5 distinct differences; 4-subsets with one new point
have 6 distinct differences unless the three old points form an AP, then 5. So C is a (4,5)-set with H(C) = H + e,
e = {y, a, x}. Independent sets of H + e: if both x, y are in I then a is not, so |I| <= alpha(H - a) + 2; otherwise
|I| <= alpha(H) + 1. Both bounds are attained. QED.
Lemma E (a extreme) and its Remark below (a any vertex, x the midpoint of a and y; symmetrically y the midpoint of a and x) are the generic parts of case T2 of certificate L001. The 3 roles x 14 points = 42 lines for A_base split as 2 (a extreme and the midpoint of x and y: this lemma) + 28 (a an endpoint, x or y the midpoint: the Remark) + 12 (a non-extreme, hence a midpoint of some b, c in A, and the midpoint of x and y: every point of such a line gives a parallelogram {x, y, b, c} with x + y = b + c = 2a, so there is no (4,5)-set). The labeled hypergraph H(A_base) + {a, x, y} has alpha = 10 on all 42 lines (for the 12 parallelogram lines this is a statement about the abstract hypergraph only).

**Lemma U (Henning-Yeo obstruction to universal vertices).** If a is universal in H(A) then
  17 tau(H) <= 5(n - 1) + 3(m - deg a).
*Proof.* alpha(H - a) = alpha(H) - 1 gives tau(H - a) = tau(H); H - a is linear and F7-free on n - 1 vertices with
m - deg(a) edges; apply Henning-Yeo. QED.
*Corollary U1.* A saturated extremal 14-point set (n = 14, m = 12, tau = 6) has NO universal vertex: 102 > 101 - 3 deg a.
So Lemma E can never produce a 16-point record from one of the 2,910 classes of L004 (no T2 line of the sweep is deficient,
by theory; the sweep confirms it on the data: all 122,220 line hypergraphs have alpha = 10).
*Corollary U2.* More generally a universal vertex a needs 17 tau <= 5n + 3m - 5 - 3 deg a, i.e. Henning-Yeo slack
delta = 5n + 3m - 17 tau >= 5 + 3 deg a; so delta >= 8 when deg a >= 1, and delta >= 5 for a vertex in no AP (such a
vertex is trivially universal). Record-type sets (small D, hence small slack) have no universal vertices.
*Remark (other roles; falsifier-checked).* Lemma E has a variant in which the new point x is the midpoint of a and
the second new point y = 2x - a, for ANY vertex a (not necessarily extreme) and generic x: C is again a (4,5)-set with
H(C) = H + {a, x, y} (a parallelogram {a, y, b, c} would need x to be the midpoint of b, c, which generic x is not),
and h(C) = h(A) + 1 iff a is universal, h(A) + 2 otherwise.

**Lemma Δ (degrees in a 16-point record set).** Let C be a 16-point (4,5)-set with h(C) = 9 (a record, 9/16 < 4/7),
m = m(C). Then m ∈ {13, 14}, every 15-point subset is extremal (h = 9 = f(15)), no vertex is universal, and
  deg p <= m - 9 for every p ∈ C (so deg p <= 5, and <= 4 when m = 13).
*Proof.* m >= 13 is the feasibility table (START_HERE section 4), m <= n - 2 = 14 by injectivity. For p ∈ C:
9 = f(15) <= h(C - p) <= h(C) = 9, so tau(H) = 16 - 9 = 7 and tau(H - p) = 15 - 9 = 6; apply Henning-Yeo to H - p: 102 <= 75 + 3(m - deg p). QED.
*Consequence for the sweep.* If C = A ∪ {x, y} with A one of the 2,910 saturated extremal classes, then
m(C) = 12 + k with k ∈ {1, 2} new edges, every new edge contains x or y, and deg x, deg y <= 3 + k. With k = 1 the
new edge is either {a, x, y} in some role (Lemma E or its remark: h(C) = 9 only if a is universal in H(A), excluded by
U1) or {x, a, b} with y in no AP: then h(C) = h(A ∪ {x}) + 1, and h(A ∪ {x}) = 8 is impossible by Henning-Yeo applied
directly to A ∪ {x} (n = 15, m = 13, tau would be 7: 119 <= 114 is false); equivalently alpha(H(A) + {x, a, b}) = 8
would need both a and b universal in H(A). So a record extension needs exactly k = 2 new edges, i.e. m(C) = 14 and
Henning-Yeo slack 3. [verified-here] K46/L005 (experiments/20261015-2340-ext14-all/results.json) rules this out for every one of the 2,910 saturated extremal classes: every (4,5) two-point extension of every class has h = 10 (cases T0, T1a, T1b, T2 of L005), so none reaches h <= 9 (4,970,208 enumerated (4,5) T1b pairs, plus the 141,153 single-extension and 122,220 T2-line cases, all with h = 10). Hence, granting that the 2,910 classes are all the saturated extremal 14-point classes (the completeness of the L004 census, K45, was re-checked independently only by sampling 28% of the prefixes plus consistency checks, not by a second full enumeration), a 16-point record contains no saturated extremal 14-point subset, and any 14-point subset of a record with h = 8 has m = 11 (Q11, still open); by K48/L006 such a subset, if it exists, contains no extremal 12-point subset.

**Falsifier report (2026-10-15 23:47 UTC; experiments/falsify/extension-lemmas/).** No lemma broken on ~11,000 sets
(the 7 sets of data/small_records.json; realized extremal AP patterns for n = 6..8 in full and for n = 9, 10 capped at 1,200 random per (n, m) file; 724 sampled sets at n = 11 (m = 6, 7, 8); 1,500 random of the 54,243 twelve-point classes; 150 random of the 2,910 fourteen-point classes; A_base; Fibonacci prefixes n = 8, 10, 12, 14; not covered: n = 13 (no realized 13-point sets exist: the saturated census was started and stopped as infeasible, D22/Q12) and the 466,961 saturated n = 11 classes (not loaded by that run; they are stored only in the git-ignored directory experiments/20261014-1430-small-counts/n11/results/post/ and were used later for K49)): Lemma E 197,946 (set, a, t) triples with 0 formula
failures plus a symbolic-t (4,5) check on 21,994 cases; Lemma U 5,443 universal vertices, 0 violations; no sampled
14-point class has a universal vertex (U1). Universal extreme points do exist at n = 7, 9, 11 (and in Fibonacci
prefixes); on the extremal sets Lemma E then yields (n + 2)-point sets with h + 1 = f(n + 2) exactly, never a record (the Fibonacci prefixes n = 8, 10, 12 give (n + 2, h + 1) = (10, 7), (12, 8), (14, 9), above f(n + 2) = 6, 7, 8, so no record either). The falsifier
corrected an arithmetic slip in U2 (deg a >= 1 needed for delta >= 8) and two gaps in the consequence paragraph
(wrong universality condition in the {x, a, b} case; the role "x midpoint of a, y" was missing); both fixed above.
[verified-here on data; the lemmas themselves remain derived-here]

**Lemma Δ' (deletion version; Henning-Yeo bound on which pairs can leave an extremal subset) [derived-here].** Let A be an
n-point (4,5)-set with h(A) = f(n), m APs, tau = n - f(n), and suppose A - p - q is extremal with f(n-2) = f(n) - 1 (so
tau(H - p - q) = tau - 1). Henning-Yeo applied to H - p - q (n - 2 vertices, m - deg p - deg q + eps edges, eps = 1 if p, q
share an AP) gives 17 (tau - 1) <= 5 (n - 2) + 3 (m - deg p - deg q + eps), i.e.
  deg p + deg q - eps <= m - (17 tau - 5 n - 7) / 3.
At (14, 12, tau = 6): deg p + deg q - eps <= 11/3, so <= 3: since every vertex of a saturated extremal 14-point class has degree
>= 2 (K47), an extremal 12-point subset could only arise by deleting two ADJACENT degree-2 vertices (eps = 1); K47 shows that
no such deletion works in any of the 2,910 classes. At (12, 10, tau = 5): deg p + deg q - eps <= 10 - 18/3 = 4, which allows
any two degree-2 vertices, consistent with the 49.5% of classes that do contain an extremal 10-point subset (K49). At
(16, m, tau = 7) a hypothetical record: an extremal 14-point subset would need deg p + deg q - eps <= m - 32/3, i.e. <= 3 for
m = 14 and <= 2 for m = 13, so the deleted pair has small degrees (for m = 14: two degree-1 vertices, a degree-1 and a degree-2 vertex,
or two adjacent degree-2 vertices, or a degree-1 with an adjacent degree-3 vertex); combined with K46
(no saturated extremal 14-subset at all) this says a 16-point record contains at most (14,11)-type extremal subsets, through
such low-degree pairs. [derived-here; falsifier HOLDS-ON-DATA (experiments/falsify/deletion-lemma/): 0 violations on all 54,243 twelve-point classes (deleted pairs leaving h = 6 have d = deg p + deg q - eps in {2, 3}, bound 4), the 6,644 saturated 10-point and 66 saturated 8-point classes (bound attained at n = 8), and the 2,910 fourteen-point classes (18,330 adjacent degree-2 pairs, all with d = 3 = bound, none leaving h = 7); the four numeric bounds re-derived.]
