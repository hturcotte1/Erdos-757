"""Full recursion plan for the open n=27 cells: which (n,m,t,D) cells the L012 engine needs (recursively), which exist in the seeded CELLDIR, estimated #inputs where known.
Arithmetic only. Uses engine.decompositions unchanged."""
import os, sys, math, json
HERE = os.path.dirname(os.path.abspath(__file__))
os.environ.setdefault('CELLDIR', os.path.join(HERE, 'out', 'cells')); os.environ.setdefault('ENGINELOG', os.path.join(HERE, 'out', 'plan_engine.log'))
sys.path.insert(0, HERE)
import engine
from arith import analyse
MD = 10
def valid(n, m, t, D): return not (m == 0 or t < 1 or t > m or n > 2 * m + 1 or m > n - 2 or 17 * t > 5 * n + 3 * m or D < 1)
def exists(k): return os.path.exists(os.path.join(engine.OUT, 'cell_%d_%d_%d_D%d.txt' % k))
def count(k):
    p = os.path.join(engine.OUT, 'cell_%d_%d_%d_D%d.txt' % k)
    return sum(1 for l in open(p) if l.startswith('FOUND:')) if os.path.exists(p) else None
seen = {}
def visit(k, depth=0):
    if k in seen or not valid(*k): return
    n, m, t, D = k
    e = exists(k); seen[k] = dict(exists=e, count=count(k), direct=(m <= MD), branches=[])
    if e or m <= MD: return
    for d in range(max(1, math.ceil(3 * m / n)), D + 1):
        for tp in (t - 1, t):
            Sp = 3 * (n - 1) + 2 * (m - d) - 11 * tp
            if Sp < 0 or tp < 0: continue
            decs = engine.decompositions(n - 1, m - d, Sp); tot = 0; unknown = False; dl = []
            for dec in decs:
                groups = {}
                for c in dec: groups[c] = groups.get(c, 0) + 1
                size = 1
                for typ, kk in groups.items():
                    ck = (typ[0], typ[1], typ[2], d)
                    if typ == (1, 0, 0): continue
                    if not valid(*ck): size = 0; continue
                    visit(ck)
                    c = seen[ck]['count']
                    if c is None: unknown = True; continue
                    size *= math.comb(c + kk - 1, kk)
                dl.append(['+'.join('%dx(%d,%d,%d)' % (kk, *typ) for typ, kk in sorted(groups.items())), size]); tot += size
            seen[k]['branches'].append(dict(d=d, tp=tp, Sp=Sp, ndec=len(decs), inputs_known=tot, unknown_components=unknown, decs=dl))
tops = []
for r in analyse(27):
    if r['status'].startswith('OPEN'):
        k = (r['n'], r['m'], r['tau'], r['dmax']); tops.append(k); visit(k)
new = {k: v for k, v in seen.items() if not v['exists']}
print('top cells:', tops)
print('total cells visited:', len(seen), ' missing:', len(new))
for k in sorted(new, key=lambda k: (k[0], k[1])):
    v = new[k]
    print(k, 'direct' if v['direct'] else 'recurse')
    for b in v['branches']:
        print('    d=%d tp=%d S\'=%d ndec=%d known_inputs=%d%s' % (b['d'], b['tp'], b['Sp'], b['ndec'], b['inputs_known'], ' (+unknown comps)' if b['unknown_components'] else ''))
        for dd in b['decs']:
            if dd[1] or True: print('        ', dd)
json.dump({str(k): v for k, v in seen.items()}, open('plan.json', 'w'), indent=1)
