"""Referee check of L020 Lemma 2.1 (7 nu >= 2|E| for simple graphs with Delta<=3) on all graphs with <= 9 vertices
(nauty geng, independent binary; own exact maximum matching by bitmask recursion), and of Theorem 2's inequality
7 s >= 21 n_0 + n_2 on random linear 3-graphs with Delta <= 2 (own tau)."""
import sys, subprocess, random, itertools
sys.path.insert(0, '/home/user/Erdos-757/experiments/referee/L020-round1-fable')
import ref3 as R
GENG = '/home/user/Erdos-757/experiments/referee/L013-round2/out/nauty_build/geng'

def parse_g6(s):
    N = ord(s[0]) - 63
    bits = []
    for ch in s[1:]:
        v = ord(ch) - 63
        bits.extend((v >> k) & 1 for k in range(5, -1, -1))
    edges = []
    k = 0
    for j in range(N):
        for i in range(j):
            if bits[k]:
                edges.append((i, j))
            k += 1
    return N, edges

def max_matching(N, edges):
    adj = [[] for _ in range(N)]
    for (i, j) in edges:
        adj[i].append(j); adj[j].append(i)
    from functools import lru_cache
    @lru_cache(maxsize=None)
    def best(mask):
        # lowest unmatched vertex
        if mask == (1 << N) - 1:
            return 0
        v = 0
        while (mask >> v) & 1:
            v += 1
        res = best(mask | (1 << v))  # v unmatched
        for u in adj[v]:
            if not (mask >> u) & 1:
                res = max(res, 1 + best(mask | (1 << v) | (1 << u)))
        return res
    return best(0)

def main():
    tot = 0; fails = 0; eq = 0
    for N in range(1, 10):
        out = subprocess.run([GENG, '-q', '-D3', str(N)], capture_output=True, text=True).stdout.split('\n')
        for s in out:
            if not s.strip():
                continue
            n, edges = parse_g6(s)
            nu = max_matching(n, edges)
            tot += 1
            if 7 * nu < 2 * len(edges):
                fails += 1; print('FAIL', s, nu, len(edges))
            if edges and 7 * nu == 2 * len(edges):
                eq += 1
        print('N', N, 'graphs so far', tot, 'fails', fails, 'equality cases', eq, flush=True)
    print('LEMMA 2.1: graphs', tot, 'failures', fails, 'equality (E>0)', eq)
    # Theorem 2 on random linear Delta<=2 3-graphs
    random.seed(3)
    bad = 0; tested = 0
    for trial in range(3000):
        n = random.randint(3, 14)
        E = []
        deg = [0] * n
        for _ in range(random.randint(1, 9)):
            e = tuple(sorted(random.sample(range(n), 3)))
            if any(deg[x] >= 2 for x in e):
                continue
            if any(len(set(e) & set(f)) > 1 for f in E):
                continue
            E.append(e)
            for x in e:
                deg[x] += 1
        if not E:
            continue
        t = R.tau(n, E)
        s = 3 * n + 2 * len(E) - 11 * t
        n0 = deg.count(0); n2 = deg.count(2)
        tested += 1
        if 7 * s < 21 * n0 + n2:
            bad += 1; print('THM2 FAIL', n, E, t, s, n0, n2)
    print('THEOREM 2 random test: tested', tested, 'failures', bad)

if __name__ == '__main__':
    main()
