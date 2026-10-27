#!/usr/bin/env python3
"""Level-by-level generation of all connected members of class C (linear, F7-free, e(S)<=|S|-2) with max degree <= D, up to
isomorphism, for n <= N.  Files out/cls_<n>_<m>.txt hold canon lines ("C m a.b.c ...").  Usage: gen.py N [D=3] [mmin_delta]"""
import os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
CANON = os.path.join(HERE, '..', 'prover', 'L012', 'bin', 'canon')
EXT = os.path.join(HERE, 'bin', 'extend')
OUT = os.path.join(HERE, 'out')
def path(n, m): return os.path.join(OUT, f'cls_{n}_{m}.txt')
def gen(N, D=3, jobs=2):
    os.makedirs(OUT, exist_ok=True)
    with open(path(3, 1), 'w') as f: f.write('C 1 0.1.2\n')
    counts = {(3, 1): 1}
    for m in range(2, N):          # m <= n-2 <= N-2
        cells = [n for n in range(m + 2, min(2 * m + 1, N) + 1)]
        for n in cells:
            if os.path.exists(path(n, m)) and os.path.getsize(path(n, m)) > 0 or (n, m) in counts: continue
            # pipeline: three extension steps -> canon -> sort -u
            cmds = []
            for k in (2, 1, 0):
                npv = n - k
                src = path(npv, m - 1)
                if os.path.exists(src):
                    cmds.append(f'{EXT} {npv} {k} {D} < {src}')
            sh = '( ' + '; '.join(cmds) + f' ) | {CANON} {n} 2>/dev/null | LC_ALL=C sort -u > {path(n, m)}'
            subprocess.run(['nice', '-n', '5', 'bash', '-c', sh], check=True)
            c = sum(1 for _ in open(path(n, m)))
            counts[(n, m)] = c
            print(n, m, c, flush=True)
if __name__ == '__main__':
    N = int(sys.argv[1]); D = int(sys.argv[2]) if len(sys.argv) > 2 else 3
    gen(N, D)
