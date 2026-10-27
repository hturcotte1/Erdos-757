# Tight (slack 0) connected class-C cells with maximum degree <= 4 (Conjecture T)

Date 2026-10-27 (started 02:47 UTC). Tags: everything below is [verified-here] as an UNREFEREED computation with the unchanged L012/L014
engine, unless marked [heuristic]. Nothing here is a certificate.

## Question
Conjecture T (kb/methods/i11_proof_plan.md): every connected member of C (linear, F7-free, e(S) <= |S|-2) with slack
3n+2m-11tau = 0 has at most 17 vertices. Known tight cells: (3,1,1), (10,7,4), (14,12,6), (17,13,7) and the empty Delta<=3 cells
(20,14,8), (21,18,9), (24,19,10). Compute the missing Delta<=4 cells (17,13,7,4), (20,14,8,4), (21,18,9,4), (24,19,10,4) and the
Delta<=3 cell (27,20,11,3) (bonus: (27,20,11,4)).

## Method
- Engine: `src/engine.py` (= L012/L014 engine.py, byte-identical), streamed driver `src/stream.py` and `src/run_cells.py` (= L014), decompositions
  `src/decomp22.py`, binaries `src/bin/*` = L014 binaries, EXCEPT `src/bin/ext_d`, which is the MAXP=640 build of the n=27 chain
  (`../20261017-2150-i11-n27/src/ext_d_maxp640.c`; differs from L012's ext_d.c only in `#define MAXP 640`; rebuilt here with `gcc -O2`,
  byte-identical to that experiment's binary; the original is kept as `src/bin/ext_d_maxp256`). The first attempt at (27,20,11,3) with the
  MAXP=256 binary stopped with the `MAXP` error (no list was written); `regress.py`: both binaries give identical output on the 36 inputs
  of the (24,19,10,4) d=4 branch (5,752 hits, md5 equal).
- Seed: CELLDIR `out/cells` hard-links every cell file found in the tarballs of L012, L013, L014, L016, in the n=27 experiment (tarball +
  out/cells) and in `../20261027-0235-cost-n28-n29/out/cells` (`cells_seed/`, 258 files, git-ignored). All FOUND lines of files that occur in
  several sources are identical (0 differences in 492 comparisons). Nothing seeded was recomputed.
- Recursion (L012 engine docstring): for a cell with m > MD = 10, branch over the degree d of a maximum-degree vertex w
  (ceil(3m/n) <= d <= Delta) and tau(X-w) = t' in {t-1, t}; X - w is a disjoint union of members of lower cells with total slack
  S' = 3(n-1)+2(m-d)-11t'; inputs = products of class counts; `ext_d` adds w with d edges; `filt` re-checks C, connectivity and tau; `canon` (nauty).
  Needs I11 for all components, i.e. for n-1 <= 26 here (L013 gives n <= 26; the top cell (27,...) has components with at most 26 vertices).
- `src/plan.py` (dry run: decompositions and input counts), `run.sh` (NPROC=1, nice 15, timeout), `collect.py` -> `results.json`,
  `lists/*.txt.gz` (the target class lists), `cells_new.tar.gz` (all 17 cell files computed here, with INFO lines).
- Independent re-verification of the non-empty lists: `verify_lists.py` (pure Python/numpy, not the engine's code): linear, F7-free (all
  5-subsets), e(S) <= |S|-2 for ALL 2^n subsets, connected, tau by exhaustive search equals the stated value, slack 0, pairwise
  non-isomorphic (output `verify_lists_output.txt`: ALL OK for the 10 and the 12 classes).
- Bonus `realize_search.py` [heuristic pruning, exact leaf test]: midpoint-labelling backtracking pruned by a random point of the solution
  space mod 2^61-1 (forced equal points or forced weak-Sidon violations; rank is exact since all minors are < 2^61), leaves via `e757.core.realize`.

## Commands
```
cd experiments/20261027-0300-tight-cells-d4
cp -al cells_seed out/cells; mkdir -p out/work     # after extracting the seed (see Method)
./run.sh 17,13,7,4            # 0.3 s
./run.sh 20,14,8,4 21,18,9,4  # 11 s
./run.sh 24,19,10,4           # 81 s
./run.sh 27,20,11,3           # first try died with MAXP (old ext_d); with the MAXP=640 build: 1097 s wall (machine load ~10)
./run.sh 27,20,11,4           # 867 s wall (bonus)
python3 collect.py; python3 verify_lists.py out/cells/cell_21_18_9_D4.txt 21 18 9; python3 realize_search.py out/cells/cell_21_18_9_D4.txt 21 60
```

## Results (classes = connected isomorphism classes; bad_tau = 0 in every branch of every cell)
| cell | classes | decompositions with nonzero inputs (class-count products) | inputs d=3 / d=4 | ext_d nodes d=3 / d=4 | s |
|---|---|---|---|---|---|
| (17,13,7,4) | **10** (6 with Delta 3 = L014's list, 4 with Delta 4) | d=3,t'=6,S'=2: (16,10,6) 16; 2x(8,5,3) 3; (6,3,2)+(10,7,4) 4; (3,1,1)+(13,9,5) 84; 2x(3,1,1)+(10,8,4) 63. d=4,t'=6,S'=0: 2x(3,1,1)+(10,7,4) 5 | 170 / 5 | 3.6e5 / 4.9e5 | 0.2 |
| (20,14,8,4) | **0** | d=3,S'=2: 174 inputs (only (19,10,7,4)=0 as new subcell); d=4,S'=0: 3x(3,1,1)+(10,7,4) 5 | 174 / 5 | 1.6e6 / 2.6e6 | 1.6 |
| (21,18,9,4) | **12** (0 with Delta 3; all Delta 4, degree sequences 444333333322222222221 (3 classes) and 443333333332222222221 (9 classes)) | d=3,S'=2: (20,15,8) 953; (10,7,4)+(10,8,4) 252; (8,5,3)+(12,10,5) 298; (6,3,2)+(14,12,6) 2; (3,1,1)+(17,14,7) 1708 -> 0 hits in C. d=4,S'=0: 2x(10,7,4) 15; (3,1,1)+(17,13,7) 10; 2x(3,1,1)+(14,12,6) 11 -> all 12 classes | 3213 / 36 | 4.1e6 / 1.6e7 | 9.5 |
| (24,19,10,4) | **0** | d=3,S'=2: 3773 inputs, 252 hits in C, none connected tau=10; d=4,S'=0: (3,1,1)+2x(10,7,4) 15; 2x(3,1,1)+(17,13,7) 10; 3x(3,1,1)+(14,12,6) 11 -> 5,752 hits in C, none connected | 3773 / 36 | 2.9e7 / 6.4e7 | 81 |
| (27,20,11,3) | **0** | d=3,t'=10,S'=2: 23 decompositions, 3865 inputs, 1,424 hits in C, none connected with tau 11 | 3865 | 1.0e8 | 1097 wall |
| (27,20,11,4) [bonus] | **0** | d=3 branch identical to the line above; d=4,S'=0: 9 decompositions, 36 inputs, 22,924 hits in C, none connected | 3865 / 36 | 1.0e8 / 2.1e8 | 867 wall |
Full per-branch data: `results.json`. New subcells computed on the way (all in `cells_new.tar.gz`): (19,10,7,4)=0 (direct), (22,11,8,4)=0,
(23,15,9,4)=0, (25,12,9,4)=0, (26,16,10,4)=0, (25,14,9,3)=0, (26,17,10,3)=0, (23,11,7,2)=21, (24,13,8,2)=288, (24,15,9,2)=0, (25,15,9,2)=2, ...
Consistency: the Delta<=3 lists are contained in the Delta<=4 lists ((17,13,7): 6 in 10; (21,18,9): 0 in 12; (24,19,10): 0 in 0); the d=3
branch counters of (27,20,11,4) equal those of (27,20,11,3).
Control run (engine on cells already known, recomputed with their files deleted): see "Control" below.

## Bonus: realizability of the new tight graphs [heuristic pruning; leaf test exact]
- (17,13,7,4): all 10 classes realize as 17-point (4,5)-sets with exactly these 3-APs (so h = 10 = f(17); `realize_search_output.txt`).
- (21,18,9,4): none of the 12 classes has any midpoint labelling surviving the pruning (0 leaves), so none is the AP hypergraph of a
  (4,5)-set, even allowing extra forced APs. So these 12 tight graphs do not give a 21-point (4,5)-set with h = 12. They do show the
  abstract class C has tight connected graphs with 21 vertices.

## Conclusion
- **Conjecture T is false for the abstract class C once Delta = 4 is allowed**: cell(21,18,9,4) has 12 classes (independently verified to be connected
  members of C with n=21, m=18, tau=9, slack 0). They are the d=4 extensions of 2x(10,7,4), (3,1,1)+(17,13,7) and 2x(3,1,1)+(14,12,6). With
  Delta <= 3 the bound n <= 17 still holds on the tested range ((20,14,8), (21,18,9), (24,19,10), (27,20,11) empty).
- Tight connected graphs with Delta <= 4 exist for n = 3, 10, 14, 17, 21 and the cells (20,14,8), (24,19,10), (27,20,11) are empty (Delta <= 4). Other slack-0
  shapes (n,m,tau) with n <= 27 were not recomputed here (e.g. (25,23,11,4), see next item).
- Relevance for f(25): the record cell (25,23,11,4) has d=4 branch built from tight pieces (n-1=24, m-4=19: (21,18,9)+(3,1,1) -> 12 inputs, (14,12,6)+(10,7,4) etc.),
  now computable; the remaining missing subcells for it are (16,12,6,3), (17,15,7,3), (18,10,6,3), (19,13,7,3), (20,16,8,3), (21,11,7,3), (21,19,9,3),
  (22,14,8,3), (23,17,9,3), (24,20,10,3) (about 2.5e5 inputs by plan.py).
- Status: unrefereed computation; same engine as L012-L016 (referee ACCEPTed there), plus the MAXP=640 build.

## Control (engine re-run on known Delta<=4 lists)
`run_ctl.sh 19,16,8,4 22,17,9,4` with their files deleted from a hard-linked copy of the cells (`ctl/`): (19,16,8,4) = 956 classes in 107 s and (22,17,9,4) = 95 classes
in 436 s, FOUND lines identical to the seeded lists of L012 (956 and 95). Also: (17,13,7,4)'s Delta<=3 part (6 classes) equals L014's cell(17,13,7,3).

## Files
README.md, results.json, lists/cell_*.txt.gz (targets), cells_new.tar.gz (17 new cell files), src/ (engine, driver, binaries, plan.py),
src_c/ext_d_maxp640.c, run.sh, run_ctl.sh, collect.py, verify_lists.py (+ _output), realize_search.py (+ _output), regress.py. Git-ignored: cells_seed/, out/, ctl/.
