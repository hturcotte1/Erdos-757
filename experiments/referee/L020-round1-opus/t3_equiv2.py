"""Theorem 3 (iv)/(v) equivalences, direction 'condition => (*)' (and consistency), own code:
build attachments that SATISFY the stated NC-pair condition from the components' NC structure, then
compute (*) directly as tau(G + w(P1,P2,P3)) == tau(G) + 1.  Components: stored graphs with free choice."""
import sys, random, itertools
sys.path.insert(0, '/home/user/Erdos-757/experiments/referee/L020-round1-opus')
import hg
from roles_check import read_cell
from t3_equiv import union, prep, star


def star_product(n, es, vs_of, P):
    """(*) evaluated directly from the definition: no minimum transversal of G (= union of minimum
    transversals of the components) meets all three pairs."""
    pats = []
    for vs in vs_of:
        S = set(vs)
        ce = [e for e in es if e[0] in S]
        nn, cer, idx = hg.relabel(vs, ce)
        tc = hg.tau_bb(cer)
        met = set()
        for T in hg.all_min_transversals(cer, tc):
            mask = 0
            for j, p in enumerate(P):
                if any(x in S and (T >> idx[x]) & 1 for x in p):
                    mask |= 1 << j
            met.add(mask)
        pats.append(met)
    reach = {0}
    for met in pats:
        reach = {a | b for a in reach for b in met}
    return 7 not in reach
I = '/home/user/Erdos-757/experiments/20261027-0300-transversal-richness/inputs/'
pool = []
for c in ['3_1_1', '6_3_2', '8_5_3', '10_7_4', '9_4_3', '10_8_4', '12_10_5', '13_9_5', '15_11_6']:
    for n, m, t, es in read_cell(I + 'cell_%s.txt' % c)[:30]:
        pool.append((c, n, es))
# targeted pools (components that carry the needed configurations), to make the 'condition true' cases frequent
from roles_check import analyse
def has(cfg):
    out = []
    for c, n, es in pool:
        t = hg.tau_bb(es)
        TL, d, NC, b_any, e_cfg, f_cfg, B = analyse(n, es, t)
        if (cfg == 'b' and b_any) or (cfg == 'e' and e_cfg) or (cfg == 'f' and f_cfg) or (cfg == 'nc' and NC):
            out.append((c, n, es))
    return out
POOLS = {k: has(k) for k in ('b', 'e', 'f', 'nc')}
print('targeted pools:', {k: len(v) for k, v in POOLS.items()}, flush=True)
FIRST = {'b': 'b', 'e': 'e', 'f': 'f', 'i2-1': 'e', 'i2-2': 'e', 'i2-3': 'e', 'i2-4': 'nc', 'i3': 'e'}
SECOND = {'b': 'b', 'e': 'e', 'f': 'nc', 'i2-1': None, 'i2-2': None, 'i2-3': 'nc', 'i2-4': 'nc', 'i3': None}
random.seed(int(sys.argv[1]))
NPER = int(sys.argv[2])
res = {}
tries = 0
pats = ['b', 'e', 'f', 'i2-1', 'i2-2', 'i2-3', 'i2-4', 'i3']
while any(res.get(p, [0, 0])[0] + res.get(p, [0, 0])[1] < NPER for p in pats) and tries < 40000:
    tries += 1
    pat = random.choice([p for p in pats if res.get(p, [0, 0])[0] + res.get(p, [0, 0])[1] < NPER])
    r = 3 if pat == 'i3' else 2
    iso = 1 if pat.startswith('i') else 0
    parts = [random.choice(POOLS[FIRST[pat]])] + [random.choice(POOLS[SECOND[pat]]) if SECOND[pat] else random.choice(pool)] + [random.choice(pool) for _ in range(r - 2)]
    n, es, vs_of, ys = union([(p[1], p[2]) for p in parts], iso)
    t, B, d, share = prep(n, es, vs_of)
    if not all(B[x] for vs in vs_of for x in vs):
        continue
    low = [[x for x in vs if d[x] <= 2] for vs in vs_of]
    nc = lambda x, y: d[x] <= 2 and d[y] <= 2 and (B[x] & B[y]) == 0
    sh = lambda x, y: (min(x, y), max(x, y)) in share
    def bconf(L):
        return [tr for tr in itertools.combinations(L, 3) if all(nc(a, b) for a, b in itertools.combinations(tr, 2))]
    def econf(L):
        return [(z, x, y) for z in L for x, y in itertools.combinations(L, 2) if z not in (x, y) and not sh(x, y) and nc(z, x) and nc(z, y)]
    def ncp(L):
        return [(x, y) for x, y in itertools.combinations(L, 2) if nc(x, y)]
    P = None
    if pat == 'b':
        X, Y = bconf(low[0]), bconf(low[1])
        if X and Y:
            x = list(random.choice(X)); y = list(random.choice(Y)); random.shuffle(y)
            P = [(x[i], y[i]) for i in range(3)]
    elif pat == 'e':
        X, Y = econf(low[0]), econf(low[1])
        if X and Y:
            (e, a, b), (f, c, dd) = random.choice(X), random.choice(Y)
            P = [(a, b), (c, dd), (e, f)]
    elif pat == 'f':
        Fc = [((a, b), (c, e)) for a, b in itertools.combinations(low[0], 2) if not sh(a, b)
              for c, e in itertools.combinations([u for u in low[0] if u not in (a, b)], 2)
              if nc(a, c) and nc(a, e) and nc(b, c) and nc(b, e)]
        N2 = ncp(low[1])
        if Fc and N2:
            (a, b), (c, e) = random.choice(Fc); dd, f = random.choice(N2)
            P = [(a, b), (c, dd), (e, f)]
    else:
        y = ys[0]
        if pat in ('i2-1', 'i2-2', 'i3'):
            X = econf(low[0])
            if X:
                f, a, b = random.choice(X)
                if pat == 'i2-1':
                    Q = [q for q in itertools.combinations(low[1], 2) if not sh(*q)]
                    if Q:
                        P = [(a, b), random.choice(Q), (y, f)]
                elif pat == 'i2-2':
                    cs = [u for u in low[0] if u not in (a, b, f)]
                    if cs and low[1]:
                        P = [(a, b), (random.choice(cs), random.choice(low[1])), (y, f)]
                else:
                    if low[1] and low[2]:
                        P = [(a, b), (random.choice(low[1]), random.choice(low[2])), (y, f)]
        elif pat == 'i2-3':
            X = econf(low[0]); N2 = ncp(low[1])
            if X and N2:
                c, a, b = random.choice(X); dd, f = random.choice(N2)
                P = [(a, b), (c, dd), (y, f)]
        elif pat == 'i2-4':
            A = [(f, a, c) for f in low[0] for a, c in itertools.permutations(low[0], 2) if f not in (a, c) and nc(f, a) and nc(f, c)]
            N2 = ncp(low[1])
            if A and N2:
                f, a, c = random.choice(A); b, dd = random.choice(N2)
                P = [(a, b), (c, dd), (y, f)]
    if P is None:
        continue
    lhs = star_product(n, es, vs_of, P)
    if tries % 7 == 0:
        assert lhs == star(n, es, P, t), 'product and tau(G+w) evaluations of (*) disagree'
        res.setdefault('crosschecked', [0, 0])[0] += 1
    k = res.setdefault(pat, [0, 0])
    k[0 if lhs else 1] += 1
    if not lhs:
        print('COUNTEREXAMPLE condition true but (*) false', pat, [p[0] for p in parts], P, flush=True)
print('tries', tries, 'pattern: [condition true and (*) true, condition true but (*) FALSE]')
for p in pats + ['crosschecked']:
    print(' ', p, res.get(p))
