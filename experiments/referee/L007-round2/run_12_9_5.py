"""Window cell (12,9,5) by SAT.  d0 = max degree >= ceil(3*9/12) = 3 (degree sum 27 > 2*12), and d0 <= 5 (2*d0+1 <= 12),
so the splits d0 = 3, 4, 5 cover every graph.  (d0 = 1 was also run in the first pass: UNSAT.)"""
import time, json
from sat_ref import solve_cell
t0 = time.time()
r, e, info = solve_cell(12, 9, 5, d0s=[3, 4, 5], conn='eager', verbose=True)
print('WINDOW CELL (12,9,5)', r, round(time.time() - t0, 1), 's', json.dumps(info), flush=True)
r2, e2, info2 = solve_cell(12, 9, 4, conn='eager')
print('   control (12,9,4)', r2, e2, flush=True)
