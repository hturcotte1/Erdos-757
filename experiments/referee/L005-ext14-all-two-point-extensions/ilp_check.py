"""Third method for h: CP-SAT on the Sidon definition (no 3-AP reduction, no weak-Sidon lemma).
For a set B, every coincidence v-u = z-w of positive differences between two distinct pairs (u<v), (w<z) (the pairs may share
one point) forbids choosing all points of {u,v,w,z}; maximise the number of chosen points.
Run on random (4,5) T1b extensions B = A u {x,y} (y forms a 3-AP with two points of A u {x}) of random classes, and on h(A).
usage: python3 ilp_check.py NCLASSES PAIRS_PER_CLASS SEED"""
import sys, json, gzip, random, itertools, os
from ortools.sat.python import cp_model
import cases, locus

os.nice(15)


def h_cpsat(B):
    B = sorted(B)
    n = len(B)
    by = {}
    for i, j in itertools.combinations(range(n), 2):
        by.setdefault(B[j] - B[i], []).append((i, j))
    m = cp_model.CpModel()
    z = [m.NewBoolVar('z%d' % i) for i in range(n)]
    ncons = 0
    for d, prs in by.items():
        for p, q in itertools.combinations(prs, 2):
            S = sorted(set(p) | set(q))
            m.AddBoolOr([z[i].Not() for i in S])
            ncons += 1
    m.Maximize(sum(z))
    s = cp_model.CpSolver()
    s.parameters.num_workers = 1
    s.parameters.max_time_in_seconds = 60
    st = s.Solve(m)
    assert st == cp_model.OPTIMAL
    val = int(round(s.ObjectiveValue()))
    T = [B[i] for i in range(n) if s.Value(z[i])]
    assert locus.is_sidon_sums(T) and len(T) == val
    return val


ncl, per, seed = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
sets = [json.loads(l)['set'] for l in gzip.open('/home/user/Erdos-757/data/census_n14_m12_classes.jsonl.gz', 'rt') if l.strip()]
rng = random.Random(seed)
cls = sorted(set(rng.sample(range(len(sets)), ncl)) | {2440})
tot = 0
hist = {}
hA_ok = True
for c in cls:
    A = sorted(12 * v for v in sets[c])
    if h_cpsat(A) != 8:
        hA_ok = False
    Px = sorted(cases.ap_partners(A))
    ok1 = [x for x in Px if all(locus.ndist((x,) + q) >= 5 for q in itertools.combinations(A, 3))]
    got = 0
    tries = 0
    while got < per and tries < 20000:
        tries += 1
        x = rng.choice(ok1)
        y = rng.choice(sorted(cases.ap_partners(A + [x])))
        if not locus.b_is45(A, x, y):
            continue
        h = h_cpsat(A + [x, y])
        hist[h] = hist.get(h, 0) + 1
        got += 1
        tot += 1
print(json.dumps({'classes': len(cls), 'pairs': tot, 'h_hist': hist, 'hA_all_8_by_cpsat': hA_ok}))
