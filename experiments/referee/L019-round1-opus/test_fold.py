"""Referee test of L019 Theorem 5 (folding lemma), independent code (refhg.py).
For every graph K (checked to be in C unless mode 'random'), every vertex x of degree 2 with edges {x,u,u'},{x,w,w'},
every y in {u,u'}, z in {w,w'}:
 - adjacent pairs are counted (no fold);
 - (a) n(K°) = n-2, m(K°) = m-2, no degenerate image, phi injective on E(K-x), d(zeta) = d(y)+d(z)-2,
       Delta(K°) <= max(Delta(K), d(y)+d(z)-2), every other degree <= its degree in K;
 - (b) tau(K) <= tau(K°)+1;  also record tau(K°) - tau(K) in general;
 - (c) if x is co-transversal (tau(K-x) = tau(K)-1): tau(K°) = tau(K)-1 and s(K°) = s(K)+1;
 - (d) (only for K in C) K° linear <=> y,z have no common neighbour in K-x; every F7 copy of K° contains zeta;
       K° satisfies (P3) <=> no saturated S of K with y,z in S, x not in S; every such S has |S| >= 6;
       and the classification of the blocked folds.
usage: test_fold.py cells <path> <K> | random <N> <seed> | sets <name>"""
import sys, os, random, json, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from refhg import *

STATS = collections.Counter()
FAIL = []


def fail(msg):
    FAIL.append(msg)
    if len(FAIL) <= 20:
        print('FAIL', msg)


def check_graph(n, E, inC_known=None, tag=''):
    m = len(E)
    E = [tuple(sorted(g)) for g in E]
    if inC_known is None:
        inC = in_C(n, E, use_table=(n <= 22))
    else:
        inC = inC_known
    t = tau_bb(E)
    s = 3 * n + 2 * m - 11 * t
    d = degrees(n, E)
    Delta = max(d) if d else 0
    f = edge_table(n, E) if (inC and n <= 23) else None
    pc = popcounts(n) if f is not None else None
    idx = np.arange(1 << n, dtype=np.int64) if f is not None else None
    satmask = ((pc >= 3) & (f == pc - 2)) if f is not None else None
    STATS['graphs'] += 1
    for x in range(n):
        if d[x] != 2:
            continue
        ex = [g for g in E if x in g]
        assert len(ex) == 2
        Kx = [g for g in E if x not in g]
        tx = tau_bb(Kx)
        cot = (tx == t - 1)
        A = [u for u in ex[0] if u != x]
        B = [u for u in ex[1] if u != x]
        if len(set(A) | set(B)) != 4:
            fail('%s x=%d edges not linear' % (tag, x)); continue
        for y in A:
            for z in B:
                if adjacent(E, y, z):
                    STATS['adjacent'] += 1
                    continue
                STATS['folds'] += 1
                n2, imgs, zeta = fold(n, E, x, y, z)
                # (a)
                if n2 != n - 2:
                    fail('%s (a) n2' % tag)
                if len(imgs) != m - 2:
                    fail('%s (a) m2' % tag)
                if any(len(set(g)) != 3 for g in imgs):
                    fail('%s (a) degenerate image' % tag)
                if len(set(frozenset(g) for g in imgs)) != len(imgs):
                    fail('%s (a) phi not injective' % tag)
                E2 = [tuple(sorted(g)) for g in imgs]
                d2 = degrees(n2, E2)
                if d2[zeta] != d[y] + d[z] - 2:
                    fail('%s (a) deg zeta' % tag)
                if max(d2) > max(Delta, d[y] + d[z] - 2):
                    fail('%s (a) Delta bound' % tag)
                # other degrees: vertex labels: keep order of range(n) minus x,y,z
                keep = [u for u in range(n) if u not in (x, y, z)]
                for i, u in enumerate(keep):
                    if d2[i] > d[u]:
                        fail('%s (a) degree increased' % tag)
                # (b), (c)
                t2 = tau_bb(E2)
                s2 = 3 * n2 + 2 * len(E2) - 11 * t2
                STATS['dtau=%d' % (t2 - t)] += 1
                if not t <= t2 + 1:
                    fail('%s (b) tau(K) <= tau(K°)+1 violated' % tag)
                if cot:
                    STATS['folds_cotrans'] += 1
                    if t2 != t - 1:
                        fail('%s (c) tau(K°) != tau-1 at co-transversal x' % tag)
                    if s2 != s + 1:
                        fail('%s (c) slack change != +1' % tag)
                else:
                    STATS['folds_noncotrans'] += 1
                # (d) linearity criterion needs only K linear
                if linear(E):
                    lin2 = linear(E2)
                    cn = common_neighbours(E, y, z, avoid=x)
                    if lin2 != (len(cn) == 0):
                        fail('%s (d) linearity criterion' % tag)
                if not inC:
                    continue
                STATS['folds_KinC'] += 1
                lin2 = linear(E2)
                cps = f7_copies(E2)
                for (c, g1, g2) in cps:
                    if zeta != c and zeta not in g1 and zeta not in g2:
                        fail('%s (d) F7 copy avoiding zeta' % tag)
                if n2 <= 22:
                    p3_2 = p3_ok_table(n2, E2)
                else:
                    p3_2 = p3_ok_flow(E2)
                # saturated S of K with y,z in S, x not in S
                if f is not None:
                    mask_need = (1 << y) | (1 << z)
                    sel = satmask & ((idx & mask_need) == mask_need) & (((idx >> x) & 1) == 0)
                    sizes = pc[sel]
                    has_sat = bool(sel.any())
                    if p3_2 == has_sat:
                        fail('%s (d) P3 criterion mismatch' % tag)
                    if has_sat:
                        STATS['sat_min_size=%d' % int(sizes.min())] += 1
                        if int(sizes.min()) < 6:
                            fail('%s (d) saturated set of size < 6' % tag)
                inC2 = lin2 and not cps and p3_2
                key = ('N' if not lin2 else '') + ('F' if cps else '') + ('P' if not p3_2 else '')
                STATS['class_' + (key or 'inC')] += 1
                if inC2 and cot and s2 < 0:
                    fail('%s fold in C with negative slack' % tag)


def random_linear(rng, n, m):
    E = []; used = set()
    for _ in range(5000):
        if len(E) >= m:
            break
        g = tuple(sorted(rng.sample(range(n), 3)))
        ps = list(itertools.combinations(g, 2))
        if any(p in used for p in ps):
            continue
        used.update(ps); E.append(g)
    return E


if __name__ == '__main__':
    mode = sys.argv[1]
    if mode == 'cells':
        path, K = sys.argv[2], int(sys.argv[3])
        for i, (n, m, t, E) in enumerate(read_cell(path, K)):
            check_graph(n, E, tag='%s#%d' % (os.path.basename(path), i))
    elif mode == 'random':
        N, seed = int(sys.argv[2]), int(sys.argv[3])
        rng = random.Random(seed)
        for i in range(N):
            n = rng.randint(6, 14); m = rng.randint(2, n + 2)
            E = random_linear(rng, n, m)
            check_graph(n, E, tag='rand%d' % i)
    print(sys.argv[1:], dict(sorted(STATS.items())), 'FAILURES:', len(FAIL))
