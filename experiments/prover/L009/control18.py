"""Control for the final step (the pipeline is not vacuous): 2,000 random extensions H = G + {17,a_i,b_i} of random final-step inputs
(pairwise disjoint pairs, not inside an edge of G, endpoints of G-degree <= 2), WITHOUT the requirement tau >= 8; written as HIT lines for
filter_hits.  Every such H has tau >= 7 (it contains G)."""
import itertools, random
random.seed(2027)
L = open('rerun/inH18.txt').read().splitlines()
out = []
while len(out) < 2000:
    t = list(map(int, random.choice(L).split()))[1:]; g = [tuple(t[3*k:3*k+3]) for k in range(len(t) // 3)]
    deg = [sum(v in e for e in g) for v in range(17)]
    pairs = [(a, b) for a in range(17) for b in range(a + 1, 17) if deg[a] <= 2 and deg[b] <= 2 and not any(a in e and b in e for e in g)]
    trip = [(x, y, z) for x, y, z in itertools.combinations(pairs, 3) if len({*x, *y, *z}) == 6]
    if not trip: continue
    x, y, z = random.choice(trip)
    out.append(g + [x + (17,), y + (17,), z + (17,)])
with open('control18_hits.txt', 'w') as f:
    for H in out: f.write('HIT: ' + ' '.join('(%d,%d,%d)' % tuple(sorted(e)) for e in H) + '\n')
print('control extensions written:', len(out))
