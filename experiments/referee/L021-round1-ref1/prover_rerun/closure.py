"""L021: compute the irreducible special family L (epsilon = 1/6) on the stored complete Delta<=3 cell lists
whose shifted slack A = 27n + 35m - 132 tau is negative, in increasing n; verify KT (A + DEF >= 0) for every
stored graph of these cells; record the pieces.  Run: python3 closure.py > closure_output.txt"""
import json, sys, time
sys.path.insert(0, '/home/user/Erdos-757/experiments/referee/L021-round1-ref1/prover_rerun')
from kt import *
rows = json.load(open('/home/user/Erdos-757/experiments/referee/L021-round1-ref1/prover_rerun/special_cells.json'))
cells = []
for r in rows:
    st = r['stored']
    if not st: continue
    st = eval(st) if isinstance(st, str) else st
    if st[0] == 'only D2': continue
    cells.append((r['n'], r['m'], r['tau'], r['A'], st[1]))
cells.sort()
L = []
summary = []
t0 = time.time()
for (n, m, t, A, path) in cells:
    gs = read_cell(path)
    gs = [g for g in gs if max([sum(1 for e in g if x in e) for x in range(nverts(g))] or [0]) <= 3]
    irr = 0; red = 0; tight_red = 0; minP = None
    newpieces = []
    for gi, g in enumerate(gs):
        assert nverts(g) == n and len(g) == m
        tt = tau_masks(masks(g)); assert tt == t, (n, m, t, tt)
        D, fam, ncop = deficiency(n, g, L, proper=True, want_family=True)
        P = A + D
        minP = P if minP is None else min(minP, P)
        if P < 0:
            irr += 1; newpieces.append(Piece(g, f'({n},{m},{t})#{gi}'))
        else:
            red += 1
            if P == 0: tight_red += 1
    L.extend(newpieces)
    summary.append(dict(cell=(n, m, t), A=A, graphs=len(gs), irreducible=irr, reducible=red, reducible_with_equality=tight_red,
                        min_A_plus_DEF_over_proper_pieces=minP))
    print(f"cell ({n},{m},{t}) A={A}: {len(gs)} graphs, irreducible {irr}, reducible {red} (equality {tight_red}), min(A+DEF_proper)={minP}  [{time.time()-t0:.0f}s]", flush=True)
print('IRREDUCIBLE SPECIAL PIECES (epsilon = 1/6):', len(L))
for P in L:
    print(' ', P.name, 'W =', P.W, 'deg seq', sorted(P.deg, reverse=True), 'edges', P.edges)
json.dump(dict(summary=summary, pieces=[dict(name=P.name, n=P.n, m=P.m, tau=P.tau, W=P.W, edges=P.edges) for P in L]),
          open('/home/user/Erdos-757/experiments/referee/L021-round1-ref1/prover_rerun/closure_results.json', 'w'), indent=1)
