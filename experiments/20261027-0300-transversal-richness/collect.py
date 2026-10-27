"""Collect connected classes of slack <= 2 (slack = 3n+2m-11tau) from the stored cell lists; highest available D per (n,m,tau).
Writes inputs/cell_<n>_<m>_<tau>.txt (lines: n m tau edges...) and cells.json (source, D)."""
import glob, re, os, json, sys
here = os.path.dirname(os.path.abspath(__file__))
best = {}
for f in glob.glob(os.path.join(here, 'data', '**', 'cell_*.txt'), recursive=True):
    n, m, t, D = map(int, re.match(r'cell_(\d+)_(\d+)_(\d+)_D(\d+)', os.path.basename(f)).groups())
    s = 3 * n + 2 * m - 11 * t
    if not (0 <= s <= 2): continue
    cnt = sum(1 for l in open(f) if l.startswith('FOUND'))
    cur = best.get((n, m, t))
    if cur is None or D > cur[0] or (D == cur[0] and cnt > cur[2]):
        best[(n, m, t)] = (D, f, cnt)
os.makedirs(os.path.join(here, 'inputs'), exist_ok=True)
meta = {}
for (n, m, t), (D, f, cnt) in sorted(best.items()):
    if cnt == 0: continue
    out = []
    for l in open(f):
        if not l.startswith('FOUND'): continue
        E = [tuple(map(int, x)) for x in re.findall(r'\((\d+),(\d+),(\d+)\)', l)]
        assert len(E) == m and max(max(e) for e in E) == n - 1 and len(set(v for e in E for v in e)) == n
        out.append('%d %d %d %s' % (n, m, t, ' '.join('%d %d %d' % e for e in E)))
    assert len(set(out)) == len(out)
    open(os.path.join(here, 'inputs', 'cell_%d_%d_%d.txt' % (n, m, t)), 'w').write('\n'.join(out) + '\n')
    meta['%d_%d_%d' % (n, m, t)] = dict(n=n, m=m, tau=t, slack=3*n+2*m-11*t, D=D, source=os.path.relpath(f, here), classes=len(out))
json.dump(meta, open(os.path.join(here, 'cells.json'), 'w'), indent=1)
for k, v in meta.items(): print(k, v['slack'], 'D<=%d' % v['D'], v['classes'], v['source'])
