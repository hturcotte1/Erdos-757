#!/usr/bin/env python3
"""Referee L015 round 1, script r3: h(S_K) by the referee's own exact methods, on the INTEGER sets I_K
(built from scratch with Fractions), using only the Sidon definition (no copy/level structure, no
transfer matrix, no assumption that Sidon = 3-AP-free):
  forbidden sets = point sets {a,b,c,d} of pairs (a<=b) != (c<=d) with a+b = c+d;
  a subset is Sidon iff it contains no forbidden set.
 Method A: exact frontier (path-decomposition) dynamic programme, vertex order chosen greedily
           (min frontier); pure Python integers.
 Method B: OR-tools CP-SAT, one worker, maximise |T| s.t. sum_{v in f} x_v <= |f|-1 for every forbidden f;
           accepted only if status OPTIMAL and objective == bound.
 Method C (n <= 22): literal enumeration of ALL Sidon subsets by DFS on pairwise differences.
 Controls: method A vs brute force on random small integer sets (including non-(4,5) sets).
Usage: python3 -I r3_h.py KMAX_A KMAX_B
"""
import random
import sys
import time
from fractions import Fraction as F
from itertools import combinations

KA = int(sys.argv[1]) if len(sys.argv) > 1 else 8
KB = int(sys.argv[2]) if len(sys.argv) > 2 else 8
FAILS = []


def check(cond, msg):
    print(("PASS " if cond else "FAIL ") + msg, flush=True)
    if not cond:
        FAILS.append(msg)


O = [0, 49, 75, 83, 98, 101, 117, 119, 121, 159, 269]
r = F(18, 269)


def IK(K):
    pts = set()
    for x in O:
        v = F(x)
        for j in range(K + 1):
            pts.add(v)
            v = 101 + r * v
    sc = 269 ** K
    out = []
    for v in pts:
        w = v * sc
        assert w.denominator == 1
        out.append(int(w))
    return sorted(out)


def forbidden(I):
    n = len(I)
    bysum = {}
    for i in range(n):
        for k in range(i, n):
            bysum.setdefault(I[i] + I[k], []).append((i, k))
    Fs = set()
    for L in bysum.values():
        for p, q in combinations(L, 2):
            Fs.add(tuple(sorted(set(p) | set(q))))
    return sorted(Fs)


def order_greedy(n, Fs, inc):
    cnt = [len(f) for f in Fs]
    processed = [False] * n
    front = set()
    order = []
    for step in range(n):
        bestv, bestkey = None, None
        for v in range(n):
            if processed[v]:
                continue
            sv = set(inc[v])
            newf = 0
            for u in list(front) + [v]:
                if any(cnt[i] - (1 if i in sv else 0) > 0 for i in inc[u]):
                    newf += 1
            key = (newf, len(inc[v]), v)
            if bestkey is None or key < bestkey:
                bestv, bestkey = v, key
        v = bestv
        order.append(v)
        processed[v] = True
        for i in inc[v]:
            cnt[i] -= 1
        front.add(v)
        front = {u for u in front if any(cnt[i] > 0 for i in inc[u])}
    return order


def order_bfs(n, Fs, inc):
    adj = [set() for _ in range(n)]
    for f in Fs:
        for a in f:
            for b in f:
                if a != b:
                    adj[a].add(b)
    seen = [False] * n
    order = []
    for s0 in range(n):          # vertices are indexed in increasing integer value
        if seen[s0]:
            continue
        seen[s0] = True
        queue = [s0]
        while queue:
            v = queue.pop(0)
            order.append(v)
            for w in sorted(adj[v]):
                if not seen[w]:
                    seen[w] = True
                    queue.append(w)
    return order


def profile(n, Fs, inc, order):
    cnt = [len(f) for f in Fs]
    front = set()
    mx = 0
    for v in order:
        for i in inc[v]:
            cnt[i] -= 1
        front.add(v)
        front = {u for u in front if any(cnt[i] > 0 for i in inc[u])}
        mx = max(mx, len(front))
    return mx


def frontier_dp(n, Fs, which="best"):
    inc = [[] for _ in range(n)]
    for idx, f in enumerate(Fs):
        for v in f:
            inc[v].append(idx)
    cands = {}
    if which in ("best", "greedy"):
        o = order_greedy(n, Fs, inc)
        cands["greedy"] = (profile(n, Fs, inc, o), o)
    if which in ("best", "bfs"):
        o = order_bfs(n, Fs, inc)
        cands["bfs"] = (profile(n, Fs, inc, o), o)
    name = min(cands, key=lambda k: cands[k][0])
    order = cands[name][1]
    assert sorted(order) == list(range(n))
    cnt = [len(f) for f in Fs]
    fmask = [sum(1 << v for v in f) for f in Fs]
    front = set()
    states = {0: 0}
    maxfront = 0
    for v in order:
        vbit = 1 << v
        closing = [fmask[i] & ~vbit for i in inc[v] if cnt[i] == 1]
        new = {}
        for key, val in states.items():
            if new.get(key, -1) < val:
                new[key] = val
            okc = True
            for cm in closing:
                if key & cm == cm:
                    okc = False
                    break
            if okc:
                k1 = key | vbit
                if new.get(k1, -1) < val + 1:
                    new[k1] = val + 1
        for i in inc[v]:
            cnt[i] -= 1
        front.add(v)
        front = {u for u in front if any(cnt[i] > 0 for i in inc[u])}
        fm = sum(1 << u for u in front)
        states = {}
        for key, val in new.items():
            k = key & fm
            if states.get(k, -1) < val:
                states[k] = val
        maxfront = max(maxfront, len(front))
    assert all(c == 0 for c in cnt)
    return max(states.values()), "%s:%d" % (name, maxfront)


def brute_max_sidon(I):
    """all Sidon subsets by DFS on differences (definition); returns (max size, number of Sidon subsets incl. empty)"""
    n = len(I)
    best = [0]
    count = [0]

    def rec(i, chosen, diffs):
        count[0] += 1
        if len(chosen) > best[0]:
            best[0] = len(chosen)
        for k in range(i, n):
            x = I[k]
            nd = [x - c for c in chosen]
            if len(set(nd)) == len(nd) and not (set(nd) & diffs):
                rec(k + 1, chosen + [x], diffs | set(nd))

    rec(0, [], set())
    return best[0], count[0]


t0 = time.time()
# ---------------- controls for method A
random.seed(757)
okc = True
for trial in range(300):
    n = random.randint(4, 13)
    I = sorted(random.sample(range(0, 40), n))
    a, _ = frontier_dp(n, forbidden(I), "greedy")
    a2, _ = frontier_dp(n, forbidden(I), "bfs")
    b, _ = brute_max_sidon(I)
    if not (a == a2 == b):
        okc = False
        print("   control mismatch", I, a, b)
check(okc, "control: frontier DP == brute force on 300 random integer sets (n 4..13, values < 40; %.1fs)" % (time.time() - t0))

# ---------------- method C: literal enumeration for n <= 22
for K in (0, 1):
    I = IK(K)
    b, c = brute_max_sidon(I)
    check(b == 7 + 5 * K, "method C (literal DFS over all Sidon subsets): K=%d n=%d h=%d (Sidon subsets incl. empty: %d; %.1fs)" % (K, len(I), b, c, time.time() - t0))

# ---------------- method A
for K in range(KA + 1):
    I = IK(K)
    Fs = forbidden(I)
    sizes = sorted(set(len(f) for f in Fs))
    h, mf = frontier_dp(len(I), Fs)
    check(h == 7 + 5 * K, "method A (frontier DP): K=%d n=%d forbidden sets=%d (sizes %s) h=%d =? 7+5K=%d (order:max frontier %s; %.1fs)" %
          (K, len(I), len(Fs), sizes, h, 7 + 5 * K, mf, time.time() - t0))

# ---------------- method B
try:
    from ortools.sat.python import cp_model
    for K in range(KB + 1):
        I = IK(K)
        Fs = forbidden(I)
        m = cp_model.CpModel()
        x = [m.NewBoolVar("x%d" % i) for i in range(len(I))]
        for f in Fs:
            m.Add(sum(x[v] for v in f) <= len(f) - 1)
        m.Maximize(sum(x))
        s = cp_model.CpSolver()
        s.parameters.num_search_workers = 1
        s.parameters.max_time_in_seconds = 600
        st = s.Solve(m)
        obj, bd = s.ObjectiveValue(), s.BestObjectiveBound()
        sol = [I[i] for i in range(len(I)) if s.Value(x[i])] if st in (cp_model.OPTIMAL, cp_model.FEASIBLE) else []
        sm = [a + b for i, a in enumerate(sol) for b in sol[i:]]
        okw = len(sm) == len(set(sm))
        check(st == cp_model.OPTIMAL and round(obj) == round(bd) == 7 + 5 * K and okw and len(sol) == 7 + 5 * K,
              "method B (CP-SAT, 1 worker): K=%d n=%d status=%s obj=%s bound=%s, solution Sidon by definition: %s (%.1fs)" %
              (K, len(I), s.StatusName(st), obj, bd, okw, time.time() - t0))
except ImportError:
    print("ortools not available")

print("SUMMARY: %d failures" % len(FAILS))
for f in FAILS:
    print("  FAILED:", f)
