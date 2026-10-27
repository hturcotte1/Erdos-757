# L028: the pendant-triple lemma PT (I11 form)

Question. SYNTHESIS.md (experiments/prover/e1hub-synthesis/) Section 5, step 3: attack the
pendant-triple lemma PT (a connected slack-1 member of C with maximum degree <= 3 has no three
pairwise non-co-transversal degree-1 vertices in three different edges), via the sub-cases
(R1a) saturated and (R1b) restriction to the saturated set S_0.

Result (certificate results/proofs/L028-pendant-triple-lemma.md, submitted, unrefereed).
PT holds, in a stronger form: for G in C connected, Delta(G) <= 3, s(G) <= 1, and I11 for all
members of C with fewer than n(G) vertices, G has no pendant b-configuration (Theorem 1).
Two new steps:
1. Degree budget. In a 3-graph with Delta <= 3 every saturated set S (e(S) = |S|-2) has
   sum_{t in S} (3 - d_{G[S]}(t)) = 6. The six attachment vertices W have G''-degree <= 2 and lie
   in the saturated set S_0 of L025 Theorem 12(j), so each contributes exactly 1: all of W has
   degree 2, S_0 = V(G''), and L025's case (R1b) is void.
2. Replacement. For non-adjacent u in A, w in B (both of degree 2),
   Q = (G'' - u - w) + pendant edge on C has tau(Q) >= tau(G'') and slack <= s(G'') - 9 < 0 with
   n(G) - 4 vertices. A vertex of degree 2 sees at most two other vertices of W, so such a pair
   exists.
Corollaries (conditional on the unrefereed L025 Theorem 10 / Corollary 11(b) and L026
Corollary 14): the I11 form of the E1-hub lemma holds; no minimal counterexample to I11 has an
E1-hub; every degree-3 vertex of a minimal counterexample has pattern (a) or (f).

Files (own code; no import of e757/, judge/ or other L0xx code; exact integer/bitmask arithmetic):
- hyp28.py: toolkit (tau by branching, transversals up to size k, linear / F7 / (P3) tests,
  saturated sets).
- lemma_tests.py: random tests T1 (pendant replacement), T2 (move), T3 (the replacement Q),
  T4 (unions of saturated sets), T5 (degree budget).
- pt_search.py: end-to-end search for configurations (A,B,C) with (i), (ii) on random class-C
  graphs and on stored lists; records their slack and checks the bound of Step 7 for every
  replacement Q.
- stored_files_slack7_12.txt: the stored cell files used by C3 (relative to
  experiments/prover/L017/out).

Exact commands (each under timeout and nice -n 10, one process) and results:
- `python3 lemma_tests.py 60 1`  -> lemma_tests_output_seed1.txt (0 failures)
- `python3 lemma_tests.py 400 7` -> lemma_tests_output_seed7.txt (0 failures)
  Totals: T1 24,854; T1C 23,912; T2 10,018; T3 631,150; T4 1,991; T5 2,681; 0 failures.
- `python3 pt_search.py random 1500 11 9 13` -> pt_search_random_output.txt:
  17,800 configurations on 875 connected class-C graphs, minimum slack 11 (prediction >= 9);
  427,200 replacements Q, 0 violations of tau(Q) >= tau, 0 of the slack bound, none negative.
- `cd ../L017/out && python3 ../../L028/pt_search.py files $(cat ../../L028/stored_files_slack7_12.txt)`
  -> pt_search_stored_output.txt: 1,746 stored classes (slack 7-12, n <= 16, Delta <= 3);
  4 configurations, all of slack 12; 96 replacements, all consistent.

Conclusion. PT is proved by hand (no computation is a proof step); the computations are tests.
What remains: refereeing; the KT analogue (PT-KT) needs the KT version of L025 Theorem 12(a)-(j);
I11 itself still needs patterns (a) and (f) (see the certificate, "What remains").
