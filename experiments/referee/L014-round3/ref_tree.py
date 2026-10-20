"""Referee (L014 round 3): own dry run of the engine's recursion tree (rules of certificate Step 0.5), listing the keys visited,
their route (direct if m <= MD, else recursion with branches d in [ceil(3m/n), D], t' in {t-1, t}, S' >= 0) and the own
brute-force decompositions (ref_decomp.py).  Prints the keys and compares with the prover's tree file if given."""
import sys, math, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ref_decomp import decompositions_bf
MD = 10
seen = {}; order = []; branches = []
def trivial(n, m, t, D):
    if (n, m) == (1, 0): return 'isolated'
    if m == 0 or t < 1 or t > m or n > 2 * m + 1 or m > n - 2 or 17 * t > 5 * n + 3 * m or D < 1: return 'empty'
    return None
def visit(n, m, t, D):
    key = (n, m, t, D)
    if key in seen: return
    tr = trivial(n, m, t, D)
    if tr: seen[key] = tr; return
    if m <= MD: seen[key] = 'direct'; order.append(key); return
    seen[key] = 'recurse'; needs = []
    for d in range(max(1, math.ceil(3 * m / n)), D + 1):
        for tp in (t - 1, t):
            Sp = 3 * (n - 1) + 2 * (m - d) - 11 * tp
            if Sp < 0 or tp < 0: continue
            decs = decompositions_bf(n - 1, m - d, Sp)
            branches.append((key, d, tp, Sp, len(decs)))
            for dec in decs:
                for (a, b, c) in dec:
                    visit(a, b, c, d); needs.append((a, b, c, d))
    order.append(key)
n, m, t, D = map(int, sys.argv[1:5])
visit(n, m, t, D)
direct = [k for k in order if seen[k] == 'direct']; rec = [k for k in order if seen[k] == 'recurse']
print('nontrivial keys', len(order), 'direct', len(direct), 'recursion', len(rec), 'branches', len(branches), 'decompositions', sum(b[4] for b in branches))
for b in branches: print('BRANCH', b)
if len(sys.argv) > 5:
    import re
    prov = set()
    for l in open(sys.argv[5]):
        mm = re.match(r'CELL \((\d+), (\d+), (\d+), (\d+)\) (\w+)', l)
        if mm: prov.add((tuple(map(int, mm.groups()[:4])), mm.group(5)))
    mine = set((k, seen[k]) for k in order)
    print('prover keys', len(prov), 'mine', len(mine), 'only prover', sorted(prov - mine), 'only mine', sorted(mine - prov))
