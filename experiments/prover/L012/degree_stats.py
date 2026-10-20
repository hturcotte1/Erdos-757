"""(L012, descriptive) Degree statistics of the 699 route-4 classes: m, covered vertices, degree counts, number of degree-4 vertices."""
import re, collections, gzip
L = [l for l in gzip.open('route4_classes.txt.gz', 'rt') if l.startswith('FOUND')]
stats = collections.Counter(); bad = 0
for l in L:
    es = [tuple(map(int, t)) for t in re.findall(r'\((\d+),(\d+),(\d+)\)', l)]
    d = collections.Counter(v for e in es for v in e)
    if len(es) != 21 or len(d) != 23: bad += 1
    stats[tuple(sorted(collections.Counter(d.values()).items()))] += 1
print('classes', len(L), '| with m != 21 or an uncovered vertex:', bad)
for k, v in sorted(stats.items(), key=lambda x: -x[1]): print('  (degree, number of vertices)', k, ':', v, 'classes')
print('number of degree-4 vertices -> classes:', dict(sorted(collections.Counter(dict(k).get(4, 0) for k in stats.elements()).items())))
print('number of degree-1 vertices -> classes:', dict(sorted(collections.Counter(dict(k).get(1, 0) for k in stats.elements()).items())))
