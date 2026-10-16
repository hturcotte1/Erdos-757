"""Exact comparison of the deficient loci computed by Route V (this round) and round-1 Route L (imported read-only, no bytecode written):
the point sets off the common lines must coincide, and the common-line sets must coincide."""
import sys, json, gzip, importlib.util
from fractions import Fraction as F
sys.dont_write_bytecode = True
sys.path.insert(0, '/home/user/Erdos-757/experiments/referee/L006-round3')
import route_V as R
spec = importlib.util.spec_from_file_location('route_L', '/home/user/Erdos-757/experiments/referee/L006-round1/route_L.py')
RL = importlib.util.module_from_spec(spec); spec.loader.exec_module(RL)
cen = json.load(gzip.open('/home/user/Erdos-757/experiments/20261014-1005-census-dfs/results/realized_n12.json.gz', 'rt'))
def points_V(A):
    A = sorted(A); Aset = set(A); k, Ts = R.max_sidon(A)
    excl = {(1, -1, 0)} | {(1, 0, a) for a in A} | {(0, 1, a) for a in A}
    U = [R.lines_of(T, excl) for T in Ts]; order = sorted(range(len(Ts)), key=lambda i: len(U[i])); i1 = order[0]
    common = set(); cand = set()
    for l in U[i1]:
        miss = [i for i in order if l not in U[i]]
        if not miss: common.add(l); continue
        a1, b1, g1 = l
        for (a2, b2, g2) in U[miss[0]]:
            det = a1 * b2 - a2 * b1
            if det == 0: continue
            px = F(g1 * b2 - g2 * b1, det); py = F(a1 * g2 - a2 * g1, det)
            if px == py or px in Aset or py in Aset: continue
            cand.add((px, py))
    return common, {p for p in cand if R.deficient_pt(p[0], p[1], Ts)}, Ts
for c in [int(v) for v in sys.argv[1].split(',')]:
    A = sorted(cen[c]['set'])
    CV, PV, Ts = points_V(A)
    kL, TsL = RL.max_sidon(A)
    LL, PL, _ = RL.deficient_locus(A, TsL)
    PL = {(F(X, d), F(Y, d)) for X, Y, d in PL}
    CL = {tuple(RL.norm(*l)) if hasattr(RL, 'norm') else tuple(l) for l in LL}
    on = lambda p, C: any(a * p[0] + b * p[1] == g for a, b, g in C)
    offV = {p for p in PV if not on(p, CV)}; offL = {p for p in PL if not on(p, CV)}
    print(json.dumps({'class': c, 'common_V': sorted(CV), 'common_L': sorted(CL), 'common_equal': CV == CL, 'V_points': len(PV), 'L_points': len(PL),
                      'V_off_common': len(offV), 'L_off_common': len(offL), 'off_common_sets_equal': offV == offL,
                      'V_on_common': len(PV) - len(offV), 'L_on_common': len(PL) - len(offL)}), flush=True)
