# I11 on class O for n = 19 and n = 20   RESULT: HOLDS (computer-assisted, [derived-here], needs referee).  No (20,18,9) pattern: f(20) = 12 within O.

Class O, slack and the vertex-deletion lemma as in ../20261017-0615-n17-n18-via-i11/README.md (violator H with slack s<=-1, I11 known below n: tau(H-v)=tau-1, deg(v)<=floor((8+s)/2), slack(H-v)=s+8-2deg(v);
components of members of O have slack>=0).  Assumed: HY; I11 on O for n<=18 (L007-L009) when treating n=19, and for n<=19 when treating n=20.  No survivor, no RECORD_CANDIDATE.json, `new_claim.py` not run; nothing committed.

## Window cells (connected, m<=n-2, n<=2m+1, least violating tau = floor((3n+2m)/11)+1 <= min(HY, m))
| n | cell (n,m,tau) | slack | deg bound | decision |
|---|---|---|---|---|
| 19 | (19,9,7) | -2 | 3 | empty: unrestricted DFS 8,550 nodes |
| 19 | (19,14,8) | -3 | 2 | impossible: sum deg = 42 > 2*19 = 38 |
| 19 | (19,15,8) | -1 | 3 | empty (below) |
| 20 | (20,12,8) | -4 | 2 | empty: maxdeg<=2 DFS 6,278,507 nodes |
| 20 | (20,13,8) | -2 | 3 | empty (below) |
| 20 | (20,18,9) | -3 | 2 | impossible: sum deg = 54 > 2*20 = 40 (the n=20 record cell) |
(`windows.py`; these are all cells at n=19, 20.)

## (19,15,8)  [sum deg = 45, >=7 vertices of degree 3]
G = H-v = (18,12,7), slack 1, maxdeg 3.  `parts.py 18 12 1` (slack-0/1 connected cells): [AP,AP,(12,10,5)], [AP,(15,11,6)], [(10,7,4),(8,5,3)], [connected (18,12,7)].
Classes (maxdeg<=3, F7-free, e(S) ok): (12,10,5) 149 (of 150 F7-free; 145,033 labelled), (15,11,6) 19 (from the 49 verified classes of the n=16 folder; 22 F7-free, 3 killed by e(S)), (10,7,4) 4, (8,5,3) 2.
Connected (18,12,7), slack 1:
* maxdeg<=2: direct DFS, 16,616,566 nodes, 0 graphs.
* has a degree-3 vertex w: X-w = (17,9,6), slack 3 (tau drops since 1<3+6).  `parts.py 17 9 3`: 7 partitions [AP,AP,AP,(8,6,3)] [AP,AP,(11,7,4)] [AP,(8,5,3),(6,3,2)] [AP,(14,8,5)] [(8,5,3),(9,4,3)] [(11,6,4),(6,3,2)] [(17,9,6)];
  all component cells have m<=9 and are enumerated directly ((11,6,4) and (17,9,6) have no graphs).  51 graphs G', 3,053,913 extensions, 4,251 hits (tau>=7): 1,555 contain F7, 187 F7-free iso classes, 11 killed by e(S), **176 classes**.
Final: 352 candidate G ((176 + 149 + 19 + 8) graphs), extension by a degree-3 vertex with tau>=8: 4,306,086 extensions, 2,140 hits: **2,056 contain F7, 84 F7-free violate e(S)<=|S|-2, 0 survive**.
numpy cross-check (`crosscheck_ext2.py`, 40 graphs): 243 = 243 hits.  Control with tau>=7 (4,000 sampled hits): 3,733 survive F7/e(S)/orderability, 12 F7, 255 e(S).
=> **I11 holds for n=19.**

## n = 20, (20,13,8)  [sum deg = 39]
* maxdeg<=2: DFS 79,682,223 nodes, 0 graphs.
* has a degree-3 vertex: G = H-v = (19,10,7), slack 0; `parts.py 19 10 0`: [AP,AP,AP,(10,7,4)], [AP,AP,(13,8,5)], [AP,(16,9,6)], [(19,10,7)].
  (10,7,4)+3AP: 4 graphs, 571,849 extensions, 72 hits with tau>=8, all contain F7.  (13,8,5): all 159 connected graphs contain F7.  (16,9,6): no graphs (2.3M nodes, n17 folder).  Connected (19,10,7), maxdeg 3: 2,310,245 nodes, 0 graphs.
=> empty.  With (20,12,8) and (20,18,9): **I11 holds for n=20**; no 20-point (4,5)-set with h=11 (f(20)=12 for O).

## Validation
`validate_generic.py` samples random slices of the direct DFS for connected (18,12,7), maxdeg 3 and checks that every F7-free e(S)-ok graph found is isomorphic to one of the 176 reconstructed classes: VALIDATE_X18.
(The reconstruction trick and the earlier cells were validated in the n16 and n17/n18 folders.)

## What the referee must check
1. The lemma and the degree-counting impossibilities (19,14,8), (20,18,9); the window list.
2. Cell decompositions (`parts.py`), notably the slack-3 list for (17,9) and that every needed cell has small m.
3. `conn_dfs3` completeness (also used with maxdeg 2), `ext_vertex2`, `find_f7`, e(S) filter (see earlier folders); reuse of the 49 classes of (15,11,6) from the n16 folder.
4. maxdeg<=2 searches rely on the degree bound, i.e. on I11 at n-1.
Files: results.json, stats_*.json, windows.py, parts.py, run_X18.py, run_H19.py, run_20_13_8.py, build.py, post.py, hits_*.txt, X18_deg3_classes.json, D_*.txt (DFS logs).
