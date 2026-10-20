"""hg2g6.py N [TAG] < lines : convert hypergraph lines containing "(a,b,c)" tuples (optionally only lines starting with TAG)
into graph6 strings of the incidence bigraph: points 0..N-1 first, then the edges in input order.  (Referee L009 round 2.)"""
import sys, re
N = int(sys.argv[1]); tag = sys.argv[2] if len(sys.argv) > 2 else None
def g6(nv, adj):
    assert nv <= 62
    bits = []
    for j in range(1, nv):
        for i in range(j):
            bits.append(1 if (i, j) in adj else 0)
    while len(bits) % 6: bits.append(0)
    out = [chr(nv + 63)]
    for k in range(0, len(bits), 6):
        v = 0
        for b in bits[k:k+6]: v = (v << 1) | b
        out.append(chr(v + 63))
    return ''.join(out)
for line in sys.stdin:
    if tag is not None and not line.startswith(tag): continue
    es = [tuple(map(int, t.split(','))) for t in re.findall(r'\((\d+,\d+,\d+)\)', line)]
    if not es: continue
    assert all(0 <= v < N for e in es for v in e), line
    nv = N + len(es); adj = set()
    for j, e in enumerate(es):
        for v in e: adj.add((v, N + j))
    print(g6(nv, adj))
