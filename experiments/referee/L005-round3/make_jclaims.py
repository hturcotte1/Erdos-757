"""Build frozen-judge spot-check claim files from ATE outputs (pairs) plus a T1a-type, a T2-type and a negative example."""
import json, gzip
from fractions import Fraction as Fr
from math import lcm
OUT = '/home/user/Erdos-757/experiments/referee/L005-round3/jclaims/'
rows = {}
for fn in ['ate_2440.jsonl', 'ate_a.jsonl', 'ate_b.jsonl', 'ate_c.jsonl', 'ate_d.jsonl']:
    for l in open(fn):
        r = json.loads(l); rows[r['class']] = r
census = {}
with gzip.open('/home/user/Erdos-757/data/census_n14_m12_classes.jsonl.gz', 'rt') as f:
    for i, l in enumerate(f):
        if i in rows: census[i] = json.loads(l)['set']
def write(name, A, pts, claimed, note):
    D = 1
    for p in pts: D = lcm(D, Fr(p).denominator)
    S = sorted([a * D for a in A] + [int(Fr(p) * D) for p in pts])
    json.dump({'id': name, 'type': 'construction', 'set': S, 'claimed_h': claimed, 'notes': note}, open(OUT + name + '.json', 'w'))
for c in (2440, 1524, 2564, 1829, 941):
    ps = rows[c]['pairs45']; p = ps[len(ps) // 2]
    write('R3-L005-c%d-pair' % c, census[c], p, 10, 'referee round 3: class %d plus ATE (4,5) pair %s' % (c, p))
A = census[2440]
write('R3-L005-c2440-T1a', A, [Fr(298 + 400, 2), Fr(100001, 7)], 10, 'x = midpoint 349 of 298,400 (A u {x} (4,5)?), y generic')
write('R3-L005-c2440-T2', A, [Fr(100003, 7), Fr(200006, 7) - 136], 10, 'T2 line y = 2x - 136, generic x')
write('R3-L005-c2440-NEG', A, [Fr(5000), Fr(5000 + 136 - 0)], 10, 'negative: x - y = 0 - 136 (F line), must FAIL (4,5)')
print('written')
