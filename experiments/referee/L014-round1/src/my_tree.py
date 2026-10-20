"""Referee L014 r1: own dry run of the key tree of (23,21,10,3) (own branches/decompositions from decomp_bf.decs, own guards,
MD = 10), compared with the prover's tree listing.  Usage: python3 my_tree.py tree_keys.txt"""
import sys, math
src = open('/home/user/Erdos-757/experiments/referee/L014-round1/src/decomp_bf.py').read().split('from math import comb')[0]
exec(src.replace('CD = sys.argv[1]', 'CD = None'))
def trivial(n, m, t, D):
    if (n, m) == (1, 0): return True
    # guards: each is a valid emptiness condition for connected members of C (see review)
    return m == 0 or t < 1 or t > m or n > 2 * m + 1 or m > n - 2 or 17 * t > 5 * n + 3 * m or D < 1
seen = {}; order = []
def visit(k):
    if k in seen: return
    seen[k] = 'trivial' if trivial(*k) else None
    if seen[k]: return
    n, m, t, D = k
    if m <= 10: seen[k] = 'direct'; order.append(k); return
    seen[k] = 'recurse'
    for d in range(max(1, math.ceil(3 * m / n)), D + 1):
        for tp in (t - 1, t):
            Sp = 3 * (n - 1) + 2 * (m - d) - 11 * tp
            if Sp < 0 or tp < 0: continue
            for dec in decs(n - 1, m - d, Sp):
                for typ in set(dec): visit((typ[0], typ[1], typ[2], d))
    order.append(k)
visit((23, 21, 10, 3))
mine = {k: v for k, v in seen.items() if v != 'trivial'}
theirs = {}
for l in open(sys.argv[1]):
    a, r = l.split(); theirs[tuple(map(int, a.split(',')))] = r
print('my tree: nontrivial', len(mine), 'direct', sum(v == 'direct' for v in mine.values()), 'recurse', sum(v == 'recurse' for v in mine.values()))
print('prover tree:', len(theirs), 'equal key sets and routes:', mine == theirs)
print('trivial keys visited:', sorted(k for k, v in seen.items() if v == 'trivial'))
