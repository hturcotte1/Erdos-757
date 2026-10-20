"""Referee L009: class-level inputs for the rebuild (Lemma R) and the final step, from the referee's own genbg outputs.
Each component type is represented by the genbg class representatives lying in C (lines 'G tau=.. C=1:').
Writes 'I:' lines (disjoint unions on consecutive vertex blocks)."""
import re, sys, itertools
D = '/home/user/Erdos-757/experiments/referee/L009-round1/out/'
def reps(cell, tag='G', need='C=1'):
    L = []
    for l in open(D + 'g_%s.txt' % cell):
        if l.startswith(tag) and need in l.split(':')[0]:
            L.append([tuple(map(int, t.split(','))) for t in re.findall(r'\(([\d,]+)\)', l)])
    return L
E = [[(0, 1, 2)]]
def nv(es): return max(max(e) for e in es) + 1
def union(parts):
    out = []; off = 0
    for es in parts:
        n = nv(es); assert set().union(*es) == set(range(n))
        out += [tuple(v + off for v in e) for e in es]; off += n
    return out, off
def write(fn, combos, N):
    with open(D + fn, 'w') as f:
        for parts in combos:
            es, n = union(parts); assert n == N, (n, N)
            f.write('I: ' + ' '.join('(%d,%d,%d)' % e for e in es) + '\n')
    print(fn, len(combos), 'inputs on', N, 'vertices')
R = {c: reps(c) for c in ['6_3_2', '8_5_3', '10_7_4', '10_8_4', '13_9_5', '16_10_6']}
print({c: len(v) for c, v in R.items()})
# (16,10) slack-2 types of Lemma R
c17 = [[a] for a in R['16_10_6']] + [[a] + E for a in R['13_9_5']] + [[a] + E + E for a in R['10_8_4']] \
    + [[a, b] for a in R['10_7_4'] for b in R['6_3_2']] + [[a, b] for a, b in itertools.combinations_with_replacement(R['8_5_3'], 2)]
write('in17_classlevel.txt', c17, 16)
# (13,9) slack-2 types
c14 = [[a] for a in R['13_9_5']] + [[a] + E for a in R['10_8_4']]
write('in14_classlevel.txt', c14, 13)
