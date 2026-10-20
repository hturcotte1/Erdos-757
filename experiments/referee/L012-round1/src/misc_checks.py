"""Referee: Remark 5 record cells; degree statistics of the 699 classes (descriptive)."""
import math, re, collections
cells = []
for n in range(3, 41):
    hmax = math.ceil(4 * n / 7) - 1
    for m in range(0, n - 1):
        for t in range(n - hmax, m + 1):
            if 17 * t <= 5 * n + 3 * m and 11 * t <= 3 * n + 2 * m:
                cells.append((n, m, t, 3 * n + 2 * m - 11 * t))
print('Remark 5 cells:', cells)
deg4 = collections.Counter(); deg1 = collections.Counter(); pats = collections.Counter(); bad = 0
for l in open('out/r4_699.txt'):
    E = [tuple(map(int, x.split(','))) for x in re.findall(r'\((\d+,\d+,\d+)\)', l)]
    d = collections.Counter(v for e in E for v in e)
    if len(E) != 21 or len(d) != 23: bad += 1
    ds = sorted(d.values()); deg4[ds.count(4)] += 1; deg1[ds.count(1)] += 1; pats[tuple(ds.count(i) for i in range(1, 5))] += 1
print('classes with m!=21 or uncovered vertex:', bad, '| #deg-4 vertices:', dict(deg4), '| #deg-1 vertices:', dict(deg1), '| degree patterns (n1,n2,n3,n4):', dict(pats))
