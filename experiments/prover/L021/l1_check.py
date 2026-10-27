"""L021: property (L1) for the 32 pieces: every vertex lies in some minimum transversal (exact enumeration)."""
import sys, json
sys.path.insert(0, '/home/user/Erdos-757/experiments/prover/L021')
from kt import *
R = json.load(open('/home/user/Erdos-757/experiments/prover/L021/closure_results.json'))
bad = 0
for p in R['pieces']:
    P = Piece(p['edges'], p['name']); T = min_transversals(masks(P.edges), P.tau)
    U = 0
    for t in T: U |= t
    ok = U == (1 << P.n) - 1
    bad += (not ok)
    print(P.name, 'tau', P.tau, '#min transversals', len(T), 'every vertex in one:', ok, 'W', P.W, 'max deg', max(P.deg))
print('L1 failures:', bad, 'of', len(R['pieces']), '; max W =', max(p['W'] for p in R['pieces']), '(edge cost 35)')
