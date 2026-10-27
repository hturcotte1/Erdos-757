import json, sys
sys.path.insert(0, '/home/user/Erdos-757/experiments/referee/C008')
from refcheck import parse, aps
from collections import Counter
import sympy
A = parse(json.load(open('/home/user/Erdos-757/results/claims/C008-f19-h11.json'))['set'])
E = aps(A); n = len(A)
M = sympy.zeros(len(E), n)
for r, (a, b, c) in enumerate(E):
    M[r, a] += 1; M[r, c] += 1; M[r, b] -= 2
rk = M.rank()
print('AP equation rank over Q', rk, 'solution-space dim', n - rk, 'dim after affine normalisation', n - rk - 2)
deg = Counter(v for e in E for v in e)
print('degree-4 point(s):', [A[v] for v in range(n) if deg[v] == 4], 'index', [v for v in range(n) if deg[v] == 4])
print('degree-3 points:', [A[v] for v in range(n) if deg[v] == 3])
print('degree-2 points:', [A[v] for v in range(n) if deg[v] == 2])
print('degree-0/1 points:', [A[v] for v in range(n) if deg[v] < 2])
