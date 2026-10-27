"""Validate w1.search (level search with WLOG labelling + min-index e1 + avoid/N pruning) against brute force on REAL pieces with
a custom clause family (all nonempty subsets of size <= 3 of the vertex set, no linearity/degree rules), where Claim B positives abound
(e.g. one E1: clauses {0},{1}).  Also verifies the final Claim B verdict on every found set against the definition (all tuples of
minimum transversals)."""
import sys, itertools, time
sys.argv = ['x']
sys.path.insert(0, '/home/user/Erdos-757/experiments/20261027-0915-l024-w1-w2')
from w1 import *
pieces = load_pieces(); by = {P['name']: P for P in pieces}
E1 = '(3,1,1)#0'; Q0 = '(8,5,3)#0'; Q1 = '(8,5,3)#1'; T1 = '(10,7,4)#1'
def custom(Ps, maxsize=3, verts=None):
    S = Setup(Ps, need2=False)
    vs = list(range(S.N)) if verts is None else verts
    cands = []
    for r in range(1, maxsize + 1):
        for c in itertools.combinations(vs, r): cands.append(c)
    S.cands = cands; S.nc = len(cands)
    S.cmask = [sum(1 << x for x in c) for c in cands]
    S.cap = [99] * S.N
    S.cw = [0] * S.N
    for i, c in enumerate(cands):
        for x in c: S.cw[x] |= 1 << i
    S.incompat = [0] * S.nc          # no linearity rule
    S.chit = []
    for c in cands:
        row = [0] * S.k
        for x in c: row[S.piece_of[x]] |= S.hitbits[S.piece_of[x]][x]
        S.chit.append(row)
    S.all_c = (1 << S.nc) - 1
    return S
def brute_def(S):
    K = S.k + 1; res = set()
    for sub in itertools.combinations(range(S.nc), K):
        masks = [S.cmask[c] for c in sub]
        viol = False
        for Ts in itertools.product(*S.MT):
            U = 0
            for T in Ts: U |= T
            if all(U & m for m in masks): viol = True; break
        if not viol: res.add(frozenset(sub))
    return res
tests = [((E1,), 3, None), ((E1, E1), 3, None), ((E1, Q0), 2, None), ((Q0,), 3, None), ((Q1,), 3, None), ((E1, E1, E1), 2, None),
         ((T1,), 3, [0, 1, 2, 3]), ((Q0, E1), 3, [0, 1, 2, 3, 4, 8, 9, 10])]
allok = True
for names, ms, verts in tests:
    S = custom([by[n] for n in names], ms, verts)
    t = time.time()
    a = search(S, {'nodes': 0})
    b = brute_def(S) if S.nc <= 80 or S.k == 1 else None
    if b is None:
        # too big for full brute: check every found set against the definition and that found sets are Claim B
        okc = all(S.claimB_brute(sorted(x)) for x in a)
        print(names, 'cands', S.nc, 'search', len(a), 'brute skipped; found sets all Claim B:', okc, f'{time.time()-t:.0f}s', flush=True)
    else:
        ok = a == b; allok &= ok
        print(names, 'cands', S.nc, 'search', len(a), 'brute(definition)', len(b), 'MATCH' if ok else 'MISMATCH', f'{time.time()-t:.0f}s', flush=True)
print('ALL MATCH' if allok else 'SOME MISMATCH')
