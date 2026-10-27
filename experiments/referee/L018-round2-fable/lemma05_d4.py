"""Adversarial test of the revised Lemma 0.5 (case d_K(p)>=4 now included) on the six tight
connected members of C with Delta=4 in the unrefereed list cell_25_23_11_D4 (I11 holds for all
members of C with fewer than 25 vertices by L016, so the lemma applies): the two co-vertices of
every pendant must have degree 2. Also evaluate the (Red) values of the proof's pairs."""
from common import *
path = '/home/user/Erdos-757/experiments/20261027-0340-induction-n28-n29-f25/lists/cell_25_23_11_D4.txt'
for i, l in enumerate(open(path)):
    if not l.startswith('FOUND'):
        continue
    E = parse_found(l); V = set(range(25)); d = degrees(E, V)
    for x in [v for v in V if d[v] == 1]:
        (e,) = [e for e in E if x in e]
        p, q = sorted(e - {x})
        # values of the proof's candidate pairs
        v1, _ = value_of({x, p}, E, V)      # case d(p)>=3 pair (Z,T)=({x,p},{p}) -> value_T = 6+2d(p)-11
        v2, _ = value_of({x, p, q}, E, V)   # case d(p)=1 pair ({x,p,q},{q})
        print(f'class #{i}: pendant {x} in edge {sorted(e)}: d(p)={d[p]} d(q)={d[q]} '
              f'-> Lemma 0.5 {"holds" if d[p]==2 and d[q]==2 else "FAILS"}; value({{x,p}})={v1}, value({{x,p,q}})={v2} (both must be <0 in a tight graph)')
