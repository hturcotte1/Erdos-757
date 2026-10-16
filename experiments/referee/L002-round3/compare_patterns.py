"""Referee round 3: compare two pattern lists as sets.
A: census file (json lines [[i,j,k],...]); B: lines 'i,j,k i,j,k ...'.  Prints sizes, |A-B|, |B-A|."""
import sys, gzip, json, hashlib

def load_census(p):
    S = set()
    for l in gzip.open(p, 'rt'):
        S.add(' '.join('%d,%d,%d' % tuple(e) for e in sorted(map(tuple, json.loads(l)))))
    return S

def load_lines(p):
    S = set(); nl = 0
    for l in gzip.open(p, 'rt'):
        nl += 1
        S.add(' '.join('%d,%d,%d' % t for t in sorted(tuple(map(int, x.split(','))) for x in l.split())))
    return S, nl

A = load_census(sys.argv[1]); B, nb = load_lines(sys.argv[2])
print('census=%d mine_lines=%d mine_distinct=%d census-mine=%d mine-census=%d' % (len(A), nb, len(B), len(A - B), len(B - A)))
for x in list(A - B)[:5]: print('missing from mine:', x)
for x in list(B - A)[:5]: print('extra in mine:', x)
h = hashlib.sha256('\n'.join(sorted(A)).encode()).hexdigest()[:16]; h2 = hashlib.sha256('\n'.join(sorted(B)).encode()).hexdigest()[:16]
print('sha256(sorted census)=%s sha256(sorted mine)=%s' % (h, h2))
