"""Referee check of the 32 pieces of L*: membership, parameters, weights, (L1), degree sequences,
non-co-transversal pairs, richness; and agreement with the stored cell lists (Delta<=3 classes)."""
import sys, json
from itertools import combinations
from rlib import *

pieces = load_pieces()
INP = '/home/user/Erdos-757/experiments/20261027-0300-transversal-richness/inputs/'
cells = {(3,1,1):'cell_3_1_1.txt',(8,5,3):'cell_8_5_3.txt',(10,7,4):'cell_10_7_4.txt',(15,11,6):'cell_15_11_6.txt',(17,13,7):'cell_17_13_7.txt'}
out = {}
rich_names = []; nonrich_names = []
for name, n, E, rec in pieces:
    m = len(E)
    d = degs(n, E)
    t, mts = min_transversals(n, E)
    A = 27*n + 35*m - 132*t
    W = -A
    ok = in_C3(n, E) and connected(n, E)
    L1 = all(any(T >> x & 1 for T in mts) for x in range(n))
    nct = []
    for x, y in combinations(range(n), 2):
        if not any((T >> x & 1) and (T >> y & 1) for T in mts):
            nct.append((x, y))
    rich = (len(nct) == 0)
    (rich_names if rich else nonrich_names).append(name)
    degseq = sorted(d, reverse=True)
    out[name] = dict(n=n, m=m, tau=t, W=W, inC3_conn=ok, L1=L1, nmt=len(mts), maxdeg=max(d),
                     degseq=''.join(map(str, degseq)), n_nct=len(nct), nct=nct[:12], rich=rich,
                     stored_match=(n == rec['n'] and m == rec['m'] and t == rec['tau'] and W == rec['W']))
    print(name, out[name])
print('RICH', rich_names)
print('NONRICH', nonrich_names)
print('Delta<=2 pieces', [nm for nm in out if out[nm]['maxdeg'] <= 2])
# compare with stored complete cell lists, filtered to Delta<=3
for cell, fn in cells.items():
    L = load_cell(INP + fn)
    L3 = [(n, E) for (n, m, t, E) in L if max(degs(n, E)) <= 3]
    P = [(n, E) for (name, n, E, rec) in pieces if (n, len(E)) == cell[:2]]
    # check stored entries: params, C3 membership, tau
    for (n, E) in L3:
        t, _ = min_transversals(n, E)
        assert t == cell[2] and in_C3(n, E) and connected(n, E), (cell, E)
    # bijection up to isomorphism
    used = [False]*len(P)
    okmatch = True
    for (n, E) in L3:
        hit = [j for j, (n2, E2) in enumerate(P) if isomorphic(n, E, n2, E2)]
        if len(hit) != 1:
            okmatch = False
        else:
            used[hit[0]] = True
    # pairwise non-isomorphic pieces
    pair_iso = sum(1 for i in range(len(P)) for j in range(i+1, len(P)) if isomorphic(P[i][0], P[i][1], P[j][0], P[j][1]))
    print('cell', cell, 'stored', len(L), 'stored Delta<=3', len(L3), 'pieces', len(P), 'bijection', okmatch and all(used), 'iso pairs among pieces', pair_iso)
json.dump(out, open('check_pieces_out.json', 'w'), indent=1)
