VERDICT: NEEDS-WORK
(Editorial fixes only. On the workflow's scale this is ACCEPT WITH FIXES: I found no mathematical error and no unmarked gap. Every theorem not marked GAP is correctly proved as stated, and GAP 1-4 are honestly marked. The first line is NEEDS-WORK only because the referee format allows just ACCEPT / REJECT / NEEDS-WORK, and ACCEPT requires that no problem remain.)

Referee #1, round 1, of results/proofs/L022-i11-realizable-route.md (submitted 2026-10-27 06:36 UTC). Scratch folder: experiments/referee/L022-round1-referee1/. I did not read any other review of L022. I also did not open the other L022 folders under experiments/referee/.

## Summary

L022 is a PARTIAL certificate on the realizable class R, the AP hypergraphs of (4,5)-sets. I checked every part it presents as proved.

- **Theorem 1.** Line by line, it is correct.
  - (b) The maximum-principle proof that the AP forms of any ordered set with injective midpoints are linearly independent is sound.
  - (c) Edge deletion yields a realization in the same order whose AP hypergraph is exactly H(A)\D.
  - (b'), (d), (e), (f) hold. In (f), edge-criticality transfers to R for an (n,m)-minimal counterexample.
- **Theorem 2 (i)-(vii).** Each sub-claim follows from L017 Theorem 4 and the sub-extension count 2.0. That count is valid for every linear vertex-critical violator.
- **Corollary 3.** Correct. Its conditional parts are marked as conditional.
- **Corollary 3'.** Correct, given the stored lists. I re-derived the data it uses (D1-D3) from the refereed tarballs with my own code.
- **Theorem 4 (O1-O7).** Elementary and correct.
- **Theorem 5.** Its computational table is reproduced. Q10 = (10,7,4)#0 = {012,034,157,268,379,489,569} is non-realizable, and all seven one-edge deletions are exactly realizable. I checked both with my own exact code, written from scratch.

The defects are editorial:
- outdated dependency statuses (L017 and L018 are now ACCEPTED);
- a one-word imprecision in the non-load-bearing hypertree sketch of Theorem 1(e);
- one clause of Corollary 3' that should state its hypothesis.

Nothing outside GAP 1-4 is unproved, apart from the parts explicitly tagged as conditional, as computations, or as discussion (W1-W7).

## Theorem-by-theorem audit

### Theorem 1
- **(a) Heredity.** Trivial: whether a triple is an AP depends only on its three points. Correct.
- **(b) Independence, Step 1.2.**
  - Injectivity of mu makes the m x m minor N (columns = the midpoint variables) have diagonal -2.
  - Each row has at most two further entries 1, at the columns of e^- and e^+. These are the APs whose midpoints are a(e) and c(e). They are unique by injectivity and distinct from e and from each other.
  - Take y with Ny = 0 and max|y_e| = Lambda > 0. Choose e_0 with y = Lambda and c(e_0) largest. Row e_0 gives 2*Lambda <= Lambda + Lambda, with equality only if e_0^+ exists with y = Lambda. Then c(e_0^+) > mu(e_0^+) = c(e_0), a contradiction.
  - So N is nonsingular, and the forms are independent.
  - The proof uses only injectivity of mu and a(e) < mu(e) < c(e). Linearity is not needed. Correct.
  - "Every point is the midpoint of at most one AP" does follow from weak Sidon: 2x_b = x_a + x_c = x_a' + x_c' is a coincidence of sums of distinct elements over different pairs.
- **(b') Rigidity.** dim V = n - m = 2, and V contains x and the all-ones vector 1, which are independent. Correct.
- **(c) Edge deletion, Step 1.3.** This is the point the task asked me to check carefully.
  - Let V' be the solution space of the forms l_f, f in E' = E\D. A form of Phi that vanishes identically on V' vanishes at x. So it is an l_e with e in E, because x is weak Sidon and has distinct points.
  - For e in D, l_e does not vanish identically on V'. Otherwise l_e would lie in (V')^perp = span{l_f : f in E'}, contradicting (b). This is exactly where independence is needed: no deleted AP is forced by the remaining ones.
  - A rational point y in V' close to x avoids the finitely many proper subspaces. Rational points are dense because V' is defined over Q. Such a y keeps the order, is weak Sidon, and has 3-APs exactly E', with the same midpoints.
  - Since E' is linear, y is a (4,5)-set by 0.2. I re-proved 0.2 by hand: (4,5) iff weak Sidon and the APs are linear.
  - So "deleting an edge" means a realization, in the same order, whose AP hypergraph is exactly the smaller edge set. Correct.
- **(d) Isolated vertex and disjoint union.** Correct.
  - Cross coincidences have the form phi_A(x) + q*phi_B(z) + t*phi_B(1) = 0.
  - If phi_B(1) != 0, the equation fails for all t but one.
  - If phi_B(1) = 0, then phi_B = X_p - X_q with p != q. This comes from a split parallelogram; no split AP form has coefficient sum 0 on one side. Then the equation fails for all q but one.
  - The wording "(inspect the three types ...)" is terse but right.
- **(e)** The R-membership characterization via M_R is correct, because R is closed under vertex and edge deletion. Members of M_R are connected with no isolated vertex, by (d). F7 is in M_R.
  - The clause "at least 5 edges if linear" relies on K33 [verified-here] plus a sketch for the 9-vertex hypertrees. The sketch does not say which role the shared vertex u takes in the new AP. If u were made the midpoint (p = u - delta, q = u + delta) and u is already a midpoint (a,u,b), then p + q = a + b is a forced weak-Sidon violation. With u as an endpoint (p = u + delta, q = u + 2*delta), every Phi-form touching p or q has delta-coefficient alpha + 2*beta != 0, except the new AP form itself. So generic delta works.
  - I verified the clause independently: all 502 labelled connected linear configurations with at most 4 edges are exactly realizable (check_small_configs.py). Every isomorphism class appears in that list. The clause is true, and the sketch needs one word (E2).
- **(f)** Proper induced subgraphs lie in R by (a) and have fewer vertices, so H is a linear vertex-critical violator. Then n >= 28 by R ⊆ C and L016. For an (n,m)-minimal H, H\D is in R by (c), with the same n and fewer edges, so s(H\D) >= 0. The arithmetic of L017 Step 5.7 then applies verbatim. Correct.

### Theorem 2
All sub-claims are valid for every linear vertex-critical violator. L017 Theorem 4 (i)-(v) holds in that generality: I re-checked the dependency chain of L017 Step 10.1, including the case Z = V(H), which 1.3 covers with s(empty) = 0. All slack bounds I used are for proper induced subgraphs.
- **2.0.** n = n_F + |Q| + 1, m = m_F + k + k', tau >= tau_F + t. And a transversal with at most tau_F vertices lies inside V(F) and is a minimum transversal of F. Correct.
- **(i)** With P1 and P2 inside F1:
  - P3 is not inside F1, by 0.4(ii).
  - A minimum transversal of F1 meeting P1 and P2, together with one through the P3-vertex in another component, would contradict (star).
  - Hence t = 1, and s(H[V(F1)+v]) <= s_F1 - 4 < 0.
  - Correct; this re-proves L018 6(b'). r <= 2 follows because (d) is the only pattern with r = 3.
- **(ii) Pattern (e).**
  - With Q = {f}, the edges are those of F1, {v}+P1 and {v,e,f}; no edge links F1 to f except at v.
  - t = 1 by L017 4(iv)(e), so the slack is <= s_F1 - 1. The set is proper because |V(F2)| >= 3.
  - Hence s_F1 >= 1, and symmetrically s_F2 >= 1, which contradicts s_F1 + s_F2 <= 1. Correct.
- **(iii) Pattern (f).** Q = {d} (respectively {f}), t = 1 by 4(iv)(f), so s_F1 >= 1. Then s_F1 = 1, s_F2 = 0, s = -1, and both sub-extensions are tight. Correct.
- **(iv)** The pair lemma gives d(d) + d(f) - sigma <= 2. Suppose sigma = 1 with g = {d,f,z} and F2 != g. Take Q = g, so k = 3, k' = 1.
  - If |T| = tau_F1 + 1, then T = T1 + u with u in g and v not in T.
  - u = z: T1 must meet P1 and contain c and e. u = d: T1 must meet P1 and contain e. u = f: T1 must meet P1 and contain c.
  - Each case is excluded by 4(iv)(f). So t = 2 and the slack is <= s_F1 - 2 = -1 on a proper subset.
  - Correct. The case analysis u in {z, d, f} is complete.
- **(v)** Q = {y1,y2,y3}. If |T| = tau_F1 + 1, then T = T1 + y_j, and the two other edges at v force two of the x_k into T1, which 4(iv)(b) excludes. So t = 2 and the slack is <= s_F1 - 2 < 0. With both triples edges, H is F7, as I checked against {012,034,056,135,246}. Correct.
- **(vi)** The pair lemma applied to pairs of x's with d_F = 2 gives 4 - sigma <= 2, which is impossible. Correct; it is also true for single edges.
- **(vii)** d_F(w) = 1, and tau(F-w) = tau_F - 1 because w is co-transversal.
  - T = T'_F + (other T_i) + v has size tau(G) = tau(H) - 1 = tau(H-w) (L017 Theorem 1(b)), and it meets every edge of H - w.
  - If T met {p,q}, it would meet both edges at w and be a transversal of H of size tau(H) - 1, which is absurd. (This is immediate; citing L017 5(A)(iii) is fine.)
  - So no minimum transversal of F - w contains p or q, which is equivalent to {w,p} and {w,q} being non-co-transversal. Correct.
- **Summary list (2.8).** Correct.

### Corollary 3
- 3.1: correct. With s = -2 all components are tight, pattern (f) is excluded by (iii), and (vi) applies. Two single edges would give n = 7.
- 3.2 (under P2'): correct. P2' for C equals L018's Conjecture P2: connected and not a single edge implies at least 5 vertices.
- 3.3: correct as a conditional.
  - z is not a co-vertex of v, so it is a pendant of H.
  - The transfer of L018 Theorem 5 to R is plausible: its proof (Lemmas 0.3 and 0.5, Steps 5.1-5.11) applies I11 only to induced subgraphs.
  - The bound ">= 27" rests on role counts, which I recomputed (below).

### Corollary 3' (computation; tagged as such)
- The logic of Step 3.4 is correct:
  - (f): F1 has slack 1 and carries a role_f1 configuration.
  - (b) with s = -1: the slack-1 side carries a role_b triple.
  - (b) with s = -2: one tight side has at least two pendants. For the cell (25,23,11) with Delta <= 3, I re-did the count 2*n1 + n2 = 6, and with L018 Lemma 0.5 this gives at most one pendant.
  - In each case one side has at least 27 vertices, so n >= 31.
- I re-derived the data D1-D3 independently:
  - **D2 and D3 recomputed by my own code** (check_roles.py) on every Delta <= 3 class of the stored lists (1, 4, 2, 6 tight; 2, 149, 19, 227, 37, 36 slack-1):
    - role_b > 0 only in E1;
    - role_f1 = 0 everywhere;
    - role_e > 0 only in the two (8,5,3) classes;
    - every tight class other than E1 has at most 1 pendant.
  - **D1 check:**
    - the Delta <= 3 counts of inputs/ equal the FOUND counts of the refereed L013 and L016 D3 lists;
    - all 16 other connected slack-0/1 cells with n <= 26 have FOUND = 0 (each with an INFO line) in experiments/prover/L013/cells.tar.gz and L016/cells_new.tar.gz (runA);
    - the cell enumeration (check_cells.py) reproduces exactly the 15 tight and 14 slack-1 connected cells.
- Arithmetic:
  - the n = 30 violator cells are (30,15,11), (30,20,12), (30,26,13);
  - H - v lies in (29,12,10), (29,17,11), (29,23,12);
  - 29 > 2*12 + 1, so (29,12,10) cannot be connected.
  - In fact, even with r <= 3 components (sum of 2*m_i + 1 <= 27 < 29), so the (30,15,11) exclusion does not need the stored lists at all (E3).
- N4' arithmetic (in "Computations needed", not a claim): (27,15,10) is the only slack-1 connected cell with 27 vertices, and (27,20,11) the only tight one. Correct.

### Theorem 4 (O1-O7)
- All proofs are elementary and correct.
- O3 case analysis: b = b'; b = a'; a = b'; and otherwise a weak Sidon violation. I also derived the "at most twice" reformulation.
- O6: rho_2 has nonzero coefficients on P3, which do not occur in rho_1, and rho_1 != 0. The dimensions are n - m and (n-1) - (m-3) by (b).
- O7: K31 re-derived (x_a + x_q = x_b + x_p).

### Theorem 5 (computation; tagged as such)
- Every one of the 290 stored explicit realizations in experiments/prover/L022/out/realize_*.jsonl passes my independent checks:
  - distinct points;
  - (4,5), by brute force over all 4-subsets for n <= 26, and by weak Sidon plus linearity;
  - AP set exactly equal to the class edge set.
- The Delta <= 3 counts and the tested/realizable/non-realizable splits match the table. There were no timeouts.
- The (19,16,8) row is partial, and honestly says so: 66 of 227 classes tested.
- Q10 (check_q10.py):
  - tau = 4, slack 0, linear, F7-free, (P3), degrees 2^9 3^1.
  - All 3^7 = 2187 midpoint labellings are dead: 1230 force equal points and 957 force a parallelogram. So Q10 is not even a sub-hypergraph of any H(A).
  - Each of the 7 one-edge deletions has an explicit integer realization with exactly those APs, checked by brute force.
  - Since R is closed under sub-hypergraphs and Q10 has no vertex of degree < 2, Q10 is in M_R.
- As an independent control, 3 of the 23 non-realizable (12,10,5) classes (0, 36, 42) are confirmed non-realizable by my exhaustive search over 59,049 labellings each.
- All 12 stored (21,18,9) obstructions have a vertex of degree 4.

### Corollary 6 (computation; tagged as such)
It follows from L017 Corollary 13.3, which applies because R ⊆ C and Theorem 4 holds for linear vertex-critical violators. The role counts it uses agree with my recomputation. E1 and both (8,5,3) classes are realizable, as I verified from the stored realizations.

## Checks performed (all in experiments/referee/L022-round1-referee1/)
Every command was run as `timeout ... nice -n 10 python3 ...`, one process at a time. My code imports nothing from e757, judge/ or the prover folders. The library files are rlib.py and realize.py: exact Fraction RREF, subset-recursion and branch-and-bound tau, brute-force (4,5) check.

- `check_q10.py` → check_q10_output.txt: Q10 non-realizable (2187/2187 labellings dead); 7/7 one-edge deletions exactly realizable.
- `check_thm1.py` → check_thm1_output.txt:
  - (b), exhaustive over every ordered injective-midpoint pattern with n <= 7: 30,471 patterns, 0 dependent. Full rank mod 2^61-1 certifies full rank over Q.
  - (b), 4,000 random patterns with n <= 45: 0 dependent.
  - 15 stored sets (data/small_records.json, C001-C008): rank = m in 15/15; the 7 saturated ones have dim V = 2.
  - (c): 261/261 deletions (every single AP, plus random subsets) realized in the same order with exactly the remaining APs.
- `check_small_configs.py` → check_small_configs_output.txt: 502 labelled connected linear configurations with <= 4 edges, all exactly realizable; F7 not realizable (243/243 labellings dead); all its 4-edge sub-hypergraphs exactly realizable.
- `check_thm2.py` → check_thm2_output.txt:
  - F7 (vertex 0: pattern (b), both sides single edges) and the two (9,8,4) violators (all 12 degree-3 vertices: pattern (a)) were confirmed by my own code to be linear vertex-critical violators with s = -2, -1, -1. 0 failures of (i)-(vii) (40 pairs tested in (vii)).
  - Random search, 12,000 graphs with n in 8..13: 117 vertex-critical violators in total (including the three above), 697 degree-3 vertices, patterns (a) 696 and (b) 1. 0 failures.
- `check_thm4.py` → check_thm4_output.txt: O1-O7 and rank = m on 305 sets (the stored sets plus 290 realizations): 0 failures. Theorem 1(d): 60/60 generic gluings are (4,5)-sets with H(C) = H(A) + H(B).
- `check_thm5.py` → check_thm5_output.txt: the Theorem 5 table, as above.
- `check_roles.py` → check_roles_output.txt: D2 and D3, as above.
- `check_cells.py` → check_cells_output.txt: the cell arithmetic.
- D1: the tarball FOUND counts were obtained by extracting the refereed tarballs into my session scratchpad and running grep -c.
- Re-runs of the prover's own scripts:
  - minimal_obstruction_10_7_4.py, local_configs.py and independence_stress.py reproduce their out/ files byte for byte.
  - order_checks.py reproduces its output, with 305 instead of 303 sets, because C007 and C008 appeared after the prover's run; 0 fails.
  - I ran these with PYTHONDONTWRITEBYTECODE=1 and stdout redirected to my folder; git status shows nothing changed under experiments/prover/L022.

## Problems found (in order of severity; all editorial)
- **E1. Outdated dependency statuses.** DEPENDS ON calls L017 "the revised text is unrefereed". L017 is ACCEPTED (two referee ACCEPTs in round 2, 05:25 and 05:30 UTC; K64). L018 is marked "[unrefereed]", but it is now ACCEPTED as a partial certificate, including Theorem 5(vi) and Proposition 6.2 (conditional on P2). Update:
  - the STATUS and DEPENDS ON lines;
  - the "[unrefereed]" on L018 Theorem 5(vi) in the Corollary 3 statement, in Step 3.3 and in the Tags line;
  - the Statement of Corollary 3 and the Tags line, which should say that P2' (C-version) is L018's Conjecture P2.
  These labels understate the dependencies, so nothing is overclaimed.
- **E2. Theorem 1(e), Step 1.5: the hypertree sketch.** Specify that each new edge {u,p,q} takes the shared vertex u as an endpoint (p = u + delta, q = u + 2*delta, delta generic). If u is made the midpoint and u is already a midpoint, the extension is forced to violate weak Sidon. Add the one-line delta-coefficient argument. The clause is true (all 502 labelled configurations verified) and not load-bearing.
- **E3. Corollary 3', last clause.** "The cell (30,15,11) contains no violator" should repeat the hypothesis "if I11 holds for all graphs with at most 29 vertices". Optionally, note that this clause needs no stored list: with r <= 3 components, G has at most 2*12 + 3 = 27 < 29 vertices.
- **E4 (cosmetic).**
  - Theorem 2(vi) holds for single edges too, so "that is not a single edge" can be dropped.
  - In Step 2.7, the appeal to L017 Theorem 5(A)(iii) is not needed: a transversal of H with tau(H) - 1 vertices is absurd directly.
  - Step 1.4's "inspect the three types" could list the cases (parallelogram split 2+2 gives X_p - X_q on B; no split AP form has coefficient sum 0 on one side).

## GAPs and what remains unproved
- GAP 1 (pattern (a): H - v connected), GAP 2 (pattern (b)), GAP 3 (pattern (f)) and GAP 4 (the uncomputed tight cell (25,23,11)) are stated honestly. None is finite, and I11 on R is not claimed.
- Outside GAP 1-4, nothing presented as proved is unproved. The remaining non-theorem material is explicitly tagged:
  - the conditional sentences of Corollary 3, which depend on P2' and on L018 Theorem 5(vi), now accepted;
  - the computational statements Corollary 3', Theorem 5 and Corollary 6, which I re-derived as above;
  - the discussion W1-W7.
- W7 cites realizability results that I did not re-verify: all 12 tight (21,18,9) classes non-realizable, the four (25,23,11) candidates non-realizable, 2 of the 11 tight (14,12,6) classes non-realizable. These come from the unrefereed experiment experiments/20261027-0400-realize-21-18-9. They are discussion only, and no theorem uses them.

## Independence statement
I wrote every verification script in experiments/referee/L022-round1-referee1/ myself, for this review. They import no code from e757/, judge/, experiments/prover/ or any other experiment. Their only inputs are data files:
- the stored class lists;
- the explicit point vectors in experiments/prover/L022/out/realize_*.jsonl;
- obstructions.json;
- data/small_records.json and results/claims;
- the edge lists of the two (9,8,4) violators, copied from L017's C3 output and then independently verified to be linear vertex-critical violators.

I read SYNTHESIS.md section 1 after my own line-by-line reading of the proofs of Theorems 1, 2 and 4, and before running my computations. I re-verified each item it lists myself. I did not read any other review of L022. I modified no file outside my scratch folder and this review.
