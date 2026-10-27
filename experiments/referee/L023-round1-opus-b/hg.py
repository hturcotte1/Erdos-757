"""Referee L023 (opus-b): own hypergraph toolkit (no code from e757/, judge/, the engine or the prover).
 - canon(n, edges): exact canonical form of a 3-graph by individualization-refinement, the lexicographically least leaf certificate
   (the search tree is defined by isomorphism-invariant rules, so the set of leaf certificates is an invariant, and each certificate is
   a relabelling of the graph: equal forms <=> isomorphic);
 - tau(n, edges): exact transversal number (branching on an uncovered edge);
 - min_covers(n, edges, k): all covers of size exactly k (k = tau), as bitmasks;
 - has_F7, p3 (via Lemma P: e(S) <= |S|-2 for all |S| >= 2 <=> for every vertex pair {u,w} the edges have distinct representatives
   avoiding u and w; proof in the review), connected, linear.
"""
import itertools

def parse(line):
    import re
    return [tuple(map(int, t.split(','))) for t in re.findall(r'\((\d+,\d+,\d+)\)', line)]

def refine(n, inc, others, col):
    """inc[v] = list of edge indices; others[v] = list of (a,b) other vertices per incident edge. col: list of ints (canonical)."""
    ncol = len(set(col))
    while True:
        sig = []
        for v in range(n):
            s = sorted(tuple(sorted((col[a], col[b]))) for (a, b) in others[v])
            sig.append((col[v], tuple(s)))
        keys = sorted(set(sig))
        idx = {k: i for i, k in enumerate(keys)}
        new = [idx[s] for s in sig]
        if len(keys) == ncol:
            return new
        col = new; ncol = len(keys)

def canon(n, edges, leaf_cap=200000):
    others = [[] for _ in range(n)]
    for (a, b, c) in edges:
        others[a].append((b, c)); others[b].append((a, c)); others[c].append((a, b))
    inc = None
    col0 = refine(n, inc, others, [0] * n)
    best = [None]; leaves = [0]
    def rec(col):
        if len(set(col)) == n:
            leaves[0] += 1
            cert = tuple(sorted(tuple(sorted((col[a], col[b], col[c]))) for (a, b, c) in edges))
            if best[0] is None or cert < best[0]: best[0] = cert
            if leaves[0] > leaf_cap: raise RuntimeError('leaf cap')
            return
        # target cell: smallest colour value whose class has size > 1
        cnt = {}
        for x in col: cnt[x] = cnt.get(x, 0) + 1
        c = min(k for k, v in cnt.items() if v > 1)
        for v in range(n):
            if col[v] == c:
                ind = [2 * col[x] + (1 if (col[x] == c and x != v) else 0) for x in range(n)]
                # renormalize to 0..k-1 preserving order
                ks = sorted(set(ind)); ix = {k: i for i, k in enumerate(ks)}
                rec(refine(n, inc, others, [ix[x] for x in ind]))
    rec(col0)
    return best[0], leaves[0]

def tau(n, edges):
    E = [(1 << a) | (1 << b) | (1 << c) for (a, b, c) in edges]
    best = [n]
    def rec(T, size):
        if size >= best[0]: return
        for e in E:
            if not (e & T):
                for v in range(n):
                    if e >> v & 1: rec(T | (1 << v), size + 1)
                return
        best[0] = size
    rec(0, 0)
    return best[0]

def covers_upto(n, edges, k):
    """all inclusion-minimal covers of size <= k (as bitmasks); for k = tau these are all covers of size tau."""
    E = [(1 << a) | (1 << b) | (1 << c) for (a, b, c) in edges]
    out = set()
    def rec(T, size):
        for e in E:
            if not (e & T):
                if size == k: return
                for v in range(n):
                    if e >> v & 1: rec(T | (1 << v), size + 1)
                return
        out.add(T)
    rec(0, 0)
    # keep minimal ones only
    res = [T for T in out if not any((S != T and (S & T) == S) for S in out)]
    return res

def linear(edges):
    seen = set()
    for (a, b, c) in edges:
        for p in ((a, b), (a, c), (b, c)):
            q = tuple(sorted(p))
            if q in seen: return False
            seen.add(q)
    return True

def connected(n, edges):
    adj = [[] for _ in range(n)]
    for (a, b, c) in edges:
        adj[a] += [b, c]; adj[b] += [a, c]; adj[c] += [a, b]
    seen = {0}; st = [0]
    while st:
        v = st.pop()
        for w in adj[v]:
            if w not in seen: seen.add(w); st.append(w)
    return len(seen) == n

def has_F7(n, edges):
    """F7 = {012,034,056,135,246}: centre 0 with three edges whose other vertices form pairs P1,P2,P3, and two further disjoint edges,
    each containing exactly one vertex of each pair (so together they cover the six).  Searched directly."""
    inc = [[] for _ in range(n)]
    for e in edges:
        for v in e: inc[v].append(e)
    Es = set(tuple(sorted(e)) for e in edges)
    for c0 in range(n):
        if len(inc[c0]) < 3: continue
        for trip in itertools.combinations(inc[c0], 3):
            P = [tuple(v for v in e if v != c0) for e in trip]
            if len(set(P[0] + P[1] + P[2])) != 6: continue
            trans = []
            for x in P[0]:
                for y in P[1]:
                    for z in P[2]:
                        if tuple(sorted((x, y, z))) in Es: trans.append({x, y, z})
            for s, t in itertools.combinations(trans, 2):
                if not (s & t): return True
    return False

def p3(n, edges):
    """Lemma P: for every pair {u,w} the edges have an SDR in V minus {u,w}.  Implemented with one base matching and re-augmentation."""
    m = len(edges)
    if m == 0: return True
    if m > n - 2: return False
    def augment(i, match_v, banned, seen):
        for v in edges[i]:
            if v in banned or v in seen: continue
            seen.add(v)
            j = match_v.get(v)
            if j is None or augment(j, match_v, banned, seen):
                match_v[v] = i
                return True
        return False
    base = {}
    for i in range(m):
        if not augment(i, base, (), set()): return False
    for u in range(n):
        for w in range(u + 1, n):
            mv = dict(base)
            banned = (u, w)
            freed = [mv.pop(x) for x in banned if x in mv]
            for i in freed:
                if not augment(i, mv, banned, set()): return False
    return True

def p3_brute(n, edges):
    for r in range(2, n + 1):
        for S in itertools.combinations(range(n), r):
            Ss = set(S)
            if sum(1 for e in edges if Ss.issuperset(e)) > r - 2: return False
    return True
