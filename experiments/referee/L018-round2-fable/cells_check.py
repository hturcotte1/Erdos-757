"""Check (i) the 13 tight classes of Remark 5.4 (L013 lists, extracted to the scratchpad):
n, m, tau, slack 0, connected, Delta<=3, class C, and Lemma 0.5 (co-vertices of every pendant have
degree 2); (ii) the 6 classes of the new unrefereed list cell_25_23_11_D4 (degree sequences:
is any of them Delta<=3, which would refute Conjecture T'?)."""
import sys, glob, os
from common import *

CELLS = '/tmp/claude-0/-home-user-Erdos-757/32619e2f-2987-5d2f-a1f8-a110778bce61/scratchpad/cells13/cells'
ok_all = True
for (n, m, t) in [(3, 1, 1), (10, 7, 4), (14, 12, 6), (17, 13, 7), (13, 8, 5), (16, 9, 6)]:
    path = os.path.join(CELLS, f'cell_{n}_{m}_{t}_D3.txt')
    lines = [l for l in open(path) if l.startswith('FOUND')]
    print(f'cell ({n},{m},{t}) D3: {len(lines)} classes')
    for i, l in enumerate(lines):
        E = parse_found(l)
        V = set(range(n))
        assert vertices(E) <= V
        d = degrees(E, V)
        tt = tau(E)
        s = 3 * n + 2 * len(E) - 11 * tt
        conn = is_connected(E, V)
        inC = in_class_C(E, V)
        pend = [v for v in V if d[v] == 1]
        lem05 = True
        for x in pend:
            (e,) = [e for e in E if x in e]
            for y in e - {x}:
                if d[y] != 2:
                    lem05 = False
        degseq = ''.join(f'{k}^{list(d.values()).count(k)} ' for k in sorted(set(d.values())))
        good = (len(E) == m and tt == t and s == 0 and conn and inC and max(d.values()) <= 3 and lem05)
        ok_all &= good
        print(f'  #{i}: m={len(E)} tau={tt} slack={s} conn={conn} C={inC} degs={degseq} pendants={len(pend)} Lemma0.5={lem05} -> {"OK" if good else "FAIL"}')

print('\n--- new unrefereed list cell_25_23_11_D4 (6 classes) ---')
path = '/home/user/Erdos-757/experiments/20261027-0340-induction-n28-n29-f25/lists/cell_25_23_11_D4.txt'
lines = [l for l in open(path) if l.startswith('FOUND')]
for i, l in enumerate(lines):
    E = parse_found(l)
    V = set(range(25))
    d = degrees(E, V)
    tt = tau(E)
    s = 3 * 25 + 2 * len(E) - 11 * tt
    degseq = ''.join(f'{k}^{list(d.values()).count(k)} ' for k in sorted(set(d.values())))
    pend = sum(1 for v in V if d[v] == 1)
    print(f'  #{i}: m={len(E)} tau={tt} slack={s} Delta={max(d.values())} degs={degseq} pendants={pend} linear={is_linear(E)} conn={is_connected(E,V)} C={in_class_C(E,V)}')
print('ALL TIGHT CLASS CHECKS OK' if ok_all else 'SOME CHECK FAILED')
