"""Positive control for routeF.analyse: A' = A_base minus {a} (13 points, h = 8). Deficient (4,5) extensions of A'
exist (e.g. x = a, y generic: h(A_base u {y}) = 9 < 10), so Route F must flag the whole lines X=a, Y=a (no symbolic
witness, since A_base is (4,5)) and must report (4,5) deficient points with h = 9."""
import json, random, sys
sys.path.insert(0, '.')
import routeF
AB = [0, 136, 200, 243, 246, 249, 272, 286, 298, 323, 400, 528, 596, 1056]
for a in (0, 272, 1056):
    Ap = [v for v in AB if v != a]
    r = routeF.analyse(Ap, f'Abase-minus-{a}', random.Random(5))
    flagged = r['whole']['flagged']
    exp = sorted([[1, 0, 12 * a], [0, 1, 12 * a]])
    print(json.dumps({'removed': a, 'nS': r['nS'], 'selftest_bad': r['selftest_bad'], 'flagged_whole': flagged,
                      'expected_flagged_present': all(e in flagged for e in exp),
                      'n_D_points': r['n_D_points'], 'n_D_points_45': r['n_D_points_45'],
                      'h_of_45_points': sorted({p[2] for p in r['D_points_45']}), 'secs': r['secs']}), flush=True)
