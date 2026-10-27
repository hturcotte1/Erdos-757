"""(L023) Independent verifier of membership in the class C (no code shared with filt, pyverify or the engine).
 C: (P1) linear, (P2) F7-free (F7 = {012,034,056,135,246}), (P3) e(S) <= |S|-2 for every vertex set S with |S| >= 2.
 (P3) is tested through Lemma P (L023, Step 2.2): (P3) <=> for every pair {u,w} of vertices the edges have a system of distinct
 representatives avoiding u and w (Hall); the matching is found by augmenting paths.
 tau by exhaustive branching on the first uncovered edge (returns a minimum cover).
 usage: python3 verify_c.py  (unit tests)"""
import itertools
def linear(E):
    seen = {}
    for i, e in enumerate(E):
        for p in itertools.combinations(sorted(e), 2):
            if p in seen: return False
            seen[p] = i
    return True
def has_F7(E, n):
    """assumes E linear. F7 present <=> some vertex v with three edges {v,a_i,b_i} and two edges T, T' with
    T u T' = {a1,b1,a2,b2,a3,b3}, |T n {a_i,b_i}| = 1 = |T' n {a_i,b_i}| for i = 1,2,3."""
    S = set(frozenset(e) for e in E)
    inc = [[] for _ in range(n)]
    for e in E:
        for v in e: inc[v].append(e)
    for v in range(n):
        for e1, e2, e3 in itertools.combinations(inc[v], 3):
            P = [tuple(x for x in e if x != v) for e in (e1, e2, e3)]
            for c in itertools.product((0, 1), repeat=3):
                T = frozenset(P[i][c[i]] for i in range(3)); T2 = frozenset(P[i][1 - c[i]] for i in range(3))
                if T in S and T2 in S: return True
    return False
def sdr_avoiding(E, n, forbid):
    """True iff the edges have distinct representatives (rep(e) in e) none in forbid (augmenting paths)."""
    match = {}   # vertex -> edge index
    def aug(i, seen):
        for v in E[i]:
            if v in forbid or v in seen: continue
            seen.add(v)
            if v not in match or aug(match[v], seen):
                match[v] = i; return True
        return False
    return all(aug(i, set()) for i in range(len(E)))
def p3(E, n):
    if not E: return True
    return all(sdr_avoiding(E, n, {u, w}) for u, w in itertools.combinations(range(n), 2))
def p3_brute(E, n):
    """direct definition over all vertex subsets S (only for small n)."""
    for r in range(2, n + 1):
        for S in itertools.combinations(range(n), r):
            s = set(S)
            if sum(1 for e in E if set(e) <= s) > r - 2: return False
    return True
def connected(E, n):
    adj = [set() for _ in range(n)]
    for e in E:
        for v in e: adj[v] |= set(e) - {v}
    seen = {0}; st = [0]
    while st:
        v = st.pop()
        for w in adj[v]:
            if w not in seen: seen.add(w); st.append(w)
    return len(seen) == n
def tau_exact(E, n):
    """minimum vertex cover of the 3-graph by iterative deepening + branching on the first uncovered edge."""
    masks = [sum(1 << v for v in e) for e in E]
    def rec(cov, k):
        for mk in masks:
            if not (mk & cov):
                if k == 0: return None
                for v in range(n):
                    if (mk >> v) & 1:
                        r = rec(cov | (1 << v), k - 1)
                        if r is not None: return r
                return None
        return cov
    for k in range(0, len(E) + 1):
        r = rec(0, k)
        if r is not None: return k, [v for v in range(n) if (r >> v) & 1]
def in_C(E, n):
    if any(len(set(e)) != 3 or not all(0 <= v < n for v in e) for e in E): return False, 'labels'
    if len(set(frozenset(e) for e in E)) != len(E): return False, 'repeated edge'
    if not linear(E): return False, 'not linear'
    if has_F7(E, n): return False, 'contains F7'
    if not p3(E, n): return False, 'violates (P3)'
    return True, 'in C'
def degrees(E, n):
    d = [0] * n
    for e in E:
        for v in e: d[v] += 1
    return d
if __name__ == '__main__':
    F7 = [(0, 1, 2), (0, 3, 4), (0, 5, 6), (1, 3, 5), (2, 4, 6)]
    assert has_F7(F7, 7) and in_C(F7, 7) == (False, 'contains F7')
    perm = [3, 6, 0, 5, 1, 4, 2]
    F7r = [tuple(perm[v] for v in e) for e in F7] + [(7, 8, 0)]
    assert in_C(F7r, 9)[1] == 'contains F7'
    fano = [(0, 1, 2), (0, 3, 4), (0, 5, 6), (1, 3, 5), (1, 4, 6), (2, 3, 6), (2, 4, 5)]
    assert linear(fano) and not p3(fano, 7) and not p3_brute(fano, 7)
    grid = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8)]
    assert in_C(grid, 9) == (True, 'in C') and tau_exact(grid, 9)[0] == 3 and p3_brute(grid, 9)
    assert not linear([(0, 1, 2), (0, 1, 3)])
    assert not connected([(0, 1, 2), (3, 4, 5)], 6)
    # (P3) by matching agrees with the definition on 300 random linear 3-graphs on 9 vertices
    import random
    rnd = random.Random(23); agree = 0; viol = 0
    for _ in range(300):
        n = 9; E = []
        for t in rnd.sample(list(itertools.combinations(range(n), 3)), rnd.randint(1, 60)):
            if linear(E + [t]): E.append(t)
        a, b = p3(E, n), p3_brute(E, n); assert a == b; agree += 1; viol += (not a)
    print('unit tests OK; (P3) matching == brute force on %d random linear graphs (%d violate (P3))' % (agree, viol))
