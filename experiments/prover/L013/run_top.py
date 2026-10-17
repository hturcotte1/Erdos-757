"""(L013, prover) Driver for the top-level violator cells.  Usage: python3 run_top.py n m tau D [n m tau D ...]
Runs engine.cell(n, m, tau, D) (the L012 engine, byte-identical copy in this directory) for each listed cell, in the given order,
and appends one JSON line per cell to $TOPJSONL (default top_results.jsonl).  CELLDIR, ENGINELOG, NPROC, MD come from the environment."""
import os, sys, json, time
HERE = os.path.dirname(os.path.abspath(__file__))
os.environ.setdefault('CELLDIR', os.path.join(HERE, 'out', 'cells'))
os.environ.setdefault('ENGINELOG', os.path.join(HERE, 'out', 'engine.log'))
sys.path.insert(0, HERE)
import engine
a = list(map(int, sys.argv[1:])); assert len(a) % 4 == 0
for i in range(0, len(a), 4):
    key = tuple(a[i:i + 4]); t0 = time.time()
    reps = engine.cell(*key)
    rec = dict(cell=list(key), classes=len(reps), secs=round(time.time() - t0, 1), MD=engine.MD, NPROC=engine.NPROC, celldir=engine.OUT)
    print('TOP', json.dumps(rec), flush=True)
    with open(os.environ.get('TOPJSONL', os.path.join(HERE, 'top_results.jsonl')), 'a') as f: f.write(json.dumps(rec) + '\n')
