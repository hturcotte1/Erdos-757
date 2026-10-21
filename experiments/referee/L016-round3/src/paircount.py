# paircount.py NG EP < inputs : own count of the admissible pairs (not inside an edge, both G-degrees <= EP) per input; prints max and #inputs with P>256
import sys, itertools
NG, EP = int(sys.argv[1]), int(sys.argv[2]); mx = 0; over = 0; tot = 0
for line in sys.stdin:
    a = list(map(int, line.split()));
    if not a: continue
    m = a[0]; es = [tuple(a[1 + 3 * i:4 + 3 * i]) for i in range(m)]; tot += 1
    deg = [0] * NG; inside = set()
    for e in es:
        for v in e: deg[v] += 1
        for x, y in itertools.combinations(sorted(e), 2): inside.add((x, y))
    P = sum(1 for x in range(NG) for y in range(x + 1, NG) if deg[x] <= EP and deg[y] <= EP and (x, y) not in inside)
    mx = max(mx, P); over += P > 256
print('inputs %d max_pairs %d inputs_with_P>256 %d' % (tot, mx, over))
