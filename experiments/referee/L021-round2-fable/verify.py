#!/usr/bin/env python3
"""Referee #4 round 2 (fable) for L021: independent recomputation.
No import of e757, judge, or experiments/prover/L021/kt.py.
(1) 18 hypertrees of cell(27,13,9,3): parse, class-C checks, tau, induced copies of all 32 pieces,
    exact DEF over disjoint families, A and P = A + DEF.
(2) The 32 pieces of closure_results.json: recompute n, m, tau, A, W, I11 slack s from the edge lists.
(3) Exact arithmetic for the edited passages (KT* remark, sign fix, 7.6 slack bookkeeping)."""
import json, sys, itertools, re
from fractions import Fraction

ROOT = '/home/user/Erdos-757'

def parse_list(path):
    graphs = []
    for line in open(path):
        if line.startswith('FOUND:'):
            edges = [tuple(int(x) for x in t.split(',')) for t in re.findall(r'\((\d+,\d+,\d+)\)', line)]
            graphs.append([frozenset(e) for e in edges])
    return graphs

def vertices(E):
    return sorted(set().union(*E)) if E else []

def is_linear(E):
    return all(len(a & b) <= 1 for a, b in itertools.combinations(E, 2)) and len(set(E)) == len(E) and all(len(e) == 3 for e in E)

def components(E, V):
    adj = {v: set() for v in V}
    for e in E:
        for a in e:
            adj[a] |= e - {a}
    seen, comps = set(), []
    for v in V:
        if v in seen: continue
        stack, comp = [v], set()
        while stack:
            x = stack.pop()
            if x in comp: continue
            comp.add(x); stack.extend(adj[x] - comp)
        seen |= comp; comps.append(comp)
    return comps

def degrees(E, V):
    d = {v: 0 for v in V}
    for e in E:
        for a in e: d[a] += 1
    return d

F7 = [frozenset(s) for s in [(0,1,2),(0,3,4),(0,5,6),(1,3,5),(2,4,6)]]
def has_F7(E):
    # F7 as a (not necessarily induced) subhypergraph: 5 edges on 7 vertices, degree seq (3,2,2,2,2,2,2),
    # every pair of edges meets; linear. For linear E this characterises F7 uniquely? Check by explicit isomorphism.
    for S in itertools.combinations(E, 5):
        V = set().union(*S)
        if len(V) != 7: continue
        d = degrees(S, V)
        if sorted(d.values()) != [2,2,2,2,2,2,3]: continue
        if iso(list(S), F7): return True
    return False

def iso(E1, E2):
    """Backtracking isomorphism test between two 3-graphs given as edge lists (frozensets)."""
    V1, V2 = vertices(E1), vertices(E2)
    if len(V1) != len(V2) or len(E1) != len(E2): return False
    d1, d2 = degrees(E1, V1), degrees(E2, V2)
    if sorted(d1.values()) != sorted(d2.values()): return False
    S2 = set(E2)
    order = sorted(V1, key=lambda v: -d1[v])
    def bt(i, f, used):
        if i == len(order):
            return all(frozenset(f[x] for x in e) in S2 for e in E1)
        v = order[i]
        for w in V2:
            if w in used or d1[v] != d2[w]: continue
            # partial consistency: edges of E1 fully mapped must be in E2
            f[v] = w
            ok = True
            for e in E1:
                if v in e and all(x in f for x in e):
                    if frozenset(f[x] for x in e) not in S2: ok = False; break
            if ok:
                used.add(w)
                if bt(i+1, f, used): return True
                used.discard(w)
            del f[v]
        return False
    return bt(0, {}, set())

def P3_ok(E):
    """e(S) <= |S|-2 for all |S|>=2  <=>  |V(U)| >= |U|+2 for every nonempty edge subset U."""
    m = len(E)
    for k in range(1, m+1):
        for U in itertools.combinations(E, k):
            if len(set().union(*U)) < k + 2: return False
    return True

def tau(E):
    """Exact transversal number by branching on an uncovered edge, with the matching lower bound as pruning."""
    best = [len(vertices(E))]
    def lb(rem):
        # greedy disjoint edges give a lower bound
        used, cnt = set(), 0
        for e in rem:
            if not (e & used): used |= e; cnt += 1
        return cnt
    def rec(rem, size):
        if not rem:
            if size < best[0]: best[0] = size
            return
        if size + lb(rem) >= best[0]: return
        e = min(rem, key=lambda x: 0)  # any uncovered edge
        for v in sorted(e):
            rec([f for f in rem if v not in f], size + 1)
    rec(list(E), 0)
    return best[0]

def induced_copies(E, piece):
    """All induced copies of `piece` (edge list) in E: choose m_F edges, union must have n_F vertices,
    no other edge of E inside the union, and the chosen edges must be isomorphic to the piece."""
    nF, mF = len(vertices(piece)), len(piece)
    copies = []
    for S in itertools.combinations(E, mF):
        U = set().union(*S)
        if len(U) != nF: continue
        if any(e <= U for e in E if e not in S): continue
        if iso(list(S), piece): copies.append(frozenset(U))
    return copies

def DEF_exact(E, copies_w):
    """copies_w: list of (vertexset, W). Maximise sum W - 35 |E*| over vertex-disjoint subfamilies (exhaustive)."""
    best = 0
    best_fam = ()
    N = len(copies_w)
    def estar(fam):
        VX = set().union(*[c for c, _ in fam]) if fam else set()
        inside = set()
        for c, _ in fam:
            for e in E:
                if e <= c: inside.add(e)
        return sum(1 for e in E if (e & VX) and e not in inside)
    def rec(i, fam, VX):
        nonlocal best, best_fam
        if i == N:
            val = sum(w for _, w in fam) - 35 * estar(fam)
            if val > best: best, best_fam = val, tuple(fam)
            return
        rec(i+1, fam, VX)
        c, w = copies_w[i]
        if not (c & VX):
            rec(i+1, fam + [(c, w)], VX | c)
    rec(0, [], set())
    return best, best_fam

def A_of(n, m, t): return 27*n + 35*m - 132*t
def s_of(n, m, t): return 3*n + 2*m - 11*t

def main():
    out = []
    def pr(*a):
        s = ' '.join(str(x) for x in a); print(s); out.append(s)

    # ---- (2) the 32 pieces
    cr = json.load(open(f'{ROOT}/experiments/prover/L021/closure_results.json'))
    pieces = []
    for p in cr['pieces']:
        E = [frozenset(e) for e in p['edges']]
        V = vertices(E); n, m = len(V), len(E); t = tau(E)
        A = A_of(n, m, t); W = -A; s = s_of(n, m, t)
        ok = (n, m, t, W) == (p['n'], p['m'], p['tau'], p['W']) and is_linear(E) and len(components(E, V)) == 1 \
             and max(degrees(E, V).values()) <= 3 and not has_F7(E) and P3_ok(E)
        pieces.append((p['name'], E, W, n, m, t, s, ok))
    pr('pieces:', len(pieces), 'all consistent with json and in connected C_3:', all(x[-1] for x in pieces))
    pr('weights by cell:', sorted(set((x[3], x[4], x[5], x[2]) for x in pieces)))
    pr('I11 slacks s of pieces:', sorted(set((x[3], x[4], x[5], x[6]) for x in pieces)), ' max s =', max(x[6] for x in pieces))
    pr('7.6 bookkeeping: s(F_1 + v) = s(F_1) + 3 + 6 - 11 = s(F_1) - 2 ; max over pieces =', max(x[6] for x in pieces) - 2, '< 0:', max(x[6] for x in pieces) - 2 < 0)
    pr('n(F_1)+1 max =', max(x[3] for x in pieces) + 1, '<= 27 (L016 range)')

    # ---- (1) the 18 hypertrees
    G = parse_list(f'{ROOT}/experiments/20261027-0730-kt-cells/lists/cell_27_13_9_D3.txt')
    pr('graphs parsed:', len(G))
    allP = []
    for gi, E in enumerate(G):
        V = vertices(E); n, m = len(V), len(E)
        assert V == list(range(27)), 'vertex labels not 0..26'
        lin = is_linear(E); conn = len(components(E, V)) == 1; D = max(degrees(E, V).values())
        f7 = has_F7(E); p3 = P3_ok(E); t = tau(E)
        hypertree = conn and n == 2*m + 1
        # induced copies of every piece
        copies_w = []
        per_piece = {}
        for name, PE, W, pn, pm, pt, ps, _ in pieces:
            cs = induced_copies(E, PE)
            if cs: per_piece[name] = len(cs)
            copies_w += [(c, W) for c in cs]
        D_, fam = DEF_exact(E, copies_w)
        A = A_of(n, m, t); P = A + D_
        allP.append(P)
        # structure of the optimal family
        k = len(fam); 
        pr(f'graph {gi:2d}: n={n} m={m} linear={lin} conn={conn} Delta={D} F7={f7} P3={p3} hypertree={hypertree} tau={t} '
           f'copies={dict(per_piece)} A={A} DEF={D_} P={P} |X|={k} E*={ (sum(w for _,w in fam) - D_)//35 if fam else 0}')
        assert lin and conn and D <= 3 and not f7 and p3 and (n, m, t) == (27, 13, 9)
    pr('all 18: A=-4, DEF=4, P=0 :', all(p == 0 for p in allP) and len(allP) == 18)

    # pairwise non-isomorphism of the 18 (own backtracking test)
    niso = 0
    for i, j in itertools.combinations(range(len(G)), 2):
        if iso(G[i], G[j]): niso += 1
    pr('isomorphic pairs among the 18:', niso)

    # ---- (3) exact arithmetic for the edited passages
    pr('A(21,10,7) =', A_of(21,10,7), ' s =', s_of(21,10,7))
    pr('A(27,13,9) =', A_of(27,13,9), ' s =', s_of(27,13,9))
    pr('A = 12 s - 9 n + 11 m check on (21,10,7),(27,13,9),(14,12,6):',
       all(A_of(n,m,t) == 12*s_of(n,m,t) - 9*n + 11*m for n,m,t in [(21,10,7),(27,13,9),(14,12,6)]))
    pr('saturated m=n-2: A = 12 s + 2n - 22 check:', all(A_of(n,n-2,t) == 12*s_of(n,n-2,t) + 2*n - 22 for n in range(5,30) for t in range(1,n)))
    pr('HY slack floor with m=n-2: s >= (m-4n)/17 = -(3n+2)/17 check:', all(Fraction(n-2-4*n,17) == Fraction(-(3*n+2),17) for n in range(3,40)))
    hyper = [(k, A_of(6*k+3, 3*k+1, 2*k+1), 16*(2*k+1) - 35*k) for k in range(0, 7)]
    pr('hypertrees with perfect matching (k, A, DEF_matching-family):', hyper, ' A == 3k-16:', all(a == 3*k-16 for k,a,_ in hyper), ' DEF_M == 16-3k:', all(d == 16-3*k for k,_,d in hyper))
    pr('general perfect matching M, tau=|M|=n/3: A + DEF_M = 27n -132|M| + 16|M| -35(m-|M|) +35 m ... = 27n - 81|M| = 0 :',
       all(27*n - 81*(n//3) == 0 for n in range(3, 100, 3)))
    pr('Theorem 1: 35/66 > 9/17 :', Fraction(35,66) > Fraction(9,17), ' (6-eps)/11 > 9/17 iff eps < 3/17:',
       all(((Fraction(6,1)-e)/11 > Fraction(9,17)) == (e < Fraction(3,17)) for e in [Fraction(0), Fraction(1,6), Fraction(3,17)-Fraction(1,1000), Fraction(3,17), Fraction(1,5)]))
    pr('G2 remark: 19|X| - 43 > 0 for |X| >= 3 :', 19*3 - 43)
    open(f'{ROOT}/experiments/referee/L021-round2-fable/verify_output.txt', 'w').write('\n'.join(out) + '\n')

if __name__ == '__main__':
    main()
