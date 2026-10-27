# Provenance of the new cell lists (n <= 27, connected members of C, Delta <= 3)

Unrefereed computation [verified-here as a computation]; written 2026-10-27. Folder: experiments/20261027-0730-kt-cells.
Cell semantics (L012 `engine.py`, byte-identical copy in `src/`, md5 in README): cell(n,m,t,3) = canonical representatives (one per isomorphism
class, nauty `canon`) of the CONNECTED members of C (linear, F7-free, (P3) e(S) <= |S|-2) with n vertices, m edges, tau exactly t, maximum degree <= 3.

## Results (lists/ and progress.tsv)
| cell | classes | inputs (graphs extended) | ext_d nodes | seconds | decompositions per branch (d = max degree of the deleted vertex, tp = tau of X - w, S' = I11 slack of X - w) |
|---|---|---|---|---|---|
| (25,14,9,3) | 0 | 661 | 49,619,374 | 60 | d=2,tp=8,S'=8: 104 decompositions / 371 inputs; d=3,tp=8,S'=6: 42 / 290 |
| (26,17,10,3) | 0 | 11,558 | 655,329,931 | 621 | d=2,tp=9,S'=6: 92 / 57; d=3,tp=9,S'=4: 49 / 11,501 |
| (27,13,9,3) | 18 | 232 | 19,471,826 | 1,283 | d=2,tp=8,S'=12: 100 / 190; d=2,tp=9,S'=1: 4 / 1; d=3,tp=8,S'=10: 26 / 41 |
| (27,20,11,3) | 0 | 3,865 | 102,464,486 | 155 | d=3,tp=10,S'=2: 23 / 3,865 |
(Wall-clock on a machine with load 13-21 on 4 cores, nice -n 15, 1 worker process per cell, 2 cells in parallel.)
All four were computed here from the refereed seeds (see "Inputs"); `bad_tau = 0` for all.  Cells used from other folders, NOT recomputed
here (they are all EMPTY and enter KT only as "no connected class with A<0"):
- (26,13,9,3), (27,15,10,3), (27,16,10,3): computed by experiments/20261027-0340-induction-n28-n29-f25 (progress.tsv; 10,273,694 / 12,137,486 / 355,639,121 nodes; hits_in_C 456,835 / 5,204 / 576,080, all disconnected or failing tau);
  unrefereed.  Also scan2/closure2 read them as input lists (0 classes each).
- (27,15,10,3), (27,16,10,3) are listed in the task as "already stored" and also appear in experiments/20261027-0340-.../progress.tsv.

## D bound and why the list is the WHOLE class of connected C_3 graphs in the triple [derived-here from L016/L013]
KT concerns members of C_3 (Delta <= 3); cell(n,m,t,3) is by definition the set of connected members with Delta <= 3, so no bound D needs to be proved
beyond this definition.  For a member X with maximum degree d <= 3 (d >= ceil(3m/n)) and a vertex w of degree d: G = X - w is in C (hereditary), has n-1 vertices,
m-d edges, tau(G) = t' in {t-1, t} (deleting a vertex lowers tau by at most 1 and cannot raise it), maximum degree <= d.  Its components have at most n-1 <= 26 vertices,
so each satisfies I11 (L013 Theorem 1, refereed: n <= 26) and has slack >= 0; the slack S' = 3(n-1)+2(m-d)-11t' of G is the sum of the component slacks.

## Completeness argument (L012/L013 Lemma E' style; exactly `engine.recurse`/`stream.recurse` of L012/L014/L016)
For each (d, t') with S' >= 0, the multiset of component types (n_i,m_i,tau_i) of G is one of `engine.decompositions(n-1, m-d, S')` (the component slacks are
>= 0 and sum to S'; isolated vertices have type (1,0,0)).  Each component is isomorphic to a member of cell(n_i,m_i,tau_i,d) (connected, Delta <= d).  The d edges
at w use pairwise disjoint pairs of vertices of G, not inside an edge of G, each of G-degree <= d-1; `ext_d n-1 t' t d (d-1)` (= L016 `ext_d_fast`, Lemma B) enumerates
for every input G (disjoint union of class representatives, multisets for repeated types) all such d-edge insertions with tau(G+w) >= t (kill search: no
(t-1)-cover, with F7 / (P3) pruning, which only discards non-members of C), the output is filtered by `filt HIT n` (linear, F7-free, (P3), connected, tau as required)
and reduced by `canon n`.  Hence every member of the cell arises from one of the processed decompositions.  The `dec` lists in the INFO line of each
`out/cells/cell_*.txt` (not committed; sizes up to 600 MB for the whole folder, see .gitignore) record every processed decomposition.

## Inputs (component cells) and their provenance (deps_provenance.py -> deps_provenance.json)
Every component cell used by the decompositions was loaded from `out/cells/` of this folder.  That directory was seeded with symlinks to
experiments/20261027-0340-induction-n28-n29-f25/out/cells_ref (refereed L012-L016 lists plus lists computed there from refereed seeds) and the four target
files were removed before the run.  `deps_provenance.py` compares each component file (as a set of FOUND lines) with the extracted refereed tarball copy in experiments/prover/L017/out:
| target | component cells | identical to refereed copy | others |
|---|---|---|---|
| (25,14,9,3) | 75 | 75 | none |
| (26,17,10,3) | 82 | 79 | (24,15,9,2) = 0 classes and (25,15,9,2) = 2 classes: no refereed copy (cost-study and d4-worker runs agree, unrefereed); (25,14,9,3) = 0: computed here |
| (27,13,9,3) | 65 | 62 | (5,3,1,3) = 0, (8,4,2,3) = 3, (11,5,3,3) = 4: no refereed copy (two unrefereed runs agree) |
| (27,20,11,3) | 22 | 21 | (26,17,10,3) = 0: computed here |
The non-refereed inputs were re-derived INDEPENDENTLY of the engine here:
- indep_small.py (growth of all connected linear 3-graphs with <= 5 edges + brute force tau, Delta, (P3)): (5,3,1,3) = 0, (8,4,2,3) = 3, (11,5,3,3) = 4 (matches).
- indep_delta2.py (nauty geng on the dual graph; Delta <= 2 hypergraphs <-> simple graphs with Delta <= 3, tau = m - nu): (24,15,9,2) = 0 of 65,451 graphs, (25,15,9,2) = 2 of 193,699 graphs (matches).
- (27,13,9,3) itself: indep_27_13_9.py enumerates the 18 classes by structure (see below) and matches the engine list class by class (18/18).
- cell(26,17,10,3) = 0 and cell(27,20,11,3) = 0 were also computed by the 0340 worker (progress_chk.tsv: identical inputs and node counts) and the d4 worker (unrefereed), (25,14,9,3) = 0 by the d4 worker.
Refereed-input status of the final lists: the three empty cells are computed from refereed lists except for the independently re-derived small/Delta<=2 cells above; the 18 classes of
cell(27,13,9,3) are independently re-derived and are not an artefact of the engine.

## cell(27,13,9,3), the only non-empty new cell: structure and independent derivation
n = 2m+1: every member is a linear 3-uniform hypertree (acyclic), hence in C (F7 has cycles, e(S) <= (|S|-1)/2).  tau = nu = 9 (hypertrees are Konig), 9 disjoint edges
cover all 27 vertices ("blocks"), the 4 other edges are connectors meeting 3 different blocks; contracting blocks gives a linear hypertree T on 9 nodes with 4 edges
(4 shapes).  Delta <= 3 means each block vertex lies in at most 2 connectors.  indep_27_13_9.py enumerates the shapes and, per block, the partitions of its connectors
into parts of size <= 2 with <= 3 parts, deduplicates by networkx isomorphism, checks tau = 9 by brute force: 18 classes, all 18 isomorphic to the engine's 18.
All 18 have A = 27*27+35*13-132*9 = -4 and DEF = 4 (the nine blocks, each a copy of E_1), P = A + DEF = 0 (kt.deficiency and the brute force of validate_27_13_9.py agree).
