
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
- (iv): my own Delta <= 2 test (networkx atlas plus random subcubic graphs) agrees (check3). The count 27,525 equals the number of connected subcubic graphs on at most 12 vertices.
- (v): the conclusion is correct, but the proof in 7.6 has a missing case (item 1). The role tables are confirmed independently, both in the strict version and in a conservative version without the "trace not inside an edge" restriction for role_c and role_f1. A direct brute force over the 28 pairs of pieces with at most 10 vertices confirms (v), including the missing case (check2).
- Conjecture KT* is correctly tagged [conjecture], and G4 is correctly described as a restatement of KT*. The equivalence "KT* iff every connected irreducible member of C_3 lies in L*" holds in both directions: a minimal counterexample has DEF = DEF^proper = 0 by (F), and is not in L* by (C).
