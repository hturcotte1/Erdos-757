# Exact realizability of tight class-C patterns: (21,18,9), (25,23,11), (32,29,14) gluings, and cell (21,19,9)

Date 2026-10-27. Tags: [verified-here] = exact computation, unrefereed, reproducible with the commands below, unless marked [heuristic].

## Question
Are the 12 tight class-C hypergraphs (21,18,9,Delta<=4) (experiments/20261027-0300-tight-cells-d4) the AP hypergraph of a 21-point (4,5)-set?
Do degree-4 gluings of tight pieces give a realizable (32,29,14) pattern (a 32-point set with h = 18 would be 18/32 < 4/7)? Extra tasks: the
(25,23,11) candidates and the (21,19,9,4) cell of experiments/20261027-0340-induction-n28-n29-f25.

## Method: rexact (complete decision procedure)  [verified-here]
`rexact.py` (Python, Fractions) and `rexact.c` (C port, arithmetic mod p = 2^61-1). A realization of a 3-graph H as a (4,5)-set A (A -> vertices) gives an
injective midpoint map mu (each edge -> its middle vertex; injective by the (4,5) property, K-facts of START_HERE s.2) with 2x_mu(e) = x_a + x_c.
The search enumerates ALL injective labellings mu by backtracking over edges (BFS-like order); at each node the solution space V of the equations so
far is computed (RREF); the coordinates r_v of the generic point of V are exact. A node is cut only when one of these is FORCED on V (the corresponding
combination of the r_v is the zero vector; exact test):
 EQ: x_a = x_b;  SIDON: x_a+x_b = x_c+x_d with {a,b} != {c,d}, a != b, c != d;  NONLIN: two forced 3-APs sharing two points.
Each is a necessary condition for a (4,5)-set (distinct points, weak Sidon, linear AP hypergraph), and V only shrinks along a branch, so cuts are sound.
A leaf without a forced event is realizable: a generic (random integer) point of V is distinct, weak Sidon, with linear forced-AP set containing H,
i.e. a (4,5)-set whose AP hypergraph CONTAINS H (extra forced APs allowed; equal to H exactly when #APs = m, checked on the integer set).
What NOT-REALIZABLE certifies: no (4,5)-set whose AP hypergraph contains the edge set of H exists (a fortiori none with exactly H), assuming the code is right;
the exhaustiveness is over all injective midpoint labellings (no labelling is skipped except through the sound cuts).
Exactness of the C port: all entries are small integers, every minor involved is < 2^61-1 (Hadamard, <= 6^9.5 ~ 2.4e7 for the AP rows; the forms have entries 1..2),
so rank, nullspace and the zero-test of every form mod p coincide with those over Q. rexact_c prints a labelling for each realizable graph;
`verify_lab.py` rebuilds V over Q from that labelling, takes an integer point and re-verifies it with e757.core (is_45_set, ap_edges, alpha); for C006 a separate brute
force (all 4-subsets, DFS for the maximum Sidon subset) agrees.
Cross-check Python vs C: identical node counts and (in `all` mode) identical numbers of realizable labellings on (10,7,4) [0,210,192,210,258], (14,12,6)
[498,282,560,569,702,0,446,0,698,430,506], (17,13,7) classes 0-3 [10304,8676,10308,10308] (C also 10 classes), the 12 (21,18,9) classes (nodes 4414,1129x4,1107,1024,...),
the 4 (25,23,11) candidates, 6 (25,23,11,4) classes, 20 route-4 controls. Python took 8-90 s per n=21-25 class (loaded machine), C ~0.02 s.
Not covered: this is a computation, not a certificate; no referee; the class lists themselves are other workers' unrefereed computations.

## Positive and negative controls [verified-here]
- A_base pattern (14,12,2-rigid): 569 realizing labellings, all rigid, A_base among them (`rexact.py`, checked in this session).
- (10,7,4,4): 4 of 5 classes realizable, 1-parameter families (results_ctl_10_7_4.json). (14,12,6,4): 9 of 11 realizable, rigid (results_ctl_14_12_6.json);
  the 2 non-realizable ones (classes 5, 7) are exactly the two found by the sub-pattern embedding test. (17,13,7,4): 10/10 realizable (rexact_c; Python all-labellings for classes 0-3, dim 2; earlier heuristic run also 10/10).
- L012 route-4 (23,21,10) degree-4 classes (experiments/prover/L012/route4_classes.txt.gz): random sample of 20 (seed 0): 20/20 NOT-REALIZABLE (results_ctl_route4.json), consistent with L012's 0 realizations out of all 699.
- Engine control: C006 and the whole (21,19,9) sweep give realizable cases, so the procedure does return REALIZABLE.

## Results
1. **(21,18,9,4): all 12 classes NOT-REALIZABLE** (results_main_21_18_9.json; Python 8-44 s each, nodes 4414/1129/1107/1024/1043; also rexact_c). Every class contains one of two small
   non-realizable sub-patterns (11 vertices, 9 edges; or 14 vertices, 12 edges: obstructions.json, found by minimal edge prefixes, `obstruction.py`). So no 21-point set with h=12 comes from a TIGHT (21,18,9) pattern.
2. **(25,23,11) candidates** (experiments/falsify/i11-structure-lemmas, the 4 graphs K21_0..3; tight and verified files identical): all 4 NOT-REALIZABLE (results_25_23_11_candidates.json).
   Their 21-vertex part (vertices 0..20) is isomorphic to (21,18,9) classes 3, 9, 7, 5 (canonical forms; restriction argument: a realization would restrict to a realization of that class, which does not exist).
   **cell(25,23,11,4) list (6 classes, lists/cell_25_23_11_D4.txt of the n28-n29 worker): all 6 NOT-REALIZABLE** (results_25_23_11_D4.json; Python and C agree; nodes 1502,1502,1395,4618,4618,4449).
   So no 25-point (4,5)-set with h=14 realizes a Delta<=4 member of the (25,23,11) cell; f(25)=15 follows only if that worker's cell list is complete and the cell has no vertex of degree >= 5 (not checked here).
3. **(32,29,14) gluings (w of degree 4 over disjoint unions of tight pieces; X-w tight pieces total (31,25,13))**: the only multisets of known tight pieces (3,1,1),(10,7,4),(14,12,6),(17,13,7),(21,18,9) are
   (a) 21+10, (b) 17+14, (c) 3+14+14.
   - (a) is moot: any realization of X restricts to a realization (with possibly extra APs) of the 21-vertex component, one of the 12 non-realizable classes. Not enumerated.
   - (b) engine `glue32.py` (ext_d with MAXP=640, 110 inputs, 1.4e9 nodes, filt, canon): 480 connected hits in C, 72 classes (glue32_classes_b.txt, glue32_results_b.json). **All 72 NOT-REALIZABLE**:
     every class embeds one of the two non-realizable sub-patterns (embed_b.json; sub-pattern argument), rexact_c says NOT for all 72, rexact.py (first 15) agrees.
   - (c): see the end of this file / `finish_c.log` (job `jobc/`, restarted at 06:40 UTC; results go to glue32_results_c.json, glue32_c_rexact_c.txt). If that file is missing the job was not finished.
   Caveat: components of X-w of unknown tight shapes (e.g. a single tight (31,25,13)) and Delta >= 5 are not covered; I11 is unproven beyond n=27.
4. **cell (21,19,9,4)** (31,268 classes, m = n-2 saturated): the sweep with rexact_c is NOT complete (see results_21_19_9.json: tested/realizable counts at the time of writing, 518 tested, 413 realizable, 105 not; the job
   `out_21_19_9_full.txt` keeps running (timeout 14000 s, some classes have trees of millions of nodes); rerun `python3 finalize_21_19_9.py 300` to refresh the json and sets).
   Realizable classes: **a 21-point (4,5)-set with h = 12** exists, so **f(21) = 12** [verified-here].
   **C006** = results/claims/C006-tight-21pt-h12.json: class index 43 of lists/cell_21_19_9_D4.txt, labelling (mu, as (a,mid,c)) = see verify_realizable_21_19_9.json entry cls 43, dimension 0 (rigid),
   normalised by x -> (x - min)/gcd to the integer set {0,210,396,420,444,792,888,1374,1566,1581,1596,1758,1935,1941,2231,2301,2304,2375,2449,2521,2667}. Verified: 19 APs (= m, so the AP hypergraph is exactly the class),
   is_45_set True, independent brute force over all 4-subsets True, max Sidon subset = 12 (DFS). Judge: `JUDGE: PASS NO-IMPROVEMENT C006-tight-21pt-h12 n=21 h=12 ratio=4/7` (new_claim_21pt.log). Not a record (12/21 = 4/7).
   Sets for the first 100 realizable classes: sets_21_19_9_realizable.json (all (4,5), 19 APs, h = 12).

## Commands (all `nice -n 5`, with timeout)
```
python3 run_cell.py <cellfile> <n> <tag>      # Python rexact; ALL=0 for first-solution mode
gcc -O2 -o rexact_c rexact.c; ./rexact_c N [all] < lines        # C port
python3 run_cell.py ../20261027-0300-tight-cells-d4/out/cells/cell_21_18_9_D4.txt 21 main_21_18_9
python3 obstruction.py; python3 embed_obs.py glue32_classes_b.txt b 32
python3 glue32.py            # (b),(c),(a) gluings; glue32_c.py for (c) only
python3 cand25.py; ./rexact_c 25 < work/c25_D4.txt
./rexact_c 21 < work/cell_21_19_9.txt > out_21_19_9_full.txt; python3 finalize_21_19_9.py 300
python3 verify_lab.py work/cell_21_19_9.txt out_21_19_9.txt 21 out.json 60
cd /home/user/Erdos-757 && python3 scripts/new_claim.py --slug tight-21pt-h12 --set-file experiments/20261027-0400-realize-21-18-9/set_21pt_h12.json --notes '...'
```
Wall times (loaded machine, load 11-17): 12 (21,18,9) classes 3 min; 20 route-4 controls 12 min; 6 (25,23,11,4) classes 6 min (Python); glue32 (b) ext_d ~50 min wall; C port: 12 classes 0.3 s, 72 classes 12 s.
