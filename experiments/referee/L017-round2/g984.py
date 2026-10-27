import itertools
GS = [[(0,1,2),(0,3,4),(1,6,7),(2,5,8),(3,5,7),(3,6,8),(4,5,6),(4,7,8)], [(0,1,4),(0,2,3),(1,7,8),(2,5,6),(3,5,8),(3,6,7),(4,5,7),(4,6,8)]]
F7 = [(0,1,2),(0,3,4),(0,5,6),(1,3,5),(2,4,6)]
def tau(vs, E):
    es = [set(e) for e in E if set(e) <= set(vs)]
    for k in range(len(vs)+1):
        for S in itertools.combinations(vs, k):
            if all(set(S) & e for e in es): return k
def sl(vs, E): return 3*len(vs) + 2*len([e for e in E if set(e) <= set(vs)]) - 11*tau(vs, E)
def has_F7(n, E):
    Es = set(frozenset(e) for e in E)
    for p in itertools.permutations(range(n), 7):
        if all(frozenset(p[i] for i in f) in Es for f in F7): return True
    return False
for E in GS:
    n = 9; V = list(range(n))
    lin = all(len(set(a) & set(b)) <= 1 for a, b in itertools.combinations(E, 2))
    bad = [Z for k in range(1, n+1) for Z in itertools.combinations(V, k) if sl([v for v in V if v not in Z], E) < 0]
    p3 = all(len([e for e in E if set(e) <= set(S)]) <= len(S) - 2 for k in range(2, n+1) for S in itertools.combinations(V, k))
    deg = [sum(1 for e in E if v in e) for v in V]
    print('n=9 m=8 tau=%d s=%d linear=%s F7-free=%s P3=%s vertex-critical=%s degrees=%s' % (tau(V, E), sl(V, E), lin, not has_F7(n, E), p3, not bad, deg))
