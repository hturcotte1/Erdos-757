"""python3 run_one.py n m tau D : compute one cell with the unchanged L012 engine and append a line to progress.tsv immediately."""
import os, sys, json, time
HERE = os.path.dirname(os.path.abspath(__file__))
os.environ.setdefault('CELLDIR', os.path.join(HERE, 'out', 'cells'))
os.environ.setdefault('ENGINELOG', os.path.join(HERE, 'out', 'engine.log'))
sys.path.insert(0, HERE)
import engine, streamdirect
_orig = engine.direct
engine.direct = lambda n, m, t, D: (streamdirect.direct(n, m, t, D) if n >= 13 else _orig(n, m, t, D))
key = tuple(map(int, sys.argv[1:5])); t0 = time.time()
reps = engine.cell(*key)
secs = round(time.time() - t0, 1)
info = {}
p = os.path.join(engine.OUT, 'cell_%d_%d_%d_D%d.txt' % key)
for l in open(p):
    if l.startswith('INFO '): info = json.loads(l[5:])
inputs = sum(b.get('inputs', 0) for b in info.get('branches', []))
bad = sum(b.get('ext', {}).get('bad_tau', 0) for b in info.get('branches', []))
nodes = sum(b.get('ext', {}).get('nodes', 0) for b in info.get('branches', []))
line = '\t'.join(map(str, ['(%d,%d,%d,%d)' % key, len(reps), secs, info.get('route'), inputs, bad, nodes]))
with open(os.path.join(HERE, 'progress.tsv'), 'a') as f: f.write(line + '\n')
print('DONE', line, flush=True)
