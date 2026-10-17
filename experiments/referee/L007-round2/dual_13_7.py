"""Referee L007 r2: cell (13,7,tau>=5) restricted to max degree <= 2, via the dual graph.
If H is a connected linear 3-graph with Delta(H) <= 2, its dual G* (nodes = edges of H, one G*-edge per degree-2
vertex of H) is a simple connected graph with max degree <= 3, |E(G*)| = 3m - n, and tau(H) = m - nu(G*).
For (n,m) = (13,7): G* has 7 nodes and 8 edges, and tau >= 5 needs nu(G*) <= 2.
Brute force over all C(21,8) edge sets on 7 nodes.  Also a sanity check of tau(H) = m - nu(G*) on random
Delta<=2 linear 3-graphs reconstructed from random G* (pendant vertices added)."""
import itertools, random
def nu(nodes, E):
    best = 0
    for k in range(len(nodes) // 2, 0, -1):
        for F in itertools.combinations(E, k):
            if len(set(itertools.chain(*F))) == 2 * k: return k
    return 0
def connected(nodes, E):
    seen = {0}; st = [0]
    while st:
        u = st.pop()
        for a, b in E:
            for p, q in ((a, b), (b, a)):
                if p == u and q not in seen: seen.add(q); st.append(q)
    return len(seen) == len(nodes)
nodes = list(range(7)); P = list(itertools.combinations(nodes, 2))
cnt = dict(total=0, conn_deg3=0, bad=0)
for E in itertools.combinations(P, 8):
    cnt['total'] += 1
    deg = [0] * 7
    for a, b in E: deg[a] += 1; deg[b] += 1
    if max(deg) > 3 or not connected(nodes, E): continue
    cnt['conn_deg3'] += 1
    if nu(nodes, E) <= 2: cnt['bad'] += 1; print('COUNTEREXAMPLE', E)
print(cnt)
# sanity: tau(H) = m - nu(G*) for random G* with max degree <= 3
rng = random.Random(3)
def tau(H, n):
    for k in range(n + 1):
        for S in itertools.combinations(range(n), k):
            s = set(S)
            if all(s & set(e) for e in H): return k
ok = 0
for trial in range(300):
    m = rng.randint(2, 7); nodes = list(range(m)); E = []
    for a, b in rng.sample(list(itertools.combinations(nodes, 2)), rng.randint(0, m * (m - 1) // 2)):
        d = [sum(x in e for e in E) for x in (a, b)]
        if max(d) < 3: E.append((a, b))
    # build H: vertex per G*-edge, plus pendant vertices to fill each node to 3
    nv = 0; mem = {i: [] for i in nodes}
    for a, b in E: mem[a].append(nv); mem[b].append(nv); nv += 1
    for i in nodes:
        while len(mem[i]) < 3: mem[i].append(nv); nv += 1
    H = [tuple(mem[i]) for i in nodes]
    assert tau(H, nv) == m - nu(nodes, E)
    ok += 1
print('tau = m - nu verified on', ok, 'random instances')
