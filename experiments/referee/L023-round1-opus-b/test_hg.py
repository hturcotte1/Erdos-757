"""Unit tests of hg.py: canon invariance under random relabelling and separation; p3 vs brute force; F7 detection; tau vs brute force."""
import random, itertools, time, sys
from hg import *
rng = random.Random(7)
F = '/home/user/Erdos-757/experiments/20261027-0340-induction-n28-n29-f25/out/cells/cell_20_16_8_D3.txt'
G = []
with open(F) as f:
    for l in f:
        if l.startswith('FOUND'):
            G.append(parse(l))
            if len(G) >= 1500: break
t0 = time.time(); forms = set(); maxleaves = 0
for E in G:
    c, lv = canon(20, E); forms.add(c); maxleaves = max(maxleaves, lv)
print('canon on first %d stored (20,16,8,3) graphs: %.1f ms each, max leaves %d, distinct forms %d' % (len(G), 1000 * (time.time() - t0) / len(G), maxleaves, len(forms)))
bad = 0
for E in G[:300]:
    p = list(range(20)); rng.shuffle(p)
    E2 = [tuple(p[v] for v in e) for e in E]; rng.shuffle(E2)
    if canon(20, E2)[0] != canon(20, E)[0]: bad += 1
print('relabelling invariance failures on 300 graphs:', bad)
# p3 vs brute force, linear random 3-graphs on 8-9 vertices
agree = dis = viol = 0
for trial in range(400):
    n = rng.choice([7, 8, 9]); allt = list(itertools.combinations(range(n), 3)); rng.shuffle(allt)
    E = []
    for t in allt:
        if len(E) >= rng.randint(3, n): break
        if linear(E + [t]): E.append(t)
    a, b = p3(n, E), p3_brute(n, E)
    if a == b: agree += 1
    else: dis += 1
    if not b: viol += 1
print('p3 vs brute force: agree %d disagree %d (violating %d)' % (agree, dis, viol))
F7 = [(0,1,2),(0,3,4),(0,5,6),(1,3,5),(2,4,6)]
p = list(range(9)); rng.shuffle(p)
print('F7 detected:', has_F7(7, F7), 'relabelled with pendant edge:', has_F7(9, [tuple(p[v] for v in e) for e in F7] + [(p[6], p[7], p[8])]),
      'Fano minus... grid 3x3 lines (no F7):', has_F7(9, [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8)]))
# tau vs brute force
bad = 0
for E in G[:200]:
    t = tau(20, E)
    bt = min(k for k in range(21) if any(all(set(e) & set(S) for e in E) for S in itertools.combinations(range(20), k))) if False else None
    if t != 8: bad += 1
print('tau == 8 on the first 200 stored graphs: failures', bad)
for trial in range(100):
    n = 9; allt = list(itertools.combinations(range(n), 3)); rng.shuffle(allt); E = allt[:rng.randint(2, 9)]
    bt = min(k for k in range(n + 1) if any(all(set(e) & set(S) for e in E) for S in itertools.combinations(range(n), k)))
    if tau(n, E) != bt: bad += 1
    cv = covers_upto(n, E, bt)
    bf = [S for S in itertools.combinations(range(n), bt) if all(set(e) & set(S) for e in E)]
    if sorted(cv) != sorted(sum(1 << v for v in S) for S in bf): bad += 1
print('tau and min covers vs brute force (100 random 9-vertex 3-graphs): failures', bad)
