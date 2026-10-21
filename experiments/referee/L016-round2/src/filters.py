"""Own filters on every stored class of the given lists: m, labels, linear, F7-free, (P3), connected on n vertices, exact tau,
Delta <= D (rext filt), and distinctness of classes (labelg)."""
import sys, os, subprocess, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rlib
for path in sys.argv[1:]:
    import re
    n, m, t, D = map(int, re.findall(r'cell_(\d+)_(\d+)_(\d+)_D(\d+)', path)[0])
    reps, info = rlib.read_cell(path)
    lines = ['FOUND: ' + ' '.join('(%d,%d,%d)' % e for e in es) for es in reps]
    r = subprocess.run([rlib.REXT, 'filt', str(n), str(D)], input='\n'.join(lines) + '\n', capture_output=True, text=True)
    rows = [tuple(map(int, l.split())) for l in r.stdout.split('\n') if l.strip()]
    c = collections.Counter(rows)
    good = (n, m, t) 
    ok = sum(v for k, v in c.items() if k[0] == n and k[1] == m and k[2] == t and k[3] <= D and k[4:] == (1, 1, 1, 1))
    labs = all(max(max(e) for e in es) < n and all(len(set(e)) == 3 for e in es) for es in reps) if reps else True
    dist = len(rlib.canon_set_of_reps(reps, n))
    print('%s: classes=%d all_ok=%d (m=%d, tau=%d exactly, Delta<=%d, linear, F7-free, P3, connected) labels_ok=%s distinct_classes=%d INFO=%s | %s' % (
        os.path.basename(path), len(reps), ok, m, t, D, labs, dist, info is not None, r.stderr.strip()))
    if ok != len(reps): print('   FAILURES', [k for k in c if not (k[0] == n and k[1] == m and k[2] == t and k[3] <= D and k[4:] == (1, 1, 1, 1))][:5])
