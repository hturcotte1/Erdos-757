import sys, itertools
sys.path.insert(0, '/home/user/Erdos-757/experiments/referee/L020-round1-opus')
import hg
from t1_verify import parse_k29
from roles_check import read_cell, analyse
K = parse_k29()
F = [e for e in K if max(e) <= 19]
X = [tuple(x - 20 for x in e) for e in K if min(e) >= 20 and max(e) <= 27]
print('K - 28 = F + X ?', len(F) + len(X) == 20 and all(28 in e for e in K if e not in F and min(e) < 20 or 28 in e) )
for name, n, es in [('F', 20, F), ('X', 8, X)]:
    t = hg.tau_bb(es)
    TL, d, NC, b_any, e_cfg, f_cfg, B = analyse(n, es, t)
    print(name, 'n', n, 'm', len(es), 'tau', t, 'slack', hg.slack(n, len(es), t), 'connected', hg.is_connected(n, es), 'maxdeg', max(d),
          'e-configs', e_cfg, 'in C', hg.in_C(n, es))
I = '/home/user/Erdos-757/experiments/20261027-0300-transversal-richness/inputs/'
for name, n, es, cell in [('F', 20, F, 'cell_20_15_8.txt'), ('X', 8, X, 'cell_8_5_3.txt')]:
    L = read_cell(I + cell)
    hits = [i for i, (nn, mm, tt, ee) in enumerate(L) if hg.iso_exact(n, es, nn, ee) is not None]
    print(name, 'isomorphic to stored class index', hits, 'of', cell)
