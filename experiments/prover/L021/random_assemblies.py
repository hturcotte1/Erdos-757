"""L021 mini-falsifier for KT (epsilon = 1/6, list L*): random assemblies of 2..6 pieces of L* joined by random edges
(between pieces, with new vertices) and random degree-2/3 hub vertices, kept in C_3 (linear, F7-free, e(S)<=|S|-2 tested
in its Hall form on the 3 pairs inside each new edge, max degree 3), connected; for every graph with A < 0 the exact DEF
is computed and A + DEF >= 0 is checked.  Usage: python3 random_assemblies.py SEED SECONDS"""
import sys, json, random, time, itertools
sys.path.insert(0, '/home/user/Erdos-757/experiments/prover/L021')
from kt import *
R = json.load(open('/home/user/Erdos-757/experiments/prover/L021/closure_results.json'))
pieces = [Piece(p['edges'], p['name']) for p in R['pieces']]
seed = int(sys.argv[1]); secs = float(sys.argv[2]); rng = random.Random(seed)
def sdr_avoiding(edges, x, y):
    # bipartite matching edges -> vertices not in {x,y}
    match = {}
    def aug(i, seen):
        for u in edges[i]:
            if u == x or u == y or u in seen: continue
            seen.add(u)
            if u not in match or aug(match[u], seen):
                match[u] = i; return True
        return False
    return all(aug(i, set()) for i in range(len(edges)))
def can_add(edges, deg, e):
    if len(set(e)) < 3: return False
    if any(deg.get(x, 0) >= 3 for x in e): return False
    se = set(e)
    for f in edges:
        if len(se & set(f)) > 1: return False
    new = edges + [e]
    for x, y in itertools.combinations(e, 2):
        if not sdr_avoiding(new, x, y): return False
    # F7 through e: a centre of degree 3 with three edges, two further disjoint edges each meeting the three outside the centre
    inc = {}
    for i, f in enumerate(new):
        for u in f: inc.setdefault(u, []).append(i)
    for c, es in inc.items():
        if len(es) < 3: continue
        for trip in itertools.combinations(es, 3):
            rest = [new[j] for j in range(len(new)) if j not in trip]
            outs = [set(new[j]) - {c} for j in trip]
            ok = [set(f) for f in rest if c not in f and all(set(f) & o for o in outs)]
            for f, g in itertools.combinations(ok, 2):
                if not f & g: return False
    return True
def connected(n, edges):
    adj = {u: set() for u in range(n)}
    for f in edges:
        for u in f:
            adj[u] |= set(f) - {u}
    seen = {0}; st = [0]
    while st:
        u = st.pop()
        for w in adj[u]:
            if w not in seen: seen.add(w); st.append(w)
    return len(seen) == n
t0 = time.time(); tried = 0; kept = 0; special = 0; fails = 0; eqs = 0; minP = None; hist = {}
while time.time() - t0 < secs:
    k = rng.randint(2, 6)
    edges = []; n = 0
    for _ in range(k):
        P = rng.choice(pieces)
        edges += [tuple(x + n for x in e) for e in P.edges]; n += P.n
    deg = {}
    for f in edges:
        for u in f: deg[u] = deg.get(u, 0) + 1
    steps = rng.randint(k - 1, 3 * k)
    for _ in range(steps):
        low = [u for u in range(n) if deg.get(u, 0) <= 2]
        r = rng.random()
        if r < 0.4 and len(low) >= 3:
            e = tuple(rng.sample(low, 3))
            if can_add(edges, deg, e):
                edges.append(e)
                for u in e: deg[u] = deg.get(u, 0) + 1
        elif r < 0.6 and len(low) >= 2:
            a, b = rng.sample(low, 2); e = (a, b, n)
            if can_add(edges, deg, e):
                edges.append(e); n += 1
                for u in e: deg[u] = deg.get(u, 0) + 1
        else:
            d = rng.choice([2, 3]); h = n; ok = True; added = []
            cand = list(low); rng.shuffle(cand)
            n += 1
            for j in range(d):
                if len(cand) < 2: ok = False; break
                a, b = cand.pop(), cand.pop(); e = (h, a, b)
                if can_add(edges, deg, e):
                    edges.append(e); added.append(e)
                    for u in e: deg[u] = deg.get(u, 0) + 1
            if not added:
                n -= 1
    tried += 1
    if not connected(n, edges): continue
    kept += 1
    t = tau_masks(masks(edges)); A = A_value(n, len(edges), t)
    if A >= 0: continue
    special += 1
    D = deficiency(n, edges, pieces, proper=False)
    P = A + D
    minP = P if minP is None else min(minP, P)
    hist[n] = hist.get(n, 0) + 1
    if P == 0: eqs += 1
    if P < 0:
        fails += 1
        print('KT FAILS', n, len(edges), t, A, D, edges, flush=True)
print(f'seed {seed}: assemblies {tried}, connected in C3 {kept}, with A<0 {special} (by n: {dict(sorted(hist.items()))}), KT failures {fails}, equality {eqs}, min(A+DEF) {minP}')
