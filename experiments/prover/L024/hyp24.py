"""L024 library: own exact routines (membership in C_3, transversals, automorphisms, deficiency certificates).
Independent of kt.py except where stated (pieces are read from L021's closure_results.json).
Hypergraphs: vertex set 0..n-1, edges = tuples of 3 ints. Exact integers only."""
import json, itertools, sys
sys.setrecursionlimit(100000)
CN, CM, CT, CE = 27, 35, 132, 35

def load_pieces():
    D = json.load(open('/home/user/Erdos-757/experiments/prover/L021/closure_results.json'))
    out = []
    for P in D['pieces']:
        edges = [tuple(sorted(e)) for e in P['edges']]
        out.append(dict(name=P['name'], n=P['n'], m=P['m'], edges=edges))
    for P in out:
        P['tau'] = tau(P['n'], P['edges'])
        P['W'] = -(CN * P['n'] + CM * P['m'] - CT * P['tau'])
        P['deg'] = degrees(P['n'], P['edges'])
        P['mts'] = min_transversals(P['n'], P['edges'], P['tau'])
    return out

def degrees(n, edges):
    d = [0] * n
    for e in edges:
        for x in e: d[x] += 1
    return d

def emasks(edges):
    return [(1 << a) | (1 << b) | (1 << c) for (a, b, c) in edges]

def tau(n, edges):
    em = emasks(edges)
    best = [len(em)]
    def lb(rem):
        used = 0; k = 0
        for e in rem:
            if not e & used: used |= e; k += 1
        return k
    def rec(rem, k):
        if not rem:
            if k < best[0]: best[0] = k
            return
        if k + lb(rem) >= best[0]: return
        # branch on the edge whose vertices have the fewest... just first edge
        e = rem[0]; m = e
        while m:
            b = m & -m; m ^= b
            rec([f for f in rem if not f & b], k + 1)
    rec(em, 0)
    return best[0]

def min_transversals(n, edges, t):
    """all transversals of size t (as bitmasks); t must be tau."""
    em = emasks(edges)
    res = []
    def rec(rem, chosen, k, forb):
        if not rem:
            res.append(chosen); return
        if k == t: return
        # lower bound by greedy disjoint edges
        used = 0; lbk = 0
        for e in rem:
            if not e & used: used |= e; lbk += 1
        if k + lbk > t: return
        e = rem[0]; cand = e & ~forb; f2 = forb
        while cand:
            b = cand & -cand; cand ^= b
            rec([f for f in rem if not f & b], chosen | b, k + 1, f2)
            f2 |= b
    rec(em, 0, 0, 0)
    return res

def is_linear(edges):
    seen = set()
    for e in edges:
        for p in itertools.combinations(sorted(e), 2):
            if p in seen: return False
            seen.add(p)
    return True

def f7_free(n, edges):
    """F7 = {012,034,056,135,246}: a vertex c with three edges whose co-vertex pairs are crossed by two disjoint edges.
    Valid for any 3-graph (every copy of F7 has such a centre; with Delta <= 3 the three edges are all edges at c,
    in general we try all 3-subsets of edges at c)."""
    eset = set(tuple(sorted(e)) for e in edges)
    inc = [[] for _ in range(n)]
    for e in edges:
        for x in e: inc[x].append(e)
    for c in range(n):
        for trio in itertools.combinations(inc[c], 3):
            pairs = [tuple(x for x in e if x != c) for e in trio]
            if len(set(pairs[0] + pairs[1] + pairs[2])) < 6: continue
            for bits in range(4):  # fix the choice for pair 0 as index 0 (complement covers the other)
                f = (pairs[0][0], pairs[1][bits & 1], pairs[2][(bits >> 1) & 1])
                g = (pairs[0][1], pairs[1][1 - (bits & 1)], pairs[2][1 - ((bits >> 1) & 1)])
                if tuple(sorted(f)) in eset and tuple(sorted(g)) in eset:
                    return False
    return True

def p3_ok(n, edges):
    """(P3): e(S) <= |S|-2 for all S with |S| >= 2  <=>  for every pair {u,w} the edges have distinct
    representatives (each edge matched to one of its own vertices) avoiding u and w (Hall's theorem: for a set E' of
    edges with union S, |S - {u,w}| >= |E'| for all u,w in S iff e(S) <= |S| - 2).
    Implementation: one base matching, then for each pair re-augment the (at most two) edges matched to u, w."""
    m = len(edges)
    if m == 0: return True
    if m > n - 2: return False
    def aug(i, seen, match_v, forb):
        for x in edges[i]:
            if x in forb or x in seen: continue
            seen.add(x)
            if x not in match_v or aug(match_v[x], seen, match_v, forb):
                match_v[x] = i
                return True
        return False
    base = {}
    for i in range(m):
        if not aug(i, set(), base, ()): return False
    for u in range(n):
        for w in range(u + 1, n):
            mv = dict(base); todo = []
            for x in (u, w):
                if x in mv: todo.append(mv.pop(x))
            forb = (u, w)
            for i in todo:
                if not aug(i, set(), mv, forb): return False
    return True

def p3_ok_slow(n, edges):
    """reference implementation: a fresh matching for every pair."""
    m = len(edges)
    if m == 0: return True
    if m > n - 2: return False
    def matching(forb):
        match_v = {}
        def aug(i, seen):
            for x in edges[i]:
                if x in forb or x in seen: continue
                seen.add(x)
                if x not in match_v or aug(match_v[x], seen):
                    match_v[x] = i
                    return True
            return False
        for i in range(m):
            if not aug(i, set()): return False
        return True
    for u in range(n):
        for w in range(u + 1, n):
            if not matching({u, w}): return False
    return True

def p3_brute(n, edges):
    """brute force over all vertex subsets (small n only)."""
    em = emasks(edges)
    for S in range(1, 1 << n):
        k = bin(S).count('1')
        if k >= 2 and sum(1 for e in em if e & S == e) > k - 2: return False
    return True

def in_C3(n, edges):
    d = degrees(n, edges)
    if d and max(d) > 3: return False
    return is_linear(edges) and f7_free(n, edges) and p3_ok(n, edges)

def automorphisms(n, edges):
    """all automorphisms (as tuples) of a connected 3-graph without isolated vertices."""
    eset = set(tuple(sorted(e)) for e in edges)
    adj = [set() for _ in range(n)]
    for e in edges:
        for x in e:
            for y in e:
                if x != y: adj[x].add(y)
    d = degrees(n, edges)
    order = [0]; seen = {0}; i = 0
    while i < len(order):
        for y in sorted(adj[order[i]]):
            if y not in seen: seen.add(y); order.append(y)
        i += 1
    assert len(order) == n
    pos = {x: k for k, x in enumerate(order)}
    check_at = [[] for _ in range(n)]
    for e in edges:
        last = max(e, key=lambda x: pos[x]); check_at[pos[last]].append(e)
    res = []; phi = {}; used = set()
    def rec(k):
        if k == n:
            res.append(tuple(phi[x] for x in range(n))); return
        x = order[k]
        nb = [phi[y] for y in adj[x] if y in phi]
        cand = set(adj[nb[0]]) if nb else set(range(n))
        for z in nb[1:]: cand &= adj[z]
        for u in cand:
            if u in used or d[u] != d[x]: continue
            phi[x] = u; used.add(u)
            ok = all(tuple(sorted(phi[y] for y in e)) in eset for e in check_at[k])
            if ok: rec(k + 1)
            del phi[x]; used.discard(u)
    rec(0)
    return res

def induced_copies(P, n, edges):
    """all vertex sets (bitmasks) S of the 3-graph (n, edges) with H[S] isomorphic to the piece P."""
    eset = set(tuple(sorted(e)) for e in edges)
    adj = [set() for _ in range(n)]
    for e in edges:
        for x in e:
            for y in e:
                if x != y: adj[x].add(y)
    d = degrees(n, edges)
    Pn, Pe = P['n'], P['edges']
    Padj = [set() for _ in range(Pn)]
    for e in Pe:
        for x in e:
            for y in e:
                if x != y: Padj[x].add(y)
    Pd = degrees(Pn, Pe)
    order = [max(range(Pn), key=lambda x: Pd[x])]; seen = set(order); i = 0
    while i < len(order):
        for y in sorted(Padj[order[i]]):
            if y not in seen: seen.add(y); order.append(y)
        i += 1
    pos = {x: k for k, x in enumerate(order)}
    check_at = [[] for _ in range(Pn)]
    for e in Pe:
        last = max(e, key=lambda x: pos[x]); check_at[pos[last]].append(e)
    em = emasks(edges)
    found = set(); phi = {}; used = set()
    def rec(k):
        if k == Pn:
            S = 0
            for x in phi.values(): S |= 1 << x
            if S in found: return
            if sum(1 for e in em if e & S == e) == len(Pe): found.add(S)
            return
        x = order[k]
        nb = [phi[y] for y in Padj[x] if y in phi]
        cand = set(adj[nb[0]]) if nb else set(range(n))
        for z in nb[1:]: cand &= adj[z]
        for u in cand:
            if u in used or d[u] < Pd[x]: continue
            phi[x] = u; used.add(u)
            if all(tuple(sorted(phi[y] for y in e)) in eset for e in check_at[k]): rec(k + 1)
            del phi[x]; used.discard(u)
    rec(0)
    return found

def family_def(n, edges, fam_masks_weights):
    """DEF_H(X) = sum W - 35 |E*(X)| for a family given as [(mask, W)], checking disjointness."""
    U = 0; Wsum = 0
    for S, w in fam_masks_weights:
        assert S & U == 0
        U |= S; Wsum += w
    em = emasks(edges)
    estar = 0
    for e in em:
        if e & U and not any(e & S == e for S, _ in fam_masks_weights):
            estar += 1
    return Wsum - CE * estar

def def_certificate(n, edges, pieces, target):
    """search an L*-family X (members: induced copies of the pieces) with DEF_H(X) >= target; exact branch and bound
    (returns the best value found and the family if >= target, else the exact maximum and its family)."""
    em = emasks(edges)
    copies = []
    for P in pieces:
        for S in induced_copies(P, n, edges):
            copies.append((S, P['W'], P['m'], P['name']))
    copies.sort(key=lambda c: -c[1])
    best = [0, []]
    def bd(U):
        return sum(1 for e in em if e & U)
    def rec(i, U, gain, fam):
        obj = gain - CE * bd(U)
        if obj > best[0]:
            best[0] = obj; best[1] = list(fam)
            if obj >= target: return True
        ub = obj + sum(c[1] for c in copies[i:] if not c[0] & U)
        if ub <= best[0]: return False
        for j in range(i, len(copies)):
            S, w, mP, name = copies[j]
            if S & U: continue
            fam.append((S, w, name))
            if rec(j + 1, U | S, gain + w + CE * mP, fam): return True
            fam.pop()
        return False
    rec(0, 0, 0, [])
    return best[0], best[1], len(copies)
