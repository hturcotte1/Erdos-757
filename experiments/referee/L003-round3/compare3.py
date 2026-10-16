"""Compare sat3 class lists with the census realized sets (census files read as data only).
usage: python3 -I compare3.py n myfile [myfile ...]"""
import sys, gzip, json, glob, math
n = int(sys.argv[1]); mine = set(); dup = 0
for fn in sys.argv[2:]:
    op = gzip.open if fn.endswith('.gz') else open
    for l in op(fn, 'rt'):
        if l.startswith('S '):
            t = tuple(int(v) for v in l.split()[1:1 + n])
            if t in mine: dup += 1
            mine.add(t)
def norm(v):
    v = sorted(v); v = [x - v[0] for x in v]; g = 0
    for x in v: g = math.gcd(g, x)
    v = tuple(x // g for x in v); r = tuple(v[-1] - x for x in reversed(v))
    return min(v, r)
C = '/home/user/Erdos-757/experiments/20261014-1430-small-counts/'
recs = []
if n <= 10:
    recs = json.load(gzip.open(C + 'results/n%d_m%d_real.json.gz' % (n, n - 2), 'rt'))
else:
    for f in sorted(glob.glob(C + 'n11/results/post/real_*.json.gz')): recs += json.load(gzip.open(f, 'rt'))['real']
cen = [norm(r['set']) for r in recs]; cs = set(cen)
print("n=%d mine=%d (dup lines %d) census_records=%d census_classes=%d  mine-census=%d census-mine=%d" %
      (n, len(mine), dup, len(recs), len(cs), len(mine - cs), len(cs - mine)))
