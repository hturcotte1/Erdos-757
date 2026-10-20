#!/usr/bin/env python3
"""Aggregate out/hist_*.txt (slope*120 histograms per seed set and overlap type) -> out/aggregate.json"""
import glob, json, re, collections
from fractions import Fraction as F
agg = collections.defaultdict(lambda: collections.Counter())
for fn in sorted(glob.glob('out/hist_*.txt')):
    m = re.match(r'out/hist_(n\d+)_', fn); tag = m.group(1)
    for l in open(fn):
        if l.startswith('#HIST'):
            _, t, g, c = l.split(); agg[(tag, t)][int(g)] += int(c)
res = {}
for (tag, t), c in sorted(agg.items()):
    n0 = int(tag[1:])
    res[f'{tag}_{t}'] = {'n0': n0, 'total_survivors': sum(c.values()),
        'slope_hist': {str(F(g, 120)): v for g, v in sorted(c.items())},
        'min_slope': str(F(min(c), 120)), 'min_limit_ratio': str(F(min(c), 120) / (n0 - 2)),
        'below_5_9': sum(v for g, v in c.items() if F(g, 120) / (n0 - 2) < F(5, 9)),
        'equal_5_9': sum(v for g, v in c.items() if F(g, 120) / (n0 - 2) == F(5, 9))}
json.dump(res, open('out/aggregate.json', 'w'), indent=1)
for k, v in res.items(): print(k, v['total_survivors'], 'min slope', v['min_slope'], 'min ratio', v['min_limit_ratio'], float(F(v['min_limit_ratio'])), 'below', v['below_5_9'], 'eq', v['equal_5_9'])
