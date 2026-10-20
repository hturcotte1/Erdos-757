"""(L011) Controls for the extension steps (the pipeline is not vacuous): COUNT random extensions H = G + {NG,a_i,b_i} of random inputs
of SRC (pairwise disjoint pairs, not inside an edge of G, endpoints of G-degree <= 2), WITHOUT the tau requirement, written as HIT
lines for filter_hits (each such H has tau(H) in {tau(G), tau(G)+1}).  For a random input, a uniformly random 3-set of admissible
pairs is drawn and redrawn until the three pairs are pairwise disjoint (rejection sampling: uniform over the admissible triples).
Usage: control22.py SRC NG COUNT SEED OUT"""
import random, sys
src, NG, cnt, seed, outf = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), sys.argv[5]
random.seed(seed)
L = open(src).read().splitlines()
out = []
while len(out) < cnt:
    t = list(map(int, random.choice(L).split()))[1:]; g = [tuple(t[3*k:3*k+3]) for k in range(len(t) // 3)]
    deg = [sum(v in e for e in g) for v in range(NG)]
    pairs = [(a, b) for a in range(NG) for b in range(a + 1, NG) if deg[a] <= 2 and deg[b] <= 2 and not any(a in e and b in e for e in g)]
    if len(pairs) < 3: continue
    for _ in range(100000):
        x, y, z = random.sample(pairs, 3)
        if len({*x, *y, *z}) == 6: break
    else: continue
    out.append(g + [x + (NG,), y + (NG,), z + (NG,)])
with open(outf, 'w') as f:
    for H in out: f.write('HIT: ' + ' '.join('(%d,%d,%d)' % tuple(sorted(e)) for e in H) + '\n')
print(src, 'control extensions written:', len(out), '->', outf)
