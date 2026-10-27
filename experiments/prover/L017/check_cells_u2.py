"""L017, illustrative check C2 of Theorem 2 (U) (Lemma U'', its two-vertex form and the pair lemma; proof in Step 2) on stored tight and slack-1 cells.
For every graph F of each cell list: compute tau(F) and ALL minimum transversals (exact, hyp.py); then
 (U'')  every vertex x with slack(F) < 3 + 2 d_F(x) lies in some minimum transversal;
 (U2)   every pair x != y with slack(F) < 2 |d(x,y)| - 5 lies in a common minimum transversal, where
        |d(x,y)| = number of edges of F meeting {x, y};
 (pair lemma, contrapositive of U2) every pair contained in NO minimum transversal has 2 |d(x,y)| <= slack(F) + 5.
These predictions rest on I11 for F - x and F - x - y (at most 25 vertices: L007-L016, verified-here); the check is
illustrative, not load-bearing.  Also reported: the pairs in no minimum transversal, by (d_F(x), d_F(y), share-an-edge).
Usage: python3 check_cells_u2.py <cellfile> [<cellfile> ...]"""
import sys, os, collections, itertools, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hyp import read_cell, masks, all_min_transversals, slack, degrees

def check_file(path):
    base = os.path.basename(path); n = int(base.split('_')[1]); mm = int(base.split('_')[2]); tt = int(base.split('_')[3])
    graphs = read_cell(path); t0 = time.time()
    viol_u = viol_u2 = 0; nopair_types = collections.Counter(); n_pairs_pred = 0; n_vert_pred = 0
    max_nT = 0; min_nT = None
    for es in graphs:
        assert len(es) == mm
        em = masks(es); Ts, t = all_min_transversals(em)
        assert t == tt, (path, t, tt)
        s = slack(n, mm, t); d = degrees(n, es)
        inT = 0; pairs = set()
        for T in Ts:
            inT |= T
            vs = [x for x in range(n) if T >> x & 1]
            for a, b in itertools.combinations(vs, 2): pairs.add((a, b))
        max_nT = max(max_nT, len(Ts)); min_nT = len(Ts) if min_nT is None else min(min_nT, len(Ts))
        share = set()
        for e in es:
            for a, b in itertools.combinations(sorted(e), 2): share.add((a, b))
        for x in range(n):
            if s < 3 + 2 * d[x]:
                n_vert_pred += 1
                if not inT >> x & 1: viol_u += 1
        for x, y in itertools.combinations(range(n), 2):
            sxy = 1 if (x, y) in share else 0
            dxy = d[x] + d[y] - sxy
            covered = (x, y) in pairs
            if s < 2 * dxy - 5:
                n_pairs_pred += 1
                if not covered: viol_u2 += 1
            if not covered:
                assert 2 * dxy <= s + 5, ('PAIR LEMMA VIOLATED', path, es, x, y)
                key = tuple(sorted((d[x], d[y]))) + (sxy,)
                nopair_types[key] += 1
    print('%s: %d graphs (n,m,tau)=(%d,%d,%d) slack=%d; #min transversals per graph in [%s,%s]; U\'\' predictions %d, failures %d; '
          'two-vertex predictions %d, failures %d; pairs in no min transversal by (dx,dy,share): %s  [%.1fs]'
          % (base, len(graphs), n, mm, tt, slack(n, mm, tt), min_nT, max_nT, n_vert_pred, viol_u, n_pairs_pred, viol_u2,
             dict(sorted(nopair_types.items())), time.time() - t0), flush=True)
    return viol_u + viol_u2

if __name__ == '__main__':
    bad = 0
    for p in sys.argv[1:]: bad += check_file(p)
    print('TOTAL failures:', bad)
