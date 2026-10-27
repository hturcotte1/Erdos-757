"""my_thm8.py -- referee's independent recomputation of the transversal data of L018 Step 8.3 for the 12 tight classes
(cells 10_7_4, 14_12_6, 17_13_7 with Delta<=3 from the refereed L013 lists, extracted into cells13/).
For each class: verify tight/connected/linear/F7-free/Hall/Delta<=3 with own code; enumerate ALL minimum transversals;
Phi = pairs in no common minimum transversal (restricted to degree<=2 vertices); admissible pairs = degree<=2, not inside an
edge; check every two disjoint admissible pairs are met by a common minimum transversal; Phi-triangles; (x,P) patterns.
Also checks (U1): every non-isolated vertex lies in some minimum transversal.  No import from experiments/prover."""
import re, itertools, glob, os
import networkx as nx

BASE = os.path.dirname(os.path.abspath(__file__))

def load(fn):
    out = []
    for line in open(fn):
        if line.startswith('FOUND'):
            out.append([tuple(map(int, t)) for t in re.findall(r'\((\d+),(\d+),(\d+)\)', line)])
    return out

def tau_edges(E):
    E = [frozenset(e) for e in E]
    best = [len(E)]
    def rec(rem, k):
        if not rem:
            best[0] = min(best[0], k); return
        if k + 1 >= best[0]: return
        e = max(rem, key=lambda f: sum(1 for g in rem if f & g))
        for v in e:
            rec([f for f in rem if v not in f], k + 1)
    rec(E, 0)
    return best[0]

def has_f7(E):
    Es = [frozenset(e) for e in E]
    for c in itertools.combinations(range(len(Es)), 5):
        U = set().union(*(Es[i] for i in c))
        if len(U) != 7: continue
        deg = {}
        for i in c:
            for v in Es[i]: deg[v] = deg.get(v, 0) + 1
        if sorted(deg.values()) == [2, 2, 2, 2, 2, 2, 3]: return True
    return False

def hall_ok(E):
    Es = [frozenset(e) for e in E]; m = len(Es)
    for mask in range(1, 1 << m):
        F = [Es[i] for i in range(m) if mask >> i & 1]
        if len(set().union(*F)) < len(F) + 2: return False
    return True

def analyse(E):
    n = 1 + max(max(e) for e in E); m = len(E)
    deg = [0] * n
    for e in E:
        for v in e: deg[v] += 1
    t = tau_edges(E)
    slack = 3 * n + 2 * m - 11 * t
    Hn = nx.Graph()
    for e in E: Hn.add_edges_from(itertools.combinations(e, 2))
    props = dict(n=n, m=m, tau=t, slack=slack, Delta=max(deg), connected=(Hn.number_of_nodes() == n and nx.is_connected(Hn)),
                 linear=all(len(set(a) & set(b)) <= 1 for a, b in itertools.combinations(E, 2)), f7free=not has_f7(E), hall=hall_ok(E),
                 degseq=''.join('%d^%d ' % (d, sum(1 for x in deg if x == d)) for d in (1, 2, 3) if any(x == d for x in deg)))
    MT = [frozenset(T) for T in itertools.combinations(range(n), t) if all(set(T) & set(e) for e in E)]
    low = [v for v in range(n) if deg[v] <= 2]
    inedge = {frozenset(p) for e in E for p in itertools.combinations(e, 2)}
    phi_all = {frozenset(p) for p in itertools.combinations(range(n), 2) if not any(p[0] in T and p[1] in T for T in MT)}
    phi_low = sorted(tuple(sorted(p)) for p in phi_all if all(deg[v] <= 2 for v in p))
    adm = [frozenset(p) for p in itertools.combinations(low, 2) if frozenset(p) not in inedge]
    pp_tot = pp_fail = 0
    for P1, P2 in itertools.combinations(adm, 2):
        if P1 & P2: continue
        pp_tot += 1
        if not any((T & P1) and (T & P2) for T in MT): pp_fail += 1
    tri = [c for c in itertools.combinations(low, 3) if all(frozenset(p) in phi_all for p in itertools.combinations(c, 2))]
    xP = [(x, tuple(sorted(P))) for x in low for P in adm if x not in P and all(frozenset((x, z)) in phi_all for z in P)]
    u1 = all(any(v in T for T in MT) for v in range(n) if deg[v] >= 1)
    return props, len(MT), phi_low, len(phi_all), pp_tot, pp_fail, tri, xP, u1

if __name__ == '__main__':
    allok = True
    for name in ['3_1_1', '10_7_4', '14_12_6', '17_13_7']:
        fn = os.path.join(BASE, 'cells13', 'cells', 'cell_%s_D3.txt' % name)
        for k, E in enumerate(load(fn)):
            props, nMT, phi_low, nphi, pp_tot, pp_fail, tri, xP, u1 = analyse(E)
            ok = props['slack'] == 0 and props['connected'] and props['linear'] and props['f7free'] and props['hall'] and props['Delta'] <= 3
            allok &= ok and (pp_fail == 0) and u1
            print('%s #%d: %s  class-C tight connected: %s | #minT=%d |Phi_all|=%d Phi_low=%s | disjoint admissible pair-pairs %d, uncovered %d | Phi-triangles(low)=%s | (x,P) patterns=%s | U1 holds=%s'
                  % (name, k, props, ok, nMT, nphi, phi_low, pp_tot, pp_fail, tri, xP, u1))
            print('      edges:', ' '.join('%d.%d.%d' % e for e in E))
    print('ALL CLASSES OK (tight, in C, connected, Delta<=3, no uncovered disjoint admissible pair-pair, U1):', allok)
