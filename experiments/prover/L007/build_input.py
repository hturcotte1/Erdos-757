"""Rebuild the 796-line input of ext_vertex from the two conn_dfs2_all outputs and compare with the stored file."""
import re, sys
F = '/home/user/Erdos-757/experiments/falsify/i11-inequality/'
def parse(path):
    out = []
    for l in open(path):
        if l.startswith('FOUND:'):
            out.append([tuple(map(int, t.split(','))) for t in re.findall(r'\(([\d,]+)\)', l)])
    return out
g13 = parse('rerun/conn_all_13_8_5.txt'); g10 = parse('rerun/conn_all_10_7_4.txt')
print('parsed', len(g13), 'graphs (13,8,>=5) and', len(g10), 'graphs (10,7,>=4)')
assert all(len(e) == 8 and set().union(*e) == set(range(13)) for e in g13)
assert all(len(e) == 7 and set().union(*e) == set(range(10)) for e in g10)
mine = []
for es in g13: mine.append(es)
for es in g10: mine.append(es + [(10, 11, 12)])
def key(es): return tuple(sorted(tuple(sorted(e)) for e in es))
stored = []
for l in open(F + 'ext_vertex_input.txt'):
    t = list(map(int, l.split()))
    assert t[0] == 8 and len(t) == 25
    stored.append(key([tuple(t[1 + 3*i: 4 + 3*i]) for i in range(8)]))
print('stored lines', len(stored), 'distinct', len(set(stored)))
print('rebuilt lines', len(mine), 'distinct', len(set(map(key, mine))))
print('stored == rebuilt as multisets:', sorted(stored) == sorted(map(key, mine)))
# which stored lines are of which type
n13 = sum(1 for s in stored if s in set(map(key, g13)))
print('stored lines that are (13,8,5) graphs:', n13, '; (10,7,4)+(10,11,12):', len(stored) - n13)
with open('rerun/ext_input_rebuilt.txt', 'w') as f:
    for es in mine:
        f.write('8 ' + ' '.join('%d %d %d' % e for e in es) + '\n')
