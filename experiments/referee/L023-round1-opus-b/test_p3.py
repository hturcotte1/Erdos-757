"""p3 (Lemma P, matchings) vs brute force on random linear 3-graphs with m <= n-2 built around dense cores
(subsets of the Fano plane / AG(2,3) lines), so that many violate (P3) on a proper subset."""
import random, itertools
from hg import p3, p3_brute, linear
rng = random.Random(11)
fano = [(0,1,2),(0,3,4),(0,5,6),(1,3,5),(1,4,6),(2,3,6),(2,4,5)]
pts = [(x, y) for x in range(3) for y in range(3)]
ag = []
for a, b in itertools.combinations(range(9), 2):
    p, q = pts[a], pts[b]; r = ((-p[0] - q[0]) % 3, (-p[1] - q[1]) % 3); c = pts.index(r)
    t = tuple(sorted((a, b, c)))
    if t not in ag: ag.append(t)
agree = dis = viol = 0
for trial in range(1500):
    core = fano if rng.random() < 0.5 else ag
    k = len(core); n = rng.randint(k if core is fano else 9, 12) if False else rng.randint(7 if core is fano else 9, 12)
    E = rng.sample(core, rng.randint(3, min(len(core), 8)))
    perm = list(range(n)); rng.shuffle(perm)
    E = [tuple(sorted(perm[v] for v in e)) for e in E]
    allt = list(itertools.combinations(range(n), 3)); rng.shuffle(allt)
    for t in allt:
        if len(E) >= n - 2: break
        if rng.random() < 0.3 and linear(E + [t]): E.append(t)
    if len(E) > n - 2 or not linear(E): continue
    a, b = p3(n, E), p3_brute(n, E)
    if a == b: agree += 1
    else: dis += 1; print('DISAGREE', n, E, a, b)
    if not b: viol += 1
print('p3 vs brute force: agree %d disagree %d; violating (P3) %d' % (agree, dis, viol))
