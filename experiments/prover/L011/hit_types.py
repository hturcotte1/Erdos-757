"""(L011, descriptive) Classify HIT lines by the component vertex counts of the input graph G (the first M edges of the line, on
vertices 0..NG-1).  Usage: hit_types.py FILE M NG"""
import re, sys, collections
f, M, NG = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]); c = collections.Counter()
for l in open(f):
    if not l.startswith('HIT:'): continue
    es = [tuple(map(int, t.split(','))) for t in re.findall(r'\(([\d,]+)\)', l)][:M]
    p = list(range(NG))
    def find(x):
        while p[x] != x: p[x] = p[p[x]]; x = p[x]
        return x
    for e in es:
        for v in e[1:]: p[find(v)] = find(e[0])
    c[tuple(sorted(collections.Counter(find(v) for v in range(NG)).values()))] += 1
print(f, dict(c))
