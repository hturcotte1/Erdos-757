# Forbidden ordered AP configurations: n = 8 library and catalogue of small configurations

All statements below are [verified-here] unless tagged otherwise: they are exact computations with
`e757/realizability.py` (`order_feasible`, `forced_relations`, `forbidden_core`, `realize_exact`), reproduced by
the commands at the end and (for triangle and Pasch) by `tests/test_forbidden_catalogue.py`. The algebraic
one-line reasons are my own hand derivations, tagged [derived-here]; each is confirmed by the computation
(the forbidden verdict is the oracle's, the reason just names the mechanism).

## Questions

1. (Deliverable 1) Extend the library of minimal forbidden cores `(S, relation)` of ordered midpoint patterns
   from `|supp(S)| <= 7` to `|supp(S)| = 8`.
2. (Deliverable 2) For every connected linear 3-uniform configuration with <= 4 edges on <= 8 vertices, list
   every midpoint labeling (up to symmetry) and every vertex order consistent with it, with the exact verdict
   of `realize_exact`.

## Definitions

- Configuration H: a connected linear 3-uniform hypergraph (any two edges share <= 1 vertex), 1 to 4 edges,
  <= 8 vertices, up to isomorphism. There are 11 (H0..H10 below). Four-edge hypertrees (path or star of 4
  edges, 9 vertices) exceed 8 vertices and are not in scope. Disconnected configurations are not tabulated
  (see "Disconnected" below).
- Labeling: one midpoint chosen in each edge, up to automorphisms of H. `mid(x,y)=m` reads x_m = (x_x+x_y)/2.
- Order: a bijection vertices -> ranks with every midpoint strictly between its two endpoints. Orders are
  identified when they give the same rank-form pattern (edge set `(i,j,k)`, `2x_j = x_i+x_k`, ranks
  0..n-1), up to reflection `j -> n-1-j`; this also identifies orders related by an automorphism of the
  labeled configuration.
- Verdict of an order, from `realize_exact(n, rank_form)`: **R** = some strictly increasing rational point
  has exactly these APs and is a (4,5)-set (an exact integer realization is given, re-checked here with
  `core.ap_edges` and `core.is_45_set`); **O** = order-infeasible (no strictly increasing solution of the AP
  equations; a minimal infeasible sub-pattern is printed); **E** = the equations force an extra, unlisted AP;
  **D** = the equations force a repeated difference (parallelogram x_a+x_d = x_b+x_c, the forced relation
  is printed). Precedence O > E > D as in the n <= 7 library.
- A labeling is **forbidden in every order** if no consistent order has verdict R.
- Letters a, b, c, ... are the vertex names of the configuration as listed under each heading. In a
  realization, `a=0, b=4, ...` gives the coordinate of each vertex, listed in increasing order.
- Realization numbers are small integers found by a randomized search that is re-verified exactly
  (fallback `realize_exact`); they are examples, not canonical.

## Part 1. n = 8 library (complete)

Complete, run as a background job (`run.log` of this directory shows 597 s for n = 8 in one process, under
heavy machine load). File: `data/forbidden_ordered_n8.json` (same format as the n7 file; only cores with
`|supp(S)| = 8`; deduplicated under reflection; the n <= 7 cores stay in `data/forbidden_ordered_n7.json`).

Patterns at n = 8 (linear, each interior vertex the midpoint of at most one edge; precedence
order-infeasible > extra AP > repeated difference):

| n | total | realizable | order-infeasible | forced extra AP | forced repeated difference |
|---|---|---|---|---|---|
| 8 | 46281 | 16568 | 28697 | 498 | 518 |

(For n = 3..7 see `experiments/20261013-2257-forbidden-library/README.md`; its table has n = 7: 2364 / 1312 / 1006 / 22 / 24.)

Minimal cores at n = 8: 243 pairs (S, relation) up to reflection, by kind `{"8/diff": 87, "8/extra_ap": 22, "8/order": 134}`;
by edge count: 4 edges: 69, 5 edges: 83, 6 edges: 91 (none with fewer than 4 edges; the largest has 6
edges). Together with the 44 cores of n <= 7 the library now holds 287 cores.

Cores with <= 4 edges (n = 7 and n = 8 files), by the underlying configuration (`tally_cores.py`):

```
n=5 two edges sharing a vertex [2 edges] kind=order: 1
n=6 triangle [3 edges] kind=diff: 3
n=6 two disjoint edges [2 edges] kind=order: 1
n=7 star3+transversal [4 edges] kind=extra_ap: 4
n=7 two triangles sharing two edges [4 edges] kind=extra_ap: 4
n=7 two triangles sharing two edges [4 edges] kind=order: 4
n=8 4-cycle [4 edges] kind=diff: 10
n=8 4-cycle [4 edges] kind=order: 28
n=8 triangle+pendant at corner [4 edges] kind=order: 9
n=8 triangle+pendant at private vertex [4 edges] kind=order: 22
```

Reading: apart from the three K30/K31 families of small cores (n = 5 two-edge order core, n = 6 two disjoint
edges order core, n = 6 triangle diff cores), every minimal core with <= 4 edges lives on one of four 4-edge
configurations: star3+transversal and two-triangles-sharing-two-edges at n = 7 (extra AP and order cores),
4-cycle, triangle+pendant at a corner and triangle+pendant at a private vertex at n = 8. The Pasch
configuration carries no minimal core, and no core with 3 edges other than the triangle diff cores exists.

## Part 2. Cross-checks between the two independent code paths

- `crosscheck_catalogue.py` (output `crosscheck_catalogue.out`): the set of midpoint-injective, connected,
  full-support patterns with <= 4 edges produced by `enumerate.py`'s pattern generator equals, for every
  n = 3..8, the set produced by the permutation-based catalogue (`catalogue.py`): 1, 0, 7, 40, 662, 6154
  patterns (up to reflection) at n = 3, 4, 5, 6, 7, 8. EQUAL in all six cases.
- Failure modes among all midpoint-injective labelings (`failure_modes.py`, `failure_modes.out`): of all
  failing orders, the order-infeasible ones have a minimal infeasible sub-pattern with 2 edges (K30, monotone
  midpoints) in 3688 cases and with 4 edges in 63 cases; there are 111 forced repeated differences and 8
  forced extra APs. The counts of 4-edge order cores (4 + 9 + 22 + 28 = 63), diff cores (10) and extra-AP cores
  (8) equal exactly the 4-edge core counts of the n = 7 and n = 8 libraries in the tally above, so the
  catalogue and the library agree.

  Totals: `TOTAL {'O(core 2 edges)': 3688, 'forced repeated difference': 111, 'O(core 4 edges)': 63, 'forced extra AP': 8}`

## Part 3. Summary by configuration

Counts of labelings and ordered patterns. R/O/E/D count ordered patterns (rank-forms up to reflection).
Non-injective labelings (two edges with the same midpoint) are included; they are never realizable.

| config | name | vertices | edges | labelings | midpoint-injective | labelings realizable in >=1 order | injective but forbidden in every order | ordered patterns | R | O | E | D |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| H0 | single edge | 3 | 1 | 1 | 1 | 1 | 0 | 1 | 1 | 0 | 0 | 0 |
| H1 | two edges sharing a vertex | 5 | 2 | 3 | 2 | 2 | 0 | 9 | 6 | 2 | 0 | 1 |
| H2 | star of three edges (common vertex) | 7 | 3 | 4 | 2 | 2 | 0 | 56 | 23 | 26 | 0 | 7 |
| H3 | path of three edges | 7 | 3 | 7 | 5 | 5 | 0 | 321 | 159 | 129 | 0 | 33 |
| H4 | TRIANGLE (three edges pairwise meeting in three distinct vertices) | 6 | 3 | 7 | 5 | 4 | 1 | 60 | 22 | 28 | 0 | 10 |
| H5 | triangle + pendant edge at a corner | 8 | 4 | 30 | 15 | 13 | 2 | 5040 | 936 | 3356 | 0 | 748 |
| H6 | star of three edges + transversal edge (three triangles) | 7 | 4 | 18 | 8 | 6 | 2 | 420 | 52 | 296 | 18 | 54 |
| H7 | triangle + pendant edge at an edge-private vertex | 8 | 4 | 30 | 15 | 14 | 1 | 5040 | 1110 | 3220 | 0 | 710 |
| H8 | 4-cycle of edges (no triangle) | 8 | 4 | 15 | 9 | 8 | 1 | 2544 | 585 | 1627 | 0 | 332 |
| H9 | two triangles sharing two edges | 7 | 4 | 24 | 11 | 10 | 1 | 642 | 99 | 448 | 32 | 63 |
| H10 | PASCH (four edges on six vertices) | 6 | 4 | 6 | 2 | 1 | 1 | 15 | 1 | 13 | 1 | 0 |

No configuration is forbidden outright: each of H0..H10 has a realizable labeling and order.

### Mechanisms (the complete list of reasons labelings are forbidden in every order) [derived-here]

Every labeling that is forbidden in every order falls into (at least) one of these classes: the generator
assigns the first applicable reason to each such row and no row fell through to "see orders" (rows below).
Each mechanism is persistent: it stays a violation in any larger AP set containing these APs (a K30
violation or a forced parallelogram does not depend on which other APs are listed). A forced extra AP (E)
is not persistent, since a larger pattern could list that AP; among midpoint-injective labelings, E occurs
only in the medial-triangle rows 6.18 and 9.19, where the forced parallelogram of mechanism 2 persists anyway.

1. **Shared midpoint** (not midpoint-injective). If x_m = (x_p+x_q)/2 = (x_r+x_s)/2 then x_p+x_q = x_r+x_s
   with p, q, r, s distinct (linearity): a parallelogram, so the 4-set {p,q,r,s} has two coincident
   distances. The oracle returns O (the two intervals [p,q], [r,s] cannot be nested around the same point
   in the chosen order), D (forced x_r - x_p = x_q - x_s) or, with a fourth edge, E, depending on the order.
2. **Medial triangle** (K31). Corners a, b, d with edges {a,b,c}, {a,d,e}, {b,d,f} and the three midpoints
   c, e, f all edge-private: x_f - x_e = (x_b - x_a)/2 = x_c - x_a, so x_a + x_f = x_c + x_e with
   a, c, e, f distinct, a forced repeated difference (or order-infeasible in the other orders).
   Any labeling containing a medial triangle is forbidden in every order: rows 4.7, 5.28, 5.30, 6.11, 6.18,
   7.30, 9.19.
3. **Medial 4-cycle** (Varignon). Four edges {a,b,c}, {a,d,e}, {b,f,g}, {d,f,h} (a 4-cycle of edges on corners
   a, b, f, d) with midpoints c, e, g, h all edge-private: c + h = (a+b+d+f)/2 = e + g. This is a new
   forbidden configuration with no triangle inside it: row 8.15 (43 orders: 33 O, 10 D).
4. **Monotone midpoints** (K30) in every consistent order. Row 10.6 (a Pasch labeling): its single consistent
   order violates K30 (edges (b,d,f) and (e,c,f) share the top endpoint f, b < e forces d < c, but the order
   is b < e < c < d).

## Part 4. The triangle (H4) [verified-here]

Edges {a,b,c}, {a,d,e}, {b,d,f}; corners a, b, d (vertices in two edges); edge-private c, e, f. All 720 vertex
orders were run: 60 distinct ordered patterns up to reflection: 22 R, 28 O, 10 D.

| labeling | midpoints | verdict | reason / example |
|---|---|---|---|
| 4.1, 4.2 | a is the midpoint of two edges (shared midpoint) | forbidden in every order | mechanism 1 |
| 4.3 | a=mid(b,c), d=mid(a,e), b=mid(d,f): all three midpoints corners, cyclic | realizable in 3 of 3 orders | f=0, b=7, a=11, d=14, c=15, e=17 |
| 4.4 | two corner midpoints (a, d), one private (f=mid(b,d)) | realizable in 8 of 11 orders | b=0, a=2, c=4, f=5, d=10, e=18 |
| 4.5 | two corner midpoints (a, d), one private (e=mid(a,d)) | realizable in 4 of 5 orders | b=0, a=1, c=2, e=5, d=9, f=18 |
| 4.6 | one corner midpoint (a), two private (e, f) | realizable in 7 of 15 orders | d=0, f=2, b=4, e=5, a=10, c=16 |
| 4.7 | all three midpoints private (c, e, f) | **forbidden in every order** (2 orders: D and O) | medial triangle: x_a+x_f = x_c+x_e |

So: a midpoint-injective triangle labeling is realizable iff at least one midpoint is a corner, i.e. iff it is
not the medial triangle. The 12 failing orders of the four realizable labelings are all K30
violations (2-edge order cores); the medial labeling 4.7 has one D order and one O order. The full order lists with the printed reasons are in the section below.

## Part 5. Pasch (H10) [verified-here]

Edges {a,b,c}, {a,d,e}, {b,d,f}, {c,e,f}: four edges on six vertices, every vertex in two edges. 15 ordered
patterns up to reflection: 1 R, 13 O, 1 E. Six labelings:

- 10.1 to 10.4: shared midpoint, forbidden (mechanism 1).
- 10.5 `mid(b,c)=a; mid(a,e)=d; mid(d,f)=b; mid(e,f)=c`: **realizable in exactly one of its 3 orders**, `e d c a b f`
  with e=0, d=4, c=7, a=8, b=9, f=14. This 6-point set {0,4,7,8,9,14} has APs 7-8-9, 0-4-8, 4-9-14, 0-7-14
  exactly, is a (4,5)-set, and has h = 4 (`core.alpha`), so it attains f(6) = 4 and is midpoint-saturated
  (m = n-2 = 4: the two non-midpoints e, f are the extremes).
- 10.6 `mid(b,c)=a; mid(a,e)=d; mid(b,d)=f; mid(e,f)=c`: forbidden (its single order is O by K30).

Hence **the Pasch configuration is realizable (as an induced configuration with exactly these four APs) in
exactly one ordered pattern, up to reflection**: `[(0,1,3), (0,2,5), (1,4,5), (2,3,4)]`. The single E
verdict (labeling 10.3) means the equations force a fifth AP; that case is a 5-edge configuration outside
this catalogue and is not claimed forbidden in the persistent sense. Every other non-R Pasch order is O
(K30 or a longer infeasibility), which is persistent.

## Part 6. Disconnected configurations

Not tabulated beyond one case, run exhaustively: two disjoint edges {a,b,c}, {d,e,f}. There are 7 ordered
patterns up to reflection: 6 R and 1 O. The O pattern is `[(0,3,4), (1,2,5)]`, which is exactly the n = 6
two-edge core of the library (K30: i < i', k < k' forces j < j'). So interleaving two disjoint APs is only
restricted by K30. Larger disconnected configurations (e.g. an edge plus a "V") are not covered by this
catalogue; their n = 8 patterns are included in the n = 8 library statistics above. [heuristic: independent
components can be rescaled and translated generically, so I expect realizability to be componentwise; not
checked exhaustively here.]

## Part 7. All labelings and orders (every row carries a verdict)

Orders and their reasons are listed explicitly for configurations with <= 6 vertices (H0, H1, H4, H10).
For 7- and 8-vertex configurations the table lists all labelings with order counts; each realizable
labeling has one example realization, and the full verified catalogue is in `catalogue.json.gz`
(with every order as a rank-form pattern, its vertex order, verdict and forced relation).
`catalogue_tables_orders_7_8_vertices.md` holds the per-labeling example orders for H2, H3, H5..H9.

### H0: single edge  (3 vertices, 1 edges)

Edges: {a,b,c}.  Labelings up to Aut(H): 1.

| # | labeling (midpoints) | midpoint-injective | orders | R | O | E | D | verdict |
|---|---|---|---|---|---|---|---|---|
| 0.1 | mid(b,c)=a | yes | 1 | 1 | 0 | 0 | 0 | REALIZABLE in 1 of 1 orders |

**0.1** `mid(b,c)=a`
- order `b a c` : R  realization b=0, a=1, c=2

### H1: two edges sharing a vertex  (5 vertices, 2 edges)

Edges: {a,b,c}, {a,d,e}.  Labelings up to Aut(H): 3.

| # | labeling (midpoints) | midpoint-injective | orders | R | O | E | D | verdict |
|---|---|---|---|---|---|---|---|---|
| 1.1 | mid(b,c)=a; mid(d,e)=a | no | 2 | 0 | 1 | 0 | 1 | FORBIDDEN in every order (O/D) -- two edges share a midpoint m: x_p+x_q = 2m = x_r+x_s, a parallelogram |
| 1.2 | mid(b,c)=a; mid(a,e)=d | yes | 3 | 3 | 0 | 0 | 0 | REALIZABLE in 3 of 3 orders |
| 1.3 | mid(a,c)=b; mid(a,e)=d | yes | 4 | 3 | 1 | 0 | 0 | REALIZABLE in 3 of 4 orders |

**1.1** `mid(b,c)=a; mid(d,e)=a`
- order `b d a c e` : O: no increasing point; minimal order-infeasible sub-pattern (b,a,c), (d,a,e)
- order `b d a e c` : D: forces x_d-x_b = x_c-x_e

**1.2** `mid(b,c)=a; mid(a,e)=d`
- order `b a c d e` : R  realization b=0, a=1, c=2, d=5, e=9
- order `b a d c e` : R  realization b=0, a=4, d=7, c=8, e=10
- order `b a d e c` : R  realization b=0, a=5, d=6, e=7, c=10

**1.3** `mid(a,c)=b; mid(a,e)=d`
- order `a b c d e` : R  realization a=0, b=2, c=4, d=5, e=10
- order `c b a d e` : R  realization c=0, b=3, a=6, d=7, e=8
- order `a b d c e` : R  realization a=0, b=4, d=5, c=8, e=10
- order `a b d e c` : O: no increasing point; minimal order-infeasible sub-pattern (a,b,c), (a,d,e)

### H2: star of three edges (common vertex)  (7 vertices, 3 edges)

Edges: {a,b,c}, {a,d,e}, {a,f,g}.  Labelings up to Aut(H): 4.

| # | labeling (midpoints) | midpoint-injective | orders | R | O | E | D | verdict |
|---|---|---|---|---|---|---|---|---|
| 2.1 | mid(b,c)=a; mid(d,e)=a; mid(f,g)=a | no | 5 | 0 | 4 | 0 | 1 | FORBIDDEN in every order (O/D) -- two edges share a midpoint m: x_p+x_q = 2m = x_r+x_s, a parallelogram |
| 2.2 | mid(b,c)=a; mid(d,e)=a; mid(a,g)=f | no | 12 | 0 | 6 | 0 | 6 | FORBIDDEN in every order (O/D) -- two edges share a midpoint m: x_p+x_q = 2m = x_r+x_s, a parallelogram |
| 2.3 | mid(b,c)=a; mid(a,e)=d; mid(a,g)=f | yes | 21 | 16 | 5 | 0 | 0 | REALIZABLE in 16 of 21 orders |
| 2.4 | mid(a,c)=b; mid(a,e)=d; mid(a,g)=f | yes | 18 | 7 | 11 | 0 | 0 | REALIZABLE in 7 of 18 orders |

### H3: path of three edges  (7 vertices, 3 edges)

Edges: {a,b,c}, {a,d,e}, {b,f,g}.  Labelings up to Aut(H): 7.

| # | labeling (midpoints) | midpoint-injective | orders | R | O | E | D | verdict |
|---|---|---|---|---|---|---|---|---|
| 3.1 | mid(b,c)=a; mid(d,e)=a; mid(f,g)=b | no | 26 | 0 | 14 | 0 | 12 | FORBIDDEN in every order (O/D) -- two edges share a midpoint m: x_p+x_q = 2m = x_r+x_s, a parallelogram |
| 3.2 | mid(b,c)=a; mid(d,e)=a; mid(b,g)=f | no | 58 | 0 | 37 | 0 | 21 | FORBIDDEN in every order (O/D) -- two edges share a midpoint m: x_p+x_q = 2m = x_r+x_s, a parallelogram |
| 3.3 | mid(b,c)=a; mid(a,e)=d; mid(f,g)=b | yes | 37 | 34 | 3 | 0 | 0 | REALIZABLE in 34 of 37 orders |
| 3.4 | mid(b,c)=a; mid(a,e)=d; mid(b,g)=f | yes | 89 | 58 | 31 | 0 | 0 | REALIZABLE in 58 of 89 orders |
| 3.5 | mid(a,b)=c; mid(d,e)=a; mid(f,g)=b | yes | 11 | 10 | 1 | 0 | 0 | REALIZABLE in 10 of 11 orders |
| 3.6 | mid(a,b)=c; mid(d,e)=a; mid(b,g)=f | yes | 45 | 29 | 16 | 0 | 0 | REALIZABLE in 29 of 45 orders |
| 3.7 | mid(a,b)=c; mid(a,e)=d; mid(b,g)=f | yes | 55 | 28 | 27 | 0 | 0 | REALIZABLE in 28 of 55 orders |

### H4: TRIANGLE (three edges pairwise meeting in three distinct vertices)  (6 vertices, 3 edges)

Edges: {a,b,c}, {a,d,e}, {b,d,f}.  Labelings up to Aut(H): 7.

| # | labeling (midpoints) | midpoint-injective | orders | R | O | E | D | verdict |
|---|---|---|---|---|---|---|---|---|
| 4.1 | mid(b,c)=a; mid(d,e)=a; mid(d,f)=b | no | 16 | 0 | 10 | 0 | 6 | FORBIDDEN in every order (O/D) -- two edges share a midpoint m: x_p+x_q = 2m = x_r+x_s, a parallelogram |
| 4.2 | mid(b,c)=a; mid(d,e)=a; mid(b,d)=f | no | 8 | 0 | 5 | 0 | 3 | FORBIDDEN in every order (O/D) -- two edges share a midpoint m: x_p+x_q = 2m = x_r+x_s, a parallelogram |
| 4.3 | mid(b,c)=a; mid(a,e)=d; mid(d,f)=b | yes | 3 | 3 | 0 | 0 | 0 | REALIZABLE in 3 of 3 orders |
| 4.4 | mid(b,c)=a; mid(a,e)=d; mid(b,d)=f | yes | 11 | 8 | 3 | 0 | 0 | REALIZABLE in 8 of 11 orders |
| 4.5 | mid(b,c)=a; mid(a,d)=e; mid(b,f)=d | yes | 5 | 4 | 1 | 0 | 0 | REALIZABLE in 4 of 5 orders |
| 4.6 | mid(b,c)=a; mid(a,d)=e; mid(b,d)=f | yes | 15 | 7 | 8 | 0 | 0 | REALIZABLE in 7 of 15 orders |
| 4.7 | mid(a,b)=c; mid(a,d)=e; mid(b,d)=f | yes | 2 | 0 | 1 | 0 | 1 | FORBIDDEN in every order (O/D) -- contains a medial triangle (K31) |

**4.1** `mid(b,c)=a; mid(d,e)=a; mid(d,f)=b`
- order `d b f a e c` : O: no increasing point; minimal order-infeasible sub-pattern (d,a,e), (b,a,c)
- order `d b f a c e` : D: forces x_b-x_d = x_e-x_c
- order `f b d a c e` : O: no increasing point; minimal order-infeasible sub-pattern (b,a,c), (d,a,e)
- order `f b d a e c` : D: forces x_b-x_f = x_c-x_e
- order `d b a f e c` : O: no increasing point; minimal order-infeasible sub-pattern (d,a,e), (b,a,c)
- order `d b a f c e` : D: forces x_b-x_d = x_e-x_c
- order `d b a e f c` : O: no increasing point; minimal order-infeasible sub-pattern (d,a,e), (b,a,c)
- order `d b a c f e` : D: forces x_b-x_d = x_e-x_c
- order `c d a e b f` : D: forces x_d-x_c = x_f-x_a
- order `d b a e c f` : O: no increasing point; minimal order-infeasible sub-pattern (d,a,e), (b,a,c)
- order `d b a c e f` : O: no increasing point; minimal order-infeasible sub-pattern (d,b,f), (d,a,e)
- order `d c a e b f` : O: no increasing point; minimal order-infeasible sub-pattern (c,e,b), (a,e,f)
- order `c d a b e f` : O: no increasing point; minimal order-infeasible sub-pattern (c,a,b), (d,a,e)
- order `c d a b f e` : O: no increasing point; minimal order-infeasible sub-pattern (d,a,e), (d,b,f)
- order `d c a b e f` : D: forces x_c-x_d = x_e-x_b
- order `d c a b f e` : O: no increasing point; minimal order-infeasible sub-pattern (d,a,e), (d,b,f)

**4.2** `mid(b,c)=a; mid(d,e)=a; mid(b,d)=f`
- order `b f d a c e` : O: no increasing point; minimal order-infeasible sub-pattern (b,a,c), (d,a,e)
- order `b f d a e c` : D: forces x_d-x_b = x_c-x_e
- order `b f e a d c` : D: forces x_e-x_b = x_c-x_d
- order `b e a c f d` : O: no increasing point; minimal order-infeasible sub-pattern (b,c,f), (a,c,d)
- order `b e a f c d` : O: no increasing point; minimal order-infeasible sub-pattern (b,f,d), (e,a,d)
- order `b e f a d c` : D: forces x_e-x_b = x_c-x_d
- order `e b a f d c` : O: no increasing point; minimal order-infeasible sub-pattern (b,a,c), (b,f,d)
- order `b e a f d c` : O: no increasing point; minimal order-infeasible sub-pattern (b,f,d), (e,a,d)

**4.3** `mid(b,c)=a; mid(a,e)=d; mid(d,f)=b`
- order `f b a d c e` : R  realization f=0, b=7, a=11, d=14, c=15, e=17
- order `f b a d e c` : R  realization f=0, b=6, a=11, d=12, e=13, c=16
- order `f b a c d e` : R  realization f=0, b=5, a=9, c=10, d=11, e=17

**4.4** `mid(b,c)=a; mid(a,e)=d; mid(b,d)=f`
- order `b a c f d e` : R  realization b=0, a=2, c=4, f=5, d=10, e=18
- order `c a b f d e` : R  realization c=0, a=1, b=2, f=5, d=8, e=15
- order `b a f c d e` : R  realization b=0, a=3, f=5, c=6, d=10, e=17
- order `b f a d c e` : R  realization b=0, f=6, a=7, d=12, c=14, e=17
- order `b f a d e c` : R  realization b=0, f=5, a=7, d=10, e=13, c=14
- order `b f e d a c` : R  realization b=0, f=4, e=7, d=8, a=9, c=18
- order `b f a c d e` : O: no increasing point; minimal order-infeasible sub-pattern (f,d,e), (a,c,e)
- order `b a f d c e` : O: no increasing point; minimal order-infeasible sub-pattern (b,a,c), (b,f,d)
- order `c a d f b e` : R  realization c=0, a=7, d=12, f=13, b=14, e=17
- order `b a f d e c` : O: no increasing point; minimal order-infeasible sub-pattern (b,a,c), (b,f,d)
- order `b e f d a c` : R  realization b=0, e=10, f=14, d=17, a=18, c=20

**4.5** `mid(b,c)=a; mid(a,d)=e; mid(b,f)=d`
- order `b a c e d f` : R  realization b=0, a=1, c=2, e=5, d=9, f=18
- order `c a b e d f` : R  realization c=0, a=1, b=2, e=5, d=9, f=16
- order `b a e c d f` : R  realization b=0, a=4, e=7, c=8, d=10, f=20
- order `b a e d c f` : R  realization b=0, a=5, e=7, d=9, c=10, f=18
- order `b a e d f c` : O: no increasing point; minimal order-infeasible sub-pattern (b,a,c), (b,d,f)

**4.6** `mid(b,c)=a; mid(a,d)=e; mid(b,d)=f`
- order `d f b e a c` : R  realization d=0, f=2, b=4, e=5, a=10, c=16
- order `b a c f e d` : R  realization b=0, a=4, c=8, f=9, e=11, d=18
- order `b a c e f d` : O: no increasing point; minimal order-infeasible sub-pattern (b,f,d), (a,e,d)
- order `b f d e a c` : R  realization b=0, f=1, d=2, e=5, a=8, c=16
- order `d f e b a c` : R  realization d=0, f=4, e=8, b=9, a=11, c=14
- order `d e f b a c` : O: no increasing point; minimal order-infeasible sub-pattern (e,a,c), (f,b,c)
- order `b a f c e d` : R  realization b=0, a=6, f=10, c=12, e=13, d=20
- order `b a e c f d` : O: no increasing point; minimal order-infeasible sub-pattern (b,f,d), (a,e,d)
- order `b f a c e d` : O: no increasing point; minimal order-infeasible sub-pattern (b,e,d), (a,c,d)
- order `b a f e c d` : R  realization b=0, a=8, f=9, e=13, c=16, d=18
- order `b f a e d c` : R  realization b=0, f=7, a=8, e=11, d=14, c=16
- order `b a e f c d` : O: no increasing point; minimal order-infeasible sub-pattern (b,f,d), (a,e,d)
- order `b a f e d c` : O: no increasing point; minimal order-infeasible sub-pattern (b,a,c), (b,f,d)
- order `b f a e c d` : O: no increasing point; minimal order-infeasible sub-pattern (b,f,d), (b,a,c)
- order `b a e f d c` : O: no increasing point; minimal order-infeasible sub-pattern (b,f,d), (a,e,d)

**4.7** `mid(a,b)=c; mid(a,d)=e; mid(b,d)=f`
- order `a c b e f d` : D: forces x_c-x_a = x_f-x_e
- order `a c b f e d` : O: no increasing point; minimal order-infeasible sub-pattern (a,e,d), (b,f,d)

### H5: triangle + pendant edge at a corner  (8 vertices, 4 edges)

Edges: {a,b,c}, {a,d,e}, {a,f,g}, {b,d,h}.  Labelings up to Aut(H): 30.

| # | labeling (midpoints) | midpoint-injective | orders | R | O | E | D | verdict |
|---|---|---|---|---|---|---|---|---|
| 5.1 | mid(b,c)=a; mid(d,e)=a; mid(f,g)=a; mid(d,h)=b | no | 192 | 0 | 168 | 0 | 24 | FORBIDDEN in every order (O/D) -- two edges share a midpoint m: x_p+x_q = 2m = x_r+x_s, a parallelogram |
| 5.2 | mid(b,c)=a; mid(d,e)=a; mid(f,g)=a; mid(b,d)=h | no | 96 | 0 | 84 | 0 | 12 | FORBIDDEN in every order (O/D) -- two edges share a midpoint m: x_p+x_q = 2m = x_r+x_s, a parallelogram |
| 5.3 | mid(b,c)=a; mid(d,e)=a; mid(a,g)=f; mid(d,h)=b | no | 256 | 0 | 171 | 0 | 85 | FORBIDDEN in every order (O/D) -- two edges share a midpoint m: x_p+x_q = 2m = x_r+x_s, a parallelogram |
| 5.4 | mid(b,c)=a; mid(d,e)=a; mid(a,g)=f; mid(b,d)=h | no | 128 | 0 | 85 | 0 | 43 | FORBIDDEN in every order (O/D) -- two edges share a midpoint m: x_p+x_q = 2m = x_r+x_s, a parallelogram |
| 5.5 | mid(b,c)=a; mid(a,e)=d; mid(f,g)=a; mid(d,h)=b | no | 100 | 0 | 54 | 0 | 46 | FORBIDDEN in every order (O/D) -- two edges share a midpoint m: x_p+x_q = 2m = x_r+x_s, a parallelogram |
| 5.6 | mid(b,c)=a; mid(a,e)=d; mid(f,g)=a; mid(b,h)=d | no | 168 | 0 | 136 | 0 | 32 | FORBIDDEN in every order (O/D) -- two edges share a midpoint m: x_p+x_q = 2m = x_r+x_s, a parallelogram |
| 5.7 | mid(b,c)=a; mid(a,e)=d; mid(f,g)=a; mid(b,d)=h | no | 116 | 0 | 74 | 0 | 42 | FORBIDDEN in every order (O/D) -- two edges share a midpoint m: x_p+x_q = 2m = x_r+x_s, a parallelogram |
| 5.8 | mid(b,c)=a; mid(a,e)=d; mid(a,g)=f; mid(d,h)=b | yes | 152 | 107 | 45 | 0 | 0 | REALIZABLE in 107 of 152 orders |
| 5.9 | mid(b,c)=a; mid(a,e)=d; mid(a,g)=f; mid(b,h)=d | no | 280 | 0 | 206 | 0 | 74 | FORBIDDEN in every order (O/D) -- two edges share a midpoint m: x_p+x_q = 2m = x_r+x_s, a parallelogram |
| 5.10 | mid(b,c)=a; mid(a,e)=d; mid(a,g)=f; mid(b,d)=h | yes | 192 | 96 | 96 | 0 | 0 | REALIZABLE in 96 of 192 orders |
| 5.11 | mid(b,c)=a; mid(a,d)=e; mid(f,g)=a; mid(d,h)=b | no | 124 | 0 | 83 | 0 | 41 | FORBIDDEN in every order (O/D) -- two edges share a midpoint m: x_p+x_q = 2m = x_r+x_s, a parallelogram |
| 5.12 | mid(b,c)=a; mid(a,d)=e; mid(f,g)=a; mid(b,h)=d | no | 104 | 0 | 62 | 0 | 42 | FORBIDDEN in every order (O/D) -- two edges share a midpoint m: x_p+x_q = 2m = x_r+x_s, a parallelogram |
| 5.13 | mid(b,c)=a; mid(a,d)=e; mid(f,g)=a; mid(b,d)=h | no | 156 | 0 | 119 | 0 | 37 | FORBIDDEN in every order (O/D) -- two edges share a midpoint m: x_p+x_q = 2m = x_r+x_s, a parallelogram |
| 5.14 | mid(b,c)=a; mid(a,d)=e; mid(a,g)=f; mid(d,h)=b | yes | 184 | 97 | 87 | 0 | 0 | REALIZABLE in 97 of 184 orders |
| 5.15 | mid(b,c)=a; mid(a,d)=e; mid(a,g)=f; mid(b,h)=d | yes | 176 | 96 | 80 | 0 | 0 | REALIZABLE in 96 of 176 orders |
| 5.16 | mid(b,c)=a; mid(a,d)=e; mid(a,g)=f; mid(b,d)=h | yes | 264 | 84 | 180 | 0 | 0 | REALIZABLE in 84 of 264 orders |
| 5.17 | mid(a,c)=b; mid(a,e)=d; mid(f,g)=a; mid(d,h)=b | no | 120 | 0 | 77 | 0 | 43 | FORBIDDEN in every order (O/D) -- two edges share a midpoint m: x_p+x_q = 2m = x_r+x_s, a parallelogram |
| 5.18 | mid(a,c)=b; mid(a,e)=d; mid(f,g)=a; mid(b,d)=h | yes | 36 | 27 | 9 | 0 | 0 | REALIZABLE in 27 of 36 orders |
| 5.19 | mid(a,c)=b; mid(a,e)=d; mid(a,g)=f; mid(d,h)=b | no | 328 | 0 | 262 | 0 | 66 | FORBIDDEN in every order (O/D) -- two edges share a midpoint m: x_p+x_q = 2m = x_r+x_s, a parallelogram |
| 5.20 | mid(a,c)=b; mid(a,e)=d; mid(a,g)=f; mid(b,d)=h | yes | 104 | 42 | 62 | 0 | 0 | REALIZABLE in 42 of 104 orders |
| 5.21 | mid(a,c)=b; mid(a,d)=e; mid(f,g)=a; mid(d,h)=b | no | 128 | 0 | 87 | 0 | 41 | FORBIDDEN in every order (O/D) -- two edges share a midpoint m: x_p+x_q = 2m = x_r+x_s, a parallelogram |
| 5.22 | mid(a,c)=b; mid(a,d)=e; mid(f,g)=a; mid(b,h)=d | yes | 76 | 55 | 21 | 0 | 0 | REALIZABLE in 55 of 76 orders |
| 5.23 | mid(a,c)=b; mid(a,d)=e; mid(f,g)=a; mid(b,d)=h | yes | 108 | 49 | 59 | 0 | 0 | REALIZABLE in 49 of 108 orders |
| 5.24 | mid(a,c)=b; mid(a,d)=e; mid(a,g)=f; mid(d,h)=b | no | 320 | 0 | 254 | 0 | 66 | FORBIDDEN in every order (O/D) -- two edges share a midpoint m: x_p+x_q = 2m = x_r+x_s, a parallelogram |
| 5.25 | mid(a,c)=b; mid(a,d)=e; mid(a,g)=f; mid(b,h)=d | yes | 232 | 84 | 148 | 0 | 0 | REALIZABLE in 84 of 232 orders |
| 5.26 | mid(a,c)=b; mid(a,d)=e; mid(a,g)=f; mid(b,d)=h | yes | 312 | 75 | 237 | 0 | 0 | REALIZABLE in 75 of 312 orders |
| 5.27 | mid(a,b)=c; mid(a,d)=e; mid(f,g)=a; mid(d,h)=b | yes | 108 | 49 | 59 | 0 | 0 | REALIZABLE in 49 of 108 orders |
| 5.28 | mid(a,b)=c; mid(a,d)=e; mid(f,g)=a; mid(b,d)=h | yes | 48 | 0 | 27 | 0 | 21 | FORBIDDEN in every order (O/D) -- contains a medial triangle (K31) |
| 5.29 | mid(a,b)=c; mid(a,d)=e; mid(a,g)=f; mid(d,h)=b | yes | 312 | 75 | 237 | 0 | 0 | REALIZABLE in 75 of 312 orders |
| 5.30 | mid(a,b)=c; mid(a,d)=e; mid(a,g)=f; mid(b,d)=h | yes | 120 | 0 | 87 | 0 | 33 | FORBIDDEN in every order (O/D) -- contains a medial triangle (K31) |

### H6: star of three edges + transversal edge (three triangles)  (7 vertices, 4 edges)

Edges: {a,b,c}, {a,d,e}, {a,f,g}, {b,d,f}.  Labelings up to Aut(H): 18.

| # | labeling (midpoints) | midpoint-injective | orders | R | O | E | D | verdict |
|---|---|---|---|---|---|---|---|---|
| 6.1 | mid(b,c)=a; mid(d,e)=a; mid(f,g)=a; mid(d,f)=b | no | 24 | 0 | 21 | 3 | 0 | FORBIDDEN in every order (O/E) -- two edges share a midpoint m: x_p+x_q = 2m = x_r+x_s, a parallelogram |
| 6.2 | mid(b,c)=a; mid(d,e)=a; mid(a,g)=f; mid(d,f)=b | no | 28 | 0 | 18 | 0 | 10 | FORBIDDEN in every order (O/D) -- two edges share a midpoint m: x_p+x_q = 2m = x_r+x_s, a parallelogram |
| 6.3 | mid(b,c)=a; mid(d,e)=a; mid(a,g)=f; mid(b,d)=f | no | 20 | 0 | 16 | 0 | 4 | FORBIDDEN in every order (O/D) -- two edges share a midpoint m: x_p+x_q = 2m = x_r+x_s, a parallelogram |
| 6.4 | mid(b,c)=a; mid(d,e)=a; mid(a,f)=g; mid(d,f)=b | no | 36 | 0 | 27 | 0 | 9 | FORBIDDEN in every order (O/D) -- two edges share a midpoint m: x_p+x_q = 2m = x_r+x_s, a parallelogram |
| 6.5 | mid(b,c)=a; mid(d,e)=a; mid(a,f)=g; mid(b,d)=f | no | 12 | 0 | 7 | 0 | 5 | FORBIDDEN in every order (O/D) -- two edges share a midpoint m: x_p+x_q = 2m = x_r+x_s, a parallelogram |
| 6.6 | mid(b,c)=a; mid(a,e)=d; mid(a,g)=f; mid(d,f)=b | yes | 7 | 6 | 1 | 0 | 0 | REALIZABLE in 6 of 7 orders |
| 6.7 | mid(b,c)=a; mid(a,e)=d; mid(a,g)=f; mid(b,f)=d | no | 32 | 0 | 23 | 0 | 9 | FORBIDDEN in every order (O/D) -- two edges share a midpoint m: x_p+x_q = 2m = x_r+x_s, a parallelogram |
| 6.8 | mid(b,c)=a; mid(a,e)=d; mid(a,f)=g; mid(d,f)=b | yes | 21 | 11 | 10 | 0 | 0 | REALIZABLE in 11 of 21 orders |
| 6.9 | mid(b,c)=a; mid(a,e)=d; mid(a,f)=g; mid(b,f)=d | no | 40 | 0 | 33 | 7 | 0 | FORBIDDEN in every order (O/E) -- two edges share a midpoint m: x_p+x_q = 2m = x_r+x_s, a parallelogram |
| 6.10 | mid(b,c)=a; mid(a,e)=d; mid(a,f)=g; mid(b,d)=f | yes | 17 | 11 | 6 | 0 | 0 | REALIZABLE in 11 of 17 orders |
| 6.11 | mid(b,c)=a; mid(a,d)=e; mid(a,f)=g; mid(d,f)=b | yes | 10 | 0 | 5 | 0 | 5 | FORBIDDEN in every order (O/D) -- contains a medial triangle (K31) |
| 6.12 | mid(b,c)=a; mid(a,d)=e; mid(a,f)=g; mid(b,f)=d | yes | 29 | 10 | 19 | 0 | 0 | REALIZABLE in 10 of 29 orders |
| 6.13 | mid(a,c)=b; mid(a,e)=d; mid(a,g)=f; mid(d,f)=b | no | 18 | 0 | 14 | 4 | 0 | FORBIDDEN in every order (O/E) -- two edges share a midpoint m: x_p+x_q = 2m = x_r+x_s, a parallelogram |
| 6.14 | mid(a,c)=b; mid(a,e)=d; mid(a,f)=g; mid(d,f)=b | no | 44 | 0 | 36 | 0 | 8 | FORBIDDEN in every order (O/D) -- two edges share a midpoint m: x_p+x_q = 2m = x_r+x_s, a parallelogram |
| 6.15 | mid(a,c)=b; mid(a,e)=d; mid(a,f)=g; mid(b,d)=f | yes | 10 | 5 | 5 | 0 | 0 | REALIZABLE in 5 of 10 orders |
| 6.16 | mid(a,c)=b; mid(a,d)=e; mid(a,f)=g; mid(d,f)=b | no | 14 | 0 | 10 | 0 | 4 | FORBIDDEN in every order (O/D) -- two edges share a midpoint m: x_p+x_q = 2m = x_r+x_s, a parallelogram |
| 6.17 | mid(a,c)=b; mid(a,d)=e; mid(a,f)=g; mid(b,f)=d | yes | 40 | 9 | 31 | 0 | 0 | REALIZABLE in 9 of 40 orders |
| 6.18 | mid(a,b)=c; mid(a,d)=e; mid(a,f)=g; mid(d,f)=b | yes | 18 | 0 | 14 | 4 | 0 | FORBIDDEN in every order (O/E) -- contains a medial triangle (K31) |

### H7: triangle + pendant edge at an edge-private vertex  (8 vertices, 4 edges)

Edges: {a,b,c}, {a,d,e}, {b,f,g}, {c,d,h}.  Labelings up to Aut(H): 30.

| # | labeling (midpoints) | midpoint-injective | orders | R | O | E | D | verdict |
|---|---|---|---|---|---|---|---|---|
| 7.1 | mid(b,c)=a; mid(d,e)=a; mid(f,g)=b; mid(d,h)=c | no | 136 | 0 | 96 | 0 | 40 | FORBIDDEN in every order (O/D) -- two edges share a midpoint m: x_p+x_q = 2m = x_r+x_s, a parallelogram |
| 7.2 | mid(b,c)=a; mid(d,e)=a; mid(f,g)=b; mid(c,h)=d | no | 144 | 0 | 102 | 0 | 42 | FORBIDDEN in every order (O/D) -- two edges share a midpoint m: x_p+x_q = 2m = x_r+x_s, a parallelogram |
| 7.3 | mid(b,c)=a; mid(d,e)=a; mid(f,g)=b; mid(c,d)=h | no | 136 | 0 | 93 | 0 | 43 | FORBIDDEN in every order (O/D) -- two edges share a midpoint m: x_p+x_q = 2m = x_r+x_s, a parallelogram |
| 7.4 | mid(b,c)=a; mid(d,e)=a; mid(b,g)=f; mid(d,h)=c | no | 312 | 0 | 237 | 0 | 75 | FORBIDDEN in every order (O/D) -- two edges share a midpoint m: x_p+x_q = 2m = x_r+x_s, a parallelogram |
| 7.5 | mid(b,c)=a; mid(d,e)=a; mid(b,g)=f; mid(c,h)=d | no | 304 | 0 | 231 | 0 | 73 | FORBIDDEN in every order (O/D) -- two edges share a midpoint m: x_p+x_q = 2m = x_r+x_s, a parallelogram |
| 7.6 | mid(b,c)=a; mid(d,e)=a; mid(b,g)=f; mid(c,d)=h | no | 312 | 0 | 239 | 0 | 73 | FORBIDDEN in every order (O/D) -- two edges share a midpoint m: x_p+x_q = 2m = x_r+x_s, a parallelogram |
| 7.7 | mid(b,c)=a; mid(a,e)=d; mid(f,g)=b; mid(d,h)=c | yes | 68 | 61 | 7 | 0 | 0 | REALIZABLE in 61 of 68 orders |
| 7.8 | mid(b,c)=a; mid(a,e)=d; mid(f,g)=b; mid(c,h)=d | no | 136 | 0 | 94 | 0 | 42 | FORBIDDEN in every order (O/D) -- two edges share a midpoint m: x_p+x_q = 2m = x_r+x_s, a parallelogram |
| 7.9 | mid(b,c)=a; mid(a,e)=d; mid(f,g)=b; mid(c,d)=h | yes | 92 | 54 | 38 | 0 | 0 | REALIZABLE in 54 of 92 orders |
| 7.10 | mid(b,c)=a; mid(a,e)=d; mid(b,g)=f; mid(d,h)=c | yes | 184 | 107 | 77 | 0 | 0 | REALIZABLE in 107 of 184 orders |
| 7.11 | mid(b,c)=a; mid(a,e)=d; mid(b,g)=f; mid(c,h)=d | no | 312 | 0 | 239 | 0 | 73 | FORBIDDEN in every order (O/D) -- two edges share a midpoint m: x_p+x_q = 2m = x_r+x_s, a parallelogram |
| 7.12 | mid(b,c)=a; mid(a,e)=d; mid(b,g)=f; mid(c,d)=h | yes | 216 | 97 | 119 | 0 | 0 | REALIZABLE in 97 of 216 orders |
| 7.13 | mid(b,c)=a; mid(a,d)=e; mid(f,g)=b; mid(d,h)=c | yes | 84 | 55 | 29 | 0 | 0 | REALIZABLE in 55 of 84 orders |
| 7.14 | mid(b,c)=a; mid(a,d)=e; mid(f,g)=b; mid(c,h)=d | yes | 80 | 55 | 25 | 0 | 0 | REALIZABLE in 55 of 80 orders |
| 7.15 | mid(b,c)=a; mid(a,d)=e; mid(f,g)=b; mid(c,d)=h | yes | 132 | 49 | 83 | 0 | 0 | REALIZABLE in 49 of 132 orders |
| 7.16 | mid(b,c)=a; mid(a,d)=e; mid(b,g)=f; mid(d,h)=c | yes | 224 | 95 | 129 | 0 | 0 | REALIZABLE in 95 of 224 orders |
| 7.17 | mid(b,c)=a; mid(a,d)=e; mid(b,g)=f; mid(c,h)=d | yes | 200 | 95 | 105 | 0 | 0 | REALIZABLE in 95 of 200 orders |
| 7.18 | mid(b,c)=a; mid(a,d)=e; mid(b,g)=f; mid(c,d)=h | yes | 288 | 84 | 204 | 0 | 0 | REALIZABLE in 84 of 288 orders |
| 7.19 | mid(a,c)=b; mid(d,e)=a; mid(f,g)=b; mid(d,h)=c | no | 60 | 0 | 40 | 0 | 20 | FORBIDDEN in every order (O/D) -- two edges share a midpoint m: x_p+x_q = 2m = x_r+x_s, a parallelogram |
| 7.20 | mid(a,c)=b; mid(d,e)=a; mid(f,g)=b; mid(c,h)=d | no | 124 | 0 | 82 | 0 | 42 | FORBIDDEN in every order (O/D) -- two edges share a midpoint m: x_p+x_q = 2m = x_r+x_s, a parallelogram |
| 7.21 | mid(a,c)=b; mid(d,e)=a; mid(f,g)=b; mid(c,d)=h | no | 172 | 0 | 136 | 0 | 36 | FORBIDDEN in every order (O/D) -- two edges share a midpoint m: x_p+x_q = 2m = x_r+x_s, a parallelogram |
| 7.22 | mid(a,c)=b; mid(d,e)=a; mid(b,g)=f; mid(d,h)=c | yes | 80 | 55 | 25 | 0 | 0 | REALIZABLE in 55 of 80 orders |
| 7.23 | mid(a,c)=b; mid(d,e)=a; mid(b,g)=f; mid(c,h)=d | yes | 184 | 109 | 75 | 0 | 0 | REALIZABLE in 109 of 184 orders |
| 7.24 | mid(a,c)=b; mid(d,e)=a; mid(b,g)=f; mid(c,d)=h | yes | 248 | 97 | 151 | 0 | 0 | REALIZABLE in 97 of 248 orders |
| 7.25 | mid(a,c)=b; mid(a,e)=d; mid(f,g)=b; mid(c,h)=d | no | 88 | 0 | 72 | 0 | 16 | FORBIDDEN in every order (O/D) -- two edges share a midpoint m: x_p+x_q = 2m = x_r+x_s, a parallelogram |
| 7.26 | mid(a,c)=b; mid(a,e)=d; mid(f,g)=b; mid(c,d)=h | no | 164 | 0 | 128 | 0 | 36 | FORBIDDEN in every order (O/D) -- two edges share a midpoint m: x_p+x_q = 2m = x_r+x_s, a parallelogram |
| 7.27 | mid(a,c)=b; mid(a,e)=d; mid(b,g)=f; mid(c,h)=d | no | 136 | 0 | 94 | 0 | 42 | FORBIDDEN in every order (O/D) -- two edges share a midpoint m: x_p+x_q = 2m = x_r+x_s, a parallelogram |
| 7.28 | mid(a,c)=b; mid(a,e)=d; mid(b,g)=f; mid(c,d)=h | yes | 256 | 97 | 159 | 0 | 0 | REALIZABLE in 97 of 256 orders |
| 7.29 | mid(a,c)=b; mid(a,d)=e; mid(f,g)=b; mid(c,d)=h | no | 64 | 0 | 48 | 0 | 16 | FORBIDDEN in every order (O/D) -- two edges share a midpoint m: x_p+x_q = 2m = x_r+x_s, a parallelogram |
| 7.30 | mid(a,c)=b; mid(a,d)=e; mid(b,g)=f; mid(c,d)=h | yes | 104 | 0 | 63 | 0 | 41 | FORBIDDEN in every order (O/D) -- contains a medial triangle (K31) |

### H8: 4-cycle of edges (no triangle)  (8 vertices, 4 edges)

Edges: {a,b,c}, {a,d,e}, {b,f,g}, {d,f,h}.  Labelings up to Aut(H): 15.

| # | labeling (midpoints) | midpoint-injective | orders | R | O | E | D | verdict |
|---|---|---|---|---|---|---|---|---|
| 8.1 | mid(b,c)=a; mid(d,e)=a; mid(f,g)=b; mid(f,h)=d | no | 140 | 0 | 99 | 0 | 41 | FORBIDDEN in every order (O/D) -- two edges share a midpoint m: x_p+x_q = 2m = x_r+x_s, a parallelogram |
| 8.2 | mid(b,c)=a; mid(d,e)=a; mid(f,g)=b; mid(d,h)=f | no | 256 | 0 | 171 | 0 | 85 | FORBIDDEN in every order (O/D) -- two edges share a midpoint m: x_p+x_q = 2m = x_r+x_s, a parallelogram |
| 8.3 | mid(b,c)=a; mid(d,e)=a; mid(f,g)=b; mid(d,f)=h | no | 296 | 0 | 223 | 0 | 73 | FORBIDDEN in every order (O/D) -- two edges share a midpoint m: x_p+x_q = 2m = x_r+x_s, a parallelogram |
| 8.4 | mid(b,c)=a; mid(d,e)=a; mid(b,g)=f; mid(d,h)=f | no | 102 | 0 | 86 | 0 | 16 | FORBIDDEN in every order (O/D) -- two edges share a midpoint m: x_p+x_q = 2m = x_r+x_s, a parallelogram |
| 8.5 | mid(b,c)=a; mid(d,e)=a; mid(b,g)=f; mid(d,f)=h | no | 288 | 0 | 213 | 0 | 75 | FORBIDDEN in every order (O/D) -- two edges share a midpoint m: x_p+x_q = 2m = x_r+x_s, a parallelogram |
| 8.6 | mid(b,c)=a; mid(d,e)=a; mid(b,f)=g; mid(d,f)=h | no | 172 | 0 | 140 | 0 | 32 | FORBIDDEN in every order (O/D) -- two edges share a midpoint m: x_p+x_q = 2m = x_r+x_s, a parallelogram |
| 8.7 | mid(b,c)=a; mid(a,e)=d; mid(f,g)=b; mid(d,h)=f | yes | 41 | 34 | 7 | 0 | 0 | REALIZABLE in 34 of 41 orders |
| 8.8 | mid(b,c)=a; mid(a,e)=d; mid(f,g)=b; mid(d,f)=h | yes | 188 | 111 | 77 | 0 | 0 | REALIZABLE in 111 of 188 orders |
| 8.9 | mid(b,c)=a; mid(a,e)=d; mid(b,g)=f; mid(d,f)=h | yes | 176 | 110 | 66 | 0 | 0 | REALIZABLE in 110 of 176 orders |
| 8.10 | mid(b,c)=a; mid(a,e)=d; mid(b,f)=g; mid(d,f)=h | yes | 228 | 97 | 131 | 0 | 0 | REALIZABLE in 97 of 228 orders |
| 8.11 | mid(b,c)=a; mid(a,d)=e; mid(b,g)=f; mid(d,f)=h | yes | 124 | 48 | 76 | 0 | 0 | REALIZABLE in 48 of 124 orders |
| 8.12 | mid(b,c)=a; mid(a,d)=e; mid(b,f)=g; mid(f,h)=d | yes | 112 | 46 | 66 | 0 | 0 | REALIZABLE in 46 of 112 orders |
| 8.13 | mid(b,c)=a; mid(a,d)=e; mid(b,f)=g; mid(d,h)=f | yes | 134 | 52 | 82 | 0 | 0 | REALIZABLE in 52 of 134 orders |
| 8.14 | mid(b,c)=a; mid(a,d)=e; mid(b,f)=g; mid(d,f)=h | yes | 244 | 87 | 157 | 0 | 0 | REALIZABLE in 87 of 244 orders |
| 8.15 | mid(a,b)=c; mid(a,d)=e; mid(b,f)=g; mid(d,f)=h | yes | 43 | 0 | 33 | 0 | 10 | FORBIDDEN in every order (O/D) -- medial 4-cycle: Varignon, x_c+x_h = x_e+x_g |

### H9: two triangles sharing two edges  (7 vertices, 4 edges)

Edges: {a,b,c}, {a,d,e}, {b,f,g}, {c,d,f}.  Labelings up to Aut(H): 24.

| # | labeling (midpoints) | midpoint-injective | orders | R | O | E | D | verdict |
|---|---|---|---|---|---|---|---|---|
| 9.1 | mid(b,c)=a; mid(d,e)=a; mid(f,g)=b; mid(d,f)=c | no | 32 | 0 | 24 | 0 | 8 | FORBIDDEN in every order (O/D) -- two edges share a midpoint m: x_p+x_q = 2m = x_r+x_s, a parallelogram |
| 9.2 | mid(b,c)=a; mid(d,e)=a; mid(f,g)=b; mid(c,f)=d | no | 43 | 0 | 35 | 8 | 0 | FORBIDDEN in every order (O/E) -- two edges share a midpoint m: x_p+x_q = 2m = x_r+x_s, a parallelogram |
| 9.3 | mid(b,c)=a; mid(d,e)=a; mid(f,g)=b; mid(c,d)=f | no | 29 | 0 | 19 | 0 | 10 | FORBIDDEN in every order (O/D) -- two edges share a midpoint m: x_p+x_q = 2m = x_r+x_s, a parallelogram |
| 9.4 | mid(b,c)=a; mid(d,e)=a; mid(b,g)=f; mid(d,f)=c | no | 33 | 0 | 24 | 0 | 9 | FORBIDDEN in every order (O/D) -- two edges share a midpoint m: x_p+x_q = 2m = x_r+x_s, a parallelogram |
| 9.5 | mid(b,c)=a; mid(d,e)=a; mid(b,g)=f; mid(c,f)=d | no | 39 | 0 | 31 | 0 | 8 | FORBIDDEN in every order (O/D) -- two edges share a midpoint m: x_p+x_q = 2m = x_r+x_s, a parallelogram |
| 9.6 | mid(b,c)=a; mid(d,e)=a; mid(b,g)=f; mid(c,d)=f | no | 23 | 0 | 19 | 4 | 0 | FORBIDDEN in every order (O/E) -- two edges share a midpoint m: x_p+x_q = 2m = x_r+x_s, a parallelogram |
| 9.7 | mid(b,c)=a; mid(d,e)=a; mid(b,f)=g; mid(d,f)=c | no | 47 | 0 | 40 | 7 | 0 | FORBIDDEN in every order (O/E) -- two edges share a midpoint m: x_p+x_q = 2m = x_r+x_s, a parallelogram |
| 9.8 | mid(b,c)=a; mid(d,e)=a; mid(b,f)=g; mid(c,f)=d | no | 30 | 0 | 23 | 0 | 7 | FORBIDDEN in every order (O/D) -- two edges share a midpoint m: x_p+x_q = 2m = x_r+x_s, a parallelogram |
| 9.9 | mid(b,c)=a; mid(d,e)=a; mid(b,f)=g; mid(c,d)=f | no | 39 | 0 | 31 | 0 | 8 | FORBIDDEN in every order (O/D) -- two edges share a midpoint m: x_p+x_q = 2m = x_r+x_s, a parallelogram |
| 9.10 | mid(b,c)=a; mid(a,e)=d; mid(f,g)=b; mid(d,f)=c | yes | 16 | 12 | 4 | 0 | 0 | REALIZABLE in 12 of 16 orders |
| 9.11 | mid(b,c)=a; mid(a,e)=d; mid(f,g)=b; mid(c,d)=f | yes | 10 | 6 | 4 | 0 | 0 | REALIZABLE in 6 of 10 orders |
| 9.12 | mid(b,c)=a; mid(a,e)=d; mid(b,g)=f; mid(d,f)=c | yes | 17 | 12 | 5 | 0 | 0 | REALIZABLE in 12 of 17 orders |
| 9.13 | mid(b,c)=a; mid(a,e)=d; mid(b,f)=g; mid(d,f)=c | yes | 30 | 11 | 19 | 0 | 0 | REALIZABLE in 11 of 30 orders |
| 9.14 | mid(b,c)=a; mid(a,e)=d; mid(b,f)=g; mid(c,d)=f | yes | 29 | 11 | 18 | 0 | 0 | REALIZABLE in 11 of 29 orders |
| 9.15 | mid(b,c)=a; mid(a,d)=e; mid(f,g)=b; mid(d,f)=c | yes | 22 | 11 | 11 | 0 | 0 | REALIZABLE in 11 of 22 orders |
| 9.16 | mid(b,c)=a; mid(a,d)=e; mid(f,g)=b; mid(c,f)=d | yes | 23 | 11 | 12 | 0 | 0 | REALIZABLE in 11 of 23 orders |
| 9.17 | mid(b,c)=a; mid(a,d)=e; mid(b,g)=f; mid(d,f)=c | yes | 27 | 10 | 17 | 0 | 0 | REALIZABLE in 10 of 27 orders |
| 9.18 | mid(b,c)=a; mid(a,d)=e; mid(b,f)=g; mid(d,f)=c | yes | 28 | 10 | 18 | 0 | 0 | REALIZABLE in 10 of 28 orders |
| 9.19 | mid(b,c)=a; mid(a,d)=e; mid(b,f)=g; mid(c,f)=d | yes | 12 | 0 | 8 | 4 | 0 | FORBIDDEN in every order (O/E) -- contains a medial triangle (K31) |
| 9.20 | mid(b,c)=a; mid(a,d)=e; mid(b,f)=g; mid(c,d)=f | yes | 20 | 5 | 15 | 0 | 0 | REALIZABLE in 5 of 20 orders |
| 9.21 | mid(a,b)=c; mid(d,e)=a; mid(f,g)=b; mid(d,f)=c | no | 23 | 0 | 17 | 6 | 0 | FORBIDDEN in every order (O/E) -- two edges share a midpoint m: x_p+x_q = 2m = x_r+x_s, a parallelogram |
| 9.22 | mid(a,b)=c; mid(d,e)=a; mid(b,g)=f; mid(d,f)=c | no | 23 | 0 | 19 | 0 | 4 | FORBIDDEN in every order (O/D) -- two edges share a midpoint m: x_p+x_q = 2m = x_r+x_s, a parallelogram |
| 9.23 | mid(a,b)=c; mid(d,e)=a; mid(b,f)=g; mid(d,f)=c | no | 33 | 0 | 24 | 0 | 9 | FORBIDDEN in every order (O/D) -- two edges share a midpoint m: x_p+x_q = 2m = x_r+x_s, a parallelogram |
| 9.24 | mid(a,b)=c; mid(a,d)=e; mid(b,f)=g; mid(d,f)=c | no | 14 | 0 | 11 | 3 | 0 | FORBIDDEN in every order (O/E) -- two edges share a midpoint m: x_p+x_q = 2m = x_r+x_s, a parallelogram |

### H10: PASCH (four edges on six vertices)  (6 vertices, 4 edges)

Edges: {a,b,c}, {a,d,e}, {b,d,f}, {c,e,f}.  Labelings up to Aut(H): 6.

| # | labeling (midpoints) | midpoint-injective | orders | R | O | E | D | verdict |
|---|---|---|---|---|---|---|---|---|
| 10.1 | mid(b,c)=a; mid(d,e)=a; mid(d,f)=b; mid(e,f)=c | no | 2 | 0 | 2 | 0 | 0 | FORBIDDEN in every order (O) -- two edges share a midpoint m: x_p+x_q = 2m = x_r+x_s, a parallelogram |
| 10.2 | mid(b,c)=a; mid(d,e)=a; mid(d,f)=b; mid(c,f)=e | no | 4 | 0 | 4 | 0 | 0 | FORBIDDEN in every order (O) -- two edges share a midpoint m: x_p+x_q = 2m = x_r+x_s, a parallelogram |
| 10.3 | mid(b,c)=a; mid(d,e)=a; mid(d,f)=b; mid(c,e)=f | no | 4 | 0 | 3 | 1 | 0 | FORBIDDEN in every order (O/E) -- two edges share a midpoint m: x_p+x_q = 2m = x_r+x_s, a parallelogram |
| 10.4 | mid(b,c)=a; mid(d,e)=a; mid(b,d)=f; mid(c,e)=f | no | 1 | 0 | 1 | 0 | 0 | FORBIDDEN in every order (O) -- two edges share a midpoint m: x_p+x_q = 2m = x_r+x_s, a parallelogram |
| 10.5 | mid(b,c)=a; mid(a,e)=d; mid(d,f)=b; mid(e,f)=c | yes | 3 | 1 | 2 | 0 | 0 | REALIZABLE in 1 of 3 orders |
| 10.6 | mid(b,c)=a; mid(a,e)=d; mid(b,d)=f; mid(e,f)=c | yes | 1 | 0 | 1 | 0 | 0 | FORBIDDEN in every order (O) -- every order violates monotone midpoints (K30) |

**10.1** `mid(b,c)=a; mid(d,e)=a; mid(d,f)=b; mid(e,f)=c`
- order `d b f a c e` : O: no increasing point; minimal order-infeasible sub-pattern (d,b,f), (d,a,e), (b,a,c), (f,c,e)
- order `f b d a c e` : O: no increasing point; minimal order-infeasible sub-pattern (b,a,c), (d,a,e)

**10.2** `mid(b,c)=a; mid(d,e)=a; mid(d,f)=b; mid(c,f)=e`
- order `c e f a b d` : O: no increasing point; minimal order-infeasible sub-pattern (c,a,b), (e,a,d)
- order `f b d a e c` : O: no increasing point; minimal order-infeasible sub-pattern (f,e,c), (b,a,c)
- order `f b e a d c` : O: no increasing point; minimal order-infeasible sub-pattern (f,b,d), (f,e,c), (b,a,c), (e,a,d)
- order `f b e a c d` : O: no increasing point; minimal order-infeasible sub-pattern (b,a,c), (e,a,d)

**10.3** `mid(b,c)=a; mid(d,e)=a; mid(d,f)=b; mid(c,e)=f`
- order `c f e a b d` : O: no increasing point; minimal order-infeasible sub-pattern (f,b,d), (e,a,d)
- order `e f c a b d` : E: forces unlisted AP (f,c,b)
- order `e f b a c d` : O: no increasing point; minimal order-infeasible sub-pattern (e,a,d), (f,b,d)
- order `e f b a d c` : O: no increasing point; minimal order-infeasible sub-pattern (e,a,d), (b,a,c)

**10.4** `mid(b,c)=a; mid(d,e)=a; mid(b,d)=f; mid(c,e)=f`
- order `b e a f c d` : O: no increasing point; minimal order-infeasible sub-pattern (e,a,d), (e,f,c)

**10.5** `mid(b,c)=a; mid(a,e)=d; mid(d,f)=b; mid(e,f)=c`
- order `e d c a b f` : R  realization e=0, d=4, c=7, a=8, b=9, f=14
- order `f b a d c e` : O: no increasing point; minimal order-infeasible sub-pattern (f,c,e), (a,d,e)
- order `e d b a c f` : O: no increasing point; minimal order-infeasible sub-pattern (e,c,f), (d,b,f)

**10.6** `mid(b,c)=a; mid(a,e)=d; mid(b,d)=f; mid(e,f)=c`
- order `b a f c d e` : O: no increasing point; minimal order-infeasible sub-pattern (a,d,e), (f,c,e)


## Reproduction (exact commands)

```
cd /home/user/Erdos-757/experiments/20261014-0005-forbidden-n8
export PYTHONPATH=/home/user/Erdos-757
# Part 1: n = 8 library (10 min, run as a job):
bash ../../scripts/start_job.sh experiments/20261014-0005-forbidden-n8 1 \
     python3 experiments/20261014-0005-forbidden-n8/enumerate.py 8 /home/user/Erdos-757/data/forbidden_ordered_n8.json 8
# Part 3..7 (2 min):
python3 catalogue.py catalogue.json
python3 gen_readme.py catalogue.json catalogue_tables.md        # also writes catalogue_tables_orders_7_8_vertices.md and *.stats.json
python3 crosscheck_catalogue.py catalogue.json | tee crosscheck_catalogue.out
python3 failure_modes.py catalogue.json | tee failure_modes.out
python3 tally_cores.py | tee tally_cores.out
python3 build_readme.py                                         # assembles this README from README_template.md
cd ../.. && python3 -m pytest -q tests/test_forbidden_catalogue.py tests/test_realizability.py
```

`enumerate.py` is `experiments/20261013-2257-forbidden-library/enumerate.py` with one extra optional argument
`NMIN` (first n to enumerate). `catalogue.json` is stored gzipped (`gunzip -k catalogue.json.gz` before
rerunning the downstream scripts). No randomness except fixed seeds (`realize_exact` seed 0, `small_real`
seed 1).

## Conclusions

- The n = 8 library is complete: 243 new minimal cores, patterns 46281 = 16568 R + 28697 O + 498 E + 518 D.
- A three-edge triangle labeling is realizable iff its midpoints are distinct and not all edge-private; the
  only forbidden injective triangle labeling is the medial triangle (K31).
- Pasch (4 edges, 6 vertices) is realizable in exactly one labeling and one order, giving the saturated
  6-point (4,5)-set {0,4,7,8,9,14} with h = 4.
- Beyond shared midpoints, K31 and K30, the only new forbidden-in-every-order labeling with <= 4 edges is the
  medial 4-cycle (Varignon parallelogram, row 8.15), which contains no triangle.
- Among all 3870 failing orders of midpoint-injective labelings: 3688 are K30 violations (2-edge order cores),
  63 are order-infeasible only through a 4-edge core, 111 are forced repeated differences and 8 forced
  extra APs.
