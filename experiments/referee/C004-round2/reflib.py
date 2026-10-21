"""Independent referee tools for Erdos #757 constructions (round-2 referee of C004).

Deliberately self-contained: NO import of e757 or judge.  Only stdlib + python-sat + OR-tools.

Definitions used (and nothing else):
  * (4,5)-set: every 4 distinct points determine >= 5 distinct absolute differences.
  * S is Sidon iff all sums x + y with x <= y in S are distinct.
    Hence S fails to be Sidon iff S contains the union of two distinct pairs {i<=j}, {k<=l}
    with A[i]+A[j] = A[k]+A[l].  We call these unions "conflict sets" (size 3 or 4).
    S is Sidon  <=>  S contains no conflict set.  (Both directions are immediate.)
  * h(A) = max |S| over Sidon S subset of A = max "independent set" of the conflict set system.

Three exact methods for h, plus a literal brute force for small n:
  1. SAT: conflict clauses + cardinality constraint "at least k" (pysat CardEnc); k = h SAT with the
     model re-verified from the Sidon definition, k = h+1 UNSAT (two solvers, two encodings).
  2. CP-SAT (OR-tools) as an integer program, maximize sum x, status OPTIMAL means gap 0.
  3. Own branching solver on the set system (include/exclude a vertex, edge shrinking, forced
     exclusions, connected-component splitting, memoisation).  Exact for any set system.
  4. brute_h: literal enumeration of k-subsets (k descending from n), Sidon test from the definition.
"""
import itertools
import sys
import time
from collections import defaultdict
from fractions import Fraction


# ----------------------------------------------------------------------------- parsing
def parse_set(raw):
    vals = [Fraction(str(x)) for x in raw]
    if len(set(vals)) != len(vals):
        raise ValueError("repeated elements")
    return sorted(vals)


def as_ints(A):
    """Return python ints if every element is an integer Fraction, else raise."""
    out = []
    for x in A:
        if isinstance(x, Fraction):
            if x.denominator != 1:
                raise ValueError("non-integer element %s" % x)
            out.append(int(x.numerator))
        else:
            out.append(int(x))
    return out


# ----------------------------------------------------------------------------- (4,5) check
def check_45_literal(A):
    """All C(n,4) subsets, literally.  Returns (ok, n_subsets, min_distinct_diffs, worst_quadruple)."""
    A = sorted(A)
    n4 = 0
    mn = 7
    worst = None
    for q in itertools.combinations(A, 4):
        n4 += 1
        d = {abs(x - y) for x, y in itertools.combinations(q, 2)}
        if len(d) < mn:
            mn = len(d)
            worst = q
            if mn < 5:
                return False, n4, mn, worst
    return True, n4, mn, worst


# ----------------------------------------------------------------------------- conflict sets
def conflict_sets(A):
    """All unions of two distinct pairs (i<=j), (k<=l) with equal sums (indices into sorted A).
    Returns (set of frozensets, number_of_sum_coincidences, size histogram)."""
    n = len(A)
    by = defaultdict(list)
    for i in range(n):
        for j in range(i, n):
            by[A[i] + A[j]].append((i, j))
    confl = set()
    ncoinc = 0
    for s, ps in by.items():
        if len(ps) > 1:
            for p, q in itertools.combinations(ps, 2):
                ncoinc += 1
                confl.add(frozenset(p) | frozenset(q))
    hist = defaultdict(int)
    for F in confl:
        hist[len(F)] += 1
    return confl, ncoinc, dict(hist)


def is_sidon_def(S):
    sums = [x + y for x, y in itertools.combinations_with_replacement(sorted(S), 2)]
    return len(sums) == len(set(sums))


def is_weak_sidon_def(A):
    sums = [x + y for x, y in itertools.combinations(sorted(A), 2)]
    return len(sums) == len(set(sums))


# ----------------------------------------------------------------------------- method 1: SAT
def sat_atleast(n, confl, k, solver_name="cadical153", encoding="seqcounter"):
    """Is there a subset of size >= k containing no conflict set?  Returns (sat, chosen_indices_or_None, seconds)."""
    from pysat.card import CardEnc, EncType
    from pysat.solvers import Solver
    enc = getattr(EncType, encoding)
    lits = list(range(1, n + 1))
    t0 = time.time()
    card = CardEnc.atleast(lits=lits, bound=k, top_id=n, encoding=enc)
    clauses = [list(c) for c in card.clauses]
    for F in confl:
        clauses.append([-(i + 1) for i in sorted(F)])
    with Solver(name=solver_name, bootstrap_with=clauses) as s:
        r = s.solve()
        chosen = None
        if r:
            pos = {l for l in s.get_model() if l > 0}
            chosen = [i for i in range(n) if (i + 1) in pos]
    return bool(r), chosen, time.time() - t0


# ----------------------------------------------------------------------------- method 2: CP-SAT
def cpsat_max(n, confl, tlim=300.0, workers=1):
    from ortools.sat.python import cp_model
    m = cp_model.CpModel()
    x = [m.NewBoolVar("x%d" % i) for i in range(n)]
    for F in confl:
        m.Add(sum(x[i] for i in F) <= len(F) - 1)
    m.Maximize(sum(x))
    s = cp_model.CpSolver()
    s.parameters.max_time_in_seconds = float(tlim)
    s.parameters.num_workers = int(workers)
    t0 = time.time()
    r = s.Solve(m)
    status = s.StatusName(r)
    chosen = None
    obj = None
    bound = None
    if status in ("OPTIMAL", "FEASIBLE"):
        obj = int(round(s.ObjectiveValue()))
        bound = int(round(s.BestObjectiveBound()))
        chosen = [i for i in range(n) if s.Value(x[i])]
    return status, obj, bound, chosen, time.time() - t0


# ----------------------------------------------------------------------------- method 3: own branching solver
class Budget(Exception):
    pass


def alpha_setsystem(n, confl, time_cap=None):
    """Exact maximum size of a subset of range(n) containing no member of confl (a set of frozensets).

    solve(free, edges): free = undecided vertices (frozenset); edges = frozenset of frozensets, each a
    non-empty subset of free, meaning "not all of these may be chosen" (already-chosen vertices have been
    removed from the edges).  Returns the max number of vertices of `free` that can still be chosen.
    Steps: forced exclusions (size-1 edges), superset removal, isolated vertices, component split,
    branch on a max-degree vertex (exclude / include).  Memoised on (free, edges).  Exact by construction.
    """
    sys.setrecursionlimit(100000)
    memo = {}
    t0 = time.time()
    stats = {"calls": 0, "memo_hits": 0}

    def solve(free, edges):
        stats["calls"] += 1
        if time_cap is not None and time.time() - t0 > time_cap:
            raise Budget()
        # 1. forced exclusions
        changed = True
        while changed:
            changed = False
            forced = {next(iter(e)) for e in edges if len(e) == 1}
            if forced:
                free = free - forced
                edges = frozenset(e for e in edges if not (e & forced))
                changed = True
        if not edges:
            return len(free)
        # 2. superset removal (an edge containing another edge is redundant)
        es = sorted(edges, key=len)
        kept = []
        for e in es:
            if not any(f < e for f in kept):
                kept.append(e)
        edges = frozenset(kept)
        # 3. isolated vertices
        covered = frozenset().union(*edges)
        iso = len(free - covered)
        free = free & covered
        key = (free, edges)
        if key in memo:
            stats["memo_hits"] += 1
            return iso + memo[key]
        # 4. components
        parent = {v: v for v in free}

        def find(v):
            while parent[v] != v:
                parent[v] = parent[parent[v]]
                v = parent[v]
            return v

        for e in edges:
            it = iter(e)
            r0 = find(next(it))
            for v in it:
                parent[find(v)] = r0
        comps = defaultdict(set)
        for v in free:
            comps[find(v)].add(v)
        if len(comps) > 1:
            total = 0
            for cv in comps.values():
                cv = frozenset(cv)
                ce = frozenset(e for e in edges if e <= cv)
                total += solve(cv, ce)
            memo[key] = total
            return iso + total
        # 5. branch on a max-degree vertex
        deg = defaultdict(int)
        for e in edges:
            for v in e:
                deg[v] += 1
        v = max(free, key=lambda u: (deg[u], -u))
        # exclude v
        best = solve(free - {v}, frozenset(e for e in edges if v not in e))
        # include v
        ne = frozenset((e - {v}) if v in e else e for e in edges)
        inc = 1 + solve(free - {v}, ne)
        best = max(best, inc)
        memo[key] = best
        return iso + best

    res = solve(frozenset(range(n)), frozenset(confl))
    return res, stats, time.time() - t0


# ----------------------------------------------------------------------------- method 4: brute force
def brute_h(A, max_n=22):
    """Literal brute force from the Sidon definition.  Sidon is hereditary, so scanning k downward from n and
    stopping at the first k with a Sidon k-subset gives h(A); every (k+1)-subset was checked and failed."""
    A = sorted(A)
    n = len(A)
    if n > max_n:
        raise ValueError("too large for brute force")
    checked = 0
    for k in range(n, 0, -1):
        for S in itertools.combinations(A, k):
            checked += 1
            if is_sidon_def(S):
                return k, checked, S
    return 0, checked, ()


# ----------------------------------------------------------------------------- the reader's family (rebuilt from scratch)
O_READER = [0, 49, 75, 83, 98, 101, 117, 119, 121, 159, 269]


def reader_family_int(K):
    """I_K = 269^K * S_K, S_K = union_{j<=K} phi^j(O), phi(x) = 101 + 18x/269.  Exact Fractions, then ints."""
    pts = set()
    for j in range(K + 1):
        for x in O_READER:
            y = Fraction(x)
            for _ in range(j):
                y = 101 + Fraction(18, 269) * y
            pts.add(y * Fraction(269) ** K)
    return sorted(as_ints(sorted(pts)))
