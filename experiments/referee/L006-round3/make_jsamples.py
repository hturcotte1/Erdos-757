"""Generate sample (4,5) two-point extensions (own code) of types T1a, T1b, T2-generic for 3 classes, for the frozen judge."""
import gzip, json, itertools, random
def nd(q): return len({abs(u - v) for u, v in itertools.combinations(q, 2)})
def is45(P): return all(nd(q) >= 5 for q in itertools.combinations(P, 4))
def third(P):
    out = set()
    for a, b in itertools.combinations(P, 2):
        if (a + b) % 2 == 0: out.add((a + b) // 2)
        out.add(2 * a - b); out.add(2 * b - a)
    return out - set(P)
cen = json.load(gzip.open('/home/user/Erdos-757/experiments/20261014-1005-census-dfs/results/realized_n12.json.gz', 'rt'))
rnd = random.Random(808)
for c in (54242, 2, 30954):
    A = sorted(4 * a for a in cen[c]['set']); Px = third(A)
    singles = sorted(x for x in Px if is45(A + [x]))
    x = singles[len(singles) // 2]
    # T1a: y generic (in no 3-AP of B)
    while True:
        y = rnd.randrange(10**7, 10**8)
        B = sorted(A + [x, y])
        if y not in third(A + [x]) and is45(B): break
    samples = [('T1a', B)]
    # T1b: y in a 3-AP with two points of A u {x}
    for y in sorted(third(A + [x])):
        B = sorted(A + [x, y])
        if y not in A and is45(B): samples.append(('T1b', B)); break
    # T2 generic: {a, x, y} with x the midpoint (y = 2x - a), x,y generic
    a = A[3]
    while True:
        x2 = rnd.randrange(10**6, 10**7); y2 = 2 * x2 - a
        B = sorted(A + [x2, y2])
        if x2 not in Px and y2 not in Px and is45(B): samples.append(('T2', B)); break
    for t, B in samples:
        cid = 'R3-L006-c%d-%s' % (c, t)
        json.dump({'id': cid, 'type': 'construction', 'set': B, 'claimed_h': 9, 'notes': 'referee round 3 L006 sample, class %d (x4 coords), type %s' % (c, t)},
                  open('jsamples/%s.json' % cid, 'w'))
        print(cid, B)
