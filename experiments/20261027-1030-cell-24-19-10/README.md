# Re-certification of cell(24,19,10,3) = EMPTY

Date 2026-10-27 (10:2x UTC). Request: SYNTHESIS.md (experiments/prover/e1hub-synthesis) section 5, step 5.
Tags: [verified-here] (computation reproduced); the covering certificate is L013 (K57), ACCEPTED x3.

## Question
Is cell(24,19,10,3) = {connected members of C (linear, F7-free, e(S) <= |S|-2) with n=24, m=19, tau=10, Delta <= 3; I11 slack
3n+2m-11tau = 72+38-110 = 0} empty, and what exactly establishes it? (Used by L026 Thm 12(f)/(k1) and the judge's section 4.1.)

## Which runs establish it (answer)
1. **Accepted certificate: L013 (results/proofs/L013-i11-on-C-n-le-26.md, K57, referee ACCEPT x3).** The cell is one of the "five
   recursion-only empty sub-cells" of L013 C9 (with (21,18,9,3), (23,15,9,3), (24,14,9,3), (25,18,10,3)), named load-bearing, and used in
   L013 Step 6.3 (the cell (25,22,11,3)). L013's own cell list: experiments/prover/L017/out/L013/cells/cell_24_19_10_D3.txt (INFO line only,
   0 FOUND lines, md5 8c7a7253342b772f0612da218c52c57c). Two referees (reviews L013...20261017T195830Z.md lines 117-124, 221, 253 and
   ...T214751Z.md lines 101, 181) re-derived it with their OWN engines (A6(b)); numbers match: 3,773 inputs, 1,380 F7-free hits, 252 in C,
   0 connected.
2. Earlier run of the same recursion: experiments/20261017-1645-i11-n23-n24 (bonus (25,22,11,3): subcell (24,19,10,3) 0 classes, 666 s).
3. Delta <= 4 version (stronger statement; UNREFEREED): experiments/20261027-0300-tight-cells-d4 cell(24,19,10,4) = 0 (3,773 d=3 inputs plus
   36 d=4 inputs; 81 s), recomputed from refereed seeds only in experiments/20261027-0340-induction-n28-n29-f25 (PROVENANCE_25_23_11.md:
   3,809 inputs, 65.4 s). Delta <= 3 is a sub-case, consistent (0 in 0).
4. L021 (K71) Theorem 7 does NOT enumerate this cell. It reads the stored refereed L013 list (scan_cells_output.txt line 32: "(24,19,10)
   s=0 A=-7 -> D3 list, 0 graphs L013/cells/cell_24_19_10_D3.txt"; closure_output.txt line 32: 0 graphs). So L021's coverage is L013's.
   The kt-cells run (closure2_output.txt) also cites "refereed L017/out D3 0 classes".

So emptiness rests on the accepted L013 certificate (plus the stored refereed list), NOT on unrefereed engine runs alone; the d4 run is only
a corroborating Delta <= 4 extension.

## Method of the re-run here
Completeness argument = L012/L013 Lemma E' (engine docstring): for X in the cell and w a vertex of maximum degree d (ceil(3*19/24) = 3 <= d <= 3),
X-w lies in C (heredity), has 23 vertices, 19-d edges, tau(X-w) = t' in {9,10}; every component has I11 slack >= 0 (L013 Thm 1, n <= 26), so
S' = 3*23+2(19-d)-11t' >= 0. t' = 10: S' = -9... <0, impossible; only d=3, t'=9, S'=2. Components are members of lower cells with Delta <= 3,
total slack 2: 12 decompositions (engine.decompositions(23,16,2)); input = multiset of component-class choices; ext_d adds w with 3 edges
(pairwise disjoint pairs, not creating forbidden structure), filt re-checks C, connectivity and tau, canon dedups.
- Engine: L012/L013/L014 engine.py byte-identical (src/engine.py), L014 streamed driver (stream.py, run_cells.py, decomp22.py), binaries
  src/bin = L014 (ext_d = the original MAXP=256 build `ext_d_maxp256`; checksums_code.txt).
- Seeds: ONLY the refereed L012, L013, L014 cell lists (experiments/prover/L017/out/{L012,L013,L014}/cells, 196 distinct files), with
  cell_24_19_10_D* deleted beforehand. Nothing else; no list from the unrefereed d4/cost-study/kt-cells/0340 runs.
- Input lists used (classes): (23,16,9)=178, (11,6,4)=0, (12,10,5)=149, (10,8,4)=63, (13,8,5)=0, (10,7,4)=4, (13,9,5)=84, (9,4,3)=1, (14,12,6)=2,
  (8,5,3)=2, (15,11,6)=19, (6,3,2)=1, (17,13,7)=6, (3,1,1)=1, (20,15,8)=953, (17,14,7)=1708 (run_output.txt).

## Command
```
cd experiments/20261027-1030-cell-24-19-10   # src/ copied from 20261027-0300-tight-cells-d4/src, ext_d := ext_d_maxp256
# out/cells <- refereed L012+L013+L014 lists minus cell_24_19_10_*
CELLDIR=$PWD/out/cells ENGINELOG=$PWD/out/engine.log WORKDIR=$PWD/out/work PROGRESS=$PWD/out/progress.jsonl NPROC=1 MD=10 \
  nice -n 15 python3 src/run_cells.py 24,19,10,3          # 95 s wall (machine load ~10)
```

## Result
cell(24,19,10,3) = 0 classes. Branch d=3, t'=9, S'=2: 12 decompositions, 3,773 inputs (178 + 336 + 2 + 38 + 6 + 953 + 252 + 298 + 2 + 1708 + two with
an empty factor), bad_tau 0, 29,007,573 ext_d nodes, 1,380 F7-free hits, 252 hits in C, none connected (filt: survivors 252, survivors_connected 0).
All counters are IDENTICAL to the L013 INFO line (inputs 3773, max_min_covers 2799, nodes 29007573, hits_F7free 1380, hits_in_C 252).
Files: cell_24_19_10_D3_rerun.txt (INFO line, 0 FOUND), run_output.txt, engine.log, results.json, checksums_code.txt, src/.

## Caveats
Same engine as the certificate (re-run, not an independent engine); independence comes from the L013 referees' own engines. Completeness of the
recursion depends on L013 Thm 1 (I11 for n <= 26) and Lemma E'.
