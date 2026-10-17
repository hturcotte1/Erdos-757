# Conjecture I11: 11 tau <= 3n + 2m for the AP hypergraph of every (4,5)-set [conjecture]

Written 2026-10-17 06:12 UTC. Statement, evidence, what is proved, and what a proof would need.

**Statement.** Let A be a (4,5)-set with n points, m three-term APs and h(A) = n - tau (tau = transversal number of the
AP hypergraph H(A)). Then 11 tau <= 3 n + 2 m. Equivalently, with slack s(H) = 3n + 2m - 11 tau: s >= 0.

**Why it matters.** Henning-Yeo [published] gives 17 tau <= 5n + 3m for all linear F7-free 3-graphs, hence
h >= (9n + 6)/17 and c* >= 9/17. I11 is strictly stronger for saturated sets (m = n - 2): tau <= (5n - 4)/11, so
h >= (6n + 4)/11 and c* >= 6/11 = 0.5454... > 9/17 = 0.5294... (goal clause B would follow from a proof of I11 in
general). It also gives f(16) >= 10, f(18) >= 11, f(20) >= 12, f(22) >= 13, i.e. no record set at n = 16, 18, 20, 22;
the first size where I11 allows a record is n = 23 (h = 13 >= (138+4)/11 = 12.9).

**Evidence [verified-here, experiments/falsify/i11-inequality].** 0 violations on: every subset of the seven stored
record sets and of all 2,910 saturated extremal 14-point classes and all 54,243 extremal 12-point classes; the
1,333,217-row realizable (n, m, tau) dataset; Fibonacci prefixes to n = 25; gluings; 2,028,719 one-point extensions;
the abstract censuses (12,10) and (14,12). Equality cases: (3,1,1) (one AP), (10,7,4), (12,4,4), (13,8,5), (14,12,6) = A_base,
and disjoint unions of these (gluing A_base with itself: (28,24,12), slack 0). The LP polygon of valid bounds
tau <= a n + b m over the data has vertices (0,1), (3/11, 2/11) = I11, (3/7, 0).

**What is proved.** On the class C of linear F7-free 3-graphs with e(S) <= |S| - 2 on every vertex subset (which contains
every AP hypergraph of a (4,5)-set, K3-K7), I11 holds for all n <= 22: certificates L007 (n <= 14), L008 (n = 15, 16),
L009 (n = 17, 18), L010 (n = 19, 20) and L011 (n = 21, 22), all ACCEPTED by three referees.
Consequences: f(16) = 10, f(18) = 11, f(20) = 12, f(22) = 13; no (4,5)-set with at most 22 points beats 4/7. The method is inductive: I11 at n - 1 bounds
the degrees in a hypothetical violator at n, which makes the remaining enumeration finite and small. The method does not decide the record at n = 23: the record cell (23,21,10) has slack +1, so I11 holds there and there is nothing to
refute. The induction itself continues: by computation with the unchanged L012 engine, I11 holds on C for n = 23, 24, 25, 26 as well
(experiments/20261017-1645-i11-n23-n24, experiments/20261017-1720-i11-n26; every violator cell empty; [verified-here] as a computation,
certificate L013 in preparation), and it cannot pass n = 27 without Q14: the violator cell (27,25,12) forces a degree-3 vertex whose
deletion leaves (26,22) with slack 1, and [(23,21,10), AP] is one of its three decompositions; the first I11-allowed record cells are (23,21,10), (25,23,11), (30,27,13), (30,28,13), (32,29,14), (32,30,14),
(34,32,15). At (23,21,10) the degree-4 case is excluded by realizability (L012, ACCEPTED x3, K56); the degree-3 case is open (Q14).

**What a proof must use.** Both hypotheses of C are essential: a connected linear F7-free 3-graph with (9,8,4) has slack -1
(it has m > n - 2, so it violates e(S) <= |S| - 2), and a linear (14,11,6) graph containing F7 has slack -2
(experiments/falsify/i11-inequality/f7free_nonO_violation_9_8_4.json, f7_containing_violation.json). For n <= 13 and
m <= n - 2 the only connected linear 3-graph violating I11 is F7 itself (L007 referee rounds 1 and 3). A general proof
would be a Henning-Yeo-style discharging/induction argument on C; the equality cases above show what the extremal
structures must look like (A_base-type components and disjoint APs).

**Status tags.** The inequality in general: [conjecture]. For n <= 22 on C: [verified-here] (L007-L011).
The implication c* >= 6/11: conditional on the conjecture.
