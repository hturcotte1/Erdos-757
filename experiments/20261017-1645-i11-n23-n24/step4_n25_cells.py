"""Step (4): for every open n=25 violator cell (arith.py), one recursion level of engine.recurse: for each max-degree d and tau' in {t-1,t}
with S' = 3*24+2(m-d)-11 tau' >= 0, the decompositions of (24, m-d) with total slack S' (engine.decompositions) and the component cell types
(n_i,m_i,tau_i) with the degree bound D that the engine would need.  'computed' = a cell file exists in out/cells (from the n=23/24 runs)."""
import os, sys, math, json
os.environ.setdefault('CELLDIR', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'out', 'cells_dummy'))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import engine
from arith import analyse
CELLS = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'out', 'cells')
def valid(n, m, t, D):   # same guard as engine.cell
    return not (m == 0 or t < 1 or t > m or n > 2 * m + 1 or m > n - 2 or 17 * t > 5 * n + 3 * m or D < 1)
out = {}
for r in analyse(25):
    if not r['status'].startswith('OPEN'): continue
    n, m, t, D = r['n'], r['m'], r['tau'], r['dmax']; need = {}; branches = []
    for d in range(max(1, math.ceil(3 * m / n)), D + 1):
        for tp in (t - 1, t):
            Sp = 3 * (n - 1) + 2 * (m - d) - 11 * tp
            if Sp < 0 or tp < 0: continue
            decs = engine.decompositions(n - 1, m - d, Sp)
            types = set(c for dec in decs for c in dec if c != (1, 0, 0))
            branches.append(dict(d=d, tp=tp, Sp=Sp, decompositions=len(decs)))
            for c in types:
                if valid(c[0], c[1], c[2], d): need[(c[0], c[1], c[2], d)] = True
    cells = sorted(need)
    done = [c for c in cells if os.path.exists(os.path.join(CELLS, 'cell_%d_%d_%d_D%d.txt' % c))]
    todo = [c for c in cells if c not in done]
    print('cell (%d,%d,%d) Delta<=%d: branches %s' % (n, m, t, D, [(b['d'], b['tp'], b['Sp'], b['decompositions']) for b in branches]))
    print('   distinct nonempty-guard component cell types: %d, already computed in out/cells: %d, new: %d' % (len(cells), len(done), len(todo)))
    print('   new cells (n,m,tau,D) (n>=?): %s' % todo)
    out['%d_%d_%d_D%d' % (n, m, t, D)] = dict(branches=branches, needed=[list(c) for c in cells], already=[list(c) for c in done], new=[list(c) for c in todo])
json.dump(out, open('step4_n25_cells.json', 'w'), indent=1)
