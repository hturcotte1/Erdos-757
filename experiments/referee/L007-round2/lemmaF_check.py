import itertools
from f7_ref import det_A, is_linear, F7
T = list(itertools.combinations(range(7), 3))
tot = agree = 0
for five in itertools.combinations(T, 5):
    if set().union(*five) != set(range(7)) or not is_linear(five): continue
    deg = {}
    for e in five:
        for v in e: deg[v] = deg.get(v, 0) + 1
    lf = sorted(deg.values()) == [2, 2, 2, 2, 2, 2, 3]
    tot += 1; agree += (lf == det_A(five))
print('Lemma F vs definition on all linear 5-edge 3-graphs spanning [7]:', tot, 'agree', agree)
ext = [e for e in T if e not in F7 and is_linear(F7 + [e])]
print('triples on [7] that can be added to F7 keeping linearity:', ext)
