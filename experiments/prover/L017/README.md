# L017: structure of a minimal counterexample to I11 on C (illustrative computations)

Question. Certificate results/proofs/L017-i11-minimal-counterexample-structure.md proves a structure theorem for a
hypothetical minimal counterexample to I11 (11 tau <= 3n + 2m) on the class C, and Theorem 7 (I11 for linear 3-graphs of
maximum degree <= 2). The computations here are illustrative and falsification tests; no theorem of the certificate depends
on them. Corollary 13.3 and Remarks 13.2, 13.4 of the certificate are stated as computations (C4, C5).

Method and results (exact integer arithmetic; commands in reproduce.sh; outputs *_output.txt in this folder):
- C1 `check_lemma_m.py`: 52,662 graphs with max degree <= 3 on <= 12 vertices (nauty geng) all satisfy 11 nu >= 3 M,
  equality only for M = 0, least positive value 1 (K4 with a subdivided edge); 3,000 random linear max-degree-2 3-graphs:
  tau = m - nu(dual graph), slack = 3 n0 + 11 nu - 3|E(G)| >= 0. 0 failures.
- C2 `check_cells_u2.py`: Lemma U'' and its two-vertex form on the stored tight and slack-1 cells (3,1,1), (10,7,4),
  (14,12,6), (17,13,7), (12,10,5), (19,16,8), (22,17,9), (26,22,11): 24,151 vertex and 199,524 pair predictions, 0 failures;
  every non-co-transversal pair satisfies the pair lemma; the types of such pairs are tabulated.
- C3 `minimal_violators.py`: all connected linear 3-graphs with <= 10 vertices and tau >= floor((3n+2m)/11)+1 (L007's
  enum_conn, nauty canon); exactly 3 vertex-critical violators: F7 and two F7-free (9,8,4) graphs violating (P3); every claim
  of Theorems 1, 3, 4, 5 checked on them, 0 failures (patterns: (b) once, (a) twelve times; degree-2 case (alpha) twelve
  times; no degree-1 vertices). A run over 11 vertices (`minimal_violators.py 11 11`) was started on a machine with load
  about 15 on 4 cores; see the end of this file for its status.
- C4 `engine_decomps.py`: the engine's decompositions at the 17 top-level violator cells of L013/L016 (6 empty by Theorems
  1 and 7, 6 more by Theorem 4(iii) and the stored lists, 5 need the extension step; 19 of 64 decompositions have >= 4
  components); the tight connected cells with n <= 30 and their stored Delta<=3 class counts; the violator cells with
  s in {-1,-2} at n = 28, 29, 30 and their decompositions.
- C5 `tight_configs.py`: non-co-transversal pairs and the configuration counts of Theorem 4(iv) in the 13 tight Delta<=3
  classes: only E1 has three pairwise non-co-transversal vertices; no class has the configurations of patterns (c1), (c2),
  (d), (e), (f). Hence Corollary 13.3.
- C6 `check_lemmas_random.py`: Theorem 2 (R), (R+), (U) on 1,500 random linear 3-graphs, 0 failures.

Conclusion. All computations agree with the certificate. `hyp.py` holds the shared exact routines (transversal number by
branch and bound, enumeration of all minimum transversals, F7 test, (P3) test).

Inputs (read-only): experiments/prover/L012/bin/{enum_conn,canon}; experiments/prover/{L012,L013,L014}/cells.tar.gz,
experiments/prover/L016/cells_new.tar.gz (extracted into out/, git-ignored); nauty geng from
experiments/referee/L013-round2/out/nauty_build/geng; experiments/prover/L013/decomp22.py (imported, unchanged).
