"""Degree-4 gluing: X = w + 4 edges over disjoint unions of KNOWN tight pieces (cells from ../20261027-0300-tight-cells-d4/out/cells),
n=32, m=29, tau=14.  Uses the L012/L014 engine pieces (ext_d MAXP=640, filt, canon).  Decompositions of (31,25,13) into tight pieces
(3,1,1),(10,7,4),(14,12,6),(17,13,7),(21,18,9):  (a) 21+10  (b) 17+14  (c) 3+14+14.   [pieces of Delta<=4]"""
import os, sys, itertools, json
SRC = '/home/user/Erdos-757/experiments/20261027-0300-tight-cells-d4/src'
os.environ['CELLDIR'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'work', 'cells')
os.environ['ENGINELOG'] = '/dev/null'; os.environ['NPROC'] = '1'
sys.path.insert(0, SRC)
import engine
decs = {'b': [(17, 13, 7), (14, 12, 6)], 'c': [(3, 1, 1), (14, 12, 6), (14, 12, 6)], 'a': [(21, 18, 9), (10, 7, 4)]}
out = {}
n, m, t, d = 32, 29, 14, 4
for name, dec in decs.items():
    assert sum(x[0] for x in dec) == n - 1 and sum(x[1] for x in dec) == m - d and sum(x[2] for x in dec) == t - 1
    groups = {}
    for c in dec: groups[c] = groups.get(c, 0) + 1
    gl = []
    for typ, k in sorted(groups.items()):
        cls = engine.cell(typ[0], typ[1], typ[2], d)
        gl.append((typ, cls, list(itertools.combinations_with_replacement(range(len(cls)), k))))
    inputs = []
    for combo in itertools.product(*[g[2] for g in gl]):
        es = []; off = 0
        for (typ, cls, _), idxs in zip(gl, combo):
            for i in idxs:
                es += [tuple(v + off for v in e) for e in cls[i]]; off += typ[0]
        assert off == n - 1
        inputs.append('%d ' % len(es) + ' '.join('%d %d %d' % e for e in es))
    hits, tot = engine.ext_parallel(inputs, n - 1, t - 1, t, d, d - 1, 'glue32_' + name)
    print(name, 'inputs', len(inputs), 'hits_in_C', len(hits), tot, flush=True)
    keep = []; filt_summary = None
    if hits:
        f = engine.run([os.path.join(engine.B, 'filt'), 'HIT', str(n), 'notau'], '\n'.join(hits) + '\n')
        keep = [l.split(' #conn')[0] for l in f.splitlines() if l.startswith('SURVIVOR:') and l.endswith('#conn=1')]
        filt_summary = f.strip().splitlines()[-1]
    reps = engine.dedupe(keep, n) if keep else []
    print(name, 'connected hits', len(keep), 'classes', len(reps), filt_summary, flush=True)
    out[name] = dict(dec=dec, inputs=len(inputs), hits_in_C=len(hits), ext=tot, connected_hits=len(keep), classes=len(reps), filt=filt_summary)
    json.dump(out, open('glue32_results.json','w'), indent=1)
    with open('glue32_classes_%s.txt' % name, 'w') as fh:
        for es in reps: fh.write('FOUND: ' + ' '.join('(%d,%d,%d)' % e for e in es) + '\n')

