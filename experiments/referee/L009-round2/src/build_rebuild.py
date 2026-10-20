"""Referee L009 round 2: class-level inputs for the Lemma R rebuild, from my genbg_r2 component cells (in-C classes only, C=1 flag
of r2hooks, validated against defcheck.py).  Components are placed on consecutive vertex blocks.  Writes out/rebuild/in14.txt
(13-vertex graphs) and out/rebuild/in17.txt (16-vertex graphs); one line per graph, edges as (a,b,c)."""
import re, itertools
R = '/home/user/Erdos-757/experiments/referee/L009-round2'
def load(tag):
    L = []
    for line in open('%s/out/cells/g_%s.txt' % (R, tag)):
        if '\tC=1' not in line and ' C=1 ' not in line: continue
        L.append([tuple(map(int, t.split(','))) for t in re.findall(r'\((\d+,\d+,\d+)\)', line.split('E:')[1])])
    return L
EDGE = [[(0, 1, 2)]]
c632, c853, c1074, c1084, c1395, c16106 = (load(t) for t in ('6_3_2_3', '8_5_3_3', '10_7_4_3', '10_8_4_3', '13_9_5_3', '16_10_6_3'))
print('in-C classes per cell:', len(c632), len(c853), len(c1074), len(c1084), len(c1395), len(c16106))
def union(*comps):
    es, off = [], 0
    for c in comps:
        n = max(v for e in c for v in e) + 1
        assert {v for e in c for v in e} == set(range(n))
        es += [tuple(v + off for v in e) for e in c]; off += n
    return es, off
def write(fn, graphs, nv):
    with open(fn, 'w') as f:
        for es in graphs: f.write(' '.join('(%d,%d,%d)' % e for e in es) + '\n')
    print(fn, len(graphs), 'graphs on', nv, 'vertices')
import os; os.makedirs(R + '/out/rebuild', exist_ok=True)
g14 = []
for c in c1395: es, nv = union(c); assert nv == 13; g14.append(es)
for c in c1084: es, nv = union(c, EDGE[0]); assert nv == 13; g14.append(es)
write(R + '/out/rebuild/in14.txt', g14, 13)
g17 = []
for c in c16106: es, nv = union(c); assert nv == 16; g17.append(es)
for c in c1395: es, nv = union(c, EDGE[0]); assert nv == 16; g17.append(es)
for c in c1084: es, nv = union(c, EDGE[0], EDGE[0]); assert nv == 16; g17.append(es)
for a in c1074:
    for b in c632: es, nv = union(a, b); assert nv == 16; g17.append(es)
for a, b in itertools.combinations_with_replacement(range(len(c853)), 2):
    es, nv = union(c853[a], c853[b]); assert nv == 16; g17.append(es)
write(R + '/out/rebuild/in17.txt', g17, 16)
