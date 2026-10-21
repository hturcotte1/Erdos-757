"""Referee C005 round 1: own exact tools (no import of e757 or judge). Python ints only."""
import itertools, json
from fractions import Fraction

def load_claim(path):
    with open(path) as f:
        raw = json.load(f)
    pts = raw["set"]
    assert all(type(x) is int for x in pts), "non-int entry in set"
    return raw, pts

def four_subset_literal(A):
    """Literal test: every 4-subset of A has >= 5 distinct absolute differences.
    Returns (ok, number_of_4subsets, number with exactly 5 distinct, first_bad)."""
    A = sorted(A)
    cnt = 0; five = 0
    for q in itertools.combinations(A, 4):
        a, b, c, d = q
        ds = {b - a, c - a, d - a, c - b, d - b, d - c}
        cnt += 1
        k = len(ds)
        if k < 5:
            return False, cnt, five, q
        if k == 5:
            five += 1
    return True, cnt, five, None

def forbidden_sets_from_sums(A):
    """All Sidon violations by the SUM definition: pairs of distinct multisets {x<=y},{z<=w}
    with x+y=z+w. Returns the set of point-sets (frozensets of indices) of these relations."""
    n = len(A)
    by_sum = {}
    for i in range(n):
        for j in range(i, n):
            by_sum.setdefault(A[i] + A[j], []).append((i, j))
    F = set()
    for s, prs in by_sum.items():
        if len(prs) > 1:
            for p, q in itertools.combinations(prs, 2):
                F.add(frozenset(p) | frozenset(q))
    return F, by_sum

def forbidden_sets_from_diffs(A):
    """All Sidon violations by the DIFFERENCE definition: two distinct pairs (i<j),(k<l)
    with A[j]-A[i] = A[l]-A[k] > 0."""
    n = len(A)
    by_d = {}
    for i in range(n):
        for j in range(n):
            if A[j] > A[i]:
                by_d.setdefault(A[j] - A[i], []).append((i, j))
    F = set()
    for d, prs in by_d.items():
        if len(prs) > 1:
            for p, q in itertools.combinations(prs, 2):
                F.add(frozenset(p) | frozenset(q))
    return F

def is_sidon_def(S):
    """Definition: all sums x+y (x<=y in S) distinct."""
    S = sorted(S)
    sums = [S[i] + S[j] for i in range(len(S)) for j in range(i, len(S))]
    return len(sums) == len(set(sums))

def is_sidon_diff(S):
    S = sorted(S)
    ds = [S[j] - S[i] for i in range(len(S)) for j in range(i + 1, len(S))]
    return len(ds) == len(set(ds))

def greedy_order(n, F):
    """Order vertices greedily to keep the DP frontier small (heuristic; any order is correct)."""
    adj = [set() for _ in range(n)]
    for f in F:
        for u in f:
            adj[u] |= (f - {u})
    done = set(); order = []
    while len(order) < n:
        best = None
        for v in range(n):
            if v in done:
                continue
            # frontier after adding v: processed vertices with an unprocessed neighbour
            proc = done | {v}
            fr = sum(1 for u in proc if any(w not in proc for w in adj[u]))
            key = (fr, -len(adj[v] & done), len(adj[v]), v)
            if best is None or key < best[0]:
                best = (key, v)
        v = best[1]
        order.append(v); done.add(v)
    return order

def alpha_frontier_dp(n, F, order=None):
    """Exact maximum size of a subset of {0..n-1} containing no member of F (F: iterable of sets).
    Frontier DP along `order`; states keyed by the bitmask of chosen ACTIVE vertices;
    each state keeps the best count and one witness (full bitmask). Returns (alpha, witness, max_states)."""
    F = [frozenset(f) for f in F]
    if order is None:
        order = list(range(n))
    pos = {v: i for i, v in enumerate(order)}
    assert sorted(order) == list(range(n))
    last_nbr = [pos[v] for v in range(n)]
    for f in F:
        mx = max(pos[u] for u in f)
        for u in f:
            last_nbr[u] = max(last_nbr[u], mx)
    ending = [[] for _ in range(n)]
    for f in F:
        lastv = max(f, key=lambda u: pos[u])
        rest = 0
        for u in f:
            if u != lastv:
                rest |= 1 << u
        ending[pos[lastv]].append(rest)
    states = {0: (0, 0)}
    maxst = 1
    for i, v in enumerate(order):
        bit = 1 << v
        new = {}
        for mask, (val, wit) in states.items():
            # v not chosen
            cur = new.get(mask)
            if cur is None or cur[0] < val:
                new[mask] = (val, wit)
            # v chosen: no forbidden set whose last vertex is v may be completed
            if all((r & mask) != r for r in ending[i]):
                m2 = mask | bit
                cur = new.get(m2)
                if cur is None or cur[0] < val + 1:
                    new[m2] = (val + 1, wit | bit)
        # forget vertices whose last neighbour has been processed
        forget = 0
        for u in order[: i + 1]:
            if last_nbr[u] <= i:
                forget |= 1 << u
        keep = ~forget
        states = {}
        for mask, (val, wit) in new.items():
            m2 = mask & keep
            cur = states.get(m2)
            if cur is None or cur[0] < val:
                states[m2] = (val, wit)
        maxst = max(maxst, len(states))
    assert list(states.keys()) == [0]
    val, wit = states[0]
    return val, [v for v in range(n) if wit >> v & 1], maxst

def alpha_bruteforce(n, F):
    """Exhaustive over all 2^n subsets (small n only)."""
    Fm = []
    for f in F:
        m = 0
        for u in f:
            m |= 1 << u
        Fm.append(m)
    best = 0
    for S in range(1 << n):
        c = bin(S).count("1")
        if c <= best:
            continue
        if all((S & m) != m for m in Fm):
            best = c
    return best
