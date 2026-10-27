"""L025 lemma tests (own code; hyp25.py only; exact integer/bitmask arithmetic).

Every check below is an identity or an implication proved in results/proofs/L025-e1hub-lemma-i11-form.md,
run on stored data.  The statements are about members of C; the checks run on every stored class with
max degree <= 3 of the given lists (all triples / pairs, or a stated deterministic sample).

Usage: python3 lemmas25.py <list-spec> ...   where list-spec is
   near             the ten stored near-tight lists (slack <= 1), transversal-richness inputs
   slack2           the eight stored slack-2 lists
   file:<path>      a cell file in 'FOUND:' format (L012-L016 cells) or 'n m t e...' format
Options: --hubsample K (triples per class for the hub/fold test, default 60)

Checks (names as in the certificate):
  L1  hub lemma: G(+)(a,b,c) in C iff {a,b,c} not an edge; tau = tau+1 if some minimum transversal contains two of a,b,c, else tau+2
  L2  fold lemma: G(+)o(a,b|c) in C when a,b share no edge; tau = tau if some min transversal contains c and meets {a,b}, else tau+1
  L3  pendant gadget: (G-c)+{w,a,b} in C, tau = tau(G), s = s(G)+2-2d(c)   [a,b share no edge, c co-transversal, {a,c},{b,c} NC]
  L4  deletion lemma for pairwise NC triples: tau(G-a-b) = tau-1, tau(G-a-b-c) in {tau-2, tau-1}, and if tau-1 then s(G) >= 2|d(a,b,c)|-2
  L5  pair lemma (Prop. 6 of L020) for NC pairs: tau(G-x-y) = tau-1 and s(G-x-y) = s+5-2|d(x,y)| when x is co-transversal
  L6  identification lemma: NC pair {x,y}, no common edge, no common neighbour, one of them co-transversal: tau(G_{x=y}) = tau, s-3
  L7  move lemma: x of degree 1 with edge {x,x1,x2}, x co-transversal, {x,y},{x,z} NC: tau((G-x)+{x1,y,z}) = tau
  L8  avoided-triple lemma: Y three avoided vertices: tau(G+Y) = tau+1  (G+Y = G plus the edge Y)
  L9  necessary conditions (rules R1, R2, R3, fold) on every b-configuration, with the slack of the graph: they must hold whenever
      I11 holds for the graphs used (true for all stored data, n <= 27)
"""
import sys, time, random
from itertools import combinations
from hyp25 import *

NEAR = [(3,1,1),(10,7,4),(14,12,6),(17,13,7),(8,5,3),(12,10,5),(15,11,6),(19,16,8),(22,17,9),(26,22,11)]
SLACK2 = [(6,3,2),(9,4,3),(10,8,4),(13,9,5),(16,10,6),(17,14,7),(20,15,8),(23,16,9)]

def read_found(path):
    out = []
    for line in open(path):
        if line.startswith('FOUND'):
            parts = line.split(':', 1)[1].strip().split()
            E = [tuple(sorted(map(int, p.strip('()').split(',')))) for p in parts]
            out.append(E)
        elif line.strip() and line[0].isdigit():
            n, m, t, E = parse_line(line)
            out.append(E)
    return out

def graphs(specs):
    for sp in specs:
        if sp == 'near':
            for c in NEAR:
                for (n0, m0, t0, E) in load_cell(*c):
                    yield str(c), Hyp(E, range(n0))
        elif sp == 'slack2':
            for c in SLACK2:
                for (n0, m0, t0, E) in load_cell(*c):
                    yield str(c), Hyp(E, range(n0))
        elif sp.startswith('file:'):
            p = sp[5:]
            for E in read_found(p):
                n0 = 1 + max(max(e) for e in E)
                yield p.split('/')[-1], Hyp(E, range(n0))

def mt_hit(h, bits_all, bits_any_list):
    """is there a min transversal containing all of bits_all and meeting every mask in bits_any_list"""
    for T in h.min_transversals():
        if T & bits_all != bits_all:
            continue
        if all(T & b for b in bits_any_list):
            return True
    return False

def bm(h, X):
    b = 0
    for v in X:
        b |= h.bit(v)
    return b

def dpart(h, X):
    X = set(X)
    return sum(1 for e in h.E if set(e) & X)

def main():
    args = sys.argv[1:]
    K = 60
    if '--hubsample' in args:
        i = args.index('--hubsample'); K = int(args[i + 1]); del args[i:i + 2]
    rnd = random.Random(20261027)
    st = {k: 0 for k in ['classes', 'L1', 'L2', 'L3', 'L4', 'L4_drop1', 'L5', 'L6', 'L6_inC', 'L7', 'L7_inC', 'L8', 'L8_inC', 'L9', 'bconf']}
    bad = []
    t0 = time.time()
    for cell, h in graphs(args):
        if h.maxdeg() > 3:
            continue
        st['classes'] += 1
        tau = h.tau(); s = h.slack(); MT = h.min_transversals()
        E = h.E; V = h.V; edges = set(frozenset(e) for e in E)
        nb = neighbours(E, V)
        cov = 0
        for T in MT:
            cov |= T
        cot = lambda v: bool(cov & h.bit(v))          # vertex co-transversal
        cp = h.co_pairs()
        low = [v for v in V if h.deg[v] <= 2]
        # ---- L1 hub and L2 fold on a deterministic sample of triples of low-degree vertices
        trs = list(combinations(low, 3)); rnd.shuffle(trs)
        for (a, b, c) in trs[:K]:
            E2, V2 = oplus(E, V, a, b, c); h2 = Hyp(E2, V2)
            two = any(bin(T & bm(h, (a, b, c))).count('1') >= 2 for T in MT)
            ok = (h2.in_C() == (frozenset((a, b, c)) not in edges)) and h2.tau() == tau + (1 if two else 2)
            st['L1'] += 1
            if not ok: bad.append(('L1', cell, E, (a, b, c)))
            for (p, q, r) in ((a, b, c), (a, c, b), (b, c, a)):
                if frozenset((p, q)) in h.sig:
                    continue
                N = max(V) + 1
                E3 = E + [tuple(sorted((N, p, q))), tuple(sorted((N, N + 1, r)))]
                h3 = Hyp(E3, V + [N, N + 1])
                pred = tau + (0 if mt_hit(h, h.bit(r), [bm(h, (p, q))]) else 1)
                st['L2'] += 1
                if not (h3.in_C() and h3.tau() == pred): bad.append(('L2', cell, E, (p, q, r)))
        # ---- NC pairs (any degrees) and the pair / identification lemmas
        ncp = [frozenset(p) for p in combinations(V, 2) if frozenset(p) not in cp]
        ncs = set(ncp)
        for p in ncp:
            x, y = tuple(p)
            if cot(x) or cot(y):
                E2, V2 = delete(E, V, {x, y}); h2 = Hyp(E2, V2)
                st['L5'] += 1
                if not (h2.tau() == tau - 1 and h2.slack() == s + 5 - 2 * dpart(h, (x, y))):
                    bad.append(('L5', cell, E, (x, y)))
                if p not in h.sig and not (nb[x] & nb[y]):
                    E3, V3 = identify(E, V, x, y); h3 = Hyp(E3, V3)
                    st['L6'] += 1
                    if not (h3.tau() == tau and h3.slack() == s - 3): bad.append(('L6', cell, E, (x, y)))
                    if h3.in_C(): st['L6_inC'] += 1
        # ---- configurations (r; p, q) with {p,r},{q,r} NC
        for r in V:
            part = [u for u in V if u != r and frozenset((u, r)) in ncs]
            for p, q in combinations(part, 2):
                if frozenset((p, q)) not in h.sig and cot(r):
                    # L3 pendant gadget
                    N = max(V) + 1
                    E4, V4 = delete(E, V, {r}); E4 = E4 + [tuple(sorted((N, p, q)))]
                    h4 = Hyp(E4, V4 + [N])
                    st['L3'] += 1
                    if not (h4.in_C() and h4.tau() == tau and h4.slack() == s + 2 - 2 * h.deg[r]):
                        bad.append(('L3', cell, E, (r, p, q)))
                # L7 move: r of degree 1 co-transversal; p,q partners
                if h.deg[r] == 1 and cot(r):
                    er = [e for e in E if r in e][0]
                    for r1 in er:
                        if r1 == r or r1 in (p, q):
                            continue
                        E5, V5 = delete(E, V, {r}); E5 = E5 + [tuple(sorted((r1, p, q)))]
                        h5 = Hyp(E5, V5)
                        st['L7'] += 1
                        if h5.tau() != tau: bad.append(('L7', cell, E, (r, r1, p, q)))
                        if h5.in_C(): st['L7_inC'] += 1
        # ---- L4 / L9 on b-configurations (pairwise NC triples of low-degree vertices, not an edge)
        for t in combinations(low, 3):
            if not all(frozenset(pq) in ncs for pq in combinations(t, 2)):
                continue
            if frozenset(t) in edges:
                continue
            st['bconf'] += 1
            a, b, c = t
            for (p, q, r) in ((a, b, c), (a, c, b), (b, c, a)):
                if not cot(p):
                    continue
                Ea, Va = delete(E, V, {p, q}); ha = Hyp(Ea, Va)
                Eb, Vb = delete(E, V, {p, q, r}); hb = Hyp(Eb, Vb)
                dA = dpart(h, (a, b, c))
                st['L4'] += 1
                ok = ha.tau() == tau - 1 and hb.tau() in (tau - 2, tau - 1)
                if hb.tau() == tau - 1:
                    st['L4_drop1'] += 1
                    ok = ok and s >= 2 * dA - 2
                if not ok: bad.append(('L4', cell, E, (p, q, r)))
            # L9: rules with the slack of h
            st['L9'] += 1
            for (p, q, r) in ((a, b, c), (a, c, b), (b, c, a)):
                if frozenset((p, q)) not in h.sig:
                    if cot(r) and s < 2 * h.deg[r] - 2: bad.append(('L9-R1', cell, E, t))
                    if s < 1: bad.append(('L9-fold', cell, E, t))
                if (cot(p) or cot(q)) and 2 * dpart(h, (p, q)) > s + 5: bad.append(('L9-R2', cell, E, t))
                # R3: r isolated in G-p-q forces s >= 2|d(a,b,c)| - 2  (needs a vertex of the triple co-transversal)
                if (cot(a) or cot(b) or cot(c)) and all((p in e or q in e) for e in E if r in e):
                    if s < 2 * dpart(h, (a, b, c)) - 2: bad.append(('L9-R3', cell, E, t))
        # ---- L8 avoided triples
        av = [v for v in V if not cot(v)]
        for Y in combinations(av, 3):
            E6 = E + [tuple(sorted(Y))]
            h6 = Hyp(E6, V)
            st['L8'] += 1
            if h6.tau() != tau + 1: bad.append(('L8', cell, E, Y))
            if all(frozenset(pq) not in h.sig for pq in combinations(Y, 2)) and h6.in_C():
                st['L8_inC'] += 1
                if 3 * h.n + 2 * (h.m + 1) - 11 * (tau + 1) < 0:
                    bad.append(('L8-I11', cell, E, Y))
    print(' '.join(args), st, 'failures', len(bad), 'time %.1fs' % (time.time() - t0), flush=True)
    for b in bad[:10]:
        print('  FAIL', b)

if __name__ == '__main__':
    main()
