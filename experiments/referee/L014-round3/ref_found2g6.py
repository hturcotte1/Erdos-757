"""Referee: convert the prover's 'FOUND: (a,b,c) ...' lines (cell file) to graph6 incidence graphs (n vertices then m edges)."""
import sys, re
n = int(sys.argv[1]); m = int(sys.argv[2])
def g6(N, adj):
    bits = []
    for j in range(1, N):
        for i in range(j): bits.append(1 if (adj[i] >> j) & 1 else 0)
    while len(bits) % 6: bits.append(0)
    s = chr(N + 63)
    for k in range(0, len(bits), 6):
        v = 0
        for b in bits[k:k + 6]: v = v * 2 + b
        s += chr(v + 63)
    return s
cnt = 0
for l in sys.stdin:
    if not l.startswith('FOUND:'): continue
    es = [tuple(map(int, x.split(','))) for x in re.findall(r'\((\d+,\d+,\d+)\)', l)]
    assert len(es) == m and all(0 <= v < n for e in es for v in e)
    N = n + m; adj = [0] * N
    for j, e in enumerate(es):
        for v in e: adj[v] |= 1 << (n + j); adj[n + j] |= 1 << v
    print(g6(N, adj)); cnt += 1
print('converted', cnt, file=sys.stderr)
