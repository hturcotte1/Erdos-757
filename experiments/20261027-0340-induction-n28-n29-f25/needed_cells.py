"""Closure of cells needed by the induction scheme at n = 28 and n = 29 (tops = open violator cells of arith_base, i.e. the cells
that the L016 scheme must show empty); expansion stops at cells from refereed sources (L012-L016 tarballs); every reached cell is
reported with its class count, provenance and whether it was computed here / by the concurrent worker.  Writes needed_cells.json."""
import os, sys, json, math
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, 'src'))
os.environ['CELLDIR'] = os.path.join(HERE, 'out', 'cells'); os.environ['ENGINELOG'] = os.path.join(HERE, 'out', 'engine_plan.log')
import engine
sys.path.insert(0, os.path.join(HERE, '..', '20261027-0235-cost-n28-n29')); from arith_base import analyse
prov = json.load(open(os.path.join(HERE, 'provenance.json')))
def valid(n, m, t, D): return not (m == 0 or t < 1 or t > m or n > 2 * m + 1 or m > n - 2 or 17 * t > 5 * n + 3 * m or D < 1)
def cnt(k):
    r = engine.load(k); return None if r is None else len(r)
def closure(tops):
    seen = {}
    def visit(k):
        if k in seen or not valid(*k): return
        c = cnt(k); p = prov.get('%d,%d,%d,%d' % k, {}).get('first', '?')
        seen[k] = dict(classes=c, source=p)
        if c is None: seen[k]['MISSING'] = True; return
        if p.endswith('(refereed)'): return
        n, m, t, D = k
        if m <= engine.MD: return
        for d in range(max(1, math.ceil(3 * m / n)), D + 1):
            for tp in (t - 1, t):
                Sp = 3 * (n - 1) + 2 * (m - d) - 11 * tp
                if Sp < 0 or tp < 0: continue
                for dec in engine.decompositions(n - 1, m - d, Sp):
                    for typ in set(dec): visit((typ[0], typ[1], typ[2], d))
    for k in tops: visit(k)
    return seen
out = {}
for n in (28, 29):
    rows = analyse(n)
    tops = [(r['n'], r['m'], r['tau'], r['dmax']) for r in rows if r['status'].startswith('OPEN')]
    cl = closure(tops)
    out['n%d' % n] = dict(tops={str(k): cnt(k) for k in tops}, closure={str(k): v for k, v in sorted(cl.items())},
                          all_violator_tops_empty=all(cnt(k) == 0 for k in tops), missing=[str(k) for k, v in cl.items() if v.get('MISSING')])
    print('n=%d tops %s' % (n, {str(k): cnt(k) for k in tops}), 'closure cells', len(cl), 'missing', out['n%d' % n]['missing'])
json.dump(out, open(os.path.join(HERE, 'needed_cells.json'), 'w'), indent=1)
