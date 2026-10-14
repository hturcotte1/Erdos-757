"""Independent re-verification of every witness in witnesses.json (op and real classes).
Checks: edges i<j<k<n; unique midpoint; linearity; F7-free; monotone (K30); no medial triangle (K31);
alpha by brute force over all subsets (bitmask) == claimed; m == claimed; HY slack >= 0;
for real: integer set strictly increasing, edge list == set of all 3-APs of the set, (4,5)-set check."""
import json, itertools, sys, os
repo = "/home/user/Erdos-757"; sys.path.insert(0, repo)
from e757.cpsat_model import constraint_violations, load_cores, is_f7_free
from e757.core import is_45_set
here = os.path.dirname(os.path.abspath(__file__))
W = json.load(open(here + "/witnesses.json"))
cores = load_cores(repo + "/data/forbidden_ordered_n7.json", repo + "/data/forbidden_ordered_n8.json")

def alpha_brute(n, edges):
    masks = [(1 << i) | (1 << j) | (1 << k) for i, j, k in edges]
    best = 0
    for S in range(1 << n):
        c = bin(S).count("1")
        if c > best and all(S & mk != mk for mk in masks):
            best = c
    return best

def check(cls, rec):
    n, m, edges = rec["n"], rec["m"], [tuple(e) for e in rec["edges"]]
    assert len(edges) == m, "m"
    assert all(0 <= i < j < k < n for i, j, k in edges)
    assert len({j for _, j, _ in edges}) == m, "midpoint"
    for e, f in itertools.combinations(edges, 2):
        assert len(set(e) & set(f)) <= 1, "linear"
    assert is_f7_free(edges)
    # own K30
    for (i, j, k) in edges:
        for (a, b, c) in edges:
            if i <= a and k <= c and (i, k) != (a, c): assert j < b, "K30"
    # own K31: three edges, 6 vertices, pairwise sharing one vertex (3 distinct shared vertices),
    # all three midpoints private (not shared)
    for E3 in itertools.combinations(edges, 3):
        S = [set(e) for e in E3]
        if len(set().union(*S)) != 6: continue
        sh = [S[0] & S[1], S[0] & S[2], S[1] & S[2]]
        if all(len(x) == 1 for x in sh):
            shared = set().union(*sh)
            if len(shared) == 3:
                assert any(e[1] in shared for e in E3), "K31 medial triangle"
    assert not constraint_violations(n, edges, cores=cores), "violations"
    a = alpha_brute(n, edges)
    assert a == rec["alpha"], ("alpha", a, rec["alpha"])
    s = 5 * n + 3 * m - 17 * (n - a)
    assert s >= 0 and s == rec["slack"]
    if cls == "real":
        X = rec["set"]
        assert all(X[i] < X[i+1] for i in range(len(X)-1)) and len(X) == n
        aps = {(i, j, k) for i, j, k in itertools.combinations(range(n), 3) if X[i] + X[k] == 2 * X[j]}
        assert aps == set(edges), "AP set"
        assert is_45_set(X)
for cls in ("op", "real"):
    c = 0
    for key, rec in W[cls].items():
        check(cls, rec); c += 1
    print(cls, "verified", c, "witnesses")
