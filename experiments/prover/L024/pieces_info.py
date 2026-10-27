"""L024: basic data on the 32 pieces of L* (from experiments/prover/L021/closure_results.json):
n, m, tau, W, degree sequence, max degree, number of minimum transversals, (L1) check.
Supports Lemma A step 2-3 (which members of L* have max degree <= 2; degree-1 vertices of (8,5,3)#0).
Run: timeout 600 nice -n 10 python3 pieces_info.py > pieces_info_output.txt"""
import json, sys
sys.path.insert(0, '/home/user/Erdos-757/experiments/prover/L021')
from kt import tau_masks, masks, min_transversals, A_value
D = json.load(open('/home/user/Erdos-757/experiments/prover/L021/closure_results.json'))
pieces = D['pieces']
print('number of pieces', len(pieces))
for P in pieces:
    n, m, edges = P['n'], P['m'], [tuple(e) for e in P['edges']]
    em = masks(edges)
    t = tau_masks(em)
    assert t == P['tau']
    W = -A_value(n, m, t)
    assert W == P['W']
    deg = [sum(1 for e in edges if x in e) for x in range(n)]
    mts = min_transversals(em, t)
    cov = 0
    for T in mts: cov |= T
    L1 = (cov == (1 << n) - 1)
    deg1 = [x for x in range(n) if deg[x] == 1]
    print(P['name'], 'n', n, 'm', m, 'tau', t, 'W', W, 'maxdeg', max(deg), 'degseq', ''.join(str(d) for d in sorted(deg, reverse=True)),
          '#mintrans', len(mts), 'L1', L1, 'deg1 vertices', deg1, 'edges' if max(deg) <= 2 else '', edges if max(deg) <= 2 else '')
print('pieces with max degree <= 2:', [P['name'] for P in pieces if max(sum(1 for e in P['edges'] if x in e) for x in range(P['n'])) <= 2])
