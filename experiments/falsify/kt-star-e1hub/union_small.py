import sys, json, glob, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import hubs, kt
# components: every stored class in {cells with A<=31} with >=2 low non-inT vertices  (+ E1) -- here (7,3,2) and neighbours, by direct scan of given cells
def load_cells(paths):
    gs = []
    for p in paths: gs += kt.read_cell(p)
    return gs
E1 = [(0, 1, 2)]
paths = glob.glob('/home/user/Erdos-757/experiments/prover/L017/out/L01[2-6]/cells*/cell_7_3_2_D3.txt')[:1]
print(paths)
res = []
for C1 in load_cells(paths):
    n1 = kt.nverts(C1); t1 = kt.tau_masks(kt.masks(C1))
    A1 = kt.A_value(n1, len(C1), t1)
    for k in (1, 2):   # G' = C1 + k copies of E1
        n = n1 + 3 * k; E = list(C1)
        for i in range(k): E += [tuple(n1 + 3 * i + x for x in (0, 1, 2))]
        t = t1 + k
        bc, nT, notin = hubs.bconfigs(n, E, t)
        print('C1', C1, 'A1', A1, 'copies E1', k, 'bconfigs', len(bc), 'notinT', notin)
        reg = hubs.Registry()
        for (a, b, c) in bc:
            n2, E2 = hubs.add_hub(n, E, a, b, c)
            rec, new = reg.lookup(n2, E2)
            if not new: continue
            r = hubs.analyse_H(n2, E2, t + 2)
            print('   hub', (a, b, c), {x: r.get(x) for x in ('n', 'm', 'inC', 'tau', 'A', 'DEF', 'P', 'Pp', 'piece')})
