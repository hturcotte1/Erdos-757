"""(L014) Equivalence of the streamed driver (stream.py) with the unmodified engine.direct / engine.recurse.
python3 equiv_check.py MAINCELLS WORKROOT TIMEOUT cell1 cell2 ...   (cell = n,m,t,D; each must be complete in MAINCELLS)
For each cell: a fresh directory WORKROOT/<cell>/cells receives copies of the complete cell files of MAINCELLS of the cells visited below the cell (tree.py dry run), not of the cell itself;
`run_cells.py --orig` (engine.py unchanged, its own direct/recurse, NPROC=1, MD=10) recomputes the cell there; the list of
representatives (FOUND lines) must equal the streamed main run's list as a set, and for recursion cells every branch must have the same
(d, t', S', number of decompositions, number of inputs, all ext_d counters, hits_in_C) and the same connected_hits."""
import sys, os, json, shutil, subprocess, time
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
os.environ.setdefault('CELLDIR', os.path.join(HERE, 'out', 'dummycells')); os.environ.setdefault('ENGINELOG', os.devnull)
import tree
main, root, TO = sys.argv[1], sys.argv[2], int(sys.argv[3])
def load(fn):
    reps, info = [], None
    for l in open(fn):
        if l.startswith('FOUND:'): reps.append(l.rstrip('\n'))
        elif l.startswith('INFO '): info = json.loads(l[5:])
    return reps, info
def brsig(info):
    out = []
    for b in info.get('branches', []):
        out.append((b['d'], b['tp'], b['Sp'], b['decompositions'], b['inputs'], tuple(sorted(b.get('ext', {}).items())), b.get('hits_in_C', 0)))
    return out
allok = True
for c in sys.argv[4:]:
    key = tuple(map(int, c.split(','))); fn = 'cell_%d_%d_%d_D%d.txt' % key
    d = os.path.join(root, '%d_%d_%d_D%d' % key); shutil.rmtree(d, ignore_errors=True); os.makedirs(os.path.join(d, 'cells'))
    # copy the complete files of the cells the engine visits below this cell (dry run of tree.py), not the cell itself
    seen, order, need = {}, [], {}
    tree.visit(key, 10, seen, order, need)
    for k in order:
        f = 'cell_%d_%d_%d_D%d.txt' % k
        if k != key and os.path.exists(os.path.join(main, f)) and load(os.path.join(main, f))[1] is not None: shutil.copy(os.path.join(main, f), os.path.join(d, 'cells', f))
    env = dict(os.environ, CELLDIR=os.path.join(d, 'cells'), ENGINELOG=os.path.join(d, 'engine.log'), NPROC='1', MD='10', PROGRESS=os.path.join(d, 'progress.jsonl'))
    t0 = time.time()
    try:
        r = subprocess.run(['python3', os.path.join(HERE, 'run_cells.py'), '--orig', c], env=env, capture_output=True, text=True, timeout=TO)
        rc = r.returncode
    except subprocess.TimeoutExpired:
        rc = 'TIMEOUT'
    secs = round(time.time() - t0, 1)
    if rc != 0: print('cell %s: original engine rc=%s after %.1f s, no comparison' % (key, rc, secs), flush=True); allok = False; continue
    mo, io = load(os.path.join(d, 'cells', fn)); ms, isr = load(os.path.join(main, fn))
    same = set(mo) == set(ms) and len(mo) == len(ms)
    route = io.get('route'); extra = ''
    if route == 'recurse':
        bs_o, bs_s = brsig(io), brsig(isr); same_b = (bs_o == bs_s) and io.get('connected_hits') == isr.get('connected_hits')
        extra = ' branches %d, branch data and connected_hits (%s) %s' % (len(bs_o), io.get('connected_hits'), 'EQUAL' if same_b else 'DIFFERENT'); same = same and same_b
    else:
        same_d = io.get('enum') == isr.get('enum') and io.get('labelled') == isr.get('labelled') and io.get('in_C_tau_exact') == isr.get('in_C_tau_exact')
        extra = ' enum/labelled/in_C counters (%s, %s) %s' % (io.get('labelled'), io.get('in_C_tau_exact'), 'EQUAL' if same_d else 'DIFFERENT'); same = same and same_d
    allok = allok and same
    print('cell %s (%s): original engine %d classes in %.1f s, streamed main run %d classes: representative sets %s;%s' % (key, route, len(mo), secs, len(ms), 'EQUAL' if set(mo) == set(ms) else 'DIFFERENT', extra), flush=True)
    shutil.rmtree(os.path.join(d, 'cells'))
print('SUMMARY all compared cells equal:', allok)
