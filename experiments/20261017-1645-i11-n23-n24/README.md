# I11 (11 tau <= 3n + 2m) on the class C for n = 23 and n = 24 (and, as a bonus, n = 25)

Date: 2026-10-17. C = linear, F7-free 3-graphs with e(S) <= |S|-2 for all |S| >= 2 (L007-L012).
Tags: everything below was computed here with exact integers / the L012 programs and is [verified-here] **as a computation**; it has NOT been
refereed. Nothing here is a statement about (4,5)-sets beyond "I11 holds on C".

## Question
Does I11 hold on C for n = 23, then n = 24, by the window-cell induction of L011/L012 using the L012 prover engine?

## Method
1. `arith.py` (exact integers). A minimal violator H (n vertices, slack s = 3n+2m-11 tau < 0) is connected (slack is additive over components,
   an isolated vertex has slack 3, smaller components satisfy I11 by induction). For a vertex v of degree d >= 1, H-v lies in C with
   (n-1, m-d, tau'), tau' in {tau-1, tau}, slack(H-v) = s-3-2d+11(tau-tau'). tau' = tau would need s >= 3+2d > 0, impossible; tau' = tau-1
   needs d <= floor((s+8)/2) for EVERY vertex, so Delta <= dmax = floor((s+8)/2), and 3m <= dmax*n is necessary. Cells considered: connected
   (n <= 2m+1), 1 <= tau <= m <= n-2, K8 (17 tau <= 5n+3m), s < 0.
2. For every violator cell not excluded by counting, `engine.cell(n, m, tau, dmax)` (the L012 engine, unchanged) lists all connected members of C with
   exactly those parameters and Delta <= dmax. I11 at n holds on C iff all these cells are empty (minimal violators are connected, have exact tau,
   and Delta <= dmax by step 1; the engine's recursion uses I11 at <= n-1, which is available by induction: L011 for n <= 22, then this run).
3. Cross-checks (step 5 of the spec).

## Changes to the L012 code
None. `engine.py`, `decomp22.py`, `route.py` are byte-identical copies (`diff` in the log below); `bin` is a symlink to `../prover/L012/bin`.
Checked: the decomposition generator is generic in N: `engine.pieces(N,S)` calls `decomp22.slack_cells(N,S)`, which lists every connected (n,m,tau) with
n <= N, m in [n//2, n-2], tau <= m, K8 and slack in [0,S]; there is no hard-coded limit of 21 vertices anywhere in the code (the
"at most 21 vertices" sentence is only in the docstring/proof text for n = 23). The needed hypothesis "components of X-w have slack >= 0" holds because
they have <= n-1 vertices and I11 holds there (n = 23: L011; n = 24: the result below for 23; n = 25: below for 24). Engine guards: tau <= m,
n <= 2m+1, m <= n-2, K8; MD = 10 (m <= 10 by direct `enum_conn`, m >= 11 by vertex re-insertion); every `ext_d` call raises on bad_tau != 0.

## Results
### Arithmetic (arith_output.txt, arith_results.json)
Open violator cells after the counting exclusion:
- n = 23: (23,13,9) Delta<=2 (s=-4); (23,14,9) Delta<=3 (s=-2); (23,20,10) Delta<=3 (s=-1). Excluded by counting: (23,19,10) (s=-3, dmax 2, 3m=57>46).
- n = 24: (24,12,9) Delta<=2 (s=-3); (24,13,9) Delta<=3 (s=-1); (24,18,10) Delta<=3 (s=-2). Excluded: (24,17,10) (s=-4, 3m=51>48).
- n = 25: (25,16,10) Delta<=2 (s=-3); (25,17,10) Delta<=3 (s=-1); (25,22,11) Delta<=3 (s=-2). Excluded: (25,15,10), (25,21,11).
- Acceptance: `compare_arith23.py` ALL OK: slack, degree bound and the slacks of H-v for m = 19, 20 (and 21, a non-violator) agree with
  `../prover/L012/arith23_output.txt`.

### Engine (every top-level cell empty; bad_tau = 0 in all calls; `cells_table.tsv`: 125 cells touched by the n = 23, 24 runs, 34 by recursion)
| cell (n,m,tau,Delta) | classes | seconds |
|---|---|---|
| (23,13,9,2) | 0 | 0.5 |
| (23,14,9,3) | 0 | 3.0 |
| (23,20,10,3) (recomputation of L012 Step 4) | 0 | 329.8 |
| (24,12,9,2) | 0 | 0.0 (all subcells present from the n=23 run, loaded) |
| (24,13,9,3) | 0 | 0.1 |
| (24,18,10,3) | 0 | 3.4 |
| bonus (25,16,10,2) | 0 | 0.6 |
| bonus (25,17,10,3) | 0 | 4.7 |
| bonus (25,22,11,3) | 0 | 673.7 (its subcell (24,19,10,3): 0 classes, 666.1 s) |

(23,20,10,3) reproduces L012 Step 4 exactly: sub-cells (22,17,9,3) = 37 classes, (19,16,8,3) = 227, 864 inputs, 84 F7-free extensions with tau >= 10,
none in C. Seconds are wall time at NPROC=3 including nested sub-cells. Per-cell counts and times: `cells_table.tsv` (n = 23, 24 runs) and
`results.json` (all); the n = 25 bonus cell files are in `cells25.tar.gz` (150 cells, 51 by recursion; bad_tau 0).

### Step 4 (n = 25): `step4_n25_cells.py`, `step4_n25_output.txt`
One recursion level of the engine for each open n = 25 cell: (25,16,10,2): branch d=2, tau'=9, S'=1, 11 decompositions, 12 component cell types, 1 not yet
computed at the n=23/24 stage ((24,14,9,2)); (25,17,10,3): d=3, tau'=9, S'=1, 11 decompositions, 12 types, new (18,12,7,3), (21,13,8,3), (24,14,9,3);
(25,22,11,3): d=3, tau'=10, S'=0, 5 types, new (21,18,9,3), (24,19,10,3). The bonus run above then computed everything (about 21 min).

### Step 5: cross-checks
- Known counts reproduced by the engine (direct route): cell(12,10,5,3) = 149, cell(10,7,4,3) = 4.
- Recursion (MD=10) versus direct enumeration (MD=15: enum_conn + filt + canon), compared as sets of nauty canonical forms
  (`crosscheck.py`, `crosscheck_results.jsonl`): (17,11,6,2) 114 = 114, (21,11,7,2) 36 = 36, (20,12,7,2) 38 = 38, (20,11,7,3) 45 = 45 (Delta=3),
  (20,11,7,2) 1 = 1, (19,12,7,2) 1 = 1: all EQUAL, all non-empty. Not done: (15,11,6,3) and (14,12,6,3) (direct enumeration over 14 min, stopped).
  Caveat: these are cells with n <= 21; the cells at n = 22..25 are validated only through the engine's general validation in L012 (C6) and
  by the agreement with L012 on (22,17,9,3), (19,16,8,3), (23,20,10,3).

## Conclusion
- I11 holds on C for n = 23: **YES** [verified-here; computation, unrefereed; relies on L011 (I11 for n <= 22), the engine, and nauty canonical forms]. The three
  open cells are empty and (23,19,10) is excluded by counting.
- I11 holds on C for n = 24: **YES** [verified-here; same status; also relies on the n = 23 result].
- Bonus: I11 holds on C for n = 25: **YES** [verified-here, same status; relies on n = 24]. This was not requested; the n = 25 cells ran in 21 min.
- Consequence if accepted [derived-here]: 11 tau <= 3n+2m for n <= 25; the arithmetic of `arith23.py` (d) applies (the n = 25 record cell (25,23,11) has s = 0).

Files: arith.py, arith_output.txt, arith_results.json, compare_arith23.py, run_cells.py, step4_n25_cells.py, step4_n25_output.txt, step4_n25_cells.json,
run_n25_bonus.sh, crosscheck.py, crosscheck_results.jsonl, collect.py, make_results.py, cells_table.tsv, results.json, run.sh, cells25.tar.gz;
logs and cell files in out/ (git-ignored).
