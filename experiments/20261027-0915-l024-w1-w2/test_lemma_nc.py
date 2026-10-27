"""Check Lemma NC (Claim B + Claim E  =>  for every clause e and piece i with nonempty trace A, some other clause has nonempty trace A'
in piece i with A, A' disjoint and every pair (a,a') non-co-transversal) on all Claim-B sets of the custom instances of test_search_custom.py."""
import sys, itertools
sys.argv = ['x']
sys.path.insert(0, '/home/user/Erdos-757/experiments/20261027-0915-l024-w1-w2')
exec(open('/home/user/Erdos-757/experiments/20261027-0915-l024-w1-w2/test_search_custom.py').read().split("tests = [")[0])
def claimE_generic(S, clauses):
    k = S.k
    for r in range(1, k + 1):
        for Y in itertools.combinations(range(k), r):
            vm = 0
            for i in Y: vm |= ((1 << S.Ps[i]['n']) - 1) << S.offs[i]
            if sum(1 for c in clauses if any(vm >> x & 1 for x in c)) < r + 1: return False
    return True
def nc_pair(S, i, a, b):
    return a != b and not any((T >> a & 1) and (T >> b & 1) for T in S.MT[i])
tests = [((E1,), 3, None), ((E1, E1), 3, None), ((E1, Q0), 2, None), ((Q0,), 3, None), ((Q1,), 3, None), ((E1, E1, E1), 2, None), ((T1,), 3, [0, 1, 2, 3])]
tot = dict(sets=0, claimE_sets=0, violations=0)
for names, ms, verts in tests:
    S = custom([by[n] for n in names], ms, verts)
    sets = search(S, {'nodes': 0})
    for x in sets:
        tot['sets'] += 1
        cl = [S.cands[c] for c in sorted(x)]
        if not claimE_generic(S, cl): continue
        tot['claimE_sets'] += 1
        for p, e in enumerate(cl):
            for i in range(S.k):
                A = [v for v in e if S.piece_of[v] == i]
                if not A: continue
                ok = False
                for q, f in enumerate(cl):
                    if q == p: continue
                    A2 = [v for v in f if S.piece_of[v] == i]
                    if A2 and not set(A) & set(A2) and all(nc_pair(S, i, a, b) for a in A for b in A2): ok = True; break
                if not ok: tot['violations'] += 1
    print(names, tot, flush=True)
print('LEMMA NC CHECK', tot)
