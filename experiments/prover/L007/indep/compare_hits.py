"""Exact comparison of the hit lists of ext_vertex_all (falsifier) and ext_indep (prover); breakdown by the type of G."""
import re
def parse(path):
    out = []
    for l in open(path):
        if l.startswith('HIT:'):
            out.append(frozenset(tuple(sorted(map(int, t.split(',')))) for t in re.findall(r'\(([\d,]+)\)', l)))
    return out
a = parse('../rerun/ext_vertex_hits.txt'); b = parse('ext_indep_hits.txt')
print('falsifier hits', len(a), 'distinct', len(set(a)), '| prover hits', len(b), 'distinct', len(set(b)))
print('identical as sets:', set(a) == set(b))
g13 = 0; g10 = 0
for h in b:
    G = [e for e in h if 13 not in e]
    if (10, 11, 12) in G and all(max(e) <= 9 for e in G if e != (10, 11, 12)): g10 += 1
    else: g13 += 1
print('hits whose G is a connected (13,8,5) graph:', g13, '; whose G is (10,7,4) + (10,11,12):', g10)
