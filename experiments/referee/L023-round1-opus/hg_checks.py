"""Referee L023 round 1 (own code; no import of e757/, judge/ or any prover script).
Checks on the six classes X_0..X_5 of the certificate and on Q8:
  * parse the certificate's X_i lines; compare with the stored list and the json (as sets of edge sets);
  * membership in C from the definitions: distinct triples, linear, F7-free (subgraph search), (P3) by brute force over ALL vertex
    subsets (numpy bitmasks), connected, tau exactly (branching on an uncovered edge; complete), max degree;
  * pairwise non-isomorphism by colour refinement (1-WL) on the vertex-edge incidence graph (different histograms => non-isomorphic);
  * Q8 in C; every embedding of Q8 into each X_i (explicit vertex map, every Q8 edge checked to be an X_i edge)."""
import re, sys, json, itertools
import numpy as np
from collections import Counter

def parse(line):
    return [tuple(sorted(map(int, t.split(',')))) for t in re.findall(r'\((\d+,\d+,\d+)\)', line)]

def is_linear(E):
    for e, f in itertools.combinations(E, 2):
        if len(set(e) & set(f)) > 1: return False
    return True

def has_F7(E):
    Es = set(frozenset(e) for e in E); inc = {}
    for e in E:
        for v in e: inc.setdefault(v, []).append(e)
    for v0, es in inc.items():
        for e1, e2, e3 in itertools.combinations(es, 3):
            P = [tuple(x for x in e if x != v0) for e in (e1, e2, e3)]
            if len(set(P[0]) | set(P[1]) | set(P[2])) != 6: continue
            for choice in itertools.product((0, 1), repeat=3):
                f = frozenset(P[i][choice[i]] for i in range(3)); g = frozenset(P[i][1 - choice[i]] for i in range(3))
                if f in Es and g in Es: return True
    return False

def p3_bruteforce(E, n):
    """max over S, |S| >= 2, of e(S) - |S| + 2 must be <= 0. All 2^n subsets."""
    S = np.arange(1 << n, dtype=np.int64)
    cnt = np.zeros(1 << n, dtype=np.int16)
    for e in E:
        m = sum(1 << v for v in e)
        cnt += ((S & m) == m).astype(np.int16)
    pc = np.zeros(1 << n, dtype=np.int16)
    for v in range(n): pc += ((S >> v) & 1).astype(np.int16)
    mask = pc >= 2
    worst = int((cnt[mask] - pc[mask] + 2).max())
    return worst <= 0, worst

def connected(E, n):
    adj = {v: set() for v in range(n)}
    for e in E:
        for v in e: adj[v] |= set(e) - {v}
    seen = {0}; st = [0]
    while st:
        v = st.pop()
        for w in adj[v]:
            if w not in seen: seen.add(w); st.append(w)
    return len(seen) == n

def has_cover(E, k, chosen=frozenset()):
    for e in E:
        if not (set(e) & chosen): break
    else: return chosen
    if k == 0: return None
    for v in e:
        r = has_cover(E, k - 1, chosen | {v})
        if r is not None: return r
    return None

def tau(E):
    k = 0
    while True:
        r = has_cover(E, k)
        if r is not None: return k, sorted(r)
        k += 1

def wl_hist(E, n, rounds=8):
    """1-WL on the incidence graph; returns the final colour histogram (canonical, label-free)."""
    col = {('v', v): 'v' for v in range(n)}; col.update({('e', i): 'e' for i in range(len(E))})
    nb = {('v', v): [] for v in range(n)}; nb.update({('e', i): [] for i in range(len(E))})
    for i, e in enumerate(E):
        for v in e: nb[('e', i)].append(('v', v)); nb[('v', v)].append(('e', i))
    for _ in range(rounds):
        sig = {x: (col[x], tuple(sorted(col[y] for y in nb[x]))) for x in col}
        names = {s: str(j) for j, s in enumerate(sorted(set(sig.values()), key=repr))}
        col = {x: names[sig[x]] for x in col}
        # canonical names depend only on the multiset structure via sorted signatures -> recompute histogram each round
    return tuple(sorted(Counter(sig.values()).items(), key=repr))

def deg(E, n):
    d = [0] * n
    for e in E:
        for v in e: d[v] += 1
    return d

def q8_edges():
    a, b, c = 0, 1, [None, 2, 3, 4, 5, 6, 7]
    return [(a, c[1], c[2]), (a, c[3], c[4]), (a, c[5], c[6]), (b, c[2], c[3]), (b, c[4], c[5]), (b, c[6], c[1])]

def q8_embeddings(E):
    """all (a,b,c1..c6) with the six Q8 edges in E; returned as explicit maps Q8-vertex -> X-vertex."""
    Es = set(frozenset(e) for e in E); inc = {}
    for e in E:
        for v in e: inc.setdefault(v, []).append(e)
    out = []
    Q = q8_edges()
    for a in inc:
        for ea in itertools.combinations(inc[a], 3):
            pa = [tuple(x for x in e if x != a) for e in ea]
            C = set(pa[0]) | set(pa[1]) | set(pa[2])
            if len(C) != 6: continue
            for b in inc:
                if b == a or b in C: continue
                for eb in itertools.combinations(inc[b], 3):
                    pb = [tuple(x for x in e if x != b) for e in eb]
                    if set(pb[0]) | set(pb[1]) | set(pb[2]) != C: continue
                    # build c1..c6: c1,c2 = pa[0]; walk the hexagon
                    for c1, c2 in (pa[0], pa[0][::-1]):
                        def mate_b(x):
                            for p in pb:
                                if x in p: return p[0] if p[1] == x else p[1]
                        def mate_a(x):
                            for p in pa:
                                if x in p: return p[0] if p[1] == x else p[1]
                        c3 = mate_b(c2); c4 = mate_a(c3); c5 = mate_b(c4); c6 = mate_a(c5)
                        mp = {0: a, 1: b, 2: c1, 3: c2, 4: c3, 5: c4, 6: c5, 7: c6}
                        if len(set(mp.values())) == 8 and all(frozenset(mp[x] for x in q) in Es for q in Q):
                            out.append(mp)
    return out

if __name__ == '__main__':
    cert = [parse(l) for l in open('six_from_certificate.txt')]
    stored = [parse(l) for l in open('/home/user/Erdos-757/experiments/prover/L023/cell_25_23_11_D4.txt') if l.startswith('FOUND:')]
    js = json.load(open('/home/user/Erdos-757/experiments/prover/L023/six_classes_25_23_11_D4.json'))['classes']
    js = [[tuple(sorted(e)) for e in X] for X in js]
    key = lambda L: sorted(tuple(sorted(X)) for X in L)
    print('certificate text == stored list:', key(cert) == key(stored), '; == json:', key(cert) == key(js), '; counts', len(cert), len(stored), len(js))
    res = []
    for i, E in enumerate(cert):
        n = 25
        d = deg(E, n)
        ok_p3, worst = p3_bruteforce(E, n)
        t, cov = tau(E)
        t10 = has_cover(E, 10)
        tauminus = [tau([e for e in E if v not in e])[0] for v in range(n)]
        emb = q8_embeddings(E)
        info = dict(i=i, m=len(E), distinct=len(set(E)) == len(E), allin=all(0 <= v < n for e in E for v in e) and all(len(set(e)) == 3 for e in E),
                    used_vertices=len(set(v for e in E for v in e)), linear=is_linear(E), F7=has_F7(E), P3=ok_p3, P3_max_excess=worst,
                    connected=connected(E, n), tau=t, cover=cov, cover10=t10, Delta=max(d), degseq=dict(sorted(Counter(d).items())),
                    deg4=[v for v in range(n) if d[v] == 4], tau_minus_v=sorted(set(tauminus)),
                    q8_embeddings=len(emb), q8_example=emb[0] if emb else None)
        res.append(info); print(json.dumps(info))
    H = [wl_hist(E, 25) for E in cert]
    print('WL histograms pairwise distinct:', len(set(H)) == 6, [sum(1 for h in H if h == H[i]) for i in range(6)])
    Q = q8_edges()
    print('Q8: linear', is_linear(Q), 'F7', has_F7(Q), 'P3', p3_bruteforce(Q, 8), 'connected', connected(Q, 8), 'tau', tau(Q), 'deg', deg(Q, 8))
    # Q8 embeddings as AG(2,3): points (x,y) in Z3^2; a=(0,0), b=(1,0); third point of ab is (2,0)
    pts = [(x, y) for x in range(3) for y in range(3)]
    lines = set()
    for p in pts:
        for dvec in ((1, 0), (0, 1), (1, 1), (1, 2)):
            lines.add(frozenset(((p[0] + k * dvec[0]) % 3, (p[1] + k * dvec[1]) % 3) for k in range(3)))
    A, Bp, P = (0, 0), (1, 0), (2, 0)
    L6 = [l for l in lines if (A in l or Bp in l) and P not in l]
    idx = {p: j for j, p in enumerate([q for q in pts if q != P])}
    G = [tuple(sorted(idx[q] for q in l)) for l in L6]
    print('AG(2,3): 12 lines', len(lines) == 12, '; six lines through a or b avoiding p:', len(L6), '; contains Q8 (8 vertices, 6 edges):', len(q8_embeddings(G)) > 0)
