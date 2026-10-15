"""Referee L004: independent CNF model + CDCL enumeration of saturated ordered midpoint patterns (own code).
Imports nothing from e757/, judge/ or earlier referee directories.

Vertices 0..n-1 in rank order. One Boolean per triple (i,j,k), i<j<k: "x_j is the midpoint of x_i, x_k".
Constraints (all necessary for the rank-ordered 3-AP hypergraph of a saturated n-point (4,5)-set with h <= T):
  (sat)  every interior vertex j (1..n-2) is the middle of EXACTLY one triple   [m = n-2; injective midpoints]
  (lin)  no two triples share two vertices                                     [linearity of the AP hypergraph]
  (k30)  no triples (i,j,k),(a,b,c) with j<b, i>=a, k>=c                        [x_j=(x_i+x_k)/2 >= (x_a+x_c)/2=x_b]
  (alp)  every (T+1)-subset of vertices contains a triple                      [alpha <= T]
F7 is NOT encoded (models containing F7 are kept and realized separately).

Cubes: the triples at midpoints 1, 2, 3 (all combinations of triples with those middles, not only census prefixes).
Every model has exactly n-2 true triple variables, so blocking the true literals is exact.

Option LAZYF7=1 (env): a model containing a copy of F7 is not output; instead one 5-literal clause per F7 copy in it
("not all five of these triples") is added. Sound for the F7-free class (K7, Gyarfas-Lehel): it removes exactly
patterns containing that F7 copy. Without it, F7 models are output like all others.

usage: python3 sat14.py N T OUTFILE.gz CUBESPEC [solver]
   CUBESPEC: 'all' | 'census:<prefixes.txt>:<idx list a,b,c or a-b>' | 'list:<file of cubes i-k,i-k,i-k>'
Output lines: "<cube> <i,j,k> ... " for each model; final stats on stderr and as '# ' lines.
"""
import sys, gzip, time, itertools
from pysat.solvers import Solver

n, T = int(sys.argv[1]), int(sys.argv[2])
OUT, SPEC = sys.argv[3], sys.argv[4]
SNAME = sys.argv[5] if len(sys.argv) > 5 else "cd15"

tri = list(itertools.combinations(range(n), 3))
var = {t: q + 1 for q, t in enumerate(tri)}
cls = []
bymid = {j: [t for t in tri if t[1] == j] for j in range(1, n - 1)}
for j, ts in bymid.items():
    cls.append([var[t] for t in ts])
    for a, b in itertools.combinations(ts, 2):
        cls.append([-var[a], -var[b]])
for a, b in itertools.combinations(range(n), 2):
    ts = [t for t in tri if a in t and b in t]
    for s, u in itertools.combinations(ts, 2):
        if s[1] != u[1]:
            cls.append([-var[s], -var[u]])
for s in tri:
    for u in tri:
        if s[1] < u[1] and s[0] >= u[0] and s[2] >= u[2]:
            cls.append([-var[s], -var[u]])
for S in itertools.combinations(range(n), T + 1):
    cls.append([var[t] for t in itertools.combinations(S, 3)])
# any triple whose middle is an extreme vertex cannot exist (middle is 1..n-2 automatically since i<j<k)


def cubes_all():
    for t1 in bymid[1]:
        for t2 in bymid[2]:
            for t3 in bymid[3]:
                yield (t1, t2, t3)


def parse_cube(s):
    out = []
    for lvl, tok in enumerate(s.split(","), start=1):
        a, b = tok.split("-"); out.append((int(a), lvl, int(b)))
    return tuple(out)


if SPEC == "all":
    cubes = list(cubes_all())
elif SPEC.startswith("census:"):
    _, pf, sel = SPEC.split(":")
    pl = open(pf).read().split()
    idxs = []
    for part in sel.split(","):
        if "-" in part:
            a, b = part.split("-"); idxs += list(range(int(a), int(b) + 1))
        else:
            idxs.append(int(part))
    cubes = [parse_cube(pl[q]) for q in idxs]
elif SPEC.startswith("list:"):
    cubes = [parse_cube(x) for x in open(SPEC[5:]).read().split()]
else:
    raise SystemExit("bad spec")

import os
LAZY = os.environ.get("LAZYF7", "0") == "1"


def f7_copies(es):
    """all F7 copies in a linear triple system es (list of sorted triples): centre c, three triples through c,
    two vertex-disjoint triples avoiding c, each meeting every arm in exactly one vertex."""
    out = set()
    verts = set(v for e in es for v in e)
    for c in verts:
        thr = [e for e in es if c in e]
        if len(thr) < 3: continue
        for a, b, d in itertools.combinations(thr, 3):
            arms = [set(e) - {c} for e in (a, b, d)]
            if len(arms[0] | arms[1] | arms[2]) != 6: continue
            U = arms[0] | arms[1] | arms[2]
            tv = [e for e in es if c not in e and set(e) <= U and all(len(set(e) & A) == 1 for A in arms)]
            for x, y in itertools.combinations(tv, 2):
                if not (set(x) & set(y)):
                    out.add(tuple(sorted((a, b, d, x, y))))
    return out


t0 = time.time()
nf7cl = 0
tot_models = 0; ncubes = 0; nsat_cubes = 0
with gzip.open(OUT, "wt") as g:
    s = Solver(name=SNAME, bootstrap_with=cls)
    for cube in cubes:
        ncubes += 1
        tc = time.time()
        assum = [var[t] for t in cube]
        cnt = 0
        while s.solve(assumptions=assum):
            mdl = s.get_model()
            truev = [l for l in mdl if 0 < l <= len(tri)]
            es = sorted(tri[l - 1] for l in truev)
            assert len(es) == n - 2, es
            if LAZY:
                cp = f7_copies(es)
                if cp:
                    for C in cp:
                        s.add_clause([-var[t] for t in C]); nf7cl += 1
                    continue
            g.write("%s %s\n" % (",".join("%d-%d" % (t[0], t[2]) for t in cube), " ".join("%d,%d,%d" % e for e in es)))
            s.add_clause([-l for l in truev])
            cnt += 1
        tot_models += cnt
        if cnt: nsat_cubes += 1
        g.write("# cube %s models %d time %.2f\n" % (",".join("%d-%d" % (t[0], t[2]) for t in cube), cnt, time.time() - tc))
    s.delete()
msg = "DONE cubes=%d sat_cubes=%d models=%d f7clauses=%d lazy=%d time=%.1f" % (ncubes, nsat_cubes, tot_models, nf7cl, LAZY, time.time() - t0)
print(msg, file=sys.stderr)
with gzip.open(OUT, "at") as g:
    g.write("# " + msg + "\n")
