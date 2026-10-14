"""Route L (referee round 4): the deficiency locus, over ALL real (x,y), from the Sidon definition only.

Let A be a finite set with h(A) = k and M = all Sidon k-subsets of A.  For B = A u {x,y} (x,y distinct, not in A):
  h(B) <= k+2, and h(B) = k+2  <=>  some S in M has S u {x,y} Sidon
(a Sidon (k+2)-subset T of B has |T n A| = k, so T = S u {x,y} with S in M).
S u {x,y} fails to be Sidon  <=>  (x,y) lies on a line of K(S) = relation_lines(S)  (all formal coincidences
s1+s2 = s3+s4 over the symbols S u {X,Y}; x=y and x in S, y in S are also lines of K(S)).
So the deficient pairs are exactly D n Valid, where D = intersection over S in M of (union of lines of K(S)),
Valid = {x != y, x,y not in A, B is (4,5)}.
D is contained in K(S1) for any S1 in M.  For each line l of K(S1): if l is a line of K(S) for every S, l is a
whole line of D; otherwise pick S2 with l not in K(S2): l n D is inside the finite set l n K(S2) and each of
its points is tested against all S in M.  No 3-AP reduction, no weak-Sidon lemma, no case split is used.
Whole lines of D are decided at a point verified to be generic on the line (every formal coincidence over
A u {X,Y} that holds there holds identically on the line), which decides validity for the whole line."""
import itertools, json, sys, time, random
from fractions import Fraction as Fr
sys.path.insert(0, '/home/user/Erdos-757/experiments/referee/L001-round4')
from r4_lib import A_BASE, is45_full, is_sidon, sidon_subsets, relation_lines, intersect, on_line, n_dists

SC = 120   # scale: all intersection points of relation lines have denominators dividing 120


def all_relation_lines_full(A):
    """All lines of formal coincidences over the symbols A u {X,Y} (A arbitrary): (a,b) != (0,0) only."""
    from r4_lib import norm_line
    syms = [(0, 0, s) for s in A] + [(1, 0, 0), (0, 1, 0)]
    sums = [tuple(p + q for p, q in zip(syms[i], syms[j])) for i in range(len(syms)) for j in range(i, len(syms))]
    out = set()
    for u, v in itertools.combinations(sums, 2):
        a, b, c = u[0] - v[0], u[1] - v[1], v[2] - u[2]
        if a or b:
            out.add(norm_line(a, b, c))
    return out


def valid(A, Aset, x, y):
    if x == y or x in Aset or y in Aset:
        return False
    B = A + [x, y]
    # A itself is checked (4,5) once by the caller; here: every 4-subset meeting {x,y}
    for q in itertools.combinations(A, 3):
        if n_dists(q + (x,)) < 5 or n_dists(q + (y,)) < 5:
            return False
    for q in itertools.combinations(A, 2):
        if n_dists(q + (x, y)) < 5:
            return False
    return True


def generic_point(l, fulllines, rng):
    a, b, c = l
    for _ in range(100):
        t = Fr(rng.randrange(10**9, 2 * 10**9), rng.choice([7919, 104729, 1299709]))
        p = (t, Fr(c - a * t, b)) if b != 0 else (Fr(c, a), t)
        assert on_line(l, p)
        if all(m == l for m in fulllines if on_line(m, p)):
            return p
    raise RuntimeError('no generic point found')


def locus(A0, s1_index=0, label='', want_points=False):
    t0 = time.time()
    A = sorted(SC * a for a in A0)
    Aset = set(A)
    assert len(Aset) == len(A) and is45_full(A), 'base set must be a (4,5)-set'
    k = None
    for r in range(len(A), 0, -1):
        if sidon_subsets(A, r):
            k = r
            break
    M = sidon_subsets(A, k)
    Minfo = []
    for S in M:
        sums = {S[i] + S[j] for i in range(len(S)) for j in range(i, len(S))}
        Minfo.append((set(S), sums, S))
    rng = random.Random(12345 + s1_index)
    order = list(range(len(M)))
    rng.shuffle(order)
    Mord = [Minfo[i] for i in order]

    def killed(Si, x, y):
        Sset, Ssums, Sl = Si
        if x == y or x in Sset or y in Sset:
            return True
        new = [x + s for s in Sl] + [y + s for s in Sl] + [2 * x, 2 * y, x + y]
        ns = set(new)
        return len(ns) != len(new) or not ns.isdisjoint(Ssums)

    def in_D(x, y):
        return all(killed(Si, x, y) for Si in Mord)

    K = [relation_lines(S) for S in M]
    S1 = s1_index % len(M)
    whole, pts, tested = [], set(), set()
    nonint = 0
    for l in sorted(K[S1]):
        j = next((j for j in range(len(M)) if l not in K[j]), None)
        if j is None:
            whole.append(l)
            continue
        for m in K[j]:
            p = intersect(l, m)
            if p is None or p in tested:
                continue
            tested.add(p)
            if p[0].denominator != 1 or p[1].denominator != 1:
                nonint += 1
            if in_D(*p):
                pts.add(p)
    # validity of points
    valid_pts = sorted(p for p in pts if valid(A, Aset, *p))
    # whole lines
    full = all_relation_lines_full(A)
    whole_report = []
    for l in whole:
        p = generic_point(l, full, rng)
        v = valid(A, Aset, *p)
        whole_report.append((l, v))
    res = {
        'label': label, 'n': len(A0), 'k=h(A)': k, '|M|': len(M), 'S1': S1,
        '|K(S1)|': len(K[S1]), 'tested_points': len(tested), 'nonintegral_tested(scaled)': nonint,
        '|D points|': len(pts), 'whole_lines': len(whole),
        'whole_lines_list(scaled)': [list(l) for l in whole],
        'valid_D_points(unscaled)': [[str(x / SC), str(y / SC)] for x, y in valid_pts],
        'valid_whole_lines(scaled)': [list(l) for l, v in whole_report if v],
        'seconds': round(time.time() - t0, 1)}
    if want_points:
        res['_pts'] = pts
    return res


if __name__ == '__main__':
    out = {}
    # ---- main run on A_base, two different choices of S1 (results must coincide)
    r1 = locus(A_BASE, 0, 'A_base S1=0', want_points=True)
    r2 = locus(A_BASE, 77, 'A_base S1=77', want_points=True)
    wl = [tuple(l) for l in r1['whole_lines_list(scaled)']]
    def off_whole(P):
        return {p for p in P if not any(on_line(l, p) for l in wl)}
    iso1, iso2 = off_whole(r1['_pts']), off_whole(r2['_pts'])
    same = (iso1 == iso2) and (sorted(r1['whole_lines_list(scaled)']) == sorted(r2['whole_lines_list(scaled)']))
    A120 = [SC * a for a in A_BASE]; A120s = set(A120)
    reasons = {'x=y': 0, 'x or y in A': 0, 'not (4,5)': 0, 'valid': 0}
    for x, y in iso1:
        if x == y: reasons['x=y'] += 1
        elif x in A120s or y in A120s: reasons['x or y in A'] += 1
        elif not is45_full(A120 + [x, y]): reasons['not (4,5)'] += 1
        else: reasons['valid'] += 1
    for r in (r1, r2):
        r.pop('_pts')
        print(json.dumps(r), flush=True)
    print('isolated D points (off the whole lines): S1=0 ->', len(iso1), ' S1=77 ->', len(iso2), flush=True)
    print('D minus whole lines identical for the two choices of S1:', same, flush=True)
    print('isolated D points by reason (full 1820-quadruple check):', reasons, flush=True)
    out['A_base'] = [r1, r2, {'isolated_1': len(iso1), 'isolated_2': len(iso2), 'identical': same, 'reasons': reasons}]
    # whole lines of D for A_base: each X=c or Y=c must have c in A or A u {c} not (4,5)
    A120 = [SC * a for a in A_BASE]
    chk = []
    for a, b, c in r1['whole_lines_list(scaled)']:
        if b == 0 or a == 0:
            cc = Fr(c, a if a else b)
            chk.append((str(cc / SC), cc in set(A120), is45_full(A120 + [cc]) if cc not in set(A120) else None))
        else:
            chk.append(('2-var', a, b, c))
    print('whole lines of D (value, in A, A u {c} is (4,5)):', chk, flush=True)
    out['A_base_whole_lines'] = chk
    # ---- positive controls
    ctrl = []
    # (c1) A' = A_base minus two points u,v with h(A') >= 7: since h(A' u {u,v}) = h(A_base) = 8 < h(A')+2,
    #      (u,v) and (v,u) must be found as valid deficient points
    from r4_lib import sidon_subsets as ss
    hp = {}
    for u, v in itertools.combinations(A_BASE, 2):
        Ap = [a for a in A_BASE if a not in (u, v)]
        hp[(u, v)] = 8 if ss(Ap, 8) else (7 if ss(Ap, 7) else 6)
    print('h(A_base - {u,v}) over all 91 pairs:', {k: list(hp.values()).count(k) for k in set(hp.values())}, flush=True)
    for u, v in [(0, 246), (243, 249), (528, 1056), (136, 596)]:
        assert hp[(u, v)] >= 7
        Ap = [a for a in A_BASE if a not in (u, v)]
        r = locus(Ap, 0, 'control c1: A_base - {%d,%d}' % (u, v))
        found = [str(u), str(v)] in r['valid_D_points(unscaled)'] and [str(v), str(u)] in r['valid_D_points(unscaled)']
        r['removed_pair_detected'] = found
        r['n_valid_D_points'] = len(r['valid_D_points(unscaled)'])
        r['valid_D_points(unscaled)'] = r['valid_D_points(unscaled)'][:5]
        print(json.dumps(r), flush=True)
        ctrl.append(r)
    # (c2) A'' = A_base minus one point u (h = 8): lines X=u and Y=u must be valid whole lines of D
    for u in (0, 246, 1056):
        Ap = [a for a in A_BASE if a != u]
        r = locus(Ap, 0, 'control c2: A_base - {%d}' % u)
        vl = r['valid_whole_lines(scaled)']
        r['X=u and Y=u detected as valid whole lines'] = ([1, 0, SC * u] in vl) and ([0, 1, SC * u] in vl)
        r['n_valid_D_points'] = len(r['valid_D_points(unscaled)'])
        r['valid_D_points(unscaled)'] = r['valid_D_points(unscaled)'][:5]
        print(json.dumps(r), flush=True)
        ctrl.append(r)
    out['controls'] = ctrl
    json.dump(out, open('/home/user/Erdos-757/experiments/referee/L001-round4/r4_locus_out.json', 'w'), indent=1)
