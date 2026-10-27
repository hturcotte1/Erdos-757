VERDICT: NEEDS-WORK
(Workflow category: ACCEPT WITH FIXES. I found no mathematical error in any theorem presented as proved, and the GAPs are marked honestly. The first line is NEEDS-WORK only because the referee rules allow just three verdict strings and say that any remaining fixable problem means NEEDS-WORK. The required fixes are items 1 to 7 below: one missing case in the proof of Theorem 7(v), which is true by L016 and only needs a line; one unqualified remark; and five editorial items.)

Referee #1, round 1. Certificate: results/proofs/L021-i11-deficiency-route.md (submitted 2026-10-27 07:00 UTC). Work folder: experiments/prover/L021/. My scratch folder: experiments/referee/L021-round1-ref1/.

## Summary

L021 is a partial certificate and says so. It sets up the shifted potential A = 27n + 35m - 132 tau and a deficiency DEF, a maximum over families of vertex-disjoint induced copies of the 32 graphs of L*, with edge cost 35. It proves that the inequality KT (132 tau <= 27n + 35m + DEF on C_3) would give J_{1/6} on C and hence c* >= 35/66 (Theorems 1, 2). It derives the structure of a minimal counterexample to KT (Theorems 3 to 5, Propositions 8 and 9), proves KT for Delta <= 2 (Theorem 6), and verifies KT by computation up to 24 vertices (Theorem 7). KT* itself is left open as G1 to G4.

I checked every step of Theorems 1 to 6 and of Propositions 8 and 9 line by line. This includes all of the 27/35/132 bookkeeping, the Hall exchange in 3.4, the case split j = 1, 2, 3, >= 4 in 4.3, the Tutte-Berge computation, the theta table, the K4^s-to-(8,5,3)#0 identification, and the bounds 19|X| - 16 - 27 nu and 19|X| - 97. All of it is correct.

I recomputed Theorem 7(i) to (iii) and (v) with my own code, which shares nothing with kt.py, e757 or the judge:
- tau and DEF by CP-SAT integer programs;
- induced copies by VF2 monomorphisms of typed incidence graphs;
- minimum transversals by brute force;
- a direct brute force of the pure hub assemblies over pairs of pieces (R3 to R3c);
- inputs: the cell lists re-extracted from the refereed tarballs and hash-compared.

Every number agrees:
- 43 candidate triples (32 with n <= 24);
- 12 non-empty cells with 328 graphs, all re-verified;
- exactly 32 irreducible graphs, namely the full cells (3,1,1), (8,5,3), (10,7,4), (15,11,6) and (17,13,7);
- the other 296 graphs have A + DEF = 0 exactly;
- (L1) holds for all 32 pieces, and the weights are 16, 5, 13, 2, 10;
- the role tables are identical.

The prover's own scripts reproduce their outputs exactly. KT survives every induced subgraph of A_base, of the three 12-point sets and of the other record sets, as well as Fibonacci sets and hypertrees.

The defects, in order (details under Problems):
1. The proof of Theorem 7(v) omits the case in which all three hub edges go into one piece, giving a disconnected H. The statement is still true: L016 rules the case out, and so does the brute force.
2. The side remark "no saturated graph with n >= 11 is special" silently uses I11, which is proved only for n <= 27.
3. KT* is not stated to be a new conjecture that is not known to follow from I11.
4. The panel judge's sign typo is confirmed: A = 3k - 16, not 16 - 3k.
5. "The special family is 32 pieces" (title, README) is established only for n <= 24.
6. DEPENDS is out of date: L017 is now accepted, and the use of L016 in Proposition 9 is not listed.
7. The README calls Theorem 6 "new" without citing the related known results.

## Theorem-by-theorem audit (step numbers are the certificate's)

**Definition 2 and DEF.**
- The identity holds: 12(s + n/6 - 11(n-m)/12) = 36n + 24m - 132 tau + 2n - 11n + 11m = 27n + 35m - 132 tau.
- The spec normalisation holds: 3 + eps - t = 9/4 and 2 + t = 35/12, with t = 11/12.
- DEF(H) is a maximum over the finite, non-empty set of L-families of H; X = empty is always admissible, so DEF is well defined and DEF >= 0. It is invariant under isomorphism of H.
- Members are induced subgraphs H[U]. Since W depends only on the isomorphism class, a member that is isomorphic to several list entries causes no ambiguity.
- E*_H(X) is well defined. By disjointness, an edge lies inside at most one member (0.3).
- The weights are W(E_1) = 16, W(8,5,3) = 5, W(10,7,4) = 13, W(15,11,6) = 2, W(17,13,7) = 10, and A(14,12,6) = +6. I recomputed all of them from the graphs (check1).
- Correct.

**Step 0.**
- 0.3 (edge partition), 0.4, 0.5 (E*_H(X u Y) = E*_H(X) disjoint-union E*_R(Y)) and 0.6 (additivity of DEF and P) are correct. I re-proved each inclusion in both directions.
- 0.2 (n >= m on C, and n >= m + 2 for n >= 2) is (P3) applied to S = V.
- Randomised tests of the identities 0.3, 0.5, 4.1 and 5.1 on graphs from the cell lists gave no failure (check5).

**Theorem 1.**
- (a) Take a minimal violator H with fewest vertices and a vertex v of degree d >= 4. Then 11 tau(H) <= 11(tau(H-v) + 1) <= (3+eps)(n-1) + 2(m-d) + 11 = (3+eps)n + 2m + (8 - eps - 2d) <= (3+eps)n + 2m - eps. So H satisfies J_eps, a contradiction. The proof needs only that C is hereditary and that the minimal violator has fewest vertices. Correct.
- (b) For a (4,5)-set, H(A) is in C and m <= n - 2 (K4 to K7, [published]). Then 11 tau <= (5 + eps)n - 4, so h >= ((6 - eps)n + 4)/11 > (6 - eps)n/11. Since c* = inf f(n)/n (K1), c* >= (6 - eps)/11. Moreover (6 - eps)/11 > 9/17 iff eps < 3/17, and for eps = 1/6 the bound is 35/66, since 595 > 594. Correct.

**Theorem 2.**
- 2.1: W(F) <= 11(n_F - m_F) iff 66 tau_F <= 19 n_F + 12 m_F, which is J_{1/6}. For L* this follows from L016, since all members have at most 17 vertices. I also checked it directly on all 32 pieces: s(F) is 0 or 1 and W <= 11(n - m) (check1).
- 2.2: DEF_H(X) <= 11(n - m) - 11(n(R) - m(R)) - 24|E*| <= 11(n - m), using n(R) >= m(R) for R in C or R empty.
- 2.3: KT gives 132 tau <= 38n + 24m, that is J_{1/6}.
- DEF enters only through the upper bound 11(n - m). This is exactly where the edge cost 35 exceeding the "J_{1/6} edge price" 11 is used: each E* edge costs 35 in DEF but changes n - m by -1.
- Correct.

**Theorem 3.**
- (A): additivity, plus P(empty) = 0 and P(K_1) = 27.
- (B): T_R together with the union of the T_F is a transversal of H, so A(H) >= A(R) - DEF_H(X). Combined with 0.5 this gives P(H) >= P(R) >= 0. The graph R is in C_3 and strictly smaller (V(X) is non-empty).
- (C): take X = {H}, so E* = empty.
- (E): Hall on the bipartite graph between E*(X*) and X*.
  - A matching saturating E*(X*) gives, through (L1), one prescribed vertex per member and contradicts (B).
  - Otherwise there is S with |N_B(S)| < |S|. Put X' = X* \ N_B(S). X' = empty contradicts |E*| <= |X*|.
  - Otherwise E*(X') is contained in E*(X*) \ S: an edge of E*(X') meets V(X'), so it lies inside no member of N_B(S), and it is not in S. This contradicts the minimality of |E*| - |X|.
  - I checked the exchange line by line. It is correct.
- (F): with (E) and (L2), DEF_H(X) <= 35|X| - 35(|X| + 1) < 0.
- Correct as stated, under (L1) and (L2).

**Theorem 4.**
- 4.1: E*_H(X') = E*_{H-v}(X') disjoint-union K. With (F) and W <= 16 this gives DEF(H - v) <= max(0, 35d - 54).
- 4.2: if tau(H - v) = tau(H), then A(H) >= 27 + 35d - max(0, 35d - 54) = min(27 + 35d, 81) >= 62 > 0.
- 4.3: the free hub holds, 27 + 105 = 132, so A(H - v) = A(H) and DEF(H - v) >= 1. The two constraints are (i) 35 e_v <= 16|X_v| - 1 and (ii) e_v + k_v >= |X_v| + 1.
  - j >= 4 gives 19j <= 69, which is impossible.
  - j = 1 gives e_v = 0 and k_v >= 2.
  - j = 2 gives e_v = 0 and k_v = 3.
  - j = 3 gives e_v = 1, k_v = 3 and sum W >= 36.
  - All four cases are correct.
- e_v = 0 together with connected members makes the members components of H - v.
- The bounds A(H) >= -(sum W - 35 e_v) and A(H) >= -32 hold. The Claim-B transfer to X_v in H is valid by 0.4.
- Correct.

**Theorem 5.**
- If tau does not drop, DEF(H \ e) >= 35 - A(H).
- If no member of the optimal family contains e in its vertex set, every member is induced in H and E*_H is contained in E*_{H\e} together with {e}. Then DEF_H > 0, which contradicts (F).
- Correct.

**Theorem 6.**
- 6.1, the dual graph: N = m, M = n_2, n_1 = 3N - 2M, n = 3N - M. The identity tau = N - nu(G) is L017 4.2 = HY EJC 2017 Prop. 9. I re-derived it: covering by T_2 (degree-2 vertices) and T_1 gives |covered| <= |T| + nu. This yields A = 132 nu - 16N - 27M.
- The C_3-membership argument holds: |E(G[U])| <= 2|U| - 2.
- 6.2: Tutte-Berge with M <= 3|U| + sum e_i gives A >= 35|U| + sum theta_i.
- 6.3 is the theta table. c = 5 with e = 7 forces degrees (3,3,3,3,2), and the complement in K5 is P3 + K2, so the graph is K4^s with theta = -5. For even c >= 6, theta >= 19c/2; for odd c >= 7, theta >= (19c - 105)/2 >= 14. The numerical check confirms that, among all 113 connected subcubic graphs with at most 7 vertices, theta < 0 only for K_1 (-16) and K4^s (-5) (check3).
- 6.4, the family X:
  - The singleton components give induced E_1 copies, by linearity.
  - Each K4^s component together with the third vertex p of the subdivision edge gives an induced 8-vertex, 5-edge subgraph with dual K4^s whose pendant vertex sits on the subdivision vertex. This is (8,5,3)#0 = {012, 156, 247, 346, 357}. I re-derived the dual: ab, ac, bd, be, cd, ce, de, which is K4 on {b,c,d,e} with bc subdivided by a.
  - Members are disjoint because they come from different components of G - U.
  - E*_H(X) is contained in U. An outside edge meeting a member does so through a degree-2 vertex whose other G-end is in U, or through p.
- 6.5: P >= 35|U| - 16 o_1 - 5 o_5 + 16 o_1 + 5 o_5 - 35|U| = 0.
- Correct.
- Related known results: the identity is HY 2017 Prop. 9 (cited). Matching lower bounds for subcubic graphs of Chvatal-Hanson / Biedl et al. type are related. The certificate makes no novelty claim; the README's "(new, via Tutte-Berge)" should cite these (item 7).

**Proposition 8.**
- 8.1 (H.1): Hall on B - e with |X| = |X| sides. Since E*_H(S) = N_B(S) for S contained in X, a Hall violator S gives |E*_H(S)| <= |S|, which contradicts (E).
- 8.2: the replacement transversal and the counts n(H) = n(H') - nu + sum n_F and m(H) = m(H') + sum m_F + |X| give A(H) >= A(H') + 19|X| - 27 nu.
- 8.3: DEF(H') <= 16.
  - Case 1: Q = X u Y has |E*_H(Q)| <= |Q|, which contradicts (E).
  - Case 2: Q = X u (Y \ {R'}) is another minimiser with |Q| > |X|, which contradicts the maximality of |X|.
- 8.4: for (H_1), H' is in C_3: no F7 (minimum degree 2), linear, (P3), and u's degree does not grow. The size n + m drops. The bounds give 3, 14 and 6 for nu = 0, 1, 2. For (H_0), R = empty by connectivity and A >= 19|X| - 97 >= 17.
- The concluding "only (D1) with k_v = 3 remains" is correct given |E*| >= |X| + 2: then j = 1 needs k_v = 3, and j = 2 and j = 3 need k_v >= 4.
- Correct as a conditional statement.
- I also re-derived the judge's observation that G2 is narrower than stated (item 8). It is a suggestion, not a defect.

**Proposition 9.**
- 9.2: B = H[V(F) u {v}] = F + v + e_1 + e_2. A transversal of B with at most tau(F) vertices avoids v and would be a minimum transversal of F meeting Q_1 and Q_2, which (D1) excludes. So s(B) = s(F) - 4 < 0 with at most 18 vertices, which contradicts L016.
- 9.3: B' = H[V(F) u {v, o}], with the edge set argued correctly: o's other edges avoid v by linearity and avoid V(F) because F is a component of H - v. Here s(B') = s(F) - 1, which is negative for tight F, and n(B') <= 19, which contradicts L016.
- 9.1: the slacks s = (A + 9n - 11m)/12 are 0, 1, 0, 1, 0 for the five types. I recomputed them.
- Correct.

**Theorem 7 (computations).**
- (i), (ii) and (iii) are reproduced exactly by independent code (check1).
- The candidate scan's pruning rules are all valid for connected members of C_3 with n <= 27: n <= 2m + 1, 3m >= n, m <= n - 2, s >= 0 (L016), 17 tau <= 5n + 3m (K8) and A < 0. The lists used are complete by L013 Lemma E' (I11 below n, n <= 24).
- The logic of 7.3 is correct: A >= 0 is trivial; a member of L* is handled by X = {H}; otherwise DEF >= DEF^proper >= -A.
- (iv): my own Delta <= 2 test (networkx atlas plus random subcubic graphs) agrees (check3). delta2_test's per-N counts agree with the atlas for N <= 7 (113 graphs), and its N <= 10 run is reproduced identically (2,571 graphs).
- (v): the conclusion is correct, but the proof in 7.6 has a missing case (item 1). The role tables are confirmed independently, both in the strict version and in a conservative version without the "trace not inside an edge" restriction for role_c and role_f1. A direct brute force over the 28 pairs of pieces with at most 10 vertices confirms (v), including the missing case (check2).
- Conjecture KT* is correctly tagged [conjecture], and G4 is correctly described as a restatement of KT*. The equivalence "KT* iff every connected irreducible member of C_3 lies in L*" holds in both directions: a minimal counterexample has DEF = DEF^proper = 0 by (F), and is not in L* by (C).

## Checks performed (all in experiments/referee/L021-round1-ref1/; each run as `timeout ... nice -n 10 python3 ...`, one process at a time)

- **R0: integrity of inputs.** I extracted experiments/prover/L012/cells.tar.gz and L013/cells.tar.gz into tar/ and tar13/. The sha256 of each of the 34 stored lists from L012 and L013 that scan_cells.py uses equals the tarball copy: **34 checked, 0 mismatches**. The three L016 lists are used only for n >= 25 and are not load-bearing.

- **R1: the candidate triples of 7.1, by my own enumeration.**
  - Constraints: n <= 2m + 1, 3m >= n, m <= n - 2, s >= 0, 17 tau <= 5n + 3m, A < 0, with 3 <= n <= 27 and all tau.
  - Result: **43 triples, identical as a set to scan_cells_output.txt; 32 of them have n <= 24.**

- **R2: check1.py 24 (Theorem 7(i) to (iii)), from scratch.**
  - Every listed graph in the 32 candidate cells with n <= 24 was re-verified: n, m, distinct edges, connected, linear, F7-free, (P3) by Hall matchings, Delta <= 3, and tau by a CP-SAT ILP.
  - The closure was then run in increasing n. For each graph, all induced copies of the pieces found so far with fewer vertices were found by VF2, DEF was maximised exactly by a CP-SAT ILP, and the optimal family was re-evaluated from the definition.
  - Result, from check1_report_output.txt (generated from check1_pieces.json): **328 graphs in 12 non-empty cells**:
    - (3,1,1): 1, (8,5,3): 2, (9,4,3): 1, (10,7,4): 4, (14,8,5): 9, (15,7,5): 2, (15,11,6): 19, (16,10,6): 16, (17,13,7): 6, (21,10,7): 5, (22,13,8): 85, (23,16,9): 178;
    - the other 20 candidate cells are empty;
    - **irreducible: exactly 32, the full cells (3,1,1), (8,5,3), (10,7,4), (15,11,6), (17,13,7);**
    - **all 296 others have A + DEF = 0 exactly, none > 0;**
    - the 32 pieces are identical, in names and edge lists, to the prover's closure_results.json.
  - Piece table, with all minimum transversals by brute force over k-subsets:
    - (L1) holds for 32/32;
    - W = 16, 5, 13, 2, 10;
    - s in {0, 1};
    - J_{1/6} holds and W <= 11(n - m);
    - max W = 16;
    - **piece failures: 0**;
    - the numbers of minimum transversals match l1_check_output.txt.
  - The run took about 25 minutes. The tail of its stdout was lost because the shared repository was rewritten at 08:13:34 UTC while the run was in progress (commit 4625917 "reviews and live scratch of running agents"). The JSON is written at the very end of the run and is complete, and check1_report.py prints it.

- **R3: check2.py 10 (Theorem 7(v)).**
  - (a) Role counts from brute-force minimum transversals. The strict version is identical to roles_output.txt: role_b > 0 only for E_1 (1); role_e > 0 only for (8,5,3)#0 (2) and #1 (3); role_c = role_f1 = 0 for all 32. In the conservative version (no "trace not inside an edge" restriction), role_c and role_f1 are still 0 for all 32, and role_b > 0 only for E_1.
  - (b) Direct brute force without the pattern analysis, over all 28 pairs of pieces with at most 10 vertices. Every hub with three pairwise disjoint pairs of G-degree <= 2 not inside an edge was enumerated, in all distributions including the one leaving a piece unattached. Result: **249 tau-raising configurations, 19 of them in C_3, all 19 isomorphic to (17,13,7) pieces; 0 counterexamples to (v).**
  - **R3b: check2b.py 10.** The same brute force over 31 pairs: the four large pieces (15,11,6)#0, #11 and (17,13,7)#0, #4, each with every piece of at most 10 vertices, plus three large-large pairs. Result: **130 tau-raising configurations. Every one of them has all three pairs inside one piece (the distribution omitted in 7.6, item 1), and none is in C_3: 0 counterexamples.**
  - **R3c: check2c.py 10**, the same brute force over **all 528 pairs** of the 32 pieces: see the line at the end of this section.

- **R4: check3.py 12 80 (Theorem 6).**
  - Theta table on all 113 connected subcubic graphs with at most 7 vertices (networkx atlas): theta < 0 **only for K_1 (-16) and K4^s (-5)**.
  - KT on the duals of these 113 graphs plus 80 random connected subcubic graphs with 8 <= N <= 12. Each dual was checked to be in C_3. tau(H) was computed by ILP and compared with N - nu(G) (networkx matching), and A was compared with 132 nu - 16N - 27M. DEF was computed by ILP over all 32 pieces.
  - Result: **193 graphs, 4 with A < 0, 0 failures, min P = 0.**

- **R5: check4.py (data).**
  - The record sets of data/small_records.json (n = 8, 10, 11; the three 12-point sets; A_base) were checked to be (4,5)-sets by brute force over all 4-subsets, with H built by my own AP code.
  - For **every induced subgraph** (16,383 for A_base), I computed tau by brute force and DEF by exhaustive family enumeration. Theorem 2 (0 <= DEF <= 11(n - m)) has **0 violations**. KT on all induced subgraphs with Delta <= 3 has **0 violations** (min P = 0). The 8-point record is itself an (8,5,3) piece: A = -5, P = 0.
  - Fibonacci sets {F_3, ..., F_k} for n = 4..22: 0 violations.
  - Random hypertrees with a perfect matching, k = 0..6: **A = 3k - 16** and DEF = max(0, 16 - 3k), so P = 0 for k <= 5 and P = 2 for k = 6.
  - F7: A = -32, DEF = 0.
  - Sanity values by hand: A_base A = 6 with J slack 14; 12-point A = 14 with J slack 18; S_K A = 84 + 30K with J slack 53 + 15K; C003 A = 264 with J slack 143. All agree with the certificate.

- **R6: check5.py 5 8.** Randomised tests of the set identities 0.3 (edge partition), 0.5 (E*_H(X u Y) = E*_H(X) disjoint-union E*_R(Y)), 4.1 (E*_H(X') = E*_{H-v}(X') disjoint-union K) and 5.1 (members are induced in H, and E*_H is contained in E*_{H\e} together with {e}), on random L*-families in graphs from six cell lists: **240 tests, 0 failures.**

- **R7: re-runs of the prover's own scripts.** These are copies in prover_rerun/ with their output paths redirected to my folder. I read the code of kt.py first and checked three properties:
  - the induced-copy matcher maps BFS-ordered piece vertices with common-neighbour candidate sets and a degree filter, and then checks that exactly m_P host edges lie inside the image, which tests isomorphism and inducedness;
  - the DEF branch and bound uses objective(X) = sum(W + 35 m_P) - 35 |edges meeting U| = sum W - 35|E*|, with bound obj + sum of W over the remaining disjoint copies, which is valid because E* is monotone under adding disjoint copies;
  - tau_masks and min_transversals are exact (branching on the vertices of an uncovered edge, with the forbidden-vertex trick so that each transversal is produced once).

  Re-run results:
  - `scan_cells.py`: output **identical**;
  - `closure.py`: output **identical** (timings stripped), and closure_results.json **identical**;
  - `l1_check.py`, `roles.py`, `sanity.py`: **identical**;
  - `validate_def.py`: **identical** (173 graphs, 0 mismatches);
  - `delta2_test.py 10`: **identical** (2,571 graphs, 7 with A < 0, 0 failures).
  - Not re-run:
    - `delta2_test.py 12` (27,525 graphs): R4 tests Theorem 6 independently, and the N <= 10 part matches;
    - `attach.py`: illustrative and partial, used only for G1;
    - `random_assemblies.py`: uninformative, by the certificate's own account.
- **R3c: check2c.py 10** (all 528 pairs) was still running when I wrote this review: 410 of 528 pairs done, every completed pair with 0 counterexamples. The tau-raising configurations in C_3 found so far are only the 19 from (8,5,3) + (8,5,3), all isomorphic to (17,13,7) pieces.

## Problems found, in order of severity

1. **Theorem 7(v): the proof omits a case. The statement is true. Minor gap, one-line fix.**
   - As stated, (v) covers every H in C_3 with a degree-3 vertex v such that H - v is the disjoint union F_1 + F_2 of two members of L* and tau(H) = tau(H - v) + 1. Connectivity of H is not assumed.
   - 7.6 asserts that the distribution of the three pairs is one of (b), (c1), (c2), (e), (f). That list (L017 7.3) excludes the distributions {1,1,1} and {2,2,2}, in which all three pairs lie in one piece. L017 can exclude them because there H is connected, by L017 Theorem 4(ii).
   - The distribution {1,1,1} gives a disconnected H = (F_1 + v) + F_2. It is not isomorphic to a member of L*, so 7.6 does not cover it as written.
   - The case is empty. F_1 + v = H[V(F_1) u {v}] lies in C, has tau(F_1) + 1 and slack s(F_1) - 2 < 0, and has at most 18 vertices, which contradicts L016.
   - My brute force enumerates this distribution explicitly (check2 and check2b, and check2c over all 528 pairs, R3c). Every τ-raising configuration of this kind lies outside C_3. For example, (8,5,3) with all three pairs gives the (9,8,4) graphs, which violate (P3), and (15,11,6) gives (16,14,7) graphs outside C.
   - Fix: add "connected" to (v). The only application, case (D2) in a minimal counterexample, has H connected. Alternatively, dispose of {1,1,1} by L016 in one sentence.

2. **An unqualified statement relies on I11 beyond its proved range.** The Note after "The list L*" says: "no saturated graph (m = n-2) with n >= 11 is special, since then A = 12s + 2n - 22 >= 0".
   - The inequality needs s >= 0, which is I11. I11 is proved on C only for n <= 27 (L016).
   - For n >= 28, Henning-Yeo gives only s >= -(3n + 2)/17, and then A could be negative.
   - The remark is not used in any proof, but as written it is unproved for n >= 28.
   - Fix: append "(for n <= 27 by L016; in general under I11)". Remark 2.4 already words its analogue correctly ("with s >= 0").

3. **KT* is not labelled as a new conjecture independent of I11.**
   - The certificate tags KT* [conjecture], but nowhere says that it is introduced here and is not known to follow from I11. It is also not known to imply I11: it implies only J_{1/6}.
   - I11 gives A = 12s - 9n + 11m >= 0 only when 11m >= 9n. In the sparse region KT needs DEF to compensate. The candidate cells (21,10,7) (s = 6, A = -7) and (27,13,9) (s = 8, A = -4) show that I11-satisfying graphs with A < 0 exist or are allowed.
   - The only evidence for KT* is Theorem 7 (n <= 24). The random assemblies never reached A < 0.
   - Fix: one sentence after Conjecture KT* and in the CLAIM-TYPE line.

4. **Sign typo (Sanity checks, hypertrees with a perfect matching).** The text has "A = 16 - 3k"; the correct value is A = 3k - 16.
   - The prover's own sanity_output.txt shows A = -13, -10, -7, -4, -1 for k = 1..5.
   - My check4 confirms A = 3k - 16 and DEF = 16 - 3k on random hypertrees with a perfect matching for k = 0..5, so P = 0. For k = 6: A = 2, DEF = 0.
   - As printed, the line is internally inconsistent: A + DEF would be 32 - 6k, not 0.

5. **"The special family is 32 pieces" is overstated.**
   - The title says "the computed special family (32 pieces)", and experiments/prover/L021/README.md line 16 says "The special family, computed exactly from the stored refereed lists, is 32 pieces".
   - Both must say "among connected members of C_3 with at most 24 vertices". The candidate cells (25,14,9) (only a D2 list), (26,13,9), (26,17,10) and the four n = 27 cells are not computed.
   - Theorem 7(i) and GAP G4 are correctly qualified.

6. **DEPENDS block: one status out of date and one use of L016 missing.**
   - DEPENDS describes L017 as "[round 1: two referees, no mathematical error; round 2 pending]". L017 is ACCEPTED (round 2: two referees ACCEPT; K64).
   - DEPENDS says L016 is "used only in the cell scan of Step 7 ... and for J_{1/6} of the pieces (Theorem 2)". L016 is also used in Proposition 9 (9.2 and 9.3 end with "contradiction with L016"), and it would be used in the fix of item 1.
   - Both lines should be updated.

7. **Novelty wording (README only).**
   - The README calls Theorem 6 "(new, via Tutte-Berge)".
   - The identity tau = N - nu(G) is HY EJC 24(2) (2017) P2.50 Prop. 9, which the certificate cites. The matching bound behind Theorem 6 belongs to the Chvatal-Hanson / subcubic-matching circle of results.
   - The README should cite these and leave the novelty question to the scout. The certificate itself makes no novelty claim.

8. **Suggestion, not a defect: G2 is narrower than stated.**
   - Let p, q in ∂(X) share no edge of R = H - V(X), with |X| >= 3 and |∂(X)| >= 2. Then the replacement e' = {p, q, z} (z new) always lies in C_3:
     - z has degree 1 and F7 has minimum degree 2, so no copy of F7 uses z;
     - linearity holds because no edge of R contains both p and q;
     - (P3) holds because e_{H'}(S) = e_R(S - z) + 1 <= |S| - 2;
     - p and q each lose an E* edge, so no degree exceeds 3.
   - 8.2 and 8.3 apply verbatim with nu = 1 and give A(H) >= 19|X| - 43 > 0.
   - So for |X| >= 3 and |∂(X)| >= 2 the only remaining exception is "every two vertices of ∂(X) share an edge of R". I re-derived this; the panel judge noted it first.

## GAPs as marked, and whether anything outside them is unproved

The certificate marks four GAPs. I agree with each description.
- **G1: impure configurations.**
  - (D1) with H - v = F + G', G' non-empty;
  - (D2) with H - v strictly containing F_1 + F_2;
  - (D3).
  - The free-hub accounting gives exactly A(H) >= A(G') - W(F). This is balanced, so it yields no contradiction.
- **G2: Claim H in the exceptional cases.** The replacement leaves C_3, or |X| is small for the given boundary size. For |∂(X)| = 0 and |X| <= 5 there is a finite check, not done. Item 8 above narrows G2.
- **G3: degree-2 vertices.** Deleting such a vertex costs exactly 35, so Theorem 4 gives nothing there beyond co-transversality.
- **G4: the special family outside n <= 24.** This is KT* itself, as the certificate says.

Consequently KT* and c* >= 35/66 are not proved, and the certificate says so in its CLAIM-TYPE line and in the GAP section.

Outside G1 to G4, I found only two things that are not proved as written:
- the missing case in the proof of Theorem 7(v) (item 1; the statement is true by L016);
- the unqualified remark on saturated graphs for n >= 28 (item 2; not used anywhere).

Everything else presented as proved is proved. This covers Theorems 1 to 6, Propositions 8 and 9, Theorem 7(i) to (iv), and the "Closes" list of the GAP section.

## Independence statement

Before writing this review I did not read any other review of L021. I read section 1 (on L021) and the header of experiments/prover/panel-synthesis/SYNTHESIS.md, as the task instructed. I verified each of its points myself:
- the sign typo;
- the 32-pieces overstatement;
- the KT*/I11 labelling;
- its observation (b) on G2.

I did not look inside experiments/referee/L021/, which belongs to someone else.

My scripts in experiments/referee/L021-round1-ref1/ import neither experiments/prover/L021/kt.py nor e757 nor judge/:
- rcore.py, the core module: CP-SAT integer programs for tau and DEF; VF2 subgraph monomorphisms of typed incidence graphs plus an induced-edge count for the copies; brute-force minimum transversals; class-C tests by pairs, an explicit F7 search and (P3) by Hall matchings;
- check1.py to check5.py.

They read only:
- the cell lists that I re-extracted from the refereed tarballs;
- the edge lists of the 32 pieces in closure_results.json, which check1 re-derives from scratch.

The prover's own scripts were re-run only as copies in prover_rerun/, with their output paths redirected, so that no file outside my scratch folder and this review was written.
