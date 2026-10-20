"""Referee: re-verify every representative of every prover cell with refx check (own code): exactly m distinct triples on 0..n-1,
linear, connected on all n vertices, F7-free (embedding search), (P3) (Hall surplus; and brute force over all edge subsets for m <= 16),
tau == t exactly, maxdeg <= D; and no two representatives isomorphic (labelg canonical forms distinct)."""
import sys, os, re, subprocess
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import myengine as E
bad = 0; tot = 0; cells = 0; brute = 0
for fn in sorted(os.listdir(E.PROVER)):
    mt = re.match(r'cell_(\d+)_(\d+)_(\d+)_D(\d+)\.txt$', fn)
    if not mt: continue
    n, m, t, D = map(int, mt.groups()); cells += 1
    reps = [E.parse_edges(l) for l in open(os.path.join(E.PROVER, fn)) if l.startswith('FOUND:')]
    if not reps: continue
    for r in reps:
        if len(set(r)) != m or any(len(set(e)) != 3 or max(e) >= n or min(e) < 0 for e in r): bad += 1
    inp = ''.join('X: ' + ' '.join('(%d,%d,%d)' % e for e in es) + '\n' for es in reps)
    args = [os.path.join(HERE, 'bin', 'refx'), 'check', str(n)] + (['brute'] if m <= 16 else [])
    out = subprocess.run(args, input=inp, capture_output=True, text=True).stdout.splitlines()
    assert len(out) == len(reps)
    for l in out:
        c = {k: int(v) for k, v in (kv.split('=') for kv in l.split()[1:])}; tot += 1
        ok = c['m'] == m and c['linear'] == 1 and c['connected'] == 1 and c['F7'] == 0 and c['P3'] == 1 and c['tau'] == t and c['maxdeg'] <= D
        if m <= 16: ok = ok and c['P3brute'] == 1; brute += 1
        if not ok: bad += 1; print('BAD', fn, l)
    cf = E.canon(n, m, reps)
    if len(set(cf)) != len(cf): bad += 1; print('DUPLICATE CLASS in', fn)
print('cells %d representatives %d (P3 also by brute force on %d) problems %d' % (cells, tot, brute, bad))
