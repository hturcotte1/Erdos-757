"""KT check for connected members of C_3 with n<=27 (L021 closure.py extended).
Input: scan2_<AMAX>.json (cells with A<=AMAX and their stored D3 list).  Pass 1: cells with A<0 in increasing (n,m,tau): for every
graph (Delta<=3 filter), recompute tau, DEF over the pieces found so far (proper induced copies), P=A+DEF; P<0 => irreducible special
piece (added to L).  Pass 2: cells with 0<=A<=AMAX (informational: P>=A>=0 trivially): min P and #P==A etc.
Cells without a stored list are reported as MISSING and make the verdict INCOMPLETE.
usage: python3 closure2.py AMAX > closure2_output.txt"""
import json, sys, time
sys.path.insert(0, '/home/user/Erdos-757/experiments/prover/L021')
from kt import *
AMAX = int(sys.argv[1])
rows = json.load(open(f'scan2_{AMAX}.json'))
rows.sort(key=lambda r: (r['n'], r['m'], r['tau']))
old = json.load(open('/home/user/Erdos-757/experiments/prover/L021/closure_results.json'))['pieces']
oldkeys = {(p['n'], p['m'], p['tau'], len(p['edges'])) for p in old}
L = []; summary = []; missing = []; t0 = time.time()
def run_cell(r, pas):
    n, m, t, A = r['n'], r['m'], r['tau'], r['A']
    if not r.get('path'):
        missing.append((n, m, t, A)); print(f"cell ({n},{m},{t}) A={A}: MISSING list", flush=True); return
    gs = [g for g in read_cell(r['path']) if max([sum(1 for e in g if x in e) for x in range(nverts(g))] or [0]) <= 3]
    irr = red = eq = 0; minP = None; newp = []
    for gi, g in enumerate(gs):
        assert nverts(g) == n and len(g) == m, (n, m, t)
        assert tau_masks(masks(g)) == t, (n, m, t)
        D, fam, ncop = deficiency(n, g, L, proper=True, want_family=True)
        P = A + D
        minP = P if minP is None else min(minP, P)
        if P < 0: irr += 1; newp.append(Piece(g, f'({n},{m},{t})#{gi}'))
        else:
            red += 1
            if P == 0: eq += 1
    L.extend(newp)
    summary.append(dict(cell=[n, m, t], A=A, source=r['src'], path=r['path'], graphs=len(gs), irreducible=irr, reducible=red,
                        P_zero=eq, minP=minP, pass_=pas))
    print(f"cell ({n},{m},{t}) A={A}: {len(gs)} graphs, irreducible {irr}, reducible {red} (P==0: {eq}), min P={minP}  [{r['src']}] [{time.time()-t0:.0f}s]", flush=True)
for r in rows:
    if r['A'] < 0: run_cell(r, 1)
npieces1 = len(L)
for r in rows:
    if r['A'] >= 0: run_cell(r, 2)
assert len(L) == npieces1
print('IRREDUCIBLE SPECIAL PIECES:', len(L))
new = [P for P in L if (P.n, P.m, P.tau, len(P.edges)) not in oldkeys or P.n >= 25]
print('NEW pieces beyond L021 closure (n>=25 or unseen type):', len(new))
for P in new: print('  NEW', P.name, 'W =', P.W, P.edges)
print('MISSING lists:', missing)
json.dump(dict(amax=AMAX, summary=summary, missing=missing,
               pieces=[dict(name=P.name, n=P.n, m=P.m, tau=P.tau, W=P.W, edges=P.edges) for P in L]), open('closure2_results.json', 'w'), indent=1)
