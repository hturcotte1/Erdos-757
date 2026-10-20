#!/usr/bin/env python3
"""Independent referee verifier for claim C003 (round 1).

Does NOT import e757 or judge.  Everything exact (int / Fraction).

Checks
  1. strict JSON parsing (no floats), distinctness, n
  2. (4,5): every 4-subset has >= 5 distinct positive differences  (and literal |B-B| >= 11)
  3. relation census straight from the Sidon definition:
        every pair of distinct 2-multisets {a,b} != {c,d} of A with a+b = c+d
     (cross-checked against a census of equal positive differences)
  4. witness: subset of A, size, Sidon by sums AND by differences
  5. h(A) = max size of a subset containing no "forbidden union" {a,b,c,d} of a relation,
     by a generic exact frontier dynamic program (any hypergraph, any vertex order),
     run with two different vertex orders; the optimal set is reconstructed and
     re-checked as Sidon from the definition
  6. exact ratio h/n vs 4/7 with Fractions
"""
import functools
import itertools
import json
import resource
import sys
import time
from collections import defaultdict
from fractions import Fraction

resource.setrlimit(resource.RLIMIT_AS, (4 * 1024 ** 3, 4 * 1024 ** 3))  # 4 GB cap, shared machine
print = functools.partial(print, flush=True)  # noqa: A001


def strict_load(path):
    def no_float(s):
        raise ValueError(f"float literal {s!r} in claim file")

    def no_const(s):
        raise ValueError(f"constant {s!r} in claim file")

    with open(path) as fh:
        return json.load(fh, parse_float=no_float, parse_constant=no_const)


def to_exact(x):
    if isinstance(x, bool):
        raise ValueError("bool in set")
    if isinstance(x, int):
        return Fraction(x)
    if isinstance(x, str):
        return Fraction(x)
    raise ValueError(f"unsupported entry {x!r} ({type(x)})")


def check_45(A):
    """Return (ok, bad_quadruple, n_checked). Literal check on |B-B| and on positive diffs."""
    n = len(A)
    D = [[abs(A[i] - A[j]) for j in range(n)] for i in range(n)]
    cnt = 0
    for a, b, c, d in itertools.combinations(range(n), 4):
        cnt += 1
        s = {D[a][b], D[a][c], D[a][d], D[b][c], D[b][d], D[c][d]}
        if len(s) < 5:
            return False, (A[a], A[b], A[c], A[d]), cnt
    return True, None, cnt


def check_45_literal_BminusB(A, limit=None):
    """Literal |B - B| >= 11 (B-B includes 0 and negatives)."""
    cnt = 0
    for q in itertools.combinations(A, 4):
        cnt += 1
        if len({x - y for x in q for y in q}) < 11:
            return False, q, cnt
        if limit and cnt >= limit:
            break
    return True, None, cnt


def sum_census(A):
    """All pairs of distinct multisets {i<=j} with equal sums. Returns list of (pair1, pair2)."""
    n = len(A)
    by_sum = defaultdict(list)
    for i in range(n):
        for j in range(i, n):
            by_sum[A[i] + A[j]].append((i, j))
    rels = []
    for s, lst in by_sum.items():
        if len(lst) >= 2:
            for p, q in itertools.combinations(lst, 2):
                rels.append((p, q))
    return rels, by_sum


def diff_census(A):
    """All pairs of distinct ordered pairs (i<j) with equal positive difference."""
    n = len(A)
    by_diff = defaultdict(list)
    for i in range(n):
        for j in range(i + 1, n):
            by_diff[A[j] - A[i]].append((i, j))
    rels = []
    for d, lst in by_diff.items():
        if len(lst) >= 2:
            for p, q in itertools.combinations(lst, 2):
                rels.append((p, q))
    return rels


def is_sidon_sums(S):
    S = sorted(S)
    sums = [S[i] + S[j] for i in range(len(S)) for j in range(i, len(S))]
    return len(sums) == len(set(sums))


def is_sidon_diffs(S):
    S = sorted(S)
    diffs = [S[j] - S[i] for i in range(len(S)) for j in range(i + 1, len(S))]
    return len(diffs) == len(set(diffs))


class TooWide(Exception):
    pass


def frontier_dp(n, edges, order, cap=3_000_000):
    """Exact max |T|, T subset of range(n), containing no edge (edges: iterables of vertices).

    Processes vertices in `order`; a state is the set (bitmask) of chosen vertices that are
    still 'active' (some edge through them is not yet complete).  Returns
    (best, a best full set as bitmask, max frontier width, max #states)."""
    pos = {v: i for i, v in enumerate(order)}
    assert sorted(pos) == list(range(n))
    emask = []
    by_last = defaultdict(list)
    last = {v: pos[v] for v in range(n)}
    for e in edges:
        e = tuple(sorted(set(e)))
        m = 0
        for v in e:
            m |= 1 << v
        lp = max(pos[v] for v in e)
        lastv = order[lp]
        by_last[lp].append(m & ~(1 << lastv))  # the other vertices
        for v in e:
            last[v] = max(last[v], lp)
        emask.append(m)
    retire_at = defaultdict(int)
    for v in range(n):
        retire_at[last[v]] |= 1 << v
    states = {0: (0, 0)}  # active chosen mask -> (count, full chosen mask)
    active = 0
    maxw = 0
    maxs = 1
    for i, v in enumerate(order):
        bit = 1 << v
        others = by_last[i]
        keep = ~retire_at[i]
        new = {}
        for st, (val, full) in states.items():
            # skip v
            k = st & keep
            cur = new.get(k)
            if cur is None or cur[0] < val:
                new[k] = (val, full)
            # take v (allowed iff no edge ending at v has all other vertices chosen)
            ok = True
            for om in others:
                if st & om == om:
                    ok = False
                    break
            if ok:
                k2 = (st | bit) & keep
                cur = new.get(k2)
                if cur is None or cur[0] < val + 1:
                    new[k2] = (val + 1, full | bit)
        states = new
        if len(states) > cap:
            raise TooWide(f"more than {cap} states at step {i}")
        active = (active | bit) & keep
        maxw = max(maxw, bin(active).count("1"))
        maxs = max(maxs, len(states))
    assert list(states) == [0] or all(k == 0 for k in states), states.keys()
    best, full = max(states.values())
    return best, full, maxw, maxs


def greedy_order(n, edges):
    """Greedy min-frontier vertex order (generic heuristic)."""
    inc = defaultdict(set)
    for e in edges:
        for v in e:
            inc[v].add(tuple(sorted(e)))
    done = set()
    order = []
    remaining = set(range(n))

    def frontier_after(cand):
        d2 = done | {cand}
        f = 0
        for u in d2:
            if any(any(w not in d2 for w in e) for e in inc[u]):
                f += 1
        return f

    while remaining:
        best = min(sorted(remaining), key=lambda c: (frontier_after(c), c))
        order.append(best)
        done.add(best)
        remaining.discard(best)
    return order


def bfs_order(n, edges, root):
    adj = defaultdict(set)
    for e in edges:
        for u in e:
            for w in e:
                if u != w:
                    adj[u].add(w)
    seen = [root]
    seenset = {root}
    k = 0
    while k < len(seen):
        u = seen[k]
        k += 1
        for w in sorted(adj[u]):
            if w not in seenset:
                seenset.add(w)
                seen.append(w)
    rest = [v for v in range(n) if v not in seenset]
    return seen + rest


def main():
    path = sys.argv[1]
    t0 = time.time()
    claim = strict_load(path)
    print("claim id:", claim.get("id"), "| type:", claim.get("type"))
    raw = claim["set"]
    print("entry types:", sorted({type(x).__name__ for x in raw}))
    vals = [to_exact(x) for x in raw]
    n = len(vals)
    assert len(set(vals)) == n, "DUPLICATES"
    A = sorted(vals)
    assert all(x.denominator == 1 for x in A)
    A = [int(x) for x in A]
    print(f"n = {n}, distinct = True, min = {A[0]}, max = {A[-1]}")
    print("min gap between consecutive points:", min(A[i + 1] - A[i] for i in range(n - 1)))

    # 2. (4,5)
    t = time.time()
    ok, bad, cnt = check_45(A)
    print(f"(4,5) check (>=5 distinct positive differences): ok={ok} bad={bad} checked={cnt} "
          f"[{time.time() - t:.1f}s]")
    t = time.time()
    ok2, bad2, cnt2 = check_45_literal_BminusB(A)
    print(f"(4,5) literal |B-B|>=11: ok={ok2} bad={bad2} checked={cnt2} [{time.time() - t:.1f}s]")

    # 3. census
    rels, by_sum = sum_census(A)
    forb = set()
    kinds = defaultdict(int)
    for p, q in rels:
        u = frozenset(p) | frozenset(q)
        kinds[len(u)] += 1
        forb.add(u)
    print(f"sum census: {len(rels)} relations a+b=c+d with distinct multisets; union sizes {dict(kinds)}; "
          f"max multiplicity of a sum = {max(len(v) for v in by_sum.values())}")
    drels = diff_census(A)
    dforb = set()
    for p, q in drels:
        dforb.add(frozenset(p) | frozenset(q))
    print(f"difference census: {len(drels)} equal-difference pair-pairs; same forbidden unions as sums: "
          f"{dforb == forb}")
    # weak Sidon: all x+y with x<y distinct
    ws = [A[i] + A[j] for i in range(n) for j in range(i + 1, n)]
    print("weak Sidon (x<y sums distinct):", len(ws) == len(set(ws)))
    # the 3-AP list
    aps = sorted(tuple(sorted(u)) for u in forb if len(u) == 3)
    print("number of 3-APs:", len(aps))
    for u in forb:
        if len(u) == 3:
            a, b, c = sorted(u)
            assert A[a] + A[c] == 2 * A[b], u
    # linearity
    lin = all(len(set(e) & set(f)) <= 1 for e, f in itertools.combinations(aps, 2))
    print("3-AP hypergraph linear:", lin)
    mids = {e[1] for e in aps}
    print("number of distinct midpoints m =", len(mids), "(n-2 =", n - 2, ")")
    deg = defaultdict(int)
    for e in aps:
        for v in e:
            deg[v] += 1
    hist = defaultdict(int)
    for v in range(n):
        hist[deg[v]] += 1
    print("AP-degree histogram {degree: #vertices}:", dict(sorted(hist.items())))

    # 4. witness
    W = claim.get("witness_sidon_subset")
    if W is not None:
        Wv = [int(to_exact(x)) for x in W]
        print(f"witness: size={len(Wv)}, distinct={len(set(Wv)) == len(Wv)}, subset={set(Wv) <= set(A)}, "
              f"Sidon(sums)={is_sidon_sums(Wv)}, Sidon(diffs)={is_sidon_diffs(Wv)}")
    print("claimed_h:", claim.get("claimed_h"))

    # 5. exact h by frontier DP, two orders
    edges = [tuple(sorted(u)) for u in forb]
    results = []
    for name, order in [("greedy min-frontier order", greedy_order(n, edges)),
                        ("BFS order from the minimum", bfs_order(n, edges, 0)),
                        ("BFS order from the maximum", bfs_order(n, edges, n - 1)),
                        ("value order", list(range(n)))]:
        t = time.time()
        try:
            best, full, maxw, maxs = frontier_dp(n, edges, order)
        except TooWide as exc:
            print(f"frontier DP [{name}]: skipped ({exc}) [{time.time() - t:.1f}s]")
            continue
        T = [A[i] for i in range(n) if full >> i & 1]
        okT = len(T) == best and is_sidon_sums(T) and is_sidon_diffs(T)
        print(f"frontier DP [{name}]: h = {best}; max frontier width {maxw}; max #states {maxs}; "
              f"reconstructed optimum is Sidon by definition: {okT} [{time.time() - t:.1f}s]")
        results.append(best)
    assert len(results) >= 2 and len(set(results)) == 1, results
    h = results[0]
    r = Fraction(h, n)
    print(f"h/n = {r} = {float(r):.6f};  4/7 = {float(Fraction(4, 7)):.6f};  h/n < 4/7: {r < Fraction(4, 7)}"
          f"  (7h = {7 * h} vs 4n = {4 * n})")
    print(f"claimed_h == h: {claim.get('claimed_h') == h}")
    print(f"total {time.time() - t0:.1f}s")


if __name__ == "__main__":
    main()
