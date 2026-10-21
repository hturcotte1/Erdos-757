#!/usr/bin/env python3
"""Referee L016 round 1 (own code): 3-graph lines -> graph6 of the vertex-edge incidence graph.
Usage: hg2g6.py n < lines   (each line contains tokens '(a,b,c)'; any prefix such as 'FOUND:' or 'X:' is ignored;
lines without tokens are skipped).  Vertex nodes 0..n-1, edge nodes n..n+m-1 (edges sorted).
Canonical form: pipe into 'labelg -q -f' + 'a'*n (vertex nodes and edge nodes in different cells)."""
import sys, re

n = int(sys.argv[1])
pat = re.compile(r'\((\d+),(\d+),(\d+)\)')
out = sys.stdout
for line in sys.stdin:
    es = sorted(tuple(sorted(map(int, t))) for t in pat.findall(line))
    if not es:
        continue
    N = n + len(es)
    assert N <= 62
    adj = set()
    for j, e in enumerate(es):
        for v in e:
            assert 0 <= v < n
            adj.add((v, n + j))
    bits = []
    for jj in range(1, N):
        for ii in range(jj):
            bits.append(1 if (ii, jj) in adj else 0)
    while len(bits) % 6:
        bits.append(0)
    s = [chr(N + 63)]
    for k in range(0, len(bits), 6):
        v = 0
        for b in bits[k:k + 6]:
            v = 2 * v + b
        s.append(chr(v + 63))
    out.write(''.join(s) + '\n')
