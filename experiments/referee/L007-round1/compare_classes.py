"""Compare isomorphism classes of the referee's enumerator output with the prover's/falsifier's output lists."""
import sys, re
sys.path.insert(0, '/home/user/Erdos-757/experiments/referee/L007-round1')
from ref_classes import *
from ref_f7 import has_f7
def P3_ok(es):
    vs = sorted(set(v for e in es for v in e)); n = len(vs)
    # e(S) <= |S|-2 for all S with |S|>=2 : check all subsets (n <= 14 -> 16384)
    idx = {v: i for i, v in enumerate(vs)}; masks = [sum(1 << idx[v] for v in e) for e in es]
    for S in range(1, 1 << n):
        k = bin(S).count('1')
        if k < 2: continue
        if sum(1 for mk in masks if mk & S == mk) > k - 2: return False
    return True
mine = parse_lines(open(sys.argv[1]).read().splitlines(), 'G:')
theirs = parse_lines(open(sys.argv[2]).read().splitlines(), 'FOUND:')
cm = classes(mine); ct = classes(theirs)
print('referee outputs', len(mine), 'classes', len(cm), '| other outputs', len(theirs), 'classes', len(ct))
# match classes
matched = 0
for r in cm:
    if any(nx.is_isomorphic(r[2], q[2], node_match=nm) for q in ct): matched += 1
print('referee classes found in other list:', matched, 'of', len(cm))
matched2 = sum(1 for q in ct if any(nx.is_isomorphic(q[2], r[2], node_match=nm) for r in cm))
print('other classes found in referee list:', matched2, 'of', len(ct))
for r in cm:
    es = r[0]
    print('  class: outputs', r[1], 'tau', tau(es), 'maxdeg', maxdeg(es), '|Aut|', aut(r[2]), 'F7', has_f7(es), 'P3', P3_ok(es))
print('referee outputs containing F7:', sum(has_f7(es) for es in mine), 'of', len(mine))
