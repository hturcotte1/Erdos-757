#!/usr/bin/env python3
"""Referee L016 round 1 (own code): one-level recomputation of a cell (n,m,t,D) from the lower lists.
Every X in C(n,m,t,D) with a vertex w of maximum degree d: ceil(3m/n) <= d <= D, X - w has n-1 vertices, m-d edges,
tau(X-w) = t' in {t-1, t} with S' = 3(n-1)+2(m-d)-11t' >= 0 (components have slack >= 0 by I11 below n), components in
C(.,.,.,d).  For each branch: inputs from my decompositions and the lists with bound d (build_inputs.py), extension by my
program myext2 (TG = t', EP = d-1, DMAX = d; mode 'same' when t' = t), canonical forms with labelg.
Usage: onelevel.py n m t D outprefix   -> prints per-branch counters and the class count; writes outprefix.g6 (classes)."""
import sys, os, math, subprocess
R = '/home/user/Erdos-757/experiments/referee/L016-round1'
n, m, t, D = map(int, sys.argv[1:5]); pre = sys.argv[5]
allX = []
for d in range(max(1, math.ceil(3 * m / n)), D + 1):
    for tp in (t - 1, t):
        Sp = 3 * (n - 1) + 2 * (m - d) - 11 * tp
        if Sp < 0 or tp < 1:
            continue
        inp = '%s_in_d%d_t%d.txt' % (pre, d, tp)
        b = subprocess.run(['python3', R + '/src/build_inputs.py', str(n - 1), str(m - d), str(tp), str(d), inp], capture_output=True, text=True)
        if b.returncode:
            print(b.stderr); raise SystemExit('build failed')
        miss = [l for l in b.stderr.splitlines() if 'MISSING' in l]
        tot = [l for l in b.stderr.splitlines() if l.startswith('TOTAL')][0]
        args = [R + '/bin/myext2', str(n - 1), str(tp), str(d), str(d - 1), str(d)] + (['same'] if tp == t else [])
        with open(inp) as fi:
            out = subprocess.run(args, stdin=fi, capture_output=True, text=True)
        if out.returncode:
            raise SystemExit('myext2 failed rc=%d %s' % (out.returncode, out.stderr))
        xs = [l for l in out.stdout.splitlines() if l.startswith('X:')]
        summ = out.stdout.splitlines()[-1]
        print('branch d=%d t\'=%d S\'=%d: %s | %s | %s' % (d, tp, Sp, tot, summ, ('MISSING lists: ' + '; '.join(miss)) if miss else 'no missing lists'))
        allX += xs
        os.remove(inp)
lab = subprocess.run('python3 %s/src/canon_lines.py %d | %s/bin/labelg -q -f%s | LC_ALL=C sort -u' % (R, n, R, 'a' * n), shell=True,
                     input='\n'.join(allX) + '\n', capture_output=True, text=True).stdout
open(pre + '.g6', 'w').write(lab)
print('CELL (%d,%d,%d,%d): connected survivors %d, classes %d' % (n, m, t, D, len(allX), len(lab.split())))
