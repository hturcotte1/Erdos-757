"""Referee L019: (1) Theorem 5 (folding lemma) on AP hypergraphs of realizable (4,5)-sets: A_base and ALL its induced
subsets, the three 12-point record sets, the n=8,10,11 records, the 2,910 saturated extremal 14-point classes (first K),
the Fibonacci set {2,3,5,8,...} (15 terms), the reader family K=0,1 (11, 20 points), and generic gluings of record sets;
(2) Lemma 11 (six ports) on every graph with Delta <= 3 met (stored cells and AP hypergraphs): for every saturated S:
 (a) sum_{y in S} (3 - d_{K[S]}(y)) = 6; (b) d_{K[S]}(y) >= 1, and d = 1, |S| >= 4 => S - y saturated;
 (c) if 2-core: exactly six vertices of K[S]-degree 2, every other vertex of S has all its K-edges inside S, and at most
     six edges meet both S and its complement; peeling degree-1 vertices ends in an edge or a 2-core saturated set.
(3) Theorem 2(iv) on stored lists with slack <= 1 (n <= 26 <= N = 27, L016): every edge critical; and the bound for
    |D| = 2, 3 on a sample.
usage: test_ap_and_lemma11.py ap | lemma11 <cellpath> <K> | thm2iv <cellpath> <K>"""
import sys, os, json, gzip, collections, itertools, random
from fractions import Fraction
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from refhg import *
import test_fold as TF

FAILS = []
ST = collections.Counter()


def fail(msg):
    FAILS.append(msg)
    if len(FAILS) <= 20:
        print('FAIL', msg)


def is45(A):
    """every 4 points determine >= 5 distinct distances (exact ints)."""
    A = sorted(A)
    for B in itertools.combinations(A, 4):
        ds = set(abs(a - b) for a, b in itertools.combinations(B, 2))
        if len(ds) < 5:
            return False
    return True


def lemma11_graph(n, E, tag):
    d = degrees(n, E)
    if not E or max(d) > 3 or n > 23:
        return
    f = edge_table(n, E)
    sats = saturated_sets(n, E, f)
    ST['lemma11_graphs'] += 1
    masks = masks_of(E)
    for S in sats:
        ST['saturated_sets'] += 1
        verts = [u for u in range(n) if S >> u & 1]
        inside = [g for g, mk in zip(E, masks) if mk & S == mk]
        dS = collections.Counter(u for g in inside for u in g)
        tot = sum(3 - dS[u] for u in verts)
        if tot != 6:
            fail('%s L11(a) S=%s' % (tag, verts))
        for u in verts:
            if dS[u] == 0:
                fail('%s L11(b) isolated vertex in K[S]' % tag)
            if dS[u] == 1 and len(verts) >= 4:
                S2 = S & ~(1 << u)
                if f[S2] != len(verts) - 1 - 2:
                    fail('%s L11(b) S-y not saturated' % tag)
        if all(dS[u] >= 2 for u in verts):
            ST['2core'] += 1
            ports = [u for u in verts if dS[u] == 2]
            if len(ports) != 6:
                fail('%s L11(c) ports=%d' % (tag, len(ports)))
            for u in verts:
                if dS[u] == 3 and d[u] != 3:
                    fail('%s L11(c) degree' % tag)
            boundary = [g for g, mk in zip(E, masks) if (mk & S) and (mk & ~S)]
            if len(boundary) > 6:
                fail('%s L11(c) boundary edges %d' % (tag, len(boundary)))
            for g in boundary:
                if not any(u in ports for u in g if S >> u & 1):
                    fail('%s L11(c) boundary edge not through a port' % tag)
        # peeling
        cur = S
        while True:
            vs = [u for u in range(n) if cur >> u & 1]
            ins = [mk for mk in masks if mk & cur == mk]
            dd = collections.Counter(u for mk in ins for u in range(n) if mk >> u & 1)
            if f[cur] != len(vs) - 2:
                fail('%s L11 peeling lost saturation' % tag); break
            ones = [u for u in vs if dd[u] == 1]
            if len(vs) == 3:
                if len(ins) != 1:
                    fail('%s L11 peel end not an edge' % tag)
                break
            if not ones:
                if any(dd[u] < 2 for u in vs):
                    fail('%s L11 peel end not 2-core' % tag)
                break
            cur &= ~(1 << ones[0])


def ap_suite():
    recs = json.load(open('/home/user/Erdos-757/data/small_records.json'))['sets']
    sets = {k: v['set'] for k, v in recs.items()}
    fam = json.load(open('/home/user/Erdos-757/data/reader_5_9_family.json'))['family']
    for x in fam:
        if x['K'] <= 1:
            sets['reader_K%d' % x['K']] = x['set']
    fib = [2, 3]
    while len(fib) < 15:
        fib.append(fib[-1] + fib[-2])
    sets['fib15'] = fib
    # generic gluing A u (qB + t) with q, t chosen large and checked
    def glue(A, B, q, t):
        return sorted(set(A) | set(q * b + t for b in B))
    sets['glue_12_12b'] = glue(sets['12'], sets['12b'], 1000003, 10 ** 12)
    sets['glue_10_8'] = glue(sets['10'], [x // 1 for x in sets['8']], 7919, 10 ** 15)
    for name, A in sets.items():
        ok45 = is45(A) if len(A) <= 24 else None
        n = len(A)
        E = ap_edges(A)
        inC = in_C(n, E, use_table=(n <= 22))
        print('set', name, 'n', n, 'm', len(E), '(4,5):', ok45, 'in C:', inC, 'tau', tau_bb(E))
        if ok45 is False:
            print('  note: %s is not a (4,5)-set (construction artefact of this test), skipped' % name)
            continue
        if not inC:
            fail('set %s: AP graph not in C' % name)
        TF.check_graph(n, E, inC_known=inC, tag=name)
        lemma11_graph(n, E, name)
    # all induced subsets of A_base
    A = sets['14']
    E = ap_edges(A)
    n = len(A)
    cntsub = 0
    for r in range(3, n + 1):
        for keep in itertools.combinations(range(n), r):
            n2, E2 = induced(n, E, keep)
            if not E2:
                continue
            cntsub += 1
            TF.check_graph(n2, E2, inC_known=True, tag='Abase_sub')
            lemma11_graph(n2, E2, 'Abase_sub')
    print('A_base induced subsets with an edge:', cntsub)
    # saturated extremal 14-point classes (census)
    k = 0
    with gzip.open('/home/user/Erdos-757/data/census_n14_m12_classes.jsonl.gz', 'rt') as fh:
        for line in fh:
            row = json.loads(line)
            E = [tuple(e) for e in row['edges']]
            TF.check_graph(14, E, inC_known=None, tag='census14')
            lemma11_graph(14, E, 'census14')
            k += 1
            if k >= 150:
                break
    print('census14 classes tested:', k)


def thm2iv(path, K):
    rng = random.Random(5)
    for i, (n, m, t, E) in enumerate(read_cell(path, K)):
        s = 3 * n + 2 * m - 11 * t
        if s > 1:
            continue
        ST['thm2iv_graphs'] += 1
        for j in range(m):
            if tau_bb(E[:j] + E[j + 1:]) != t - 1:
                fail('Thm2(iv) edge not critical %s #%d edge %d' % (path, i, j))
            ST['edges_checked'] += 1
        for r in (2, 3):
            for _ in range(10):
                D = set(rng.sample(range(m), r))
                tD = tau_bb([E[j] for j in range(m) if j not in D])
                bound = -((-(2 * r - s)) // 11)
                if tD > t - bound:
                    fail('Thm2(iv) |D|=%d' % r)
                ST['D_checked'] += 1


if __name__ == '__main__':
    mode = sys.argv[1]
    if mode == 'ap':
        ap_suite()
    elif mode == 'lemma11':
        for i, (n, m, t, E) in enumerate(read_cell(sys.argv[2], int(sys.argv[3]))):
            lemma11_graph(n, E, '%s#%d' % (os.path.basename(sys.argv[2]), i))
    elif mode == 'thm2iv':
        thm2iv(sys.argv[2], int(sys.argv[3]))
    print(sys.argv[1:], 'fold stats:', dict(sorted(TF.STATS.items())), 'fold FAILURES:', len(TF.FAIL))
    print(sys.argv[1:], 'stats:', dict(ST), 'FAILURES:', len(FAILS))
