# Two-point extensions and universal vertices [derived-here]

Written 2026-10-15 23:40 UTC while the sweep experiments/20261015-2340-ext14-all (2-point extensions of all 2,910
saturated extremal 14-point classes, the L001 case analysis applied to every class) was running. All statements are
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
This is exactly case T2 of certificate L001 (42 lines for A_base, all with alpha = 10).

**Lemma U (Henning-Yeo obstruction to universal vertices).** If a is universal in H(A) then
  17 tau(H) <= 5(n - 1) + 3(m - deg a).
*Proof.* alpha(H - a) = alpha(H) - 1 gives tau(H - a) = tau(H); H - a is linear and F7-free on n - 1 vertices with
m - deg(a) edges; apply Henning-Yeo. QED.
*Corollary U1.* A saturated extremal 14-point set (n = 14, m = 12, tau = 6) has NO universal vertex: 102 > 101 - 3 deg a.
So Lemma E can never produce a 16-point record from one of the 2,910 classes of L004 (case T2 of the sweep is empty
by theory; the sweep checks this on the data as well).
*Corollary U2.* More generally a universal vertex needs 17 tau <= 5n + 3m - 5 - 3 deg a, i.e. Henning-Yeo slack
delta = 5n + 3m - 17 tau >= 5 + 3 deg a >= 8. Record-type sets (small D, hence small slack) have no universal vertices.

**Lemma Δ (degrees in a 16-point record set).** Let C be a 16-point (4,5)-set with h(C) = 9 (a record, 9/16 < 4/7),
m = m(C). Then m ∈ {13, 14}, every 15-point subset is extremal (h = 9 = f(15)), no vertex is universal, and
  deg p <= m - 9 for every p ∈ C (so deg p <= 5, and <= 4 when m = 13).
*Proof.* m >= 13 is the feasibility table (START_HERE section 4), m <= n - 2 = 14 by injectivity. For p ∈ C:
9 = f(15) <= h(C - p) <= h(C) = 9, so tau(H) = 16 - 9 = 7 and tau(H - p) = 15 - 9 = 6; apply Henning-Yeo to H - p: 102 <= 75 + 3(m - deg p). QED.
*Consequence for the sweep.* If C = A ∪ {x, y} with A one of the 2,910 saturated extremal classes, then
m(C) = 12 + k with k ∈ {1, 2} new edges, every new edge contains x or y, and deg x, deg y <= 3 + k. With k = 1 the
new edge is either {a, x, y} (Lemma E, excluded by U1) or {x, a, b} with y in no AP (then h(C) = h(A ∪ {x}) + 1, which
is 9 only if h(A ∪ {x}) = 8, i.e. x is universal in H(A) + {x, a, b}: excluded by Lemma U with n = 15, m = 13,
tau = 7: 119 > 70 + 36). So a record extension needs exactly k = 2 new edges, i.e. m(C) = 14 and
Henning-Yeo slack 3. [derived-here; not yet cross-checked by an independent agent]
