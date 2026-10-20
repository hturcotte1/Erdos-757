"""(L012) Final steps.  route 4: H = (23,21,10) with a vertex v of degree 4: G = H - v = (22,17,9), slack 1, max degree <= 4, the 8
endpoints of the 4 new pairs of G-degree <= 3.  route 20: H = (23,20,10) (slack -1, max degree <= 3): G = H - v for a degree-3 vertex,
(22,17,9), slack 1, max degree <= 3, endpoints of G-degree <= 2.  G is a disjoint union of components of the 4 types of the
decomposition of (22,17) with total slack 1 (no isolated vertex), each isomorphic to a class representative of cell(., ., ., D);
the inputs are all multisets of representatives; ext_d 22 9 10 d EP gives every H with tau >= 10 in C (F7 pruning, P3 at the end)."""
import sys, os, json, itertools, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import engine
from engine import cell, decompositions, ext_parallel, run, dedupe, log, B, HERE
route = sys.argv[1]
D, d, EP = {'4': (4, 4, 3), '20': (3, 3, 2)}[route]
N, M, S, TG, T = 22, 17, 1, 9, 10
t0 = time.time()
decs = decompositions(N, M, S); log('ROUTE', route, 'decompositions of (22,17) slack 1:', decs)
inputs = []; info = []
for dec in decs:
    groups = {}
    for c in dec: groups[c] = groups.get(c, 0) + 1
    gl = []
    for typ, k in sorted(groups.items()):
        cls = cell(typ[0], typ[1], typ[2], D)
        gl.append((typ, cls, list(itertools.combinations_with_replacement(range(len(cls)), k))))
    size = 1
    for g in gl: size *= len(g[2])
    info.append([list(dec), [len(g[1]) for g in gl], size])
    for combo in itertools.product(*[g[2] for g in gl]):
        es = []; off = 0
        for (typ, cls, _), idxs in zip(gl, combo):
            for i in idxs: es += [tuple(v + off for v in e) for e in cls[i]]; off += typ[0]
        assert off == N
        inputs.append('%d ' % len(es) + ' '.join('%d %d %d' % e for e in es))
log('ROUTE', route, 'types/classes/products', info, 'inputs', len(inputs))
open(os.path.join(HERE, 'out', 'route%s_inputs.txt' % route), 'w').write('\n'.join(inputs) + '\n')
hits, tot = ext_parallel(inputs, N, TG, T, d, EP, 'route' + route)
log('ROUTE', route, 'ext_d', tot, 'hits in C', len(hits))
open(os.path.join(HERE, 'out', 'route%s_hits.txt' % route), 'w').write('\n'.join(hits) + ('\n' if hits else ''))
res = dict(route=route, decompositions=[list(x) for x in decs], types=info, inputs=len(inputs), ext=tot, hits_in_C=len(hits))
if hits:
    f = run([os.path.join(B, 'filt'), 'HIT', '23', 'notau'], '\n'.join(hits) + '\n'); res['filt'] = f.strip().splitlines()[-1]
    surv = [l.split(' #conn')[0] for l in f.splitlines() if l.startswith('SURVIVOR:')]
    reps = dedupe(surv, 23); res['classes'] = len(reps)
    with open(os.path.join(HERE, 'out', 'route%s_classes.txt' % route), 'w') as fo:
        for es in reps: fo.write('FOUND: ' + ' '.join('(%d,%d,%d)' % e for e in es) + '\n')
res['secs'] = round(time.time() - t0, 1)
json.dump(res, open(os.path.join(HERE, 'results_route%s.json' % route), 'w'), indent=1)
log('ROUTE', route, 'RESULT', {k: v for k, v in res.items() if k not in ('types',)})
