"""Referee round 3 (L002): independent CNF model of ordered midpoint patterns on n vertices (rank order 0..n-1).
Written from scratch; imports nothing from e757/, judge/ or earlier referee directories.

Variables: one per triple (i,j,k), i<j<k, meaning "x_j is the midpoint of x_i,x_k" (j = middle-ranked vertex).
Necessary conditions for the AP hypergraph of a (4,5)-set A (sorted x_0<...<x_{n-1}):
  (inj)   at most one triple per midpoint j  [weak Sidon: x_i+x_k = 2x_j = x_i'+x_k' forces {i,k}={i',k'}]
  (lin)   no two triples share two vertices  [linearity, K6]
  (K30)   no triples (i,j,k),(i',j',k') with j<j', i>=i', k>=k'  [x_i+x_k >= x_i'+x_k' would give x_j >= x_j']
  (alpha) alpha <= T: every (T+1)-subset of vertices contains a triple
Optional: (sat) every interior vertex is a midpoint; (nonsat) at least one interior vertex is not a midpoint.
No F7 constraint is encoded."""
from itertools import combinations


def build(n, T, mode):
    """mode: 'sat' (exactly one triple per interior midpoint) or 'nonsat' (<=1 per midpoint, >=1 midpoint empty)
    or 'any' (<=1 per midpoint)."""
    triples = [t for t in combinations(range(n), 3)]
    var = {t: idx + 1 for idx, t in enumerate(triples)}
    nv = len(triples)
    clauses = []
    bymid = {j: [t for t in triples if t[1] == j] for j in range(1, n - 1)}
    for j, ts in bymid.items():
        for a, b in combinations(ts, 2):
            clauses.append([-var[a], -var[b]])
        if mode == 'sat':
            clauses.append([var[t] for t in ts])
    # linearity
    for a, b in combinations(range(n), 2):
        ts = [t for t in triples if a in t and b in t]
        for s, u in combinations(ts, 2):
            if s[1] == u[1]:
                continue  # already excluded by (inj)
            clauses.append([-var[s], -var[u]])
    # K30
    nk = 0
    for s in triples:
        for u in triples:
            if s[1] < u[1] and s[0] >= u[0] and s[2] >= u[2]:
                clauses.append([-var[s], -var[u]]); nk += 1
    # alpha <= T
    for S in combinations(range(n), T + 1):
        clauses.append([var[t] for t in combinations(S, 3)])
    aux = {}
    if mode == 'nonsat':
        for j in range(1, n - 1):
            nv += 1; aux[j] = nv
            for t in bymid[j]:
                clauses.append([-nv, -var[t]])
        clauses.append([aux[j] for j in range(1, n - 1)])
    return triples, var, nv, clauses, bymid, aux
