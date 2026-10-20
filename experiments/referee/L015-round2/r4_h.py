#!/usr/bin/env python3
"""h(S_K) by two exact methods, both starting from the Sidon DEFINITION on the integer set I_K
(no AP list, no copies, no transfer matrix):
  constraints = for every two distinct pairs {a<=b} != {c<=d} with a+b = c+d, the set {a,b,c,d} must not
  be fully chosen.  T is Sidon iff it violates no constraint.
(1) SAT (pysat, CaDiCaL 1.9.5 and Glucose 4 as a second solver) with a cardinality constraint:
    'at least 7+5K' must be SAT (model re-checked Sidon by definition) and 'at least 8+5K' UNSAT.
(2) a generic frontier DP (vertex elimination): exact for ANY vertex order; the order is a maximum
    cardinality search on the primal graph of the constraint hypergraph (ties: smaller frontier, index).
Usage: python3 r4_h.py SATmaxK DPmaxK
"""
import sys, time
sys.path.insert(0, ".")
from r2_family import build
from collections import defaultdict

def constraints_from_definition(I):
    by_sum = defaultdict(list)
    n = len(I)
    for i in range(n):
        for j in range(i, n):
            by_sum[I[i] + I[j]].append((i, j))
    cons = set()
    for s, prs in by_sum.items():
        for x in range(len(prs)):
            for y in range(x + 1, len(prs)):
                cons.add(frozenset(prs[x]) | frozenset(prs[y]))
    return sorted(tuple(sorted(c)) for c in cons)

def is_sidon(T):
    T = sorted(T)
    seen = set()
    for i in range(len(T)):
        for j in range(i, len(T)):
            s = T[i] + T[j]
            if s in seen:
                return False
            seen.add(s)
    return True

def sat_h(I, cons, t, solver):
    from pysat.formula import CNF
    from pysat.card import CardEnc, EncType
    from pysat.solvers import Solver
    n = len(I)
    cnf = CNF()
    for c in cons:
        cnf.append([-(v + 1) for v in c])
    card = CardEnc.atleast(lits=list(range(1, n + 1)), bound=t, top_id=n, encoding=EncType.seqcounter)
    cnf.extend(card.clauses)
    with Solver(name=solver, bootstrap_with=cnf.clauses) as s:
        res = s.solve()
        model = s.get_model() if res else None
    if res:
        T = [I[v] for v in range(n) if model[v] > 0]
        return True, T
    return False, None

def frontier_dp(n, cons):
    inc = [[] for _ in range(n)]
    for k, c in enumerate(cons):
        for v in c:
            inc[v].append(k)
    processed = [False] * n
    remaining_unproc = [len(c) for c in cons]   # number of unprocessed vertices per constraint
    # frontier = processed vertices lying in a constraint with an unprocessed vertex
    def frontier_after(v):
        # frontier if v were processed next
        fr = set()
        for u in range(n):
            if processed[u] or u == v:
                for k in inc[u]:
                    left = remaining_unproc[k] - (1 if v in cons[k] else 0)
                    if left > 0:
                        fr.add(u)
                        break
        return fr
    nbr = [set() for _ in range(n)]
    for c in cons:
        for a in c:
            for b in c:
                if a != b:
                    nbr[a].add(b)
    pn = [0] * n          # number of processed primal neighbours
    order = []
    states = {0: 0}           # bitmask over vertex indices (chosen frontier vertices) -> best count
    maxw = 0
    maxstates = 1
    for step in range(n):
        # maximum cardinality search: most processed primal neighbours first; ties: smaller frontier, smaller index
        best_v, best_fr, best_key = None, None, None
        for v in range(n):
            if processed[v]:
                continue
            fr = frontier_after(v)
            key = (-pn[v], len(fr), v)
            if best_key is None or key < best_key:
                best_v, best_fr, best_key = v, fr, key
        v = best_v
        for u in nbr[v]:
            pn[u] += 1
        # constraints closed by v: all other vertices processed
        closing = [cons[k] for k in inc[v] if remaining_unproc[k] == 1]
        closing_masks = [sum(1 << u for u in c if u != v) for c in closing]
        frmask = sum(1 << u for u in best_fr)
        new = {}
        for key, cnt in states.items():
            k0 = key & frmask
            if new.get(k0, -1) < cnt:
                new[k0] = cnt
            if all((key & cm) != cm for cm in closing_masks):
                k1 = (key | (1 << v)) & frmask
                if new.get(k1, -1) < cnt + 1:
                    new[k1] = cnt + 1
        states = new
        processed[v] = True
        for k in inc[v]:
            remaining_unproc[k] -= 1
        order.append(v)
        maxw = max(maxw, len(best_fr))
        maxstates = max(maxstates, len(states))
    assert all(x == 0 for x in remaining_unproc)
    return max(states.values()), maxw, maxstates

def main(satK, dpK):
    allok = True
    for K in range(0, max(satK, dpK) + 1):
        copies, S, I = build(K)
        n = len(I)
        cons = constraints_from_definition(I)
        line = "K=%d n=%d constraints=%d (sizes %s)" % (K, n, len(cons), sorted(set(len(c) for c in cons)))
        h = 7 + 5 * K
        if K <= dpK:
            t0 = time.time()
            val, w, ms = frontier_dp(n, cons)
            ok = val == h
            allok &= ok
            line += " | DP h=%d (max frontier %d, max states %d, %.1fs) %s" % (val, w, ms, time.time() - t0, "OK" if ok else "FAIL")
        if K <= satK:
            for solver in ("cadical195", "glucose4"):
                t0 = time.time()
                r1, T = sat_h(I, cons, h, solver)
                r2, _ = sat_h(I, cons, h + 1, solver)
                ok = r1 and (not r2) and is_sidon(T) and len(T) >= h and set(T) <= set(I)
                allok &= ok
                line += " | %s: >=%d %s (model Sidon=%s, |T|=%d), >=%d %s (%.1fs) %s" % (
                    solver, h, "SAT" if r1 else "UNSAT", is_sidon(T) if T else None, len(T) if T else -1,
                    h + 1, "SAT" if r2 else "UNSAT", time.time() - t0, "OK" if ok else "FAIL")
        print(line, flush=True)
    print("ALL R4 h CHECKS OK" if allok else "R4 FAILED")

if __name__ == "__main__":
    main(int(sys.argv[1]), int(sys.argv[2]))
