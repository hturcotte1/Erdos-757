"""Referee L007 r2: SAT decision of cells of connected linear 3-graphs (no canonical labelling).
Instance (n, m, t, D, f7free): does a 3-graph on vertex set [n] exist that is linear, connected and spans [n],
has exactly m edges, tau >= t, max degree <= D (optional) and (optionally) contains no F7?
Encoding (one Boolean x_e per triple e of [n]):
  linear      : at most one triple through each pair (pairwise AMO)
  edges       : exactly m triples (sequential counter)
  tau >= t    : for every (t-1)-subset S of [n], some chosen triple is disjoint from S
  spanning    : every vertex lies in a chosen triple
  connected   : lazy cut clauses (for a model with components C1..Ck, k>1, add for each Ci the clause
                'some chosen triple meets Ci and its complement'); every connected graph satisfies all of them
  F7-free     : one clause per copy of F7 in K_n^(3) (all copies, generated from the definition: centre p,
                three pairs, two complementary transversals); copies containing a triple fixed false are skipped
  symmetry    : split on d0 = max degree (d0 = 1..floor((n-1)/2), d0 <= D); vertex 0 has degree d0 with edges
                {0,1,2},{0,3,4},...,{0,2d0-1,2d0}; every vertex has degree <= d0.
                Sound: take a max-degree vertex v; by linearity its d0 edges meet only in v; relabel.
UNSAT for every d0 <=> no such graph."""
import itertools, sys, time, json
from pysat.formula import IDPool
from pysat.card import CardEnc, EncType
from pysat.solvers import Solver

def f7_copies(n, allowed=None):
    """All copies of F7 in the complete 3-graph on [n] (as frozensets of 5 sorted triples)."""
    out = []
    V = range(n)
    for p in V:
        others = [v for v in V if v != p]
        for pairs in itertools.combinations(itertools.combinations(others, 2), 3):
            s = set(pairs[0]) | set(pairs[1]) | set(pairs[2])
            if len(s) != 6: continue
            if not (pairs[0] < pairs[1] < pairs[2]): continue
            E = [tuple(sorted((p,) + q)) for q in pairs]
            a0, a1 = pairs[0]
            for c2 in (0, 1):
                for c3 in (0, 1):
                    T1 = tuple(sorted((a0, pairs[1][c2], pairs[2][c3])))
                    T2 = tuple(sorted((a1, pairs[1][1 - c2], pairs[2][1 - c3])))
                    out.append(frozenset(E + [T1, T2]))
    return out

def components(n, edges):
    par = list(range(n))
    def f(a):
        while par[a] != a:
            par[a] = par[par[a]]; a = par[a]
        return a
    for e in edges:
        for v in e[1:]:
            par[f(v)] = f(e[0])
    comp = {}
    for v in range(n): comp.setdefault(f(v), set()).add(v)
    return list(comp.values())

def solve_cell(n, m, t, D=None, f7free=False, d0s=None, solver='cadical153', verbose=False, extra=None,
               allowed=None, conn_vertices=None, sb=True, timeout_note='', conn='lazy'):
    """Returns ('UNSAT', info) if no graph exists, else ('SAT', edges)."""
    T = [e for e in itertools.combinations(range(n), 3) if (allowed is None or allowed(e))]
    if d0s is None:
        hi = (n - 1) // 2
        if D is not None: hi = min(hi, D)
        d0s = list(range(1, hi + 1)) if sb else [None]
    F7 = f7_copies(n) if f7free else []
    info = dict(n=n, m=m, t=t, D=D, f7free=f7free, per_d0={})
    for d0 in d0s:
        t0 = time.time()
        pool = IDPool(); x = {e: pool.id(('x', e)) for e in T}
        s = Solver(name=solver)
        fixed_false = set()
        if d0 is not None:
            fixed_true = [(0, 2 * i - 1, 2 * i) for i in range(1, d0 + 1)]
            if any(e not in x for e in fixed_true):
                info['per_d0'][d0] = 'skip(not allowed)'; continue
            for e in T:
                if 0 in e:
                    if e in fixed_true: s.add_clause([x[e]])
                    else: s.add_clause([-x[e]]); fixed_false.add(e)
            for v in range(1, n):
                lits = [x[e] for e in T if v in e]
                if len(lits) > d0:
                    for c in CardEnc.atmost(lits, d0, vpool=pool, encoding=EncType.seqcounter).clauses: s.add_clause(c)
        if D is not None:
            for v in range(n):
                lits = [x[e] for e in T if v in e]
                if len(lits) > D:
                    for c in CardEnc.atmost(lits, D, vpool=pool, encoding=EncType.seqcounter).clauses: s.add_clause(c)
        # linear
        for a, b in itertools.combinations(range(n), 2):
            lits = [x[e] for e in T if a in e and b in e]
            for i in range(len(lits)):
                for j in range(i + 1, len(lits)): s.add_clause([-lits[i], -lits[j]])
        # exactly m edges
        if m > len(T):
            s.add_clause([pool.id('false_lit')]); s.add_clause([-pool.id('false_lit')])
        else:
            for c in CardEnc.equals([x[e] for e in T], m, vpool=pool, encoding=EncType.seqcounter).clauses: s.add_clause(c)
        # tau >= t
        if t >= 1:
            for S in itertools.combinations(range(n), t - 1):
                Ss = set(S)
                s.add_clause([x[e] for e in T if not (Ss & set(e))])
        # spanning
        cv = range(n) if conn_vertices is None else conn_vertices
        for v in range(n):
            s.add_clause([x[e] for e in T if v in e])
        # F7
        nf7 = 0
        for cp in F7:
            if any(e not in x or e in fixed_false for e in cp): continue
            s.add_clause([-x[e] for e in cp]); nf7 += 1
        if conn == 'eager':
            # one clause per vertex set S with 0 in S, S != [n]: some chosen triple meets S and its complement
            for mask in range(1, 1 << n, 2):
                if mask == (1 << n) - 1: continue
                s.add_clause([x[e] for e in T if any(mask >> v & 1 for v in e) and not all(mask >> v & 1 for v in e)])
        if extra: extra(s, x, pool, T)
        iters = 0; cuts = 0
        while True:
            iters += 1
            if not s.solve():
                res = 'UNSAT'; break
            model = set(l for l in s.get_model() if l > 0)
            edges = [e for e in T if x[e] in model]
            comps = components(n, edges)
            if len(comps) == 1:
                res = 'SAT'; break
            for C in comps:
                cl = [x[e] for e in T if (set(e) & C) and not set(e) <= C]
                s.add_clause(cl); cuts += 1
        s.delete()
        info['per_d0'][d0] = dict(result=res, iters=iters, cuts=cuts, f7_clauses=nf7, secs=round(time.time() - t0, 2))
        if verbose: print(n, m, t, D, f7free, 'd0=', d0, info['per_d0'][d0], flush=True)
        if res == 'SAT':
            return 'SAT', edges, info
    return 'UNSAT', None, info

if __name__ == '__main__':
    a = sys.argv[1:]
    n, m, t = map(int, a[:3]); D = int(a[3]) if len(a) > 3 and a[3] != '-' else None
    f7 = len(a) > 4 and a[4] == 'f7free'
    r, edges, info = solve_cell(n, m, t, D, f7, verbose=True)
    print('RESULT', r, edges, json.dumps(info))
