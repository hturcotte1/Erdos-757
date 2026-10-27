#!/usr/bin/env python3
"""Independent check of L020 Theorem 1 (the graph K_29), written for the panel synthesis.
Does not import e757, judge, or any L0xx code.
Checks: n, m, degrees, connectivity, linearity, F7-freeness (complete for Delta<=3),
(P3) e(S) <= |S|-2 for all |S|>=2 via a max-closure / Hall test per vertex pair,
tau exactly (branch and bound), slack 3n+2m-11tau.
Optionally (--triples): enumerates all minimum transversals and tests every triple of
pairwise disjoint 2-sets none inside an edge: covered by some minimum transversal, or
K+v(P1,P2,P3) not in C (Theorem 1(ii)).
"""
import sys, itertools

K29 = [(0,1,14),(1,2,15),(2,16,17),(3,4,13),(3,10,18),(4,11,18),(5,8,9),(5,15,16),(6,7,16),
       (6,8,17),(7,9,17),(10,11,19),(12,14,15),(12,18,19),(13,14,19),(20,21,22),(21,25,26),
       (22,24,27),(23,24,26),(23,25,27),(28,1,12),(28,21,23),(28,0,20)]

def basic(E, n):
    deg = [0]*n
    for e in E:
        for x in e: deg[x] += 1
    # connectivity
    adj = [set() for _ in range(n)]
    for e in E:
        for x in e:
            adj[x] |= set(e) - {x}
    seen = {0}; st = [0]
    while st:
        u = st.pop()
        for w in adj[u]:
            if w not in seen: seen.add(w); st.append(w)
    return deg, len(seen) == n

def linear(E):
    for e, f in itertools.combinations(E, 2):
        if len(set(e) & set(f)) >= 2: return False
    return True

def f7_free(E, n):
    # F7 = centre with 3 edges {c}+P1,{c}+P2,{c}+P3 plus two disjoint edges each meeting every Pi once.
    # Any copy has its centre at a vertex of degree >= 3; we enumerate all 3-subsets of edges at each vertex.
    Es = [frozenset(e) for e in E]
    inc = [[i for i, e in enumerate(Es) if x in e] for x in range(n)]
    for c in range(n):
        for trip in itertools.combinations(inc[c], 3):
            P = [Es[i] - {c} for i in trip]
            U = P[0] | P[1] | P[2]
            trans = [e for e in Es if e <= U and all(len(e & p) == 1 for p in P)]
            for e, f in itertools.combinations(trans, 2):
                if not (e & f): return False
    return True

def p3_ok(E, n):
    # For each pair {x,y}: the edges must have a system of distinct representatives in V\{x,y}
    # (equivalent to e(S) <= |S|-2 for all S with |S|>=2). Simple augmenting-path matching.
    for x, y in itertools.combinations(range(n), 2):
        owner = {}
        def aug(i, vis):
            for u in E[i]:
                if u == x or u == y or u in vis: continue
                vis.add(u)
                if u not in owner or aug(owner[u], vis):
                    owner[u] = i; return True
            return False
        for i in range(len(E)):
            if not aug(i, set()): return False
    return True

def tau(E, n):
    best = [len(E)]
    Es = [frozenset(e) for e in E]
    def rec(chosen, k):
        if k >= best[0]: return
        unc = [e for e in Es if not (e & chosen)]
        if not unc:
            best[0] = k; return
        # lower bound: greedy disjoint uncovered edges
        used = set(); lb = 0
        for e in unc:
            if not (e & used): used |= e; lb += 1
        if k + lb >= best[0]: return
        e = unc[0]
        for u in sorted(e):
            rec(chosen | {u}, k + 1)
    rec(frozenset(), 0)
    return best[0]

def all_min_transversals(E, n, t):
    Es = [frozenset(e) for e in E]
    out = set()
    def rec(chosen, k, banned):
        unc = [e for e in Es if not (e & chosen)]
        if not unc:
            out.add(chosen); return
        if k == t: return
        used = set(); lb = 0
        for e in unc:
            if not (e & used): used |= e; lb += 1
        if k + lb > t: return
        e = min(unc, key=lambda f: len(f - banned))
        cand = [u for u in sorted(e) if u not in banned]
        newb = set(banned)
        for u in cand:
            rec(chosen | {u}, k + 1, frozenset(newb))
            newb.add(u)
    rec(frozenset(), 0, frozenset())
    return out

def in_C_plus(E, n, P):
    w = n
    E2 = list(E) + [tuple(sorted((w,) + tuple(p))) for p in P]
    if not linear(E2): return False
    if not f7_free(E2, n + 1): return False
    return p3_ok(E2, n + 1)

def main():
    E = K29; n = 29
    deg, conn = basic(E, n)
    print("n", n, "m", len(E), "maxdeg", max(deg), "mindeg", min(deg), "connected", conn,
          "deg2", deg.count(2), "deg3", deg.count(3))
    print("linear", linear(E))
    print("F7-free", f7_free(E, n))
    print("P3", p3_ok(E, n))
    t = tau(E, n)
    print("tau", t, "slack", 3*n + 2*len(E) - 11*t)
    if "--triples" in sys.argv:
        T = all_min_transversals(E, n, t)
        print("min transversals", len(T))
        T = list(T)
        Es = [frozenset(e) for e in E]
        pairs = [p for p in itertools.combinations(range(n), 2)
                 if not any(set(p) <= e for e in Es)]
        mask = {}
        for p in pairs:
            b = 0
            for i, tr in enumerate(T):
                if p[0] in tr or p[1] in tr: b |= (1 << i)
            mask[p] = b
        print("pairs not inside an edge", len(pairs))
        unc = 0; adm_unc = 0; checked = 0
        for i in range(len(pairs)):
            p = pairs[i]; mp = mask[p]
            for j in range(i + 1, len(pairs)):
                q = pairs[j]
                if set(p) & set(q): continue
                mpq = mp & mask[q]
                for k in range(j + 1, len(pairs)):
                    r = pairs[k]
                    if set(r) & set(p) or set(r) & set(q): continue
                    checked += 1
                    if mpq & mask[r]: continue
                    unc += 1
                    if in_C_plus(E, n, [p, q, r]): adm_unc += 1
        print("triples checked", checked, "uncovered", unc, "uncovered and admissible", adm_unc)

if __name__ == "__main__":
    main()
