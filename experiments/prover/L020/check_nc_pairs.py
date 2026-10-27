"""L020 check of Proposition 6 on stored near-tight graphs (Delta<=3, slack<=1): for every NC pair {x,y} (degrees <= 2,
in no common minimum transversal): tau(K-x-y) = tau(K)-1 and s(K-x-y) = s(K)+5-2|d(x,y)| >= 0, where
|d(x,y)| = d(x)+d(y)-[x,y share an edge]; for d(x)=d(y)=2: x,y share an edge, s(K)=1, K-x-y is a union of <= 5 tight graphs."""
import sys, itertools, collections
sys.path.insert(0, '/home/user/Erdos-757/experiments/prover/L017'); sys.path.insert(0, '/home/user/Erdos-757/experiments/prover/L020')
import hyp
from roles import read_any
tally = collections.Counter(); bad = []
for p in sys.argv[1:]:
    for (n, es) in read_any(p):
        deg = hyp.degrees(n, es)
        if max(deg) > 3: continue
        Ts, t = hyp.all_min_transversals(hyp.masks(es)); s = 3*n + 2*len(es) - 11*t
        if s > 1: continue
        cov = [0]*n
        for T in Ts:
            mm = T
            while mm:
                b = mm & -mm; mm ^= b; cov[b.bit_length()-1] |= T
        share = set(frozenset(q) for e in es for q in itertools.combinations(e, 2))
        for x, y in itertools.combinations([u for u in range(n) if deg[u] <= 2], 2):
            if (cov[x] >> y) & 1: continue
            sig = 1 if frozenset((x, y)) in share else 0
            d = deg[x] + deg[y] - sig
            rest = [u for u in range(n) if u not in (x, y)]
            E2 = [e for e in es if x not in e and y not in e]
            t2 = hyp.tau_masks(hyp.masks(E2)); s2 = 3*(n-2) + 2*len(E2) - 11*t2
            ok = (t2 == t - 1) and (s2 == s + 5 - 2*d) and s2 >= 0
            key = (deg[x], deg[y], sig) if deg[x] <= deg[y] else (deg[y], deg[x], sig)
            tally[('type', key, 'slackK', s, 's(K-x-y)', s2)] += 1
            if key == (2, 2, 1) or key == (2, 2, 0):
                comps = hyp.components(rest, E2)
                sl = [3*len(c) + 2*len(hyp.induced(E2, set(c))) - 11*hyp.tau_sub(c, E2) for c in comps]
                ok = ok and sig == 1 and s == 1 and all(v == 0 for v in sl) and len(comps) <= 5
            if not ok: bad.append((p, x, y))
    print(p.split('/')[-1], 'done', flush=True)
for k in sorted(tally): print(k, tally[k])
print('violations', len(bad), bad[:5])
