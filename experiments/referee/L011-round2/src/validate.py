"""Referee L011 r2: genbg+hook (classes, tau prune) vs labelled brute force.  sum n!/|Aut| over genbg classes with tau>=T0
must equal the labelled count, for every (n, m, D, T0).  Usage: python3 -I validate.py BIN nlist Dlist"""
import subprocess, sys, math
B = sys.argv[1]; ns = [int(x) for x in sys.argv[2].split(',')]; Ds = [int(x) for x in sys.argv[3].split(',')]
comps = mism = 0
for n in ns:
    for D in Ds:
        for m in range(1, (D * n) // 3 + 1):
            if n > 2 * m + 1: continue
            for T0 in range(1, m + 1):
                g = subprocess.run([B + '/genbg_h', '-q', '-c', '-Z1', '-d1:3', '-D%d:3' % D, str(n), str(m), '%d:%d' % (3*m, 3*m)],
                                   env={'TAU0': str(T0)}, capture_output=True, text=True).stdout
                c = subprocess.run([B + '/canon', str(n)], input=g, capture_output=True, text=True).stdout.split('\n')
                tot = 0; ncls = 0
                for line in c:
                    if not line.strip(): continue
                    aut = int(line.split()[2]); assert math.factorial(n) % aut == 0; tot += math.factorial(n) // aut; ncls += 1
                bfc = int(subprocess.run([B + '/bf', str(n), str(m), str(D), str(T0)], capture_output=True, text=True).stdout)
                comps += 1
                if bfc != tot: mism += 1; print('MISMATCH', n, m, D, T0, bfc, tot)
                if bfc == 0 and ncls == 0: break
        print('n', n, 'D', D, 'done; comparisons so far', comps, 'mismatches', mism, flush=True)
print('comparisons', comps, 'mismatches', mism)
