# I11 on class O for n = 17 and n = 18   RESULT: HOLDS (computer-assisted, [derived-here], needs referee).  No (18,16,8) pattern: f(18) = 11 within O.

Class O = linear, F7-free, injective ordered midpoints (so e(S) <= |S|-2 on every subset).  slack = 3n+2m-11tau.  Assumed: Henning-Yeo; I11 on O for n <= 16 (L007, L008).
No survivor, no RECORD_CANDIDATE.json, `new_claim.py` not run.  Lemma used throughout (a violator H with slack s<=-1, all smaller members satisfy I11): tau(H-v)=tau-1 for every v,
deg(v) <= (8+s)/2, and H-v has slack s+8-2deg(v); components of any member of O on <= n-1 vertices have slack >= 0.

## 1. Window cells (`windows.py`, results_windows.json)
Connected cells (m<=n-2, n<=2m+1, 11tau>3n+2m, 17tau<=5n+3m): n=17: only (17,12,7), **slack -2** (not -1).  n=18: **three** cells: (18,10,7) slack -3, (18,11,7) slack -1, (18,16,8) slack -2
(the two small-m cells were missing from the requested list).  Slack-0 connected cells n<=17: (3,1,1) (10,7,4) (13,8,5) (14,12,6) (16,9,6) (17,13,7).

## 2. n = 17, cell (17,12,7)
deg<=3, sum deg=36 gives a degree-3 vertex; G=H-v is (16,9,6), slack 0.  Decompositions (checked by script): [(16,9,6)], [(13,8,5)+AP], [(10,7,4)+AP+AP].
* connected (16,9,6): `conn_dfs3 16 9 6 3 0 0` 2,316,873 nodes, **0** graphs (unrestricted degree: 2,763,175 nodes, 0).
* (13,8,5)+AP: all 159 connected (13,8,5) graphs contain F7: none.
* (10,7,4)+2AP: 637 labelled connected (10,7,4), 126 with F7, 5 F7-free iso classes; 5 graphs, 169,560 extensions by a degree-3 vertex with tau>=7: 32 hits, **all 32 contain F7**; numpy cross-check 32 = 32.
=> (17,12,7) empty; **I11 holds for n=17.**

## 3. n = 18
* (18,10,7): `conn_dfs3 18 10 7 100` (no degree restriction): 3,322,249 nodes, 0 graphs.
* (18,11,7): deg<=3 (valid by I11 n<=17): 316,932,284 nodes, 0 graphs.
* (18,16,8): deg<=3, >=12 degree-3 vertices; G=H-v is (17,13,7), slack 0; decompositions: [(17,13,7)], [(14,12,6)+AP] (script).  Both connected tight graphs were reconstructed by the same vertex trick instead of a 1e11-node DFS
  (Knuth/slice estimate for connected (17,13,7) deg<=3: ~1.1e11 nodes, ~30 CPU-h):
  - connected (14,12,6), deg<=3: remove a degree-3 vertex -> (13,9,5), slack 2 = [AP+(10,8,4)] or [(13,9,5) connected]; class counts (F7-free, e(S) ok): (10,8,4) 63, (13,9,5) 84; 147 graphs, 184,099 extensions, 260 hits (224 contain F7, 5 violate e(S), **2 classes** remain).  All 700 realizable census classes (data/census_n14_m12_classes.jsonl.gz) with max degree <=3 are isomorphic to these 2 classes; a random sample of the direct DFS (1,412 slices, 3,369 graphs, 96 F7-free & e(S)-ok) lands only in these 2 (both hit).
  - connected (17,13,7), deg<=3: remove a degree-3 vertex -> (16,10,6), slack 2 = [AP+AP+(10,8,4)] [AP+(13,9,5)] [(10,7,4)+(6,3,2)] [(8,5,3)+(8,5,3)] [connected (16,10,6)] (script `parts_g.py`); component classes: (6,3,2) 1, (8,5,3) 2, (10,7,4) 4, (10,8,4) 63, (13,9,5) 84, (16,10,6) 16 (12,394 labelled, 181.7M nodes);
    170 graphs, 2,357,887 extensions, 1,521 hits (1,350 F7, 13 e(S)) -> **8 classes**.  Direct DFS check: 62 random slices, 735 graphs, 26 F7-free & e(S)-ok, all inside the 8 classes (5 of them hit).
  - Final step: G in {8 classes of connected (17,13,7)} + {2 classes (14,12,6)+AP} = 10 graphs; extension by a degree-3 vertex whose other endpoints have degree <=2: 44,570 extensions, **0 with tau>=8** (every extension has tau=7); numpy cross-check agrees (0); control with T=7: 44,570 hits, 1,628 of 2,000 sampled survive F7/e(S)/orderability, so the pipeline is not vacuous.
=> (18,16,8) empty (not even before the F7 filter); **I11 holds for n=18**, f(18)=11 for O, no 18-point (4,5)-set with h=10.

## What the referee must check
1. The lemma (deg bound, tau(H-v)=tau-1, slack bookkeeping, existence of degree-3 vertices) and the decomposition lists (`windows.py`, `parts_g.py`: slack-0/1/2 connected cells with m<=n-2, n<=2m+1, HY).
2. Completeness of `conn_dfs3` (canonical growth, max-degree and tau prunes; consistent slicing; see the n16 folder), the vertex-deletion reconstruction (valid because every connected tight graph has a degree-3 vertex and G-w is in O with all components of slack >=0), and the dedupe filters (F7-free, e(S)<=|S|-2, both hereditary).
3. `ext_vertex2.c` (disjoint pairs not inside an edge, endpoints of degree <=2) - cross-checked with numpy; `find_f7`.
4. The slack-2 cell lists for (16,10) and (13,9) (partitions above) - e.g. missing a cell with isolated vertices is impossible since an isolated vertex has slack 3.
Reproduce: see run_C14.py, run_G17.py, run_H18.py (compile conn_dfs3.c, ext_vertex2.c first; `conn_dfs3s` = SD=6 variant), validate_*.py.  Files: results.json, stats_*.json, hits_*.txt, C14_classes.json, G17_classes.json.
