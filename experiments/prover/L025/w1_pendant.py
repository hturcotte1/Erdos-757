"""W1 (consistency test of Theorem 10 and Remark 10.3 on pendant b-configurations that do occur).

For every stored class F (max degree <= 3) of the given cell files: let Av be the avoided vertices of F of degree <= 2
(in no minimum transversal).  For every triple of 2-sets P1,P2,P3 of Av (pairwise meeting in <= 1 vertex, no vertex in
all three, no P_i inside an edge of F, and d_F(u) + #{i: u in P_i} <= 3), build G = F + pendant edges {a}+P1, {b}+P2,
{c}+P3 and test whether {a,b,c} is a b-configuration of G (pairwise not co-transversal).  Theorem 10 (unconditional for
n(G) <= 25 by L016) says: a connected such G has s(G) >= 1, and s(G) = 1 only for pendant triples (these are pendant by
construction); Remark 10.3 says a connected such G with n(G) <= 26 has s(G) >= 2.  The script reports every hit with
s(G) <= 1 (none expected) and the distribution of s(G).
Usage: python3 w1_pendant.py <cell file> ...   (FOUND: format or 'n m t edges' format)"""
import sys, time
from itertools import combinations
from hyp25 import *
from lemmas25 import read_found, inC

def run(path):
    stats = {}
    hits = 0; bad = 0; t0 = time.time(); ncls = 0
    for E in read_found(path):
        n0 = 1 + max(max(e) for e in E)
        F = Hyp(E, range(n0))
        if F.maxdeg() > 3:
            continue
        ncls += 1
        cov = 0
        for T in F.min_transversals():
            cov |= T
        av = [u for u in F.V if not (cov & F.bit(u)) and F.deg[u] <= 2]
        if len(av) < 3:
            continue
        prs = [p for p in combinations(av, 2) if frozenset(p) not in F.sig]
        for P in combinations(prs, 3):
            S = [set(p) for p in P]
            if any(len(S[i] & S[j]) > 1 for i, j in ((0, 1), (0, 2), (1, 2))):
                continue
            if S[0] & S[1] & S[2]:
                continue
            cnt = {}
            for s_ in S:
                for u in s_:
                    cnt[u] = cnt.get(u, 0) + 1
            if any(F.deg[u] + k > 3 for u, k in cnt.items()):
                continue
            N = n0
            a, b, c = N, N + 1, N + 2
            E2 = list(E) + [tuple(sorted((a,) + P[0])), tuple(sorted((b,) + P[1])), tuple(sorted((c,) + P[2]))]
            G = Hyp(E2, list(range(n0 + 3)))
            ba, bb, bc = G.bit(a), G.bit(b), G.bit(c)
            nc = all(not ((T & x) and (T & y)) for T in G.min_transversals() for (x, y) in ((ba, bb), (ba, bc), (bb, bc)))
            if not nc:
                continue
            hits += 1
            s = G.slack(); con = G.connected()
            key = (s, con, len(cnt) == 6)
            stats[key] = stats.get(key, 0) + 1
            if con and (s <= 0 or (s == 1 and G.n <= 26)):
                bad += 1
                print('  UNEXPECTED', path.split('/')[-1], E, P, 'n', G.n, 's', s, 'inC', inC(G), flush=True)
    print(path.split('/')[-1], 'classes', ncls, 'pendant b-configurations', hits,
          '(slack, connected, |W|=6): count', dict(sorted(stats.items())), 'unexpected', bad, 'time %.1fs' % (time.time() - t0), flush=True)

if __name__ == '__main__':
    for p in sys.argv[1:]:
        run(p)
