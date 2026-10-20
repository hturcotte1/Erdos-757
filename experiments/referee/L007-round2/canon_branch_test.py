"""Empirical test of Lemma D: for random connected linear 3-graphs H (n<=11), run the canonical process of Lemma D
(my own implementation, random choice of the start vertex and of the order of (c)-edges), and check that the resulting
labelled copy of H is among the outputs of conn_dfs2_all and of enum_conn with parameters (n, m, tau(H), Delta(H))."""
import random, itertools, subprocess, re, sys
rng = random.Random(11)
def tau(n, es):
    for k in range(n + 1):
        for S in itertools.combinations(range(n), k):
            s = set(S)
            if all(s & set(e) for e in es): return k
def canonical(n, E, rng):
    E = [frozenset(e) for e in E]
    lab = {}; start = rng.randrange(n); lab[start] = 0; ell = 1; placed = set(); out = []
    c = 0
    while len(placed) < len(E):
        x = [v for v, l in lab.items() if l == c]
        assert x, 'no vertex with label c (D3 violated)'
        x = x[0]; l0 = ell
        F = [e for e in E if e not in placed and x in e]
        A = []; B = []; C = []
        for e in F:
            others = sorted(e - {x}); L = [v for v in others if v in lab]
            if len(L) == 2: A.append(e)
            elif len(L) == 1: B.append(e)
            else: C.append(e)
        A.sort(key=lambda e: sorted(lab[v] for v in e - {x}))
        B.sort(key=lambda e: [lab[v] for v in e - {x} if v in lab][0])
        rng.shuffle(C)
        for e in A: placed.add(e); out.append(e)
        for e in B:
            u = [v for v in e - {x} if v not in lab][0]; lab[u] = ell; ell += 1; placed.add(e); out.append(e)
        for e in C:
            u, w = sorted(e - {x}); rng.shuffle_pair = None
            pair = [u, w]; rng.shuffle(pair)
            lab[pair[0]] = ell; lab[pair[1]] = ell + 1; ell += 2; placed.add(e); out.append(e)
        c += 1
    assert ell == n
    return frozenset(tuple(sorted(lab[v] for v in e)) for e in E)
def parse(out):
    return {frozenset(tuple(sorted(map(int, t.split(',')))) for t in re.findall(r'\(([0-9,]+)\)', l)) for l in out.splitlines() if l.startswith('FOUND:')}
cache = {}
ok = 0; tried = 0
while tried < 60:
    n = rng.randint(5, 11); E = []
    for _ in range(500):
        e = tuple(sorted(rng.sample(range(n), 3)))
        if e in E: continue
        if any(len(set(e) & set(f)) >= 2 for f in E): continue
        E.append(e)
        if len(E) >= rng.randint(3, n - 2): break
    # keep only connected spanning graphs
    if set().union(*E) != set(range(n)): continue
    seen = {0}; changed = True
    while changed:
        changed = False
        for e in E:
            if set(e) & seen and not set(e) <= seen: seen |= set(e); changed = True
    if len(seen) != n: continue
    tried += 1; m = len(E); t = tau(n, E); D = max(sum(v in e for e in E) for v in range(n))
    key = (n, m, t, D)
    if key not in cache:
        a = subprocess.run(['./rerun/conn_dfs2_all', str(n), str(m), str(t), str(D)], capture_output=True, text=True).stdout
        b = subprocess.run(['./rerun/enum_conn', str(n), str(m), str(t), str(D), '1'], capture_output=True, text=True).stdout
        cache[key] = (parse(a), parse(b))
    A, B = cache[key]
    for rep in range(5):
        L = canonical(n, E, rng)
        ok += (L in A) and (L in B)
        if not ((L in A) and (L in B)): print('MISSING', key, E, sorted(L))
print('canonical labelled copies checked:', tried * 5, 'found in both outputs:', ok)
