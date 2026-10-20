"""Referee L010 r2: test the prover's enum_conn (copy in out/prover_copy/indep) against the labelled brute force bin/bf at
class level.  For connected cells (n, m, T0, D) with n <= NMAX: the set of isomorphism classes of enum_conn's outputs must
equal the set of classes of ALL labelled connected linear 3-graphs with those parameters (brute force, canonicalised by
bin/canon), and every enum_conn output must itself satisfy the parameters (checked by the canonical form being in the bf
set, since bf lists exactly the graphs with the parameters)."""
import subprocess, os, sys
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EC = R + '/out/prover_copy/indep/enum_conn'
def classes(lines, n):
    if not lines: return set()
    out = subprocess.run([R + '/bin/canon', str(n)], input='\n'.join(lines) + '\n', capture_output=True, text=True).stdout.split()
    return set(out[0::2])
NMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 8
tot = bad = 0
for n in range(3, NMAX + 1):
    for m in range((n - 1 + 1) // 2, n + 2):
        if n > 2 * m + 1: continue
        for D in (2, 3, 9):
            if 3 * m > D * n: continue
            env = dict(os.environ, BFPRINT='1')
            bfl = [l for l in subprocess.run([R + '/bin/bf', str(n), str(m), '0', str(D), '1', '1'], capture_output=True, text=True, env=env).stdout.splitlines() if l.startswith('L:')]
            # tau of each labelled graph via the histogram is not per-graph; recompute classes per threshold with bf T0
            for T0 in range(1, m + 2):
                bfT = [l for l in subprocess.run([R + '/bin/bf', str(n), str(m), str(T0), str(D), '1', '1'], capture_output=True, text=True, env=env).stdout.splitlines() if l.startswith('L:')]
                ec = [l for l in subprocess.run([EC, str(n), str(m), str(T0), str(D), '1'], capture_output=True, text=True).stdout.splitlines() if l.startswith('FOUND')]
                cb, ce = classes(bfT, n), classes(ec, n)
                tot += 1
                if cb != ce: bad += 1; print('MISMATCH', (n, m, T0, D), len(cb), len(ce))
                if not bfT: break
print('enum_conn vs brute force: compared', tot, 'cells, mismatches', bad)
