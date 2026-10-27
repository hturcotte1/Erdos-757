import sys
sys.path.insert(0, '/home/user/Erdos-757/experiments/referee/L020-round1-opus')
import hg
from roles_check import read_cell, analyse
I = '/home/user/Erdos-757/experiments/20261027-0300-transversal-richness/inputs/'
for c in sys.argv[1:]:
    L = [g for g in read_cell(I + 'cell_%s.txt' % c) if max(hg.degrees(g[0], g[3])) <= 3]
    with_any = with_nonedge = with_e = 0
    for n, m, t, es in L:
        TL, d, NC, b_any, e_cfg, f_cfg, B = analyse(n, es, t)
        E = set(frozenset(e) for e in es)
        ne = [b for b in b_any if frozenset(b) not in E]
        with_any += bool(b_any); with_nonedge += bool(ne); with_e += bool(e_cfg)
    print(c, 'classes', len(L), 'b-config (edges allowed)', with_any, 'b-config (not an edge)', with_nonedge, 'e-config', with_e, flush=True)
