"""L026 C6: the merge lemma on stored data (own code; uses ownlib.py only).
For every graph G of the given lists and every non-co-transversal (NC) pair {x,y} of G:
  * if x,y are non-adjacent, build G/(x=y) and check tau(G/(x=y)) == tau(G)   (Lemma 11(a), any graph)
  * test G/(x=y) in C (linear, F7-free, (P3); no degree bound) and record why it is blocked
  * if s(G) <= 2 and G/(x=y) in C, report a VIOLATION (would contradict I11 below n(G), L016)
Usage: python3 merge_check.py <list files...>   (FOUND-format or flat 'n m tau e...' format)"""
import sys, itertools, time
sys.path.insert(0, '/home/user/Erdos-757/experiments/prover/L026')
import ownlib as L

def load(path):
    out = L.read_found(path)
    if not out:
        out = L.read_flat(path)
    return out

def merge(n, E, x, y):
    # identify y into x, relabel to 0..n-2
    lab = {}
    k = 0
    for u in range(n):
        if u == y: continue
        lab[u] = k; k += 1
    lab[y] = lab[x]
    E2 = [tuple(sorted(lab[u] for u in e)) for e in E]
    return n - 1, E2

def nc_pairs(n, E, t):
    T = L.all_min_transversals(E, t)
    cov = set()
    for Tm in T:
        vs = [i for i in range(n) if Tm >> i & 1]
        for p in itertools.combinations(vs, 2): cov.add(p)
    return [p for p in itertools.combinations(range(n), 2) if p not in cov], len(T)

def in_C(n, E):
    if not L.is_linear(E): return 'nonlinear'
    if L.has_F7(n, E): return 'F7'
    if not L.p3_ok(n, E): return 'P3'
    return 'inC'

def main(files):
    tot = {'graphs': 0, 'nc': 0, 'nc_adj': 0, 'nc_nonadj': 0, 'tau_fail': 0, 'commonnbr': 0,
           'P3': 0, 'F7': 0, 'inC': 0, 'violations': 0}
    types = {}
    t0 = time.time()
    for f in files:
        Gs = load(f)
        c = {'graphs': 0, 'nc': 0, 'nonadj': 0, 'blocked_commonnbr': 0, 'blocked_P3': 0, 'blocked_F7': 0,
             'mergeable': 0, 'tau_fail': 0}
        for E in Gs:
            n = L.nv(E); m = len(E); t = L.tau(E); s = 3 * n + 2 * m - 11 * t
            d = L.degs(n, E)
            adj = [set() for _ in range(n)]
            for e in E:
                for u in e:
                    for w in e:
                        if u != w: adj[u].add(w)
            NC, nT = nc_pairs(n, E, t)
            c['graphs'] += 1
            for (x, y) in NC:
                c['nc'] += 1
                sig = 1 if y in adj[x] else 0
                key = (min(d[x], d[y]), max(d[x], d[y]), sig, s)
                types[key] = types.get(key, 0) + 1
                if sig: continue
                c['nonadj'] += 1
                n2, E2 = merge(n, E, x, y)
                t2 = L.tau(E2)
                if t2 != t:
                    c['tau_fail'] += 1
                    print('TAU-FAIL', f, E, (x, y), t, t2)
                if adj[x] & adj[y]:
                    c['blocked_commonnbr'] += 1
                    # sanity: then G/(x=y) is non-linear
                    assert not L.is_linear(E2)
                    continue
                r = in_C(n2, E2)
                if r == 'inC':
                    c['mergeable'] += 1
                    s2 = 3 * n2 + 2 * m - 11 * t2
                    if s <= 2:
                        print('VIOLATION', f, E, (x, y), 's', s, 's2', s2)
                        tot['violations'] += 1
                elif r == 'P3': c['blocked_P3'] += 1
                elif r == 'F7': c['blocked_F7'] += 1
                else:
                    print('UNEXPECTED nonlinear without common neighbour', f, E, (x, y))
        print(f.split('/')[-1], c, '[%ds]' % (time.time() - t0), flush=True)
        for k in ('graphs', 'nc'): tot[k] += c[k]
        tot['nc_nonadj'] += c['nonadj']; tot['tau_fail'] += c['tau_fail']
        tot['commonnbr'] += c['blocked_commonnbr']; tot['P3'] += c['blocked_P3']; tot['F7'] += c['blocked_F7']
        tot['inC'] += c['mergeable']
    print('NC pair types (dmin,dmax,sigma,slack): count')
    for k in sorted(types): print('  ', k, types[k])
    print('TOTAL', tot)

if __name__ == '__main__':
    main(sys.argv[1:])
