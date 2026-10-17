"""Referee L011: validate the genbg + rhooks pipeline against the labelled brute force rbf.
For n in NS, D in DS: brute-force labelled counts by (m, tau); for every m and every threshold t, run
  TAU0=t rgenbg -q -c -Z1 -d1:3 -D<D>:3 n m 3m:3m
and compare sum over output classes of n!/|Aut| with the number of labelled graphs with tau >= t.
Usage: python3 -I validate.py BIN_DIR n1,n2,... D1,D2,..."""
import subprocess, sys, math, collections, os
B = sys.argv[1]; NS = [int(x) for x in sys.argv[2].split(',')]; DS = [int(x) for x in sys.argv[3].split(',')]
comparisons = mism = 0
for n in NS:
    for D in DS:
        bf = collections.defaultdict(int)
        for l in subprocess.run([B + '/rbf', str(n), str(D)], capture_output=True, text=True, check=True).stdout.split('\n'):
            if l.strip():
                _, _, m, t, c = map(int, l.split()); bf[(m, t)] += c
        ms = sorted({m for (m, t) in bf} | set(range(1, (n * D) // 3 + 1)))
        for m in ms:
            if 3 * m > n * D or n > 2 * m + 1:
                continue
            maxt = max([t for (mm, t) in bf if mm == m], default=0)
            for t in range(0, maxt + 2):
                env = dict(os.environ, TAU0=str(t))
                r = subprocess.run([B + '/rgenbg', '-q', '-c', '-Z1', '-d1:3', '-D%d:3' % D, str(n), str(m), '%d:%d' % (3 * m, 3 * m)],
                                   capture_output=True, text=True, env=env, check=True)
                lines = [l for l in r.stdout.split('\n') if l.startswith('G:')]
                lab = 0
                if lines:
                    c = subprocess.run([B + '/rcanon', str(n), 'G'], input='\n'.join(lines) + '\n', capture_output=True, text=True, check=True)
                    for l in c.stdout.split('\n'):
                        if l.strip():
                            aut = int(l.split()[1]); assert math.factorial(n) % aut == 0
                            lab += math.factorial(n) // aut
                want = sum(c for (mm, tt), c in bf.items() if mm == m and tt >= t)
                comparisons += 1
                if lab != want:
                    mism += 1; print('MISMATCH n=%d D=%d m=%d t=%d genbg_labelled=%d bf=%d' % (n, D, m, t, lab, want))
        print('n=%d D=%d done; brute-force labelled total %d' % (n, D, sum(bf.values())), flush=True)
print('comparisons', comparisons, 'mismatches', mism)
