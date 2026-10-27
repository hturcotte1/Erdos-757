#!/usr/bin/env python3
"""L026 check C3: random tests of the general (minimality-free) inequalities behind Lemmas 3-6 of L026.
 (B') bridge identity: H in C_3, edge e with H \\ e = H1 u H2 (both nonempty, e meets both); if
      tau(H) = tau(H1) + tau(H2) then P(H) >= P(H1) + P(H2).
 (C') pendant block: same with e = {p,q,c}, c in H2, p,q in H1, tau(H) = tau(H1) + tau(H2) + 1, c in no
      minimum transversal of H2 and no minimum transversal of H1 meets {p,q}; then
      A(H) = A(H#) + A(H2 - c) + 35 d_{H2}(c) and P(H) >= P(H#) + P(H2 - c), H# = H1 + w + {p,q,w}.
 (D)  Lemma 5: DEF(G) <= 16 for connected G, DEF(G) <= 10 if moreover n(G) >= 11.
 (E)  Lemma 6: if c is in no minimum transversal of G then P(G) >= P(G - c) + 27.
Random graphs: random linear 3-graphs with Delta <= 3 grown edge by edge inside C_3 (own membership test).
Usage: python3 check_lemmas.py <seed> <trials> <nmax>"""
import sys, random, itertools
sys.path.insert(0, '/home/user/Erdos-757/experiments/prover/L026')
import ownlib as L

pieces = L.load_pieces()

def random_connected(rng, n, target_m):
    """grow a connected member of C_3 on vertices 0..n-1 (all vertices covered), or None."""
    E = []; d = [0] * n
    used = [0]
    pairs = set()
    def ok(e):
        if any(d[x] >= 3 for x in e): return False
        for p in itertools.combinations(sorted(e), 2):
            if p in pairs: return False
        return True
    def add(e):
        E.append(tuple(e))
        for x in e: d[x] += 1
        for p in itertools.combinations(sorted(e), 2): pairs.add(p)
    covered = {0}
    tries = 0
    while len(covered) < n and tries < 2000:
        tries += 1
        u = rng.choice(sorted(covered))
        new = [x for x in range(n) if x not in covered]
        k = rng.choice([1, 2]) if len(new) >= 2 else 1
        others = rng.sample(new, k)
        rest = [x for x in covered if x != u]
        if k == 1:
            if not rest: continue
            others.append(rng.choice(rest))
        e = tuple(sorted([u] + others))
        if len(set(e)) < 3 or not ok(e): continue
        add(e)
        if not L.in_C3(n, E):
            E.pop()
            for x in e: d[x] -= 1
            for p in itertools.combinations(sorted(e), 2): pairs.discard(p)
            continue
        covered |= set(e)
    if len(covered) < n: return None
    tries = 0
    while len(E) < target_m and tries < 300:
        tries += 1
        e = tuple(sorted(rng.sample(range(n), 3)))
        if not ok(e): continue
        add(e)
        if not L.in_C3(n, E):
            E.pop()
            for x in e: d[x] -= 1
            for p in itertools.combinations(sorted(e), 2): pairs.discard(p)
    return E

def mts(E):
    return L.all_min_transversals(E) if E else [0]

def main():
    seed, trials, nmax = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    rng = random.Random(seed)
    st = dict(D_tested=0, D_fail=0, E_tested=0, E_fail=0, B_tested=0, B_fail=0, C_tested=0, C_fail=0, C_Aid_fail=0)
    for tr in range(trials):
        n1 = rng.randint(3, nmax); n2 = rng.randint(1, max(1, nmax - n1))
        if n2 == 2: n2 = 1
        m1 = rng.randint((n1 - 1) // 2, n1 - 2) if n1 >= 3 else 0
        m2 = rng.randint((n2 - 1) // 2, n2 - 2) if n2 >= 3 else 0
        G1 = random_connected(rng, n1, m1)
        G2 = random_connected(rng, n2, m2) if n2 >= 3 else []
        if G1 is None or G2 is None: continue
        # (D) and (E) on G1
        P1 = L.P_val(n1, G1, pieces)
        D1 = L.DEF(n1, G1, pieces)
        st['D_tested'] += 1
        if D1 > 16 or (n1 >= 11 and D1 > 10): st['D_fail'] += 1; print('D FAIL', n1, G1, D1, flush=True)
        T1 = mts(G1); cov1 = 0
        for t in T1: cov1 |= t
        for c in range(n1):
            if not (cov1 >> c) & 1:
                S = [x for x in range(n1) if x != c]
                Pm = L.P_of_vertexset(G1, S, pieces)
                st['E_tested'] += 1
                if P1 < Pm + 27: st['E_fail'] += 1; print('E FAIL', n1, G1, c, P1, Pm, flush=True)
        # bridge: e = {p,q,c} with p,q in G1 (degree <= 2, not adjacent), c in G2 (degree <= 2)
        d1 = L.degs(n1, G1); d2 = L.degs(n2, G2) if G2 else [0] * n2
        adj1 = set()
        for e in G1:
            for pr in itertools.combinations(sorted(e), 2): adj1.add(pr)
        cand = [(p, q) for p, q in itertools.combinations(range(n1), 2) if d1[p] <= 2 and d1[q] <= 2 and (p, q) not in adj1]
        if not cand: continue
        T2a = mts(G2) if G2 else [0]; cov2a = 0
        for t in T2a: cov2a |= t
        if rng.random() < 0.6:
            # bias towards the pendant-block situation: p, q outside every minimum transversal of G1,
            # c outside every minimum transversal of G2
            c1 = [(p, q) for (p, q) in cand if not (cov1 >> p) & 1 and not (cov1 >> q) & 1]
            if c1: cand = c1
            cs = [c for c in range(n2) if d2[c] <= 2 and not (cov2a >> c) & 1]
        else:
            cs = []
        if not cs: cs = [c for c in range(n2) if d2[c] <= 2]
        if not cs: continue
        p, q = rng.choice(cand)
        c = rng.choice(cs)
        nH = n1 + n2
        EH = list(G1) + [tuple(x + n1 for x in e) for e in G2] + [(p, q, c + n1)]
        if not L.in_C3(nH, EH): continue
        t1 = L.tau(G1) if G1 else 0; t2 = L.tau(G2) if G2 else 0; tH = L.tau(EH)
        PH = L.P_val(nH, EH, pieces)
        P2 = L.P_val(n2, G2, pieces) if G2 else 27 * n2
        if tH == t1 + t2:
            st['B_tested'] += 1
            if PH < P1 + P2: st['B_fail'] += 1; print('B FAIL', G1, G2, (p, q, c), flush=True)
        else:
            T2 = mts(G2); cov2 = 0
            for t in T2: cov2 |= t
            cNC = not (cov2 >> c) & 1
            pqNC = not any(t & ((1 << p) | (1 << q)) for t in T1)
            if cNC and pqNC and (n2 > 1):
                st['C_tested'] += 1
                Es = list(G1) + [(p, q, n1)]
                Psharp = L.P_val(n1 + 1, Es, pieces)
                tS = L.tau(Es)
                Asharp = L.A_val(n1 + 1, len(Es), tS)
                S2 = [x for x in range(n2) if x != c]
                G2c = L.induced(G2, S2)
                A2c = L.A_val(len(S2), len(G2c), L.tau(G2c) if G2c else 0)
                P2c = L.P_val(len(S2), G2c, pieces) if G2c else 27 * len(S2)
                AH = L.A_val(nH, len(EH), tH)
                if AH != Asharp + A2c + 35 * d2[c]: st['C_Aid_fail'] += 1; print('C A-identity FAIL', flush=True)
                if PH < Psharp + P2c: st['C_fail'] += 1; print('C FAIL', G1, G2, (p, q, c), PH, Psharp, P2c, flush=True)
    print(st, flush=True)

if __name__ == '__main__':
    main()
