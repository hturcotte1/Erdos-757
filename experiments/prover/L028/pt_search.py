"""End-to-end consistency search for the PT residual (L028).

For a 3-graph F in C with maximum degree <= 3, a *PT configuration* is a triple of
pairwise disjoint 2-sets A, B, C of vertices of degree <= 2, none inside an edge, with
 (i)  no minimum transversal of F meets A u B u C, and
 (ii) no transversal of F with tau(F)+1 vertices meets all of A, B, C.
L028 Theorem 1 (with I11 below n(F)+3, true for n(F) <= 24 by L013/L016) predicts
s(F) >= 9 for every connected F carrying a PT configuration, and its proof predicts
more: (P1) G = F + three pendant edges has s(G) = s(F) - 7 ... (only when tau(G) = tau(F)+2);
(P2) if s(F) = 8 a saturated set contains W, all of W has degree 2, and two vertices of
different pairs are non-adjacent: impossible.
We record, per graph, the configurations, their slack, the degrees of W, and the
slack of the replacement Q = (F-u-w) + {t} u Z of Lemma 2 for every admissible (u,w).

Usage:
  python3 pt_search.py random <trials> <seed> <nmin> <nmax>
  python3 pt_search.py files <cell files...>
"""
import random
import sys
from itertools import combinations

from hyp28 import (tau, transversals_upto, popcount, in_C, degrees, adjacent,
                   read_cell, saturated_sets)


def connected(n, edges):
    if n == 0:
        return True
    adj = [set() for _ in range(n)]
    for e in edges:
        for u in e:
            adj[u].update(e)
    seen = {0}
    st = [0]
    while st:
        u = st.pop()
        for w in adj[u]:
            if w not in seen:
                seen.add(w)
                st.append(w)
    return len(seen) == n


def configs(n, edges, t=None):
    if t is None:
        t = tau(n, edges)
    trs = transversals_upto(n, edges, t + 1)
    mins = [T for T in trs if popcount(T) == t]
    plus = [T for T in trs if popcount(T) == t + 1]
    cov = 0
    for T in mins:
        cov |= T
    deg = degrees(n, edges)
    cand = [u for u in range(n) if not (cov >> u) & 1 and deg[u] <= 2]
    pairs = [p for p in combinations(cand, 2) if not adjacent(edges, p[0], p[1])]
    out = []
    for P, Q, R in combinations(pairs, 3):
        if len(set(P) | set(Q) | set(R)) != 6:
            continue
        bP = (1 << P[0]) | (1 << P[1])
        bQ = (1 << Q[0]) | (1 << Q[1])
        bR = (1 << R[0]) | (1 << R[1])
        if any((T & bP) and (T & bQ) and (T & bR) for T in plus):
            continue
        out.append((P, Q, R))
    return t, out


def analyse(n, edges, t, cfgs, stats):
    s = 3 * n + 2 * len(edges) - 11 * t
    deg = degrees(n, edges)
    for (A, B, C) in cfgs:
        stats['configs'] += 1
        stats['min_slack'] = min(stats['min_slack'], s)
        stats['slack_hist'][s] = stats['slack_hist'].get(s, 0) + 1
        W = A + B + C
        dW = tuple(sorted(deg[w] for w in W))
        stats['degW'][dW] = stats['degW'].get(dW, 0) + 1
        # Lemma 2 replacements: u in X, w in Y (different pairs), deg 2 each, non-adjacent
        for X, Y, Z in ((A, B, C), (A, C, B), (B, A, C), (B, C, A), (C, A, B), (C, B, A)):
            for u in X:
                for w in Y:
                    keep = [v for v in range(n) if v not in (u, w)]
                    mp = {v: i for i, v in enumerate(keep)}
                    Qe = [tuple(sorted(mp[v] for v in e)) for e in edges
                          if u not in e and w not in e]
                    tt = len(keep)
                    Qe.append(tuple(sorted((mp[Z[0]], mp[Z[1]], tt))))
                    tq = tau(tt + 1, Qe)
                    sq = 3 * (tt + 1) + 2 * len(Qe) - 11 * tq
                    dd = sum(1 for e in edges if u in e or w in e)
                    pred = s - 1 - 2 * dd
                    stats['Q'] += 1
                    if tq < t:
                        stats['Q_tau_below_lower_bound'] += 1
                    if sq > s - 1 - 2 * dd:
                        stats['Q_slack_above_bound'] += 1
                    if tq == t:
                        stats['Q_tau_eq'] += 1
                        if sq != pred:
                            stats['Q_slack_mismatch'] += 1
                    if sq < 0:
                        stats['Q_negative'] += 1


def new_stats():
    return dict(graphs=0, connected_inC=0, configs=0, min_slack=10 ** 9,
                slack_hist={}, degW={}, Q=0, Q_tau_eq=0, Q_slack_mismatch=0,
                Q_negative=0, Q_tau_below_lower_bound=0, Q_slack_above_bound=0)


def random_connected_C(n, rng, maxdeg=3):
    m = rng.randint(n // 2, n - 2)
    edges = []
    deg = [0] * n
    tries = 0
    while len(edges) < m and tries < 3000:
        tries += 1
        e = tuple(sorted(rng.sample(range(n), 3)))
        if any(deg[u] >= maxdeg for u in e):
            continue
        if any(len(set(e) & set(f)) >= 2 for f in edges):
            continue
        edges.append(e)
        for u in e:
            deg[u] += 1
    return edges


if __name__ == '__main__':
    mode = sys.argv[1]
    st = new_stats()
    if mode == 'random':
        trials, seed, nmin, nmax = map(int, sys.argv[2:6])
        rng = random.Random(seed)
        for _ in range(trials):
            n = rng.randint(nmin, nmax)
            edges = random_connected_C(n, rng)
            st['graphs'] += 1
            if not edges or not connected(n, edges) or not in_C(n, edges):
                continue
            st['connected_inC'] += 1
            t, cf = configs(n, edges)
            analyse(n, edges, t, cf, st)
    else:
        for path in sys.argv[2:]:
            for (n, edges, t) in read_cell(path):
                st['graphs'] += 1
                if max(degrees(n, edges)) > 3 or not connected(n, edges):
                    continue
                st['connected_inC'] += 1
                t2, cf = configs(n, edges, t)
                analyse(n, edges, t2, cf, st)
    print(st)
