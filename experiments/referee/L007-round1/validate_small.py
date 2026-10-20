"""Validate ref_enum against ref_bf for all cells with 3 <= n <= NMAX: for every m, every t in 0..taumax+1 and every
D in {1,2,3,maxdeg,1000}, the labelled count of connected spanning linear 3-graphs with tau>=t, maxdeg<=D (brute force)
must equal sum n!/|Aut| over the isomorphism classes output by ref_enum n m t D (and every output must have the
required parameters).  Also checks the closed-component prune (L5) against runs without it."""
import sys, subprocess, math, json
sys.path.insert(0, '/home/user/Erdos-757/experiments/referee/L007-round1')
from ref_classes import *
NMAX = int(sys.argv[1])
D0 = '/home/user/Erdos-757/experiments/referee/L007-round1/'
res = dict(cells=0, mismatches=0, nonempty=0, bad_params=0, close_mismatch=0)
for n in range(3, NMAX + 1):
    bf = {}
    for l in open(D0 + 'bf/bf_%d.txt' % n):
        a = list(map(int, l.split())); bf[(a[1], a[2], a[3])] = a[4]
    ms = sorted(set(k[0] for k in bf))
    for m in range(1, n):            # linear 3-graphs on n vertices: m <= n(n-1)/6 ; connected: n <= 2m+1
        if 2 * m + 1 < n or m > n * (n - 1) // 6: continue
        taumax = max([k[1] for k in bf if k[0] == m], default=0)
        dmx = max([k[2] for k in bf if k[0] == m], default=0)
        for close in (1, 0):
            for t in range(0, taumax + 2):
                for D in sorted(set([1, 2, 3, dmx, 1000])):
                    if close == 0 and not (t == 0 and D == 1000): continue
                    p = subprocess.run([D0 + 'ref_enum', str(n), str(m), str(t), str(D), '1', str(close)], capture_output=True, text=True)
                    gs = parse_lines(p.stdout.splitlines())
                    for es in gs:
                        if len(es) != m or set(v for e in es for v in e) != set(range(n)) or tau(es) < t or maxdeg(es) > D:
                            res['bad_params'] += 1
                    cl = classes(gs)
                    lab = sum(math.factorial(n) // aut(r[2]) for r in cl)
                    want = sum(c for (mm, tt, dd), c in bf.items() if mm == m and tt >= t and dd <= D)
                    res['cells'] += 1
                    if lab != want:
                        res['mismatches'] += 1; print('MISMATCH', n, m, t, D, close, lab, want, flush=True)
                    if want: res['nonempty'] += 1
print(json.dumps(res))
