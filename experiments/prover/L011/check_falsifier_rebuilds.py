"""(L011) Component vertex counts (union-find over all N vertices) of the falsifier's final input lists F/in_x17.txt (first 18 lines =
its rebuilt (20,14,8) classes, N = 20) and F/in_x22.txt (first 176 lines = its rebuilt (21,13,8) classes, N = 21)."""
import collections
F = '/home/user/Erdos-757/experiments/20261017-0825-n21-n22-via-i11/'
def comps(line, N):
    t = list(map(int, line.split()))[1:]; es = [t[3*k:3*k+3] for k in range(len(t)//3)]
    p = list(range(N))
    def find(x):
        while p[x] != x: p[x] = p[p[x]]; x = p[x]
        return x
    for e in es:
        for v in e[1:]: p[find(v)] = find(e[0])
    return tuple(sorted(collections.Counter(find(v) for v in range(N)).values()))
for f, N, k in [('in_x17.txt', 20, 18), ('in_x22.txt', 21, 176)]:
    L = open(F + f).read().splitlines()
    print(f, 'first', k, 'lines:', dict(collections.Counter(comps(l, N) for l in L[:k])), '| all', len(L), 'lines:',
          dict(collections.Counter(comps(l, N) for l in L)))
