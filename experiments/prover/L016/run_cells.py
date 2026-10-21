"""(L014) python3 run_cells.py [--orig] key1 key2 ...   (key = n,m,t,D)
Computes the cells in the given order with engine.cell (streamed twins of direct/recurse unless --orig), appends one JSON line per
cell to $PROGRESS (default out/progress.jsonl).  CELLDIR, ENGINELOG, NPROC, MD as for engine.py."""
import os, sys, json, time
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
args = sys.argv[1:]; orig = False
if args and args[0] == '--orig': orig = True; args = args[1:]
import engine, stream
if not orig: stream.install()
prog = os.environ.get('PROGRESS', os.path.join(HERE, 'out', 'progress.jsonl'))
for a in args:
    key = tuple(map(int, a.split(',')))
    t0 = time.time(); reps = engine.cell(*key); secs = round(time.time() - t0, 1)
    rec = dict(cell=key, classes=len(reps), secs=secs, driver='orig' if orig else 'stream', MD=engine.MD, NPROC=engine.NPROC,
               celldir=engine.OUT, utc=time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()))
    with open(prog, 'a') as f: f.write(json.dumps(rec) + '\n')
    print('DONE', json.dumps(rec), flush=True)
