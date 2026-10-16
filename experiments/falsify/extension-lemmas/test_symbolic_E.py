"""Test 4: Lemma E (4,5) claim for ALL t > T0, done symbolically: points of C are linear forms c0 + c1*t,
(c1 in {-1,0,1}); for t beyond all breakpoints every difference is |form| with sign fixed by (c1, c0) lexicographically.
Counts distinct differences of every 4-subset containing a new point. Also: universal extreme vertices table; negative control
(non-extreme a that is a midpoint -> must fail); bound on the bad t found in the numeric sweep."""
import sys, json, itertools, random, gzip
sys.path.insert(0, '/home/user/Erdos-757'); sys.path.insert(0, '.')
import falsify as F
from falsify import HG, pr
from e757.core import is_45_set

def sym_diffs_ok(B, ai):
    """B sorted ints (the scaled set), a=B[ai]; points: (c0,c1). Return list of 4-subsets with <5 distinct |differences| for t large."""
    a = B[ai]
    P = [(b, 0) for b in B] + [(a, 1), (a, -1)]
    bad = []
    nB = len(B)
    for q in itertools.combinations(range(nB + 2), 4):
        if max(q) < nB: continue
        ds = set()
        for i, j in itertools.combinations(q, 2):
            c0 = P[i][0] - P[j][0]; c1 = P[i][1] - P[j][1]
            if (c1, c0) < (0, 0): c0, c1 = -c0, -c1    # lexicographic sign for large t
            ds.add((c0, c1))
        if len(ds) < 5: bad.append(tuple(P[i] for i in q))
    return bad

if __name__ == '__main__':
    rng = random.Random(3)
    sets = F.load_sets()
    tot = 0; fails = []; ctrl = 0; ctrl_fail = 0
    table = {}
    for src, S in sets:
        A = sorted(S); B = [2 * x for x in A]; n = len(A)
        for ai in (0, n - 1):
            tot += 1
            bad = sym_diffs_ok(B, ai)
            if bad: fails.append((src, ai, bad[:2]))
        # control: non-extreme a which is a midpoint (should produce a 4-subset with <5 differences)
        H = HG(A)
        mids = {e[1] for e in H.E}
        for ai in list(mids)[:2]:
            ctrl += 1
            if sym_diffs_ok(B, ai): ctrl_fail += 1
        # universal extreme table
        U = H.universal()
        for ai in (0, n - 1):
            if ai in U:
                key = (n, H.alpha, H.deg[ai], 'extremal' if src.startswith(('n', 'rec', 'A_base')) and not src.startswith('fib') else 'fib')
                table[key] = table.get(key, 0) + 1
    pr('Lemma E symbolic (t large): extreme a tested', tot, 'failures', len(fails), fails[:3])
    pr('control (non-extreme midpoint a): tested', ctrl, 'sets showing <5 distinct diffs', ctrl_fail)
    pr('universal extreme vertices (n, h, deg a, family): count')
    FN = {5:3,6:4,7:5,8:5,9:6,10:6,11:7,12:7,13:8,14:8,15:9}
    for k, v in sorted(table.items()):
        n, h, d, fam = k
        pr(k, v, ' -> C: (n+2,h+1)=(%d,%d); f(n+2)=%s; D(A)=%d D(C)=%d' % (n + 2, h + 1, FN.get(n + 2), 17*h - 9*n, 17*(h+1) - 9*(n+2)))
    json.dump(dict(tot=tot, fails=fails, ctrl=ctrl, ctrl_fail=ctrl_fail, table={str(k): v for k, v in table.items()}), open('results_symbolic_E.json', 'w'), default=str)
