"""Positive control PC3: mutual completeness of Route L (locus.py) and Route C (cases.py) on 13-point sets
A' = A minus one point (h(A') = 8 typically, so many deficient (4,5) two-point extensions exist: 15-point sets with h = 9).
Both routes are the referee's own code. Comparison (all as unordered pairs {x,y}, 12-scaled coordinates):
  (i)   T1a-deficient x (h(A' u x) = h(A'))      <->  whole lines X = x and Y = x of D'
  (ii)  universal vertices a of A'                <->  whole lines 2X-Y=a, X-2Y=-a, X+Y=2a of D'
  (iii) every (4,5) deficient pair of Route C (T1b or T2 intersections) lies in D' (isolated or on a whole line)
  (iv)  every (4,5) isolated point of D' not on a whole line is a deficient pair of Route C
"""
import sys, json, gzip, os, random, itertools
os.nice(15)
import locus, cases

sets = [json.loads(l)['set'] for l in gzip.open('/home/user/Erdos-757/data/census_n14_m12_classes.jsonl.gz', 'rt') if l.strip()]
todo = [(2440, 0), (2440, 6), (2440, 13), (0, 3), (777, 9), (1500, 1), (2909, 7), (1524, 12), (712, 5)]
if len(sys.argv) > 1:
    todo = [tuple(map(int, t.split(':'))) for t in sys.argv[1].split(',')]
allok = True
res = []
for c, k in todo:
    A = sorted(12 * v for v in sets[c])
    Ap = [v for i, v in enumerate(A) if i != k]
    h, allmax, whole, pts = locus.deficient_locus(Ap)
    # Route C on the same 13-point set (cases.run_class scales by 12 itself, so feed original coordinates)
    P0 = sorted(sets[c]); P0 = [v for i, v in enumerate(P0) if i != k]
    rc = cases.run_class(P0, c)
    assert rc['hA'] == h
    target = h + 2
    def on_whole(x, y):
        return any(a * x + b * y == cc for (a, b, cc) in whole)
    # (i)
    t1a_x = {x for x, hx in rc['t1a_deficient']}
    wl_x = {cc for (a, b, cc) in whole if (a, b) == (1, 0) and cc not in set(Ap)}
    wl_y = {cc for (a, b, cc) in whole if (a, b) == (0, 1) and cc not in set(Ap)}
    ok_i = (t1a_x <= wl_x) and (wl_x == wl_y)
    # vertical whole lines not explained by T1a must be non-(4,5) singles (A' u {v} not (4,5)) -- check
    extra_v = sorted(wl_x - t1a_x)
    extra_v_45 = [v for v in extra_v if all(locus.ndist((v,) + q) >= 5 for q in itertools.combinations(Ap, 3))]
    # (ii)
    U = set(rc['universal'])
    t2w = set()
    for a in U:
        t2w |= {(2, -1, a), (1, -2, -a), (1, 1, 2 * a)}
    # whole lines of the T2 directions: (2,-1) and (1,-2) can only come from universal vertices; a (1,1,c) whole line
    # either comes from a universal vertex (c = 2a) or is a parallelogram line X+Y = b+c, which must then carry a
    # symbolic non-(4,5) witness
    whole_t2_strict = {l for l in whole if (l[0], l[1]) in ((2, -1), (1, -2))}
    whole_11 = {l for l in whole if (l[0], l[1]) == (1, 1)}
    ok_ii = (t2w <= whole) and whole_t2_strict == {l for l in t2w if (l[0], l[1]) != (1, 1)}
    for l in whole_11 - t2w:
        w = locus.identically_failing_quad(Ap, l)
        if w is None or w[0] != 'quad':
            ok_ii = False
    # (iii)
    defC = set()
    for x, y, hb in rc['t1b_deficient']:
        defC.add((min(x, y), max(x, y)))
    for x, y, hb in rc['t2_isect_def']:
        defC.add((min(x, y), max(x, y)))
    D_un = {(min(x, y), max(x, y)) for (x, y) in pts}
    miss_iii = [p for p in defC if p not in D_un and not on_whole(*p)]
    # (iv)
    P45 = {(min(x, y), max(x, y)) for (x, y) in pts if not on_whole(x, y) and locus.b_is45(Ap, x, y)}
    miss_iv = [p for p in P45 if p not in defC]
    ok = ok_i and ok_ii and not miss_iii and not miss_iv
    allok &= ok
    r = {'class': c, 'dropped_index': k, 'h': h, 'nS': len(allmax), 'n_whole': len(whole), 'n_pts': len(pts),
         'n_pts45_isolated': len(P45), 'routeC_deficient_45_pairs': len(defC), 't1a_def': len(t1a_x),
         'universal': sorted(U), 'extra_vertical_whole_lines_not_T1a': len(extra_v), 'of_which_45_single': len(extra_v_45),
         'ok_i': ok_i, 'ok_ii': ok_ii, 'miss_iii': len(miss_iii), 'miss_iv': len(miss_iv), 'ok': ok}
    res.append(r)
    print(json.dumps(r), flush=True)
print('PC3 all ok:', allok)
json.dump(res, open('pc3_out.json', 'w'), indent=1)
