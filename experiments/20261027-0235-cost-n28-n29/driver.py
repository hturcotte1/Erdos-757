"""Bottom-up exact computation of the cheap missing cells (global budget), measuring classes/nodes/seconds; used to calibrate the cost model."""
import os, sys, time, subprocess, json, math
from plan2 import *
from dag import size_of
BUDGET = float(os.environ.get('BUDGET', '1080')); INLIM = int(os.environ.get('INLIM', '30000')); PERCELL = float(os.environ.get('PERCELL', '120'))
OUTC = os.path.join(HERE, 'out', 'cells')
def cnt(k):
    p = os.path.join(OUTC, 'cell_%d_%d_%d_D%d.txt' % k)
    if not os.path.exists(p): return None
    return sum(1 for l in open(p) if l.startswith('FOUND:'))
seen = {}
for nm in ('n28', 'n29full', 'rec25'): seen.update(build(tops_for(nm)))
order = sorted([k for k, v in seen.items() if not v['exists']], key=lambda k: (k[0], k[1], k[3], k[2]))
t0 = time.time(); log = []
for k in order:
    if time.time() - t0 > BUDGET: print('BUDGET EXHAUSTED'); break
    if cnt(k) is not None: continue
    v = seen[k]; known = {}
    for kk in seen:
        c = cnt(kk)
        if c is not None: known[kk] = c
    tot = 0; unk = set()
    for b in v['branches']:
        for dec in b['decs']:
            sz, u = size_of(dec, known); tot += sz; unk |= set(u)
    if unk: print('BLOCKED', k, 'unknown comps', sorted(unk)); log.append(dict(key=k, status='blocked', inputs_known=tot)); continue
    if not v['direct'] and tot > INLIM: print('SKIP big', k, 'inputs', tot); log.append(dict(key=k, status='skipped_big', inputs=tot)); continue
    rem = BUDGET - (time.time() - t0); to = min(PERCELL, rem)
    s = time.time()
    try:
        r = subprocess.run(['nice', '-n', '10', 'timeout', str(int(to)), 'python3', os.path.join(HERE, 'run_cell.py')] + [str(x) for x in k], capture_output=True, text=True)
        rc = r.returncode
    except Exception as e: rc = -1
    dt = time.time() - s; c = cnt(k)
    print('RAN', k, 'rc', rc, 'secs %.1f' % dt, 'classes', c, 'inputs', tot, flush=True)
    log.append(dict(key=k, status='done' if c is not None else 'timeout', secs=dt, classes=c, inputs=tot))
    json.dump(log, open('driver_log.json', 'w'))
print('TOTAL SECS', time.time() - t0)
