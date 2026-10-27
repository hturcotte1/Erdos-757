"""Referee #2 (L021): independent cell scan + closure (Theorem 7(i),(ii)), (L1) and weights (7(iii)).
Own parser, SAT tau, edge-subset+VF2 copies, own DEF maximisation.  Compares with closure_results.json at the end."""
import os, re, sys, json, time
sys.path.insert(0, '/home/user/Erdos-757/experiments/referee/L021')
from ref_lib import *
ROOT = '/home/user/Erdos-757/experiments/prover/L017/out'
t0 = time.time()
# ---- 1. candidate triples (own implementation of the constraints stated in 7.1)
stored = {}
pat = re.compile(r'cell_(\d+)_(\d+)_(\d+)_D(\d+)\.txt$')
for dp, dn, fn in os.walk(ROOT):
    for f in fn:
        mm = pat.match(f)
        if mm:
            n, m, t, D = map(int, mm.groups())
            stored.setdefault((n, m, t), []).append((D, os.path.join(dp, f)))
cands = []
for n in range(3, 28):
    for m in range(1, n + 1):
        if n > 3 and m > n - 2: continue        # P3 with S = V (n >= 2); n = 3 allows only m = 1 (E_1)
        if n == 3 and m != 1: continue
        if n > 2 * m + 1: continue              # connected linear 3-graph: n <= 2m + 1
        if n > 3 * m: continue                  # no isolated vertex
        for t in range(1, m + 1):
            if 3 * n + 2 * m - 11 * t < 0: continue      # I11 (L016, n <= 27)
            if 17 * t > 5 * n + 3 * m: continue          # Henning-Yeo
            A = CN * n + CM * m - CT * t
            if A >= 0: continue
            cands.append((n, m, t, A))
print('candidate triples with A<0, n<=27:', len(cands))
cells = []
for (n, m, t, A) in cands:
    lists = sorted(stored.get((n, m, t), []))
    d3 = [x for x in lists if x[0] >= 3]
    if n <= 24:
        assert d3, ('no D>=3 list for', n, m, t)
        cells.append((n, m, t, A, d3[0][1], d3[0][0]))
    else:
        print('  n>=25 candidate', (n, m, t), 'A', A, 'stored D>=3:', [os.path.relpath(p, ROOT) for D, p in d3], 'other:', [os.path.relpath(p, ROOT) for D, p in lists if D < 3])
print('candidate triples with n<=24:', len(cells))
# ---- 2. load, verify, closure in increasing n
cells.sort()
L = []            # pieces found so far
allres = []
total_graphs = 0; nonempty = 0; irr_total = 0; red_eq = 0; red_pos = 0
for (n, m, t, A, path, D) in cells:
    gs = parse_cell(path)
    gs = [g for g in gs if max(degrees(nverts(g), g)) <= 3]
    irr = []; red = 0; eq = 0; minP = None
    for gi, g in enumerate(gs):
        nn = nverts(g)
        assert nn == n and len(g) == m, (n, m, nn, len(g))
        assert is_linear(g) and is_connected(n, g), (n, m, t, gi)
        assert max(degrees(n, g)) <= 3
        assert not has_F7(g), ('F7 in', n, m, t, gi)
        tt = tau_sat(n, g)
        assert tt == t, (n, m, t, gi, tt)
        DEFp, fam, ncop = deficiency(n, g, L, proper=True)
        P = A + DEFp
        minP = P if minP is None else min(minP, P)
        if P < 0:
            irr.append(gi); L.append(Piece(g, f'({n},{m},{t})#{gi}'))
        else:
            red += 1
            if P == 0: eq += 1
    total_graphs += len(gs); irr_total += len(irr); red_eq += eq; red_pos += red - eq
    if gs: nonempty += 1
    allres.append(dict(cell=[n, m, t], A=A, graphs=len(gs), irreducible=len(irr), reducible=red, equality=eq, minP=minP, D=D))
    print(f'cell ({n},{m},{t}) A={A} D{D}: {len(gs)} graphs, irreducible {len(irr)} {irr}, reducible {red} (equality {eq}), min(A+DEFproper)={minP}  [{time.time()-t0:.0f}s]', flush=True)
print(f'TOTAL: {total_graphs} graphs in {nonempty} non-empty cells; irreducible {irr_total}; reducible with equality {red_eq}; reducible with P>0 {red_pos}')
# ---- 3. (L1) and weights for the pieces
bad = 0
for P in L:
    for x in range(P.n):
        if not sat_transversal(P.n, P.edges, P.tau, with_vertices=(x,)):
            bad += 1; print('L1 FAILS', P.name, 'vertex', x)
    s = 3 * P.n + 2 * P.m - 11 * P.tau
    J = 19 * P.n + 12 * P.m - 66 * P.tau
    assert P.W <= 11 * (P.n - P.m), P.name
print('L1 failures:', bad, '; weights:', sorted(set((p.name.split('#')[0], p.W) for p in L)), '; max W', max(p.W for p in L), '; I11 slacks', sorted(set((p.name.split('#')[0], 3*p.n+2*p.m-11*p.tau) for p in L)))
# ---- 4. compare with the prover's list
R = json.load(open('/home/user/Erdos-757/experiments/prover/L021/closure_results.json'))
prov = R['pieces']
print('prover pieces:', len(prov), 'mine:', len(L))
matched = 0
for p in prov:
    pe = [tuple(e) for e in p['edges']]; pn = nverts(pe)
    hit = [q for q in L if q.n == pn and q.m == len(pe) and hyper_iso(range(pn), pe, range(q.n), q.edges)]
    assert len(hit) == 1, (p['name'], len(hit))
    assert hit[0].W == p['W'] and hit[0].tau == p['tau']
    matched += 1
print('all prover pieces matched one-to-one by isomorphism:', matched == len(prov) == len(L))
json.dump(dict(cells=allres, pieces=[dict(name=p.name, n=p.n, m=p.m, tau=p.tau, W=p.W, edges=p.edges) for p in L]),
          open('/home/user/Erdos-757/experiments/referee/L021/closure_ref.json', 'w'), indent=0)
print('done', f'{time.time()-t0:.0f}s')
