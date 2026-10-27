"""Referee round 2, L017: F7 is a linear vertex-critical violator; check the conclusions of Theorems 1(a)-(f), 3, 4, 5(A) on it (Step 10.2)."""
import itertools
E = [(0,1,2),(0,3,4),(0,5,6),(1,3,5),(2,4,6)]; n = 7; V = list(range(n))
def edges_in(vs): return [set(e) for e in E if set(e) <= set(vs)]
def tau(vs):
    es = edges_in(vs)
    for k in range(len(vs)+1):
        for S in itertools.combinations(vs, k):
            if all(set(S) & e for e in es): return k
def sl(vs): return 3*len(vs) + 2*len(edges_in(vs)) - 11*tau(vs)
t, s = tau(V), sl(V); deg = [sum(1 for e in E if v in e) for v in V]
assert all(len(set(a) & set(b)) <= 1 for a, b in itertools.combinations(E, 2))
print('F7: linear, n=7 m=5 tau=%d s=%d degrees=%s' % (t, s, deg))
bad = [Z for k in range(1, n+1) for Z in itertools.combinations(V, k) if sl([v for v in V if v not in Z]) < 0]
print('proper induced subgraphs with s<0:', bad, '-> vertex-critical violator' if not bad else '-> NOT vertex-critical')
for v in V:
    G = [u for u in V if u != v]; assert tau(G) == t-1 and sl(G) == s + 8 - 2*deg[v]
print('Theorem 1(b) tau(H-v)=tau-1, s(H-v)=s+8-2d: ok for all v; Delta=%d (1(c),(d)); s=%d in {-1,-2} (1(e))' % (max(deg), s))
for x, y in itertools.combinations(V, 2):
    bd = len([e for e in E if x in e or y in e])
    if 2*bd > s + 5: assert tau([u for u in V if u not in (x, y)]) == t-2, (x, y)
print('Theorem 1(f) for pairs: ok. Theorem 3: no degree-1 vertex, so (a)-(f) vacuous/true.')
v = 0; pairs = [tuple(sorted(set(e)-{v})) for e in E if v in e]; G = [u for u in V if u != v]; GE = edges_in(G)
par = {u: u for u in G}
def find(x):
    while par[x] != x: x = par[x]
    return x
for e in GE:
    e = sorted(e)
    for x in e[1:]: par[find(x)] = find(e[0])
comps = {}
for u in G: comps.setdefault(find(u), []).append(u)
comps = list(comps.values()); tG = tau(G)
print('Theorem 4 at v=0: pairs', pairs, 'components of G', comps, 's(G)=%d (= s+2)' % sl(G), 'tau(G)=%d' % tG)
mts = [S for S in itertools.combinations(G, tG) if all(set(S) & e for e in GE)]
print('  minimum transversals of G meeting all three pairs:', [S for S in mts if all(set(S) & set(p) for p in pairs)], '(star) holds' )
split = all(len(set(p) & set(c)) == 1 for p in pairs for c in comps)
print('  every pair split between the two components (pattern (b)):', split)
for v in [u for u in V if deg[u] == 2]:
    G = [u for u in V if u != v]; GE = edges_in(G); tG = tau(G); prs = [set(e)-{v} for e in E if v in e]
    assert tG == t-1 and sl(G) == s+4
    mt = [S for S in itertools.combinations(G, tG) if all(set(S) & e for e in GE)]
    assert not any(all(set(S) & p for p in prs) for S in mt)
    assert [u for u in G if not any(u in e for e in GE)] == []
print('Theorem 5(A) at the six degree-2 vertices: tau(G)=tau-1, s(G)=s+4=%d, (star_2) holds, no isolated vertex (case alpha): ok' % (s+4))
