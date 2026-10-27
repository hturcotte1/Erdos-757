"""Referee round 2, L017: independent recomputation of C5 (the roles of Theorem 4(iv)) and C2 (Lemma U'' and the pair lemma) on the
stored lists.  Every transversal number is computed by an ILP (scipy/HiGHS); co-transversality by Fact 0.4 (tau(F-X) = tau(F)-|X|);
nothing is imported from experiments/prover/L017.  Usage: python3 roles.py full|v2 cellfile ..."""
import sys, re, itertools, time
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds
def read(path):
    return [[tuple(map(int, t.split(','))) for t in re.findall(r'\((\d+,\d+,\d+)\)', l)] for l in open(path) if l.startswith('FOUND:')]
def tau(n, edges, removed=()):
    rem = set(removed); es = [e for e in edges if not (set(e) & rem)]
    if not es: return 0
    keep = [v for v in range(n) if v not in rem]; idx = {v: i for i, v in enumerate(keep)}
    A = np.zeros((len(es), len(keep)))
    for i, e in enumerate(es):
        for v in e: A[i, idx[v]] = 1
    res = milp(c=np.ones(len(keep)), constraints=LinearConstraint(A, lb=np.ones(len(es))), integrality=np.ones(len(keep)), bounds=Bounds(0, 1))
    assert res.success; return int(round(res.fun))
def analyse(n, edges, full_pairs):
    m = len(edges); t = tau(n, edges); s = 3*n + 2*m - 11*t
    assert all(len(set(a) & set(b)) <= 1 for a, b in itertools.combinations(edges, 2))
    deg = [0]*n
    for e in edges:
        for v in e: deg[v] += 1
    inedge = set(tuple(sorted(p)) for e in edges for p in itertools.combinations(e, 2))
    u_fail = [v for v in range(n) if deg[v] >= 1 and s < 3 + 2*deg[v] and tau(n, edges, (v,)) != t - 1]
    V2 = [v for v in range(n) if deg[v] <= 2]
    pairs = list(itertools.combinations(range(n), 2)) if full_pairs else list(itertools.combinations(V2, 2))
    anti = set(); pl_fail = []
    for x, y in pairs:
        if tau(n, edges, (x, y)) != t - 2:
            anti.add((x, y))
            if 2*(deg[x] + deg[y] - (1 if (x, y) in inedge else 0)) > s + 5: pl_fail.append((x, y))
    A = lambda x, y: (min(x, y), max(x, y)) in anti
    antiV2 = [(x, y) for (x, y) in anti if deg[x] <= 2 and deg[y] <= 2]
    rb = sum(1 for x, y, z in itertools.combinations(V2, 3) if A(x, y) and A(x, z) and A(y, z))
    P = [(a, b) for a, b in itertools.combinations(V2, 2) if (a, b) not in inedge]
    rc = sum(1 for p, q in itertools.combinations(P, 2) if not set(p) & set(q) and all(A(x, y) for x in p for y in q))
    re_ = sum(1 for (a, b) in P for e in V2 if e not in (a, b) and A(a, e) and A(b, e))
    rf1 = sum(1 for (a, b) in P for c, e in itertools.combinations([x for x in V2 if x not in (a, b)], 2) if all(A(x, y) for x in (a, b) for y in (c, e)))
    types = sorted((deg[x], deg[y], int((x, y) in inedge)) for x, y in antiV2)
    return dict(n=n, m=m, tau=t, s=s, u_fail=u_fail, pl_fail=pl_fail, anti_types=types, n_anti_all=len(anti), role_b=rb, role_c=rc, role_e=re_, role_f1=rf1, role_f2=len(antiV2))
if __name__ == '__main__':
    full = sys.argv[1] == 'full'
    for path in sys.argv[2:]:
        gs = read(path); n = int(path.split('cell_')[1].split('_')[0]); t0 = time.time()
        summ = dict(classes=0, with_b=0, with_c=0, with_e=0, with_f1=0, with_f2=0, u_fail=0, pl_fail=0, anti_all=0, types={})
        for i, es in enumerate(gs):
            r = analyse(n, es, full); summ['classes'] += 1
            for k in ('b', 'c', 'e', 'f1', 'f2'): summ['with_'+k] += 1 if r['role_'+k] > 0 else 0
            summ['u_fail'] += len(r['u_fail']); summ['pl_fail'] += len(r['pl_fail']); summ['anti_all'] += r['n_anti_all']
            for ty in r['anti_types']: summ['types'][ty] = summ['types'].get(ty, 0) + 1
            if len(gs) <= 40:
                print('%s #%d (n,m,tau,s)=(%d,%d,%d,%d) antiV2=%s role_b=%d role_c=%d role_e=%d role_f1=%d role_f2=%d U-fail=%s pairlemma-fail=%s' % (path.split('/')[-1], i, r['n'], r['m'], r['tau'], r['s'], r['anti_types'], r['role_b'], r['role_c'], r['role_e'], r['role_f1'], r['role_f2'], r['u_fail'], r['pl_fail']))
        print('SUMMARY %s (%s pairs): %s  [%.1fs]' % (path.split('/')[-1], 'all' if full else 'deg<=2', summ, time.time()-t0), flush=True)
