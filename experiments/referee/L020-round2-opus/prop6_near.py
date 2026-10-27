"""Diagnose the 5.2 sentence '1+2+2=5 vertices other than x,y': list the failure kinds and show an example."""
from collections import Counter
import prop6_check as P   # re-runs the check (small) and exposes 'fails'
from hgr2 import parse_list
print('fail kinds:', Counter(f[0] for f in P.fails))
c, gi, x, y = P.fails[0][1:5]
n, m, t, E = parse_list(P.I + c + '.txt')[gi]
print('example', c, 'class', gi, 'NC pair', (x, y), 'edges meeting {x,y}:', [e for e in E if x in e or y in e])
