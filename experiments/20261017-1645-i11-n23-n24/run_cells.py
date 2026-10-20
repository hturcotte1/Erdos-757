"""Driver: python3 run_cells.py n m tau Delta [more cells...] ; MD/NPROC from the environment.  Appends to results_cells.jsonl."""
import os, sys, json, time
HERE = os.path.dirname(os.path.abspath(__file__))
os.environ.setdefault('CELLDIR', os.path.join(HERE, 'out', 'cells'))
os.environ.setdefault('ENGINELOG', os.path.join(HERE, 'out', 'engine.log'))
sys.path.insert(0, HERE)
import engine
args = list(map(int, sys.argv[1:]))
for i in range(0, len(args), 4):
    key = tuple(args[i:i + 4]); t0 = time.time()
    reps = engine.cell(*key)
    rec = dict(cell=key, classes=len(reps), secs=round(time.time() - t0, 1), MD=engine.MD, celldir=engine.OUT)
    print('TOP', rec, flush=True)
    open(os.path.join(HERE, os.environ.get('RESJSONL', 'results_cells.jsonl')), 'a').write(json.dumps(rec) + '\n')
