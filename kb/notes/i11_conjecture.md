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
every AP hypergraph of a (4,5)-set, K3-K7), I11 holds for all n <= 26: certificates L007 (n <= 14), L008 (n = 15, 16),
L009 (n = 17, 18), L010 (n = 19, 20), L011 (n = 21, 22) and L013 (n = 23, 24, 25, 26), all ACCEPTED by three referees (K51-K55, K57).
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

**Status tags.** The inequality in general: [conjecture]. For n <= 26 on C: [verified-here] (L007-L011, L013).
The implication c* >= 6/11: conditional on the conjecture.
