"""b-configurations counted WITHOUT the edge restriction (three vertices of degree <= 2, pairwise not co-transversal),
on Delta<=3 classes; re-check of L017 C5 'role_b non-zero only for E_1'."""
import sys, itertools
sys.path.insert(0, '/home/user/Erdos-757/experiments/prover/L017'); sys.path.insert(0, '/home/user/Erdos-757/experiments/prover/L020')
import hyp
from roles import read_any
for p in sys.argv[1:]:
    cls = 0; hit = 0
    for (n, es) in read_any(p):
        deg = hyp.degrees(n, es)
        if max(deg) > 3: continue
        cls += 1
        Ts, t = hyp.all_min_transversals(hyp.masks(es))
        cov = [0] * n
        for T in Ts:
            mm = T
            while mm:
                b = mm & -mm; mm ^= b; cov[b.bit_length() - 1] |= T
        A = [x for x in range(n) if deg[x] <= 2]
        if any(not (cov[x] >> y) & 1 and not (cov[x] >> z) & 1 and not (cov[y] >> z) & 1 for x, y, z in itertools.combinations(A, 3)): hit += 1
    print(p.split('/')[-1], 'Delta<=3 classes', cls, 'with a b-configuration (edges allowed)', hit, flush=True)
