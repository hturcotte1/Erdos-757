"""Post-process the positive controls of r4_locus.py: (u,v) counts as detected if it is a valid isolated
D point or lies on a reported valid whole line; spot-check reported deficient points with MaxSAT + full (4,5)."""
import json, sys, random
from fractions import Fraction as Fr
sys.path.insert(0, '/home/user/Erdos-757/experiments/referee/L001-round4')
from r4_lib import A_BASE, is45_full, h_maxsat
SC = 120
o = json.load(open('r4_locus_out.json'))
rng = random.Random(3)
for r in o['controls']:
    lab = r['label']
    rem = [int(t) for t in lab.split('{')[1].rstrip('}').split(',')]
    Ap = [a for a in A_BASE if a not in rem]
    k = r['k=h(A)']
    vw = [tuple(l) for l in r['valid_whole_lines(scaled)']]
    def on_valid_whole(x, y):
        return any(a * SC * x + b * SC * y == c for a, b, c in vw)
    if len(rem) == 2:
        u, v = rem
        det = on_valid_whole(u, v) or [str(u), str(v)] in r['valid_D_points(unscaled)']
        # direct: h(A' u {u,v}) = h(A_base) = 8 < k + 2
        hB, _ = h_maxsat(A_BASE)
        print(lab, '| (u,v) detected:', det, '| h(A_base) =', hB, '< h(A\')+2 =', k + 2)
    else:
        u = rem[0]
        t = Fr(10**9 + 7, 7919)
        B = Ap + [u, t]
        hB, _ = h_maxsat(B)
        print(lab, '| X=u valid whole line reported:', (1, 0, SC * u) in vw, '| at (u,t) generic: (4,5)', is45_full(B), 'h =', hB, '< h(A\'\')+2 =', k + 2)
    # spot-check the first few reported valid isolated points: (4,5) and h < k+2
    for xs, ys in r['valid_D_points(unscaled)'][:5]:
        x, y = Fr(xs), Fr(ys)
        B = [Fr(a) for a in Ap] + [x, y]
        ok45 = is45_full(B)
        hB, _ = h_maxsat(B)
        print('    reported deficient point', (xs, ys), '(4,5):', ok45, 'h =', hB, 'deficient:', hB < k + 2)
