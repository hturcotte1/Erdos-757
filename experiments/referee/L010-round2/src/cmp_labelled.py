"""Labelled comparison of hit sets.  Usage: cmp_labelled.py NG inputs.txt(-n format) prover_hits(.gz) my_hits
Hits are compared as sets of sorted edge lists, restricted to the input graphs in inputs.txt (a hit's G-part = its edges
not containing vertex NG)."""
import sys, re, gzip
NG = int(sys.argv[1])
def norm(es): return tuple(sorted(tuple(sorted(e)) for e in es))
S = set()
for l in open(sys.argv[2]):
    a = list(map(int, l.split()));
    if not a: continue
    S.add(norm([a[1+3*i:4+3*i] for i in range(a[0])]))
def hits(fn):
    op = gzip.open if fn.endswith('.gz') else open
    out = set(); n = 0
    with op(fn, 'rt') as f:
        for l in f:
            if not l.startswith('HIT'): continue
            es = [tuple(map(int, t.split(','))) for t in re.findall(r'\(([\d,]+)\)', l.split('|')[0])]
            g = norm([e for e in es if NG not in e])
            if g in S: out.add(norm(es)); n += 1
    return out, n
P, np_ = hits(sys.argv[3]); M, nm = hits(sys.argv[4])
print('inputs', len(S), '| prover hits on these inputs', np_, 'distinct', len(P), '| mine', nm, 'distinct', len(M), '| identical:', P == M)
