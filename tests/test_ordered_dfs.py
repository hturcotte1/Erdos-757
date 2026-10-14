"""Tests for the independent ordered-midpoint DFS (e757/ordered_dfs.py + e757/c/ordered_dfs.c).

Checks:
  * class definition: the DFS's staircase test equals the literal conditions (a),(b),(c) (brute force, n<=7);
  * min alpha for n=5..12 equals the CP-SAT table (experiments/20261013-2257-chyp-table);
  * pruning soundness: pruned enumeration == unpruned enumeration filtered by alpha, n<=9;
  * monotone rule (c) never prunes an order-feasible pattern (exact order_feasible), n<=8;
  * own independence routine and F7 detector vs brute force / e757.saturated;
  * C port agrees with Python (solution sets for n<=9, counts for n<=10), incl. flags.
"""
import itertools
import json
import os
import random
import subprocess
import sys

import pytest

from e757.ordered_dfs import (enumerate_solutions, exists, has_f7, hy_m_need, independence_number,
                              min_alpha, reflect_edges)
from e757.realizability import order_feasible
from e757.saturated import alpha_of_edges

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CBIN = os.path.join(ROOT, "e757", "c", "ordered_dfs")
TABLE = os.path.join(ROOT, "experiments", "20261013-2257-chyp-table", "results")


def _c_available():
    if not os.path.exists(CBIN):
        try:
            subprocess.run(["bash", os.path.join(ROOT, "e757", "c", "build.sh")], check=True,
                           capture_output=True, timeout=120)
        except Exception:  # noqa: BLE001
            return False
    return os.path.exists(CBIN)


def run_c(**kw):
    """Run the C binary; returns (list of (alpha, edges), stats dict)."""
    args = [CBIN] + ["%s=%s" % (k, int(v) if isinstance(v, bool) else v) for k, v in kw.items()]
    out = subprocess.run(args, capture_output=True, text=True, timeout=600, check=True).stdout
    sols, stats = [], {}
    for line in out.splitlines():
        if line.startswith("SOL"):
            parts = line.split()
            sols.append((int(parts[1]), tuple(tuple(int(x) for x in p.split(",")) for p in parts[2:])))
        elif line.startswith("DONE"):
            stats = dict(kv.split("=") for kv in line.split()[1:])
    return sols, stats


def all_patterns(n, **kw):
    out = []
    enumerate_solutions(n, n, callback=lambda e, a: out.append(tuple(e)), **kw)
    return out


# ----------------------------------------------------------------------------- class definition
def literal_class(n):
    """All choice vectors satisfying (a),(b),(c) checked literally (no staircase)."""
    opts = []
    for j in range(1, n - 1):
        opts.append([None] + [(i, j, k) for i in range(j) for k in range(j + 1, n)])
    res = set()
    for choice in itertools.product(*opts):
        es = [e for e in choice if e is not None]
        sets = [frozenset(e) for e in es]
        if any(len(a & b) > 1 for a, b in itertools.combinations(sets, 2)):
            continue
        ok = True
        for (i, j, k), (i2, j2, k2) in itertools.permutations(es, 2):
            if i <= i2 and k <= k2 and (i, k) != (i2, k2) and not j < j2:
                ok = False
                break
        if ok:
            res.add(tuple(sorted(es)))
    return res


@pytest.mark.parametrize("n", [4, 5, 6, 7])
def test_staircase_equals_literal_conditions(n):
    mine = all_patterns(n)
    assert len(mine) == len(set(mine))
    assert set(mine) == literal_class(n)


# ----------------------------------------------------------------------------- table values
def _table(n):
    p = os.path.join(TABLE, "table_n%d.json" % n)
    if not os.path.exists(p):
        pytest.skip("table missing")
    d = json.load(open(p))
    return d["f7"]["alpha"], d["nof7"]["alpha"]


@pytest.mark.parametrize("n", [5, 6, 7, 8, 9])
def test_min_alpha_python_matches_cpsat_table(n):
    t_f7, t_nof7 = _table(n)
    a, e, st = min_alpha(n, forbid_f7=True)
    assert a == t_f7 and independence_number(n, e) == a and alpha_of_edges(n, e) == a
    assert not has_f7(e)
    a2, e2, _ = min_alpha(n, forbid_f7=False)
    assert a2 == t_nof7 and alpha_of_edges(n, e2) == a2


@pytest.mark.parametrize("n", list(range(5, 13)))
def test_min_alpha_C_matches_cpsat_table(n):
    if not _c_available():
        pytest.skip("no C compiler")
    t_f7, t_nof7 = _table(n)
    for f7, want in ((1, t_f7), (0, t_nof7)):
        sols, st = run_c(n=n, mode="min", f7=f7, progress=0)
        assert st["timed_out"] == "0"
        a, e = sols[-1]
        assert a == want, (n, f7, a, want)
        assert alpha_of_edges(n, list(e)) == a


# ----------------------------------------------------------------------------- soundness of pruning
@pytest.mark.parametrize("n", [6, 7, 8, 9])
def test_pruned_equals_unpruned_filtered(n):
    for f7 in (False, True):
        full = all_patterns(n, forbid_f7=f7)
        alphas = {e: independence_number(n, e) for e in full}
        for T in sorted(set(alphas.values()))[:3] + [max(alphas.values()) - 1]:
            for m_min in (0, n - 4):
                got = []
                enumerate_solutions(n, T, m_min=m_min, forbid_f7=f7,
                                    callback=lambda e, a: got.append(tuple(e)))
                want = {e for e in full if alphas[e] <= T and len(e) >= m_min}
                assert set(got) == want and len(got) == len(want)
                got2 = []
                enumerate_solutions(n, T, m_min=m_min, forbid_f7=f7, refine=False,
                                    callback=lambda e, a: got2.append(tuple(e)))
                assert set(got2) == want
                if m_min:
                    got3 = []
                    enumerate_solutions(n, T, m_exact=m_min, forbid_f7=f7,
                                        callback=lambda e, a: got3.append(tuple(e)))
                    assert set(got3) == {e for e in want if len(e) == m_min}


def test_hy_option_is_consistent():
    # hy_m_need(16, 9) = 13, matching START_HERE section 4
    assert [hy_m_need(16, 9), hy_m_need(18, 10), hy_m_need(20, 11), hy_m_need(22, 12)] == [13, 16, 18, 20]
    n, T = 9, 6
    a = []
    enumerate_solutions(n, T, forbid_f7=True, callback=lambda e, al: a.append(tuple(e)))
    b = []
    enumerate_solutions(n, T, forbid_f7=True, use_hy=True, callback=lambda e, al: b.append(tuple(e)))
    assert set(a) == set(b)  # HY is a theorem; it must not remove any F7-free solution


def test_reflection_filter_gives_one_per_orbit():
    n, T = 9, 6
    allsol = []
    enumerate_solutions(n, T, callback=lambda e, a: allsol.append(tuple(e)))
    half = []
    enumerate_solutions(n, T, up_to_reflection=True, callback=lambda e, a: half.append(tuple(e)))
    orbits = {min(e, tuple(reflect_edges(n, e))) for e in allsol}
    assert len(half) == len(orbits)
    assert {min(e, tuple(reflect_edges(n, e))) for e in half} == orbits
    # the class is closed under reflection
    s = set(allsol)
    assert all(tuple(reflect_edges(n, e)) in s for e in s)


# ----------------------------------------------------------------------------- monotone rule (c)
def _feasible_filter():
    cache = {}

    def feas(n, edges):
        key = (n, tuple(sorted(edges)))
        if key not in cache:
            ok, _ = order_feasible(n, list(key[1]))
            assert ok is not None
            cache[key] = ok
        return cache[key]
    return feas


@pytest.mark.parametrize("n", [5, 6, 7, 8])
def test_monotone_rule_never_prunes_order_feasible_patterns(n):
    feas = _feasible_filter()
    # with (c): all patterns, then keep order-feasible ones
    with_c = [e for e in all_patterns(n) if feas(n, e)]
    # without (c): node-level exact order-feasibility pruning (infeasibility is monotone in the edge set)
    without_c = []
    enumerate_solutions(n, n, monotone=False, node_filter=lambda es: feas(n, es),
                        callback=lambda e, a: without_c.append(tuple(e)))
    assert len(without_c) == len(set(without_c))
    assert set(with_c) == set(without_c)
    # sanity: (c) is a strict relaxation of order feasibility only in the sense of being necessary
    assert len(with_c) == len(without_c)


# ----------------------------------------------------------------------------- helpers vs references
def _rand_edges(rng, n, m):
    es = set()
    for _ in range(m):
        es.add(tuple(sorted(rng.sample(range(n), 3))))
    return sorted(es)


def test_independence_number_matches_reference():
    rng = random.Random(5)
    for _ in range(300):
        n = rng.randint(4, 14)
        es = _rand_edges(rng, n, rng.randint(0, 20))
        assert independence_number(n, es) == alpha_of_edges(n, es)
        assert independence_number(n, es, stop_at=3) >= min(3, alpha_of_edges(n, es))


def _f7_brute(edges):
    es = {frozenset(e) for e in edges}
    F7 = [frozenset(x) for x in ((0, 1, 2), (0, 3, 4), (0, 5, 6), (1, 3, 5), (2, 4, 6))]
    verts = sorted({v for e in es for v in e})
    for img in itertools.permutations(verts, 7):
        if all(frozenset(img[v] for v in f) in es for f in F7):
            return True
    return False


def test_has_f7():
    F7 = [(0, 1, 2), (0, 3, 4), (0, 5, 6), (1, 3, 5), (2, 4, 6)]
    assert has_f7(F7)
    assert not has_f7(F7[:4])
    assert has_f7([tuple(sorted((v * 3) % 7 + 10 * (v % 2) for v in e)) for e in F7] + [(100, 101, 102)])
    rng = random.Random(7)
    for _ in range(150):
        n = rng.randint(7, 8)
        es = _rand_edges(rng, n, rng.randint(5, 12))
        assert has_f7(es) == _f7_brute(es)
    # planted copy in a random hypergraph
    for _ in range(30):
        perm = rng.sample(range(9), 7)
        es = [tuple(sorted(perm[v] for v in f)) for f in F7] + _rand_edges(rng, 9, 4)
        assert has_f7(es)


# ----------------------------------------------------------------------------- C vs Python
@pytest.mark.parametrize("n,T,m_min,f7", [(7, 4, 0, 0), (8, 5, 0, 0), (8, 6, 3, 1), (9, 6, 0, 1),
                                           (9, 7, 5, 0), (9, 6, 6, 1)])
def test_c_equals_python_solution_sets(n, T, m_min, f7):
    if not _c_available():
        pytest.skip("no C compiler")
    py = []
    st = enumerate_solutions(n, T, m_min=m_min, forbid_f7=bool(f7), callback=lambda e, a: py.append(tuple(e)))
    sols, cst = run_c(n=n, T=T, m_min=m_min, f7=f7, mode="enum", progress=0)
    assert {e for a, e in sols} == set(py) and len(sols) == len(py)
    assert int(cst["nodes"]) == st["nodes"]  # same pruning, same tree
    assert int(cst["leaves"]) == st["leaves"]
    for a, e in sols:
        assert alpha_of_edges(n, list(e)) == a <= T


def test_c_equals_python_flags():
    if not _c_available():
        pytest.skip("no C compiler")
    n, T = 9, 6
    py = []
    enumerate_solutions(n, T, forbid_f7=True, up_to_reflection=True, callback=lambda e, a: py.append(tuple(e)))
    sols, _ = run_c(n=n, T=T, f7=1, refl=1, mode="enum", progress=0)
    assert {e for a, e in sols} == set(py) and len(sols) == len(py)
    py = []
    enumerate_solutions(n, T, m_exact=6, callback=lambda e, a: py.append(tuple(e)))
    sols, _ = run_c(n=n, T=T, m_exact=6, mode="enum", progress=0)
    assert {e for a, e in sols} == set(py)
    # unrefined and non-monotone variants agree between implementations
    py = []
    st = enumerate_solutions(n, T, refine=False, callback=lambda e, a: py.append(tuple(e)))
    sols, cst = run_c(n=n, T=T, refine=0, mode="enum", progress=0)
    assert {e for a, e in sols} == set(py) and int(cst["nodes"]) == st["nodes"]
    py = []
    st = enumerate_solutions(8, 5, monotone=False, callback=lambda e, a: py.append(tuple(e)))
    sols, cst = run_c(n=8, T=5, mono=0, mode="enum", progress=0)
    assert {e for a, e in sols} == set(py) and int(cst["nodes"]) == st["nodes"]


def test_c_counts_n10():
    if not _c_available():
        pytest.skip("no C compiler")
    py = []
    st = enumerate_solutions(10, 6, forbid_f7=True, callback=lambda e, a: py.append(tuple(e)))
    sols, cst = run_c(n=10, T=6, f7=1, mode="count", progress=0)
    assert int(cst["solutions"]) == len(py) == 3 and int(cst["nodes"]) == st["nodes"]


def test_exists_and_unsat():
    assert exists(8, 5) is not None
    assert exists(8, 4) is None  # f(8)=5 and the class has min alpha 5
    e = exists(10, 6, m_min=7)
    assert e is not None and alpha_of_edges(10, e) <= 6 and len(e) >= 7
