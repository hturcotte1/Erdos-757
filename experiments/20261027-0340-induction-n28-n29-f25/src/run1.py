"""One cell per invocation (so that `timeout` bounds a single cell).  usage: python3 run1.py n,m,t,D
Uses L014/L016's streamed engine (stream.install), ext_d = ext_d_fast.  Refuses to start if a component cell is missing
(dependencies are computed by earlier invocations in plan order).  Appends one line to $PROGRESS_TSV right after the cell is saved:
cell classes inputs nodes seconds bad_tau (+ hits, utc, route).  Guard: aborts if the concatenated chunk key files exceed 2,000,000 lines."""
import os, sys, time, math, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import engine, stream
stream.install()
PT = os.environ.get('PROGRESS_TSV', os.path.join(HERE, '..', 'progress.tsv'))
LIM = 2000000
key = tuple(map(int, sys.argv[1].split(',')))
def deps(k):
    n, m, t, D = k; out = []
    if m <= engine.MD: return out
    for d in range(max(1, math.ceil(3 * m / n)), D + 1):
        for tp in (t - 1, t):
            Sp = 3 * (n - 1) + 2 * (m - d) - 11 * tp
            if Sp < 0 or tp < 0: continue
            for dec in engine.decompositions(n - 1, m - d, Sp):
                for typ in set(dec):
                    c = (typ[0], typ[1], typ[2], d)
                    if c[:2] == (1, 0): continue
                    if c[1] == 0 or c[2] < 1 or c[2] > c[1] or c[0] > 2 * c[1] + 1 or c[1] > c[0] - 2 or 17 * c[2] > 5 * c[0] + 3 * c[1]: continue
                    if engine.load(c) is None: out.append(c)
    return sorted(set(out))
miss = deps(key)
if miss: print('MISSING DEPS', miss); sys.exit(3)
okeys = stream.keys_to_reps
def guarded(keyfiles):
    tot = 0
    for kf in keyfiles:
        with open(kf, 'rb') as f: tot += sum(1 for _ in f)
    if tot > LIM:
        with open(PT, 'a') as f: f.write('%s\tEXPLODED(>%d key lines, files kept in out/work)\t\t\t\t\n' % (str(key), LIM))
        raise RuntimeError('class explosion %d' % tot)
    return okeys(keyfiles)
stream.keys_to_reps = guarded
osave = engine.save
def save(k, reps, info):
    osave(k, reps, info)
    brs = info.get('branches', [])
    inputs = sum(b.get('inputs', 0) for b in brs) if brs else info.get('labelled', '')
    nodes = sum(b.get('ext', {}).get('nodes', 0) for b in brs) if brs else ''
    bad = sum(b.get('ext', {}).get('bad_tau', 0) for b in brs) if brs else ''
    hits = sum(b.get('hits_in_C', 0) for b in brs) if brs else ''
    row = ['(%d,%d,%d,%d)' % k, len(reps), inputs, nodes, info.get('secs', ''), bad, hits, info.get('route'), time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())]
    with open(PT, 'a') as f: f.write('\t'.join(map(str, row)) + '\n')
engine.save = save
t0 = time.time(); r = engine.cell(*key)
print('DONE', key, len(r), round(time.time() - t0, 1), flush=True)
