import sys, re
sys.path.insert(0, '/home/user/Erdos-757/experiments/referee/L007-round1')
from ref_f7 import f7_copies, is_linear
from ref_classes import classes, maxdeg, tau, aut, nm
import networkx as nx
hits = []
for l in open('out/ref_ext_hits.txt'):
    if l.startswith('HIT:'):
        hits.append([tuple(sorted(map(int, t.split(',')))) for t in re.findall(r'\(([\d,]+)\)', l)])
print('hits', len(hits), 'linear', sum(is_linear(h) for h in hits))
nof7 = [h for h in hits if not f7_copies(h, True)]
print('hits without F7:', len(nof7))
# hits from (10,7,4)+edge inputs: the last 3 edges contain 13; the first 8 are the input graph
from10 = [h for h in hits if (10,11,12) in h[:8]]
print('hits from (10,7,4)+edge inputs:', len(from10), '; from (13,8,5) inputs:', len(hits) - len(from10))
# every F7 copy uses vertex 13?  (for the F7-free (10,7,4) classes)
use13 = 0
for h in from10:
    cps = f7_copies(h)
    if all(any(13 in h[i] for i in c) for c in cps): use13 += 1
print('hits from (10,7,4)+edge where every F7 copy uses vertex 13:', use13)
# classes of hits and their max degrees
cl = classes(hits)
print('isomorphism classes of hits:', len(cl), ' by maxdeg:', sorted((maxdeg(r[0]), r[1]) for r in cl))
