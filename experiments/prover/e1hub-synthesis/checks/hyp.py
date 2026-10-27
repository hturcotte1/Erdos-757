"""Own minimal 3-graph toolkit for the E1-hub synthesis checks.

Independent of e757/, judge/ and all L0xx code: exact integer arithmetic only.
A graph is (n, edges) with edges a list of 3-tuples of ints in range(n).
"""
from itertools import combinations


def parse_line(line):
    t = list(map(int, line.split()))
    n, m, tau = t[0], t[1], t[2]
    e = t[3:]
    assert len(e) == 3 * m, (n, m, len(e))
    edges = [tuple(sorted(e[3 * i:3 * i + 3])) for i in range(m)]
    return n, edges, tau


def read_cell(path):
    """Reads either 'n m tau e1 e2 ...' lines or engine 'FOUND: (a,b,c) ...' lines
    (then n, m, tau are taken from the file name cell_n_m_tau_D*.txt)."""
    import os, re
    base = os.path.basename(path)
    mm = re.match(r'cell_(\d+)_(\d+)_(\d+)', base)
    out = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#') or line.startswith('INFO'):
                continue
            if line.startswith('FOUND:'):
                n, m, tau = map(int, mm.groups())
                tri = re.findall(r'\((\d+),(\d+),(\d+)\)', line)
                edges = [tuple(sorted(map(int, t))) for t in tri]
                assert len(edges) == m, (path, len(edges), m)
                out.append((n, edges, tau))
            else:
                out.append(parse_line(line))
    return out


def degrees(n, edges):
    d = [0] * n
    for e in edges:
        for u in e:
            d[u] += 1
    return d


def tau_masks(edge_masks, bound):
    """Exact transversal number of the hypergraph given by vertex bitmasks, by 3-way branching.
    Returns min(tau, bound+1) (stops exploring beyond bound)."""
    best = [bound + 1]

    def rec(chosen_mask, k, remaining):
        if k >= best[0]:
            return
        # first uncovered edge
        for em in remaining:
            if not (em & chosen_mask):
                # branch on its vertices
                x = em
                while x:
                    low = x & -x
                    rec(chosen_mask | low, k + 1, remaining)
                    x ^= low
                return
        best[0] = k

    rec(0, 0, edge_masks)
    return best[0]


def tau(n, edges, removed=0):
    ems = [sum(1 << u for u in e) for e in edges]
    ems = [em for em in ems if not (em & removed)]
    return tau_masks(ems, len(ems))


def all_min_transversals(n, edges):
    """All minimum transversals as bitmasks (exhaustive search over size-tau subsets via branching)."""
    ems = [sum(1 << u for u in e) for e in edges]
    t = tau_masks(ems, len(ems))
    res = set()

    def rec(chosen, k):
        if k > t:
            return
        for em in ems:
            if not (em & chosen):
                x = em
                while x:
                    low = x & -x
                    rec(chosen | low, k + 1)
                    x ^= low
                return
        # chosen is a transversal with k <= t vertices; it is minimum iff k == t
        if k == t:
            res.add(chosen)

    rec(0, 0)
    return t, sorted(res)


def is_linear(edges):
    seen = {}
    for i, e in enumerate(edges):
        for p in combinations(e, 2):
            if p in seen:
                return False
            seen[p] = i
    return True
