"""(L013, prover) Remark on n = 27 (descriptive; nothing is decided here).  For each open violator cell at n = 27 (arith13.py) list the
engine's top-level branches (d from ceil(3m/n) to Delta, t' in {tau-1, tau} with S' >= 0) and the decompositions of (26, m-d) with
total slack S', by the engine's generator and by the independent decomp_bf generator (must be EQUAL).  Then the same one level down for
the connected types (26,22,11) and (23,21,10) that the cell (27,25,12,3) needs."""
import sys, os, math
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
os.environ.setdefault('CELLDIR', os.path.join(HERE, 'out', 'cells_dummy'))
import engine
from decomp_bf import bf_decomps
from arith13 import violator_cells
def branches(n, m, t, D):
    out = []
    for d in range(max(1, math.ceil(3 * m / n)), D + 1):
        for tp in (t - 1, t):
            Sp = 3 * (n - 1) + 2 * (m - d) - 11 * tp
            if Sp < 0 or tp < 0: continue
            a = set(tuple(sorted(x)) for x in engine.decompositions(n - 1, m - d, Sp)); b = bf_decomps(n - 1, m - d, Sp)
            out.append((d, tp, Sp, sorted(a), a == b))
    return out
cells = [(c['n'], c['m'], c['tau'], c['dmax']) for c in violator_cells(27) if c['status'].startswith('OPEN')]
print('open violator cells at n = 27:', cells)
for key in cells + [(26, 22, 11, 3), (23, 21, 10, 3)]:
    for d, tp, Sp, decs, eq in branches(*key):
        print("cell %s branch d=%d t'=%d: decompositions of (%d,%d) with total slack %d: %d (two generators %s)" % (key, d, tp, key[0] - 1, key[1] - d, Sp, len(decs), 'EQUAL' if eq else 'DIFFERENT'))
        if key in [(27, 25, 12, 3), (26, 22, 11, 3), (23, 21, 10, 3)]:
            for x in decs: print('      ' + ' + '.join('(%d,%d,%d)' % c for c in x))
print('[(3,1,1),(23,21,10)] is a decomposition of (26,22) with slack 1:', ((3, 1, 1), (23, 21, 10)) in bf_decomps(26, 22, 1))
print('[(3,1,1),(22,18,9)] is a decomposition of (25,19) with slack 3:', ((3, 1, 1), (22, 18, 9)) in bf_decomps(25, 19, 3))
