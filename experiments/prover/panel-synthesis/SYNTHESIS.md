# Panel synthesis: three attempts at I11 (L020, L021, L022)

Judge: referee agent (opus), 2026-10-27, 07:04 to 07:45 UTC. Scope: results/proofs/L020-joint-induction-i11.md (the file exists; submitted 06:13 UTC), results/proofs/L021-i11-deficiency-route.md (07:00 UTC) and results/proofs/L022-i11-realizable-route.md (06:36 UTC). I read all three in full, plus L017 (Theorems 1 to 7 and Section 13), the parts of L018 they cite (Lemma 0.5, Remarks 5.4 and 7.3), kb/notes/i11_conjecture.md, kb/methods/i11_proof_plan.md and kb/notes/hy_proof_technique.md. I did not edit any certificate. My scratch code is in experiments/prover/panel-synthesis/checks/; it does not import e757, the judge or any L0xx code.

Tags used here:
- [verified-here, judge]: re-computed by my own code (Appendix).
- [checked, judge]: hand proof read line by line and found correct.
- [derived-here, judge, unrefereed]: a new argument written in this synthesis. A prover must formalize it and a referee must check it before anyone relies on it.

## 0. Bottom line

1. None of the three attempts proves I11 or any bound beyond 9/17, and none claims to. Every hand-proved step I checked is correct. I found no load-bearing statement that is claimed without a GAP but is unproved. The defects are editorial: one sign typo in L021, outdated status lines, and one summary-level overstatement (Section 1).
2. **All three routes leave the same residual configuration, the E1-hub.** It consists of a vertex v with edges {v,x,a}, {v,y,b}, {v,z,c} and an edge {x,y,z}, where d(x) = d(y) = d(z) = 2 and no minimum transversal of G' = H - {v,x,y,z} contains two of a, b, c. Call {a,b,c} a *b-configuration* of G'. Where it appears in each route:
   - In I11 language it is pattern (b) with one side a single edge. It is the whole of pattern (b) under P2' in L022 Corollary 3, and the b-half of R-big in L020 Corollary 5.
   - In L021's language it is what a minimal counterexample to KT reduces to at a minimal apex, if G2 is closed and n >= 67 (Lemma A in Section 3; my derivation, unrefereed).
3. **L020 and L022 also need C1-big (pattern (a): H - v connected).** This is not a lemma separate from I11. L020 Remark 4.6 shows that C1-big at size N is equivalent to the pattern-(a) case of I11 at size N+1. Neither route has any inductive handle on it.
4. **L021's potential removes pattern (a) by design** (my observation, Section 1). In a minimal counterexample to KT, if H - v is connected for some degree-3 vertex v, then H - v is three special pieces joined by one edge, so n <= 52. That is the structural reason L021 is ranked first.
   - Price 1: the target is weaker. L021 aims at J_{1/6}, i.e. 11 tau <= (19/6) n + 2 m, which gives c* >= 35/66. That still beats 9/17 (goal B).
   - Price 2: its key conjecture KT* is new. It is verified only for n <= 24, is not implied by I11, and is knife-edge (296 equality cases).

## 1. Verdict per attempt

### L020: joint induction with T'' (refutation plus a corrected conditional reduction)

**Proved, and checked by me:**
- **Theorem 1 (Conjecture T'' is false)** [verified-here, judge, for the displayed graph K_29]. My own code gives:
  - basic data: n = 29, m = 23, connected, degree sequence 2^18 3^11;
  - membership in C: linear; F7-free (exhaustive over all 3-sets of edges at every vertex); (P3) by a per-pair distinct-representatives test;
  - transversal number: tau = 12 exactly (branch and bound), so slack = 87 + 46 - 132 = 1.
  
  So one connected member of C with Delta <= 3, slack 1 and 29 vertices exists, and T'' (bound 26) is refuted. I also re-ran the claim of Theorem 1(ii) for K_29:
  - all 19,502 minimum transversals (inside L020's range 18,283 to 20,912);
  - 337 pairs not inside an edge;
  - 4,078,620 triples of pairwise disjoint such pairs;
  - exactly 6 triples are uncovered, and none of them is admissible (K + v is not in C).
  
  This matches L020's C5. I did not re-check the other 44 classes, part (iii), or Observation 7.
- **Theorem 2** [checked, judge]. The case table of Lemma 2.1 (t_i >= 0, using Tutte-Berge) is correct, and so is the identity s = 3 n_0 + 11 nu(G*) - 3 n_2. So 7s >= 21 n_0 + n_2, and a connected graph has s >= (m-1)/7. In substance this is Chvatal-Hanson and L018 Theorem 2.
- **Theorem 3** (a degree-3 vertex of a near-tight graph) [checked, judge]: Steps 3.1 to 3.8, i.e. free choice, pair richness with slack budget <= 3, the Hall argument that gives r <= 2 when Y is empty, and the equivalences for (b), (e), (f), (i1) to (i3).
- **Proposition 6** [checked, judge].
- **Theorem 4 and Corollary 5** [checked, judge] as conditional statements. They rest on L017 Theorem 4 (accepted) and on the unrefereed role table C5 of L017 (tagged as such).

**Marked GAP or open:** no GAP inside the proofs. The hypotheses FC1, C1-big and R-big of Corollary 5 are open, and the certificate says so.

**Claimed without a GAP but not proved:** nothing load-bearing.
- (i) DEPENDS ON describes L017 as "round 2 pending" and L018 as partly accepted. Both are now accepted. Editorial.
- (ii) Remark 4.6 should be read as the main limitation, not a side remark. Corollary 5 reduces I11 to C1-big, which is the pattern-(a) part of I11 itself. So Corollary 5 is not a reduction to anything easier.
- (iii) Part of R-big is superseded. Its e-configuration clause is unnecessary: L022 Theorem 2(ii) shows that pattern (e) never occurs in a linear vertex-critical violator. In pattern (f), L022 Theorem 2(iii) gives s(F_1) = 1, s(F_2) = 0 and s(H) = -1.

**Finite computations it would need:**
- W1: FC1, i.e. cell(25,23,11,3) is empty.
- W2: the complete lists of cell(29,23,12,3) and cell(29,17,11,3), each class run through the triple test. This gives I11 at 30 vertices, and it tests the Theta-chain bound 29 of Observation 7.
- W3: cell(28,24,12,3).

None of these closes I11.

**Verdict:** correct. Its value is the refutation of T'' (now independently re-verified), the degree-3 lemma for near-tight graphs, and the Theta-chain data. As a route to I11 it is a dead end: by Remark 4.6 the joint induction cannot close, and the remaining hypotheses are global.

### L021: Henning-Yeo deficiency route (KT, epsilon = 1/6)

**Proved, and checked by me:**
- **Theorem 1** [checked, judge].
  - (a) A minimal violator of J_eps with a vertex of degree >= 4 satisfies J_eps, because 8 - eps - 2d <= -eps.
  - (b) If eps < 3/17 then c* >= (6 - eps)/11 > 9/17. For eps = 1/6 this is 35/66, since 35 * 17 = 595 > 594 = 9 * 66.
- **Definition 2** [checked, judge].
  - The identity A = 27n + 35m - 132 tau = 12(s + n/6 - 11(n-m)/12) holds.
  - The weights are correct: W(E_1) = 16, W(8,5,3) = 5, W(10,7,4) = 13, W(15,11,6) = 2, W(17,13,7) = 10, and A(14,12,6) = +6.
  - The free hub is exact: 27 + 3 * 35 = 132.
- **Theorem 2** [checked, judge]: DEF(H) <= 11(n - m) on C, using n(R) >= m(R). Hence KT implies J_{1/6} on C_3, and by Theorem 1 on C.
- **Theorem 3, Claims A, B, C, E, F** [checked, judge]. This includes the Hall step 3.4, i.e. the exchange giving E*(X') ⊆ E*(X*) \ S.
- **Theorem 4** [checked, judge].
  - (a) The bound (4.1), DEF(H - v) <= max(0, 35d - 54), gives A(H) >= 62 > 0 if tau does not drop, so every vertex is co-transversal.
  - (b) The case split is correct: j >= 4 is impossible since it needs 19j <= 69, and the cases (D1), (D2), (D3) follow.
- **Theorem 5** [checked, judge].
- **Theorem 6** (KT for Delta <= 2) [checked, judge]:
  - the dual-graph formula A = 132 nu - 16N - 27M;
  - the theta table of 6.3;
  - the identification of the K4^s component with (8,5,3)#0 = {012, 156, 247, 346, 357};
  - disjointness of the family and E*(X) ⊆ U.
- **Proposition 8** (Claim H, conditional) [checked, judge]: Steps 8.1 to 8.4, including the bound 19|X| - 16 - 27 nu and, for (H_0), 19|X| - 97.
- **Proposition 9** [checked, judge]: these cases are killed by small I11 violators via L016.

**Marked GAP:**
- G1: impure (D1), (D2), (D3) configurations.
- G2: the exceptions to Claim H.
- G3: degree-2 vertices.
- G4: this is KT* itself, a restatement.

**Claimed without a GAP but not proved:** nothing load-bearing.
- (i) Sign typo in the Sanity checks. For hypertrees with a perfect matching (n = 6k+3, m = 3k+1, tau = 2k+1), A = 3k - 16, not "16 - 3k". DEF = 16 - 3k and P = 0 are correct.
- (ii) The prover summary says "the special family is 32 pieces with at most 17 vertices". This is established only among connected members of C_3 with at most 24 vertices; Theorem 7(i) states it correctly. Several special candidate cells are not computed:
  - (25,14,9): only a D = 2 list exists;
  - (26,13,9) and (26,17,10): no list;
  - all four candidates at n = 27: no list (experiments/prover/L021/scan_cells_output.txt).
- (iii) KT* is not a consequence of I11, and the certificate should say so. KT constrains the sparse region m < 9n/11 at any I11 slack. For example, the candidate cells (21,10,7) with s = 6 and (27,13,9) with s = 8 have A < 0. So the only evidence for KT* is Theorem 7 (n <= 24). The certificate's own random assemblies never reached A < 0, so no falsifier has tested n >= 25.

**My additions** [derived-here, judge, unrefereed]:
- (a) **Pattern (a) is finite under KT.** Let v have degree 3 in a minimal counterexample. In (D1) and (D2) the members are components of H - v, and H - v = F would give n <= 18 < 25. In (D3) exactly one edge g of H - v leaves the three members. If H - v is connected, g must meet all three members, so H - v is the union of F_1, F_2, F_3 and g, and n <= 3 * 17 + 1 + 1 = 53. So, except for this finite family, H - v is disconnected at every degree-3 vertex.
- (b) **G2 is narrower than stated.** Let R = H - V(X), and let p, q in ∂(X) share no edge of R. Then the replacement e' = {p, q, z}, with z a new vertex, always stays in C_3:
  - F7 has minimum degree 2, so z lies in no copy of F7;
  - (P3): e_{H'}(S) = e_R(S - z) + 1 <= |S| - 2 whenever S contains z, p, q;
  - degrees: p and q each lose at least one E*-edge.
  
  The arithmetic of 8.2 with nu = 1, together with DEF(H') <= 16 from 8.3, gives A(H) >= 19|X| - 43 > 0 when |X| >= 3. So for |X| >= 3 and |∂(X)| >= 2, the only exception left in G2 is that every two vertices of ∂(X) share an edge of R; the clause "replacement outside C_3" is otherwise vacuous. The cases |X| <= 2, |∂(X)| = 1 with |X| <= 3, and ∂(X) = ∅ with |X| <= 5 remain.
- (c) Lemma A (Section 3) reduces G1 to the E1-hub, given G2.

**Finite computations it would need:**
- KT on the uncomputed special cells at n = 25 to 27;
- a KT falsifier at 25 <= n <= 40 (Section 5, step 1);
- (H_0): assemblies of at most 5 pieces of L* joined by |X| + 1 edges (at most 85 vertices);
- the finite (D3) family in (a) (at most 53 vertices).

**Verdict:** a correct and well-built framework. The remaining gaps concern configurations of bounded size around a degree-3 vertex, but they are substantial, and KT* is untested beyond 24 vertices.

### L022: the realizable class R and the sub-extension lemma

**Proved, and checked by me:**
- **Theorem 1** [checked, judge].
  - (b) The maximum-principle proof of independence works: take the maximal |y_e| with the largest right endpoint and follow the chain e -> e^+ with mu(e^+) = c(e). It is elegant, and it uses only injective midpoints and the order. Hence rank = m.
  - (b'): saturated (4,5)-sets are affinely rigid.
  - (c): edge deletion. Generic rational points of V' avoid every coincidence form except the l_f with f in E \ D, and by (b) no l_e with e in D vanishes on V'. So R is closed under sub-hypergraphs.
  - (a), (d) and (f) are routine.
  - The clause "every linear member of M_R has >= 5 edges" in (e) rests on K33 plus a sketched hypertree argument. It is not load-bearing.
- **Theorem 2** [checked, judge], valid for every linear vertex-critical violator and hence in C:
  - (i): this is L018 6(b').
  - (ii) Pattern (e) never occurs. H[V(F_1) ∪ {v,f}] has tau >= tau(F_1) + 1, so its slack is <= s(F_1) - 1; this forces s(F_1) >= 1 and symmetrically s(F_2) >= 1, contradicting s(F_1) + s(F_2) <= 1.
  - (iii) In pattern (f): s(F_1) = 1, s(F_2) = 0, s(H) = -1.
  - (iv) In pattern (f), F_2 is a single edge or has two non-adjacent pendants d, f. The case analysis u in {z, d, f} is correct.
  - (v), (vi) and (vii) hold.
- **Corollary 3, and Corollary 3' for n <= 30** [checked, judge] given the unrefereed role table. The bound "at most one pendant" for tight (25,23,11) graphs with Delta <= 3 needs L018 Lemma 0.5 and the count 2 n_1 + n_2 = 6 (L018 Remark 7.3); I re-did the count.
- **Theorem 4** (O1 to O7) [checked, judge]: elementary.
- **Theorem 5, Q10** [verified-here, judge]. Q10 = {012, 034, 157, 268, 379, 489, 569} is tight with degree sequence 2^9 3^1. No injective midpoint labelling makes it a sub-hypergraph of the AP hypergraph of a (4,5)-set. Every 6-edge subset is realizable. Checked with my own exact RREF code, testing difference forms, parallelogram forms, and linearity of the forced APs.

**Marked GAP:**
- GAP 1: C1-big, i.e. pattern (a).
- GAP 2: pattern (b), which needs P2' and B1-big.
- GAP 3: pattern (f), which needs P2' and F1-big.
- GAP 4: FC1.

**Claimed without a GAP but not proved:** nothing load-bearing. The DEPENDS ON statuses are outdated (L017 and L018 are now accepted), and the "at least 5 edges" sketch noted above.

**Finite computations it would need:** N2 to N4'. None is decisive.

**Verdict:** the most rigorous certificate of the panel. Theorem 2 is the best new hand-proved content and holds in C. W1 to W7 show convincingly that realizability and the order structure do not interact with the transversal conditions, so the R route is no closer to I11 than the C route.

## 2. Ranking (by distance to a complete proof of a bound beating 9/17)

1. **L021 (closest).** It is the only route whose completion gives goal (B), and it has no global gap of the C1-big type: pattern (a) is finite under KT (addition (a) above). What it still needs:
   - the falsification of KT* at n >= 25 has to come out negative;
   - G2, narrowed by addition (b);
   - G1, which reduces to the E1-hub plus a bounded range 25 <= n <= 66 once G2 is closed (Lemma A, Section 3).
   
   Caveats:
   - it proves J_{1/6} (c* >= 35/66), not I11 (6/11);
   - KT* is a new conjecture, not implied by I11 and knife-edge (all 296 reducible special graphs up to 24 vertices are equality cases);
   - Henning-Yeo needed long case analyses (Claims H.1 to H.5) at exactly this point.
2. **L022.** It gives the sharpest unconditional reduction of I11: for every n, and in C as well as R, the seven patterns become (a), (b), (f), with strong side conditions. But GAPs 1 to 3 are global statements about all large near-tight graphs, and GAP 1 is I11's own pattern (a).
3. **L020.** Mostly negative: T'' is false and the joint induction cannot close. Its conditional reduction is weaker than L020 and L022 combined (Section 4).

If the criterion is read literally as "distance to a proof of I11 itself": L022 comes before L020, and L021 does not target I11, since even a completed L021 proves only J_{1/6}.

## 3. Decisive missing lemma

**The E1-hub (b-configuration) lemma.** This is the one configuration that every route must exclude. Notation: G ⊕ (a,b,c) is G plus new vertices v, x, y, z and the edges {x,y,z}, {v,x,a}, {v,y,b}, {v,z,c}. Then tau(G ⊕ (a,b,c)) equals tau(G) + 1 if some minimum transversal of G contains two of a, b, c, and tau(G) + 2 otherwise. So the I11 slack changes by +9 or by -2.

- **I11 form** (needed by L020 as R-big for b-configurations, and by L022 as GAP 2 under P2'). Let G in C be connected with Delta(G) <= 3, s(G) <= 1 and n(G) >= 27, and assume I11 for all members of C with fewer than n(G) + 4 vertices. If a, b, c are vertices of G-degree <= 2 with {a,b,c} not an edge of G and G ⊕ (a,b,c) in C, then some minimum transversal of G contains two of them. Equivalently, G ⊕ (a,b,c) satisfies I11.
  - Data: role_b is non-zero only for E_1 among all 482 stored slack <= 1 graphs with Delta <= 3 and at most 26 vertices (L017 C5, L020 C3).
  - Data: the 36 classes of (26,22,11,3) and the 45 known (29,23,12) classes have no NC pair at all.
- **KT form** (needed by L021 for G1). Let H be a minimal counterexample to KT^{L*}. Then H contains no E1-hub with d(x) = d(y) = d(z) = 2 whose outer triple {a,b,c} has no two members in a common minimum transversal of G' = H - {v,x,y,z}. In such a hub tau(H) = tau(G') + 2 and A(G') = A(H) + 16 <= 15.

**Lemma A (minimal apex)** [derived-here, judge, unrefereed; this is what makes the KT form the decisive case for L021]. Let H be a minimal counterexample to KT^{L*} in which every degree-3 vertex v is a (D1) apex with k_v = 3. Proposition 8 gives exactly this when the exceptions of G2 do not occur. Choose v and a special component F_v of H - v with |V(F_v)| minimum.
- (a) Every vertex w of F_v with d_H(w) = 3 has v in F_w.

  *Proof.* The components of H - w that avoid v are of two kinds. (i) Subsets of F_v - w: these contradict the minimality of |F_v|. (ii) Components D of H - v other than F_v that attach to v only through the edge at v containing w: then the family X = {D} has E*(X) = {that edge}, contradicting Claim E.
- (b) If n >= 67, the minimal apex is an E1-hub. That is, F_v = E_1 = {x,y,z}, the edges at v are {v,x,a}, {v,y,b}, {v,z,c}, d_H(x) = d_H(y) = d_H(z) = 2, and no minimum transversal of G' = H - {v,x,y,z} contains two of a, b, c.

  *Proof.*
  1. H - v - V(F_v) has at most 3 components, one per outer co-vertex. Since n >= 67, at least one component D has >= 17 vertices.
  2. By (a), D can attach to v by only one edge e_D, and every degree-3 vertex of F_v lies in e_D. So Delta(F_v) <= 2, and F_v is E_1 or (8,5,3)#0.
  3. Three disjoint traces exclude (8,5,3)#0, since its only vertex of degree 1 is 0. So F_v = E_1.
  4. If some minimum transversal of G' contained two of a, b, c, then tau(H) <= tau(G') + 1. This gives A(H) >= A(G') + 116 and DEF(H) >= DEF(G') - 105, hence P(H) >= P(G') + 11 > 0, a contradiction.

So, given G2, KT* for n >= 67 reduces to the KT form of the E1-hub lemma. The range 25 <= n <= 66 is bounded, but far too large to enumerate, and needs a structural argument.

**Why this lemma is not sufficient for L020 and L022.** Those routes also need C1-big (pattern (a)), and by L020 Remark 4.6 that is the core case of I11 itself. Only L021's change of potential removes pattern (a). A note on difficulty: in the KT form G' may have large I11 slack, because A(G') <= 15 permits slack of order 0.1 n in sparse graphs. So the KT form may be harder to prove than the I11 form, which assumes s(G) <= 1. The E1-hub mechanism is also exactly how the known special pieces arise: (10,7,4) is the triangle (6,3,2) ⊕ its b-configuration {2,4,6}, and (17,13,7) arises the same way from (13,9,5). So it is also the most likely source of a counterexample to KT*. Hence step 1 below.

## 4. Cross-pollination

1. **L022 Theorem 2 into L020 Theorem 4** gives the sharpest I11 reduction available. The inputs are L017 Theorem 4, L022 Theorem 2 and the unrefereed C5 role table. The result: I11 holds on C if FC1, C1-big, B1-big, B0-big and F1-big all hold, where
   - B1-big: no slack-1 near-tight graph with >= 27 vertices has a b-configuration;
   - B0-big: no tight graph with Delta <= 3 and >= 27 vertices has a b-configuration; this follows from P2'-big via L022 2(vi);
   - F1-big: no slack-1 near-tight graph with >= 27 vertices has (P; c, e) with all four cross pairs non-co-transversal.
   
   The last three would all follow from one statement, NC0: near-tight graphs with >= 27 vertices have no non-co-transversal pair of degree-<=2 vertices. But NC0 is thinly supported: all 37 (22,17,9) classes do have NC pairs (L020 Observation 7), so its evidence is the 36 classes at n = 26 and the 45 at n = 29.
2. **L021's potential into L020 and L022.** It is the only known way around C1-big: pattern (a) becomes finite (Section 1, L021 addition (a)). The price is the weaker target J_{1/6}, plus G1 and G2.
3. **L022's sub-extension identity (Step 2.0, using L016's I11 for <= 27 vertices) into L021 G1.** L021 Proposition 9 is one instance. The general rule kills any (D1) or (D2) configuration in which H[V(F) ∪ {v} ∪ Q] has at most 27 vertices and s_F + 3(|Q| + 1) + 2(k + k') - 11t < 0. That covers every piece of L* with |Q| <= 9. A worker can enumerate all trace and outer-vertex patterns of the 32 pieces with this test, a finite and fast job, to shrink G1 before any proof is written.
4. **L020 Proposition 6 into L022 GAPs 2 and 3 and into NC0.** An NC pair of type (2,2,1) in a near-tight K splits K - x - y into at most 5 tight graphs with Delta <= 3. Under T' this gives n(K) <= 87 for that type, so NC0 for (2,2,1)-pairs follows from T' plus a finite check. The other types leave remainders of slack 0 to 3.
5. **Lemma A connects L021's G1 to L022 Corollary 3's residual pattern (b) with an E1 side.** These are the same configuration seen through two potentials.
6. **Realizability (L022 W1 to W7) gives nothing** for the transversal conditions. Q10 is forbidden only in R and only at pattern-(a) attachments. The order facts K30 and K31 kill single labellings, never a whole pattern. Do not invest further in the R route as a way to I11.
7. **L020 Observation 7 (Theta-chains)** is the best evidence for the B and NC statements. Every stored near-tight graph with 15 to 26 vertices, and every one of the 45 (29,23,12) classes, is Theta(X) of a smaller near-tight graph, and the chains stop because NC pairs are used up. So an induction along Theta, tracking NC pairs, is a plausible attack on NC0 [conjecture].

## 5. Recommended next steps (ordered)

1. **[worker, about 3 h wall, one process]** Targeted falsifier for KT* via the E1-hub mechanism. This decides whether L021 deserves a prover. Spec:
   - Inputs: all stored connected class lists with Delta <= 3. These are experiments/20261027-0300-transversal-richness/inputs/, the extracted tarballs in experiments/prover/L017/out/ (L012 to L016), and the unrefereed n = 27, 28 lists in experiments/20261027-0340-induction-n28-n29-f25/out/cells.
   - Main pass: for every class G' with A(G') <= 15, at any slack:
     - enumerate all minimum transversals;
     - list every triple {a,b,c} of vertices of G'-degree <= 2, not an edge, with no two in a common minimum transversal;
     - build H = G' ⊕ (a,b,c), keep it if H is in C_3, and assert tau(H) = tau(G') + 2;
     - compute A(H), DEF(H) and DEF^proper(H) with experiments/prover/L021/kt.py;
     - report any H with A + DEF < 0 (a counterexample to KT^{L*}), and any H not in L* with A + DEF^proper < 0 (a new irreducible special piece).
   - Extra cases: repeat with G' a disjoint union of 2 or 3 stored classes, where each of a, b, c then lies in no minimum transversal of its own component. Iterate once on every new H with A(H) <= 15.
   - Second pass: run the growth and beam generators of experiments/falsify/i11-n28-40 at 25 <= n <= 40 with objective "minimise A + DEF", Delta <= 3.
   - Acceptance: every hit is re-verified by a brute-force tau and a brute-force DEF (in the style of L021 validate_def.py). Write a REPORT.md with counts per input cell.
2. **[worker, background]** KT for n <= 27. Compute the missing special cells (25,14,9,3), (26,13,9,3), (26,17,10,3), (27,13,9,3), (27,15,10,3), (27,16,10,3) and (27,20,11,3) with the L012 engine, re-using lists that exist, then run L021 closure.py on them. This extends Theorem 7(ii) from n <= 24 to n <= 27.
3. **[worker, about 1 h]** The finite G1 shrink from Section 4 item 3. For each of the 32 pieces and every (D1) or (D2) trace pattern with at most 9 outer vertices, test the sub-extension inequality with L016's I11. List the patterns that survive.
4. **[prover, about 2.5 h, then a referee for about 1.5 h]**, only if steps 1 and 2 find no counterexample. Write certificate "KT reduction":
   - (i) Lemma A, exactly as stated in Section 3;
   - (ii) the pendant-replacement strengthening of Proposition 8 (L021 addition (b));
   - (iii) the finite (D3) family for pattern (a);
   - (iv) a precise list of what remains: the G2 residue (|X| <= 2; boundaries that are cliques in R; |∂(X)| = 1 with |X| <= 3; ∂(X) = ∅ with |X| <= 5), the range 25 <= n <= 66, and the E1-hub lemma in KT form.
   
   Every unproved step marked GAP.
5. **[two referees in parallel, about 1.5 h each]** Referee the reusable hand-proved content so it can be cited: L022 Theorems 1 and 2 with Corollaries 3 and 3', and L021 Theorems 1 to 6 with Propositions 8 and 9. Also ask L021 to fix the sign typo and to add the sentence "KT* is not implied by I11".
6. **[prover, about 3 h, after step 4]** Attack the E1-hub lemma. Start with the I11 form, using Proposition 6 (each NC pair has |∂| <= 3, and G - a - b has slack s + 5 - 2|∂| in [0, 3]) together with the Theta-chain structure. Then transfer to the KT form.
7. **[worker, background, only if CPU is free; tens of core-hours]** L020 W1 and W2: cell(25,23,11,3); cell(29,23,12,3) and cell(29,17,11,3) with the triple test. This gives I11 at n <= 30 and tests the Theta-chain bound 29. Useful for f(25), f(29), f(30), but it does not advance a general proof.

**Do not pursue:** the joint induction with T'' (refuted, and it cannot close by L020 Remark 4.6), and the realizable class as a route to I11 (L022 W1 to W7).

## Appendix: checks performed by the judge

All checks were run from experiments/prover/panel-synthesis/checks/ with `nice -n 10`, one process each, under `timeout`.

- `timeout 600 nice -n 10 python3 check_k29.py` produced check_k29_output.txt:
  ```
  n 29 m 23 maxdeg 3 mindeg 2 connected True deg2 18 deg3 11
  linear True
  F7-free True
  P3 True
  tau 12 slack 1
  ```
- `timeout 1500 nice -n 10 python3 check_k29.py --triples` produced check_k29_triples_output.txt:
  ```
  min transversals 19502
  pairs not inside an edge 337
  triples checked 4078620 uncovered 6 uncovered and admissible 0
  ```
- `timeout 900 nice -n 10 python3 check_q10.py` produced check_q10_output.txt:
  ```
  degrees [2,2,2,2,2,2,2,2,2,3] tau 4 slack 0
  Q10 realizable as sub-hypergraph of a (4,5)-set: False
  all 6-edge subsets realizable: True
  ```
- Hand checks: every step listed under "Proved" in Section 1 was verified line by line. Lemma A and L021 additions (a) and (b) are my own derivations and have not been refereed.
