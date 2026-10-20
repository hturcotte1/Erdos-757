#!/usr/bin/env python3
"""L015 / C4: h(S_K) by computations that do not use the copy structure or the transfer matrix.
 (a) K <= 1: literal brute force from the Sidon definition: no (8+5K)-subset of S_K is Sidon (all subsets enumerated),
     and the explicit T_K (Step 6) is a Sidon subset of size 7+5K.
 (b) K <= KMAX: a generic exact maximum-independent-set solver for the 3-AP hypergraph of the integer set
     (hyperedges recomputed from all pair sums; branching on a maximum-degree vertex, splitting into connected
     components, memoisation of residual sub-hypergraphs).  Exact for any hypergraph.
Run:  python3 -I v4_h.py KMAX
"""
import sys
import time
from itertools import combinations

sys.setrecursionlimit(100000)
O = [0, 49, 75, 83, 98, 101, 117, 119, 121, 159, 269]
USTAR = [0, 98, 101, 117, 119, 159, 269]


def N(j, x):
    v = x
    for i in range(1, j + 1):
        v = 101 * 269 ** i + 18 * v
    return v


def S_int(K, base=O):
    return sorted({269 ** (K - j) * N(j, x) for j in range(K + 1) for x in base})


def is_sidon(U):
    s = [a + b for i, a in enumerate(U) for b in U[i:]]
    return len(s) == len(set(s))


def ap_edges(A):
    S = set(A)
    return [frozenset((a, (a + c) // 2, c)) for a, c in combinations(sorted(A), 2) if (a + c) % 2 == 0 and (a + c) // 2 in S]


MEMO = {}
CALLS = [0]


def components(V, E):
    adj = {v: set() for v in V}
    for e in E:
        for u in e:
            adj[u] |= e
    seen, comps = set(), []
    for v in V:
        if v in seen:
            continue
        stack, comp = [v], set()
        seen.add(v)
        while stack:
            u = stack.pop()
            comp.add(u)
            for w in adj[u]:
                if w not in seen:
                    seen.add(w)
                    stack.append(w)
        comps.append(frozenset(comp))
    return [(c, frozenset(e for e in E if e <= c)) for c in comps]


def solve(V, E):
    """max |X|, X subset of V, containing no e in E (E: frozensets of size 1..3 inside V)."""
    CALLS[0] += 1
    forced_out = {next(iter(e)) for e in E if len(e) == 1}
    if forced_out:
        V = V - forced_out
        E = frozenset(e for e in E if not (e & forced_out))
    # drop constraints implied by smaller ones (e superset of f): keeps the memo small
    E = frozenset(e for e in E if not any(f < e for f in E))
    used = set().union(*E) if E else set()
    free = len(V - used)
    V = frozenset(used)
    if not E:
        return free
    total = free
    for Vc, Ec in components(V, E):
        key = (Vc, Ec)
        if key in MEMO:
            total += MEMO[key]
            continue
        deg = {}
        for e in Ec:
            for u in e:
                deg[u] = deg.get(u, 0) + 1
        v = max(sorted(Vc), key=lambda u: deg.get(u, 0))
        out_ = solve(Vc - {v}, frozenset(e for e in Ec if v not in e))
        in_ = 1 + solve(Vc - {v}, frozenset((e - {v}) if v in e else e for e in Ec))
        val = max(out_, in_)
        MEMO[key] = val
        total += val
    return total


def main():
    KMAX = int(sys.argv[1])
    # (a) literal brute force, K = 0, 1
    for K in (0, 1):
        A = S_int(K)
        T = S_int(K, USTAR)
        h = 7 + 5 * K
        assert len(T) == h and set(T) <= set(A) and is_sidon(T)
        t0 = time.time()
        cnt = 0
        found = False
        for U in combinations(A, h + 1):
            cnt += 1
            if is_sidon(U):
                found = True
                break
        print(f"(a) K={K} n={len(A)}: T_K Sidon of size {h}; all {cnt} subsets of size {h+1} checked by definition: Sidon one found = {found}  ({time.time()-t0:.1f}s)", flush=True)
        assert not found
    # (b) generic exact solver
    for K in range(KMAX + 1):
        A = S_int(K)
        E = ap_edges(A)
        MEMO.clear()
        CALLS[0] = 0
        t0 = time.time()
        a = solve(frozenset(A), frozenset(E))
        print(f"(b) K={K} n={len(A)} APs={len(E)}: alpha = {a}  (expected 7+5K = {7+5*K}; {CALLS[0]} calls, {len(MEMO)} memo entries, {time.time()-t0:.1f}s)", flush=True)
        assert a == 7 + 5 * K
    print("ALL h CHECKS OK")


if __name__ == "__main__":
    main()
