"""pendant_check.py -- referee's falsification test of L018 Theorem 3 on the census graphs (own code).

For every pendant vertex y of every census graph (connected members of C, Delta <= 3) with 5 <= n <= NMAX:
  * r-reducible (r = 1, 2, 3): exists Z subset of B_r(y), Z nonempty, Z != V, with value(Z) >= 0 (brute force over Z,
    exact tau by branch and bound);
  * structural type at radius 2 by a direct test of the definitions P-tree-2 / P-tri-2 of Theorem 3(b).
Checks: (a) not 1-reducible => d(a) = d(b) = 2; (b) not 2-reducible => type P-tree-2 or P-tri-2;
(c) for n <= 11 every pendant is 3-reducible (P-tree-3 needs 15 and P-tri-3 needs 12 vertices within distance 3).
Prints the counts per n for comparison with the prover's validate_catalog_output.txt.
"""
import itertools, sys, os
from collections import Counter

BASE = '/home/user/Erdos-757/experiments/20261027-0230-red-config/out'


def read_census(n):
    out = []
    for m in range(1, n - 1):
        f = os.path.join(BASE, 'cls_%d_%d.txt' % (n, m))
        if not os.path.exists(f):
            continue
        with open(f) as fh:
            for line in fh:
                es = [p for p in line.split() if '.' in p]
                if es:
                    out.append([tuple(int(x) for x in p.split('.')) for p in es])
    return out


def tau_bb(E):
    if not E:
        return 0
    best = [len(E)]
    def rec(es, k):
        if k >= best[0]:
            return
        if not es:
            best[0] = k; return
        e = es[0]
        for v in e:
            rec([f for f in es if v not in f], k + 1)
    rec([frozenset(e) for e in E], 0)
    return best[0]


def analyse(n, E):
    deg = [0] * n
    inc = [[] for _ in range(n)]
    for j, e in enumerate(E):
        for v in e:
            deg[v] += 1; inc[v].append(j)
    adj = [set() for _ in range(n)]
    for e in E:
        for a, b in itertools.permutations(e, 2):
            adj[a].add(b)
    vm = [0] * n
    for j, e in enumerate(E):
        for v in e:
            vm[v] |= 1 << j
    memo = {}
    def reducible_within(ball):
        ball = sorted(ball)
        for k in range(1, len(ball) + 1):
            for Z in itertools.combinations(ball, k):
                if len(Z) == n:
                    continue
                F = 0
                for z in Z:
                    F |= vm[z]
                if F not in memo:
                    memo[F] = tau_bb([E[j] for j in range(len(E)) if (F >> j) & 1])
                if 3 * len(Z) + 2 * bin(F).count('1') - 11 * memo[F] >= 0:
                    return True
        return False
    def ball(y, r):
        B = {y}; fr = {y}
        for _ in range(r):
            fr = set(u for x in fr for u in adj[x]) - B
            B |= fr
        return B
    res = []
    for y in range(n):
        if deg[y] != 1:
            continue
        e0 = E[inc[y][0]]
        a, b = [v for v in e0 if v != y]
        red1 = reducible_within(ball(y, 1))
        red2 = red1 or reducible_within(ball(y, 2))
        red3 = red2 or reducible_within(ball(y, 3))
        typ = 'other'
        if deg[a] == 2 and deg[b] == 2:
            A = [E[j] for j in inc[a] if E[j] != e0][0]
            Bq = [E[j] for j in inc[b] if E[j] != e0][0]
            B2 = ball(y, 2)
            inter = set(A) & set(Bq)
            if not inter:
                others = [u for u in set(A) | set(Bq) if u not in (a, b)]
                if all(deg[u] == 2 for u in others):
                    sec = []
                    for u in others:
                        f = [E[j] for j in inc[u] if E[j] not in (A, Bq)]
                        sec.append(f[0])
                    if len(set(sec)) == 4 and all(len(set(f) & B2) == 1 for f in sec):
                        typ = 'P-tree-2'
            else:
                c = next(iter(inter))
                if deg[c] == 3:
                    ap = [u for u in A if u not in (a, c)][0]
                    bp = [u for u in Bq if u not in (b, c)][0]
                    if deg[ap] == 2 and deg[bp] == 2:
                        Cc = [E[j] for j in inc[c] if E[j] not in (A, Bq)][0]
                        Ap = [E[j] for j in inc[ap] if E[j] != A][0]
                        Bp = [E[j] for j in inc[bp] if E[j] != Bq][0]
                        if len({Cc, Ap, Bp}) == 3 and all(len(set(f) & B2) == 1 for f in (Cc, Ap, Bp)):
                            typ = 'P-tri-2'
        res.append((y, deg[a], deg[b], red1, red2, red3, typ))
    return res


def main():
    nmax = int(sys.argv[1]) if len(sys.argv) > 1 else 11
    viol = 0
    for n in range(5, nmax + 1):
        cnt = Counter()
        for E in read_census(n):
            assert 1 + max(v for e in E for v in e) == n
            for (y, da, db, r1, r2, r3, typ) in analyse(n, E):
                if not r1 and not (da == 2 and db == 2):
                    viol += 1; print('VIOLATION (a)', n, E, y)
                if not r2 and typ == 'other':
                    viol += 1; print('VIOLATION (b)', n, E, y)
                if n <= 11 and not r3:
                    viol += 1; print('VIOLATION (c) n<=11 pendant not 3-reducible', n, E, y)
                cnt[(typ, 'irreducible2' if not r2 else 'reducible2', 'irreducible3' if not r3 else 'reducible3')] += 1
        print('n=%d' % n, sorted(cnt.items()), flush=True)
    print('violations:', viol)


if __name__ == '__main__':
    main()
