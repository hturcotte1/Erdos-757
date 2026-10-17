# Falsification of I11:  11 tau <= 3 n + 2 m   (H = 3-AP hypergraph of a (4,5)-set, tau = n - h)

**VERDICT: HOLDS-ON-DATA (no counterexample), with one derived-here reduction that goes beyond data: I11 is
proved (computer-assisted, class O below) for every hypergraph on <= 15 vertices, and the first cells where it
could still fail are (n,m,tau) = (16,14,7) and above.**  NONE-FOUND is evidence, not proof, except where a cell is
marked "exhaustive" (then it is a finite computation whose assumptions are listed).

Notation: slack = 3n + 2m - 11 tau (I11 <=> slack >= 0).  "Class O" = ordered midpoint hypergraphs: vertices 0..n-1, edges
(i<j<k) with j the midpoint, midpoint injective, linear, F7-free (so every induced S has e(S) <= |S|-2).  O is hereditary
(induced subhypergraphs), every (4,5)-set gives a member of O, Henning-Yeo (HY) 17 tau <= 5n+3m holds on O [published].
All counting is exact integer arithmetic; engines: `subsets.c` (bitmask DP over all 2^n subsets, validated against
`e757.core.alpha` on all subsets of A_base and 12b: `sanity.log`), `conn_dfs2.c` (exhaustive, see Test 5).
Tags: [verified-here] = computation in this folder; [derived-here] = argument + computation, needs referee.

## 0. Equality structure (important for any proof attempt)
Equality cases found over all data (n, m, tau): (3,1,1) single AP (and k disjoint APs: (3k,k,k)), (10,7,4), (13,8,5),
(14,12,6).  Examples: (13,8,5) = A_base minus its degree-4 point 0 (this is the disjoint union of an AP and a (10,7,4) piece,
not connected); (14,12,6) = A_base (and all 2,910 saturated extremal classes, 2,910 equality hits); (10,7,4) occurs in
the 11-/12-/14-point records and in 31,364 subsets of the 12-point census.  The 12-point records have slack 1 (full set,
tau 5, m 10) but contain equality sub-pieces.  **Exact LP (Fractions) over the union of all subset data (73 (n,m) cells,
`results_tau_max_union.json`): the polygon {(a,b) >= 0 : tau <= a n + b m on all data} has exactly three vertices
(0,1), (3/11,2/11) = I11, (3/7,0)** (`polygon.py`, `results_polygon_vertices.json`).  So I11 is the unique
"middle" vertex, determined by the two tight cells (3,1,1) and (14,12,6); the other vertex tau <= 3n/7 is the 4/7 conjecture
(stronger than I11 for dense m > 6n/7, weaker for sparse m).  Consequence of I11 with m <= n-2: h >= (6n+4)/11, i.e.
f(n) >= ceil((6n+4)/11), which equals the known f(n) for every n <= 15 and n = 17, gives f(16) = 10, f(18) >= 11, f(20) >= 12.

## 1. Test results (all: 0 violations)
| # | data | inputs | subsets checked | min slack | equality (n,m,tau) | time |
|---|---|---|---|---|---|---|
| T1 | all 2^n subsets of the 7 `small_records` sets (n=8,10,11,12,12b,12c,14) | 7 | 2^8..2^14 each | 0 | (3,1,1),(6,2,2),(9,3,3),(10,7,4) [n>=11], (13,8,5),(14,12,6) [A_base only] | <1 s |
| T2 | all 2,910 saturated 14-pt classes, all 2^14 subsets | 2,910 | 47,677,440 | 0 | (3,1,1),(6,2,2),(9,3,3),(10,7,4),(12,4,4),(13,8,5) x3,150,(14,12,6) x2,910 | 1 s |
| T3 | ALL 54,243 twelve-point classes, all 2^12 subsets | 54,243 | 222,179,328 | 0 | (3,1,1),(6,2,2),(9,3,3),(10,7,4) x31,364 | 5 s |
| T4 | lp-fit dataset (rows (n,m,tau)) | 1,333,217 | rows | 0 | (6,2,2),(9,3,3),(10,7,4),(12,4,4),(13,8,5),(14,12,6),(15,5,5) | <1 min |
| T6a | Fibonacci prefixes {2,3,5,8,..}, n=5..25 (all (4,5)); all 2^n subsets | 21 | up to 2^25 | 0 | only disjoint-AP pieces; full-set slack 2..21 (n=25: m=22,tau=9, slack 20) | 3 s |
| T6b | gluings (generic q=1000003, t=10^12; (4,5) verified): A_base+A_base (28,24,12) | 5 | whole sets | slack 0 (equality, as predicted) | A_base+12-pt: (26,22,11) slack 1; 12+12b: (24,20,10) slack 2; 12+12c+A_base (38,32,16) slack 2 | 3 min |
| x1 | one-point amalgams (A, q B reflected or not, identified at a in A, b in B; 8 pairs of record sets, 2,404 tried, 772 are (4,5)) | 772 | whole sets | 2 (A_base+11-pt record: (24,20,10)); A_base+A_base: 8 | none | 2.5 min |
| x2 | realizable classes n=6..11, all m stored (small-counts) | 72,210 | 45,831,488 | 0 | (3,1,1),(6,2,2),(9,3,3),(10,7,4) | 2 s |
| x3 | ALL (4,5) single-point extensions (new point in a new AP) of the 2,910 classes: 141,153 fifteen-point sets | 141,153 | 4,625,301,504 | 0 (whole 15-pt set: min slack 5, (15,13,6)) | as T2 | 103 s |
| x4 | ALL 1,887,566 single-point extensions of the 54,243 twelve-point classes (13-pt sets) | 1,887,566 | 15,462,940,672 | 0 | as T3 | 281 s |
| x5 | ABSTRACT census (12,10,alpha<=7): all 2,226,490 labelled class-O patterns, all subsets | 2,226,490 | 9,119,703,040 | 0 | (3,1,1),(6,2,2),(9,3,3),(10,7,4) x1,498,714 | 188 s |
| x6 | ABSTRACT census (14,12,alpha<=8): all 205,529 labelled patterns (`n14/results/post/filtered.txt.gz`), all subsets | 205,529 | 3,367,387,136 | 0 | + (12,4,4),(13,8,5),(14,12,6) x205,529 | 94 s |

(T2 equality (13,8,5) count 3,150 and (14,12,6) 2,910 are from `results_n14.json`.)  The minimum slack by subset size over x3 is in
`results_minslack_by_size_ext14.json` (size 15: 5; size 11: 1 via (11,6,4); size 8: 1 via (8,5,3)).

## 2. Test 5: the abstract class.  [exhaustive; assumptions listed]
**Reduction (derived-here, elementary):** slack and tau are additive over connected components; so a violation has a connected
spanning violating component C in O.  C satisfies HY, tau <= m, m <= n-2, n <= 2m+1.  Hence a violation exists only in
"window cells" (n,m) with lo = floor((3n+2m)/11)+1 <= min(floor((5n+3m)/17), m), n <= 2m+1.  Window cells with n <= 16:
(8,4,3) (10,6,4) (11,5,4) (12,9,5) (13,7,5) (14,11,6) (15,9,6) (15,10,6) (16,8,6) (16,13,7) (16,14,7)  [format (n,m,least violating tau)].
Every other (n,m) is safe on O by HY alone.

**Decisions (`conn_dfs2.c`, exhaustive enumeration of ALL connected linear 3-graphs with n vertices, m edges, tau >= lo — no
F7-freeness, no ordering, no midpoint condition imposed, so strictly larger than O):**
| cell | result | nodes |
|---|---|---|
| (8,4,3) (10,6,4) (11,5,4) (13,7,5) | none | 151 / 8,448 / 197 / 19,596 |
| (12,9,5) | none (agrees with L002 class-O census) | 18,326,058 |
| (15,9,6) | none | 2,459,440 |
| (15,10,6) | none | 186,011,577 |
| (16,8,6) | none | 19,144 |
| (14,11,6) | **exists in the unordered linear class, but every example contains F7** (see 3) | |
| (16,13,7),(16,14,7) | not decided here (this is f(16)); reductions in section 4 | |
Also CaDiCaL (`sat_cell.py`, ordered class O with lazy F7 cuts, exact m) proves UNSAT for (8,4,3) (0.1 s), (10,6,4) (20 s), (11,5,4) (82 s)
(CP-SAT `feasible_alpha_le` returned UNKNOWN at (10,6,4) after 60 s and after several further minutes; not used).
DFS validation: v2 (`conn_dfs2`, canonical BFS-growth, complete for connected hypergraphs) agrees with the naive v1 (`conn_dfs.c`) on
existence for a 200-cell grid (n<=10, m<=7, tau0<=5; 0 mismatches) and on the number of isomorphism classes (networkx) in 8 cells
(`isocheck.py`: e.g. (10,7,4): 6 classes; (10,6,3): 45; (9,5,3): 6); it reproduces the 159/637 labelled (13,8,5)/(10,7,4) tight graphs.
**Conclusion for n <= 13: no hypergraph in O (indeed no F7-free linear 3-graph with m <= n-2 on every subset) violates I11,
except that (14,11,6) needs the argument below.**  Table of tau_max slack for the O' and realizable cells known to the project: `abstract_table.md`
(min slack 0 at (6,2),(9,3),(10,7),(12,4),(13,8),(14,12); the only unresolved entries there are (12,9) [now closed] and (14,11) [now closed, section 3]).

## 3. Result [derived-here, needs referee]: the cell (14,11,6) is EMPTY in class O.
Let H in O with (n,m,tau) = (14,11,6) (HY gives tau <= 6; slack = -2).
1. For every v, H-v is in O with n=13, so I11 holds for it (section 2, n<=13).  tau(H-v) in {5,6}; tau = 6 would need 66 <= 61-2d, false;
   so tau(H-v)=5 and 55 <= 61-2 deg(v): **deg(v) <= 3 for all v**.  With sum deg = 33 on 14 vertices at least 5 vertices have degree 3.
2. For such v, G = H-v has (13,8,5), slack 0.  Every component of G satisfies I11 (n<=13), so every component has slack 0 and no
   isolated vertex.  Slack-0 connected cells with m <= n-2, n <= 2m+1, n <= 13 are only (3,1,1), (10,7,4), (13,8,5); so
   G = connected (13,8,5) or (10,7,4) + one AP.
3. `conn_dfs2_all 13 8 5` gives 159 labelled (2 isomorphism classes, both contain F7: `tight_classes.py`), `10 7 4` gives 637 labelled (6 classes, 5 F7-free).
   Adding a vertex v with 3 new edges {v,a_i,b_i} (disjoint pairs, none inside an edge of G): `ext_vertex.c`
   enumerates all 6,699,128 extensions of the 796 graphs; 3,186 have tau >= 6, **all 3,186 contain F7** (`analyze_hits.py`, `ext_vertex_hits.txt`).
   The C code was cross-checked by an independent numpy implementation on 25 random G (210,104 extensions, 111 hits both ways, `crosscheck_ext.py`).
4. Independent route: `conn_dfs2_all 14 11 6 3` (all connected linear 3-graphs with 14,11,tau>=6 and max degree <= 3, 1.17e9 nodes) found
   998 labelled graphs (`conn2_all_14_11_6_deg3.txt`), **all 998 contain F7** (`ud_check.py`, `results_ud_check.json`) - consistent with step 3 (this route uses only step 1, not steps 2-3).
So tau_max^O(14,11) = 5; i.e. **Q11 (open in kb) has the answer "empty" for the abstract class, hence for realizable sets**, and with the m=12
census (L004) the 2,910 classes are all extremal 14-point (4,5)-classes.  (Assumptions: HY theorem; correctness of `conn_dfs2` (validated as above)
and of the find_f7 test; the K-lemmas are NOT used.)
An F7-containing example (shows F7-freeness is essential for I11): `f7_containing_violation.json` (14 vertices, 11 edges, tau 6, slack -2).
**Also not provable from "linear + F7-free" alone:** `f7free_nonO_violation_9_8_4.json` is a connected linear F7-free 3-graph with n=9, m=8, tau=4,
slack -1 (HY holds with slack 1; tau verified by brute force); it has m > n-2, so it is not an ordered midpoint pattern.  128 such graphs were found
by `ud_check.py` (`ud_9_8_4.txt`).  Hence any proof of I11 must use the injective-midpoint condition e(S) <= |S|-2 (not only linearity and F7-freeness);
Other unordered dense cells (m > n-2, connected, tau >= least violating): (10,12,5) 1,892 and (11,10,5) 620 labelled violators, all contain F7; (11,16,6) and (12,20,7): none at all; (12,14,6), (13,13,6) timed out at 600 s (undecided); (13,18,7), (13,24,8) not completed (`unordered_dense.log`).

## 4. Consequences for n = 16 (stated, not decided)  [derived-here]
Given I11 for all n <= 15 on O (section 2 + 3): for a minimal violator H (slack s <= -1): every vertex has tau(H-v) = tau-1 and deg(v) <= (8+s)/2, i.e. deg <= 3.
* (16,13,7): slack -3, deg <= 2, but sum deg = 39 > 32: **impossible in O** (so f(16)=9 would need m = 14 = n-2, a saturated pattern).
* (16,14,7): slack -1; deg <= 3 everywhere, at least 10 vertices of degree 3; deleting a degree-3 vertex leaves a (15,11,6) graph of slack 1.  Its
  slack-1 components can only be (8,5,3),(11,6,4),(12,10,5),(14,7,5),(15,11,6) (3n+2m-11tau = 1, m <= n-2), giving G = connected (15,11,6) or (12,10,5) + one AP.
  This is a much stronger constraint than the K44 degree bound (deg <= 5) and could be fed into the CP-SAT/SAT model for Q1.  CaDiCaL on (16,14,alpha<=9) with max degree <= 3 (once without and once with K30) was run for about 35 minutes each and returned no answer before being stopped (UNKNOWN; recorded in `sat16_*.log` as empty); it is NOT a refutation or a witness.
This is exactly the open f(16) question; no attempt to decide it beyond the SAT run above.

## 5. Simplest hypothetical violator (Test 7)
By section 2/3 the minimal violating pattern would be (14,11,6) in O: a 14-point (4,5)-set with h = 8 and exactly 11 APs (HY slack 1, D = 10, three non-midpoints).
It is excluded by the argument of section 3 (uses HY, the n<=13 cells, F7).  The cells (8,4,3),(10,6,4),(11,5,4),(12,9,5),(13,7,5) are excluded by DFS/SAT.
The next candidates are (15,9/10,6) (excluded by DFS), (16,8,6) (excluded) and the f(16) cells.  Known lemmas: K30 (monotone midpoints), K31 (medial triangle),
the cores, and Lemma U were not needed for n <= 15; they would only shrink class O further.  The structural reason I11 is plausible: equality is attained by
exactly the "rigid" pieces AP, C10=(10,7,4), A_base, which pairwise glue additively; deleting any vertex from a minimal violator must drop tau by one, and
slack-0 pieces are very few.

## 6. Free-coefficient LP (step 6)
Exact vertex enumeration (above, section 0) of the family tau <= a n + b m over all data: vertices (0,1), (3/11,2/11), (3/7,0).  I11 is the unique vertex with
b > 0 other than the trivial tau <= m; on the saturated regime (m ~ n) its constant a+b = 5/11 is worse than the 3/7 vertex.  The lp-fit dataset's frontier
(`results_frontier.json`) agrees.  Tight cells at I11: (3,1,1),(6,2,2),(9,3,3),(10,7,4),(12,4,4),(13,8,5),(14,12,6).

## Files
Scripts: `subsets.c`, `common.py`, `test1.py`, `test23.py`, `test4.py`, `test6.py`, `test6b.py`, `amalgam.py`, `ext_gen.py`, `run_c_file.py`, `hist_union.py`, `frontier_lp.py`,
`polygon.py`, `abstract_table.py`, `conn_dfs.c`, `conn_dfs2.c`, `conn_dfs2_all.c`, `verify_cells.py`, `isocheck.py`, `tight_classes.py`, `ext_vertex.c`, `ext_vertex_all.c`,
`analyze_hits.py`, `crosscheck_ext.py`, `ud_check.py`, `sat_cell.py`, `reproduce.sh`.  Results: `results_*.json`, `*.log`, `conn_all_*.txt`, `ext_vertex_hits.txt`,
`f7_containing_violation.json`, `f7free_nonO_violation_9_8_4.json`.  Heavy intermediate files (extension inputs, 0.2 GB) were kept in the session scratchpad only; regenerate with `ext_gen.py`.
