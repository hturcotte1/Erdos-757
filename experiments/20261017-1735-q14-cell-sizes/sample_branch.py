"""Measurement-only: for each branch (d,tp) of engine.recurse(n,m,t,D) build the exact ext_d input list from the cell files that exist, run ext_d on an
evenly spaced SAMPLE of each decomposition's inputs (HIT lines discarded, SUMMARY kept: nothing is written to disk) and extrapolate nodes / hits / CPU seconds.
Usage: python3 sample_branch.py n m t D [per_dec_min=30] [frac_den=50]  -> prints and appends a JSON line to samples.jsonl.  [heuristic extrapolation]"""
import os, sys, json, time, math, itertools, subprocess
HERE = os.path.dirname(os.path.abspath(__file__))
os.environ.setdefault('CELLDIR', os.path.join(HERE, 'out', 'cells')); os.environ.setdefault('ENGINELOG', os.path.join(HERE, 'out', 'sample_engine.log'))
sys.path.insert(0, HERE)
import engine
n, m, t, D = map(int, sys.argv[1:5]); kmin = int(sys.argv[5]) if len(sys.argv) > 5 else 30; den = int(sys.argv[6]) if len(sys.argv) > 6 else 50
res = dict(cell=[n, m, t, D], branches=[])
for d in range(max(1, math.ceil(3 * m / n)), D + 1):
    for tp in (t - 1, t):
        Sp = 3 * (n - 1) + 2 * (m - d) - 11 * tp
        if Sp < 0 or tp < 0: continue
        br = dict(d=d, tp=tp, Sp=Sp, decs=[], missing=[]); tot = dict(inputs=0, nodes=0.0, hits_in_C=0.0, cpu=0.0, sampled=0)
        for dec in engine.decompositions(n - 1, m - d, Sp):
            groups = {}
            for c in dec: groups[c] = groups.get(c, 0) + 1
            gl = []; miss = False
            for typ, k in sorted(groups.items()):
                key = (typ[0], typ[1], typ[2], d)
                if typ == (1, 0, 0): cls = [[]]
                elif (typ[2] < 1 or typ[2] > typ[1] or typ[0] > 2 * typ[1] + 1 or typ[1] > typ[0] - 2 or 17 * typ[2] > 5 * typ[0] + 3 * typ[1] or d < 1): cls = []
                else:
                    cls = engine.load(key)
                    if cls is None: br['missing'].append(list(key)); miss = True; break
                gl.append((typ, cls, k))
            if miss: continue
            size = 1; combos = []
            for typ, cls, k in gl:
                c = list(itertools.combinations_with_replacement(range(len(cls)), k)); combos.append(c); size *= len(c)
            if size == 0: br['decs'].append(dict(dec=[list(x) for x in dec], inputs=0)); continue
            step = max(1, size // max(kmin, min(size, size // den)) if size > kmin else 1)
            sel = []
            for idx, combo in enumerate(itertools.product(*combos)):
                if idx % step: continue
                es = []; off = 0
                for (typ, cls, _), idxs in zip(gl, combo):
                    for i in idxs:
                        es += [tuple(v + off for v in e) for e in cls[i]]; off += typ[0]
                sel.append('%d ' % len(es) + ' '.join('%d %d %d' % e for e in es))
            t0 = time.time()
            p = subprocess.run('%s %d %d %d %d %d | grep "^SUMMARY"' % (os.path.join(engine.B, 'ext_d'), n - 1, tp, t, d, d - 1), input='\n'.join(sel) + '\n', capture_output=True, text=True, shell=True)
            cpu = time.time() - t0; s = dict(kv.split('=') for kv in p.stdout.split()[1:] if '=' in kv)
            assert int(s.get('bad_tau', 0)) == 0, s
            w = size / len(sel); nodes = int(s['nodes']) * w; hits = int(s['hits_in_C']) * w if 'hits_in_C' in s else 0
            br['decs'].append(dict(dec=[list(x) for x in dec], inputs=size, sampled=len(sel), nodes_est=nodes, hits_in_C_est=hits, cpu_est=cpu * w))
            tot['inputs'] += size; tot['nodes'] += nodes; tot['hits_in_C'] += hits; tot['cpu'] += cpu * w; tot['sampled'] += len(sel)
            print('  dec', dec, 'inputs', size, 'sampled', len(sel), 'nodes_est %.3g hits_in_C_est %.3g cpu_est %.0fs' % (nodes, hits, cpu * w), flush=True)
        br['total'] = tot; res['branches'].append(br)
        print('BRANCH d=%d tp=%d S\'=%d inputs=%d (sampled %d) nodes_est=%.3g hits_in_C_est=%.3g cpu_est=%.0fs missing=%s' % (d, tp, Sp, tot['inputs'], tot['sampled'], tot['nodes'], tot['hits_in_C'], tot['cpu'], br['missing']), flush=True)
open(os.path.join(HERE, 'samples.jsonl'), 'a').write(json.dumps(res) + '\n')
