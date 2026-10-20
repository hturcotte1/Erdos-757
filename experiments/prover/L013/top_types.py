"""(L013, prover) For each top-level branch: every decomposition with the class count of each component cell (type, Delta = d) in the
prover's cell directory, and the resulting number of inputs.  Usage: python3 top_types.py CELLDIR n m t D [...]"""
import sys, os, json, math
cd = sys.argv[1]; a = list(map(int, sys.argv[2:]))
def cnt(n, m, t, D):
    if (n, m) == (1, 0): return 1
    fn = os.path.join(cd, 'cell_%d_%d_%d_D%d.txt' % (n, m, t, D))
    if not os.path.exists(fn): return 0 if (m == 0 or t < 1 or t > m or n > 2 * m + 1 or m > n - 2 or 17 * t > 5 * n + 3 * m) else None
    return sum(1 for l in open(fn) if l.startswith('FOUND:'))
for i in range(0, len(a), 4):
    key = tuple(a[i:i + 4]); info = json.loads([l for l in open(os.path.join(cd, 'cell_%d_%d_%d_D%d.txt' % key)) if l.startswith('INFO ')][0][5:])
    for b in info['branches']:
        print("%s d=%d t'=%d S'=%d:" % (key, b['d'], b['tp'], b['Sp']))
        for dec, size in b['dec']:
            g = {}
            for c in dec: g[tuple(c)] = g.get(tuple(c), 0) + 1
            parts = ['%s(%d,%d,%d)[%s]' % ('%dx' % k if k > 1 else '', t[0], t[1], t[2], cnt(t[0], t[1], t[2], b['d'])) for t, k in sorted(g.items(), key=lambda x: -x[0][0])]
            print('    %-70s -> %d inputs' % (' + '.join(parts), size))
