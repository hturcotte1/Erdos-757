"""Referee L014 round 2: validate bin/myext against pure-Python brute force from the definitions on random linear 3-graphs.
(a) verify mode (d=0): tau by all vertex subsets, F7 by trying all bijections on every 5-edge/7-vertex sub-configuration,
    (P3) by all vertex subsets S, connectivity by BFS;
(b) extension mode: every d-set (d=2,3) of pairwise disjoint admissible pairs, tau(H) by brute force; hit sets compared."""
import itertools, random, subprocess, sys
F7 = [(0,1,2),(0,3,4),(0,5,6),(1,3,5),(2,4,6)]
F7S = set(frozenset(e) for e in F7)
def tau_bf(n, E):
    for k in range(0, n + 1):
        for T in itertools.combinations(range(n), k):
            s = set(T)
            if all(s & set(e) for e in E): return k
def has_f7(n, E):
    for F in itertools.combinations(E, 5):
        V = sorted(set().union(*map(set, F)))
        if len(V) != 7: continue
        Fs = set(frozenset(e) for e in F)
        for perm in itertools.permutations(V):
            mp = dict(zip(range(7), perm))
            if all(frozenset(mp[x] for x in e) in Fs for e in F7): return True
    return False
def p3_bf(n, E):
    for k in range(2, n + 1):
        for S in itertools.combinations(range(n), k):
            s = set(S)
            if sum(1 for e in E if set(e) <= s) > k - 2: return False
    return True
def conn(n, E):
    adj = {v: set() for v in range(n)}
    for e in E:
        for a in e:
            adj[a] |= set(e) - {a}
    seen = {0}; st = [0]
    while st:
        v = st.pop()
        for w in adj[v]:
            if w not in seen: seen.add(w); st.append(w)
    return len(seen) == n
def rand_linear(n, m, dmax, rng):
    for _ in range(200):
        E = []; pairs = set(); deg = [0]*n
        tries = 0
        while len(E) < m and tries < 500:
            tries += 1
            e = tuple(sorted(rng.sample(range(n), 3)))
            pr = [(e[0],e[1]),(e[0],e[2]),(e[1],e[2])]
            if any(p in pairs for p in pr) or any(deg[v] >= dmax for v in e): continue
            E.append(e); pairs |= set(pr)
            for v in e: deg[v] += 1
        if len(E) == m: return E
    return None
def line(n, E): return '%d %d ' % (n, len(E)) + ' '.join('%d %d %d' % e for e in E)
rng = random.Random(20261020)
B = "/home/user/Erdos-757/experiments/referee/L014-round2/bin/" + (sys.argv[1] if len(sys.argv) > 1 else "myext")
# (a) verify mode
bad = 0; tested = 0; nmem = 0
for it in range(400):
    n = rng.randint(6, 10); m = rng.randint(2, min(n - 1, 9)); E = rand_linear(n, m, 3, rng)
    if E is None: continue
    if it % 3 == 0:  # plant an F7 sometimes
        if n >= 7:
            perm = rng.sample(range(n), 7); E2 = [tuple(sorted(perm[x] for x in e)) for e in F7]
            pairs = set()
            ok = True
            for e in E2:
                for p in itertools.combinations(e, 2):
                    if p in pairs: ok = False
                    pairs.add(p)
            if ok:
                extra = [e for e in E if not any(p in pairs for p in itertools.combinations(e, 2))]
                E = E2 + extra[:2]
    t = tau_bf(n, E)
    out = subprocess.run([B, str(t), '0', '0', '3'], input=line(n, E) + '\n', capture_output=True, text=True).stdout
    deg = [sum(1 for e in E if v in e) for v in range(n)]
    py_member = (not has_f7(n, E)) and p3_bf(n, E) and conn(n, E) and max(deg) <= 3
    c_member = 'BADREP' not in out
    tested += 1; nmem += py_member
    if py_member != c_member:
        bad += 1; print('MISMATCH verify', n, E, out)
    else:
        if not c_member:
            # compare the individual flags
            fl = dict(kv.split('=') for kv in out.split(':')[0].split()[1:])
            if int(fl['f7'] != '0') != int(has_f7(n, E)) or int(fl['p3']) != int(p3_bf(n, E)) or int(fl['conn']) != int(conn(n, E)):
                bad += 1; print('FLAG MISMATCH', n, E, out)
print('verify-mode tests', tested, 'python members', nmem, 'mismatches', bad)
# (b) extension mode
bad2 = 0; tested2 = 0; hits_tot = 0
for it in range(250):
    d = rng.choice([2, 3, 3]); n = rng.randint(6, 11); m = rng.randint(3, min(n - 2, 8)); E = rand_linear(n, m, d, rng)
    if E is None: continue
    t = tau_bf(n, E); emax = rng.choice([d - 1, d])
    deg = [sum(1 for e in E if v in e) for v in range(n)]
    pairs_in = set(p for e in E for p in itertools.combinations(e, 2))
    adm = [(a, b) for a in range(n) for b in range(a + 1, n) if deg[a] <= emax and deg[b] <= emax and (a, b) not in pairs_in]
    hits = set()
    for S in itertools.combinations(adm, d):
        vs = [v for p in S for v in p]
        if len(set(vs)) != 2 * d: continue
        H = E + [tuple(sorted((n,) + p)) for p in S]
        if tau_bf(n + 1, H) >= t + 1: hits.add(tuple(sorted(tuple(sorted(e)) for e in H)))
    out = subprocess.run([B, str(t), str(t + 1), str(d), str(emax), '1'], input=line(n, E) + '\n', capture_output=True, text=True).stdout
    chits = set()
    for l in out.splitlines():
        if l.startswith('HIT') or l.startswith('MEMBER'):
            a = list(map(int, l.split(':')[1].split())); nv, ne = a[0], a[1]
            chits.add(tuple(sorted(tuple(sorted(a[2 + 3*i: 5 + 3*i])) for i in range(ne))))
    tested2 += 1; hits_tot += len(hits)
    if chits != hits: bad2 += 1; print('MISMATCH ext', n, E, d, emax, len(hits), len(chits))
print('extension-mode tests', tested2, 'total brute-force hits', hits_tot, 'mismatches', bad2)
