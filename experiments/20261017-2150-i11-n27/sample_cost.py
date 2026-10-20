"""Estimate the ext_d cost of the (25,19,10,3) branch d=3 tp=9 by timing ext_d on random samples of inputs of each big decomposition (SEED fixed).
usage: python3 sample_cost.py NSAMPLE   (needs cell (24,16,9,3) for the full list; the big three decompositions do not)"""
import os, sys, random, itertools, subprocess, time
H = os.path.dirname(os.path.abspath(__file__)); os.environ['CELLDIR'] = os.path.join(H, 'out', 'cells'); os.environ['ENGINELOG'] = os.path.join(H, 'out', 'sample.log'); sys.path.insert(0, H)
import engine
random.seed(20261017); NS = int(sys.argv[1]); n, m, t, D = 25, 19, 10, 3; d = 3; tp = 9
Sp = 3 * (n - 1) + 2 * (m - d) - 11 * tp
for dec in engine.decompositions(n - 1, m - d, Sp):
    groups = {}
    for c in dec: groups[c] = groups.get(c, 0) + 1
    gl = []; size = 1
    for typ, k in sorted(groups.items()):
        cls = engine.cell(typ[0], typ[1], typ[2], d) if not (typ == (24, 16, 9)) or os.path.exists(os.path.join(H, 'out/cells/cell_24_16_9_D3.txt')) else []
        combos = list(itertools.combinations_with_replacement(range(len(cls)), k)) if len(cls) * k < 4000 else None
        gl.append((typ, cls, k, combos)); size *= (len(combos) if combos is not None else __import__('math').comb(len(cls) + k - 1, k))
    if size < 20000: continue
    ins = []
    for _ in range(NS):
        es = []; off = 0
        for typ, cls, k, combos in gl:
            idxs = random.choice(combos) if combos is not None else tuple(sorted(random.randrange(len(cls)) for _ in range(k)))
            for i in idxs:
                es += [tuple(v + off for v in e) for e in cls[i]]; off += typ[0]
        ins.append('%d ' % len(es) + ' '.join('%d %d %d' % e for e in es))
    t0 = time.time()
    r = subprocess.run([os.path.join(H, 'bin', 'ext_d'), str(n - 1), str(tp), str(t), str(d), str(d - 1)], input='\n'.join(ins) + '\n', capture_output=True, text=True)
    el = time.time() - t0
    summ = [l for l in r.stdout.splitlines() if l.startswith('SUMMARY')][0]
    print('dec', dec, 'size', size, 'sample', NS, 'secs %.1f' % el, 'est total secs %.0f' % (el / NS * size), summ, flush=True)
