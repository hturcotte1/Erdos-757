# Referee round 2: build route-4 / route-20 inputs from the prover's cell lists (decompositions from my own brute force).
import re, sys, itertools, subprocess
sys.path.insert(0, '/home/user/Erdos-757/experiments/referee/L012-round2/src')
from decomp_bf import decomps
cdir = '/home/user/Erdos-757/experiments/referee/L012-round2/out/cells_x/cells/'
def reps(n, m, t, D):
    if (n, m, t) == (3, 1, 1): return [[(0, 1, 2)]]
    return [[tuple(map(int, x.split(','))) for x in re.findall(r'\((\d+,\d+,\d+)\)', l)] for l in open(cdir + 'cell_%d_%d_%d_D%d.txt' % (n, m, t, D)) if l.startswith('FOUND')]
route = sys.argv[1]; D = {'4': 4, '20': 3}[route]
decs = decomps(22, 17, 1)
inputs = []; summary = []
for dec in decs:
    cnt = {}
    for ty in dec: cnt[ty] = cnt.get(ty, 0) + 1
    groups = [(ty, reps(*ty, D), k) for ty, k in sorted(cnt.items())]
    # validate each representative with fr: in C, connected, right parameters, max degree <= D
    for ty, R, k in groups:
        if ty == (3, 1, 1): continue
        out = subprocess.run(['./out/fr', str(ty[0]), 'print'], input=''.join('X: ' + ' '.join('(%d,%d,%d)' % e for e in E) + '\n' for E in R), capture_output=True, text=True).stdout
        sv = [l for l in out.splitlines() if l.startswith('SURV')]
        assert len(sv) == len(R), ('rep not in C', ty)
        for l in sv:
            f = dict(kv.split('=') for kv in l.split(':')[0].split()[1:])
            assert f['conn'] == '1' and int(f['tau']) == ty[2] and int(f['maxdeg']) <= D, (ty, l)
        assert all(len(E) == ty[1] and max(max(e) for e in E) < ty[0] for E in R)
    sizes = []
    choice_lists = []
    for ty, R, k in groups:
        cs = list(itertools.combinations_with_replacement(range(len(R)), k)); choice_lists.append(cs); sizes.append(len(cs))
    summary.append((dec, [len(R) for ty, R, k in groups], sizes))
    for combo in itertools.product(*choice_lists):
        es = []; off = 0
        for (ty, R, k), idxs in zip(groups, combo):
            for i in idxs:
                es += [tuple(v + off for v in e) for e in R[i]]; off += ty[0]
        assert off == 22 and len(es) == 17
        inputs.append('%d ' % len(es) + ' '.join('%d %d %d' % e for e in es))
print('route', route, 'decompositions', summary, 'inputs', len(inputs))
open('out/route%s_in.txt' % route, 'w').write('\n'.join(inputs) + '\n')
# compare with the prover's input file as sets of edge sets
P = '/home/user/Erdos-757/experiments/prover/L012/out/route%s_inputs.txt' % route
def key(l):
    a = list(map(int, l.split())); return tuple(sorted(tuple(sorted(a[1 + 3 * i: 4 + 3 * i])) for i in range(a[0])))
mine = set(key(l) for l in inputs); theirs = set(key(l) for l in open(P) if l.strip())
print('identical to the prover\'s input set:', mine == theirs, len(mine), len(theirs))
