# Referee L017 round 1: check the conclusions of Theorems 1(a)-(f), 3, 4, 5 (which Step 10.1 says hold for every
# linear vertex-critical violator) on all linear vertex-critical violators found by vcrit (n <= 11 all degrees,
# n = 12, 13 with Delta <= 3).  Exact tau by exhaustive search over subsets (n <= 13).
import re, itertools, collections, sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
def load():
    gs = []
    for fn in ('vcrit_le11.txt', 'vcrit_12_13_D3.txt'):
        for line in open(os.path.join(HERE, fn)):
            if line.startswith('VIOL crit=1'):
                n = int(re.search(r' n=(\d+)', line).group(1))
                E = [tuple(int(x) for x in t.split(',')) for t in re.findall(r'\(([^)]*)\)', line)]
                gs.append((n, E))
    return gs
class Hyp:
    def __init__(self, V, E):
        self.V = frozenset(V); self.E = [frozenset(e) for e in E if set(e) <= set(V)]
    def tau(self):
        return tau_of(self.V, tuple(sorted(tuple(sorted(e)) for e in self.E)))
_memo = {}
def tau_of(V, E):
    key = (V, E)
    if key in _memo: return _memo[key]
    if not E: _memo[key] = 0; return 0
    # branch on first edge
    best = None
    e = E[0]
    for v in e:
        rest = tuple(f for f in E if v not in f)
        t = 1 + tau_of(V - {v}, rest)
        if best is None or t < best: best = t
    _memo[key] = best; return best
def induced(V, E, W):
    W = frozenset(W); return W, tuple(sorted(tuple(sorted(e)) for e in E if set(e) <= W))
def slack(W, E):
    return 3*len(W) + 2*len(E) - 11*tau_of(W, E)
def components(W, E):
    W = set(W); adj = collections.defaultdict(set)
    for e in E:
        for x in e:
            adj[x] |= set(e) - {x}
    comps = []; seen = set()
    for v in sorted(W):
        if v in seen: continue
        st = [v]; c = set([v]); seen.add(v)
        while st:
            x = st.pop()
            for y in adj[x]:
                if y not in seen: seen.add(y); c.add(y); st.append(y)
        comps.append(frozenset(c))
    return comps
def all_min_transversals(W, E):
    t = tau_of(W, E); res = []
    for T in itertools.combinations(sorted(W), t):
        S = set(T)
        if all(S & set(e) for e in E): res.append(frozenset(T))
    return res
def cotrans(W, E, X):
    W2, E2 = induced(W, E, set(W) - set(X))
    return tau_of(W2, E2) == tau_of(frozenset(W), E) - len(X)
fails = collections.Counter(); stats = collections.Counter()
def check(cond, tag):
    stats[tag] += 1
    if not cond: fails[tag] += 1; print('FAIL', tag)
for gi, (n, Elist) in enumerate(load()):
    V = frozenset(range(n)); E = tuple(sorted(tuple(sorted(e)) for e in Elist)); m = len(E)
    t = tau_of(V, E); s = 3*n + 2*m - 11*t
    deg = collections.Counter(v for e in E for v in e)
    inedge = lambda x, y: any(x in e and y in e for e in E)
    dX = lambda X: sum(1 for e in E if set(e) & set(X))
    print('graph', gi, (n, m, t), 's=', s, 'degrees', sorted(collections.Counter(deg.values()).items()))
    # vertex-critical (re-check)
    for k in range(1, n+1):
        for Z in itertools.combinations(range(n), k):
            W, EW = induced(V, E, V - set(Z))
            if slack(W, EW) < 0: fails['not vcrit'] += 1
    # Theorem 1
    check(len(components(V, E)) == 1 and all(deg[v] >= 1 for v in V), 'T1a')
    for v in V:
        W, EW = induced(V, E, V - {v})
        check(tau_of(W, EW) == t - 1, 'T1b tau')
        check(slack(W, EW) == s + 8 - 2*deg[v] and slack(W, EW) >= 0, 'T1b slack')
    check(max(deg.values()) == 3, 'T1c,d')
    check(s in (-1, -2), 'T1e')
    for k in (1, 2, 3):
        for X in itertools.combinations(range(n), k):
            if 2*dX(X) > s + 8*k - 11:
                check(cotrans(V, E, X), 'T1f')
    # Theorem 3
    for e in E:
        ds = [deg[x] for x in e]
        check(sorted(ds)[:2] != [1, 1], 'T3a'); check(sum(ds) >= 5, 'T3b')
        if 1 in ds: check(sorted(ds) == [1, 2, 2], 'T3c,d'); check(s == -1, 'T3f')
    for x in V:
        cnt = sum(1 for e in E if x in e and any(deg[y] == 1 for y in e if y != x))
        check(cnt <= 1, 'T3e')
    # Theorem 4 at degree-3 vertices
    for v in V:
        if deg[v] != 3: continue
        Ev = [e for e in E if v in e]; P = [tuple(sorted(set(e) - {v})) for e in Ev]
        co = [x for p in P for x in p]
        check(len(set(co)) == 6 and all(deg[x] in (2, 3) for x in co), 'T4i deg')
        W, EG = induced(V, E, V - {v})
        check(not any(set(p) <= set(e) for p in P for e in EG), 'T4i pairs')
        check(tau_of(W, EG) == t - 1 and slack(W, EG) == s + 2, 'T4ii')
        comps = components(W, EG)
        check(all(len(c) >= 3 for c in comps), 'T4ii no isolated')
        cs = []
        for c in comps:
            Wc, Ec = induced(W, EG, c); cs.append((Wc, Ec, slack(Wc, Ec)))
        check(sum(x[2] for x in cs) == s + 2 and all(x[2] >= 0 for x in cs), 'T4ii slacks')
        check(all(c & set(co) for c in comps), 'T4ii meets')
        # (star): no min transversal of G meets all three pairs
        mts = all_min_transversals(W, EG)
        star = not any(all(T & set(p) for p in P) for T in mts)
        check(star, 'T4iii star')
        for (Wc, Ec, sc) in cs:
            for x in Wc: check(cotrans(Wc, Ec, (x,)), 'T4iii free choice')
        r = len(comps); check(r <= 3, 'T4iii r<=3')
        lab = {x: i for i, c in enumerate(comps) for x in c}
        typ = []
        for p in P:
            typ.append(('in', lab[p[0]]) if lab[p[0]] == lab[p[1]] else ('split', tuple(sorted((lab[p[0]], lab[p[1]])))))
        stats['T4 pattern r=%d %s' % (r, sorted(typ))] += 1
        # Hall deficiency
        nbrs = [{lab[p[0]], lab[p[1]]} for p in P]
        matching = any(len(set(ch)) == 3 for ch in itertools.product(*[sorted(x) for x in nbrs]))
        check(not matching, 'T4iii Hall')
        # (v): every pair inside one component that, in a min transversal, would allow meeting all pairs: check pair lemma
        for (Wc, Ec, sc) in cs:
            for x, y in itertools.combinations(sorted(Wc & set(co)), 2):
                if not cotrans(Wc, Ec, (x, y)):
                    dxy = sum(1 for e in Ec if x in e or y in e)
                    check(2*dxy <= sc + 5, 'T4v pair lemma')
    # Theorem 5(A) at degree-2 vertices
    for v in V:
        if deg[v] != 2: continue
        Ev = [e for e in E if v in e]; P = [tuple(sorted(set(e) - {v})) for e in Ev]
        W, EG = induced(V, E, V - {v})
        check(tau_of(W, EG) == t - 1 and slack(W, EG) == s + 4, 'T5Ai')
        comps = components(W, EG)
        iso = [c for c in comps if len(c) == 1]
        check(len(iso) <= 1 and all(deg[next(iter(c))] == 1 for c in iso), 'T5Aii')
        if iso: check(s == -1, 'T5Aii s')
        nontriv = [c for c in comps if len(c) > 1]
        check(len(nontriv) == 1, 'T5Aiv one comp')
        mts = all_min_transversals(W, EG)
        check(not any(all(T & set(p) for p in P) for T in mts), 'T5Aiii')
        if not iso:
            F = nontriv[0]; Wc, Ec = induced(W, EG, F); sF = slack(Wc, Ec)
            for x in P[0]:
                for y in P[1]:
                    dxy = sum(1 for e in Ec if x in e or y in e)
                    check(not cotrans(Wc, Ec, (x, y)) and 2*dxy <= sF + 5, 'T5A alpha')
            stats['T5 case alpha'] += 1
        else:
            stats['T5 case beta'] += 1
    # Theorem 5(B) at degree-1 vertices
    for y in V:
        if deg[y] != 1: continue
        stats['T5B instances'] += 1
print('checks:', sum(v for k, v in stats.items() if not k.startswith('T4 pattern') and not k.startswith('T5 case') and not k.startswith('T5B')), 'failures:', dict(fails))
for k, v in sorted(stats.items()):
    if k.startswith('T4 pattern') or k.startswith('T5'): print(k, v)
