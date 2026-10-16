"""Compare my saturated (4,5)-sets with h = f(n) (satenum output) with the census realized sets, as affine normal forms.
usage: python3 compare_census.py n mine.txt[.gz] census_real.json.gz [more census files]"""
import sys, json, gzip, math
from fractions import Fraction
F = {6: 4, 7: 5, 8: 5, 9: 6, 10: 6, 11: 7}
def nf(vals):
    v = sorted(Fraction(x) for x in vals)
    lo = v[0]; v = [x - lo for x in v]
    den = 1
    for x in v: den = den * x.denominator // math.gcd(den, x.denominator)
    w = [int(x * den) for x in v]
    g = 0
    for x in w: g = math.gcd(g, x)
    w = [x // g for x in w]
    r = sorted(w[-1] - x for x in w)
    return tuple(min(w, r))
n = int(sys.argv[1]); T = F[n]
op = gzip.open if sys.argv[2].endswith('.gz') else open
mine, mine_pats = set(), 0
hs = {}
with op(sys.argv[2], 'rt') as f:
    for line in f:
        if not line.startswith('SET'): continue
        left = line.split('|')[0].split()
        h = int(left[1]); vals = list(map(int, left[2:]))
        assert len(vals) == n
        hs[h] = hs.get(h, 0) + 1
        if h == T: mine.add(nf(vals)); mine_pats += 1
census = set(); ccount = 0; bad = 0
for fn in sys.argv[3:]:
    d = json.load(gzip.open(fn, 'rt'))
    recs = d['real'] if isinstance(d, dict) else d
    for r in recs:
        ccount += 1
        census.add(nf(r['set']))
print('n=%d my h-hist of output %s; my labelled sets with h=f: %d, my classes: %d; census records: %d, census classes: %d; mine-census=%d census-mine=%d'
      % (n, hs, mine_pats, len(mine), ccount, len(census), len(mine - census), len(census - mine)))
