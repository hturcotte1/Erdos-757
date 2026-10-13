# Forbidden ordered AP configurations, n <= 7

**Question.** Which labeled ordered AP patterns (vertices = ranks, edge (i,j,k): 2x_j = x_i+x_k) are
realizable by a (4,5)-set, and what are the minimal forbidden sub-patterns? (RESEARCH_PLAN P1.3; the
realizability half of Track U2 CEGAR.)

**Method.** `e757/realizability.py` (new). Order feasibility is decided exactly by Stiemke duality with an
exact (Fraction, Bland) simplex: either a strictly increasing rational point or a rational Farkas
certificate y with E^T y >= 0, != 0, both re-verified in exact arithmetic. Forced extra APs and forced
parallelograms (x_a+x_d = x_b+x_c, which gives two coincident distances) are identities on the
solution space, detected by row-space membership over Q. A 4-set violates (4,5) iff it has >= 2 coincident
distances, each an AP or a parallelogram, so these cover everything (plus two listed edges in one 4-set,
which the linearity filter excludes here). Realizable patterns get a generic exact point that is re-verified
with `core.ap_edges` / `core.is_45_set`. Floats are not used anywhere.

Enumeration: every pattern with each interior vertex the midpoint of at most one edge and linear (two edges
share <= 1 vertex). Minimal cores (S, relation) are enumerated exhaustively: S forces the relation (order
infeasibility, an unlisted AP T not in S, or a parallelogram on 4 vertices) and no S minus one edge does.
Forced relations only involve vertices in supp(S), so every core appears at n = |supp(S)|. Dedup under the
reflection j -> n-1-j.

**Commands** (seconds; < 15 s total):
`cd experiments/20261013-2257-forbidden-library && PYTHONPATH=../.. python3 enumerate.py 7 ../../data/forbidden_ordered_n7.json`
Cross-check (slow, ~minutes, uses the independent float-LP + sympy path in ordered_search): `crosscheck.py`.
No randomness in the enumeration; `realize_exact` uses seed 0.

**Results** [verified-here]. Patterns by class (precedence: order-infeasible > extra AP > repeated diff):

| n | total | realizable | order-infeasible | forced extra AP | forced repeated difference |
|---|---|---|---|---|---|
| 3 | 2 | 2 | 0 | 0 | 0 |
| 4 | 5 | 5 | 0 | 0 | 0 |
| 5 | 24 | 22 | 2 | 0 | 0 |
| 6 | 189 | 142 | 45 | 0 | 2 |
| 7 | 2364 | 1312 | 1006 | 22 | 24 |

Minimal cores up to reflection: 44 (S, relation) pairs on 20 distinct edge sets S.
By (n, kind): 5/order 1; 6/order 1; 6/diff 3; 7/order 6; 7/extra_ap 16; 7/diff 17.
By edge count: order: 2 edges x2, 4 edges x4, 5 edges x2; diff: 3 edges x3, 5 edges x17; extra_ap: 4 edges x8,
5 edges x8. No core with 1 edge; the smallest ones are the 2-edge order cores (0,1,4),(0,2,3) and (0,3,4),(1,2,5).
Note the simplest forced-extra/forced-diff cores need n >= 6 (diff) and n >= 7 (extra AP).

All 44 cores have <= 5 edges (also in `data/forbidden_ordered_n7.json`; relation for `diff` = (a,b,c,d)
meaning x_a+x_d=x_b+x_c is forced, for `extra_ap` = (a,b,c) is the forced unlisted AP):
- n=5 order rel=None edges=[(0, 1, 4), (0, 2, 3)]
- n=6 order rel=None edges=[(0, 3, 4), (1, 2, 5)]
- n=6 diff rel=[0, 1, 3, 4] edges=[(0, 1, 2), (0, 3, 5), (2, 4, 5)]
- n=6 diff rel=[1, 2, 3, 4] edges=[(0, 1, 2), (0, 3, 5), (2, 4, 5)]
- n=6 diff rel=[1, 3, 4, 5] edges=[(0, 1, 2), (0, 3, 5), (2, 4, 5)]
- n=7 extra_ap rel=[1, 3, 4] edges=[(0, 1, 2), (0, 3, 5), (0, 4, 6), (2, 5, 6)]
- n=7 order rel=None edges=[(0, 1, 2), (0, 3, 6), (1, 4, 5), (2, 5, 6)]
- n=7 extra_ap rel=[3, 4, 5] edges=[(0, 1, 2), (0, 3, 6), (1, 4, 6), (2, 5, 6)]
- n=7 extra_ap rel=[1, 4, 6] edges=[(0, 1, 2), (0, 3, 6), (2, 5, 6), (3, 4, 5)]
- n=7 extra_ap rel=[0, 3, 5] edges=[(0, 1, 2), (0, 4, 6), (1, 3, 4), (2, 5, 6)]
- n=7 extra_ap rel=[2, 3, 4] edges=[(0, 1, 2), (0, 4, 6), (1, 3, 5), (2, 5, 6)]
- n=7 extra_ap rel=[1, 3, 5] edges=[(0, 1, 2), (0, 4, 6), (2, 3, 4), (2, 5, 6)]
- n=7 extra_ap rel=[1, 2, 4] edges=[(0, 1, 3), (0, 2, 5), (0, 4, 6), (3, 5, 6)]
- n=7 order rel=None edges=[(0, 1, 3), (0, 2, 6), (1, 4, 5), (3, 5, 6)]
- n=7 extra_ap rel=[1, 4, 6] edges=[(0, 1, 3), (0, 2, 6), (2, 4, 5), (3, 5, 6)]
- n=7 order rel=None edges=[(0, 1, 4), (0, 3, 6), (1, 2, 5), (2, 4, 6)]
- n=7 order rel=None edges=[(0, 1, 5), (0, 2, 6), (1, 3, 6), (2, 4, 5)]
- n=7 diff rel=[0, 1, 2, 4] edges=[(0, 1, 3), (0, 2, 5), (0, 4, 6), (1, 5, 6), (2, 3, 4)]
- n=7 diff rel=[0, 1, 3, 5] edges=[(0, 1, 3), (0, 2, 5), (0, 4, 6), (1, 5, 6), (2, 3, 4)]
- n=7 diff rel=[0, 3, 5, 6] edges=[(0, 1, 3), (0, 2, 5), (0, 4, 6), (1, 5, 6), (2, 3, 4)]
- n=7 diff rel=[1, 2, 3, 4] edges=[(0, 1, 3), (0, 2, 5), (0, 4, 6), (1, 5, 6), (2, 3, 4)]
- n=7 diff rel=[1, 2, 4, 5] edges=[(0, 1, 3), (0, 2, 5), (0, 4, 6), (1, 5, 6), (2, 3, 4)]
- n=7 diff rel=[2, 3, 4, 5] edges=[(0, 1, 3), (0, 2, 5), (0, 4, 6), (1, 5, 6), (2, 3, 4)]
- n=7 extra_ap rel=[1, 2, 3] edges=[(0, 1, 3), (0, 2, 5), (0, 4, 6), (1, 5, 6), (2, 3, 4)]
- n=7 extra_ap rel=[1, 3, 5] edges=[(0, 1, 3), (0, 2, 5), (0, 4, 6), (1, 5, 6), (2, 3, 4)]
- n=7 extra_ap rel=[3, 4, 5] edges=[(0, 1, 3), (0, 2, 5), (0, 4, 6), (1, 5, 6), (2, 3, 4)]
- n=7 diff rel=[0, 1, 2, 4] edges=[(0, 1, 3), (0, 2, 5), (1, 4, 6), (2, 3, 4), (3, 5, 6)]
- n=7 diff rel=[0, 1, 3, 5] edges=[(0, 1, 3), (0, 2, 5), (1, 4, 6), (2, 3, 4), (3, 5, 6)]
- n=7 diff rel=[0, 1, 5, 6] edges=[(0, 1, 3), (0, 2, 5), (1, 4, 6), (2, 3, 4), (3, 5, 6)]
- n=7 diff rel=[0, 2, 4, 6] edges=[(0, 1, 3), (0, 2, 5), (1, 4, 6), (2, 3, 4), (3, 5, 6)]
- n=7 diff rel=[1, 2, 3, 4] edges=[(0, 1, 3), (0, 2, 5), (1, 4, 6), (2, 3, 4), (3, 5, 6)]
- n=7 diff rel=[1, 2, 4, 5] edges=[(0, 1, 3), (0, 2, 5), (1, 4, 6), (2, 3, 4), (3, 5, 6)]
- n=7 extra_ap rel=[0, 3, 6] edges=[(0, 1, 3), (0, 2, 5), (1, 4, 6), (2, 3, 4), (3, 5, 6)]
- n=7 extra_ap rel=[1, 2, 3] edges=[(0, 1, 3), (0, 2, 5), (1, 4, 6), (2, 3, 4), (3, 5, 6)]
- n=7 extra_ap rel=[1, 3, 5] edges=[(0, 1, 3), (0, 2, 5), (1, 4, 6), (2, 3, 4), (3, 5, 6)]
- n=7 order rel=None edges=[(0, 1, 3), (0, 4, 6), (1, 2, 4), (1, 5, 6), (2, 3, 5)]
- n=7 order rel=None edges=[(0, 1, 4), (0, 3, 6), (1, 2, 3), (1, 5, 6), (2, 4, 5)]
- n=7 diff rel=[0, 1, 2, 5] edges=[(0, 1, 4), (0, 3, 6), (1, 2, 3), (2, 5, 6), (3, 4, 5)]
- n=7 diff rel=[0, 1, 5, 6] edges=[(0, 1, 4), (0, 3, 6), (1, 2, 3), (2, 5, 6), (3, 4, 5)]
- n=7 diff rel=[0, 2, 4, 6] edges=[(0, 1, 4), (0, 3, 6), (1, 2, 3), (2, 5, 6), (3, 4, 5)]
- n=7 diff rel=[1, 2, 3, 4] edges=[(0, 1, 4), (0, 3, 6), (1, 2, 3), (2, 5, 6), (3, 4, 5)]
- n=7 diff rel=[1, 2, 4, 5] edges=[(0, 1, 4), (0, 3, 6), (1, 2, 3), (2, 5, 6), (3, 4, 5)]
- n=7 extra_ap rel=[1, 3, 5] edges=[(0, 1, 4), (0, 3, 6), (1, 2, 3), (2, 5, 6), (3, 4, 5)]
- n=7 extra_ap rel=[2, 3, 4] edges=[(0, 1, 4), (0, 3, 6), (1, 2, 3), (2, 5, 6), (3, 4, 5)]