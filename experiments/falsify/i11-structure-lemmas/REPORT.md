FALSIFIER: BROKEN (Conjecture T, twelve connected tight (21,18,9) graphs of C with maximum degree 4; five of them in counterexample_conjecture_T_n21.json; Lemmas U' and M HOLD-ON-DATA)

# Falsification of the three statements of kb/methods/i11_proof_plan.md

Date 2026-10-27. Class C = linear, F7-free 3-graphs with e(S) <= |S|-2 for all |S| >= 2. slack = 3n + 2m - 11 tau. Tight = connected, slack 0.
Everything is exact (integers; tau by two independent solvers); floats occur only in two search heuristics (flagged below).
Tags: [verified-here] = exact computation in this folder. Nothing here is refereed.

## Headline
1. **Conjecture T is FALSE as stated [verified-here].** There are connected members of C with slack 0 on 21 vertices
   (n,m,tau) = (21,18,9), all of maximum degree 4: 12 isomorphism classes (`tight_21_all.json`; the first five, found first, are in
   `counterexample_conjecture_T_n21.json`). Each is v + (3,1,1) + one of the ten 17-vertex tight graphs, v joined to the 20 vertices by four
   disjoint pairs. Checked independently three ways: (i) the project's own filter `experiments/prover/L012/bin/filt` (linear, F7-free, P3 =
   e(S) <= |S|-2, tau exact, connected): `filt_check_21.txt`; (ii) own Python: linearity, F7 search, brute force of e(S) <= |S|-2 over all 2^21
   subsets, connectivity; (iii) tau = 9 by C branch-and-bound and by CP-SAT (`verified_tight_21_all.json`).
   Slack = 63 + 36 - 99 = 0. (Realizability as a (4,5)-set was not tested for n = 21; m = 18 = n-3 is not saturated.)
2. **The record cell (25,23,11) is NOT empty in C [verified-here].** v + (3,1,1) + (21,18,9)-tight graph gives connected slack-0 members of C with
   (n,m,tau) = (25,23,11), Delta = 4: 3 isomorphism classes (4 graphs in `tight_25_23_11_candidates.json`, from four of the five 21-vertex comps; verified
   by `filt` (`SUMMARY ... survivors=4`), brute force over all 2^25 subsets, CP-SAT: `verified_tight_25_23_11_candidates.json`).
   So I11-slack arithmetic and the abstract class C cannot exclude a 25-point record. However none of these 4 graphs is realized by a saturated midpoint
   map: for each, all 300 choices of (min,max) and about 53,500 midpoint labelings (perfect matchings edge -> midpoint) were solved numerically; none gives a
   point set whose AP hypergraph equals the graph (`realize_fast_25.log`, `realize_fast_25.json`; control: the same script finds 569+ realizations of an
   A_base-census graph). This realizability screen uses floats (tolerance 1e-9) and is evidence, not a certificate.
3. **Lemma U' holds on all data [verified-here]**: no tight graph and no slack-1 graph has a vertex lying in every maximum independent set.
4. **Lemma M holds on all data [verified-here]**: for every connected member of C with Delta <= 2, slack = 11 nu(G) - 3 e(G) >= 0.
5. Four new tight graphs at n = 17 (Delta = 4), not in the Delta <= 3 cell (17,13,7) list (6 classes), `new_tight_17_13_7_deg4.json`. They do not contradict T (n <= 17),
   but they show the known tight list is incomplete once Delta = 4 is allowed.

## (1) Lemma U' (no universal vertex in tight graphs)
Statement tested: for K tight and every vertex x, tau(K-x) = tau(K)-1 (K-x = induced subgraph, edges through x deleted), i.e. no vertex is in every maximum independent set.
Data (cell lists from the L012/L013/L014/L016 tarballs, extracted to cells*/ and deleted again before commit; regenerate with `tar xzf`):

| set | graphs | vertices with tau(K-x) = tau(K) (universal) |
|---|---|---|
| tight (3,1,1) | 1 | 0 |
| tight (10,7,4), Delta <= 4 | 5 | 0 |
| tight (14,12,6), Delta <= 4 | 11 | 0 |
| tight (17,13,7), Delta <= 3 | 6 | 0 |
| new tight (17,13,7), Delta = 4 (this run) | 4 | 0 |
| new tight (21,18,9), Delta = 4 (this run) | 5 | 0 |
| census_n14_m12_classes.jsonl.gz (2,910 AP hypergraphs of saturated extremal 14-point sets; all slack 0, connected, in C) | 2,910 | 0 |
| A_base | 1 | 0 |
| slack-1 (8,5,3) Delta <= 4 | 2 | 0 |
| slack-1 (12,10,5) Delta <= 4 | 221 | 0 |
| slack-1 (15,11,6) Delta <= 4 | 30 | 0 |
| slack-1 (19,16,8) Delta <= 4 | 956 | 0 |
| slack-1 (22,17,9) Delta <= 4 | 95 | 0 |
| slack-1 (26,22,11) Delta <= 3 | 36 | 0 |

Distribution in slack-1 graphs: 0 universal vertices in all 1,340 graphs, hence no universal vertex of degree >= 2 (`part1_results.json`).
Every graph was re-checked: connected, in C (brute force over all subsets for n <= 22, Hall-pair criterion in C otherwise; n = 26 only the latter), slack as labelled.
Control (the property is not vacuous): in sampled cells of slack 5..8 (n <= 20) universal vertices do occur: slack 5: 5 of 228 graphs, slack 6: 14/156, slack 7: 26/256, slack 8: 5/87;
none in slack 0..4 (31, 214, 180, 172, 141 graphs) (`part1c_control.json`).
Direct test of the gluing statement: all 73,842 identifications x1 = x2 of two tight graphs from {(3,1,1), 5 x (10,7,4), 11 x (14,12,6), 6+4 x (17,13,7)}: all in C
(so F7-freeness and e(S) <= |S|-2 survive), tau(K) = tau1 + tau2 - 1 in every case, slack = 8 in every case, 0 exceptions (`part1b_glue.json`).
Result: no counterexample. (Scope: only graphs of the tight cells of n <= 17, 21 and the slack-1 cells; no claim for larger n.)

## (2) Lemma M (I11 for Delta <= 2)
Structure (derived-here, then verified): a connected H with Delta <= 2 corresponds to a connected simple subcubic graph G on m vertices (one G-vertex per H-edge, one G-edge per degree-2 H-vertex),
with n = 3m - e(G) and slack = 11 nu(G) - 3 e(G) (tau = m - nu(G)). Such H is automatically F7-free, linear, and e(S) <= |S|-2 holds (checked below).
- **Enumeration, exhaustive for n <= 14**: all connected simple graphs of max degree <= 3 on m <= 11 vertices were generated (1,1,2,6,10,29,64,194,531,1733,5524 graphs for m = 1..11: the known sequence;
  8,095 in total). n <= 14 forces m <= 9, so the 208 members with n <= 14 are complete. Independent cross-check with `experiments/prover/L012/bin/enum_conn` (Delta <= 2) + `filt` + `canon`:
  identical class count for every (n,m), n <= 14 (208 classes; `part2_crosscheck.json`). For all 8,095 graphs: tau computed on H by exact DP equals m - nu(G) (0 mismatches),
  slack = 11 nu - 3e (0 mismatches), Hall-pair class-C test passes for all; brute force over all 2^n subsets for the 208 graphs with n <= 14.
- **Minimum slack** per (n,m): `part2_minslack_table.txt`. Overall minimum 0, attained only by the single edge (3,1,1); next 1 at (8,5,3); other minima: n = 6: 2, n = 9: 2, n = 11: 3, n = 14: 3.
  Minimum over all (n,m) with n <= 14 and (n,m) != (3,1): 1. By m = |V(G)|: 0,8,2,2,1,4,3,3,5,5,5 for m = 1..11. nu(G) >= 3 e(G)/11 holds in all 8,095 cases (0 violations).
- **Dual formula**: tau = m - nu(G) holds in all cases. The formula as written in the plan, with "+ number of edges all of whose vertices have degree 1", is wrong for exactly one graph, the single edge
  (it gives 2, true tau 1); for connected H with m >= 2 that correction term is 0.
- **Random**: 120,000 connected class-C graphs with Delta <= 2, n = 15..40 (about 4,300-5,200 per n), generated as random connected subcubic G (random tree + random extra edges), exact tau by DP:
  tau = m - nu in all, slack = 11 nu - 3e >= 0 in all; minimum slack found per n: 15: 4, 16: 9, 17: 5, 18: 6, 19: 9, 20: 7, 21: 6, 22: 11, ... global min 4 (`part2_random_results.json`).
  Hill climbing (random edge moves, accept if slack not larger; 6 starts x 400 steps for each m = 8..26) reached a minimum of 3; at m = 26 only 22. This is a weak adversary (a random-walk heuristic).
- No violation. Not a proof: nu >= 3e/11 for all connected subcubic graphs is checked exhaustively only for <= 11 vertices (8,095 graphs) plus random samples.

## (3) Conjecture T
(a) Structure search (degree-4 vertex v + four disjoint pairs attached to a union Q of smaller tight graphs). Lemma: if K is tight with a degree-4 vertex v then every component of K-v is tight
(by I11 for n-1, verified for n-1 <= 27); K is tight iff every maximum independent set of Q contains one of the four pairs. Library of components: (3,1,1), 5 x (10,7,4), 11 x (14,12,6),
6 x (17,13,7, Delta <= 3), plus generated graphs. All K were tested exactly (tau, class C, connected).
- Controls reproduced: n = 10: 1 class (= the Delta = 4 (10,7,4) class); n = 14: 9 classes (= all nine Delta = 4 classes of the (14,12,6) cell); no tight graph at n = 11, 12, 13, 15, 16, 18.
- n = 17: **4 new classes** (v + (3,1,1) + (3,1,1) + (10,7,4)), n = 21: **12 classes** (v + (3,1,1) + a 17-vertex tight graph; exhaustive for this form by `src/e3plus.py`, which handles
  the cover condition exactly with bitsets over the maximum independent sets and all cross/inner pair patterns), n = 25: **3 classes** (v + (3,1,1) + a 21-vertex tight graph),
  n = 29 via K25 + (3,1,1): none (raw covers exist but all violate class C).
- Scope of the exhaustiveness: complete for every union Q with at most 5 components and n <= 18 (`part3a_runner_partial.log`: n = 5..18 all done, the single n = 19 union of six edges is skipped, and by a
  hand pigeonhole argument cannot give a tight K); minimal-cover search (`src/part3m.py`, k pairs) complete for unions with 2 components and total <= 24 vertices for k = 3 and unions with 2-3 components
  and total <= 20 vertices for k = 4 (the 232-union list was cut by the time limit after 15 unions); k = 2 complete (200 unions). For k = 4 and four components,
  and for triangle/cycle shapes with two endpoints per component, the pattern analysis `src/part3p.py` shows no cover exists (all component relations contain the all-in pattern, no unsatisfiable cycle).
  Minimal covers with k = 3 pairs: inside one 17-vertex tight graph (3 pairs inside the comp; these clusters violate class C, since {v} + comp would be an (18,16,8) member of C with slack -2, impossible by I11 at n = 18) and (3,1,1) + (3,1,1) (that is F7, not in C); no others for totals <= 24.
  Not covered: unions of two large components (e.g. (14,12,6) + (10,7,4), which would give n = 25), three or more components with total > 20, anything with Delta = 3 (K - v then has slack 2).
- Every found graph was re-verified independently (see Headline).
(b) Random/local search, 13 sizes n = 18..30, for m in {n-2, n-3, n-4} plus every m in [n-9, n-2] with 3n + 2m = 0 or 1 mod 11 (the only values allowing slack 0/1): 20,000 evaluated class-C samples per (n,m),
60,000-80,000 per n, connected class-C graphs from random growth (60% from seeds = disjoint unions of known tight/slack-1 graphs plus random class-C-preserving connecting edges) with simulated annealing on tau (`src/lsearch.c`, `run3b.sh`).
Minimum slack found per n: 18: 5, 19: 1, 20: 4, 21: 9, 22: 1, 23: 8, 24: 4, 25: 7, 26: 3, 27: 6, 28: 2, 29: 5, 30: 10. The 20 distinct graphs with slack <= 1 are all in the known cells (19,16,8) and (22,17,9)
(isomorphic to cell members). **This search is low power**: it did NOT find the tight (21,18,9) and (25,23,11) graphs that (a) proves exist (minimum slack found there 11 and 11); positive control (`poscontrol3b.log`):
unseeded it finds only the (10,7,4) tight graphs and the (12,10,5) slack-1 graphs, seeded it recovers (14,12,6), (17,13,7), (15,11,6), (19,16,8), (22,17,9) only because the seeds contain them. Treat (b) as near-uninformative.

## What this means for the plan
- Conjecture T as stated is dead; the true tight list is infinite or at least reaches n = 25 with Delta = 4 (n = 29 not reached by this construction). Do not use "tight => n <= 17" in an induction.
- The record cell (25,23,11) is inhabited in C, so a proof that f(25) = 15 must use realizability (or other structure) for these graphs, not C alone; the 4 graphs here are not realizable by a saturated midpoint map (screen above).
- Lemma D/R machinery for Delta <= 3 minimal counterexamples is unaffected (all new tight graphs have a degree-4 vertex), but "tight graphs with Delta <= 3 are finite" is untested beyond the cell lists.
- Lemma U' looks robust (it also holds for all slack <= 4 samples) and may be provable via an exchange argument; Lemma M reduces to nu(G) >= 3e(G)/11 for connected subcubic graphs G.

## Files
Scripts: `src/` (hg.py + tau.c exact tau; part1*.py Lemma U'; part2_*.py Lemma M; part3a*.py, part3m*.py, part3p.py, e3plus.py, chain_e3.py, part3f.py Conjecture T (a);
lsearch.c, run3b.sh, agg3b.py (b); verify_new.py, verify_n.py independent verification; realize_fast.py realizability screen). Data/results: `results.json` (all counts),
`counterexample_conjecture_T_n21.json`, `tight_21_all.json`, `tight_25_23_11_candidates.json`, `new_tight_17_13_7_deg4.json`, `verified_*.json`, `filt_check_*.txt`, `part3b_results.json`, `part3m_*.json`, logs.
Not committed (regenerable): extracted cell directories `cells12/13/14/16` (`tar xzf experiments/prover/L012/cells.tar.gz` etc.), `levels_cache_11.pkl` (generated by `src/part2_enum.py 11`, 210 s).
Caveats: no process ran in parallel with another of mine except short checks; CPU shared; the part3a runner and part3m runs were cut by time limits (scope stated above); (b) and the realizability screen are heuristic.
