# Referee round 2: recompute the top recursion level of cell(n,m,t,D) with my own tools (decomp_bf, xr, fr, BLISS) from the prover's
# next-lower lists, and compare the class set with the prover's list (explicit verified relabellings both ways).
import sys, os, re, math, itertools, subprocess, json
H = os.path.dirname(os.path.abspath(__file__)); R = os.path.join(H, '..')
sys.path.insert(0, H)
from decomp_bf import decomps
sys.argv_saved = list(sys.argv); sys.argv = ['x', '0']
exec(open(os.path.join(H, 'bliss_classify.py')).read().split("nv = int(sys.argv[1])")[0])
sys.argv = sys.argv_saved
CD = os.path.join(R, 'out', 'cells_x', 'cells')
def reps(n, m, t, D):
    if (n, m) == (1, 0): return [[]]
    if (n, m, t) == (3, 1, 1): return [[(0, 1, 2)]]
    fn = os.path.join(CD, 'cell_%d_%d_%d_D%d.txt' % (n, m, t, D))
    if not os.path.exists(fn):
        raise RuntimeError('missing lower cell %s' % str((n, m, t, D)))
    return [parse(l) for l in open(fn) if l.startswith('FOUND')]
def lower_exists(n, m, t, D):
    if (n, m) == (1, 0) or (n, m, t) == (3, 1, 1): return True
    return os.path.exists(os.path.join(CD, 'cell_%d_%d_%d_D%d.txt' % (n, m, t, D)))
n, m, t, D = map(int, sys.argv[1:5]); tag = '%d_%d_%d_D%d' % (n, m, t, D)
keep = []; report = []
for d in range(max(1, math.ceil(3 * m / n)), D + 1):
    for tp in (t - 1, t):
        Sp = 3 * (n - 1) + 2 * (m - d) - 11 * tp
        if Sp < 0 or tp < 0: continue
        inputs = []
        for dec in decomps(n - 1, m - d, Sp):
            cnt = {}
            for ty in dec: cnt[ty] = cnt.get(ty, 0) + 1
            # trivial empty rules for connected members of C (t<=m, n<=2m+1, m<=n-2, HY); the prover's engine applies the same
            groups = []
            empty = False
            for ty, k in sorted(cnt.items()):
                a, b, c = ty
                if (a, b) != (1, 0) and (c > b or a > 2 * b + 1 or b > a - 2 or 17 * c > 5 * a + 3 * b): empty = True; break
                if not lower_exists(a, b, c, d): print('NOTE missing lower list', (a, b, c, d), '-> must be empty for the engine'); empty = True; break
                groups.append((ty, reps(a, b, c, d), k))
            if empty: continue
            for combo in itertools.product(*[list(itertools.combinations_with_replacement(range(len(g[1])), g[2])) for g in groups]):
                es = []; off = 0
                for (ty, Rr, k), idxs in zip(groups, combo):
                    for i in idxs: es += [tuple(v + off for v in e) for e in Rr[i]]; off += ty[0]
                assert off == n - 1
                inputs.append('%d ' % len(es) + ' '.join('%d %d %d' % e for e in es))
        if not inputs: report.append(dict(d=d, tp=tp, Sp=Sp, inputs=0)); continue
        fin = os.path.join(R, 'out', 'rc_in_%s_d%d_tp%d.txt' % (tag, d, tp)); open(fin, 'w').write('\n'.join(inputs) + '\n')
        fh = fin + '.hits'
        subprocess.run(['nice', '-n', '5', os.path.join(R, 'out', 'xr'), str(n - 1), str(d), str(d - 1), str(t)], stdin=open(fin), stdout=open(fh, 'w'), stderr=subprocess.DEVNULL, check=True)
        p2 = subprocess.run(['nice', '-n', '5', os.path.join(R, 'out', 'fr'), str(n), 'print'], stdin=open(fh), capture_output=True, text=True); os.remove(fh)
        lines = p2.stdout.splitlines(); summ = lines[-1]
        surv = [l for l in lines if l.startswith('SURV')]
        good = 0
        for l in surv:
            f = dict(kv.split('=') for kv in l.split(':')[0].split()[1:])
            if f['conn'] == '1' and int(f['tau']) == t and int(f['maxdeg']) <= D: keep.append(parse(l.split(':', 1)[1])); good += 1
        report.append(dict(d=d, tp=tp, Sp=Sp, inputs=len(inputs), fr=summ.replace('FRSUMMARY ', ''), kept=good))
for r in report: print(' ', r)
classes = {}
for E in keep:
    k, p = canon(n, E)
    if k not in classes: classes[k] = (E, p)
mine = len(classes)
prov = reps(n, m, t, D)
pk = {}
dup = 0
for E in prov:
    k, p = canon(n, E)
    if k in pk: dup += 1
    pk[k] = (E, p)
miss = [k for k in classes if k not in pk]; extra = [k for k in pk if k not in classes]
okmaps = all(verify_map(n, classes[k][0], classes[k][1], pk[k][0], pk[k][1]) for k in classes if k in pk)
print('CELL', (n, m, t, D), 'connected survivors', len(keep), 'my classes', mine, 'prover classes', len(prov), 'prover dup', dup,
      'mine-not-in-prover', len(miss), 'prover-not-in-mine', len(extra), 'explicit maps ok', okmaps)
