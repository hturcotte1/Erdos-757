"""tight_glue.py -- the case s = -2 under Conjecture T' (certificate L018, Theorem 8).
For each connected tight member of C with Delta<=3 (the 13 classes: single edge, 4 x (10,7,4), 2 x (14,12,6), 6 x (17,13,7);
lists from experiments/prover/L013/cells.tar.gz), compute all minimum transversals and
 Phi(F)  = pairs {x,z} of vertices lying in no common minimum transversal,
 PP(F)   = pairs of disjoint pairs {P1,P2} (each pair not contained in an edge of F, all four vertices of degree <= 2)
           such that no minimum transversal meets both P1 and P2 (should be empty),
 and then decide, for every pair of pieces (F1,F2) with 1 + n1 + n2 >= 28, whether a failing gluing pattern exists:
   (s,s,s): {x1,x2,x3} triangle of Phi(F1) and {x1',x2',x3'} triangle of Phi(F2) (all of degree <= 2);
   (1,2,s): P1 in F1, x3 in F1 Phi-adjacent to both vertices of P1; P2 in F2, x3' Phi-adjacent to both of P2;
   (1,s,s): P1 in F1, x2,x3 in F1 each Phi-adjacent to both vertices of P1; x2'x3' in Phi(F2); (and mirrored).
 Exact; brute force over vertex choices."""
import re, itertools
from hg import tau_of
def load(fn):
    G = []
    for line in open(fn):
        if line.startswith('FOUND'):
            G.append([tuple(map(int, t)) for t in re.findall(r'\((\d+),(\d+),(\d+)\)', line)])
    return G
pieces = []
for name in ['10_7_4', '14_12_6', '17_13_7']:
    for E in load('cells13/cells/cell_%s_D3.txt' % name):
        pieces.append((name, E))
def analyse(E):
    n = 1 + max(max(e) for e in E)
    t = tau_of(E)
    MT = []
    for T in itertools.combinations(range(n), t):
        s = set(T)
        if all(s & set(e) for e in E): MT.append(frozenset(T))
    d = [0]*n
    for e in E:
        for v in e: d[v] += 1
    low = [v for v in range(n) if d[v] <= 2]
    inedge = set()
    for e in E:
        for a, b in itertools.combinations(e, 2): inedge.add(frozenset((a, b)))
    phi = set()
    for x, z in itertools.combinations(range(n), 2):
        if not any(x in T and z in T for T in MT): phi.add(frozenset((x, z)))
    # PP failures
    ppfail = 0; pptot = 0
    pairs = [frozenset(p) for p in itertools.combinations(low, 2) if frozenset(p) not in inedge]
    for P1, P2 in itertools.combinations(pairs, 2):
        if P1 & P2: continue
        pptot += 1
        if not any((T & P1) and (T & P2) for T in MT): ppfail += 1
    return dict(n=n, t=t, MT=MT, d=d, low=low, phi=phi, pairs=pairs, ppfail=ppfail, pptot=pptot)
A = [analyse(E) for _, E in pieces]
for (name, E), a in zip(pieces, A):
    philow = [tuple(sorted(p)) for p in a['phi'] if all(a['d'][v] <= 2 for v in p)]
    print(name, 'n=%d tau=%d #minT=%d #low=%d |Phi|=%d |Phi on low|=%d PP: %d failing of %d' % (a['n'], a['t'], len(a['MT']), len(a['low']), len(a['phi']), len(philow), a['ppfail'], a['pptot']), sorted(philow))
def tri(a):
    L = a['low']; out = []
    for x, y, z in itertools.combinations(L, 3):
        if frozenset((x, y)) in a['phi'] and frozenset((y, z)) in a['phi'] and frozenset((x, z)) in a['phi']: out.append((x, y, z))
    return out
def vp(a):
    """(x, P): x low vertex, P a non-edge pair of low vertices not containing x, x Phi-adjacent to both vertices of P"""
    out = []
    for x in a['low']:
        for P in a['pairs']:
            if x in P: continue
            if all(frozenset((x, z)) in a['phi'] for z in P): out.append((x, tuple(sorted(P))))
    return out
def phil(a):
    return [tuple(sorted(p)) for p in a['phi'] if all(a['d'][v] <= 2 for v in p)]
fails = 0
for i, j in itertools.combinations_with_replacement(range(len(pieces)), 2):
    a, b = A[i], A[j]
    if 1 + a['n'] + b['n'] < 28: continue
    T1, T2 = tri(a), tri(b)
    V1, V2 = vp(a), vp(b)
    # (s,s,s)
    f_sss = len(T1) > 0 and len(T2) > 0
    # (1,2,s): needs a vp in F1 and a vp in F2 (vertex x3 not in P1 etc.; disjointness inside one piece automatic)
    f_12s = len(V1) > 0 and len(V2) > 0
    # (1,s,s): P1 in F1 with two vertices x2,x3 (distinct, not in P1) each Phi-adjacent to both of P1; x2'x3' in Phi(F2)
    def two_vp(a):
        cnt = 0
        for P in a['pairs']:
            xs = [x for x in a['low'] if x not in P and all(frozenset((x, z)) in a['phi'] for z in P)]
            if len(xs) >= 2: cnt += 1
        return cnt
    f_1ss = (two_vp(a) > 0 and len(phil(b)) > 0) or (two_vp(b) > 0 and len(phil(a)) > 0)
    status = 'FAILING PATTERN POSSIBLE' if (f_sss or f_12s or f_1ss) else 'no failing pattern'
    if f_sss or f_12s or f_1ss: fails += 1
    print('pieces (%s#%d, %s#%d) n=%d: triangles %d/%d, vp %d/%d, two_vp %d/%d -> %s' % (pieces[i][0], i, pieces[j][0], j, 1 + a['n'] + b['n'], len(T1), len(T2), len(V1), len(V2), two_vp(a), two_vp(b), status))
print('piece pairs with a possible failing pattern:', fails)
