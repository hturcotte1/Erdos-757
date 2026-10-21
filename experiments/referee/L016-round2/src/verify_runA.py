"""Referee: verify the 45 run-A lists of L016 (keys of listA.txt) with own programs.
 - m <= 10 ('direct' cells): unmodified nauty genbg (MAXN1=30 build) -c -Z1 -d1:3 -D<D>:3 n m 3m:3m, own filter (rext gb: linear,
   F7-free, (P3), connected, Delta <= D, tau == t), labelg; compared with the stored list (labelg of rext g6).
 - m > 10: own recursion step (recompute.py: own decompositions, own inputs, rext ext, labelg) from the lower lists of cellsF.
   Keys are processed in increasing n, so every lower list used was either a refereed seed or already verified here."""
import sys, os, subprocess, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rlib
CF = '/home/user/Erdos-757/experiments/prover/L016/out/cellsF'
GENBG = os.path.join(rlib.R, 'out', 'nauty', 'genbg30')
keys = [tuple(map(int, x.split(','))) for x in open('/home/user/Erdos-757/experiments/prover/L016/listA.txt').read().split()]
only = sys.argv[1] if len(sys.argv) > 1 else 'all'
keys.sort(key=lambda k: (k[0], k[1]))
for (n, m, t, D) in keys:
    if only == 'direct' and m > 10: continue
    if only == 'recurse' and m <= 10: continue
    if only == 'top' and n != 27: continue
    if only == 'nottop' and n == 27: continue
    t0 = time.time()
    stored, info = rlib.read_cell(rlib.cell_path(CF, n, m, t, D))
    st = rlib.canon_set_of_reps(stored, n)
    if m <= 10:
        cmd = 'nice -n 10 timeout 1800 %s -q -c -Z1 -d1:3 -D%d:3 %d %d %d:%d | nice -n 10 %s gb %d %d %d %d' % (GENBG, D, n, m, 3 * m, 3 * m, rlib.REXT, n, m, t, D)
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True, executable='/bin/bash')
        mine = rlib.labelg_set(r.stdout.split())
        print('DIRECT  (%d,%d,%d,%d) genbg+filter: %s | mine=%d stored=%d equal=%s (%.1fs)' % (n, m, t, D, r.stderr.strip().splitlines()[-1] if r.stderr.strip() else 'rc=%d' % r.returncode, len(mine), len(stored), mine == st, time.time() - t0), flush=True)
    else:
        r = subprocess.run(['python3', os.path.join(rlib.R, 'src', 'recompute.py'), str(n), str(m), str(t), str(D), CF], capture_output=True, text=True)
        lines = r.stdout.strip().splitlines()
        res = [l for l in lines if l.startswith('RESULT')]
        flags = [l for l in lines if 'decomps_equal_to_INFO=False' in l or 'MISMATCH' in l or 'MISSING' in l]
        print('RECURSE (%d,%d,%d,%d) %s %s' % (n, m, t, D, res[0] if res else ('FAILED ' + r.stderr[-300:]), ('FLAGS: ' + ' || '.join(flags)) if flags else ''), flush=True)
