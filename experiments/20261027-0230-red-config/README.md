# Reducibility engine for I11 and census of (Red)-free graphs (2026-10-27)

Question. For the minimal-counterexample method for I11 (11 tau <= 3n + 2m on the class C of linear, F7-free 3-graphs with
e(S) <= |S|-2 for all |S| >= 2): which connected members of C with maximum degree <= 3 have NO reducing pair (Z,T) with Z a proper
nonempty vertex set? ("(Red)-free".)

## Definitions and the reduction lemma [derived-here]
H in C, Z a proper nonempty vertex set, E_Z = edges meeting Z, e(Z) = |E_Z|, T a vertex set meeting every edge of E_Z.
* Lemma R. tau(H) <= tau(H-Z) + |T| (a minimum transversal of H-Z, whose edges are exactly the edges missing Z, plus T). If I11
  holds for H-Z (in C: induced subhypergraphs of C are in C) then 11 tau(H) <= 3n+2m + [11|T| - 3|Z| - 2e(Z)], so I11 holds for H as soon as
  (Red): 11|T| <= 3|Z| + 2e(Z). For fixed Z the best T is a minimum transversal of E_Z, so
  **value(Z) = 3|Z| + 2e(Z) - 11 tau(E_Z)** and (Red) holds for Z iff value(Z) >= 0. (Red) depends only on the star E_Z.
* Minimal counterexample is connected (slack and tau are additive over components), has Delta <= 3 (Z=T={v}, d(v)>=4: 11 <= 3+2d) and is (Red)-free.
* Lemma L (locality). Let R be the relation z R z' iff an edge at z meets an edge at z' (including z=z'). If value(Z) >= 0 then some R-connected
  component Z_i of Z has value(Z_i) >= 0: the components of the hypergraph (V,E_Z) are the sets E_{Z_i}, tau and e are additive over them, so value(Z)=sum value(Z_i).
  Hence it suffices to consider R-connected Z (the minimal-size Red Z is automatically R-connected: confirmed, column 14 = column 16 in all tsv files).
* (Red'): if y not in Z has all its edges in E_Z then Z+y has the same E_Z and value + 3, so maximizers are "closed" automatically
  when Z ranges over all proper subsets. Confirmed [verified-here]: in all 2,704,611 graphs of the census the maximizer Z* has no such y (closure_check.txt).
* Red_k-free := no (Red) pair with |Z| <= k. (Red)-free = Red_n-free. Large Z (|Z| about n-2) is essentially "H has positive slack"
  and is not a local configuration, so Red_k-free for small k is the meaningful notion for a discharging proof.

## Method (all exact integer arithmetic)
* `redfree.c` (+ `redfree.py`, independent pure-Python brute force used for validation): for every proper nonempty Z (bitmask, 2^n), tau(E_Z) from a table of tau over all 2^m edge subsets
  (tau(F) = 1 + min over vertices v of the lowest edge of tau(F minus edges at v)). Outputs tau, slack, value maximizer (Z*,T*), the number of Red sets, the smallest Red Z (and its e, tau, degrees).
* `extend.c` + `gen.py`: level-by-level generation of ALL connected members of C with Delta <= 3, up to isomorphism, for every (n,m): add one edge with 0/1/2 new vertices to every class of the cells
  (n,m-1), (n-1,m-1), (n-2,m-1) (every connected 3-graph has an edge whose removal, with its private vertices, leaves a connected graph; C is hereditary under edge deletion); children are filtered by C
  (linear, F7-free, Hall form of e(S)<=|S|-2) and Delta<=3, deduplicated by nauty (`../prover/L012/bin/canon`, nauty 2.8.8) and `sort -u`. A canonical-deletion key filter (edge key = number of private vertices, degrees) only removes duplicates.
* `enumc.c`, `enumred.c`: variants of the L007 enumerator (`enum_conn`) with the C check (and, in enumred, closed-vertex (Red_k) pruning, k<=ZMAX). Used for validation only; enumred is too slow beyond n=12 (the canonical growth explodes before the closed sets are large).
* Exact commands: `gcc -O2 -o bin/extend extend.c; gcc -O2 -o bin/redfree redfree.c; python3 gen.py 14; ./run_all.sh "3 4 5 6 7 8 9 10 11 12 13 14"; python3 aggregate.py; python3 tables.py > tables.md; python3 validate.py; python3 check_closure.py out/red_*.tsv`.
  (`out/` holds 1.4 GB of class lists and tsv files and is not committed; regenerate with the commands above, about 40 CPU minutes.)

## Validation [verified-here]
* Class counts: cells n<=11 (all m) identical to the independent pipeline enum_conn+filt+canon of the L012 tools; (12,10) with tau=5: 149 classes by both; (13,11) and (13,10) have no class with tau >= 6 in either.
  (14,12,tau>=6): 2 classes in our census; independent enum_conn run: see `out/indep_14_12_t6.txt` if finished (reported below if available).
* `redfree` (C) vs `redfree.py` (Python, brute force): identical (best value, tau, (Red)-free flag) on 99 random classes n=6..10 (validate.py). The pruned enumerator enumred reproduces the DP counts of Red_k-free graphs (k=2,3,4) in 18 cells n=9..12.
* Single AP (3,1,1): best value -3 at |Z|=2, T={v}: no proper Z with (Red): (Red)-free. [verified-here]
* A_base (14,12,6) (degree sequence 4^1 3^6 2^7): (Red) holds; best value 0 at Z=T={0} (the degree-4 vertex, 3+8=11 tau=1). A_base minus {0} = AP + a (10,7,4) piece (the AP is a component).
* The (10,7,4) piece (slack 0, degrees 3^2 2^7 1^1): (Red) holds with value 0 and 12 Red sets Z; optimal (max value 0, smallest) Z={0,1,2,6}, T={0,2}, e(Z)=5: 12+10-22=0. All 12 Red pairs are in `validate_out.json`.

## Results [verified-here unless marked]
Census of connected members of C with Delta <= 3 (all m with n <= 2m+1, m <= n-2), up to isomorphism, n <= 14:

| n | classes | Red-free | Red_2-free | Red_3 | Red_4 | Red_5 | Red_6 | Red_7 | Red_8 | Red_9 |
|---|---|---|---|---|---|---|---|---|---|---|
| 3 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| 4 | 0 | 0 | | | | | | | | |
| 5 | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 6 | 2 | 0 | 2 | 1 | 1 | 0 | 0 | 0 | 0 | 0 |
| 7 | 5 | 0 | 2 | 1 | 1 | 0 | 0 | 0 | 0 | 0 |
| 8 | 12 | 0 | 5 | 3 | 1 | 0 | 0 | 0 | 0 | 0 |
| 9 | 60 | 0 | 21 | 16 | 3 | 2 | 2 | 0 | 0 | 0 |
| 10 | 335 | 0 | 84 | 76 | 4 | 0 | 0 | 0 | 0 | 0 |
| 11 | 2526 | 0 | 576 | 544 | 6 | 3 | 2 | 1 | 1 | 0 |
| 12 | 22639 | 0 | 5188 | 5021 | 71 | 63 | 5 | 1 | 1 | 0 |
| 13 | 226960 | 0 | 53744 | 52547 | 1451 | 836 | 9 | 4 | 2 | 0 |
| 14 | 2452070 | 0 | 611988 | 601985 | 31221 | 2012 | 16 | 11 | 5 | 0 |

Per-cell table (n,m,d=n-m, classes, Red-free, Red_3/4/5/6/8-free, slack range): `tables.md`; everything in `results.json`.

1. **Task 1/2 headline.** The only (Red)-free connected member of C with Delta <= 3 and n <= 14 is the single AP (n=3). Every one of the 2,704,610 classes with 5 <= n <= 14 has a (Red) pair.
   So a minimal counterexample to I11 has n >= 15 (this is, of course, far below the known bound n >= 28 from L007-L016).
2. Sparse claim ("m <= n-5 is reducible"): true on the data; stronger, every class with m <= n-5 (d >= 5) and n <= 14 has a Red pair with |Z| <= 5 (Red_5-free count 0 for d >= 5; Red_4-free: 5 classes at (12,7), 14 at (13,8), none otherwise), and d >= 6 classes always have |Z| <= 3.
3. Which Z? Smallest Red set over all classes (n>=5): |Z|=2, e(Z)=3, tau=1, Z = {degree-3 vertex x, degree-1 vertex in an edge through x} (value 1): the minimal Red Z for 2,032,999 of the 2,704,610 classes ("pendant vertex next to a degree-3 vertex").
   Next: |Z|=4,e=6,tau=2 (degrees 3322): 272,729; |Z|=4,e=5,tau=2 (3222): 243,297; (3221): 43,062; (3322): 42,488; |Z|=5,e=9,tau=3 (33322): 22,098; |Z|=3,e=2,tau=1 (211): 11,295; ... The full list of types is `results.json` (types_of_minimal_Z).
4. Local reducibility is NOT enough with small Z: Red_k-free counts for k=4,5 (dense d=2 cells) grow with n (Red_4: 2, 61, 1429, 31100 at n=11..14, d=2; Red_5: 2, 59, 828, 1894), Red_6-free: 2, 5, 9, 16 (n=11..14), Red_7: 1, 1, 4, 11, Red_8: 1, 1, 2, 5, and Red_9-free: none for n=5..14 (so Z of size <= 9 always suffices up to n=14).
   BUT the Red_k-free graphs are almost all high-slack graphs (their Red sets are the trivial "H minus a few vertices" sets). Minimum slack among Red_4-free graphs by cell is >= 11 at (14,12), 9 at (14,11), 4 at (13,10), 1 at (12,10); the low-slack ones (the tight, extremal structures) are
   Red_5-free graphs (min |Z| >= 6) with slack <= 5: n=11: 1 ((11,7), tau 4, slack 3); n=12: 8 ((12,10), tau 5, slack 1; their min |Z| is 6 for 7 of them and 9 for one); n=13: 8 (1 at (13,9) slack 2; 7 at (13,10) slack 4); n=14: none. The two (14,12,6) slack-0 classes with Delta <= 3 have min |Z| = 4 (value-0 Red sets of size 4).
   Lists: `redk4_free_graphs.txt.gz` (32,760 graphs, n<=14), `redk5_...`, `redk6_...`, `redk8_...` ("m a.b.c ..." canonical edge lists, n = 1 + max label), `redfree_graphs.txt.gz` (the single AP).
5. Decreasing in n? The number of (Red)-free graphs is 0 for 5<=n<=14 (trivially non-increasing). For Red_k-free the counts are NOT decreasing for k<=5 in this range (see 4), and for k=6..8 they grow slowly (16, 11, 5 at n=14). No evidence from this range that "Red_k-free for fixed small k" is a finite family.
6. Heuristic [heuristic, `randwalk.py`]: 300 random walks from random 12-vertex classes by random one-edge extensions to n=18,19 (dense, d~2-5): all 300 graphs (240 + 60) have a Red pair; min |Z| = 2 in 92%, 3-4 otherwise. Not an exhaustive statement.
7. n=15, 16 (task 3, dense range) NOT done: the class counts at the top cell grow by a factor of about 11 per n ((12,10) 12,702; (13,11) 131,088; (14,12) 1,451,175), so (15,13) is about 1.6e7 and (16,14) about 1.8e8 classes, and the generator needs the full census of all sparser cells at the same n; the DP would need several hours at n=15.
   The pruned direct enumerator (enumred, closed-set (Red_k) pruning) is exact but its running time is dominated by partial graphs before any closed set is large, so it was no faster than the DP at n=11,12.
   Suggested next engineering step: a hit-all filter. If H' = H + e has no Red set of size <= k then every Red_k set of H meets e (the star of a set missing e is unchanged); this prunes the last extension level strongly but still needs the complete parent cells.
8. (Red') confirmed (see definitions).

## Conclusions and caveats
* [verified-here] No connected (Red)-free member of C with Delta <= 3 exists for 5 <= n <= 14. If this persisted for all n it would prove I11 outright by induction; the data say nothing about n >= 15, and the structures that stay Red_k-free for the largest k are the near-tight (slack 1..4) graphs, i.e. exactly where a discharging proof must work.
* [derived-here] Lemma R, Lemma L, (Red') above (short proofs given); they are used by the code, which was validated as described.
* The count of 2,452,070 classes at n=14 and the other cell counts are verified against the independent L012 tools only for n <= 11 (all cells), (12,10,tau=5) and (13,10/11, tau>=6); the remaining cells rest on the DP and on the correctness of the filter (the generator was cross-checked at the cells above).
* Delta <= 3 only (as required by the vertex reduction); graphs with higher degree are (Red) by Z=T={v}.
