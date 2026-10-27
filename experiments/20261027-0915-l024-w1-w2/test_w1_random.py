"""Randomised validation of w1.search (level search with WLOG labelling, pruning) against brute force over all
(k+1)-subsets of candidate edges, on random small hypergraph 'pieces' (the Claim B machinery does not depend on membership
in L*).  Also checks the final Claim B verdict against a definition-level test."""
import sys, itertools, random, time
sys.argv = ['x']
sys.path.insert(0, '/home/user/Erdos-757/experiments/20261027-0915-l024-w1-w2')
from w1 import *
random.seed(12345)
def rand_piece(nv, ne):
    while True:
        edges = set()
        tries = 0
        used_pairs = set()
        while len(edges) < ne and tries < 100:
            tries += 1
            e = tuple(sorted(random.sample(range(nv), 3)))
            ps = list(itertools.combinations(e, 2))
            if any(p in used_pairs for p in ps): continue
            edges.add(e); used_pairs.update(ps)
        edges = sorted(edges)
        d = degrees(nv, edges)
        if min(d) == 0: continue
        t = tau(nv, edges)
        return dict(name='rnd', n=nv, edges=edges, tau=t, deg=d, mts=min_transversals(nv, edges, t), m=len(edges), W=0)
def brute(S):
    K = S.k + 1; res = set()
    for sub in itertools.combinations(range(S.nc), K):
        use = [0] * S.N; ok = True
        for c in sub:
            for x in S.cands[c]:
                use[x] += 1
                if use[x] > S.cap[x]: ok = False
        if not ok: continue
        if any(S.incompat[a] >> b & 1 for a, b in itertools.combinations(sub, 2)): continue
        masks = [S.cmask[c] for c in sub]
        viol = False
        for Ts in itertools.product(*S.MT):
            U = 0
            for T in Ts: U |= T
            if all(U & m for m in masks): viol = True; break
        if not viol: res.add(frozenset(sub))
    return res
tot = dict(trials=0, pos=0, mism=0, total_sets=0)
t0 = time.time()
for trial in range(400):
    k = random.choice([1, 2, 2, 3])
    Ps = [rand_piece(random.choice([5, 6, 7]), random.choice([2, 3, 3, 4])) for _ in range(k)]
    S = Setup(Ps, need2=random.choice([True, False]))
    if S.nc > 70 or S.nc < S.k + 1: continue
    a = search(S, {'nodes': 0}); b = brute(S)
    tot['trials'] += 1; tot['total_sets'] += len(b)
    if b: tot['pos'] += 1
    if a != b:
        tot['mism'] += 1; print('MISMATCH', [P['edges'] for P in Ps], len(a), len(b))
print(tot, f'{time.time()-t0:.0f}s')
