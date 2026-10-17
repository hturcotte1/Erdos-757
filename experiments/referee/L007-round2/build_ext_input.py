"""Referee L007 r2: build the 796-graph extension input from MY re-run outputs (own parser)."""
import re, sys
def parse(path):
    out = []
    for l in open(path):
        if l.startswith('FOUND:'):
            out.append([tuple(sorted(int(x) for x in t.split(','))) for t in re.findall(r'\(([0-9,]+)\)', l)])
    return out
a = parse('rerun/conn_all_13_8_5.txt'); b = parse('rerun/conn_all_10_7_4.txt')
assert len(a) == 159 and len(b) == 637
assert all(len(g) == 8 and set().union(*g) == set(range(13)) for g in a)
assert all(len(g) == 7 and set().union(*g) == set(range(10)) for g in b)
lines = []
for g in a: lines.append(g)
for g in b: lines.append(g + [(10, 11, 12)])
with open('rerun/ext_input_mine.txt', 'w') as f:
    for g in lines:
        f.write('%d %s\n' % (len(g), ' '.join('%d %d %d' % e for e in g)))
# compare with the falsifier's stored input as a multiset of edge sets
F = '/home/user/Erdos-757/experiments/falsify/i11-inequality/ext_vertex_input.txt'
def parse_in(path):
    out = []
    for l in open(path):
        v = list(map(int, l.split()))
        if not v: continue
        m = v[0]; es = [tuple(sorted(v[1+3*i:4+3*i])) for i in range(m)]
        out.append(frozenset(es))
    return out
from collections import Counter
mine = Counter(frozenset(g) for g in lines); theirs = Counter(parse_in(F))
print('graphs mine', sum(mine.values()), 'distinct', len(mine), '; theirs', sum(theirs.values()), 'distinct', len(theirs), '; equal as multisets:', mine == theirs)
