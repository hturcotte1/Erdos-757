"""Validation of w1.search against brute force (all (k+1)-subsets of candidate edges) on small piece types."""
import sys, itertools, time
sys.argv = ['x']
sys.path.insert(0, '/home/user/Erdos-757/experiments/20261027-0915-l024-w1-w2')
from w1 import *
pieces = load_pieces(); by = {P['name']: P for P in pieces}
E1 = '(3,1,1)#0'; Q0 = '(8,5,3)#0'; Q1 = '(8,5,3)#1'; T1 = '(10,7,4)#1'; T0 = '(10,7,4)#0'
def brute(S):
    K = S.k + 1; res = set()
    for sub in itertools.combinations(range(S.nc), K):
        ok = True
        use = [0] * S.N
        for c in sub:
            for x in S.cands[c]:
                use[x] += 1
                if use[x] > S.cap[x]: ok = False
        if not ok: continue
        if any(S.incompat[a] >> b & 1 for a, b in itertools.combinations(sub, 2)): continue
        if S.claimB_brute(list(sub)): res.add(frozenset(sub))
    return res
def brute2(S):
    """independent Claim B test straight from the definition (enumerate all tuples of min transversals)."""
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
tests = [(Q0,), (Q1,), (T1,), (Q0, E1), (Q0, Q0), (E1, E1, E1), (Q0, E1, E1)]
for names in tests:
    S = Setup([by[n] for n in names], need2=False)
    t = time.time()
    st = {'nodes': 0}
    a = search(S, st)
    b = brute(S)
    c = brute2(S) if S.nc <= 150 else None
    print(names, 'cands', S.nc, 'search', len(a), 'brute', len(b), 'brute2', None if c is None else len(c),
          'MATCH' if a == b and (c is None or c == b) else 'MISMATCH', f'{time.time()-t:.0f}s', flush=True)
