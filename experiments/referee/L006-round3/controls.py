"""Positive controls for Route V: A' = S - {u,v} for a known (4,5)-set S, chosen so that h(S) <= h(A')+1 (S is a deficient (4,5)
2-extension of A'). Route V must flag (u,v): as a deficient (4,5) point or on a generically-(4,5) common line."""
import json, itertools, sys, time
from fractions import Fraction as F
sys.path.insert(0, '/home/user/Erdos-757/experiments/referee/L006-round3')
import route_V as R
Abase = [0, 136, 200, 243, 246, 249, 272, 286, 298, 323, 400, 528, 596, 1056]
known = json.load(open('/home/user/Erdos-757/data/small_records.json'))['sets']
ctrl = []
# (a) A_base minus a pair, h(A')=8 (k=8, B=A_base has h=8 <= 9): my own choice of pairs
for u, v in [(0, 1056), (243, 249), (200, 528), (246, 272), (136, 596), (298, 323)]:
    Ap = [a for a in Abase if a not in (u, v)]
    ctrl.append(('Abase-{%d,%d}' % (u, v), Ap, (u, v), Abase))
# (b) 12-point records minus a pair with h = 6 (k=6, B = record has h=7 = k+1): same family as the claim, one size down
for name in ('12', '12b', '12c'):
    S = sorted(known[name]['set']); got = 0
    for u, v in itertools.combinations(S, 2):
        Ap = [a for a in S if a not in (u, v)]
        if R.max_sidon(Ap)[0] == 6:
            ctrl.append(('%s-{%d,%d}' % (name, u, v), Ap, (u, v), S)); got += 1
            if got == 2: break
    print(name, 'pairs with h(S-{u,v})=6 used:', got, flush=True)
for tag, Ap, (u, v), S in ctrl:
    t0 = time.time()
    kS = R.max_sidon(S)[0]
    r = R.route_V(Ap, tag)
    pts = {(F(a), F(b)) for a, b in r['deficient_45_points']}
    as_point = (F(u), F(v)) in pts and (F(v), F(u)) in pts
    on_line = [l for l in r['common_lines_generic45'] if any(l[0] * p + l[1] * q == l[2] for p, q in ((u, v), (v, u)))]
    print(json.dumps({'tag': tag, 'k': r['k'], 'h(S)': kS, 'S_is_45': R.is45_int(S), 'deficient_points': r['deficient_points'],
                      'deficient_45_points': len(pts), 'common_lines': len(r['common_lines']), 'common_generic45': len(r['common_lines_generic45']),
                      'pair_flagged_as_point': as_point, 'pair_on_flagged_line': len(on_line) > 0,
                      'DETECTED': as_point or len(on_line) > 0, 'h_of_deficient_45_points': sorted(set(r['h_of_deficient_45'])),
                      'secs': round(time.time() - t0, 1)}), flush=True)
