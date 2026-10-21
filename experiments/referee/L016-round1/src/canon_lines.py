#!/usr/bin/env python3
"""Referee L016 round 1 (own code): read 3-graph lines (tokens '(a,b,c)' as in FOUND:/X: lines, or worker keys 'C m a.b.c ...'),
write graph6 of the incidence graph (vertex nodes first) for labelg -f.  Usage: canon_lines.py n < lines"""
import sys, re
n = int(sys.argv[1])
pat = re.compile(r'\((\d+),(\d+),(\d+)\)')
w = sys.stdout.write
for line in sys.stdin:
    if line.startswith('C '):
        es = [tuple(map(int, t.split('.'))) for t in line.split()[2:]]
    else:
        es = [tuple(map(int, t)) for t in pat.findall(line)]
    if not es:
        continue
    es = sorted(tuple(sorted(e)) for e in es)
    N = n + len(es); nb = N * (N - 1) // 2; arr = bytearray((nb + 5) // 6)
    for j, e in enumerate(es):
        jj = n + j; base = jj * (jj - 1) // 2
        for v in e:
            assert 0 <= v < n
            p = base + v; arr[p // 6] |= 1 << (5 - p % 6)
    w(chr(N + 63) + ''.join(chr(b + 63) for b in arr) + '\n')
