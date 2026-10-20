"""Referee L010 r2: prover's enum_conn vs referee genbg+hooks (validated against brute force for n<=9) at class level, for
connected cells 9 <= n <= NMAX, D in {2,3}, ceil((n-1)/2) <= m <= n-2, thresholds T0 from floor((3n+2m)/11)-1 upward."""
import subprocess, os, sys
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EC = R + '/out/prover_copy/indep/enum_conn'
def classes(lines, n):
    if not lines: return set()
    out = subprocess.run([R + '/bin/canon', str(n)], input='\n'.join(lines) + '\n', capture_output=True, text=True).stdout.split()
    return set(out[0::2])
NMAX = int(sys.argv[1]); tot = bad = 0; nonempty = 0
for n in range(9, NMAX + 1):
    for m in range(n // 2, n - 1):
        if n > 2 * m + 1: continue
        for D in (2, 3):
            if 3 * m > D * n: continue
            for T0 in range(max(1, (3 * n + 2 * m) // 11 - 1), m + 1):
                env = dict(os.environ, TAU0=str(T0), F7PRUNE='0')
                g = [l for l in subprocess.run([R + '/bin/genbg_r2_32', '-q', '-c', '-Z1', '-d1:3', '-D%d:3' % D, str(n), str(m), '%d:%d' % (3*m, 3*m)],
                     capture_output=True, text=True, env=env).stdout.splitlines() if l.startswith('G:')]
                cnt = int(subprocess.run([EC, str(n), str(m), str(T0), str(D), '0'], capture_output=True, text=True).stdout.split('found=')[1])
                if cnt > 2000000: print('skip (too many labelled outputs)', (n, m, T0, D), cnt, flush=True); continue
                ec = [l for l in subprocess.run([EC, str(n), str(m), str(T0), str(D), '1'], capture_output=True, text=True).stdout.splitlines() if l.startswith('FOUND')]
                cg, ce = classes(g, n), classes(ec, n); tot += 1; nonempty += bool(cg)
                if cg != ce: bad += 1; print('MISMATCH', (n, m, T0, D), len(cg), len(ce), flush=True)
                print('cell', (n, m, T0, D), 'classes', len(cg), 'labelled', len(ec), 'same', cg == ce, flush=True)
                if not cg: break
print('enum_conn vs genbg: compared', tot, 'cells (', nonempty, 'nonempty), mismatches', bad)
