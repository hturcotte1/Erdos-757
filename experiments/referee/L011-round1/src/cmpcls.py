"""Referee L011: compare two hypergraph lists as sets of isomorphism classes (nauty canonical forms via bin/rcanon).
Usage: cmpcls.py N FILE_A TAG_A FILE_B TAG_B     (TAG 'num' = numeric lines "m a b c ..."; '.gz' files are decompressed)"""
import subprocess, sys, gzip, os
B = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'bin')
def classes(N, f, tag):
    op = gzip.open if f.endswith('.gz') else open
    with op(f, 'rt') as fh:
        if tag == 'num':
            data = ''.join(l for l in fh if l.strip() and l.lstrip()[0].isdigit())
        else:
            data = ''.join(l for l in fh if l.startswith(tag + ':'))
    nlines = data.count('\n')
    if not data: return set(), 0
    r = subprocess.run([os.path.join(B, 'rcanon'), str(N), '*'], input=data, capture_output=True, text=True, check=True)
    return {l.split()[0] for l in r.stdout.split('\n') if l.strip()}, nlines
N = int(sys.argv[1])
a, na = classes(N, sys.argv[2], sys.argv[3]); b, nb = classes(N, sys.argv[4], sys.argv[5])
print('N=%d A=%s[%s]: %d lines, %d classes | B=%s[%s]: %d lines, %d classes | A-B %d, B-A %d, EQUAL=%s' %
      (N, os.path.basename(sys.argv[2]), sys.argv[3], na, len(a), os.path.basename(sys.argv[4]), sys.argv[5], nb, len(b),
       len(a - b), len(b - a), a == b))
