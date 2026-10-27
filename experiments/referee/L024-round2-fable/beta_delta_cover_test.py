"""Round-2 referee check (own code; imports nothing from hyp24/kt/e757/judge).
Tests the two structural identities that the revised 7.3 / README W2 of L024 quote from the proofs of
Lemma A+ (beta) and (delta):
  (beta)  w in V(F_v), d_H(w)=3, w not a co-vertex of v, F_w := component of H-w containing v:
          E(H) = E(F_v) u E(F_w)  and  V(H) = {v} u V(F_v) u V(F_w).
  (delta) w in Z on e_j, w' in Z on e_k (j != k), F_w, F_w' := components of H-w, H-w' containing v:
          E(H) = E(F_v) u E(F_w) u E(F_w')  and  V(H) = {v} u V(F_v) u V(F_w) u V(F_w').
Setting (as in the proofs): H connected linear 3-graph, Delta <= 3, v of degree 3, F_v a component of H-v met by
all three edges at v.  The proofs use only these facts (plus v in F_w, which here holds by definition), so the
identities must hold for every such instance, with F_v any component, not only a piece of L*."""
import random, itertools, sys
random.seed(int(sys.argv[1]) if len(sys.argv) > 1 else 1)
N_INST = int(sys.argv[2]) if len(sys.argv) > 2 else 20000

def components(n, edges, removed):
    verts = [x for x in range(n) if x not in removed]
    adj = {x: set() for x in verts}
    for e in edges:
        if any(x in removed for x in e): continue
        for x in e:
            adj[x] |= set(e) - {x}
    seen = set(); comps = []
    for s in verts:
        if s in seen: continue
        stack = [s]; comp = set()
        while stack:
            x = stack.pop()
            if x in comp: continue
            comp.add(x); stack.extend(adj[x] - comp)
        seen |= comp; comps.append(frozenset(comp))
    return comps

def induced_edges(edges, S):
    return {e for e in edges if set(e) <= S}

def random_linear(n, m):
    edges = set(); deg = [0]*n; tries = 0
    while len(edges) < m and tries < 50*m:
        tries += 1
        e = tuple(sorted(random.sample(range(n), 3)))
        if e in edges or any(deg[x] >= 3 for x in e): continue
        if any(len(set(e) & set(f)) >= 2 for f in edges): continue
        edges.add(e)
        for x in e: deg[x] += 1
    return sorted(edges)

stats = dict(instances=0, beta=0, delta=0, beta_fail=0, delta_fail=0, usable=0)
for it in range(N_INST):
    n = random.randint(7, 16); m = random.randint(n//2, n+2)
    edges = random_linear(n, m)
    stats['instances'] += 1
    if len(components(n, edges, set())) != 1: continue
    deg = [sum(1 for e in edges if x in e) for x in range(n)]
    for v in range(n):
        if deg[v] != 3: continue
        ev = [e for e in edges if v in e]
        comps = components(n, edges, {v})
        for Fv in comps:
            if not all(set(e) & Fv for e in ev): continue      # all three edges at v meet F_v
            stats['usable'] += 1
            EFv = induced_edges(edges, Fv)
            cov = set().union(*[set(e) - {v} for e in ev])    # co-vertices of v
            Z = [u for u in Fv if deg[u] == 3]
            Fcomp = {}
            def F_of(w):
                if w not in Fcomp:
                    cs = components(n, edges, {w})
                    Fcomp[w] = next(c for c in cs if v in c)
                return Fcomp[w]
            for w in Z:
                if w in cov: continue
                Fw = F_of(w); stats['beta'] += 1
                okE = (set(edges) == EFv | induced_edges(edges, Fw))
                okV = (set(range(n)) == {v} | Fv | Fw)
                if not (okE and okV):
                    stats['beta_fail'] += 1
                    print('BETA FAIL', n, edges, 'v', v, 'Fv', sorted(Fv), 'w', w)
            Zc = [u for u in Z if u in cov]
            for w, w2 in itertools.combinations(Zc, 2):
                ej = next(e for e in ev if w in e); ek = next(e for e in ev if w2 in e)
                if ej == ek: continue
                Fw, Fw2 = F_of(w), F_of(w2); stats['delta'] += 1
                okE = (set(edges) == EFv | induced_edges(edges, Fw) | induced_edges(edges, Fw2))
                okV = (set(range(n)) == {v} | Fv | Fw | Fw2)
                if not (okE and okV):
                    stats['delta_fail'] += 1
                    print('DELTA FAIL', n, edges, 'v', v, 'Fv', sorted(Fv), 'w', w, 'w2', w2)
print('STATS', stats)
