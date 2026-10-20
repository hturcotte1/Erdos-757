import json, time, sys
from sat_ref import solve_cell
cells = [(5, 3, 2), (8, 4, 3), (10, 6, 4), (11, 5, 4), (13, 7, 5), (12, 9, 5)]
out = {}
for (n, m, t) in cells:
    t0 = time.time()
    r, edges, info = solve_cell(n, m, t, conn='eager', verbose=True)
    out['%d,%d,%d' % (n, m, t)] = dict(result=r, secs=round(time.time() - t0, 1), per_d0=info['per_d0'])
    print('WINDOW CELL', (n, m, t), r, round(time.time() - t0, 1), 's', flush=True)
    r2, e2, info2 = solve_cell(n, m, t - 1, conn='eager')
    out['%d,%d,%d(control)' % (n, m, t - 1)] = dict(result=r2, witness=e2)
    print('   control', (n, m, t - 1), r2, e2, flush=True)
json.dump(out, open('sat_window_cells.json', 'w'), indent=1)
