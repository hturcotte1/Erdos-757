"""Referee (L022, referee #2): spot checks of the data claims D2, D3 of Corollary 3' on the stored lists
(experiments/20261027-0300-transversal-richness/inputs), with my own transversal code (t2.py).
 D3: every tight connected Delta<=3 class other than E_1 has at most one pendant vertex.
 D2: in the slack-1 Delta<=3 classes there is no role_b triple (three pairwise non-co-transversal vertices)
     and no role_f1 configuration (pair P not inside an edge, two further vertices c,e, all four cross pairs
     non-co-transversal); role_b also checked on the tight classes.
 Also: L017 Theorem 4(iii) free choice (every vertex co-transversal) on every class tested.
usage: python3 roles.py cell [cell ...]   (cells like 8_5_3; classes with Delta>3 are skipped)
"""
import sys, itertools, time
sys.path.insert(0, '/home/user/Erdos-757/experiments/referee/L022')
from t2 import masks, tau, all_min_transversals

INP = '/home/user/Erdos-757/experiments/20261027-0300-transversal-richness/inputs/cell_%s.txt'
for cell in sys.argv[1:]:
    lines = [l.split() for l in open(INP % cell) if l.strip()]
    tot = dict(classes=0, skipped=0, pend_ge2=0, role_b=0, role_f1=0, role_b_all=0, free_choice_fail=0, maxT=0)
    t0 = time.time()
    for ci, t in enumerate(lines):
        n, m, tt = map(int, t[:3]); xs = list(map(int, t[3:]))
        E = [tuple(xs[3 * i:3 * i + 3]) for i in range(m)]
        deg = [0] * n
        for e in E:
            for x in e: deg[x] += 1
        if max(deg) > 3:
            tot['skipped'] += 1; continue
        tot['classes'] += 1
        em = masks(E)
        Ts, tau_ = all_min_transversals(em)
        assert tau_ == tt, (cell, ci, tau_, tt)
        tot['maxT'] = max(tot['maxT'], len(Ts))
        s = 3 * n + 2 * m - 11 * tau_
        if s == 0 and not (n == 3) and deg.count(1) >= 2:
            tot['pend_ge2'] += 1; print('  tight class with >=2 pendants:', cell, ci, deg)
        cov = 0
        for T in Ts: cov |= T
        if cov != (1 << n) - 1: tot['free_choice_fail'] += 1
        # co-transversal pairs
        co = set()
        for T in Ts:
            vs = [x for x in range(n) if (T >> x) & 1]
            for a, b in itertools.combinations(vs, 2): co.add((a, b))
        anti = lambda a, b: (min(a, b), max(a, b)) not in co
        low = [x for x in range(n) if deg[x] <= 2]
        # role_b among vertices of degree <= 2 (attachment vertices), and among all vertices
        rb = sum(1 for a, b, c in itertools.combinations(low, 3) if anti(a, b) and anti(a, c) and anti(b, c))
        rb_all = sum(1 for a, b, c in itertools.combinations(range(n), 3) if anti(a, b) and anti(a, c) and anti(b, c))
        inedge = {frozenset(p) for e in E for p in itertools.combinations(e, 2)}
        rf1 = 0
        for a, b in itertools.combinations(low, 2):
            if frozenset((a, b)) in inedge: continue
            for c, e_ in itertools.combinations([x for x in low if x not in (a, b)], 2):
                if anti(a, c) and anti(a, e_) and anti(b, c) and anti(b, e_): rf1 += 1
        if rb: tot['role_b'] += 1
        if rb_all: tot['role_b_all'] += 1
        if rf1: tot['role_f1'] += 1; print('  role_f1 configuration in', cell, ci)
        if rb and not (n == 3): print('  role_b triple (deg<=2 vertices) in', cell, ci)
    tot['secs'] = round(time.time() - t0, 1)
    print(cell, tot, flush=True)
