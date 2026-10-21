"""Own unpruned final steps of the sparse top cells (no connectivity pruning, F7 and (P3) only counted)."""
import sys, os, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rlib
CF = sys.argv[1]
for (n, m, t, D) in [(27, 13, 10, 2), (27, 14, 10, 3), (27, 18, 11, 2), (27, 19, 11, 3)]:
    for (d, tp, Sp) in rlib.branches(n, m, t, D):
        if tp != t - 1: continue
        decs = rlib.my_decomps(n - 1, m - d, Sp); lines = []; per = []
        for dec in decs:
            L = list(rlib.inputs_for(dec, CF, d, n - 1)); lines += L
            if L: per.append((dec, len(L)))
        r = subprocess.run([rlib.REXT, 'ext', str(n - 1), str(tp), str(d), str(d - 1), 'noconn'], input='\n'.join(lines) + '\n', capture_output=True, text=True)
        print('(%d,%d,%d,%d) d=%d tp=%d S=%d decompositions=%d inputs=%d nonempty=%s | %s' % (n, m, t, D, d, tp, Sp, len(decs), len(lines), per, ' | '.join(r.stderr.strip().splitlines())))
