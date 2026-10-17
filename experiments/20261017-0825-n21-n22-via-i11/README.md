# I11 on class O for n = 21 and n = 22   RESULT: HOLDS (computer-assisted, [derived-here], needs referee).  (22,20,10) is impossible by counting: f(22) = 13 within O.

Setting, lemma and tools as in ../20261017-0705-n19-n20-via-i11/README.md (violator H with slack s<=-1; I11 known below n: tau(H-v)=tau-1, deg(v)<=floor((8+s)/2), slack(H-v)=s+8-2deg(v)).  Assumed: HY; I11 on O for n<=20 (n=21), n<=21 (n=22).
No survivor, no RECORD_CANDIDATE.json, `new_claim.py` not run; nothing committed.  Large intermediates are in out/ (git-ignored).

## Correction applied (isolated vertices)
An isolated vertex has slack 3 (n=1,m=0,tau=0).  `parts.py` now includes the cell (1,0,0) for slack lists with k>=3 and `parts_bf.py` regenerates every list by an independent brute force
(all multisets of component types (n_i,m_i,tau_i) with slack in [0,k], HY, summing to (N,M,tau') - it sums tau, parts.py sums slack) and compares: `results_parts_check.json`, all lists EQUAL:
(20,9,7;k=1) 4 partitions, (19,11,7;2) 9, (20,10,7;3) 14, (17,9,6;3) 10, (16,10,6;2) 5, (18,12,7;1) 4, (21,13,8;1) 7, (20,14,8;0) 4, (19,10,7;0) 4.
Affected list in this folder: only (20,10,7) slack 3 (10 partitions before, 14 now; G' candidates 51 -> 55); all other lists here have k<=2 and are unchanged.  (Earlier folders: the (17,9,6) slack-3 list of the n19/n20 work, recomputed by the prover in L010.)
The class lists reused from earlier folders ((15,11,6), connected (18,12,7)=none, C14, C17) come from slack<=2 or slack-1 lists, except connected (18,12,7), which used the (17,9) slack-3 list that L010 repaired (the repair changes nothing, according to the prover).

## Window cells (n=21, 22)
| cell | slack | deg bound | sum deg vs 2n | decision |
|---|---|---|---|---|
| (21,11,8) | -3 | 2 | 33 vs 42 | maxdeg<=2 DFS 220,119 nodes: none |
| (21,12,8) | -1 | 3 | 36 vs 42 | maxdeg<=2 DFS 7,299,871 nodes: none; deg-3 route below: empty |
| (21,16,9) | -4 | 2 | 48 > 42 | impossible |
| (21,17,9) | -2 | 3 | 51 | empty (below) |
| (22,15,9) | -3 | 2 | 45 > 44 | impossible |
| (22,16,9) | -1 | 3 | 48 | empty (below) |
| (22,20,10) | -4 | 2 | 60 > 44 | impossible (your slack: 66+40-110 = -4, confirmed) |
Window = connected cells with m<=n-2, n<=2m+1, least violating tau <= min(HY, m) (`windows`-style script in earlier folders; no other cells at n=21, 22).

## (21,12,8) deg-3 route
G=H-v=(20,9,7), slack 1: partitions [4AP,(8,5,3)] [3AP,(11,6,4)] [2AP,(14,7,5)] [AP,(17,8,6)]; (11,6,4),(14,7,5),(17,8,6) have no graphs, (8,5,3) has 2 classes -> 2 graphs; 642,638 extensions, 100 hits (tau>=8): 94 contain F7, 6 violate e(S), 0 survive.  numpy 100=100; control tau>=7: 2,998 of 3,000 sampled hits survive.

## (21,17,9)
sum deg 51 gives >=9 degree-3 vertices; G=(20,14,8), slack 0: [AP,AP,C14] (C14: 2 classes) [AP,C17] (8 classes) [C10,C10] (4 classes -> 10 unordered pairs) [connected (20,14,8)].
Connected (20,14,8): maxdeg 2 impossible (sum deg 42>40); degree-3 vertex w: G'=(19,11,7), slack 2, 9 partitions (cells (10,8,4) 63 classes, (13,9,5) 84, (16,10,6) 16, (6,3,2) 1, (9,4,3) 1, (8,5,3) 2, (19,11,7): 1,623 labelled all with F7, (13,8,5): none, (11,6,4): none); 174 G', 12,865,097 extensions, 3,965 hits -> 18 classes.
Final: 38 graphs, 2,692,668 extensions with tau>=9: 36 hits, all contain F7, 0 survive.  numpy: 12 G -> 12 = 12, and the 38 G -> 36 = 36.  Control tau>=8: 2,894 of 3,000 survive.

## (22,16,9)
sum deg 48: maxdeg 2 impossible; >=4 degree-3 vertices.  G=(21,13,8), slack 1: [3AP,(12,10,5)] (149 classes) [2AP,(15,11,6)] (19) [AP,C10,(8,5,3)] (8) [AP,(18,12,7)] (none) [C10,(11,6,4)] (none) [C13,(8,5,3)] (none, F7) [connected (21,13,8)].
Connected (21,13,8): maxdeg 2 DFS 125,635,032 nodes, none; degree-3 w: G'=(20,10,7), slack 3, 14 partitions incl. isolated vertices (55 G'); 12,751,175 extensions, 6,470 hits -> 330 iso classes (143 F7, 11 e(S)) -> 176 classes.
Final: 352 graphs; 22,406,124 extensions with tau>=9: 5,944 hits = 5,860 with F7 + 84 F7-free violating e(S) + **0 survivors**.  numpy: 15 G -> 271 = 271.  Control tau>=8 (150 sampled hits): 148 survive.
(`dedupe_fast.py`, component-wise isomorphism, replaced the networkx-on-whole-graph dedupe, which was too slow on unions of many APs; it reproduces the old counts: X20 18 kept/13 killed.)

## Why the method cannot exclude n = 23, and the first I11-allowed record cells (`record_cells.py`, results_record_cells.json)
The whole method refutes *violations* of I11 (slack<0): the deletion lemma needs s<=-1.  At n=23 the pattern (23,21,10) (saturated, h=13, 13/23 < 4/7) has slack 3*23+2*21-110 = **+1**, HY-feasible (170 <= 115+63), so I11 is satisfied: there is nothing to contradict, and I11 alone cannot be sharpened by deletion (a vertex deletion changes slack by 8-2d >= 2 in the favourable direction).  Excluding it needs a strictly stronger inequality (e.g. tau <= 3n/7 i.e. the 4/7 conjecture, or a Q8-type statement).
Cells (n,m,tau) with I11 slack>=0, HY-feasible, m<=n-2 and h=n-tau <= ceil(4n/7)-1 (so beating 4/7): none for n<=22 and none for n=24, 26-29, 31, 33, 35, 38, 40;
n=23: (23,21,10) s=1;  n=25: (25,23,11) s=0;  n=30: (30,27,13) s=1, (30,28,13) s=3;  n=32: (32,29,14) s=0, (32,30,14) s=2;  n=34: (34,32,15) s=1;  n=36: (36,34,16) s=0;  n=37: (37,33,16) s=1, (37,34,16) s=3, (37,35,16) s=5;  n=39: (39,35,17) s=0, (39,36,17) s=2, (39,37,17) s=4.

## What the referee must check
1. The slack-list generator (`parts.py`, `parts_bf.py`, isolated vertices) and the specific lists above; the counting impossibilities (21,16,9), (22,15,9) (tight: 45>44), (22,20,10).
2. `conn_dfs3` completeness incl. maxdeg 2 (here DFS up to 1.26e8 nodes), `ext_vertex2`, `find_f7`, e(S) filter, `dedupe_fast.py` (component-wise isomorphism).
3. Reused class lists from earlier folders ((15,11,6) 49 classes, C14, C17, connected (18,12,7) = none) and the cells (19,11,7), (20,10,7), (17,8,6), (14,7,5), (11,6,4) being empty or F7-only.
Files: results.json, results_parts_check.json, results_record_cells.json, run_x12.py, run_x17.py, run_x22b.py (run_x22.py = same with the slow dedupe), build.py, parts.py, parts_bf.py, dedupe_fast.py, post.py, record_cells.py, post_*.log, stats_*.json, out/.
