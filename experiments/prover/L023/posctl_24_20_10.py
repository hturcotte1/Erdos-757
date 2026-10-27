"""(L023) Positive control for the unrefereed list cell(24,20,10,3): for every X_i and every vertex v of degree 3 such that X_i - v
is connected with maximum degree <= 3, X_i - v (tau = 10 by C8) is a member of C(24,20,10,3) and must occur in the stored list.
Canonical forms by the engine's canon (L012 binary); the stored list lines are canonical representatives."""
import os, sys, re
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'topcell'))
os.environ['CELLDIR'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'topcell', 'cells'); os.environ['ENGINELOG'] = '/dev/null'
import engine
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from verify_c import connected, degrees, tau_exact, in_C
def parse(l): return [tuple(map(int, t.split(','))) for t in re.findall(r'\((\d+,\d+,\d+)\)', l)]
def line(es): return 'FOUND: ' + ' '.join('(%d,%d,%d)' % tuple(sorted(e)) for e in es)
L = set(engine.canon_lines([l.strip() for l in open(os.environ['CELLDIR'] + '/cell_24_20_10_D3.txt') if l.startswith('FOUND:')], 24))
graphs = [parse(l) for l in open('cell_25_23_11_D4.txt') if l.startswith('FOUND:')]
tested = found = 0
for gi, E in enumerate(graphs):
    d = degrees(E, 25)
    for v in range(25):
        if d[v] != 3: continue
        Ev = [e for e in E if v not in e]; idx = {u: i for i, u in enumerate([u for u in range(25) if u != v])}
        Ev = [tuple(idx[u] for u in e) for e in Ev]
        if not connected(Ev, 24) or max(degrees(Ev, 24)) > 3: continue
        assert in_C(Ev, 24)[0] and tau_exact(Ev, 24)[0] == 10
        k = engine.canon_lines([line(Ev)], 24)[0]
        tested += 1; found += (k in L)
        print('X_%d - %d: connected, Delta <= 3, tau = 10, in stored cell(24,20,10,3): %s' % (gi, v, k in L), flush=True)
print('SUMMARY members of C(24,20,10,3) obtained as X_i - v: %d, found in the stored list: %d (list size %d)' % (tested, found, len(L)))
