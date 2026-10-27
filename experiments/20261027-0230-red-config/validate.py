import sys, json, subprocess, random, os
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
sys.path.insert(0, ROOT); sys.path.insert(0, HERE)
from e757.core import ap_edges
from redfree import red_report
def cline(EE): return 'C %d %s\n' % (len(EE), ' '.join('%d.%d.%d' % tuple(sorted(e)) for e in EE))
def c_run(EE, n):
    p = subprocess.run([os.path.join(HERE, 'bin', 'redfree'), str(n)], input=cline(EE), capture_output=True, text=True, check=True)
    return p.stdout.rstrip('\n').split('\t')
out = {}
# 1. cross-validation C vs Python on random classes
random.seed(1); nchk = 0
for n, m in [(6,3),(7,4),(8,5),(8,6),(9,6),(9,7),(10,7)]:
    L = [l.split() for l in open(os.path.join(HERE, 'out', f'cls_{n}_{m}.txt'))]
    for l in random.sample(L, min(40, len(L))):
        EE = [tuple(map(int, x.split('.'))) for x in l[2:]]
        r = red_report(EE, vertices=range(n)); c = c_run(EE, n)
        assert (r['best_value'], int(r['redfree']), r['tau']) == (int(c[6]), 1 - int(c[5]) if False else int(c[5]), int(c[2])), (EE, r, c)
        nchk += 1
out['c_vs_python_graphs_checked'] = nchk
# 2. single AP
r = red_report([(0,1,2)]); out['single_AP'] = {k: v for k, v in r.items() if k != 'red_pairs'}
# 3. A_base and the (10,7,4) piece
d = json.load(open(os.path.join(ROOT, 'data', 'small_records.json')))
A = sorted(d['sets']['14']['set']); idx = {a: i for i, a in enumerate(A)}
E14 = [tuple(sorted(idx[x] for x in e)) for e in ap_edges(A)]
c = c_run(E14, 14); out['A_base'] = dict(n=14, m=len(E14), edges=E14, C_tool=c[:13])
# deg of 0
deg = [sum(v in e for e in E14) for v in range(14)]; out['A_base']['degrees'] = deg
# remove vertex 0 and then the isolated AP
rest = [e for e in E14 if 0 not in e]
comp = {}
# connected components
import itertools
par = list(range(14))
def f(x):
    while par[x] != x: par[x] = par[par[x]]; x = par[x]
    return x
for e in rest:
    for x in e[1:]: par[f(x)] = f(e[0])
cc = {}
for e in rest: cc.setdefault(f(e[0]), []).append(e)
out['A_base_minus_0_components'] = [(len(v), len(set(x for e in v for x in e))) for v in cc.values()]
big = max(cc.values(), key=len); vs = sorted(set(x for e in big for x in e)); rl = {v: i for i, v in enumerate(vs)}
P = [tuple(rl[x] for x in e) for e in big]
c = c_run(P, len(vs)); r = red_report(P, vertices=range(len(vs)), want_all=False)
out['piece_10_7_4'] = dict(n=len(vs), m=len(P), edges=P, C_tool=c[:13], python={k: v for k, v in r.items() if k != 'red_pairs'})
# all optimal pairs of the piece: list Z with max value
r2 = red_report(P, vertices=range(len(vs)), want_all=True)
out['piece_10_7_4']['num_red_Z'] = r2['num_red_Z']; out['piece_10_7_4']['red_pairs'] = r2['red_pairs'][:20]
# A_base python check on full (2^14 subsets; slow) -> use only C result; also check python for A_base minus 0 (13 vertices incl. isolated AP)
json.dump(out, open(os.path.join(HERE, 'validate_out.json'), 'w'), indent=1, default=list)
print(json.dumps(out, indent=1, default=list)[:4000])
