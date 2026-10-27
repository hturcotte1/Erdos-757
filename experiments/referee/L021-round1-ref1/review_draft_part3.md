
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
