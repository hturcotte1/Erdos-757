VERDICT: NEEDS-WORK

Referee: round 1, certificate results/proofs/L017-i11-minimal-counterexample-structure.md (submitted 2026-10-27 04:10 UTC). Scratch folder: experiments/referee/L017-round1/ (own code; README.md there lists every file).

## Summary

I checked every step of Theorems 1–7 by hand and found no mathematical error in them. That covers the reduction lemmas (R) and (R+), Lemma U″ in its 1-, 2- and k-vertex forms, the Hall lemma, the edge lemmas of Theorem 3, the degree-3, degree-2 and degree-1 configurations of Theorems 4 and 5, Theorem 6, and Theorem 7. Theorem 7 rests on the identity τ(H) = m − ν(G) for linear 3-graphs of maximum degree ≤ 2, with no correction term, and on the Tutte–Berge bound 11ν ≥ 3|E| for every subcubic graph.

- **No circularity.** I11 is used only for proper induced subgraphs, and for H∖D in Theorem 1(g), where the m-minimality hypothesis handles it.
- **Slack bookkeeping.** The identity s(H−v) = s + 8 − 2d(v) and all its uses are right.
- **Patterns.** My own enumeration finds exactly the seven Hall-deficient patterns, and r ≥ 4 is impossible.
- **Independent computation.** I recomputed the computational claims with my own programs. That includes the role counts behind Corollary 13.3, the numbers of Remark 13.2, the engine decompositions of Theorem 6(iii) and C4, Theorem 7 on every connected linear Δ ≤ 2 3-graph with at most 21 vertices, 11ν ≥ 3M on every subcubic graph with at most 14 vertices, and the list of all linear vertex-critical violators with at most 11 vertices. I also extended that list to 12–14 vertices with Δ ≤ 3, which found five new 13-vertex examples; all of them satisfy the conclusions of Theorems 1, 4 and 5.
- **Re-runs.** I re-ran the prover's scripts C1, C2, C4, C5, C6, C8 and C9; their outputs are identical.
- **Honest marking.** The computational corollaries 13.3 and 13.5 are clearly marked as computations. The caveat that Theorems 1–5 never use (P2) or (P3), so that F7 and the (9,8,4) graphs satisfy them, is stated honestly in Step 10.

What prevents an ACCEPT is four small defects:
1. Remark 13.2 contains one false sentence: Property (P) fails for E_1.
2. Step 9.3 describes the engine inaccurately: it processes all decompositions, not "up to 2d components".
3. The DEPENDS ON line overstates the independence from (P2) and (P3).
4. The converse half of Theorem 6(ii) has a one-sentence gap: the free-choice property needed for a general extension is not stated.

All four can be fixed by editing text. None affects Theorems 1–7, Corollary 13.3 or Corollary 13.5. This is what the workflow calls "ACCEPT WITH FIXES"; under the referee rules, a fixable problem means NEEDS-WORK. After these edits I would accept.

## Checks performed (all in experiments/referee/L017-round1/, `nice -n 10..15`, one process, every command under `timeout`)

1. **Stored lists (inventory).** Extracted afresh: `tar xzf` of experiments/prover/{L012,L013,L014}/cells.tar.gz and L016/cells_new.tar.gz into `cells/`. I parsed them with my own parser (`list_cells.py`): 159 (n,m,t) keys.
   - `cells_slack01.py` gives the connected tight cells with n ≤ 26: (3,1,1), (10,7,4), (13,8,5), (14,12,6), (16,9,6), (17,13,7), (19,10,7), (20,14,8), (21,18,9), (22,11,8), (23,15,9), (24,19,10), (25,12,9), (25,23,11), (26,16,10). This is exactly the list in 13.1.
   - The non-empty ones with Δ ≤ 3 are (3,1,1): 1, (10,7,4): 4, (14,12,6): 2, (17,13,7): 6. (25,23,11) is not stored.
   - The slack-1 cells with n ≤ 26 are (8,5,3): 2, (11,6,4): 0, (12,10,5): 149, (14,7,5): 0, (15,11,6): 19, (17,8,6): 0, (18,12,7): 0, (19,16,8): 227, (21,13,8): 0, (22,17,9): 37, (23,21,10): 0, (24,14,9): 0, (25,18,10): 0, (26,22,11): 36. Every one is stored, giving 470 classes.
   - Total: 13 + 470 = 483, as the proof of 13.3 says. K8 removes no cell for n ≤ 30.
2. **Co-transversality, by a different method from the prover's.** `src/cotrans.c` decides τ(F−X) ≤ τ(F) − |X| for every vertex and every pair (Fact 0.4) with a decision branch-and-bound. The prover instead enumerates all minimum transversals. `validate_cotrans.py`: 400 random linear 3-graphs with n ≤ 11 against exhaustive search, 0 mismatches.
3. **C5 / Corollary 13.3 (`roles.py`) on the 483 Δ ≤ 3 classes.**
   - role_b ≠ 0 only for E_1; role_c = 0 for all; role_e ≠ 0 only for the two (8,5,3) classes; role_f1 = 0 for all.
   - role_f2 ≠ 0 for E_1, two (10,7,4) classes, both (8,5,3), 59 of the (12,10,5), 13 of the (15,11,6), 18 of the (19,16,8) and all 37 (22,17,9) classes.
   - Vertex form of U″: 8,325 predictions, 0 failures.
   - All of this is identical to C5, and confirms the case analysis of 13.3.
4. **Remark 13.2 / C2 (`remark132.py`) on the Δ ≤ 4 lists.**
   - 24,151 vertex predictions and 199,524 pair predictions, 0 failures, 0 violations of the pair lemma.
   - Types: in the tight lists only (1,2,1) (6 pairs in (10,7,4), 8 in (14,12,6), none in (17,13,7); 4 pairs remain with Δ ≤ 3). In the slack-1 lists only (1,2,0), (1,2,1), (1,3,1), (2,2,1), and none in (26,22,11).
   - E_1 has three pairs of type (1,1,1): see Problem 1.
5. **Patterns of Theorem 4(iii) (`patterns.py`).** I enumerated every surjective assignment of a,b | c,d | e,f to r components, modulo pair permutations, swaps within pairs and component relabelling, and tested for an SDR.

   | r | classes | Hall-deficient |
   |---|---|---|
   | 1 | 1 | 1 |
   | 2 | 5 | 5 ({1,1,s}, {1,1,2}, {1,s,s}, {1,2,s}, {s,s,s}) |
   | 3 | 8 | 1 (two pairs in F1, third pair split F2/F3) |
   | 4 | 6 | 0 |
   | 5 | 2 | 0 |
   | 6 | 1 | 0 |

   That is 7 patterns in total, exactly (a), (c1), (c2), (f), (e), (b), (d).
6. **Theorem 4(iv) equivalences, tested adversarially (`test_iv.py`).**
   - Setup: G is a disjoint union of 1–3 random connected linear 3-graphs with n ≤ 8 and free choice (60 library graphs). A new vertex v gets three disjoint pairs, none inside an edge, every component met.
   - (⋆) is decided directly, as τ(H) = τ(G) + 1. The (iv) condition is evaluated on the components after mapping to the canonical names.
   - 4,097 deficient configurations: (a) 412, (b) 2,186, (c1) 126, (c2) 6, (d) 5, (e) 91, (f) 1,271. Both (⋆) true and (⋆) false occur in every pattern except (c2), where all 6 have (⋆) false. Also 1,154 non-deficient ones (5,251 in all).
   - Result: 0 mismatches, and (⋆) never holds for a non-deficient distribution.
7. **Theorem 7.**
   - `src/thm7.c` on genbg output (`genbg -c -d1:3 -D2:3 -Z1 n m`, 3 ≤ n ≤ 21): all 12,101 connected linear Δ ≤ 2 3-graphs. τ, computed by exhaustive branch-and-bound, equals m − ν(dual graph), with ν by subset DP. The identity s = 3n0 + 11ν − 3|E(G)| always holds. The dual graph was always simple. The minimum slack is 0 only at E_1; for m ≥ 2 the minimum is 1, at (8,5), the dual of K4 with one edge subdivided.
   - `src/nu_subcubic.c` on `geng -D3 N`, 2 ≤ N ≤ 14 (626,280 graphs; the counts for N = 1..12 match C1, 52,662 in all): 11ν ≥ 3M always, equality only for M = 0. The least positive value of 11ν − 3M is 1, at graph6 `D]w` (K4 with a subdivided edge, plus isolated vertices for larger N). The least ratio ν/M is 2/7, at the same graph.
   - Small cases asked for: P2 = K2 (one edge): 11 ≥ 3; K3: 11 ≥ 9; K_{1,3}: 11 ≥ 9; K4: 22 ≥ 18. All are strict, as is every M ≥ 1 case.
   - By hand: the Tutte–Berge computation of 4.4 run with weight λ = 4/7 instead of 6/11 gives ν ≥ 2M/7 for every subcubic graph (components with c = 5, e = 7 are the extremal ones). So 11ν − 3M ≥ M/7, and 4.4 holds with room to spare.
   - The phrase "equality only for matchings" refers to H. It is right: s(H) = 0 iff n0 = 0 and n2 = 0, i.e. H is a disjoint union of edges (including the empty 3-graph). For G, equality holds iff E(G) = ∅.
8. **All linear vertex-critical violators with few vertices (`src/vcrit.c`, `src/vcrit2.c`).** Generated by `genbg -c -d1:3 -D<n or 3>:3 -Z1`; each graph gets τ by subset DP, a violator test, and a criticality test on all 2^n vertex subsets.
   - n ≤ 11, all degrees: 56,426 graphs. The connected linear violators are (7,5): 1, (8,8): 1, (9,8): 4, (9,12): 1, (10,12): 3, (11,10): 2. The vertex-critical ones are exactly F7 and two (9,8,4) graphs, identical to C3 and 10.2.
   - Δ ≤ 3, n = 12, 13, 14 (30,348 + 302,145 + 3,283,654 graphs): no violator at n = 12. At n = 13 there are five vertex-critical violators, all 3-regular (13,13,6) with s = −1. At n = 14 there is one violator, (14,11,6), and it is not vertex-critical.
   - `f7_check.py`: F7 satisfies (P3) on every subset and violates only (P2). The (9,8,4) and (13,13,6) graphs are F7-free and violate (P3) only at S = V.
9. **Conclusions of Theorems 1(a)–(f), 3, 4 and 5 on all 8 violators (`check_theorems.py`, exact).** I re-checked vertex-criticality, and verified 1(b) at every vertex and 1(f) for every |X| ≤ 3. At all 78 degree-3 vertices I verified 4(i), (ii), (iii) (⋆, free choice, r ≤ 3, Hall deficiency) and (v); the patterns were (a) 77 times and (b) once. At all 12 degree-2 vertices I verified 5(A); case (α) occurred every time. In all, 4,223 checks, 0 failures.
   - There are no degree-1 vertices, so Theorems 3(c)–(f) and 5(B) are exercised only by hand (see the audit).
10. **Theorem 6(iii) / C4 (`decomps.py`, own decomposition enumerator plus stored Δ ≤ 3 counts).**
    - 64 degree-3 decompositions at the 11 D = 3 top cells. 19 have r ≥ 4; 11 of these have inputs, 208 inputs in all.
    - Inputs from r ≤ 3 decompositions: 864, 16, 8, 952 and 334 for (23,20,10), (24,18,10), (25,22,11), (26,21,11), (27,25,12); 0 for the other six. All identical to C4.
    - The slack-0 decompositions of (28,24) are exactly [(28,24,12)], [(14,12,6)²] and [(3,1,1),(25,23,11)], as Remark 13.4 says.
    - By hand: the violator cells with s ∈ {−1,−2} are (28,18,11), (28,23,12); (29,16,11), (29,22,12), (29,27,13); (30,15,11), (30,20,12), (30,26,13). These match Theorem 6(i).
11. **Prover's programs, re-run read-only.** From experiments/prover/L017 with `PYTHONDONTWRITEBYTECODE=1`, writing output only to my `rerun/` folder. C1 (`check_lemma_m.py 12 3000 20261027`), C4, C5 (tight lists), C6 (`check_lemmas_random.py 1500 7`), C8 (`ext_hits_check.py`, L012's unchanged `ext_d`) and C9 gave byte-identical outputs. C2 differs only in the timing fields. I read `tight_configs.py`, `engine_decomps.py`, `ext_hits_check.py` and the definitions in `hyp.py`; they do what the text says. One difference: Property (P) in the code exempts E_1, the text does not (Problem 1).
12. **Sanity checks (`abase_check.py`).** A_base is (14,12,6) with s = 0, and every vertex is co-transversal. A_base − 0 = E_1 ⊔ (10,7) with τ = 5 and s = 0. K46 and K48 do record "no class has a vertex in every maximum Sidon subset". The record family has s = 7 + K.
13. **Inputs the certificate does not check itself.**
    - The worker list experiments/20261027-0300-tight-cells-d4/lists/cell_27_20_11_D3.txt.gz has 0 FOUND lines and an INFO line reporting 23 decompositions and 3,865 inputs, as 13.6 says (not otherwise checked).
    - The falsifier files part1_results.json and part2_enum_results.json say what the Falsifier-report paragraph claims. Their table of minimum slacks by (n,m) agrees with my Theorem 7 run.

## Step-by-step audit

**Step 0.**
- 0.1 Additivity: correct.
- 0.2 Heredity under vertex and edge deletion: correct.
- 0.3 The bound τ − |Z| ≤ τ(H−Z) ≤ τ: correct.
- 0.4 X is co-transversal iff τ(H−X) = τ − |X|, and an isolated vertex is never co-transversal: correct.
- 0.5 The bookkeeping: correct.
- 0.6 Linearity gives |∂(x,y)| = d(x) + d(y) − σ: correct.
- 0.7: correct. The degree-1 characterisation of isolated vertices of H − v uses that H is connected with n ≥ 2, which is the context there.
- 0.8 L016 Theorem 1 covers all of C with at most 27 vertices: I checked the statement.

**Step 1.**
- 1.1 (R): correct.
- 1.2 (R+): the edge partition E(R) ⊔ E(F_i) ⊔ E* and the union of transversals are correct.
- 1.3: with Z ≠ ∅, both H − Z and R are proper induced subgraphs. When W = V(H), R is the empty graph with s = 0. The step is correct.

**Step 2, (U).**
- If X is not co-transversal, then τ(F) − τ(F−X) ≤ |X| − 1. That gives s(F−X) ≤ s(F) + 8|X| − 11 − 2|∂X|, which is negative under the threshold. Correct.
- The vertex form needs no non-isolation hypothesis. For d = 0 the threshold s(F) < 3 is incompatible with s(F−x) ≥ 0, since s(F) = s(F−x) + 3. Correct, and Step 11.5's comment on the sketch is accurate.
- The pair threshold s(F) < 2|∂(x,y)| − 5 and its contrapositive, the pair lemma, are correct.

**Step 3, (H).**
- 3.1: the matched edge e goes to F_φ(e), and x_e ∈ e ∩ W_φ(e).
  - Because F_i − x_e is a proper induced subgraph of H, (U) gives a minimum transversal T_i ∋ x_e.
  - Injectivity makes T_i well defined.
  - Every edge of E* contains x_e ∈ T_φ(e). This includes edges between two blocks and edges between a block and R: E* is exactly the set of edges meeting W that lie inside no single W_i.
  - So (R+) applies with T_0 = ∅, giving s(H) ≥ s(R) + Σ s(F_i) + 2|E*| ≥ 0, a contradiction.
  - Correct. The E* = ∅ case is consistent: it is also contradictory, as it should be.
- 3.2: correct.
- 3.3: the circularity bookkeeping is correct.

**Step 4, Theorem 7.**
- 4.1: the dual graph is simple and subcubic, and |E(G)| = n2. Correct.
- 4.2, upper bound: a maximum matching plus one vertex for each uncovered H-edge. Correct.
- 4.2, lower bound: |F| ≥ |U| − k and k ≤ ν (one edge per component of (U,F)). Edges outside U need their own degree-1 vertex, so |T1| ≥ m − |U|. Correct.
- The no-correction remark is right. An all-degree-1 edge is an isolated G-vertex: it counts 1 in m, 0 in ν, and needs one transversal vertex. G may have isolated vertices; the formula covers them. Example: E_1 gives 1 = 1 − 0.
- 4.3: correct.
- 4.4: Tutte–Berge (published). The bounds t_i for c = 1..5, even c ≥ 6 and odd c ≥ 7 are correct, including (2c − 8)/11 for odd c and t = 2/11 at c = 5. Strictness for M ≥ 1 is correct.
- 4.5: correct.
- 4.6(a): the arithmetic 8m + 22 ≤ 10n with 3m ≤ 2n gives n ≥ 5. Correct.
- 4.6(b): reproduced.

**Step 5, Theorem 1.**
- (a), (b), (c), (d), (e): correct.
- (f): the thresholds |∂| ≥ 3 for s = −1 and |∂| ≥ 2 for s = −2 are right.
- (g): all minimal counterexamples have the same number N of vertices, so choosing m least is legitimate. H∖D ∈ C has N vertices, and the ceiling bound and the conclusion T ∩ e = {x} follow. Correct.

**Step 6, Theorem 3.**
- (a): Z = e, T = {a} gives 11 > 9 + 2d(a). Correct.
- (b) and (c): Z = {y,a}, T = {a} gives d(a) ≤ 2. Correct.
- (d): correct.
- (e): Z = {x,y1,y2}, |∂| = 2, giving 11 > 13. Correct.
- (f): δ ≤ 1 and 11δ ≥ 10 − s force δ = 1 and s = −1. Correct.

**Step 7, Theorem 4.**
- (i) and (ii): correct. Components meet the co-vertices by 0.7, and there are no isolated vertices.
- (iii): (⋆), free choice and the Hall application with R = H[{v}] are correct. The deficiency analysis (|J| = 2 or 3) and the exclusion of r ≥ 4 are correct; the r = 2 classes number five, and my enumeration confirms this (check 5).
- (iv): I re-derived both directions of all six conditions. They are pure set logic given free choice, and the random test (check 6) found no counterexample.
- (v): the forced pairs are the right ones, and the pair lemma gives the bounds 2 and 3.
- (vi): all cases (b), (c1), (c2), (d), (e), (f) are correct, including the use of "no P_j inside an edge of G" and linearity for {c,e} in (f).

**Step 8, Theorem 5.**
- (A)(i)–(iv), (α) and (β): correct. The Hall step gives N(P1) = N(P2), a single non-trivial component, and the β-case reasoning (b of degree 2, c and d of degree ≥ 2) holds.
- (B)(i): the component of a has slack ≥ 5 by (U), so H − y is connected with slack 5. Correct.
- (B)(ii): F = H − {y,a} is tight, with m(F) = m − 2 and g ∈ E(F). Its components are tight with no isolated vertex, and F is connected by free choice. The facts |g ∩ {c,d}| ≤ 1 and d_H = 2 for the vertex outside g are correct.

**Step 9, Theorem 6.**
- (i): correct; I also checked the cells by hand (check 10).
- (ii): the equivalence τ(H) = τ(G) + 1 ⟺ (⋆) is proved for any extension, and the converse s(H′) = s(G) − 2 is correct. One justification is missing: Problem 4.
- (iii): the descriptive claims are reproduced (check 10), except the parenthesis criticised in Problem 2.

**Step 10.**
- 10.1 is accurate. I went through every proof in Theorems 1(a)–(f), 2–5 and 7: only linearity and I11 for proper induced subgraphs are used. The exceptions are "n ≥ 28" and "n − 2 ≥ 26", which 10.1 states.
- 10.2 is reproduced (check 8).
- 10.3 is a fair meta-remark. F7 satisfies (P1) and (P3) but not (P2); the (9,8,4) graphs, and also the five (13,13,6) graphs I found, satisfy (P1) and (P2) but not (P3). So any proof must use both (P2) and (P3). The caveat is stated honestly.

**Step 11.** I compared it with kb/methods/i11_proof_plan.md. All six corrections are accurate:
- R(c) is garbled.
- The two-vertex form is garbled.
- (H2) lists only (b) and (c), missing (e) and (f).
- The suggested correction term for Lemma M is wrong.
- d ≥ 1 is not needed.
- The class counts agree.

**13.1.** The tight-cell table is reproduced. The refutation of Conjecture T is correctly tagged as resting on an unrefereed worker computation. The Δ = 4 deletion remark is correct.

**13.3.** Valid given the completeness of the stored refereed lists (check 1) and the role counts (check 3), both reproduced.
- (i): a (25,23,11) component would leave only 2 vertices.
- (ii): the (29,16,11) arithmetic (28 > 2·13 + 1) is right.
- (iii): correct.

**13.4.** Reproduced, and conditional as stated.

**13.5.** Correct, and correctly marked.
- (i): (26,16,10) is the only tight connected cell on 26 vertices, and it is empty with Δ ≤ 3.
- (ii): n1 = n3 + 2 in (28,18,11), and n3 = 13, n2 = 15 in (28,23,12).
- (iii): correct.

**13.6.** Correctly conditional on the unrefereed worker run. The f(29) = 17 reasoning works: K8 gives h ≥ 16; h = 16 forces m ∈ {26,27}; and K1 gives the upper bound 17.

**14.3.** The claim def_t ≤ t(n − m) and "KT_t implies I11" are correct. The values of w_t are right.

## Problems found (in order of severity)

1. **(Minor, false statement in a non-load-bearing remark) Remark 13.2, Property (P).**
   - The text says that Property (P) — "every two vertices of degree ≤ 2 lie in a common minimum transversal unless they share an edge and have degrees 1 and 2" — "holds for all 13 connected tight classes with Δ ≤ 3 and at most 26 vertices".
   - This is false for E_1 = (3,1,1), which is one of the 13. Its three pairs have degrees (1,1), share the edge, and lie in no common minimum transversal, since τ = 1. The same paragraph had just said "in E_1 all three pairs".
   - The prover's `tight_configs.py` exempts E_1 explicitly ("or F is the single edge"), but the text does not.
   - Fix: "holds for the 12 tight classes with at least 10 vertices (in E_1 all three pairs are exceptions)". Nothing depends on (P); Corollary 13.3 uses the role counts, which are correct.
2. **(Minor, inaccurate description) Step 9.3.**
   - The text says the engine does not use Theorem 4(iii) "(it processes decompositions with up to 2d components)".
   - In fact `engine.recurse` (experiments/prover/L013/engine.py) processes every decomposition, whatever the number of components. C4's own output contains r = 7 > 2d = 6 at (27,14,10,3), with 2 inputs; those extensions are discarded later, because ext_d output that is not connected fails `filt`.
   - Fix: "it processes all decompositions, including those with r ≥ 4 (even r > 2d), and discards disconnected extensions only at the `filt` stage".
3. **(Minor, overstatement) DEPENDS ON, last bullet but one.**
   - The bullet says "(P2) and (P3)" are not used "in Theorems 1(a)–(f), 2, 3, 4, 5 and 7".
   - But "n ≥ 28" in Theorem 1(a) and "n − 2 ≥ 26" in Theorem 5(B)(ii) rest on L016, a statement about C. (Theorem 4(ii) also calls the components "members of C", but only as a label, not in a proof step.)
   - Step 10.1 states the exceptions correctly; the DEPENDS ON line should repeat them.
4. **(Minor gap of exposition) Theorem 6(ii), converse half (9.2).**
   - The statement says the Theorem 4(iv) condition "is equivalent to τ(H) = τ(G) + 1", and that every such extension in C is a violator.
   - For an arbitrary extension H′ (not known to be a minimal counterexample), the equivalence between the (iv) condition and (⋆) needs the free-choice property of the F_i.
   - That property holds: each F_i ∈ C has s(F_i) ≤ 1, no isolated vertex, and F_i − x ∈ C with fewer than N vertices, so (U) applies. But 9.2 cites only "Theorem 4(i)–(iv)", which were proved for a minimal counterexample.
   - One sentence fixes it.

Observations, not errors:
- (a) Step 10.2 could mention that, among linear 3-graphs with Δ ≤ 3, there are five more linear vertex-critical violators on 13 vertices: 3-regular, (13,13,6), s = −1, F7-free, violating (P3) only at S = V. There are none on 12 or 14 vertices. They satisfy every checked conclusion of Theorems 1, 4 and 5, all 65 degree-3 vertices giving pattern (a), and they strengthen 10.3.
- (b) Theorem 7 holds with room to spare: ν ≥ 2|E(G)|/7 for every subcubic G (same Tutte–Berge computation with λ = 4/7; verified for N ≤ 14), so s(H) ≥ 3n0 + n2/7.
- (c) After submission, the falsifier folder (experiments/falsify/i11-structure-lemmas/verified_tight_25_23_11_candidates.json) reports tight members of C in (25,23,11) with Δ = 4 (unrefereed). This does not conflict with the certificate, which uses only Δ ≤ 3 lists and treats (25,23,11,3) as uncomputed. It may be worth a line in 13.1(ii).

## Independence statement

All verification code in experiments/referee/L017-round1/ was written by me for this review and does not import e757, the judge, or the prover's `hyp.py`:
- the parser of the stored lists;
- the co-transversality decider `src/cotrans.c` (Fact 0.4 by decision branch-and-bound, a different method from the prover's enumeration of all minimum transversals);
- the role and type computations;
- the pattern enumerator;
- the Theorem 7 checkers `src/thm7.c` and `src/nu_subcubic.c`;
- the vertex-critical violator search `src/vcrit*.c`;
- the theorem-conclusion checker, the random Theorem 4(iv) test, the decomposition enumerator, and the A_base and F7/(P3) checks.

Generators: unmodified nauty `geng`/`genbg` from experiments/referee/L013-round2/out/nauty_build/. Data: the refereed tarballs of L012, L013, L014 and L016, extracted afresh. The prover's scripts were only re-run read-only, as a reproducibility check, with outputs written into my `rerun/` folder.

I did not modify the certificate, results/LEDGER.md, kb/, judge/ or any file outside my scratch folder and this review.
