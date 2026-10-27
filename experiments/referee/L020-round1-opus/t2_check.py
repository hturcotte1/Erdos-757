"""Lemma 2.1 (7 nu >= 2|E| for simple graphs with Delta <= 3) and Theorem 2 (7 s >= 21 n0 + n2 for linear
3-graphs with Delta <= 2; s >= (m-1)/7 when connected, m >= 2) of L020, own code.
Part 1 reads graph6 from stdin (geng -D3 output) and computes nu by an exact bitmask DP.
Part 2: random linear 3-graphs with Delta <= 2, exact tau (own B&B), dual-graph identity."""
import sys, random
sys.path.insert(0, '/home/user/Erdos-757/experiments/referee/L020-round1-opus')
import hg
from functools import lru_cache


def g6_decode(s):
    s = s.strip()
    data = [ord(c) - 63 for c in s]
    n = data[0]
    bits_ = []
    for v in data[1:]:
        for k in range(5, -1, -1):
            bits_.append(v >> k & 1)
    edges = []
    k = 0
    for j in range(1, n):
        for i in range(j):
            if bits_[k]:
                edges.append((i, j))
            k += 1
    return n, edges


def nu_exact(n, edges):
    adj = [0] * n
    for i, j in edges:
        adj[i] |= 1 << j
        adj[j] |= 1 << i

    @lru_cache(maxsize=None)
    def f(mask):
        if mask == 0:
            return 0
        lb = mask & -mask
        i = lb.bit_length() - 1
        rest = mask ^ lb
        best = f(rest)  # i unmatched
        nb = adj[i] & rest
        while nb:
            b = nb & -nb
            nb ^= b
            best = max(best, 1 + f(rest ^ b))
        return best
    return f((1 << n) - 1)


def part1():
    cnt = fails = eq = 0
    eq_examples = []
    for line in sys.stdin:
        if not line.strip():
            continue
        n, E = g6_decode(line)
        nu = nu_exact(n, E)
        cnt += 1
        if 7 * nu < 2 * len(E):
            fails += 1
            print('FAIL', line.strip())
        if 7 * nu == 2 * len(E) and E:
            eq += 1
            eq_examples.append(line.strip())
    print('Lemma 2.1: graphs', cnt, 'failures', fails, 'equality with |E|>0:', eq, eq_examples[:10])


def rand_linear_delta2(n, tries):
    edges = []
    deg = [0] * n
    pairs = set()
    for _ in range(tries):
        e = tuple(sorted(random.sample(range(n), 3)))
        if any(deg[x] >= 2 for x in e):
            continue
        ps = [(e[0], e[1]), (e[0], e[2]), (e[1], e[2])]
        if any(p in pairs for p in ps):
            continue
        edges.append(e)
        for x in e:
            deg[x] += 1
        pairs.update(ps)
    return edges


def part2(N):
    random.seed(11)
    fails = 0
    tested = 0
    conn_tested = 0
    for it in range(N):
        n = random.randint(3, 24)
        es = rand_linear_delta2(n, random.randint(1, 3 * n))
        if not es:
            continue
        t = hg.tau_bb(es)
        m = len(es)
        s = hg.slack(n, m, t)
        d = hg.degrees(n, es)
        n0 = d.count(0); n2 = d.count(2)
        # dual graph
        dual = []
        for x in range(n):
            if d[x] == 2:
                a, b = [i for i, e in enumerate(es) if x in e]
                dual.append((a, b))
        assert len(set(dual)) == len(dual)  # simple
        nu = nu_exact(m, dual) if m <= 30 else None
        ok = 7 * s >= 21 * n0 + n2
        if nu is not None:
            ok &= (s == 3 * n0 + 11 * nu - 3 * n2) and (t == m - nu)
        if hg.is_connected(n, es) and m >= 2:
            conn_tested += 1
            ok &= 7 * s >= m - 1 and n <= 2 * m + 1
        tested += 1
        if not ok:
            fails += 1
            print('FAIL', n, es, s, n0, n2, nu)
    print('Theorem 2: random linear Delta<=2 3-graphs tested', tested, '(connected with m>=2:', conn_tested, ') failures', fails)


if __name__ == '__main__':
    if sys.argv[1] == 'lemma':
        part1()
    else:
        part2(int(sys.argv[2]))
