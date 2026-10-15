"""Referee L004: random-model containment test across ALL prefixes (own code; same CNF as sat14.py).
Repeatedly: pick a uniformly random census prefix (cube at midpoints 1..3), random preferred phases, and with prob. 1/2
one extra random assumption (a random triple at a random midpoint 4..12, binary-consistent with the cube); solve under a
conflict budget; F7 models are handled lazily (5-literal clause per F7 copy, then re-solve). Every F7-free model found is
written out. Afterwards (separately) every model's reflection-orbit key must be in the census key set, and every
realizable model must be one of the census realizable classes.
usage: python3 sample14.py OUT.gz SECONDS SEED"""
import sys, gzip, time, itertools, random, os
from pysat.solvers import Solver

OUT, SECS, SEED = sys.argv[1], float(sys.argv[2]), int(sys.argv[3])
n, T = 14, 8
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "cnf14_body.txt")).read())  # tri, var, cls, bymid
PREF = '/home/user/Erdos-757/experiments/20261014-1005-census-dfs/n14/results/n14_m12_prefixes.txt'
pl = open(PREF).read().split()


def parse_cube(s):
    return [(int(a), lvl, int(b)) for lvl, tok in enumerate(s.split(","), start=1) for a, b in [tok.split("-")]]


def compat(ts):
    for s, u in itertools.combinations(ts, 2):
        if len(set(s) & set(u)) >= 2: return False
        for a, b in ((s, u), (u, s)):
            if a[1] < b[1] and a[0] >= b[0] and a[2] >= b[2]: return False
    return True


def f7_copies(es):
    out = set()
    verts = set(v for e in es for v in e)
    for c in verts:
        thr = [e for e in es if c in e]
        if len(thr) < 3: continue
        for a, b, d in itertools.combinations(thr, 3):
            arms = [set(e) - {c} for e in (a, b, d)]
            U = arms[0] | arms[1] | arms[2]
            if len(U) != 6: continue
            tv = [e for e in es if c not in e and set(e) <= U and all(len(set(e) & A) == 1 for A in arms)]
            for x, y in itertools.combinations(tv, 2):
                if not (set(x) & set(y)):
                    out.add(tuple(sorted((a, b, d, x, y))))
    return out


rng = random.Random(SEED)
s = Solver(name="cd15", bootstrap_with=cls)
t0 = time.time(); got = 0; tries = 0; unk = 0; unsat = 0; f7cl = 0
with gzip.open(OUT, "wt") as g:
    while time.time() - t0 < SECS:
        tries += 1
        cube = parse_cube(rng.choice(pl))
        assum = [var[t] for t in cube]
        if rng.random() < 0.5:
            r = rng.randint(4, n - 2)
            cand = [t for t in bymid[r] if compat(cube + [t])]
            if cand:
                assum.append(var[rng.choice(cand)])
        s.set_phases([v if rng.random() < 0.5 else -v for v in range(1, len(tri) + 1)])
        while True:
            s.conf_budget(20000)
            res = s.solve_limited(assumptions=assum)
            if res is None: unk += 1; break
            if res is False: unsat += 1; break
            mdl = s.get_model()
            es = sorted(tri[l - 1] for l in mdl if 0 < l <= len(tri))
            cp = f7_copies(es)
            if cp:
                for C in cp:
                    s.add_clause([-var[t] for t in C]); f7cl += 1
                continue
            g.write(" ".join("%d,%d,%d" % e for e in es) + "\n"); got += 1
            break
msg = "DONE tries=%d models=%d unsat=%d unknown=%d f7clauses=%d time=%.0f" % (tries, got, unsat, unk, f7cl, time.time() - t0)
print(msg)
