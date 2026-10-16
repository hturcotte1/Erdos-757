"""Positive control PC4: base sets WITH universal vertices (Fibonacci prefixes {F_3..F_k}, k = 9, 11, 13), where the T2 lines
of Lemma E are genuinely deficient. Same comparison as PC3 between Route L (locus.py) and Route C (cases.py), plus:
for every universal vertex a, the whole lines 2X-Y=a and X-2Y=-a are in D' and are flagged (no symbolic witness)."""
import json, os, itertools
os.nice(15)
import locus, cases
fib = [1, 2]
while len(fib) < 20:
    fib.append(fib[-1] + fib[-2])
allok = True
for k in (7, 9, 11):
    P0 = fib[1:1 + k]           # 2,3,5,8,...
    assert locus.is45_full(P0), P0
    Ap = sorted(12 * v for v in P0)
    h, allmax, whole, pts = locus.deficient_locus(Ap)
    rc = cases.run_class(P0, 'fib%d' % k)
    U = rc['universal']
    def on_whole(x, y):
        return any(a * x + b * y == cc for (a, b, cc) in whole)
    flagged = set()
    for l in whole:
        a, b, cc = l
        if (a, b) in ((1, 0), (0, 1)) and cc in set(Ap): continue
        if l == (1, -1, 0): continue
        w = locus.identically_failing_quad(Ap, l)
        if w is None or w[0] != 'quad':
            flagged.add(l)
    ok_U = all((2, -1, a) in flagged and (1, -2, -a) in flagged for a in U)
    strict = {l for l in whole if (l[0], l[1]) in ((2, -1), (1, -2))}
    ok_U2 = strict == {(2, -1, a) for a in U} | {(1, -2, -a) for a in U}
    defC = {(min(x, y), max(x, y)) for x, y, hb in rc['t1b_deficient']} | {(min(x, y), max(x, y)) for x, y, hb in rc['t2_isect_def']}
    D_un = {(min(x, y), max(x, y)) for (x, y) in pts}
    miss_iii = [p for p in defC if p not in D_un and not on_whole(*p)]
    P45 = {(min(x, y), max(x, y)) for (x, y) in pts if not on_whole(x, y) and locus.b_is45(Ap, x, y)}
    miss_iv = [p for p in P45 if p not in defC]
    t1a_x = {x for x, hx in rc['t1a_deficient']}
    ok_i = all((1, 0, x) in flagged for x in t1a_x)
    ok = ok_U and ok_U2 and ok_i and not miss_iii and not miss_iv
    allok &= ok
    print(json.dumps({'set': P0, 'h': h, 'nS': len(allmax), 'universal': [u // 12 for u in U], 'n_whole': len(whole),
                      'n_flagged': len(flagged), 'flagged_types': sorted({(l[0], l[1]) for l in flagged}),
                      'n_pts': len(pts), 'P45_isolated': len(P45), 'routeC_def45': len(defC), 't1a_def': len(t1a_x),
                      'ok_U': ok_U, 'ok_U2': ok_U2, 'ok_i': ok_i, 'miss_iii': len(miss_iii), 'miss_iv': len(miss_iv), 'ok': ok}))
print('PC4 all ok:', allok)
