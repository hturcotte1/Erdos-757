"""L026 C9: Lemma 9 on stored data.  For every connected graph of the given lists, compute DEF with an
optimal L*-family (ownlib.DEF, exact branch and bound) and check: if DEF > 0 then the family is a single
member covering the graph, or has an odd number p in {3,...,11} of members covering all vertices, with
exactly (p-1)/2 edges outside the members, each meeting three distinct members.
Usage: python3 lemma9_check.py <list files ...>"""
import sys, time
sys.path.insert(0, '/home/user/Erdos-757/experiments/prover/L026')
import ownlib as L
from hub_analysis import lemma9_ok, pieces
def load(f):
    out = L.read_found(f)
    if out: return out
    good = [l for l in open(f) if l.split() and l.split()[0].isdigit()]
    if not good: return []
    return L.read_flat(f)
tot = dict(graphs=0, defpos=0, single=0, multi=0, fail=0)
for f in sys.argv[1:]:
    t0 = time.time(); c = dict(graphs=0, defpos=0, single=0, multi=0, fail=0)
    for E in load(f):
        n = L.nv(E)
        if len(L.components(n, E)) != 1: continue
        c['graphs'] += 1
        D, fam = L.DEF(n, E, pieces, want=True)
        if D > 0:
            c['defpos'] += 1
            if len(fam) == 1: c['single'] += 1
            else: c['multi'] += 1
            if not lemma9_ok(n, E, fam, D): c['fail'] += 1; print('FAIL', f, E, fam, D)
    print(f.split('/')[-1], c, '[%ds]' % (time.time() - t0), flush=True)
    for k in tot: tot[k] += c[k]
print('TOTAL', tot)
