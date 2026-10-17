"""Referee: compare the prover's 167 cell lists with the worker's final cell directory (and its n23/n24 directory):
same keys, same class counts, and identical sets of labelg canonical forms (computed by the referee)."""
import sys, os, re
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import myengine as E
def lists(D_):
    out = {}
    for fn in os.listdir(D_):
        mt = re.match(r'cell_(\d+)_(\d+)_(\d+)_D(\d+)\.txt$', fn)
        if not mt: continue
        key = tuple(map(int, mt.groups()))
        out[key] = [E.parse_edges(l) for l in open(os.path.join(D_, fn)) if l.startswith('FOUND:')]
    return out
P = lists(E.PROVER)
for W in sys.argv[1:]:
    Wl = lists(W)
    common = sorted(set(P) & set(Wl)); onlyP = sorted(set(P) - set(Wl)); onlyW = sorted(set(Wl) - set(P))
    cnt = sum(1 for k in common if len(P[k]) != len(Wl[k]))
    setdiff = 0
    for k in common:
        n, m, t, D = k
        if sorted(E.canon(n, m, P[k])) != sorted(E.canon(n, m, Wl[k])): setdiff += 1
    print('%s: prover %d cells, worker %d cells, common %d, only prover %d, only worker %d, count differences %d, canonical-set differences %d, classes prover/common %d worker/common %d'
          % (W, len(P), len(Wl), len(common), len(onlyP), len(onlyW), cnt, setdiff, sum(len(P[k]) for k in common), sum(len(Wl[k]) for k in common)))
