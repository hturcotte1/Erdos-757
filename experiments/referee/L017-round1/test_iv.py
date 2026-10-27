# Referee L017 round 1: adversarial test of Theorem 4(iv) (pattern conditions <=> (star)) and of Theorem 4(v),(vi) logic.
# G = disjoint union of r <= 3 random connected linear 3-graphs in which every vertex is co-transversal ("free choice");
# add v with three edges {v} u P_j (pairwise disjoint pairs, no pair inside an edge of G, every component met).
# (star) is decided directly: tau(H) == tau(G) + 1, by brute force on H.  The (iv) condition is evaluated from the
# minimum transversals of the components after mapping the configuration onto the canonical names of its pattern.
import itertools, random, collections, sys
def tau(V, E):
    """exact transversal number by branching on an uncovered edge (with a packing lower bound)"""
    E = [frozenset(e) for e in E]
    best = [len(E)]
    def lb(rem):
        used = set(); c = 0
        for e in rem:
            if not (e & used): used |= e; c += 1
        return c
    def rec(rem, k):
        if not rem:
            best[0] = min(best[0], k); return
        if k + lb(rem) >= best[0]: return
        e = rem[0]
        for v in e:
            rec([f for f in rem if v not in f], k + 1)
    rec(E, 0)
    return best[0]
def min_trans(V, E):
    t = tau(V, E); return t, [frozenset(T) for T in itertools.combinations(sorted(V), t) if all(set(T) & e for e in E)]
def rand_conn_linear(n, m, rng):
    for _ in range(200):
        E = []; pairs = set()
        verts = list(range(n))
        for _ in range(4 * m):
            if len(E) == m: break
            e = frozenset(rng.sample(verts, 3)); ps = {frozenset(p) for p in itertools.combinations(e, 2)}
            if ps & pairs: continue
            E.append(e); pairs |= ps
        if len(E) != m: continue
        # connected, no isolated vertex
        adj = collections.defaultdict(set)
        for e in E:
            for x in e: adj[x] |= e
        seen = {0}; st = [0]
        while st:
            x = st.pop()
            for y in adj[x]:
                if y not in seen: seen.add(y); st.append(y)
        if len(seen) == n: return E
    return None
rng = random.Random(20261027)
lib = []
while len(lib) < 60:
    n = rng.choice([3, 5, 6, 7, 7, 8]); m = rng.randint((n - 1 + 1) // 2, n)
    E = rand_conn_linear(n, m, rng)
    if E is None: continue
    t, Ts = min_trans(range(n), E)
    if all(any(x in T for T in Ts) for x in range(n)):   # free choice
        lib.append((n, E, t, Ts))
print('library of free-choice components:', len(lib), collections.Counter((x[0], len(x[1])) for x in lib))
def classify(P, lab, r):
    """return (pattern, mapping) where mapping gives the canonical names; P: list of 3 pairs (tuples), lab: vertex->component"""
    for perm in itertools.permutations(range(3)):
        for sw in itertools.product((0, 1), repeat=3):
            Q = []
            for j, k in enumerate(perm):
                a, b = P[k]
                if sw[j]: a, b = b, a
                Q.append((a, b))
            for cperm in itertools.permutations(range(r)):
                L = {x: cperm[lab[x]] for x in lab}
                (a, b), (c, d), (e, f) = Q
                ins = lambda p, i: L[p[0]] == i and L[p[1]] == i
                if r == 1: return 'a', Q, L
                if r == 2:
                    if all(L[p[0]] == 0 and L[p[1]] == 1 for p in Q): return 'b', Q, L
                    if ins(Q[0], 0) and ins(Q[1], 0) and L[e] == 0 and L[f] == 1: return 'c1', Q, L
                    if ins(Q[0], 0) and ins(Q[1], 0) and ins(Q[2], 1): return 'c2', Q, L
                    if ins(Q[0], 0) and ins(Q[1], 1) and L[e] == 0 and L[f] == 1: return 'e', Q, L
                    if ins(Q[0], 0) and L[c] == 0 and L[d] == 1 and L[e] == 0 and L[f] == 1: return 'f', Q, L
                if r == 3:
                    if ins(Q[0], 0) and ins(Q[1], 0) and L[e] == 1 and L[f] == 2: return 'd', Q, L
    return None, None, None
stats = collections.Counter(); bad = 0
for trial in range(6000):
    r = rng.choice([1, 2, 2, 2, 3])
    comps = [rng.choice(lib) for _ in range(r)]
    off = 0; V = []; E = []; lab = {}; compT = []; comp_deg = {}
    for i, (n, Ec, t, Ts) in enumerate(comps):
        for x in range(n): lab[x + off] = i; V.append(x + off)
        E += [frozenset(y + off for y in e) for e in Ec]
        compT.append([frozenset(y + off for y in T) for T in Ts])
        off += n
    inedge = {frozenset(p) for e in E for p in itertools.combinations(e, 2)}
    # random three disjoint pairs, not inside an edge, meeting every component
    ok = False
    for _ in range(50):
        six = rng.sample(V, 6) if len(V) >= 6 else None
        if six is None: break
        P = [tuple(six[0:2]), tuple(six[2:4]), tuple(six[4:6])]
        if any(frozenset(p) in inedge for p in P): continue
        if len({lab[x] for x in six}) != r: continue
        ok = True; break
    if not ok: continue
    vnew = off
    H = E + [frozenset((vnew,) + p) for p in P]
    tG = sum(tau(range(c[0]), c[1]) for c in comps)
    tH = tau(V + [vnew], H)
    star = (tH == tG + 1)
    pat, Q, L = classify(P, lab, r)
    if pat is None:
        # Hall: must be non-deficient, then (star) must fail (free choice)
        stats['non-deficient'] += 1
        if star: bad += 1; print('BAD: (star) holds for a non-deficient distribution', P)
        continue
    (a, b), (c, d), (e, f) = Q
    # component index after relabelling
    inv = {}
    for x in L: inv.setdefault(L[x], set()).add(x)
    def Tof(i):  # min transversals of canonical component i
        orig = lab[next(iter(inv[i]))]; return compT[orig]
    meets = lambda T, p: bool(T & set(p))
    if pat == 'a':
        cond = not any(all(meets(T, p) for p in Q) for T in compT[0])
    elif pat == 'b':
        cond = (not any(len(T & {a, c, e}) >= 2 for T in Tof(0))) and (not any(len(T & {b, d, f}) >= 2 for T in Tof(1)))
    elif pat in ('c1', 'c2', 'd'):
        cond = not any(meets(T, (a, b)) and meets(T, (c, d)) for T in Tof(0))
    elif pat == 'e':
        cond = (not any(meets(T, (a, b)) and e in T for T in Tof(0))) and (not any(meets(T, (c, d)) and f in T for T in Tof(1)))
    elif pat == 'f':
        cond = (not any(meets(T, (a, b)) and meets(T, (c, e)) for T in Tof(0))) and (not any(d in T and f in T for T in Tof(1)))
    stats[pat] += 1; stats[pat + (' star' if star else ' nostar')] += 1
    if cond != star: bad += 1; print('BAD equivalence', pat, P, star, cond)
print(dict(sorted(stats.items())), 'BAD =', bad)
