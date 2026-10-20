"""(L014) Cross-check (c): direct enumeration of recursion cells.
python3 crosscheck_direct.py MAINCELLS WORKROOT TIMEOUT [--orig] cell1 cell2 ...
For each cell: an EMPTY directory WORKROOT/<cell>/cells, MD = 99, so engine.cell takes the direct route for the cell itself
(`enum_conn n m t D` (L007 Lemma D), `filt FOUND n tau t`, `canon`), without any sub-cell and without I11; streamed direct (stream.py)
unless --orig.  The resulting list must equal the main run's list (computed by the recursion) as a set of canonical forms."""
import sys, os, json, shutil, subprocess, time
HERE = os.path.dirname(os.path.abspath(__file__))
args = sys.argv[1:]; main, root, TO = args[0], args[1], int(args[2]); rest = args[3:]
orig = bool(rest and rest[0] == '--orig');
if orig: rest = rest[1:]
def load(fn):
    reps, info = [], None
    for l in open(fn):
        if l.startswith('FOUND:'): reps.append(l.rstrip('\n'))
        elif l.startswith('INFO '): info = json.loads(l[5:])
    return reps, info
for c in rest:
    key = tuple(map(int, c.split(','))); fn = 'cell_%d_%d_%d_D%d.txt' % key
    d = os.path.join(root, '%d_%d_%d_D%d' % key); shutil.rmtree(d, ignore_errors=True); os.makedirs(os.path.join(d, 'cells'))
    env = dict(os.environ, CELLDIR=os.path.join(d, 'cells'), ENGINELOG=os.path.join(d, 'engine.log'), NPROC='1', MD='99',
               PROGRESS=os.path.join(d, 'progress.jsonl'), WORKDIR=os.path.join(d, 'work'))
    t0 = time.time()
    try:
        r = subprocess.run(['python3', os.path.join(HERE, 'run_cells.py')] + (['--orig'] if orig else []) + [c], env=env, capture_output=True, text=True, timeout=TO)
        rc = r.returncode
    except subprocess.TimeoutExpired:
        rc = 'TIMEOUT'
    secs = round(time.time() - t0, 1)
    if rc != 0:
        print('cell %s: direct route rc=%s after %.1f s (cap %d s): no result' % (key, rc, secs, TO), flush=True)
        subprocess.run('pkill -f "enum_conn %d %d %d %d 1"' % key, shell=True); continue
    md, idd = load(os.path.join(d, 'cells', fn)); mm, im = load(os.path.join(main, fn))
    print('cell %s: main run (%s) %d classes; direct %d classes (%s, %s labelled, %s in C with tau = t; %.1f s): %s' % (
        key, im.get('route'), len(mm), len(md), idd.get('enum'), idd.get('labelled'), idd.get('in_C_tau_exact'), secs,
        'EQUAL' if set(md) == set(mm) and len(md) == len(mm) else 'DIFFERENT'), flush=True)
