"""Validate nc-mode search (NC candidate filter, Claim-E pruning, NC-packing and last-edge pruning) against brute force on
instances with L1 pieces where (Claim B and Claim E) sets exist: pieces = E1, E1+E1 (disjoint), real Q0/Q1/T1.
Compares the set of (Claim B and Claim E) edge sets from the nc search with those from the full brute force."""
import sys, itertools, time
sys.argv = ['x']
sys.path.insert(0, '/home/user/Erdos-757/experiments/20261027-0915-l024-w1-w2')
from w1 import *
pieces = load_pieces(); by = {P['name']: P for P in pieces}
def mk(name, parts):
    n = 0; edges = []
    for P in parts:
        edges += [tuple(x + n for x in e) for e in P['edges']]; n += P['n']
    t = tau(n, edges)
    return dict(name=name, n=n, edges=edges, tau=t, deg=degrees(n, edges), mts=min_transversals(n, edges, t), m=len(edges), W=0)
E1 = by['(3,1,1)#0']; Q0 = by['(8,5,3)#0']; Q1 = by['(8,5,3)#1']; T1 = by['(10,7,4)#1']
E2 = mk('E1+E1', [E1, E1]); E3 = mk('E1+E1+E1', [E1, E1, E1])
tests = [(E1, E2), (E1, E1, E1), (E2, E2), (E1, Q0), (E1, E1, Q0), (E1, E3), (Q0, Q0)]
def claimE_sets(S, sub):
    return claimE(S, [S.cands[c] for c in sub])
tot = {}
for Ps in tests:
    S = Setup(list(Ps), need2=True)
    t = time.time()
    K = S.k + 1
    bE = set()
    nB = 0
    for sub in itertools.combinations(range(S.nc), K):
        use = [0] * S.N; ok = True
        for c in sub:
            for x in S.cands[c]:
                use[x] += 1
                if use[x] > S.cap[x]: ok = False
        if not ok: continue
        if any(S.incompat[a] >> b & 1 for a, b in itertools.combinations(sub, 2)): continue
        if S.claimB_brute(list(sub)):
            nB += 1
            if claimE_sets(S, sub): bE.add(frozenset(S.cands[c] for c in sub))
    S2 = Setup(list(Ps), need2=True, nc_only=True)
    a = search(S2, {'nodes': 0}) if S2.nc >= K else set()
    aE = {frozenset(S2.cands[c] for c in x) for x in a if claimE_sets(S2, sorted(x))}
    print([P['name'] for P in Ps], 'cands', S.nc, 'ncands', S2.nc, 'ClaimB', nB, 'B&E brute', len(bE), 'B&E nc-search', len(aE),
          'MATCH' if aE == bE else 'MISMATCH', f'{time.time()-t:.0f}s', flush=True)
