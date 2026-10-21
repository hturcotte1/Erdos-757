"""genbg (unmodified, MAXN1=30) + own filter for the given keys n,m,t,D; compares the labelg class set with the stored list in CELLDIR."""
import sys, os, subprocess, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rlib
CF = sys.argv[1]; TO = int(sys.argv[2])
GENBG = os.path.join(rlib.R, 'out', 'nauty', 'genbg30')
for key in sys.argv[3:]:
    n, m, t, D = map(int, key.split(','))
    t0 = time.time()
    p = rlib.cell_path(CF, n, m, t, D)
    stored = rlib.read_cell(p)[0] if os.path.exists(p) else None
    cmd = 'set -o pipefail; nice -n 10 timeout %d %s -q -c -Z1 -d1:3 -D%d:3 %d %d %d:%d | nice -n 10 %s gb %d %d %d %d' % (TO, GENBG, D, n, m, 3 * m, 3 * m, rlib.REXT, n, m, t, D)
    r = subprocess.run(cmd, shell=True, capture_output=True, text=True, executable='/bin/bash')
    mine = rlib.labelg_set(r.stdout.split())
    st = rlib.canon_set_of_reps(stored, n) if stored is not None else None
    print('GENBG (%d,%d,%d,%d) rc=%d %s | mine=%d stored=%s equal=%s (%.1fs)' % (n, m, t, D, r.returncode, r.stderr.strip().splitlines()[-1] if r.stderr.strip() else '', len(mine),
          len(stored) if stored is not None else 'NOFILE', (mine == st) if st is not None else '-', time.time() - t0), flush=True)
