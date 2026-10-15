"""cross-check sat14.f7_copies against pchk's F7 flag on SAT models (F7 allowed)."""
import gzip, sys, subprocess, itertools, os
sys.argv = ['x', '14', '8', '/dev/null', 'all']  # not used: we import only the function by exec
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sat14.py')).read()
start = src.index('def f7_copies'); end = src.index('t0 = time.time()')
ns = {'itertools': itertools}; exec(src[start:end], ns)
f7c = ns['f7_copies']
rows = []
for f in sys.stdin.read().split():
    for l in gzip.open(f, 'rt'):
        if l.startswith('#'): continue
        w = l.split(); rows.append([tuple(map(int, t.split(','))) for t in w[1:]])
inp = ''.join(' '.join('%d,%d,%d' % e for e in r) + '\n' for r in rows)
out = subprocess.run([os.path.join(os.path.dirname(os.path.abspath(__file__)), 'pchk'), '14'], input=inp, capture_output=True, text=True).stdout.splitlines()
mism = 0; nf7 = 0; ncopies = 0
for r, o in zip(rows, out):
    f7 = int(o.split()[4]); cp = f7c(sorted(r))
    nf7 += f7; ncopies += len(cp)
    if bool(cp) != bool(f7): mism += 1
    for C in cp:  # each copy: 5 triples, 7 vertices, degrees 3,2,2,2,2,2,2
        deg = {}
        for e in C:
            for v in e: deg[v] = deg.get(v, 0) + 1
        assert len(deg) == 7 and sorted(deg.values()) == [2]*6 + [3], C
print('models', len(rows), 'pchk f7', nf7, 'copies found', ncopies, 'mismatches', mism)
