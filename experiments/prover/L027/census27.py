"""L027 census (own code): pairwise non-co-transversal non-edge triples (no degree restriction)
in stored near-tight lists.  Theorem B + Remark B.3 predict: none in a tight graph (given H_{n+2}),
and only pendant ones in a slack-1 graph.  Usage: python3 census27.py <cell files>
Cell file lines: 'n m tau e1 e2 ...' (edges as flattened triples)."""
import sys, re
from itertools import combinations


def read(path):
    """Reads 'n m tau e1 e2 ...' lines or engine 'FOUND: (a,b,c) ...' lines (then n, m, tau come
    from the file name cell_n_m_tau_*.txt)."""
    import os
    mm = re.match(r'cell_(\d+)_(\d+)_(\d+)', os.path.basename(path))
    out = []
    for line in open(path):
        line = line.strip()
        if not line or line.startswith('#') or line.startswith('INFO'):
            continue
        if line.startswith('FOUND:'):
            n, m, tau = map(int, mm.groups())
            tri = re.findall(r'\((\d+),(\d+),(\d+)\)', line)
            edges = [tuple(sorted(map(int, x))) for x in tri]
            assert len(edges) == m
            out.append((n, edges, tau))
            continue
        t = list(map(int, line.split()))
        n, m, tau = t[0], t[1], t[2]
        e = t[3:]
        assert len(e) == 3 * m
        out.append((n, [tuple(sorted(e[3 * i:3 * i + 3])) for i in range(m)], tau))
    return out


def all_min_T(n, edges):
    ems = [(1 << a) | (1 << b) | (1 << c) for (a, b, c) in edges]
    best = [len(ems)]

    def rec_t(ch, k):
        if k >= best[0]:
            return
        for em in ems:
            if not em & ch:
                x = em
                while x:
                    lo = x & -x
                    rec_t(ch | lo, k + 1)
                    x ^= lo
                return
        best[0] = k
    rec_t(0, 0)
    t = best[0]
    res = set()

    def rec(ch, k):
        if k > t:
            return
        for em in ems:
            if not em & ch:
                x = em
                while x:
                    lo = x & -x
                    rec(ch | lo, k + 1)
                    x ^= lo
                return
        if k == t:
            res.add(ch)
    rec(0, 0)
    return t, res


tot = 0
for path in sys.argv[1:]:
    cls = read(path)
    found = pend = 0
    for (n, edges, tau) in cls:
        t, Ts = all_min_T(n, edges)
        assert t == tau, (path, t, tau)
        co = set()
        for T in Ts:
            vs = [u for u in range(n) if T >> u & 1]
            co.update(combinations(vs, 2))
        es = set(edges)
        d = [0] * n
        for e in edges:
            for u in e:
                d[u] += 1
        for tr in combinations(range(n), 3):
            if tr in es:
                continue
            if any(p in co for p in combinations(tr, 2)):
                continue
            found += 1
            if all(d[u] == 1 for u in tr) and not any(len(set(tr) & set(e)) >= 2 for e in edges):
                pend += 1
    n0, m0, t0 = cls[0][0], len(cls[0][1]), cls[0][2]
    print(path.split('/')[-1], 'classes', len(cls), 'slack', 3 * n0 + 2 * m0 - 11 * t0,
          'pairwise-NC non-edge triples', found, 'of which pendant', pend, flush=True)
    tot += found
print('TOTAL pairwise-NC non-edge triples', tot)
