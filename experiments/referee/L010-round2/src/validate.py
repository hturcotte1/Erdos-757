"""Referee L010 r2: validate genbg+hooks (bin/genbg_r2_32) against the labelled brute force bin/bf.
For each (n, m, D, dmin, conn): bf gives labelled counts by tau (all, and in C).  For every threshold T0 (0..maxtau+1) and
F7PRUNE in {0,1}: genbg outputs must be pairwise non-isomorphic (canonical forms), and sum n!/|Aut| over the outputs must
equal the labelled count with tau >= T0 (F7PRUNE=0, all outputs; and outputs with f7=0,p3=1 vs the in-C count), and with
F7PRUNE=1 the outputs with p3=1 must give the in-C count."""
import subprocess, sys, os, math
from fractions import Fraction
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def bf(n, m, D, dmin, conn):
    o = subprocess.run([R + '/bin/bf', str(n), str(m), '0', str(D), str(dmin), str(conn)], capture_output=True, text=True).stdout
    h = o.split('hist')[1].split()
    return {int(x.split(':')[0]): (int(x.split(':')[1]), int(x.split(':')[2])) for x in h}
def genbg(n, m, D, dmin, conn, T0, f7p):
    env = dict(os.environ, TAU0=str(T0), F7PRUNE=str(f7p))
    args = [R + '/bin/genbg_r2_32', '-q'] + (['-c'] if conn else []) + ['-Z1', '-d%d:3' % dmin, '-D%d:3' % D, str(n), str(m), '%d:%d' % (3*m, 3*m)]
    p = subprocess.run(args, capture_output=True, text=True, env=env)
    lines = [l for l in p.stdout.splitlines() if l.startswith('G:')]
    if not lines: return []
    c = subprocess.run([R + '/bin/canon', str(n)], input='\n'.join(lines) + '\n', capture_output=True, text=True).stdout.split('\n')
    out = []
    for l, cl in zip(lines, c):
        can, aut = cl.split()
        flags = dict(kv.split('=') for kv in l.split('|')[1].split())
        out.append((can, int(aut), int(flags['tau']), int(flags['f7']), int(flags['p3']), int(flags['conn'])))
    return out
cases = []
for n in range(3, 9):
    for D in (2, 3):
        for m in range(1, min(n, 8) + 1):
            for conn in (0, 1):
                for dmin in ((0, 1) if not conn else (1,)):
                    cases.append((n, m, D, dmin, conn))
for (m, D) in [(4, 3), (6, 3), (7, 3), (6, 2), (7, 2)]:
    for conn in (0, 1): cases.append((9, m, D, 1, conn))
ncmp = 0; bad = 0
for (n, m, D, dmin, conn) in cases:
    if 3*m < dmin*n or 3*m > D*n: continue
    h = bf(n, m, D, dmin, conn)
    taus = [t for t in h if h[t][0] > 0]; tmax = max(taus) if taus else 0
    for T0 in range(0, tmax + 2):
        lab = sum(h[t][0] for t in h if t >= T0); labC = sum(h[t][1] for t in h if t >= T0)
        for f7p in (0, 1):
            g = genbg(n, m, D, dmin, conn, T0, f7p)
            cans = [x[0] for x in g]
            dup = len(cans) != len(set(cans))
            s_all = sum(Fraction(math.factorial(n), x[1]) for x in g)
            s_C = sum(Fraction(math.factorial(n), x[1]) for x in g if x[3] == 0 and x[4] == 1)
            okconn = all(x[5] == 1 for x in g) if conn else True
            ok = (not dup) and okconn and s_C == labC and (f7p == 1 or s_all == lab) and all(x[2] >= T0 for x in g)
            ncmp += 1
            if not ok:
                bad += 1; print('MISMATCH', (n, m, D, dmin, conn, T0, f7p), 'bf', lab, labC, 'genbg', s_all, s_C, 'dup', dup)
    print('case', (n, m, D, dmin, conn), 'tau hist', {t: h[t] for t in taus}, flush=True)
print('compared', ncmp, 'mismatches', bad)
