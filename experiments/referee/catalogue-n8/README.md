# Referee recomputation: n=8 forbidden-core library and small-configuration catalogue

Reviewed deliverable: `experiments/20261014-0005-forbidden-n8/` (README, `catalogue.json.gz`),
`data/forbidden_ordered_n8.json`, `tests/test_forbidden_catalogue.py`, KB row K33.

**Question.** Do the verdicts (R / O / E / D), the per-labeling order counts, the n=8 census and the
minimal-core library hold when recomputed without the `e757` package?

**Method.** Independent exact oracle (`recompute.py`, Fractions + sympy, no `e757` import):
nullspace of the AP equations over Q; strict order feasibility by exact Fourier-Motzkin on the solution
space (an integer Farkas certificate `sum y_e eq_e = sum w_r g_r`, `w >= 0`, is printed for every O);
forced extra AP / forced parallelogram by vanishing on the nullspace (the linear combination of the
AP equations giving the relation is printed, via sympy); R verdicts come with an explicit integer point
re-checked exactly (AP set equal to the pattern, every 4-subset with >= 5 distinct differences).
Precedence O > E > D as in the deliverable.

**Exact commands** (run from this directory, `python3 -I` so nothing outside it is imported):
```
python3 -I recompute.py        # 6 entries, whole censuses, Pasch point, catalogue comparison, 40 sampled cores
python3 -I census8_raw.py 7; python3 -I census8_raw.py 8    # full n=7 and n=8 census recount
python3 -I cores8.py 7; python3 -I cores8.py 8               # full minimal-core recount vs the library files
python3 -I k30_check.py        # the 12 failing orders of triangle labelings 4.3-4.6 are 2-edge (K30) cores
cd ../../.. && python3 -m pytest -q tests/test_forbidden_catalogue.py
```
Outputs: `recompute.out`, `census8.out`, `census8_raw.out`, `cores8.out`, `k30_check.out`.

**Result** [verified-here].
- Six catalogue entries, every consistent vertex order (patterns up to reflection):
  4.7 medial triangle 2 orders (1 D, 1 O), forced `x_a+x_f = x_c+x_e` = ½[a+b−2c]+½[a+d−2e]−½[b+d−2f];
  8.15 medial 4-cycle 43 orders (33 O, 10 D), forced `x_c+x_h = x_e+x_g` (Varignon);
  10.6 Pasch 1 order (O), Farkas `−[a+e−2d]+[f+e−2c] = (f−a)+2(d−c)` (K30);
  4.3: 3 orders all R; 4.6: 15 orders (7 R, 8 O); 10.5 Pasch: 3 orders (1 R, 2 O), the R order realized by
  f=0,b=4,a=7,c=8,d=9,e=14. All match the README; all 67 patterns agree order by order with
  `catalogue.json.gz`.
- Whole censuses: triangle 60 = 22 R + 28 O + 10 D; Pasch 15 = 1 R + 13 O + 1 E; two edges sharing a
  vertex 9 = 6 R + 2 O + 1 D; two disjoint edges 7 = 6 R + 1 O. {0,4,7,8,9,14}: exactly the four Pasch
  APs, (4,5)-set, h = 4.
- n=8 census, raw ordered patterns (the deliverable's convention, including the empty pattern, not
  deduplicated under reflection): 46281 = 16568 R + 28697 O + 498 E + 518 D (match); n=7:
  2364 = 1312 + 1006 + 22 + 24 (matches K32). Up to reflection the n=8 classes number 39208.
- Minimal cores: n=8 set of 243 cores (134 order / 87 diff / 22 extra_ap; 69/83/91 with 4/5/6 edges)
  recomputed and found EQUAL as a set to `data/forbidden_ordered_n8.json`; the 39 n=7 cores of
  `data/forbidden_ordered_n7.json` likewise.
- The 9 injective labelings that the catalogue marks forbidden in every order are exactly: 7 containing a
  medial triangle (structural check), the medial 4-cycle 8.15, and Pasch 10.6.
- `pytest -q tests/test_forbidden_catalogue.py`: 3 passed.

**Conclusion.** Every recomputed verdict matches. Nits (wording only): K33's "No unlabeled configuration
with <=4 edges is forbidden outright" is supported by the data only for the 11 connected configurations
on <= 8 vertices; the census totals are raw ordered patterns, not reflection classes. Process: commit
26a21d7 also carries a change to `e757/cpsat_model.py` (another agent's file, swept in by `git add -A`).

Tags: [verified-here] for every numbered statement above.
