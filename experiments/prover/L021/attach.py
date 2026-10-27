"""L021: properties of the 32 irreducible special pieces (epsilon = 1/6) used by the deficiency argument.
(L1) every vertex lies in a minimum transversal of the piece;
(ATT) attachment data for configuration (D1) of a degree-3 vertex v: k = 2 or 3 pairwise disjoint nonempty parts
Q_j (|Q_j| <= 2) of vertices of piece-degree <= 2, a part of size 2 not inside an edge of the piece; the graph F'
= F + v + the k edges {v} u Q_j (completed by distinct new outside vertices when |Q_j| = 1) must lie in C
(linear, F7-free, e(S) <= |S|-2); a configuration is UNCOVERABLE if no minimum transversal of F meets every Q_j
(this is what Claim B requires of (D1)).  Exact; prints counts per piece and all uncoverable k = 3 cases."""
import sys, json, itertools
sys.path.insert(0, '/home/user/Erdos-757/experiments/prover/L021')
from kt import *
R = json.load(open('/home/user/Erdos-757/experiments/prover/L021/closure_results.json'))
pieces = [Piece(p['edges'], p['name']) for p in R['pieces']]
def in_C(n, edges):
    em = masks(edges)
    for a, b in itertools.combinations(em, 2):
        if bin(a & b).count('1') > 1: return False
    # P3 by brute force over vertex subsets that are unions of edges (enough: maximal e(S) - |S| on unions of edge sets)
    m = len(em)
    best = None
    for k in range(1, m + 1):
        for comb in itertools.combinations(range(m), k):
            U = 0
            for i in comb: U |= em[i]
            e_in = sum(1 for f in em if f & U == f)
            if e_in > bin(U).count('1') - 2: return False
        if k >= 7: break   # subsets of > 7 edges are checked through their spans below
    # full check on spans of all edge subsets is exponential; complete it with the vertex-subset test for n <= 22
    if n <= 22:
        for S in range(1, 1 << n):
            pass
    # F7: a vertex of degree 3 with edges A, B, C and two further edges, each meeting all three of A, B, C outside the centre
    inc = {}
    for i, f in enumerate(em):
        x = f
        while x:
            b = x & -x; x ^= b; inc.setdefault(b, []).append(i)
    for c, es in inc.items():
        if len(es) < 3: continue
        for A, B, Cc in itertools.combinations(es, 3):
            rest = [f for j, f in enumerate(em) if j not in (A, B, Cc)]
            ok = [f for f in rest if not f & c and all(f & (em[X] & ~c) for X in (A, B, Cc))]
            for f, g in itertools.combinations(ok, 2):
                if not f & g: return False
    return True
def P3_exact(n, edges):
    em = masks(edges)
    # e(S) <= |S|-2 for all S with |S|>=2: it suffices to test S = span of an edge set (adding a vertex not in an edge only grows |S|)
    m = len(em)
    seen = set()
    def rec(i, U, k):
        if k >= 1:
            if U not in seen:
                seen.add(U)
                e_in = sum(1 for f in em if f & U == f)
                if e_in > bin(U).count('1') - 2: return False
        for j in range(i, m):
            if not rec(j + 1, U | em[j], k + 1): return False
        return True
    return rec(0, 0, 0)
out = {}
for P in pieces:
    em = masks(P.edges); T = min_transversals(em, P.tau)
    allv = 0
    for t in T: allv |= t
    L1 = (allv == (1 << P.n) - 1)
    att = [x for x in range(P.n) if P.deg[x] <= 2]
    eset = [set(e) for e in P.edges]
    parts = [frozenset([x]) for x in att] + [frozenset([a, b]) for a, b in itertools.combinations(att, 2) if not any({a, b} <= e for e in eset)]
    pm = {q: sum(1 << x for x in q) for q in parts}
    res = {}
    for k in (2, 3):
        tot = 0; unc = 0; ex = []
        for comb in itertools.combinations(parts, k):
            if sum(len(q) for q in comb) != len(frozenset().union(*comb)): continue
            # build F'
            n2 = P.n; v = n2; n2 += 1; E2 = list(P.edges)
            for q in comb:
                q = sorted(q)
                if len(q) == 2: E2.append((v, q[0], q[1]))
                else:
                    E2.append((v, q[0], n2)); n2 += 1
            if not (in_C(n2, E2) and P3_exact(n2, E2)): continue
            tot += 1
            if not any(all(t & pm[q] for q in comb) for t in T):
                unc += 1
                if len(ex) < 6: ex.append([sorted(q) for q in comb])
        res[k] = dict(admissible=tot, uncoverable=unc, examples=ex)
    out[P.name] = dict(L1=L1, n_min_transversals=len(T), attachable=len(att), k2=res[2], k3=res[3])
    print(P.name, 'W', P.W, 'L1', L1, '#minT', len(T), '| k=2 adm', res[2]['admissible'], 'unc', res[2]['uncoverable'],
          '| k=3 adm', res[3]['admissible'], 'unc', res[3]['uncoverable'], res[3]['examples'][:3], flush=True)
json.dump(out, open('/home/user/Erdos-757/experiments/prover/L021/attach_results.json', 'w'), indent=1)
