"""Referee closure test: for every class X of cell(n,m,t,3) and EVERY vertex w of maximum degree d, the components of X - w
(isolated vertices included) must have types (n_K, m_K, tau_K) forming one of the own decompositions of (n-1, m-d) with slack
S' = 3(n-1)+2(m-d)-11 tau(X-w) >= 0, tau(X-w) in {t-1, t}, and every non-trivial component must be isomorphic (labelg) to a class
of the stored list cell(n_K, m_K, tau_K, d) in CELLDIR.  usage: closure.py CELLDIR n m t"""
import sys, os, subprocess, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rlib
CF = sys.argv[1]; n, m, t = map(int, sys.argv[2:5]); D = 3
reps = rlib.read_cell(rlib.cell_path(CF, n, m, t, D))[0]
comps = []   # (index of (X,w) pair, nK, edges relabelled)
pairs = []
for xi, es in enumerate(reps):
    deg = collections.Counter(v for e in es for v in e); d = max(deg.values())
    for w in sorted(v for v in deg if deg[v] == d):
        rest = [e for e in es if w not in e]; verts = [v for v in range(n) if v != w]
        par = {v: v for v in verts}
        def f(x):
            while par[x] != x: par[x] = par[par[x]]; x = par[x]
            return x
        for (a, b, c) in rest:
            ra, rb, rc = f(a), f(b), f(c); par[rb] = ra; par[f(rc)] = ra
        groups = collections.defaultdict(list)
        for v in verts: groups[f(v)].append(v)
        pi = len(pairs); pairs.append((xi, w, d, len(rest)))
        for root, vs in groups.items():
            idx = {v: i for i, v in enumerate(sorted(vs))}
            ce = [(idx[a], idx[b], idx[c]) for (a, b, c) in rest if a in idx]
            comps.append((pi, len(vs), ce))
# tau of every component and canonical forms, batched by size
bysize = collections.defaultdict(list)
for k, (pi, nk, ce) in enumerate(comps): bysize[nk].append(k)
tau = {}; canon = {}
for nk, ks in bysize.items():
    if nk == 1:
        for k in ks: tau[k] = 0
        continue
    lines = ['FOUND: ' + ' '.join('(%d,%d,%d)' % e for e in comps[k][2]) for k in ks]
    r = subprocess.run([rlib.REXT, 'filt', str(nk), '3'], input='\n'.join(lines) + '\n', capture_output=True, text=True, check=True)
    rows = [l.split() for l in r.stdout.split('\n') if l.strip()]
    assert len(rows) == len(ks)
    g6 = subprocess.run([rlib.REXT, 'g6', str(nk)], input='\n'.join(lines) + '\n', capture_output=True, text=True, check=True).stdout.split()
    cf = subprocess.run([rlib.LABELG, '-q'], input='\n'.join(g6) + '\n', capture_output=True, text=True, check=True).stdout.split()
    assert len(cf) == len(ks)
    for k, row, c in zip(ks, rows, cf):
        assert row[4:] == ['1', '1', '1', '1'], row   # linear, F7-free, P3, connected
        tau[k] = int(row[2]); canon[k] = c
listsets = {}
def lset(nk, mk, tk, d):
    key = (nk, mk, tk, d)
    if key not in listsets:
        p = rlib.cell_path(CF, nk, mk, tk, d)
        listsets[key] = rlib.canon_set_of_reps(rlib.read_cell(p)[0], nk) if os.path.exists(p) else None
    return listsets[key]
bypair = collections.defaultdict(list)
for k, (pi, nk, ce) in enumerate(comps): bypair[pi].append(k)
problems = 0; typestat = collections.Counter(); decs_cache = {}
for pi, (xi, w, d, mrest) in enumerate(pairs):
    ks = bypair[pi]
    types = tuple(sorted((comps[k][1], len(comps[k][2]), tau[k]) for k in ks))
    tw = sum(x[2] for x in types)
    Sp = 3 * (n - 1) + 2 * (m - d) - 11 * tw
    if tw not in (t - 1, t) or Sp < 0: problems += 1; print('BAD tau(X-w)', xi, w, tw, Sp); continue
    key = (n - 1, m - d, Sp)
    if key not in decs_cache: decs_cache[key] = set(rlib.my_decomps(*key))
    if types not in decs_cache[key]: problems += 1; print('NOT A DECOMPOSITION', xi, w, types); continue
    for k in ks:
        nk = comps[k][1]
        if nk == 1: continue
        S = lset(nk, len(comps[k][2]), tau[k], d)
        if S is None or canon[k] not in S: problems += 1; print('COMPONENT NOT IN LIST', xi, w, (nk, len(comps[k][2]), tau[k], d)); break
    typestat[types] += 1
print('CLOSURE cell(%d,%d,%d,3): classes=%d (class, max-degree vertex) pairs=%d components=%d problems=%d' % (n, m, t, len(reps), len(pairs), len(comps), problems))
for ty, c in typestat.most_common(8): print('   ', c, ty)
