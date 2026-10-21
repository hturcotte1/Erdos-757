"""python3 recompute.py n m t D CELLDIR [--save OUT.g6]
Referee's own recomputation of cell(n,m,t,D) from the lower lists in CELLDIR (data only): branches, own decompositions (compared
with the decomposition list in the stored file's INFO line), own input construction, own extension program rext, nauty labelg;
compares the class set with the stored list cell_n_m_t_D<D>.txt in CELLDIR."""
import sys, os, time, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rlib
n, m, t, D = map(int, sys.argv[1:5]); celldir = sys.argv[5]
save = sys.argv[sys.argv.index('--save') + 1] if '--save' in sys.argv else None
t0 = time.time()
stored, info = rlib.read_cell(rlib.cell_path(celldir, n, m, t, D))
mine = set(); tot_inputs = 0
info_br = {(b['d'], b['tp']): b for b in (info or {}).get('branches', [])}
for (d, tp, Sp) in rlib.branches(n, m, t, D):
    decs = rlib.my_decomps(n - 1, m - d, Sp)
    b = info_br.get((d, tp))
    cmpmsg = ''
    if b is not None:
        theirs = sorted(tuple(sorted(tuple(x) for x in dec)) for dec, size in b['dec'])
        cmpmsg = 'decomps_equal_to_INFO=%s' % (theirs == decs)
        their_sizes = {tuple(sorted(tuple(x) for x in dec)): size for dec, size in b['dec']}
    lines = []; sizes = []
    for dec in decs:
        try:
            L = list(rlib.inputs_for(dec, celldir, d, n - 1))
        except FileNotFoundError as e:
            print('  MISSING list for decomposition', dec, e); L = []
            sizes.append((dec, 'MISSING')); continue
        sizes.append((dec, len(L))); lines += L
        if b is not None and their_sizes.get(dec) != len(L): print('  SIZE MISMATCH', dec, len(L), their_sizes.get(dec))
    tot_inputs += len(lines)
    if lines:
        s, summ, nout = rlib.run_ext(lines, n - 1, tp, d, d - 1) if tp == t - 1 else (None, None, None)
        if tp != t - 1: raise SystemExit('branch tp = t not supported')
        mine |= s
    else: summ = 'no inputs'
    print('branch d=%d tp=%d S=%d decompositions=%d inputs=%d %s | %s' % (d, tp, Sp, len(decs), len(lines), cmpmsg, summ), flush=True)
    if b is not None: print('   prover INFO: decompositions=%d inputs=%d ext=%s' % (b['decompositions'], b['inputs'], b.get('ext')))
st = rlib.canon_set_of_reps(stored, n)
print('RESULT cell(%d,%d,%d,%d): mine=%d stored=%d stored_distinct=%d equal=%s mine-stored=%d stored-mine=%d inputs=%d secs=%.1f' % (
    n, m, t, D, len(mine), len(stored), len(st), mine == st, len(mine - st), len(st - mine), tot_inputs, time.time() - t0))
if save:
    with open(save, 'w') as f: f.write('\n'.join(sorted(mine)) + ('\n' if mine else ''))
