# Referee round 2: positive controls at n = 23 for rz.  Grow saturated (4,5)-sets from A_base (and from census 14-point sets) by adding
# a new extreme x = 2*max - a (or 2*min - a) that keeps the set a (4,5)-set with exactly one new 3-AP (whose midpoint is the old
# extreme), until 23 points; then the AP pattern has 21 edges and rz must realize it and recover the set.
import itertools, subprocess, json, gzip, random
from fractions import Fraction
def aps(s):
    S = set(s); return [(a, (a + c) // 2, c) for a, c in itertools.combinations(sorted(s), 2) if (a + c) % 2 == 0 and (a + c) // 2 in S]
def is45(s):
    for q in itertools.combinations(s, 4):
        if len(set(abs(x - y) for x, y in itertools.combinations(q, 2))) < 5: return False
    return True
def is45_with(s, x):   # only 4-sets containing x need checking
    for q in itertools.combinations(s, 3):
        q4 = q + (x,)
        if len(set(abs(a - b) for a, b in itertools.combinations(q4, 2))) < 5: return False
    return True
def grow(s, rng):
    s = sorted(s)
    while len(s) < 23:
        m0 = len(aps(s)); cands = []
        for side in (1, -1):
            ext = s[-1] if side == 1 else s[0]
            for a in s:
                if a == ext: continue
                x = 2 * ext - a
                if x in s: continue
                if is45_with(s, x) and len(aps(s + [x])) == m0 + 1: cands.append(x)
        if not cands: return None
        s = sorted(s + [rng.choice(cands)])
    return s
rng = random.Random(23)
seeds = [[0,136,200,243,246,249,272,286,298,323,400,528,596,1056]]
rows = [json.loads(l) for l in gzip.open('/home/user/Erdos-757/data/census_n14_m12_classes.jsonl.gz', 'rt')]
seeds += [sorted(r['set']) for r in rng.sample(rows, 6)]
sets = []
for sd in seeds:
    g = grow(sd, rng)
    if g: sets.append(g)
print('grown 23-point sets:', len(sets))
lines = []
for s in sets:
    E = aps(s); assert len(s) == 23 and len(E) == 21 and is45(s)
    pos = {a: i for i, a in enumerate(s)}
    lab = list(range(23)); rng.shuffle(lab)                      # scramble the labels so the order is not given away
    lines.append('X: ' + ' '.join('(%d,%d,%d)' % tuple(lab[pos[v]] for v in e) for e in E) + '\n')
    sets_lab = None
open('/home/user/Erdos-757/experiments/referee/L012-round2/out/grow23_in.txt', 'w').write(''.join(lines))
out = subprocess.run(['./out/rz', '23', 'print'], stdin=open('/home/user/Erdos-757/experiments/referee/L012-round2/out/grow23_in.txt'), capture_output=True, text=True).stdout.splitlines()
blocks = []; cur = []
for l in out:
    if l.startswith('REAL'): cur.append(l)
    elif l.startswith('G '): blocks.append((l, cur)); cur = []
def canon_aff(vals):
    lo, hi = min(vals), max(vals); a = sorted(Fraction(x - lo) / (hi - lo) for x in vals); b = sorted(1 - x for x in a); return min(tuple(a), tuple(b))
for s, (stat, reals) in zip(sets, blocks):
    target = canon_aff(s); found = 0
    for l in reals:
        y = [int(t) for t in l.split(':')[1].split()]
        if canon_aff(y) == target: found += 1
    h = None
    print('set max %d: %s | realizations %d, own set among them %d' % (s[-1], stat, len(reals), found))
