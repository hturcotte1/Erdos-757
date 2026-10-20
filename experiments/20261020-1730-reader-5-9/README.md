# Reader's self-similar "5/9" family for Erdős #757: independent rebuild, exact verification, judging

Status tags: the construction and the claim c* <= 5/9 are **[community]** (not ours). Every number computed here is **[verified-here]**
(exact integers or Fractions; reproduce with the commands below). The all-depth proof in section 5 is **[derived-here]** and **unrefereed**.
Nothing here has been refereed; the orchestrator decides what goes into kb/known_results.md, results/LEDGER.md and kb/00_START_HERE.md.

## 1. Question
Is the family S_K = O u phi(O) u ... u phi^K(O), posted on Erdős Problem a Day on 19 Oct 2026 (reader submission 7bkzb8, 17 Oct 2026), a family of
(4,5)-sets with |S_K| = 11 + 9K and largest Sidon subset exactly 7 + 5K? If so, S_6 (65 points, h = 37, 37/65 = 0.56923 < 4/7) beats the
published 4/7 (goal clause (A)) and c* <= (7+5K)/(11+9K) -> 5/9.

## 2. Sources (untrusted third-party text, saved as plain text, nothing executed)
Saved in `kb/literature/sources/aday_757_reader_5_9/` (fetched 2026-10-20T17:24Z, raw GET through the agent proxy, converted by an inert HTML-to-text parser):
- https://erdosproblemaday.com/day/757-reader-five-ninths-refereed  (write-up by the site, "Patrick White with Claude", dated Oct 19 2026, status PARTIAL, "unreviewed by humans")
- https://erdosproblemaday.com/problem/757
- also read (not saved): https://erdosproblemaday.com/submission/7bkzb8 (the reader's one-paragraph submission and the site's verdict).
- The page links a verification folder (github.com/pw/ErdosProblemADay.com/tree/main/verification/757/reader-5-9; proof, two solvers, referee report); the scout found it HTTP 404 and we did not use it. The page says the submitter supplied **no code**.
- Scout notes: results/reviews/L014-f23-equals-14__scout__20261020T161510Z.md, section "NEW since 2026-10-17" (with its quick check, scratch script not part of the repo).

### The family, as stated on the page (exact quotes, brief)
- "O = {0,49,75,83,98,101,117,119,121,159,269} and phi(x) = 101 + 18x/269, so phi(0) = 101 and phi(269) = 119 are both in O."
- "S_K = O u phi(O) u ... u phi^K(O) is a (4,5)-set with 11 + 9K points whose largest Sidon subset has 7 + 5K points, so c <= lim (7+5K)/(11+9K) = 5/9. (Scale by 269^K for integers.)"
- "one 65-point set (depth 6, Sidon number 37) already beats 4/7."
- Nine 3-APs in O, "one centred at each of its nine interior points": {0,49,98}, {49,75,101}, {49,83,117}, {49,159,269}, {75,98,121}, {75,117,159}, {83,101,119}, {83,121,159}, {117,119,121}. phi shrinks by 18/269, "consecutive copies share exactly two points and copies further apart share none".
- Proof idea: "no additive relation ever crosses copies", so a Sidon subset is a chain of choices per copy avoiding that copy's nine APs; "a four-state max-plus transfer matrix -- states = which of the two shared points are taken -- ... the vector after copy 0 is [6, 7, 7, 7], one step adds exactly 5 to every entry, and so the Sidon number is 7 + 5K at every depth."
- Every-depth argument: with L = 27169/251 the fixed point of phi, "251(p - L) = (18/269)^j (251x - 27169)"; a relation "must balance its deepest level modulo 269 ... the span between the deepest and shallowest levels is at most ten", so the depth-12 census covers every depth.
- Page's own checks (not ours, not reproduced from their code): all 4-subsets for K <= 12; relation census in S_12 (117 = 9*13); CP-SAT and CaDiCaL for K <= 8; a "hostile referee" with four gaps "fixed". Page: "the lower bound 9/17 is untouched" and "it does not determine c".

## 3. Method and commands (all in this directory; run from the repo root)
```
python3 experiments/20261020-1730-reader-5-9/build_family.py          # exact Fractions -> data/reader_5_9_family.json (K=0..8)
python3 experiments/20261020-1730-reader-5-9/check_family.py --ks 0,1,2,3,4,5,6,7,8 --workers 2   # per-K exact checks -> check_results.json (log: check_K0_8.log)
python3 -I experiments/20261020-1730-reader-5-9/census_deep.py 0 1 2 3 4 5 6 7 8 9 10 11 12 15 20 30 50 75 100 150   # -> census_deep_results.json
python3 -I experiments/20261020-1730-reader-5-9/literal_big.py        # literal 4-subset test K=9..12 -> literal_big_results.json
python3 -I experiments/20261020-1730-reader-5-9/lemma_constants.py    # constants and finite facts used in section 5
python3 -I experiments/20261020-1730-reader-5-9/make_results.py       # -> results.json, table.md
python3 scripts/new_claim.py --slug reader-5-9-K6 --set-file experiments/20261020-1730-reader-5-9/set_K6.json --notes '...'   # -> results/claims/C003-reader-5-9-K6.json (log: claim_K6.log)
python3 scripts/new_claim.py --slug reader-5-9-K7 --set-file experiments/20261020-1730-reader-5-9/set_K7.json --notes '...'   # -> C004 (log: claim_K7.log)
```
**Three readings of S_K coincide** (asserted in build_family.py, K = 0..8, as exact sets of Fractions): (R1) recursion A_K = O u phi(A_{K-1}) (the scout's
reading); (R2) the page's union O u phi(O) u ... u phi^K(O); (R3) the closed form L + (18/269)^j (x - L), L = 27169/251. This is immediate (phi(A_{K-1}) = phi(O) u ... u phi^K(O)).
The lcm of the denominators is exactly 269^K for every K (gcd of the integers is 1), so the integer sets are the page's "scale by 269^K"; max element of S_6 is 101921535994725989 (matches the scout).

Checks per K (all exact; independent of each other where marked):
1. |S_K| = 11 + 9K (no duplicates).
2. (4,5): our own 4-subset loop (`>= 5` distinct positive differences among the 6; for K <= 5 also the literal `|B-B| >= 11`), plus `e757.core.is_45_set`; K = 9..12 own loop (literal_big.py).
3. Relation census: every solution of a+b = c+d (a<=b, c<=d, pairs distinct): all are 3-APs, the number of 3-APs is 9(K+1), each lies in one copy phi^j(O), no two share two points, no parallelogram on 4 distinct points (K <= 8 in check_family.py; K up to 150 in census_deep.py, pure integer recursion, 5 s).
4. h exactly, four independent routes: (a) `e757.core.alpha` for K <= 2; (b) OR-tools CP-SAT on the 3-AP hypergraph ("plain": proves optimality only for K <= 3, then status FEASIBLE with a weak bound; "+local cuts": per copy sum <= 7, sum <= 6 + [anchor], interior <= 6, valid because implied by the AP constraints of that copy, proves OPTIMAL for K <= 7 and not for K = 8 within 900 s); each CP-SAT witness is re-verified from the Sidon definition (all sums x+y, x<=y distinct); (c) a generic frontier dynamic program over the explicit AP hypergraph of the integers (vertex order by copy; exact for any hypergraph, at most 6 active vertices): equals 7+5K for K = 0..8; (d) python-sat/CaDiCaL on a direct sum-collision encoding (clause per relation a+b=c+d) with a totalizer cardinality constraint: ">= 7+5K" SAT (model re-verified as Sidon) and ">= 8+5K" UNSAT for K = 0..8.
5. The page's transfer matrix, rebuilt: own DP over all 2^11 subsets T of O that avoid the nine APs; best[(anchor state, inner state)]; M[s][s'] = best - |s|; R_0 = [6,7,7,7]; R_0 (x) M = [11,12,12,12] = R_0 + 5 (a finite eigenvector check), hence R_K = R_0 + 5K and h(S_K) = max R_K = 7 + 5K for **all** K once the chain structure holds (section 5); also checked numerically for K <= 200.
6. The reference judge: `judge/judge.py` through `scripts/new_claim.py` (section 4).

## 4. Results
RESULTS_TABLE_PLACEHOLDER

## 5. A short proof for every depth K  [derived-here, unrefereed; the finite computations in it are [verified-here]]
Notation. r = 18/269, L = 27169/251 (so phi(x) = L + r(x - L)), y(x) = 251x - 27169 = 251(x - L), O° = O \ {0,269}. A point phi^j(x) satisfies 251(phi^j(x) - L) = r^j y(x).
Finite facts used (all asserted in `lemma_constants.py`): 27169 = 101*269; 269 is prime and 251, 18 are invertible mod 269; y(x) = 251x (mod 269), so y(x) = 0 (mod 269) iff x in {0,269};
the relations a+b = c+d inside O are exactly the nine APs (no parallelogram, any two share <= 1 point, none contains both 0 and 269);
**no** x1+x2 = 0 (mod 269) with x1,x2 in O° (also with x1 = x2); the only solutions of x_a + x_b = x_c (mod 269) with x_a,x_b,x_c in O° are (49,49,98) and (159,159,49).

**Lemma 1 (minimal level).** Every p in S_inf = U_j phi^j(O) has a unique representation p = phi^j(x) with j >= 0 and x in O (j = 0) or x in O° (j >= 1).
Proof. phi(0) = 101 and phi(269) = 119 are in O°, so phi^j(0) = phi^{j-1}(101), phi^j(269) = phi^{j-1}(119): a representation with x in {0,269} and j >= 1 can be lowered, so a minimal one exists. If phi^j(x) = phi^{j'}(x') with j < j' then y(x) 269^d = 18^d y(x') (d = j'-j), so 269 | y(x'), so x' in {0,269}; hence two minimal representations cannot have different levels, and equal levels give y(x) = y(x'), x = x'. QED.
Consequences: |S_K| = 11 + 9K; copy j = phi^j(O) has 9 points of minimal level j and (j >= 1) two of level j-1 (its anchors phi^j(0), phi^j(269)); copy j meets copy j+1 in exactly {phi^j(101), phi^j(119)} = {phi^{j+1}(0), phi^{j+1}(269)}, and copies j, j' with |j-j'| >= 2 are disjoint.

**Lemma 2 (all relations are APs inside one copy).** If p1+p2 = p3+p4 in S_inf with {p1,p2} != {p3,p4} then {p1,p2,p3,p4} is an AP of the form phi^J(e), e one of the nine APs of O.
Proof. Write p_i = phi^{j_i}(x_i) minimally and eps = (+,+,-,-). The L-terms cancel: sum eps_i r^{j_i} y_i = 0. Let J = max j_i. If J = 0 this is a relation in O. Let J >= 1; multiply by 269^J: sum eps_i 18^{j_i} 269^{J-j_i} y_i = 0 (*). Let T = {i : j_i = J}, m = |T|; x_i in O° for i in T. Mod 269 only T survives: sum_T eps_i x_i = 0 (mod 269).
m = 1: x = 0 (mod 269), impossible. m = 2 with opposite signs: x_i = x_k, so the two points are equal and sit on opposite sides, the relation is trivial. m = 2 with equal signs: x_i + x_k = 0 (mod 269), no solution in O°. m = 3: after moving terms, x_a + x_b = x_c (mod 269) with a,b on one side and c on the other, so (x_a,x_b,x_c) = (49,49,98) or (159,159,49): the relation reads 2 phi^J(x_a) = phi^J(x_c) + p4, so p4 = phi^J(2x_a - x_c) (phi^J is affine) = phi^J(0) or phi^J(269), and the four points are phi^J of the AP {0,49,98} or {49,159,269}. m = 4: all four are phi^J(O°); applying phi^{-J} gives a relation in O, i.e. one of the nine APs. QED.
(The page bounds the level span by ten and uses the depth-12 census; the argument above needs only O and the mod-269 table. It also matches the census: max span of any AP in minimal levels is 1 up to K = 150.)

**Corollary 3 ((4,5)-property for every K).** (a) By Lemma 2 there is no relation a+b = c+d on four distinct points, so no 4-subset has two disjoint equal-difference pairs. (b) The AP hypergraph of S_K is {phi^j(e)} (9(K+1) edges): two APs in one copy share <= 1 point (O); in copies j < j' they share <= |copy j n copy j'| points, which is 2 only for j' = j+1 and both through phi^{j+1}(0), phi^{j+1}(269), but no AP of O contains both 0 and 269. So it is linear. (c) If 4 points had <= 4 distinct positive differences, the 6 differences would fall into <= 4 classes. A class of three equal differences contains two disjoint pairs (three pairs of equal length cannot form a star or a triangle on <= 4 points), a parallelogram, excluded by (a). Otherwise there are two classes of two: each gives a 3-AP, they are different 3-subsets of the 4-set (one 3-set carries only one coincidence), so they share two points, excluded by (b). Hence every 4-subset has >= 5 distinct differences. (This reduction is checked literally for K <= 12.)

**Proposition 4 (h(S_K) = 7 + 5K).** Sidon subsets of the weak Sidon set S_K are exactly its 3-AP-free subsets (Ma-Tang Lemma 2.3, as used in judge/judge.py). By Lemma 2 and Lemma 1, a subset T is 3-AP-free iff each T n copy_j is AP-free in the nine-AP structure of O, and consecutive copies overlap in the two points whose states must agree. That is exactly the max-plus recursion R_j = R_{j-1} (x) M of section 3 item 5, and R_0 (x) M = R_0 + 5 gives R_K = R_0 + 5K (max-plus is translation-equivariant), so h(S_K) = max R_K = 7 + 5K, and the Sidon ratio (7+5K)/(11+9K) = 5/9 + 8/(9(11+9K)) decreases to 5/9. Since c* = inf_n f(n)/n <= h(A)/|A| for every (4,5)-set A (Ma-Tang Thm 1.5, as used in START_HERE), **c* <= 5/9**, and c* <= 37/65 already from S_6.

What a referee should check: (i) Lemma 1 and Lemma 2 line by line (the mod-269 reduction, the case m = 3 including the sign bookkeeping, the claim that phi^J is affine so 2 phi^J(x_a) - phi^J(x_c) = phi^J(2x_a - x_c)); (ii) the finite facts of `lemma_constants.py` by hand or by a second implementation; (iii) the 4x4 max-plus table (M and R_0) by a second implementation; (iv) the standard facts imported from Ma-Tang (Sidon iff 3-AP-free in weak Sidon sets; c* = inf f(n)/n). The depth-12 and depth-150 censuses and the h values for K <= 8 above are consistency checks of this proof, not part of it. We have NOT had this proof refereed.

## 6. Conclusion (tags)
- [community] The family, the 11+9K / 7+5K counts and the claim c* <= 5/9 are the reader's (via the site); the site's own checks and "referee" are not ours and the site calls them unreviewed by humans.
- [verified-here] For K = 0..8 the rebuilt sets are (4,5)-sets of size 11+9K with exactly 9(K+1) 3-APs and h = 7+5K (several independent exact routes agree; CP-SAT alone is not conclusive at K = 8, the frontier DP and the SAT/UNSAT pair are). K = 5 gives exactly 4/7 (32/56); K = 6 gives 37/65 < 4/7.
- [verified-here] K = 6 (65 points) JUDGE_K6_PLACEHOLDER
- [derived-here] The every-depth structure (section 5) gives h(S_K) = 7+5K and the (4,5)-property for all K, hence c* <= 5/9 [unrefereed; a referee must go through section 5].
- Not claimed: nothing about the lower bound 9/17; nothing about f(23) or small n (the family has sizes 11, 20, 29, ...; its n = 20 member has h = 12 = f(20), n = 11 has h = 7 = f(11), consistent with K54 and the table in START_HERE).

Files: data/reader_5_9_family.json; results/claims/C003-reader-5-9-K6.json, C004-reader-5-9-K7.json (if saved); this directory (build_family.py, check_family.py, census_deep.py, literal_big.py, lemma_constants.py, make_results.py, results.json, table.md, check_results.json, census_deep_results.json, literal_big_results.json, claim_K6.log, claim_K7.log, standalone_verdict_K6.txt, check_K0_8.log, set_K6.json, set_K7.json).
