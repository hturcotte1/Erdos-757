"""Route II by SAT with lex-leader symmetry breaking (validated on n<=9 and by class coverage): n=14, m=11, tau>=6,
Delta<=3 (so d0=3), connected (eager cuts), linear, F7-free -> expect UNSAT.  Control: no F7 condition -> SAT, iso D14."""
import json, time, sys
import networkx as nx
from sat_ref import solve_cell
from f7_ref import det_A, inc
mode = sys.argv[1]; t0 = time.time()
D14 = [(0,1,2),(3,5,6),(0,3,13),(1,5,13),(2,6,13),(4,7,8),(4,9,10),(7,9,11),(8,9,12),(10,11,12),(2,3,4)]
f7 = (mode == 'main')
r, e, info = solve_cell(14, 11, 6, D=3, f7free=f7, d0s=[3], conn='eager', verbose=True, lexleader=True)
iso = nx.is_isomorphic(inc(e), inc(D14), node_match=lambda a, b: a['t'] == b['t']) if e else None
print('ROUTE II LEX', mode, r, e, 'iso D14:', iso, 'hasF7:', det_A(e) if e else None, round(time.time() - t0, 1), 's', json.dumps(info), flush=True)
