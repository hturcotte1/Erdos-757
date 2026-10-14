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
| 8 | @@N8_total@@ | @@N8_realizable@@ | @@N8_order-infeasible@@ | @@N8_forced_extra_AP@@ | @@N8_forced_repeated_difference@@ |

(For n = 3..7 see `experiments/20261013-2257-forbidden-library/README.md`; its table has n = 7: 2364 / 1312 / 1006 / 22 / 24.)

Minimal cores at n = 8: @@N8_CORES@@ pairs (S, relation) up to reflection, by kind `@@N8_KINDS@@`;
by edge count: 4 edges: 69, 5 edges: 83, 6 edges: 91 (none with fewer than 4 edges; the largest has 6
edges). Together with the 44 cores of n <= 7 the library now holds 287 cores.

Cores with <= 4 edges (n = 7 and n = 8 files), by the underlying configuration (`tally_cores.py`):

```
@@TALLY@@
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

  Totals: `@@FM@@`

## Part 3. Summary by configuration

Counts of labelings and ordered patterns. R/O/E/D count ordered patterns (rank-forms up to reflection).
Non-injective labelings (two edges with the same midpoint) are included; they are never realizable.

@@SUMMARY@@

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

@@TABLES@@

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
