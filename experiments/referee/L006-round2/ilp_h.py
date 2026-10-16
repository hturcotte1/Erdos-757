"""Referee round 2: h(B) by an ILP on the Sidon definition (OR-tools CP-SAT, 1 worker), for a random sample of the
(4,5) points found by Route V (vertex types) plus constructed T1a-type and T2-type generic points and the control A_base.
Also writes judge sample files to jsamples/.  Own code (no e757, no authors' code)."""
import gzip, json, random, os, sys
from fractions import Fraction as F
from itertools import combinations
from math import lcm
from ortools.sat.python import cp_model
ROOT = '/home/user/Erdos-757'; HERE = ROOT + '/experiments/referee/L006-round2'

def ints(A, x, y):
    D = lcm(*(F(v).denominator for v in list(A) + [x, y]))
    return sorted(int(F(v) * D) for v in list(A) + [x, y])

def is45(B):
    for q in combinations(B, 4):
        d = [abs(u - v) for u, v in combinations(q, 2)]
        if len(set(d)) < 5: return False
    return True

def h_ilp(B):
    n = len(B); m = cp_model.CpModel(); z = [m.NewBoolVar('z%d' % i) for i in range(n)]
    sums = {}
    for i in range(n):
        for j in range(i, n): sums.setdefault(B[i] + B[j], []).append((i, j))
    ncons = 0
    for s, lst in sums.items():
        for (i, j), (k, l) in combinations(lst, 2):
            S = {i, j, k, l}
            m.Add(sum(z[t] for t in S) <= len(S) - 1); ncons += 1
    m.Maximize(sum(z))
    sol = cp_model.CpSolver(); sol.parameters.num_workers = 1; sol.parameters.max_time_in_seconds = 60
    st = sol.Solve(m)
    assert st == cp_model.OPTIMAL, st
    S = [B[i] for i in range(n) if sol.Value(z[i])]
    diffs = [b - a for a, b in combinations(sorted(S), 2)]
    assert len(diffs) == len(set(diffs))   # witness really Sidon
    return int(sol.ObjectiveValue())

if __name__ == '__main__':
    os.nice(5)
    cen = json.load(gzip.open(ROOT + '/experiments/20261014-1005-census-dfs/results/realized_n12.json.gz', 'rt'))
    V = [json.loads(l) for l in open(HERE + '/routeV_main.jsonl')]
    rng = random.Random(97531)
    samples = []
    for r in V:
        A = cen[r['class']]['set']
        for p in rng.sample(r['pairs45'], 2): samples.append((r['class'], 'vertex', A, F(p[0]), F(p[1])))
        # T1a-type: admissible vertical line, generic y
        x0 = F(rng.choice(r['genV45'])); samples.append((r['class'], 'T1a-generic', A, x0, F(10 ** 7) + F(1, 7)))
        # T2-type generic points (x midpoint of a and y; y midpoint of a and x; a = min A, midpoint of x and y)
        a = rng.choice(A); t = F(10 ** 7) + F(3, 11)
        samples.append((r['class'], 'T2-xmid-generic', A, t, 2 * t - a))
        samples.append((r['class'], 'T2-amin-generic', A, t, 2 * min(A) - t))
    Ab = [0, 136, 200, 243, 246, 249, 272, 286, 298, 323, 400, 528, 596, 1056]
    res = {}; bad = []
    for c, typ, A, x, y in samples:
        B = ints(A, x, y)
        if not is45(B): res.setdefault(typ, {}).setdefault('not45', 0); res[typ]['not45'] += 1; continue
        h = h_ilp(B); res.setdefault(typ, {}).setdefault(h, 0); res[typ][h] += 1
        if h != 9: bad.append((c, typ, str(x), str(y), h))
    hc = h_ilp(Ab)
    print('ILP h on', len(samples), 'sample extensions from', len(V), 'classes:', {k: {str(a): b for a, b in v.items()} for k, v in res.items()})
    print('non-9 values:', bad[:10])
    print('control A_base (14 points): ILP h =', hc, '(published value 8)')
    # judge samples
    os.makedirs(HERE + '/jsamples', exist_ok=True)
    picks = [s for s in samples if s[1] == 'vertex'][:4] + [s for s in samples if s[1] == 'T1a-generic'][:2] + [s for s in samples if s[1].startswith('T2')][:2]
    for k, (c, typ, A, x, y) in enumerate(picks):
        B = sorted([F(v) for v in A] + [x, y])
        cid = 'R2-L006-c%d-%s-%d' % (c, typ, k)
        json.dump({'id': cid, 'type': 'construction', 'set': [str(v) for v in B], 'claimed_h': 9,
                   'notes': 'referee L006 round 2 sample: class %d, %s, x=%s, y=%s' % (c, typ, x, y)}, open(HERE + '/jsamples/%s.json' % cid, 'w'))
    json.dump({'id': 'R2-L006-control-Abase', 'type': 'construction', 'set': Ab, 'claimed_h': 8, 'notes': 'control'}, open(HERE + '/jsamples/R2-L006-control-Abase.json', 'w'))
