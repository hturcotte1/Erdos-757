"""(L016) Dry run of engine.cell for a list of keys, as tree.py (L014) but stopping at keys whose cell file already exists in CELLDIR
(engine.cell loads such a file instead of computing it).  Prints the keys that would be COMPUTED (post-order) and the keys LOADED.
Usage: CELLDIR=... python3 plan16.py n,m,t,D [n,m,t,D ...]"""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import engine
def trivial(n, m, t, D):
    if (n, m) == (1, 0): return 'isolated'
    if m == 0 or t < 1 or t > m or n > 2 * m + 1 or m > n - 2 or 17 * t > 5 * n + 3 * m or D < 1: return 'empty-by-guard'
    return None
def exists(key):
    return engine.load(key) is not None
seen = {}; order = []; loaded = set()
def visit(key):
    if key in seen: return
    seen[key] = 'pending'
    if trivial(*key): seen[key] = 'trivial'; return
    if exists(key): seen[key] = 'loaded'; loaded.add(key); return
    n, m, t, D = key
    if m <= engine.MD: seen[key] = 'direct'; order.append(key); return
    for d in range(max(1, math.ceil(3 * m / n)), D + 1):
        for tp in (t - 1, t):
            Sp = 3 * (n - 1) + 2 * (m - d) - 11 * tp
            if Sp < 0 or tp < 0: continue
            for dec in engine.decompositions(n - 1, m - d, Sp):
                for typ in sorted(set(dec)): visit((typ[0], typ[1], typ[2], d))
    seen[key] = 'recurse'; order.append(key)
for a in sys.argv[1:]: visit(tuple(map(int, a.split(','))))
for k in order: print('COMPUTE', k, seen[k])
for k in sorted(loaded): print('LOAD', k)
print('TOTAL compute', len(order), 'load', len(loaded))
