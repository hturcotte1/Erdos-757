import json
from fractions import Fraction as F
for l in open('/home/user/Erdos-757/experiments/referee/L006-round2/routeV_control.jsonl'):
    r = json.loads(l)
    u, v = map(int, r['class'].split('-')[-2:])
    hit_pt = any(d[0] == 'vertex' and {F(d[1]), F(d[2])} == {u, v} for d in r['deficient'])
    hit_line = [d for d in r['deficient'] if d[0] == 'line' and (d[1][0] * u + d[1][1] * v + d[1][2] == 0 or d[1][0] * v + d[1][1] * u + d[1][2] == 0)]
    print(r['class'], 'hA', r['hA'], 'target', r['target'], 'n_deficient', r['n_deficient'], 'min_h', r['min_h'],
          '| (u,v) is a deficient vertex:', hit_pt, '| (u,v) on a deficient line:', [(d[1], d[4]) for d in hit_line])
