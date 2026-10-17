"""Control for the final (19,15,8) step (the pipeline is not vacuous): 4,000 random extensions H = G + {18,a_i,b_i} of random inputs of
out/inH19.txt (pairwise disjoint pairs, not inside an edge of G, endpoints of G-degree <= 2), WITHOUT the requirement tau >= 8;
written as HIT lines for filter_hits (every such H has tau >= 7)."""
import itertools, random
random.seed(2028)
L = open('out/inH19.txt').read().splitlines()
out = []
while len(out) < 4000:
    t = list(map(int, random.choice(L).split()))[1:]; g = [tuple(t[3*k:3*k+3]) for k in range(len(t) // 3)]
    deg = [sum(v in e for e in g) for v in range(18)]
    pairs = [(a, b) for a in range(18) for b in range(a + 1, 18) if deg[a] <= 2 and deg[b] <= 2 and not any(a in e and b in e for e in g)]
    trip = [(x, y, z) for x, y, z in itertools.combinations(pairs, 3) if len({*x, *y, *z}) == 6]
    if not trip: continue
    x, y, z = random.choice(trip)
    out.append(g + [x + (18,), y + (18,), z + (18,)])
with open('out/control19_hits.txt', 'w') as f:
    for H in out: f.write('HIT: ' + ' '.join('(%d,%d,%d)' % tuple(sorted(e)) for e in H) + '\n')
print('control extensions written:', len(out))
