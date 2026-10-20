"""Referee L014 round 2: own dry run of the recursion tree of (23,21,10,3) (own guards without K8, own decompositions),
compared with the prover's tree_23_21_10_3.txt."""
import sys, re
from math import ceil
sys.path.insert(0, '.')
from arith_decomp import decomps_bf
MD = 10
seen = {}
def trivial(n, m, t, D):
    if (n, m) == (1, 0): return True
    return m == 0 or t < 1 or t > m or n > 2*m + 1 or m > n - 2 or D < 1
def visit(k):
    if k in seen: return
    n, m, t, D = k
    if trivial(*k): seen[k] = 'trivial'; return
    if m <= MD: seen[k] = 'direct'; return
    seen[k] = 'recurse'; br = 0
    for d in range(max(1, ceil(3*m/n)), D + 1):
        for tp in (t - 1, t):
            Sp = 3*(n-1) + 2*(m-d) - 11*tp
            if Sp < 0 or tp < 0: continue
            br += 1
            for dec in decomps_bf(n-1, m-d, Sp, False):
                for typ in set(dec): visit((typ[0], typ[1], typ[2], d))
    seen[k] = ('recurse', br)
visit((23, 21, 10, 3))
mine = {k: v for k, v in seen.items() if v != 'trivial'}
prov = {}
for l in open('/home/user/Erdos-757/experiments/prover/L014/tree_23_21_10_3.txt'):
    if l.startswith('CELL'):
        k = tuple(map(int, re.match(r'CELL \((\d+), (\d+), (\d+), (\d+)\)', l).groups())); prov[k] = 'direct' if ' direct ' in l else 'recurse'
print('my tree: nontrivial keys', len(mine), 'direct', sum(1 for v in mine.values() if v == 'direct'), 'recursion', sum(1 for v in mine.values() if v != 'direct'),
      'branches', sum(v[1] for v in mine.values() if v != 'direct'))
print('prover tree keys', len(prov), 'same key set:', set(mine) == set(prov), 'same routes:', all((mine[k] == 'direct') == (prov[k] == 'direct') for k in prov if k in mine))
