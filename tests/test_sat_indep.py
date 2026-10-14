"""Tests of e757.sat_indep (independent pysat encoding of class O').

The clause-family checker and the brute-force enumerator below are written separately from the module
(directly from the definitions in its docstring) and use only the standard library + json.
"""
import functools
import itertools
import json
import os
import re
import sys

import pytest

from e757.sat_indep import decide, enumerate_all

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")


# ------------------------------------------------------------------------------------------
# independent checker of each clause family
# ------------------------------------------------------------------------------------------
def _load_cores():
    cores = []
    for f in ("forbidden_ordered_n7.json", "forbidden_ordered_n8.json"):
        for c in json.load(open(os.path.join(ROOT, "data", f)))["cores"]:
            v = c["n"]
            e = sorted(tuple(x) for x in c["edges"])
            cores.append((v, e))
            cores.append((v, sorted((v - 1 - k, v - 1 - j, v - 1 - i) for i, j, k in e)))
    return cores


CORES = _load_cores()


def chk_a(E):
    mids = [j for (_, j, _) in E]
    return len(mids) == len(set(mids))


def chk_b(E):
    for e, f in itertools.combinations(E, 2):
        if len(set(e) & set(f)) >= 2:
            return False
    return True


def chk_d(E):
    for (i, j, k) in E:
        for (i2, j2, k2) in E:
            if i <= i2 and k <= k2 and (i, k) != (i2, k2) and not j < j2:
                return False
    return True


def chk_e(E):
    S = set(E)
    for (a, b, c) in E:
        for (a2, p, e) in E:
            if a2 == a and e > c:  # edge (a,p,e) with e > c
                for (c2, q, e2) in E:
                    if c2 == c and e2 == e:
                        return False
    return True


def chk_f7(E):
    """F7-free via the structure of F7: three lines through a point 0 (covering six points in pairs
    {1,2},{3,4},{5,6}) plus two lines {1,3,5},{2,4,6}, i.e. two 'complementary transversals'."""
    S = set(E)
    byv = {}
    for e in E:
        for v in e:
            byv.setdefault(v, []).append(e)
    for v, es in byv.items():
        for tri in itertools.combinations(es, 3):
            pairs = [tuple(x for x in e if x != v) for e in tri]
            pts = set(itertools.chain(*pairs))
            if len(pts) != 6:
                continue
            for pick in itertools.product(*[(0, 1)] * 3):
                t1 = tuple(sorted(pairs[x][pick[x]] for x in range(3)))
                t2 = tuple(sorted(pairs[x][1 - pick[x]] for x in range(3)))
                if t1 in S and t2 in S:
                    return False
    return True


@functools.lru_cache(maxsize=None)
def _core_masks(n):
    """Bitmasks (over the lexicographic list of triples) of all images of all cores under increasing maps."""
    idx = {t: x for x, t in enumerate(itertools.combinations(range(n), 3))}
    masks = set()
    for v, ce in CORES:
        if v > n:
            continue
        for sub in itertools.combinations(range(n), v):
            mk = 0
            for (a, b, c) in ce:
                mk |= 1 << idx[(sub[a], sub[b], sub[c])]
            masks.add(mk)
    return sorted(masks)


def chk_f(E, n):
    idx = {t: x for x, t in enumerate(itertools.combinations(range(n), 3))}
    lm = 0
    for t in E:
        lm |= 1 << idx[tuple(t)]
    return not any(mk & lm == mk for mk in _core_masks(n))


def chk_alpha(E, n, T):
    em = [(1 << a) | (1 << b) | (1 << c) for (a, b, c) in E]
    for S in itertools.combinations(range(n), T + 1):
        sm = 0
        for v in S:
            sm |= 1 << v
        if not any(x & sm == x for x in em):
            return False
    return True


def chk_all(E, n, T=None, cores=True):
    E = sorted(tuple(e) for e in E)
    ok = chk_a(E) and chk_b(E) and chk_d(E) and chk_e(E) and chk_f7(E)
    if ok and cores:
        ok = chk_f(E, n)
    if ok and T is not None:
        ok = chk_alpha(E, n, T)
    return ok


# ------------------------------------------------------------------------------------------
# brute-force enumerator: plain recursion over the interior vertices
# ------------------------------------------------------------------------------------------
def brute(n, T):
    """dict m -> set of edge-sets (sorted tuples) with alpha <= T in the class (all families)."""
    out = {}

    def partial_ok(E, new):
        i, j, k = new
        for (i2, j2, k2) in E:
            if len(set(new) & {i2, j2, k2}) >= 2:
                return False
            for (a, b, c), (a2, b2, c2) in (((i, j, k), (i2, j2, k2)), ((i2, j2, k2), (i, j, k))):
                if a <= a2 and c <= c2 and (a, c) != (a2, c2) and not b < b2:
                    return False
        return True

    def rec(j, E):
        if j == n - 1:
            Es = sorted(E)
            if chk_alpha(Es, n, T) and chk_e(Es) and chk_f7(Es) and chk_f(Es, n):
                out.setdefault(len(Es), set()).add(tuple(Es))
            return
        rec(j + 1, E)
        for i in range(j):
            for k in range(j + 1, n):
                if partial_ok(E, (i, j, k)):
                    rec(j + 1, E + [(i, j, k)])

    rec(1, [])
    return out


# ------------------------------------------------------------------------------------------
def _table_cc():
    txt = open(os.path.join(ROOT, "experiments/20261013-2257-chyp-table/table.md")).read()
    res = {}
    for line in txt.splitlines():
        mm = re.match(r"\|\s*(\d+)\s*\|\s*(\d+)\s*\|", line)
        if mm:
            res[int(mm.group(1))] = int(mm.group(2))
    return res


def min_alpha(n):
    T = n
    while True:
        st, r = decide(n, T - 1, None)
        if st == "UNSAT":
            return T
        assert st == "SAT"
        assert chk_all(r, n, T - 1)
        T -= 1


def test_min_alpha_matches_table():
    tab = _table_cc()
    assert set(range(5, 13)) <= set(tab)
    for n in range(5, 12):
        assert min_alpha(n) == tab[n], n


@pytest.mark.parametrize("n", [8, 9])
def test_full_solution_lists_agree_with_bruteforce(n):
    T = _table_cc()[n]
    ref = brute(n, T)
    assert ref, "brute force found nothing"
    # n=9 has ~116k solutions in total (m=5: 63444, m=6: 44642); by default only the cheaper m are
    # compared, E757_SLOW=1 compares every m (done once for the experiment README: all agree).
    ms = range(0, n - 1)
    if n == 9 and not os.environ.get("E757_SLOW"):
        ms = [0, 1, 2, 3, 4, 7]
    for m in ms:
        got = enumerate_all(n, T, m, cores="hybrid" if n == 8 else "eager")
        assert len(got) == len(set(got))
        assert set(got) == ref.get(m, set()), (n, m)
        for E in got:
            assert chk_all(E, n, T)
    # m outside 0..n-2 is impossible (midpoints are injective and interior)
    assert enumerate_all(n, T, n - 1) == []


def test_core_modes_agree_n8():
    T = 5
    for m in (4, 6):
        a = set(enumerate_all(8, T, m, cores="eager"))
        b = set(enumerate_all(8, T, m, cores="lazy"))
        c = set(enumerate_all(8, T, m, cores="hybrid", eager_max_v=6))
        assert a == b == c
    # without cores the 8-vertex cores matter (there exist solutions only killed by a core)
    nocore = set(enumerate_all(8, T, 6, cores="none"))
    assert set(enumerate_all(8, T, 6, cores="eager")) < nocore


def test_vertex1_case_split_partitions():
    n, T, m = 9, 6, 3
    allsol = set(enumerate_all(n, T, m, cores="eager"))
    parts = []
    for v1 in [0] + list(range(2, n)):
        sol = set(enumerate_all(n, T, m, vertex1=v1, cores="eager"))
        for E in sol:
            if v1 == 0:
                assert all(e[1] != 1 for e in E)
            else:
                assert (0, 1, v1) in E
        parts.append(sol)
    assert sum(len(p) for p in parts) == len(allsol)
    assert set().union(*parts) == allsol


def test_negative_controls():
    # alpha > T pattern, F7 pattern, K30 violation, core violation must all be UNSAT as full assignments
    n = 8
    def fixed(E, n):
        S = set(E)
        return [(t, t in S) for t in itertools.combinations(range(n), 3)]
    # K30 violation: (0,1,5) and (0,2,6) fine; (0,3,5) and (0,2,6): i<=i', k<=k', j=3>=2
    E = [(0, 3, 5), (0, 2, 6)]
    assert not chk_d(E)
    assert decide(n, n, len(E), extra_unit=fixed(E, n))[0] == "UNSAT"
    # alpha violation
    E = [(0, 1, 2)]
    assert decide(n, 5, 1, extra_unit=fixed(E, n))[0] == "UNSAT"
    assert decide(n, 7, 1, extra_unit=fixed(E, n))[0] == "SAT"
    # linear violation
    E = [(0, 1, 2), (0, 1, 3)]
    assert decide(n, n, 2, extra_unit=fixed(E, n))[0] == "UNSAT"
    # shared midpoint
    E = [(0, 2, 3), (1, 2, 4)]
    assert decide(n, n, 2, extra_unit=fixed(E, n))[0] == "UNSAT"
    # medial triangle (0,1,2),(0,3,4),(2,... : a=0,b=1,c=2,p=3,e=5,q=4)
    E = [(0, 1, 2), (0, 3, 5), (2, 4, 5)]
    assert not chk_e(E)
    assert decide(n, n, 3, extra_unit=fixed(E, n))[0] == "UNSAT"
    # an F7 copy that passes (a),(b),(d),(e): lazy F7 clause is the only reason for UNSAT
    found = None
    base = [(0, 1, 2), (0, 3, 4), (0, 5, 6), (1, 3, 5), (2, 4, 6)]
    for perm in itertools.permutations(range(7)):
        E = sorted(tuple(sorted(perm[x] for x in e)) for e in base)
        if chk_a(E) and chk_b(E) and chk_d(E) and chk_e(E) and chk_f(E, 7):
            found = E
            break
    if found is not None:  # F7 is not realizable, but may pass the cheap order clauses
        assert not chk_f7(found)
        assert decide(7, 7, 5, extra_unit=fixed(found, 7))[0] == "UNSAT"
        assert decide(7, 7, 5, extra_unit=fixed(found, 7), forbid_f7=False)[0] == "SAT"


def test_record_patterns_satisfy_all_clauses():
    from e757.saturated import map_of_set
    recs = json.load(open(os.path.join(ROOT, "data", "small_records.json")))["sets"]
    items = []
    for key, v in recs.items():
        if isinstance(v, dict) and "set" in v:
            items.append((key, v))
        elif isinstance(v, list):
            items.extend((key, x) for x in v)
    assert len(items) == 7, len(items)
    for key, rec in items:
        A = sorted(rec["set"])
        n, h = len(A), rec["h"]
        lo, hi, mid = map_of_set(A)
        E = sorted((i, j, k) for j, (i, k) in mid.items())
        assert len(E) == rec["m"]
        assert chk_all(E, n, h), (key, "checker")
        S = set(E)
        units = [(t, t in S) for t in itertools.combinations(range(n), 3)]
        st, _ = decide(n, h, len(E), extra_unit=units)
        assert st == "SAT", (key, "solver")
        # and the same pattern is UNSAT for alpha <= h-1 (these sets are extremal for their size)
        st2, _ = decide(n, h - 1, len(E), extra_unit=units)
        assert st2 == "UNSAT", (key, "alpha<=h-1")


def _pattern_generator(nmax):
    src = open(os.path.join(ROOT, "experiments/20261013-2257-forbidden-library/enumerate.py")).read()
    src = src.split("def main():")[0]
    old = sys.argv
    sys.argv = ["x", str(nmax), os.devnull]
    try:
        ns = {}
        exec(compile(src, "enumerate.py", "exec"), ns)
    finally:
        sys.argv = old
    return ns["patterns"]


@pytest.mark.parametrize("n", [3, 4, 5, 6, 7])
def test_census_realizable_patterns_satisfy_clauses(n):
    from e757.realizability import realize_exact
    patterns = _pattern_generator(7)
    real_total = 0
    passing = 0
    for E in patterns(n):
        E = list(E)
        ok = realize_exact(n, E)[0]
        cheap = chk_all(E, n, None)
        if ok:
            real_total += 1
            assert cheap, (n, E, "realizable pattern rejected by checker")
            units = [(t, t in set(E)) for t in itertools.combinations(range(n), 3)]
            assert decide(n, n, len(E), extra_unit=units)[0] == "SAT", (n, E)
        passing += cheap
    # cores are complete up to 7 vertices, so the class O' coincides with the realizable patterns here
    assert passing == real_total, (n, passing, real_total)
