# Provenance of cell(25,23,11,4) = 6 classes and cell(25,23,11,3) = 0 classes

Unrefereed computation [verified-here as a computation]. Folder: experiments/20261027-0340-induction-n28-n29-f25 (written 2026-10-27, ~06:55 UTC).
Cell semantics (L012 `engine.py`, byte-identical, `checksums_code.txt`): cell(n,m,t,D) = canonical representatives (one per isomorphism class, nauty `canon`) of the CONNECTED members of C (linear, F7-free, (P3) e(S)<=|S|-2) with n vertices, m edges, tau exactly t, maximum degree <= D.

## Results
- cell(25,23,11,4): 6 classes, all with degree sequence 2 vertices of degree 1, 6 of degree 2, 13 of degree 3, 4 of degree 4 (so Delta = 4 exactly for each; all 6 come from the d = 4 branch). File `lists/cell_25_23_11_D4.txt` (header line + 6 FOUND lines), sha256 `eba390d25fc041b221683256169da610c4bb220ef9e2690a3da1b4d8f6ea9fce`; engine-format file `out/cells/cell_25_23_11_D4.txt` (git-ignored) sha256 `12990c6716f4e0352080349bfa25c3c7a32f170eeea54f2e811e353bb8d69505`; md5 of the sorted FOUND lines `c9a59d581a5978642c895a0b7a80b854` (provenance.json).
- cell(25,23,11,3): 0 classes (the d = 3 branch produces no connected member; the 6 classes above have a vertex of degree 4).
- Exact realization test of the 6 classes: `realize_rec.txt`, `realize_extra_rec.txt` (0 realizations; control A_base pattern 948/1596 in `realize_control_abase.txt`).

## The bound D = 4 and why the cell is the WHOLE class (25,23,11) [derived-here, from I11 for n <= 26 = L013 Theorem 1, refereed]
Let X be a connected member of C with (n,m,tau) = (25,23,11) (so I11 slack s = 3n+2m-11tau = 75+46-121 = 0) and let v be a vertex of degree d. Then X-v lies in C, has 24 vertices, 23-d edges, tau(X-v) = t' in {10, 11} (deleting a vertex lowers tau by at most 1, and cannot raise it). Its components have at most 24 vertices, so each has I11 slack >= 0 (L013 Theorem 1), hence the slack of X-v, S' = 3*24 + 2(23-d) - 11 t', is >= 0. For t' = 11: S' = -3-2d < 0, impossible. For t' = 10: S' = 8-2d >= 0, so d <= 4. Hence EVERY vertex of EVERY member has degree <= 4: cell(25,23,11,D) = cell(25,23,11,4) for all D >= 4 (and the lists for D = 3 are the sub-lists with max degree <= 3). Also the maximum degree d satisfies d >= ceil(3m/n) = ceil(69/25) = 3, so the branches d = 3, 4 are all.

## Completeness argument (L012/L013 Lemma E' style; this is exactly `engine.recurse`/`stream.recurse`)
Let X be a member of the cell, w a vertex of maximum degree d in {3,4}. Then G = X-w is in C (C is closed under vertex deletion), has 24 vertices, 23-d edges, tau(G) = t' = 10 (t' = 11 impossible above), max degree <= d, and slack S' = 8-2d (2 for d = 3, 0 for d = 4). Its components (isolated vertices included) have slacks >= 0 summing to S', so the multiset of component types (n_i,m_i,tau_i) is one of `engine.decompositions(24, 23-d, S')`; each component is isomorphic to a member of cell(n_i,m_i,tau_i,d) (connected, max degree <= d). The d edges at w have pairwise disjoint pairs, not inside an edge of G, with endpoints of degree <= d-1 in G (linearity and max degree d); `ext_d 24 10 11 d (d-1)` enumerates, for every input G (disjoint union of class representatives, multisets for repeated types), all such d-edge insertions with tau(G+w) >= 11 (kill search: no 10-cover of the new graph; with F7 / (P3) pruning, which is sound: pruning only discards non-members of C) and the output is filtered by `filt HIT 25 notau` (linear, F7-free, (P3), connected on 25 vertices; tau = 11 is automatic: tau(G+w) >= 11 by the kill search and <= tau(G)+1 = 11), then reduced to canonical forms by `canon 25`. Hence every member arises as a hit from one of the processed decompositions.

## Decompositions processed (counts = number of input graphs)
d = 3, t' = 10, S' = 2: 4 decompositions, 15,429 inputs (`inputs = prod C(|cell|+k-1,k)`).
| decomposition | component cells (classes) | inputs | list provenance |
|---|---|---|---|
| (24,20,10) | cell(24,20,10,3) = 2,781 | 2,781 | COMPUTED HERE (this run; 1,176,201 inputs, 2,858,943,025 ext_d nodes, 1,116 s, bad_tau 0; deps below) |
| (12,10,5)+(12,10,5) | cell(12,10,5,3) = 149 (multisets of size 2) | 11,175 | refereed L012 (also L013, L014) |
| (10,8,4)+(14,12,6) | cell(10,8,4,3) = 63; cell(14,12,6,3) = 2 | 126 | refereed L012 (L013, L014) |
| (3,1,1)+(21,19,9) | AP = 1; cell(21,19,9,3) = 1,347 | 1,347 | cell(21,19,9,3) COMPUTED HERE (977,982 inputs, 246,362,118 nodes, 244 s, bad_tau 0) |
d = 4, t' = 10, S' = 0: 3 decompositions, 67 inputs (components with D = 4).
| decomposition | component cells | inputs | list provenance |
|---|---|---|---|
| (24,19,10) | cell(24,19,10,4) = 0 | 0 | concurrent worker experiments/20261027-0300-tight-cells-d4 (unrefereed; first source in provenance.tsv); being recomputed here from refereed seeds only (progress_ref.tsv, see end of file) |
| (10,7,4)+(14,12,6) | cell(10,7,4,4) = 5; cell(14,12,6,4) = 11 | 55 | refereed L012 (L014) |
| (3,1,1)+(21,18,9) | AP = 1; cell(21,18,9,4) = 12 | 12 | first computed by the cost study (experiments/20261027-0235-cost-n28-n29) and the d4 worker (both unrefereed, agree); being recomputed here from refereed seeds only |

## Commands, nodes, times (cells run by `run1.py` = streamed L016 driver, `NPROC=2`, `nice -n 5`; ext_d = `src/bin/ext_d` = L016 `ext_d_fast`, md5 c7019ef4...; filt, canon, enum_conn = L012 binaries, `checksums_code.txt`)
cell(25,23,11,4) (row in progress.tsv: 15,496 inputs, 72,303,161 nodes, 48.4 s, bad_tau 0):
- d = 3: `ext_d 24 10 11 3 2 < chunk.in | filt HIT 25 notau | (connected) | canon 25`, 2 chunks; counters `graphs=15429 bad_tau=0 tg_too_small=0 searched=15429 max_min_covers=3969 nodes=4738908 hits_F7free=2738 hits_in_C=0`: all 2,738 F7-free hits are rejected by (P3), disconnection or tau (filt: total 0 survivors in C).
- d = 4: `ext_d 24 10 11 4 3 < chunk.in | filt HIT 25 notau | ...`, 1 chunk; `graphs=67 bad_tau=0 tg_too_small=0 searched=67 max_min_covers=5613 nodes=67564253 hits_F7free=2389 hits_in_C=172`; filt: 172 survivors, all linear/F7-free/(P3), all connected on 25 vertices; after `canon` and removal of duplicates: 6 classes.
cell(25,23,11,3) (21.5 s, same d = 3 branch with D = 3 components; identical counters): 0 classes.
Full per-branch records are in the INFO line of `out/cells/cell_25_23_11_D4.txt` and in `out/engine.log`.

## Dependencies computed here (all with `ext_d_fast`, all `bad_tau = 0`)
cell(24,20,10,3) (d = 3 only; its own lists: cell(23,17,9,3) = 137,326 [12,544,926,050 nodes, 5,323 s], cell(20,16,8,3) = 314,639 [2,938,837,574 nodes, 1,522 s], cell(17,15,7,3) = 660,651, cell(16,12,6,3) = 540,610, cell(19,13,7,3) = 192,957, cell(22,14,8,3) = 47,353, cell(18,10,6,3) = 1,634 direct; remaining small lists refereed); cell(21,19,9,3) = 1,347. Their rows (classes, inputs, nodes, seconds, bad_tau) are in progress.tsv. They were NOT recomputed independently (no second run, no chunk-level cross-check with the Gosper build `bin/ext_d` of L012); the correctness of `ext_d_fast` rests on L016 Lemma B and its regressions (L016 C6).

## What is and is not independent
- Refereed inputs: cell(12,10,5,3), (10,8,4,3), (14,12,6,3), (10,7,4,4), (14,12,6,4) and all lists below them (L012-L016 tarballs; verified identical to the concurrent workers' copies as sets of canonical forms, provenance.tsv column 4).
- Computed here and not independently reproduced: cell(24,20,10,3), cell(21,19,9,3) and their chain. A worker's independent copy of these does not exist yet.
- Not rechecked: `canon` canonicity (not load-bearing for completeness, L012 editorial note).

## Update (recompute from refereed seeds only; `run_ref.sh`, CELLDIR out/cells_ref = refereed lists + lists computed here, no list of the cost study or the d4 worker; `progress_ref.tsv`)
- cell(21,18,9,4): 12 classes (3,249 inputs, 20,170,922 nodes, 13.0 s, bad_tau 0), identical as a set of canonical forms to the cost-study/d4-worker list.
- cell(24,19,10,4): 0 classes (3,809 inputs, 93,344,329 nodes, 65.4 s, bad_tau 0, hits_in_C 6,004 none of them a connected member), same as the d4 worker.
So every list entering cell(25,23,11,4) is either refereed (L012-L016) or computed here from refereed seeds; the only lists without an independent second computation are cell(24,20,10,3) and cell(21,19,9,3) (and the chain below them, see above).
