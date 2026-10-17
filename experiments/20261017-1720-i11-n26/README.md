# I11 (11 tau <= 3n + 2m) on the class C for n = 26, and what n = 27 would need

Date: 2026-10-17. C = linear, F7-free 3-graphs with e(S) <= |S|-2 for all |S| >= 2 (L007-L012). Continues `../20261017-1645-i11-n23-n24/`.
Tags: all facts below were computed here with exact integers and the unchanged L012 engine; they are [verified-here] **as a computation**, NOT refereed.

## Question
(a) Does I11 hold on C for n = 26, given it holds for n <= 25 (1645 folder; relies on L011 for n <= 22)? (b) What exactly does n = 27 need?

## Method
Same as the 1645 folder (its README, "Method"): minimal violator is connected, has Delta <= dmax = floor((s+8)/2) and 3m <= dmax*n; for every
open violator cell the engine `engine.cell(n,m,tau,dmax)` lists all connected members of C with exactly these parameters. I11 at n holds iff all are empty.
`engine.py`, `decomp22.py` are byte-identical copies of the 1645 files (`diff` in run.sh printed nothing; verified again in this session). `bin` -> `../prover/L012/bin`.
Seeding: `out/cells` was filled with the 125 cell files of the 1645 `out/cells` plus `cells25.tar.gz` (150 files, a superset): 150 seeded files (`seed_cells.txt`);
the engine prints `(loaded)` for them (176 `loaded` lines in out/engine.log); only 17 new cells were computed (`new_cells.txt`, `cells_table.tsv`, tarred as `cells26.tar.gz`, 7 KB).
Runs at `nice -n 19`, NPROC=2, `timeout 3600` per top-level cell (never approached).

## Step 1: arithmetic (arith.py -> arith_output.txt) [verified-here]
n = 26 open cells: (26,14,10) s=-4 Delta<=2; (26,15,10) s=-2 Delta<=3; (26,21,11) s=-1 Delta<=3. Excluded by counting: (26,19,11) (s=-5, dmax 1, 3m=57>26),
(26,20,11) (s=-3, dmax 2, 3m=60>52). This is exactly the expected set. Hand check of s = 3n+2m-11 tau: (26,21,11): 78+42-121 = -1; (26,15,10): 78+30-110 = -2;
(26,14,10): 78+28-110 = -4 (all agree with arith_output.txt; K8: 17*10=170 <= 130+42=172 and 17*11=187 <= 130+63=193 so they are in the window).

## Step 2: decompositions the engine uses for n = 26 (step2_n26_output.txt, step2_n26_cells.json) [verified-here]
For every cell the only branches with S' >= 0 are those with tau' = tau-1 (the tau' = tau branch has S' < 0). Components are (n_i,m_i,tau_i) of slack in [0,S'] (isolated vertex slack 3).
- (26,14,10), Delta<=2: d=2 only (ceil(3m/n)=2), tau'=9, remainder (25,12) slack 0: 6 decompositions: [(25,12,9)]; [(3,1,1),(22,11,8)]; [2x(3,1,1),(19,10,7)]; [3x(3,1,1),(16,9,6)]; [4x(3,1,1),(13,8,5)]; [5x(3,1,1),(10,7,4)]. New component cell: (25,12,9,2). Result: 0 inputs (every needed cell is empty).
- (26,15,10), Delta<=3: d=2: remainder (25,13) slack 2, 19 decompositions (single (25,13,9), two- and three-component types over (3,1,1),(6,3,2),(8,5,3),(9,4,3),(11,6,4),(13,8,5),(14,7,5),(16,9,6),(17,8,6),(19,10,7),(22,12,8), ...);
  d=3: remainder (25,12) slack 0, the same 6 decompositions as above. New component cells: (25,12,9,3), (25,13,9,2); 22 of the 24 distinct component cells were already seeded.
- (26,21,11), Delta<=3: d=3 only, tau'=10, remainder (25,18) slack 1, 9 decompositions: [(25,18,10)]; [(12,10,5),(13,8,5)]; [(11,6,4),(14,12,6)]; [(10,7,4),(15,11,6)]; [(8,5,3),(17,13,7)];
  [(3,1,1),(22,17,9)]; [(3,1,1),(10,7,4),(12,10,5)]; [(3,1,1),(8,5,3),(14,12,6)]; [2x(3,1,1),(19,16,8)]. New component cell: (25,18,10,3) only (11 of 12 seeded).
Beyond these top-level lists the engine recursion itself needed 10 further new cells below n = 25 (see cells_table.tsv).

## Step 2: engine results
| cell (n,m,tau,Delta) | classes | seconds (wall, nested sub-cells included) |
|---|---|---|
| (26,14,10,2) | 0 | 0.1 |
| (26,15,10,3) | 0 | 0.8 |
| (26,21,11,3) | 0 | 295.4 (sub-cell (25,18,10,3): 0 classes, 264.6 s; 14,340 ext_d inputs, 260M nodes, 44,913 F7-free hits, 41,540 in C, none connected with exact tau; top branch d=3,tau'=10: 952 inputs, 120 F7-free hits, 0 in C) |

All 17 new cells: bad_tau = 0 in every `ext_d` call (summed per cell in cells_table.tsv; engine raises on bad_tau != 0; `grep "bad_tau': [1-9]" out/engine.log` empty).
The only non-empty new cells are (23,13,8,2) (12 classes) and (22,11,7,2) (52 classes): non-violator cells (slack 7 and 11), as expected. Seeded counts are reloaded by the engine, not recomputed.

## Step 3: n = 27 (arithmetic only; step3_n27_output.txt, step3_q14_output.txt) [verified-here]
Open violator cells n = 27 (arith_output.txt): (27,13,10) D<=2 s=-3; (27,14,10) D<=3 s=-1; (27,18,11) D<=2 s=-4; (27,19,11) D<=3 s=-2; (27,25,12) D<=3 s=-1.
Excluded by counting: (27,23,12), (27,24,12).
Cell (27,25,12), Delta<=3 (3m = 75 <= 81, so d = ceil(75/27) = 3 is forced for the deleted maximum-degree vertex): only tau' = 11 is possible (tau' = 12 gives S' = -10);
remainder (26,22) with slack S' = 3*26+2*22-121 = 1; exactly 3 decompositions:
1. [(26,22,11)] (slack 1; connected, new cell (26,22,11,3));
2. [(12,10,5), (14,12,6)] (slacks 1, 0; both seeded cells);
3. [(23,21,10), (3,1,1)] (slacks 1, 0).
**Answer: YES, [(23,21,10),(3,1,1)] is one of them.** The cell (23,21,10) with Delta <= 3 (slack 3*23+42-110 = 1, connected, h = 13) is exactly the open degree-3 case of the
23-point record cell (kb/open_questions.md Q14). The component types needed for (27,25,12) are therefore (3,1,1), (12,10,5), (14,12,6) (seeded) and the two NOT computed
cells (23,21,10,3) and (26,22,11,3). The engine's branches for them (arithmetic only): (23,21,10): d=3, tau'=9, remainder (22,18) slack 3, 5 decompositions; (26,22,11): d=3, tau'=10,
remainder (25,19) slack 3, 15 decompositions. Without deciding cell (23,21,10,3) (Q14), the n = 27 step of the induction cannot be completed: the class [(23,21,10),(3,1,1)] feeds the cell
(27,25,12). Every other open n = 27 cell is lower in the window ((27,13,10), (27,14,10), (27,18,11), (27,19,11)) and needs only component cells with m <= 16 at n <= 26 (new: (26,16,10,3), (25,12,9,2) and
others listed in step3_n27_output.txt); I did not run them (engine not run for n = 27 by spec).
Caveat: this shows the cell (23,21,10,3) is a needed input of the recursion for (27,25,12); I did not prove that a nonempty (23,21,10,3) would actually produce a violator.

## Conclusion
**I11 holds on C for n = 26: YES** [verified-here; computation, unrefereed; relies on I11 for n <= 25 (1645 folder, L011 for n <= 22), the unchanged L012 engine, ext_d and nauty canonical forms].
The three open cells (26,14,10,2), (26,15,10,3), (26,21,11,3) are empty and (26,19,11), (26,20,11) are excluded by counting. Seeded-cell results are reused, not independently re-derived.
**n = 27** needs the open cell (23,21,10,3) (Q14) as a component type for (27,25,12): the induction stops there.

Files: arith.py, arith_output.txt, step2_decomps.py, step2_n26_output.txt, step2_n26_cells.json, step3_n27_output.txt, step2_n27_cells.json, step3_n27_q14.py, step3_q14_output.txt,
run_cells.py, collect.py, collect_new.py, run.sh, cells_table.tsv, results.json, results_cells.jsonl, seed_cells.txt, new_cells.txt, cells26.tar.gz; engine.py, decomp22.py (copies); logs in out/ (git-ignored).
