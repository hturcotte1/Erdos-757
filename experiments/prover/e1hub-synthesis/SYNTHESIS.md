# E1-hub synthesis: L025 (I11 form) and L026 (KT form)

Judge: referee agent (opus), 2026-10-27, 09:58 to 10:35 UTC.

Scope. I read in full:
- results/proofs/L025-e1hub-lemma-i11-form.md (submitted 09:56 UTC);
- results/proofs/L026-e1hub-lemma-kt-form.md (09:40, revised 09:55 UTC).

I also read:
- the statement, Lemmas 1-2, Lemma A/A+ and Proposition 5 of results/proofs/L024-kt-reduction.md;
- L017 Theorems 2, 4 and 5 (statements);
- L019 Theorems 3 and 5 (statements);
- experiments/prover/panel-synthesis/SYNTHESIS.md, sections 0 to 5;
- kb/notes/i11_conjecture.md;
- the K71 and K72 rows of kb/known_results.md.

I did not edit any certificate. My scratch code is in experiments/prover/e1hub-synthesis/checks/ (hyp.py, checks.py). It is my own code; it does not import e757/, judge/ or any L0xx code.

Tags:
- [checked, judge]: hand proof read line by line and found correct.
- [verified-here, judge]: recomputed by my own code (see the Appendix).
- [derived-here, judge, unrefereed]: a new argument written here. A prover must write it out and a referee must check it before anyone relies on it.

Notation as in L025:
- s = 3n + 2m - 11 tau;
- G (+) (a,b,c) is the hub;
- a b-configuration is a non-edge triple of vertices of degree <= 2 that is pairwise non-co-transversal (NC);
- it is pendant if all three have degree 1 and lie in three different edges.
- For a pendant triple: e_a = {a} ∪ A, e_b = {b} ∪ B, e_c = {c} ∪ C, W = A ∪ B ∪ C, G'' = G - {a,b,c}, tau'' = tau(G'').

## 0. Bottom line

1. **The two attempts agree, and neither proves the lemma.**
   - Every hand-proved step I checked is correct. Both certificates mark their gaps honestly.
   - I found no load-bearing statement that is claimed without a GAP but is unproved.
   - The defects are editorial (Section 1) plus one testing gap in L025, which I filled (check S3).
2. **The I11 form has a one-case residual.**
   - L025 Theorem 10 proves the I11 form completely except for one case, and the proof is clean. If G in C is connected with s(G) <= 1 and I11 holds up to n(G)+2 vertices, every b-configuration is pendant and s(G) = 1.
   - Neither Delta <= 3 nor n >= 27 is needed.
   - So in the I11 form, everything except the **pendant triple of a slack-1 graph** is proved.
   - That remaining case is reduced to a rigid structure (L025 Theorem 12): s(G'') = 8; the six attachment vertices W are distinct and avoided; and all of W lies in one tight set S_0. This is not a finite computation.
3. **The KT form has the same residual, with an extra finite family.**
   - L026 Theorem 12 reduces the KT form to the same pendant configuration when n(H) > 73.
   - When n(H) <= 73 there is an extra, uncomputed finite family A1.
   - **Cross-pollination removes A1 on the L024 route** (Section 4.1, my derivation). L024's GAP R3 is stated under the apex hypothesis (AH). Under (AH), an outer vertex of G'-degree 2 is impossible by C10 (no member of L* contains a hub triangle). I re-verified C10 with my own code.
   - So on the L024 route the KT residue is also exactly the pendant case, for every n >= 25, given cell(24,19,10,3) = ∅.
4. **The decisive missing step is the pendant-triple lemma PT** (Section 3). In I11 form: a connected slack-1 member of C with Delta <= 3 has no three pairwise-NC degree-1 vertices in three different edges. Equivalently, there is no slack-8 graph G'' with three disjoint avoided pairs A, B, C that no (tau''+1)-transversal meets simultaneously.
   - This is the common residual of both certificates (L025 GAP; L026 GAP A2 and GAP B).
   - Conjecture P2+ would imply it.
5. **Dependency status has improved since L026 was written.**
   - L021's proved parts (K71, including Theorems 3 and 7) and L022 Theorem 2 (K72) are now ACCEPTED. The DEPENDS ON lines of L024 and L026 that call them unrefereed are outdated.
   - Still unrefereed in L026: C10 (independently re-verified here) and the emptiness of cell(24,19,10,3), used in Theorem 12(f) and (k1).

## 1. Verdict per attempt

### L025: I11 form (pendant reduction)

**Proved, and checked by me:**
- **Lemma 1 (hub)** [checked, judge]. All three (P3) cases are right: S_1 = ∅; S_1 a proper non-empty subset of {v,x,y,z}, where h <= |S_1|-1; and S_1 = {v,x,y,z}, where h = 1 + |S_0 ∩ {a,b,c}|. The tau formula is right: tau+1 iff some minimum transversal contains two of a, b, c. The slack changes by +9 or -2.
- **Lemma 2 (fold, s-1)** [checked, judge]. **Lemma 3 (pendant replacement)** [checked, judge]: tau(G^p) = tau(G) needs c to be co-transversal and {a,c}, {b,c} to be NC, and the slack is s + 2 - 2d(c).
- **Lemma 4 (identification, s-3)** [checked, judge]. This is the same as L026 Lemma 11.
- **Lemma 5 (move, s-3)** [checked, judge]. The step "x_1 is not in T'" is right: otherwise T' would be a (tau-1)-transversal of G.
- **Lemma 6 (edge on three avoided vertices, s-9)** [checked, judge]. **Lemma 7 (pendant edges on pairs)** [checked, judge].
- **Lemma 8 (one vertex, two vertices)** [checked, judge]. **Lemma 9 (triple deletion)** [checked, judge]: a drop of 1 gives s(G-abc) = s+2-2|∂| <= s-2, since |∂| >= 2 because {a,b,c} is not an edge.
- **Theorem 10** [checked, judge].
  - The three rules hold under the stated hypotheses (all vertices co-transversal by free choice, 0.3):
    - R1 (pendant replacement at n vertices): if a, b are non-adjacent then d(c) = 1;
    - R2 (pair lemma at n-2): two vertices of degree 2 are adjacent;
    - R3 (triple deletion at n-3): no vertex has all its edges meeting the other two.
  - The four-pattern case analysis in 8.5 is complete:
    - all three pairs adjacent contradicts R3;
    - two adjacencies contradict R1, since d(a) >= 2;
    - one adjacency gives R1 twice, and then R3 fails;
    - with no adjacency the triple is pendant.
  - The fold at n+2 vertices then forces s = 1.
  - Hypotheses used: only (H_{n+2}). Neither Delta <= 3 nor n >= 27 is used.
- **Remark 10.4 (the degree bound is automatic)** [checked, judge].
- **Corollary 11** [checked, judge].
  - (a) follows from Theorem 10.
  - (b) If G' had two components, the matching P_1 -> {x,y,z}, P_2 -> G_1, P_3 -> G_2 saturates the three pairs, which contradicts L017 Theorem 4(iii) (accepted). Hence G' is connected.
  - (H_{n(G')+2}) holds because n(G') + 2 = n(H) - 2.
- **Theorem 12 (a)-(k)** [checked, judge].
  - (a): Lemma 9 with |∂| = 3 gives s(G'') = 8. W is avoided because a minimum transversal of G'' meeting A, plus {b,c}, would contradict the NC pair {b,c}.
  - (b): Lemma 8(a) forces each component to have slack >= 5, or to be an avoided isolated vertex with slack 3, and the slacks sum to 8. The edge Y = {w_0,u_2,u_3} then gives slack -1.
  - (c): deleting {u,x}, with u in A ∩ B and x in C, gives |∂| <= 1, and linearity is then violated.
  - (d): the transversal triples drop tau by exactly 1.
  - (e) holds.
  - (f): the F_7 shapes and the reduction of the (P3) failures to tight sets of G''. Here the tight sets have size >= 4 (identification) or >= 5 (move).
  - (g) and (h): pendant pairs, with slacks -4 and -10.
  - (i) holds.
  - (j): the two moves M(a -> a_1; b,c) and M(a -> a_2; b,c) cannot contain F_7, by (i), so they give tight sets S_1 and S_2. Since |S_1 ∩ S_2| >= 4, their union is tight. The largest tight set S_0 containing W is tight, and n ≡ 1 (mod 11) in the saturated case.
  - (k): the degree count 2n_1 + n_2 = 6.
- **Lemma 13 (pendant block)** [checked, judge]: s(H) = s(H^#) + s(H_2 - c) + 2 d_{H_2}(c) >= 2. Its consequence (at least 2 edges leave S_H) is also checked.

**Marked GAP:** the pendant case. This consists of R1a (S_0 = V(G''): saturated, n(G) in {34, 45, 56, ...}) and R1b (S_0 a proper subset, with >= 2 crossing edges), with P2+ as a sufficient condition. The GAP is correctly described as not a finite computation.

**Claimed without a GAP but not proved:** nothing load-bearing. Editorial points:
1. **Definition of "tight set".** L025 defines a tight set as |S| >= 2 with e(S) = |S| - 2. Every 2-set {x,y} is then "tight" (e = 0). So the exception clause of Lemma 4 ("or G has a tight set containing x and y") is literally always satisfied, and the lemma as stated says nothing. The proof (4.3) actually produces S = S' ∪ {y} with |S| >= 3.
   - Fix: write "a tight set S ⊇ {x,y} with |S| >= 3", which is L026's "saturated set".
   - Theorem 12(e), (f) and (j) involve sets of size >= 3 (Y, A∪B, {a_i}∪B∪C, W), so nothing downstream breaks.
2. **Remark 10.3.** The bound n(G) >= 27 (so n(G'') >= 24 in the GAP) rests on unrefereed computations: the L017 C4/C5 tables and the L020 computations. It is tagged as such. Fine.
3. **Testing gap (W1).** The residual of Theorem 12 has s(G'') = 8 exactly, but W1 tested slack-7 and slack-9 cells and, at slack 8, only the trivial (5,2,1). I filled this gap (check S3, Appendix).
   - S3 covers all stored slack-8 lists: (5,2,1,3), and (9,7,3), (12,8,4), (15,9,5), (18,10,6), (21,11,7), (24,12,8), all with Delta <= 2.
   - These have at most one avoided vertex per class (histograms: (15,9,5) has {0:84, 1:7}; (18,10,6) has {0:64, 1:3}; the others have none). So there is no candidate (A,B,C) at all, and 0 hits.
   - The (21,11,7) and (24,12,8) lists would have given I11 violators at n(H) = 28 and n(H) = 31.
4. **Theorem 12 hypothesis.** The header asks for (H_{n(G)}), and (h) uses exactly (H_n). Consistent.

**Finite computations it needs:** none that is decisive.
- W2 (a falsifier for the residual at 24 <= n(G'') <= 40) and W3 (P2+ beyond n = 26) are tests only.

**Verdict:** correct. Of all the E1-hub material, this is the strongest and cleanest content. It depends only on accepted certificates: L017 for Corollary 11(b) and Lemma 13, and L016 only through Remark 10.3.

### L026: KT form (plus the I11 form for tight outer graphs)

**Proved, and checked by me:**
- **Theorem 1** [checked, judge]: hub arithmetic in C_3 and in C (A changes by +116 or -16), and the fold (A - 8, s - 1).
- **Lemma 2** (families in induced subgraphs), **Lemma 3** (DEF(G) <= 16 for connected G, <= 10 if n >= 11, with the case table 3.4) and **Lemma 4** (avoided vertex, P >= P(G-u) + 27) [checked, judge].
- **Lemma 5 (bridge), Lemma 6 (pendant block) and Corollary 7** [checked, judge]: the injection psi: w -> c and the E* count of 6.5.
- **Theorem 8(a)-(e)** [checked, judge].
  - (a): three components contradict Lemma 5 at e_a, e_b and e_c. With two components, Lemma 6 makes G_2 = {c}, and then DEF(G_1) >= 12 contradicts Lemma 3, since n(G_1) >= 11.
  - (b): co-transversality of the outer vertices follows from P(G') <= 25 < 27.
  - (c), (d) and (e) (the component count with N = 4) are checked.
- **Lemma 9** (positive deficiency: p odd, p <= 11, a p-piece tree) and **Lemma 10** (boundary count, from Claim E) [checked, judge].
- **Lemma 11 and Corollary 11.1 (merge)** [checked, judge].
- **Theorem 12** [checked, judge].
  - (a): DEF(G') = 0 via Lemmas 9 and 10 and Claims B and E.
  - (b): all pairs adjacent give DEF(R') >= 39 > 32.
  - (c): the fold is deficiency-free, by the E* count (p-1)/2 or (p+1)/2 < p. Hence -8 <= A(H) <= -1.
  - (d): merges with degree sum <= 3 are blocked.
  - (e): DEF(C_hub) = 0 (via C10), the unique pendant member K, and the replacement H' with A(H) >= 3.
  - (f), (g) and (h) are checked.
  - (i): the M = Q + {w,a,b} argument gives p <= 3 and n(H) <= 73.
  - (j): the case "exactly one outer vertex of degree 2" leads in both sub-cases to P(Q) < 0 or P(Q-a-b) < 0.
  - (k1) and (k2) are checked.
- **Theorem 13 (I11 form, tight outer graph)** [checked, judge]. The pair lemma at n-2 gives q <= 2. A non-adjacent pair gives a fold at n+2 with slack -1. With three adjacent pairs, q >= 3. No degree hypothesis is needed. Of the two available proofs of the tight case, this one is the shortest.
- **Corollary 14** [checked, judge].
  - 14.2 is L022 Theorem 2(v), re-proved: s(H[Z]) <= s(F_1) - 2.
  - 14.3: a tight side that is not a single edge has a b-triple, which contradicts Theorem 13, since n(F) + 2 <= n(H) - 2. Two single-edge sides would form F_7.
  - The last sentence (s(H) = -2 gives pattern (a) everywhere) uses L022 Theorem 2, which is now accepted (K72).
- **Theorem 15** [checked, judge]. Its parts (b) to (d) are superseded by L025 Theorem 10 (L026 16.6 says so).

**Marked GAP:**
- GAP A, consisting of:
  - A1 (finite, n(H) <= 73, not computed);
  - A2 (the pendant case, n(H) > 73, infinite).
- GAP B (the I11 form at s(G) = 1).

**Claimed without a GAP but not proved:** nothing load-bearing. Points:
1. **Proof steps that rest on computations.**
   - **C1:** (L1) and the weights of L*. Now covered by the K71 acceptance of L021 Theorem 7.
   - **C10:** no hub triangle in a member of L*. Used in Theorem 12(e), and through (e) in (f), (i) and (j). These are checks of 32 explicit graphs. I re-verified C10 with my own code (S1: 0 hub triangles; the triangle (6,3,2) gives 3 as a control).
   - **Cell(24,19,10,3) = ∅:** used in Theorem 12(f) and (k1). It comes from L021 Theorem 7(ii) or experiments/20261027-0300-tight-cells-d4.
   
   L026 states all three uses.
2. **DEPENDS ON is out of date.** It calls L021 "unrefereed", but L021's proved parts, including Theorems 3 and 7, were ACCEPTED as K71, and L022 Theorem 2 as K72. Editorial.
3. **The title/summary phrase "(or at most 73 vertices)".** It is accurate, but A1 is a genuinely uncomputed family. It is not a closed case.

**Finite computations it needs:**
- N1 (the family A1);
- N2 and N3 (falsifiers for the pendant case at 25 <= n <= 40);
- N4 (complete slack-1 cells at n = 27..30).

**Verdict:** correct as far as I checked. The KT-form analysis (Lemmas 9 and 10, Theorem 12) is new and solid. Its residual is the same pendant configuration as L025's, with less structure (no tight-set theorem) and one extra finite family A1. Its I11-form content is contained in L025 (Theorem 13 is part of L025 Corollary 11(a)), except for Corollary 14, which L025 lacks and which is needed (Section 4.3).

### L024 (KT reduction; only the parts that bear on the E1-hub)

L024 Proposition 5 states GAP R3 as "no minimal counterexample **satisfying (AH)** has an E1-hub with a b-configuration outer triple". By Lemma A+(alpha) this applies for every n.

This hypothesis makes L026's finite family A1 unnecessary on the L024 route (Section 4.1). I did not referee L024 itself. Its DEPENDS ON also predates K71.

## 2. Closest to complete

**L025.**
- It proves the I11 form for every configuration except the pendant triple, by hand.
- It leaves no finite residue, and its only external inputs are accepted certificates (L017; L016 only for Remark 10.3).
- It reduces the pendant case to a rigid structure: s(G'') = 8, W avoided, A, B and C disjoint, every transversal triple dropping tau by exactly 1, and a tight set S_0 ⊇ W with at least 2 crossing edges or a saturated G.

L026's KT-form residual is the same pendant configuration with less structure, plus the uncomputed family A1. A1 is removable on the L024 route (4.1).

Caveat on value. Completing the I11 form closes only pattern (b) of the I11 induction. The I11 routes L020 and L022 still need C1-big (pattern (a)), which is I11's own core (panel SYNTHESIS §0.3).

Completing the KT form would close GAP R3 of L024. With R1 and R2 this gives c* >= 35/66 (goal B). So the KT form is the more valuable target, but it is further from done.

## 3. The decisive missing step: the pendant-triple lemma (PT)

**PT, I11 form.** Let G in C be connected with Delta(G) <= 3 and s(G) = 1, and assume I11 for every member of C with at most n(G)+3 vertices. Then there are no three vertices a, b, c of degree 1, lying in three different edges, that are pairwise non-co-transversal.

**Equivalent residual form** [checked, judge: L025 Theorem 12(a)-(c) gives one direction; Lemma 7 and Lemma 1 give the other]. No connected G'' in C with Delta <= 3 and s(G'') = 8 has three pairwise disjoint 2-sets A, B, C of vertices of degree <= 2, none of them inside an edge, such that both of the following hold:
- (i) no minimum transversal of G'' meets A ∪ B ∪ C;
- (ii) no (tau''+1)-transversal of G'' meets all of A, B and C.

Here the hypothesis is I11 for fewer than n(G'')+7 vertices.

(i) and (ii) together are exactly the condition tau(G'' + gadget) = tau'' + 4. The gadget has the 7 vertices v, x, y, z, a, b, c and the 7 edges xyz, vxa, vyb, vzc, a∪A, b∪B, c∪C. Since s(gadget) = 21 + 14 - 44 = -9, the graph G'' + gadget is then a violator with slack -1. So PT is exactly "no minimal counterexample contains the 7-vertex pendant hub gadget".

**Why PT is decisive.**
- I11 side: L025 Corollary 11(b) and L026 Corollary 14 together show the following. In a minimal counterexample to I11, a degree-3 vertex has pattern (b) only if it is the centre of an E1-hub over a slack-1 outer graph whose outer triple is pendant. So PT is exactly what remains of pattern (b), and with it B1-big of the panel synthesis §4.1. B0-big is already proved (L025 Corollary 11(a), L026 Theorem 13).
- KT side: L026 Theorem 12(k2), together with Section 4.1 below, reduces L024's GAP R3 to the KT analogue PT-KT.

**PT-KT.** No minimal counterexample H to KT^{L*} with n(H) >= 25 that satisfies (AH) has a pendant E1-hub. For such an E1-hub, R = G' - {a,b,c} would satisfy:
- tau(R) = tau(G') - 2 and A(R) = A(H) + 94, which lies in [86,93];
- DEF(G') = 0 and 8 <= A(G') <= 15;
- W is avoided in R.

**What is known about the PT residual** (all [checked, judge] from L025, unless tagged otherwise):
- s(G'') = 8; G'' is connected; A, B and C are disjoint; the vertices of W have G''-degree 1 or 2.
- Every transversal triple X = {x_A, x_B, x_C} has tau(G''-X) = tau''-1 and |∂(X)| <= 5.
- No edge lies inside W.
- G'' has a tight set S_0 ⊇ W, and every edge leaving S_0 meets it in exactly one vertex.
- In the minimal counterexample, either S_0 = V(G'') (saturated, n(G) ≡ 1 mod 11, n(G) >= 34; then W consists of exactly the avoided vertices, all of degree 2) or >= 2 edges leave S_0.
- **New constraint (J1)** [derived-here, judge, unrefereed]. Let u ∈ W, say u ∈ A, so that d_{G''}(u) ∈ {1,2}.
  1. Lemma 8(a) gives s(G''-u) = 5 - 2d(u) ∈ {1,3} and tau(G''-u) = tau''.
  2. By (ii), no minimum transversal of K_u = G''-u meets both B and C: such a transversal, plus u, would be a (tau''+1)-transversal meeting A, B and C.
  3. So K_u + w(B,C) has n'' vertices and slack s(K_u) - 4 <= -1. Here w is a new vertex with the edges {w}∪B and {w}∪C; the linearity and degree conditions hold.
  4. Hence K_u + w(B,C) is not in C: either K_u has a saturated set ⊇ B ∪ C, or there is an F_7 through w.
  
  This is the L019 Theorem 3 configuration in a graph of slack 1 or 3. It is new information exactly when u has both of its G''-edges inside S_0, since then S_0 - u is not tight.

**Stored data never comes near the residual** [verified-here, judge]:
- The slack-8 lists have at most 1 avoided vertex (S3).
- Every stored near-tight graph with Delta <= 3 and <= 26 vertices has at most 2 degree-1 vertices, apart from E_1, and none has a pendant b-configuration (S2, matching L025's pendants_output).

## 4. Cross-pollination

### 4.1 L024's (AH) plus L026 Theorem 12(e)/C10 removes the finite family A1 on the L024 route [derived-here, judge, unrefereed]

Let H be a minimal counterexample to KT^{L*} satisfying (AH), with an E1-hub whose outer triple is a b-configuration, and let a be an outer vertex with d_{G'}(a) = 2.

1. Then d_H(a) = 3, and by L026 0.7, DEF(H - a) >= -A(H) >= 1.
2. By (AH) at a, the optimal family is a single component F_a of H - a, isomorphic to a member of L* and met by all three edges at a. In particular F_a meets e_a = {v,x,a}, so F_a contains v or x, i.e. F_a = C_hub.
3. But C_hub contains the hub triangle (x,y,z,v,b,c): in H - a the degrees are d(x) = 1 and d(y) = d(z) = d(v) = 2. By C10 (re-verified, S1) no member of L* has a hub triangle. Contradiction.
4. So every outer vertex has G'-degree 1.
5. Then L026 Theorem 12(k1) (an n(H) = 24 tight graph, excluded by cell(24,19,10,3) = ∅) or (k2) (pendant) applies. A1 is never reached.

Consequence: L024's GAP R3 is equivalent to PT-KT for every n >= 25, without A1.

L026's A1 is needed only for an E1-hub at a vertex where (AH) fails, i.e. inside L024's GAP R1 (G2 residue). There it is irrelevant to R3.

### 4.2 Port L025's pendant toolkit to the KT potential (the KT analogue of L025 Theorem 12, L026 N2)

The exact changes of A = 27n + 35m - 132 tau, all following from the tau statements of L025 Lemmas 4-9:

| operation | change of A |
|---|---|
| move M(a -> a_i; b,c), or identification of an NC pair | -27 |
| edge on three avoided vertices | -97 |
| two pendant pairs with tau + 2 | -140 |
| three pendant pairs with tau + 3 | -210 |
| triple deletion with tau - 2 | +94 |

In the KT pendant case, A(G') = A(H) + 16 <= 15.

- A move M in C_3 that is connected has A(M) <= -12, while DEF(M) <= 10 by L026 Lemma 3 (n >= 11). That is a contradiction. So, exactly as in L025 11.4 and 11.8, a connected move forces a saturated set ⊇ {a_i} ∪ B ∪ C in R.
- Pendant pairs on a connected R give A <= A(H) - 46, while DEF <= 16. So the KT analogues of L025 Theorem 12(g) and (h) hold whenever the graphs involved are connected.

The one genuinely new ingredient is the disconnected case, where DEF adds over components. It is controlled by L026 Lemma 10 and Claim E, which bound the number of positive-deficiency components by the number of boundary edges. Expected outcome: the KT pendant case acquires the same tight-set structure (S_0 ⊇ W in R) as L025 Theorem 12(j). PT and PT-KT then become one combinatorial question about saturated sets.

### 4.3 L026 Corollary 14 completes L025 Corollary 11(b)

- L025 starts from an E1-hub.
- L026 Corollary 14 (checked; its last sentence now rests on accepted L022 Theorem 2) shows that pattern (b) at any degree-3 vertex of an I11 minimal counterexample is an E1-hub with s(H) = -1 and a slack-1 outer side.

Together they give the **Pattern-(b) theorem**. In a minimal counterexample H to I11, a degree-3 vertex with pattern (b) exists only if s(H) = -1 and H = G' (+) (a,b,c), where:
- G' is connected with s(G') = 1;
- {a,b,c} is a pendant b-configuration of G';
- the structure of L025 Theorem 12 and Lemma 13 holds.

So PT is equivalent to "pattern (b) never occurs". Neither certificate states this combined result. It should be written once and refereed (step 1 below).

### 4.4 Independent rediscoveries (mutual confirmation)

- L025 Lemma 4 = L026 Lemma 11 (merge/identification).
- L025 Corollary 11(a) and Remark 10.4 contain L026 Theorem 13. L026's proof is three lines, so use it in the combined certificate.
- L025 Lemma 13 = L026 Remark 7.3.
- L026 Theorem 15(b)-(d) is superseded by L025 Theorem 10.

### 4.5 Nothing from L026's KT-specific lemmas transfers back to the I11 form

The I11 residual has slack 8, not a deficiency. L026's Lemma 9 (positive DEF means a p-piece tree) has no slack analogue that would bound the size of G''.

## 5. Recommended next steps (in order)

### 1. [prover, about 2 h; then two referees in parallel, about 1.5 h] Certificate "Pattern (b) in I11 minimal counterexamples"

Content:
- L025 Lemmas 1-9, Theorem 10, Corollary 11, Theorem 12 and Lemma 13, with the tight-set definition fixed to |S| >= 3 in Lemma 4;
- L026 Theorem 13 (short proof of the tight case) and Corollary 14;
- the combined Pattern-(b) theorem of 4.3, the residual form of PT (Section 3), and constraint J1 (Section 3).

Every step must be hand-proved. Remark 10.3 is to be tagged as computational. This makes the reduction citable. Acceptance: two referee ACCEPTs.

### 2. [worker, about 2-3 h wall, one process, nice] Falsifier for PT at 24 <= n(G'') <= 40

Generators:
- (a) Saturated G'' (m = n - 2) with Delta <= 3. The degree sequence is forced: exactly six vertices of degree 2, the rest of degree 3. Take n(G'') ≡ 9 (mod 11), i.e. n(G'') = 31, 42. Use edge-by-edge linear growth inside class C, keeping (P3) exact.
- (b) G'' = M ∪ R'' with M saturated containing W, and k >= 2 crossing edges, each with one vertex in M.
- (c) The growth and beam generators of experiments/falsify/i11-n28-40, retargeted to graphs with s <= 8 and many avoided vertices of degree <= 2.

Test for each graph:
- compute all minimum transversals and the avoided set U;
- for each triple of disjoint non-edge pairs in U, test (ii) via tau(G''-X) >= tau''-1 for the 8 transversal triples X. This is how checks.py S3 does it; reuse it.

Report:
- the maximum number of avoided vertices of degree <= 2 as a function of slack (a new statistic; at slack 8 the stored data give <= 1);
- the minimum s(G'') over configurations satisfying (i) and (ii). PT predicts >= 9.

A hit with s(G'') <= 8 is an I11 counterexample, G'' + gadget with n(G'') + 7 vertices. It must be re-verified by brute-force tau and membership in C.

### 3. [prover, about 3 h, in parallel with 2] Attack PT through S_0

Two sub-lemmas to try, each to be falsified first (step 2 data):

- **(R1a) Saturated case.** If G'' is saturated with s(G'') = 8, the six degree-2 vertices W are exactly the avoided vertices, and every transversal triple of W contains an adjacent pair, then contradict I11 below n(G'')+7.
  - Suggested tools:
    - J1 at each u ∈ W (both of u's edges lie in S_0 = V(G''), so J1 gives a new saturated set ⊇ B ∪ C in G'' - u, or an F_7);
    - the folds of L019 Theorem 5 at the degree-2 vertices x, y, z, a, b, c of H (each fold of H that lies in C is a tight graph with n(H) - 2 vertices; L019 Theorem 5(e), s(H) = -1);
    - the counting 2n_1 + n_2 = 6.
- **(R1b) Restriction lemma.** Let S_0 be a proper subset of V(G''), M = G''[S_0], and let f_1, ..., f_k (k >= 2) be the crossing edges, |f_i ∩ S_0| = 1. Show that either H[S_0 ∪ gadget] is a smaller violator (i.e. (i) and (ii) hold in M and s(M) <= 8), or replacing R'' together with the crossing edges by k pendant edges at the attachment vertices gives a smaller violator.
  - Tool: L017 Theorem 2(R+) and the Hall lemma (H) with W_1 = S_0 ∪ gadget and W_2, ... the components of R''.
  - Lemma 13 is exactly the case k = 1. A "saturated block lemma" for k >= 2 is the natural general statement.

### 4. [prover, about 2 h, after 1] KT analogue of L025 Theorem 12 (Section 4.2)

Goal: in the KT pendant case, R is connected (or its components are controlled by Lemma 10), A, B and C are disjoint, the moves are blocked, and a saturated set S_0 ⊇ W exists in R. This turns PT-KT into the same saturated-set question as PT. Write the result as an addendum to L026, with 4.1 included and every step marked GAP where unproved.

### 5. [worker, about 30 min] Re-certify cell(24,19,10,3) = ∅

This is the input that L026 Theorem 12(f)/(k1) and 4.1 need. Use either the stored L021 Theorem 7 lists (accepted, K71) or an independent rerun of experiments/20261027-0300-tight-cells-d4. Record which accepted certificate covers it.

### 6. [worker, background, low priority] P2+ beyond 26 vertices

Conjecture P2+: a connected slack-1 member of C with Delta <= 3 has at most two degree-1 vertices.
- Run the complete slack-1 cells at n = 27..30 with Delta <= 3: (27,15,10), (28,19,11), (29,23,12), (30,27,13). These are L026 N4.
- Count degree-1 vertices and pendant b-configurations.
- P2+ implies PT. So a P2+ violation is not a PT violation, but it is the place to look.

**Do not pursue:**
- computing L026's family A1 (N1) for the L024 route, since 4.1 makes it unnecessary;
- further I11-form gadget variants that add edges inside S_0 (L025 "Why the gadgets stop here": all are blocked by the single tight set).

## Appendix: checks performed by the judge

All checks were run from experiments/prover/e1hub-synthesis/checks/ (own code hyp.py and checks.py), one process each, under `timeout` and `nice -n 10`.

- **S1 (C10 re-check).** `timeout 300 nice -n 10 python3 checks.py S1 ../../../prover/L021/closure_results.json` produced S1_output.txt:
  ```
  TOTAL hub triangles in 32 pieces: 0
  control triangle (6,3,2): 3 hub triangles (expect 3)
  ```
  The output has one line per piece; all 32 show 0.
- **S2 (degree-1 census, P2+ evidence; pendant b-configurations).** From experiments/prover/L017/out, `python3 .../checks.py S2` was run on the ten near-tight lists with Delta <= 3: L012 cells (3,1,1), (8,5,3), (10,7,4), (12,10,5), (14,12,6), (15,11,6), (17,13,7), (19,16,8), (22,17,9), and L016 runB2 (26,22,11). It produced S2_output.txt.
  - Degree-1 histograms: (8,5,3) {1:1, 2:1}; (12,10,5) {0:112, 1:37}; (15,11,6) {0:9, 1:8, 2:2}; (19,16,8) {0:221, 1:6}; (22,17,9) {0:18, 1:19}; (26,22,11) {0:36}; the tight cells (10,7,4) {0:2, 1:2}, (14,12,6) {0:2}, (17,13,7) {0:6}; and E_1 {3:1}.
  - Pendant b-configurations: 0 everywhere.
  - This is identical to L025's pendants_output.txt.
- **S3 (the PT residual on stored slack-8 lists).** From experiments/prover/L017/out, `timeout 1200 nice -n 10 python3 .../checks.py S3` was run on L014 (5,2,1,D3) and on (9,7,3), (12,8,4), (15,9,5), (18,10,6), (21,11,7) (L013, D2) and (24,12,8) (L016 runA, D2). It produced S3_output.txt.
  - There are 0 candidate triples (A,B,C) and 0 hits.
  - Diagnostic (inline run): the avoided-vertex histograms are (12,8,4) {0:5}, (15,9,5) {0:84, 1:7}, (18,10,6) {0:64, 1:3}, (21,11,7) {0:36} and (24,12,8) {0:14}.
  - The (9,7,3,D2) list is empty (the engine found 0 classes).
- **Hand checks.** I verified line by line every step listed under "Proved" in Section 1. Sections 3 (J1) and 4.1 are my own derivations and have not been refereed.
