"""Referee round 3: compare my F7-free SAT models for given midpoint-1 splits with the census patterns in the same
splits.  Usage: python3 compare_split.py census.jsonl.gz mine_free.txt.gz k1,k2,...  (split = triple (0,1,k))"""
import sys, gzip, json
ks = set(int(x) for x in sys.argv[3].split(','))
A = set()
for l in gzip.open(sys.argv[1], 'rt'):
    es = sorted(map(tuple, json.loads(l)))
    m1 = [e for e in es if e[1] == 1]
    if m1 and m1[0][0] == 0 and m1[0][2] in ks:
        A.add(' '.join('%d,%d,%d' % e for e in es))
B = set()
for l in gzip.open(sys.argv[2], 'rt'):
    B.add(' '.join('%d,%d,%d' % t for t in sorted(tuple(map(int, x.split(','))) for x in l.split())))
print('splits=%s census=%d mine=%d census-mine=%d mine-census=%d' % (sorted(ks), len(A), len(B), len(A - B), len(B - A)))
