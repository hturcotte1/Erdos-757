"""Convert lines 'TAG...: (a,b,c) (d,e,f) ...' into graph6 of the bipartite incidence graph (vertices 0..n1-1, edges n1..n1+m-1).
Usage: to_g6.py N1 [TAGPREFIX] < in > out.g6   (lines not starting with TAGPREFIX are skipped; default: any line with ':')"""
import sys, re
n1 = int(sys.argv[1]); tag = sys.argv[2] if len(sys.argv) > 2 else None
def g6(n, adj):
    bits = []
    for j in range(1, n):
        for i in range(j):
            bits.append('1' if adj[i][j] else '0')
    while len(bits) % 6: bits.append('0')
    s = chr(63 + n) if n <= 62 else None
    assert s is not None
    out = [s]
    for k in range(0, len(bits), 6):
        out.append(chr(63 + int(''.join(bits[k:k+6]), 2)))
    return ''.join(out)
for line in sys.stdin:
    if tag is not None and not line.startswith(tag): continue
    if ':' not in line: continue
    body = line.split(':', 1)[1]
    es = [tuple(map(int, t.split(','))) for t in re.findall(r'\(([\d,]+)\)', body)]
    if not es: continue
    m = len(es); n = n1 + m
    adj = [[0] * n for _ in range(n)]
    for j, e in enumerate(es):
        for v in e:
            assert 0 <= v < n1, (line, n1)
            adj[v][n1 + j] = adj[n1 + j][v] = 1
    print(g6(n, adj))
