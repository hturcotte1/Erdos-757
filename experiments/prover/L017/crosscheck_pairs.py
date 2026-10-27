"""L017, cross-check of hyp.all_min_transversals (used by C2 and C5) against direct transversal numbers:
for every graph of the given lists (at most LIMIT graphs per list) and every pair {x, y}: {x,y} lies in an enumerated
minimum transversal  <=>  tau(F - x - y) = tau(F) - 2 (Fact 0.4), with tau(F - x - y) computed by hyp.tau_masks.
Also every enumerated set is checked to be a transversal of size tau, and the vertex version is checked.
Usage: python3 crosscheck_pairs.py LIMIT cellfile [cellfile ...]"""
import sys, os, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hyp import read_cell, masks, all_min_transversals, tau_masks

def main(limit, files):
    bad = 0; npairs = 0; ngraphs = 0
    for f in files:
        n = int(os.path.basename(f).split('_')[1])
        for es in read_cell(f)[:limit]:
            em = masks(es); Ts, t = all_min_transversals(em); ngraphs += 1
            assert t == tau_masks(em)
            for T in Ts:
                assert bin(T).count('1') == t and all(e & T for e in em)
            assert len(set(Ts)) == len(Ts)
            cov = set(); inT = 0
            for T in Ts:
                inT |= T
                vs = [x for x in range(n) if T >> x & 1]
                for a, b in itertools.combinations(vs, 2): cov.add((a, b))
            for x in range(n):
                X = 1 << x
                direct = tau_masks([e for e in em if not e & X]) == t - 1
                if direct != bool(inT >> x & 1): bad += 1
            for x, y in itertools.combinations(range(n), 2):
                X = (1 << x) | (1 << y)
                direct = tau_masks([e for e in em if not e & X]) == t - 2
                npairs += 1
                if direct != ((x, y) in cov): bad += 1
    print('graphs %d, pairs %d, mismatches %d' % (ngraphs, npairs, bad))

if __name__ == '__main__':
    main(int(sys.argv[1]), sys.argv[2:])
