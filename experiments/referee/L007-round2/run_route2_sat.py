"""Route II by SAT: connected linear 3-graphs with n=14, m=11, tau>=6, Delta<=3 and no F7 -> expect UNSAT.
Delta = 3 exactly (degree sum 33 > 2*14), so only d0 = 3 is needed.  Control: same without F7-freeness -> SAT,
and the witness must be isomorphic to D14 (the certificate says the class is unique)."""
import json, time, sys, itertools
import networkx as nx
from sat_ref import solve_cell
from f7_ref import det_A, inc
mode = sys.argv[1]
t0 = time.time()
if mode == 'main':
    r, e, info = solve_cell(14, 11, 6, D=3, f7free=True, d0s=[3], conn='eager', verbose=True)
    print('ROUTE II SAT (14,11,>=6,D<=3,F7-free,connected):', r, round(time.time() - t0, 1), 's', json.dumps(info), flush=True)
else:
    D14 = [(0,1,2),(3,5,6),(0,3,13),(1,5,13),(2,6,13),(4,7,8),(4,9,10),(7,9,11),(8,9,12),(10,11,12),(2,3,4)]
    r, e, info = solve_cell(14, 11, 6, D=3, f7free=False, d0s=[3], conn='eager', verbose=True)
    iso = nx.is_isomorphic(inc(e), inc(D14), node_match=lambda a, b: a['t'] == b['t']) if e else None
    print('CONTROL (no F7 condition):', r, e, 'isomorphic to D14:', iso, 'has F7:', det_A(e) if e else None, round(time.time() - t0, 1), 's', flush=True)
