"""Referee L023 round 1: for the five GAP lists of (U1), recompute every branch's input count from its recorded decompositions and
the sizes of the component lists (U1's out/cells; refereed lists where the key is refereed: sizes must then agree with my seeds),
and the trivial guards of engine.cell (own re-implementation of the guard arithmetic). Checks the internal consistency of the record."""
import json, os, re, math
from collections import Counter
U1 = '/home/user/Erdos-757/experiments/20261027-0340-induction-n28-n29-f25/out/cells'
SEED = '/dev/shm/L023ref/engine_run/my_seed_output.txt'
seed = {}
for l in open(SEED):
    m = re.match(r'SEED \((\d+), (\d+), (\d+), (\d+)\) (\d+)', l)
    if m: seed[tuple(map(int, m.groups()[:4]))] = int(m.group(5))
def size(n, m, t, D):
    if (n, m) == (1, 0): return 1
    if m == 0 or t < 1 or t > m or n > 2 * m + 1 or m > n - 2 or 17 * t > 5 * n + 3 * m or D < 1: return 0
    p = os.path.join(U1, 'cell_%d_%d_%d_D%d.txt' % (n, m, t, D))
    s = sum(1 for l in open(p) if l.startswith('FOUND:'))
    if (n, m, t, D) in seed: assert seed[(n, m, t, D)] == s, ('size differs from refereed seed', (n, m, t, D))
    return s
ok = True
for key in ((24, 20, 10, 3), (23, 17, 9, 3), (21, 19, 9, 3), (20, 16, 8, 3), (17, 15, 7, 3)):
    txt = open(os.path.join(U1, 'cell_%d_%d_%d_D%d.txt' % key)).read()
    info = json.loads([l for l in txt.splitlines() if l.startswith('INFO ')][0][5:])
    for br in info['branches']:
        d = br['d']; tot = 0
        for types, sz in br['dec']:
            c = Counter(tuple(t) for t in types); prod = 1
            for (n, m, t), k in c.items():
                s = size(n, m, t, d); prod *= math.comb(s + k - 1, k)
            if prod != sz: ok = False; print('MISMATCH', key, types, prod, sz)
            tot += prod
        print(key, 'branch d=%d tp=%d' % (d, br['tp']), 'recomputed inputs', tot, 'recorded', br['inputs'], 'graphs', br['ext']['graphs'], 'EQUAL' if tot == br['inputs'] == br['ext']['graphs'] else 'DIFF')
        ok &= tot == br['inputs'] == br['ext']['graphs']
print('ALL CONSISTENT' if ok else 'INCONSISTENT')
