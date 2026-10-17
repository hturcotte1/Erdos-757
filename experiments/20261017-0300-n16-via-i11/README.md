# f(16) via I11: is there a class-O pattern with n=16, m=14, tau>=7 ?   RESULT: EMPTY (computer-assisted, [derived-here]; certified as L008 / K52 [verified-here], referee ACCEPT x3 on 2026-10-17, results/proofs/L008-f16-equals-10.md)

Class O = ordered midpoint hypergraphs (linear, F7-free, injective midpoints, hence e(S) <= |S|-2 for every vertex subset S).  Every (4,5)-set gives a
member of O with h = alpha = n - tau.  A 16-point (4,5)-set with h = 9 would be a member of O with n=16, tau=7.  Notation: slack = 3n+2m-11tau.
No survivor, no RECORD_CANDIDATE.json, and `scripts/new_claim.py` was NOT run (nothing to claim).

## Logic (all steps are in /home/user/Erdos-757/experiments/falsify/i11-inequality/README.md sections 2-4, re-derived here)
0. Assumed (referee must re-check): Henning-Yeo 17 tau <= 5n+3m on linear F7-free [published]; I11 holds on O for every n <= 15
   (windows (8,4,3) (10,6,4) (11,5,4) (12,9,5) (13,7,5) (15,9,6) (15,10,6) by exhaustive DFS; (14,11,6) by the vertex-extension argument; all in the earlier README).
1. H in O, n=16, tau>=7: HY gives m>=13 and tau=7; slack(H) = 2m-29 = -3 (m=13) or -1 (m=14); I11 on every H-v (n=15) forces tau(H-v)=6 and deg(v) <= m-11.
   m=13: deg<=2 but sum deg=39>32: impossible.  m=14: deg<=3 for all v, sum deg = 42, so >=10 vertices of degree 3.
2. Take v of degree 3; G = H-v has (15,11,tau=6) (tau=7 contradicts HY), slack 1, max degree <= 3.  Every component of G satisfies I11, so exactly one component has
   slack 1, the others slack 0, no isolated vertices.  `slack_cells.py` (results_slack_cells.json) lists connected cells (m<=n-2, n<=2m+1, HY, n<=15):
   slack 0: (3,1,1) (10,7,4) (13,8,5) (14,12,6);  slack 1: (8,5,3) (11,6,4) (12,10,5) (14,7,5) (15,11,6).  The only ways to total (15 vertices, 11 edges) are
   **[(15,11,6)]** and **[(12,10,5) + (3,1,1)]**; e.g. 8+7, 11+4, 14+1 vertices need a slack-0 piece of size 7, 4, 1 which does not exist, and (13,8,5)/(14,12,6) cannot fit.
   (The two connected (13,8,5) graphs contain F7, so they could not occur in O anyway.)
3. Case A (G = R12 + one AP, R12 connected (12,10,5), max degree <= 3) and case B (G connected (15,11,6), max degree <= 3).
4. H = G + v with three new edges {v,a_i,b_i}: disjoint pairs, no pair inside an edge of G, endpoints of G-degree <= 2.  We need tau(H) >= 7.

## Step 1: enumeration of G  (`conn_dfs3.c`; canonical BFS-growth DFS of ALL connected linear 3-graphs, no F7/order condition; the F7/e(S) prunes exist but were NOT used)
| cell | command | labelled graphs | nodes | time |
|---|---|---|---|---|
| (12,10,5) maxdeg 3 | `conn_dfs3 12 10 5 3 0 0` | 145,033 -> 36,916 contain F7; **150** F7-free iso classes; 1 violates e(S)<=|S|-2 -> **149** kept | 56,801,671 | ~40 s |
| (15,11,6) maxdeg 3 | `conn_dfs3s 15 11 6 3 0 0 2 {0,1}` (2 processes, nice 5) | 50,606 (26,041 + 24,565) -> **49** iso classes (22 F7-free) | 1,909,545,133 + 1,892,258,847 | 32.4 CPU-min each, 85 min wall |
Validation of the enumeration: (i) `conn_dfs3` output is line-for-line identical to `conn_dfs2_all` (used for I11, validated vs a naive v1 on 200 cells and 8 iso-class counts) on four cells;
(ii) slice partition check (K=3 slices of (12,10,5): 46,829+51,125+47,079 = 145,033); (iii) the 150 classes contain every one of the 39,309 realizable 12-point classes (K41) with max degree <= 3 and 14,813/14,813 sampled abstract (12,10) census patterns
(`check_R12_classes.py`); (iv) single-incidence-move closure of the 49 (15,11,6) classes: 885 valid neighbours, all inside the 49 classes (`moves_check.py`); (v) random local search (2 x 600 s, `random_search_B.py`): 396 connected tau>=6 graphs, all isomorphic to one of the 49 classes.
**A bug was found and fixed on the way:** the first (15,11,6) run used a split rule whose partition was inconsistent between the two processes (it found only 47 classes); the move-closure test exposed 25 missing neighbours; the SLICE macro in `conn_dfs3.c` now counts at node creation, and the whole run was redone.  Earlier unsplit runs (n<=14) were not affected.

## Step 2: extensions (`ext_vertex2.c`, max degree <= 3 in H, keep every hit with tau(H) >= 7)
| input | graphs | extensions tested | hits (tau>=7) |
|---|---|---|---|
| case A: 149 R12+AP | 149 | 74,916 | 18 |
| case B: 49 iso classes | 49 | 154,309 | 218 |
| case B: all 50,606 labelled graphs (redundant, kept as a check) | 50,606 | 159,914,042 | 173,687 |
Cross-check by an independent numpy implementation (`crosscheck_ext2.py`): identical hit counts on all 49 case-B classes (218) and on 40 case-A graphs (8).  All hits are in hits_caseA.txt, hits_caseB_classes.txt, hits_caseB.txt.gz.

## Step 3: filters (`post.py`)
| set | hits | contain F7 | F7-free but e(S)>|S|-2 somewhere | F7-free, e(S) ok, not orderable | survivors |
|---|---|---|---|---|---|
| case A | 18 | 0 | **18** (each has a 13-vertex subset with 13 edges) | 0 | **0** |
| case B (classes) | 218 | **218** | 0 | 0 | **0** |
| case B (all labelled) | 173,687 | **173,687** | 0 | 0 | **0** |
The filter chain is not vacuous: with T=6 instead of 7 (control on the case-A input) 2,634 of 3,000 sampled hits survive F7, e(S) and the SAT test for an ordered injective midpoint labelling (`post.py` orderability SAT: A_base accepted, a graph with m>n-2 rejected).
Because no hit survives F7-freeness or the e(S) condition, the K30 filter and the exact realizer were not needed.

## Conclusion
There is no member of O with (n,m,tau) = (16,14,7), and none with (16,13,7).  Hence f(16)=10 within class O, hence for all (4,5)-sets, **relative to** the assumptions below.
Also: the two statements "m=13 impossible" and "H has max degree <= 3, >=10 vertices of degree 3" are consequences of I11 for n<=15, independent of the DFS of this folder.

## What the referee must check
1. HY (published) and the whole I11-for-n<=15 chain (window list; `conn_dfs2` correctness; the (14,11,6) extension argument; (15,9,6),(15,10,6) DFS): see falsify/i11-inequality/README.md.
2. The reduction steps 1-2 above (slack bookkeeping, tau(H-v)=tau-1, deg bound, existence of a degree-3 vertex, classification of components: `slack_cells.py`).  Note that component slack >= 0 uses I11 for n<=15 including n=14 and 15.
3. Completeness of `conn_dfs3` (canonical growth argument: group of edges at vertex `cur` added in key order, new vertices numbered by creation; max-degree prune; tau prune; slicing); the evidence is items (i)-(v) above.  A second implementation of the enumeration (e.g. orderly generation with nauty) would be the strongest independent check.
4. `ext_vertex2.c` (pairs: disjoint, not inside a G-edge, endpoint degree <= 2) and `find_f7` (used to reject; every rejection is a concrete F7 copy: p on three edges plus complementary transversal edges).
5. The e(S) criterion for case A: e(S)<=|S|-2 holds for every subset of a (4,5)-set pattern (midpoint map injective, never hits min/max of S).
## Files
conn_dfs3.c, conn_dfs3s.c (SD=6), ext_vertex2.c, post.py, slack_cells.py, prep_R12.py, classes_B.py, moves_check.py, check_R12_classes.py, crosscheck_ext2.py, random_search_B.py, found2input.py, gutil.py,
data/logs: results.json, results_slack_cells.json, post_case*.json, hits_case*.txt(.gz), g15_11_6_part*.txt.gz, G_*.txt, classes_B_reps.json, R12_labelled.txt.gz.
Reproduce (order): `gcc -O2 -o conn_dfs3 conn_dfs3.c; sed s/SD=4/SD=6/ conn_dfs3.c > conn_dfs3s.c; gcc -O2 -o conn_dfs3s conn_dfs3s.c; gcc -O2 -o ext_vertex2 ext_vertex2.c`;
`./conn_dfs3 12 10 5 3 0 0 > R12_labelled.txt; python3 prep_R12.py R12_labelled.txt G_R12_AP.txt; ./ext_vertex2 15 7 3 < G_R12_AP.txt > hits_caseA.txt; python3 post.py hits_caseA.txt 16 post_caseA.json`;
`./conn_dfs3s 15 11 6 3 0 0 2 0 > g15_11_6_part0.txt` and `... 2 1 > g15_11_6_part1.txt`; `python3 found2input.py g15_11_6_part0.txt g15_11_6_part1.txt > G_B_conn15.txt; ./ext_vertex2 15 7 3 < G_B_conn15.txt > hits_caseB.txt; python3 post.py hits_caseB.txt 16 post_caseB.json`.
