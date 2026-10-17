"""edge lists ('FOUND: (a,b,c) ...' lines or 'n m a b c ...') -> graph6 incidence graphs (class 1 = vertices 0..n-1, class 2 = edges)."""
import sys, re
def g6(n, adj):
    bits = []
    for j in range(1, n):
        for i in range(j): bits.append(1 if (i, j) in adj else 0)
    while len(bits) % 6: bits.append(0)
    s = chr(n + 63)
    for k in range(0, len(bits), 6):
        v = 0
        for b in bits[k:k + 6]: v = 2 * v + b
        s += chr(v + 63)
    return s
def to_g6(nv, edges):
    adj = set()
    for k, e in enumerate(edges):
        for v in e: adj.add((v, nv + k))
    return g6(nv + len(edges), adj)
if __name__ == '__main__':
    nv = int(sys.argv[1])
    for l in sys.stdin:
        es = [tuple(map(int, t.split(','))) for t in re.findall(r'\((\d+,\d+,\d+)\)', l)]
        if es: print(to_g6(nv, es))
