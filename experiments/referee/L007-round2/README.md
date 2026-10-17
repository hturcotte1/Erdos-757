# Referee L007, round 2 (scratch folder)

Independent checks of results/proofs/L007-no-nonsaturated-extremal-14-point-sets.md. Nothing outside this folder
was modified (the authors' scripts that write files were copied here and run with this folder as cwd).

- arith.py: Steps 1, 3, 4 arithmetic (direct enumeration of tau values, no floor formulas).
- rerun/: authors' C sources recompiled here; re-runs of C1, C2, C4, C5 (enum_conn), C6.
- build_ext_input.py: own parser/builder of the 796-graph extension input from the re-run outputs.
- f7_ref.py: two definitional F7 detectors (all 7! relabellings; networkx subgraph monomorphism), with controls.
- test_their_f7.py: the authors' two F7 detectors vs mine (1,800 graphs).
- lemmaF_check.py: Lemma F exhaustively; F7 is a maximal linear 3-graph on its 7 points.
- bf_ref.c, bf/: own labelled brute force (n <= 9), tallies (m, tau, Delta, hasF7).
- sat_ref.py: SAT decision (pysat CaDiCaL 1.5.3) of cells of connected linear 3-graphs; no canonical labelling.
- validate_sat.py: SAT vs brute force, 1,456 instances (n <= 9) for each connectivity mode.
- run_window_sat.py, run_12_9_5.py: the six window cells of Lemma A by SAT.
- dual_13_7.py, dual_bf.c: Delta <= 2 subcases via the dual graph (tau(H) = m - nu(G*)).
- run_route1_sat.py: Route I by SAT without enumerated lists (case (i) and case (ii)), with positive controls.
- run_route2_sat.py: Route II by SAT (n=14, m=11, tau>=6, Delta<=3, F7-free), with positive control.
- canon_branch_test.py, d14_check.py: empirical test of Lemma D (canonical labelled copies are output).
- witness_check.py: Step 7 witnesses from the definitions (subset brute force and CP-SAT).
- c0/: re-run of the C0 brute-force validation (bf_cells, compare_bf.py).
