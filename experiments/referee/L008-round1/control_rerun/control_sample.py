"""Control (the filters are not vacuous): a random sample of 3,000 extensions H = G + {15,a_i,b_i} of the 149 case-A class inputs
(G = R + (12,13,14), R in O+), WITHOUT the tau >= 7 requirement (so tau(H) >= 6 only), written as HIT lines for filter_hits.
Same admissibility rules as the extension step: pairwise disjoint pairs, no pair inside an edge of G, endpoints of G-degree <= 2."""
import itertools, random
random.seed(2026)
F = '/home/user/Erdos-757/experiments/20261017-0300-n16-via-i11/G_R12_AP.txt'
allext = []
for line in open(F):
    t = list(map(int, line.split()))[1:]; g = [tuple(t[3*k:3*k+3]) for k in range(len(t) // 3)]
    deg = [sum(v in e for e in g) for v in range(15)]
    pairs = [(a, b) for a in range(15) for b in range(a + 1, 15) if deg[a] <= 2 and deg[b] <= 2 and not any(a in e and b in e for e in g)]
    for x, y, z in itertools.combinations(pairs, 3):
        if len({*x, *y, *z}) == 6: allext.append(g + [x + (15,), y + (15,), z + (15,)])
print('all extensions of the 149 inputs:', len(allext))
with open('control_sample_hits.txt', 'w') as f:
    for H in random.sample(allext, 3000):
        f.write('HIT: ' + ' '.join('(%d,%d,%d)' % tuple(sorted(e)) for e in H) + '\n')
