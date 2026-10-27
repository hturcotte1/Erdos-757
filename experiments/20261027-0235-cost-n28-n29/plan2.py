"""Recursion plan (arithmetic only) for I11 cells n=28,29 and the record cell (25,23,11,4): which cells the L012/L016 engine needs,
which exist (in the seeded n=27 CELLDIR, read only), which are missing. Uses engine.decompositions unchanged.
usage: python3 plan2.py TARGET   with TARGET in n28, n29full, n29rec, rec25"""
import os, sys, math, json
HERE = os.path.dirname(os.path.abspath(__file__))
CELLS = os.path.join(HERE, '..', '20261017-2150-i11-n27', 'out', 'cells')
os.environ['CELLDIR'] = CELLS; os.environ['ENGINELOG'] = '/tmp/claude-0/-home-user-Erdos-757/32619e2f-2987-5d2f-a1f8-a110778bce61/scratchpad/plan_engine.log'
sys.path.insert(0, HERE)
import engine
from arith_base import analyse
MD = 10
def valid(n, m, t, D): return not (m == 0 or t < 1 or t > m or n > 2 * m + 1 or m > n - 2 or 17 * t > 5 * n + 3 * m or D < 1)
CNT = {}
def exists(k): return os.path.exists(os.path.join(CELLS, 'cell_%d_%d_%d_D%d.txt' % k))
def count(k):
    if k in CNT: return CNT[k]
    p = os.path.join(CELLS, 'cell_%d_%d_%d_D%d.txt' % k)
    if not os.path.exists(p): return None
    c = 0
    for l in open(p):
        if l.startswith('FOUND:'): c += 1
    CNT[k] = c; return c
def build(tops):
    seen = {}
    def visit(k):
        if k in seen or not valid(*k): return
        n, m, t, D = k
        e = exists(k); seen[k] = dict(exists=e, count=count(k), direct=(m <= MD), branches=[])
        if e or m <= MD: return
        for d in range(max(1, math.ceil(3 * m / n)), D + 1):
            for tp in (t - 1, t):
                Sp = 3 * (n - 1) + 2 * (m - d) - 11 * tp
                if Sp < 0 or tp < 0: continue
                decs = engine.decompositions(n - 1, m - d, Sp); dl = []
                for dec in decs:
                    groups = {}
                    for c in dec: groups[c] = groups.get(c, 0) + 1
                    comps = []
                    for typ, kk in groups.items():
                        if typ == (1, 0, 0): continue
                        ck = (typ[0], typ[1], typ[2], d)
                        if not valid(*ck): comps = None; break
                        visit(ck); comps.append((ck, kk))
                    dl.append(dict(dec=sorted(groups.items()), comps=comps))   # comps None = void (some component cell empty by guard)
                seen[k]['branches'].append(dict(d=d, tp=tp, Sp=Sp, ndec=len(decs), decs=dl))
    for k in tops: visit(k)
    return seen
def tops_for(name):
    if name == 'n28': return [(r['n'], r['m'], r['tau'], r['dmax']) for r in analyse(28) if r['status'].startswith('OPEN')]
    if name == 'n29full': return [(r['n'], r['m'], r['tau'], r['dmax']) for r in analyse(29) if r['status'].startswith('OPEN')]
    if name == 'n29rec': return [(29, 27, 13, 3)]
    if name == 'rec25': return [(25, 23, 11, 4)]
if __name__ == '__main__':
    name = sys.argv[1]; tops = tops_for(name); seen = build(tops)
    new = {k: v for k, v in seen.items() if not v['exists']}
    print('TARGET', name, 'tops', tops, 'cells visited', len(seen), 'missing', len(new))
    for k in sorted(new, key=lambda k: (k[0], k[1], k[3])):
        v = new[k]; print(k, 'direct' if v['direct'] else 'recurse', 'top' if k in tops else '')
    json.dump({str(k): {kk: vv for kk, vv in v.items()} for k, v in seen.items()}, open('plan_%s.json' % name, 'w'), default=str)
