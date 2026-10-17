"""(L013, prover) Every cell file lists distinct graphs, and each listed graph is a fixed point of bin/canon (so the lists consist of
distinct nauty canonical forms, one per isomorphism class).  Usage: python3 canon_fixed_points.py CELLDIR"""
import os, subprocess, re, sys
cd = sys.argv[1]; bad = 0; tot = 0; dup = 0
HERE = os.path.dirname(os.path.abspath(__file__))
for fn in sorted(os.listdir(cd)):
    m = re.match(r'cell_(\d+)_(\d+)_(\d+)_D(\d+)\.txt$', fn)
    if not m: continue
    n = int(m.group(1)); L = [l.strip() for l in open(os.path.join(cd, fn)) if l.startswith('FOUND:')]
    dup += len(L) - len(set(L))
    if not L: continue
    out = subprocess.run([os.path.join(HERE, 'bin', 'canon'), str(n)], input='\n'.join(L) + '\n', capture_output=True, text=True).stdout.splitlines()
    assert len(out) == len(L)
    for l, c in zip(L, out):
        e1 = sorted(tuple(map(int, t.split(','))) for t in re.findall(r'\((\d+,\d+,\d+)\)', l))
        e2 = sorted(tuple(map(int, p.split('.'))) for p in c.split()[2:])
        tot += 1; bad += (e1 != e2)
print('representatives: %d; duplicates within a cell: %d; not fixed points of canon: %d' % (tot, dup, bad))
