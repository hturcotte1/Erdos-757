"""Route I by SAT (no enumerated lists used).
 case_i : connected linear 3-graph, n=13, m=8, tau>=5, F7-free -> expect UNSAT  (Step 5.1)
 case_ii: H on [14]: 7 edges inside {0..9} forming a connected 3-graph spanning {0..9}; the edge {10,11,12};
          exactly 3 edges {13,a,b} (a<b<=12); no other edges; H linear, F7-free, tau(H) >= 6 -> expect UNSAT (Step 5.2).
          Symmetry: d0 = max degree of C = H[{0..9}], vertex 0 has C-edges {0,1,2},...,{0,2d0-1,2d0}, all C-degrees <= d0
          (sound: every constraint is invariant under permutations of {0..9}).
 'nof7' variants drop F7-freeness (positive controls; must be SAT)."""
import itertools, sys, time, json
from pysat.formula import IDPool
from pysat.card import CardEnc, EncType
from pysat.solvers import Solver
from sat_ref import solve_cell, f7_copies, components
from f7_ref import det_A, is_linear
def tau(n, es):
    for k in range(n + 1):
        for S in itertools.combinations(range(n), k):
            s = set(S)
            if all(s & set(e) for e in es): return k
def case_ii(f7free, d0):
    n = 14; C = list(range(10))
    T = [e for e in itertools.combinations(range(n), 3)
         if set(e) <= set(C) or e == (10, 11, 12) or (13 in e)]
    pool = IDPool(); x = {e: pool.id(e) for e in T}; s = Solver(name='cadical153')
    TC = [e for e in T if set(e) <= set(C)]; T13 = [e for e in T if 13 in e]
    s.add_clause([x[(10, 11, 12)]])
    for cl in CardEnc.equals([x[e] for e in TC], 7, vpool=pool, encoding=EncType.seqcounter).clauses: s.add_clause(cl)
    for cl in CardEnc.equals([x[e] for e in T13], 3, vpool=pool, encoding=EncType.seqcounter).clauses: s.add_clause(cl)
    for a, b in itertools.combinations(range(n), 2):
        L = [x[e] for e in T if a in e and b in e]
        for i in range(len(L)):
            for j in range(i + 1, len(L)): s.add_clause([-L[i], -L[j]])
    for S in itertools.combinations(range(n), 5):
        Ss = set(S); s.add_clause([x[e] for e in T if not (Ss & set(e))])
    for v in C: s.add_clause([x[e] for e in TC if v in e])
    for mask in range(1, 1 << 10, 2):
        if mask == (1 << 10) - 1: continue
        s.add_clause([x[e] for e in TC if any(mask >> v & 1 for v in e) and not all(mask >> v & 1 for v in e)])
    fixed_true = [(0, 2 * i - 1, 2 * i) for i in range(1, d0 + 1)]; ff = set()
    for e in TC:
        if 0 in e:
            if e in fixed_true: s.add_clause([x[e]])
            else: s.add_clause([-x[e]]); ff.add(e)
    for v in C[1:]:
        L = [x[e] for e in TC if v in e]
        for cl in CardEnc.atmost(L, d0, vpool=pool, encoding=EncType.seqcounter).clauses: s.add_clause(cl)
    nf = 0
    if f7free:
        for cp in f7_copies(n):
            if all(e in x and e not in ff for e in cp):
                s.add_clause([-x[e] for e in cp]); nf += 1
    r = s.solve(); edges = None
    if r:
        mdl = set(l for l in s.get_model() if l > 0); edges = [e for e in T if x[e] in mdl]
    s.delete()
    return r, edges, nf
mode = sys.argv[1]; t0 = time.time()
if mode in ('case_i', 'case_i_nof7'):
    f7 = mode == 'case_i'
    # Delta >= ceil(24/13) = 2; the split d0 = 2 (Delta <= 2) is settled separately by dual_bf (8 nodes, 11 edges, nu <= 3)
    r, e, info = solve_cell(13, 8, 5, f7free=f7, conn='eager', verbose=True, d0s=[3, 4, 5, 6])
    extra = {}
    if e: extra = dict(tau=tau(13, e), hasF7=det_A(e), linear=is_linear(e), comps=len(components(13, e)))
    print(mode.upper(), r, e, extra, round(time.time() - t0, 1), 's', json.dumps(info), flush=True)
else:
    f7 = mode == 'case_ii'
    for d0 in (3, 4):   # Delta(C) >= ceil(21/10) = 3 and 2*d0+1 <= 10
        t1 = time.time(); r, e, nf = case_ii(f7, d0)
        extra = {}
        if e:
            Ce = [q for q in e if max(q) <= 9]
            extra = dict(tau=tau(14, e), hasF7=det_A(e), linear=is_linear(e), C_edges=len(Ce), C_comps=len(components(10, Ce)),
                         deg13=sum(13 in q for q in e), m=len(e))
        print(mode.upper(), 'd0=%d' % d0, 'SAT' if r else 'UNSAT', e, extra, 'f7_clauses=%d' % nf, round(time.time() - t1, 1), 's', flush=True)
        if r and not f7: break
