"""Referee #1 (L021): randomized tests of the set identities behind 0.3, 0.5, 4.1 and 5.1 on graphs of the
refereed cell lists (random L*-families computed from own induced-copy search)."""
import os, sys, json, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rcore import *
HERE = os.path.dirname(os.path.abspath(__file__))
src = json.load(open('/home/user/Erdos-757/experiments/prover/L021/closure_results.json'))['pieces']
pcs = [(p['name'], nv(p['edges']), [tuple(e) for e in p['edges']], p['W']) for p in src]
rng = random.Random(11)
def Estar(edges, fam):
    allU = frozenset().union(*fam) if fam else frozenset()
    return set(i for i, e in enumerate(edges) if set(e) & allU and not any(set(e) <= U for U in fam))
def ind(edges, U):
    return [e for e in edges if set(e) <= U]
def copies_in(n, edges, keep=None):
    out = []
    for (nm, pn, pe, W) in pcs:
        for U in induced_copies(n, edges, pn, pe):
            out.append(U)
    return out
def rand_family(cs, forbid=frozenset()):
    cs = [c for c in cs if not c & forbid]; rng.shuffle(cs); fam = []; used = set()
    for c in cs:
        if not c & used and rng.random() < 0.6: fam.append(c); used |= c
    return fam
files = ['tar/cells/cell_14_8_5_D3.txt', 'tar/cells/cell_16_10_6_D3.txt', 'tar13/cells/cell_22_13_8_D3.txt',
         'tar13/cells/cell_23_16_9_D3.txt', 'tar/cells/cell_12_10_5_D3.txt', 'tar/cells/cell_17_13_7_D3.txt']
nt = 0; bad = 0
for f in files:
    gs = parse_cell(os.path.join(HERE, f)); rng.shuffle(gs)
    for g in gs[:int(sys.argv[1]) if len(sys.argv) > 1 else 15]:
        n = nv(g); cs = copies_in(n, g)
        for _ in range(int(sys.argv[2]) if len(sys.argv) > 2 else 20):
            X = rand_family(cs)
            VX = frozenset().union(*X) if X else frozenset()
            # 0.3 edge partition
            Rv = frozenset(range(n)) - VX
            ok = len(g) == len(ind(g, Rv)) + sum(len(ind(g, U)) for U in X) + len(Estar(g, X))
            # 0.5: Y family in R (copies inside V(R) are induced copies in R)
            Y = rand_family([c for c in cs if c <= Rv])
            R_edges = ind(g, Rv)
            lhs = Estar(g, X + Y)
            rhsX = Estar(g, X)
            EY = Estar(R_edges, Y)   # indices relative to R_edges
            EY_glob = set(g.index(R_edges[i]) for i in EY)
            ok = ok and lhs == (rhsX | EY_glob) and not (rhsX & EY_glob)
            # 4.1: v not in any member of X'; E*_H(X') = E*_{H-v}(X') u K
            v = rng.randrange(n)
            Xv = rand_family([c for c in cs if v not in c])
            Hv = [e for e in g if v not in e]
            Ev = set(g.index(Hv[i]) for i in Estar(Hv, Xv))
            VXv = frozenset().union(*Xv) if Xv else frozenset()
            K = set(i for i, e in enumerate(g) if v in e and set(e) & VXv)
            ok = ok and Estar(g, Xv) == (Ev | K) and not (Ev & K)
            # 5.1: e an edge, X' family of H \ e (induced copies in H\e) with no member containing e
            ei = rng.randrange(len(g)); He = g[:ei] + g[ei+1:]
            csE = [c for c in copies_in(n, He) if not set(g[ei]) <= c] if rng.random() < 0.2 else [c for c in cs if not set(g[ei]) <= c]
            Xe = rand_family(csE)
            ok = ok and all(ind(g, U) == ind(He, U) or set(g[ei]) <= U for U in Xe)
            EHe = set(g.index(He[i]) for i in Estar(He, Xe))
            ok = ok and Estar(g, Xe) <= (EHe | {ei})
            nt += 1; bad += (not ok)
print('random identity tests:', nt, 'failures:', bad)
