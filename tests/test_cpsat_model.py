"""Tests for e757/cpsat_model.py (abstract ordered-midpoint-hypergraph engine)."""
import json
from pathlib import Path

import pytest

from e757 import cpsat_model as C
from e757.saturated import alpha_of_edges, is_linear, map_of_set, edges_of_map

REPO = Path(__file__).resolve().parent.parent
F7 = [(0, 1, 2), (0, 3, 4), (0, 5, 6), (1, 3, 5), (2, 4, 6)]


def test_f7_detection():
    assert len(C.find_f7(F7)) == 1
    # relabel F7 arbitrarily: still detected
    perm = [3, 6, 0, 5, 1, 2, 4]
    rel = [tuple(sorted(perm[v] for v in e)) for e in F7]
    assert C.find_f7(rel)
    assert C.is_f7_free(F7[:4])


def test_independent_sets_match_alpha():
    for edges in (F7, [(0, 1, 2), (1, 3, 5), (2, 4, 6)], []):
        a, I = C.independent_sets(7, edges, 0, want_max=True)
        assert a == alpha_of_edges(7, edges) == len(I)
        assert all(not set(e) <= set(I) for e in edges)


@pytest.mark.parametrize("n", [5, 6, 7, 8, 9])
@pytest.mark.parametrize("f7", [True, False])
def test_min_alpha_matches_bruteforce(n, f7):
    a, edges, st = C.solve_min_alpha(n, forbid_f7=f7, time_limit=120)
    assert st["optimal"]
    assert C.is_ordered_midpoint_hypergraph(n, edges)
    assert alpha_of_edges(n, edges) == a
    assert (not f7) or C.is_f7_free(edges)
    # nothing better exists.  For n = 9 only the F7-unrestricted search is run (about 40 s); it
    # implies the F7-free statement because F7-free hypergraphs are a subset.
    if n < 9 or not f7:
        assert not C.brute_exists(n, a - 1, forbid_f7=f7 and n < 9)
    if n < 9:
        assert C.brute_exists(n, a, forbid_f7=f7)


def test_symmetry_breaking_does_not_change_value():
    for n in (7, 8, 9):
        a1 = C.solve_min_alpha(n, symmetry=True)[0]
        a2 = C.solve_min_alpha(n, symmetry=False)[0]
        assert a1 == a2


def _brute_all(n, T, m, forbid_f7=True):
    """All ordered midpoint hypergraphs with exactly m edges and alpha <= T (plain DFS)."""
    out = []

    def rec(j, edges, used):
        if j == n - 1:
            if len(edges) == m and alpha_of_edges(n, edges) <= T and (not forbid_f7 or C.is_f7_free(edges)):
                out.append(tuple(sorted(edges)))
            return
        if len(edges) + (n - 1 - j) < m:
            return
        for i in range(j):
            for k in range(j + 1, n):
                p = (1 << (i * n + j)) | (1 << (j * n + k)) | (1 << (i * n + k))
                if not p & used:
                    rec(j + 1, edges + [(i, j, k)], used | p)
        rec(j + 1, edges, used)

    rec(1, [], 0)
    return out


@pytest.mark.parametrize("f7", [True, False])
def test_enumerate_matches_bruteforce(f7):
    n, T, m = 7, 5, 5
    c_sym, s_sym, status1 = C.enumerate_solutions(n, T, m, symmetry=True, forbid_f7=f7)
    c_all, s_all, status2 = C.enumerate_solutions(n, T, m, symmetry=False, forbid_f7=f7)
    assert status1 == status2 == "COMPLETE"
    refl = lambda E: tuple(sorted((n - 1 - k, n - 1 - j, n - 1 - i) for i, j, k in E))  # noqa: E731
    brute = set(_brute_all(n, T, m, forbid_f7=f7))
    assert {tuple(sorted(E)) for E, _ in s_all} == brute
    assert c_all == len(brute)
    orbits = {min(E, refl(E)) for E in brute}
    assert c_sym == len(orbits)
    for edges, a in s_all:
        assert a <= T and len(edges) == m and C.is_ordered_midpoint_hypergraph(n, edges)


@pytest.mark.parametrize("key,n,h", [("12", 12, 7), ("14", 14, 8)])
def test_known_sets_are_feasible_hypergraphs(key, n, h):
    d = json.load(open(REPO / "data" / "small_records.json"))["sets"][key]
    lo, hi, mid = map_of_set(d["set"])
    edges = edges_of_map(mid)
    assert C.is_ordered_midpoint_hypergraph(n, edges)
    assert C.is_f7_free(edges)
    assert alpha_of_edges(n, edges) == h  # so c_hyp(n) <= h


def test_cuts_valid_on_known_set():
    """Every alpha-cut for T = h(A) - ... is satisfied by the real 12-point set when T >= h."""
    d = json.load(open(REPO / "data" / "small_records.json"))["sets"]["12"]
    _, _, mid = map_of_set(d["set"])
    edges = edges_of_map(mid)
    T = 7
    for I in C.independent_sets(12, edges, 0, want_max=True)[1:2]:
        assert len(I) == 7  # no (T+1)-independent set exists, so no cut is generated
    assert C.independent_sets(12, edges, T + 1) == []


# ----------------------------------------------------------------------------- realizability constraints
import random

from e757 import realizability as R

CORES = C.load_cores(REPO / "data" / "forbidden_ordered_n7.json", REPO / "data" / "forbidden_ordered_n8.json")


def _all_patterns(n):
    res = []

    def rec(j, edges, used):
        if j == n - 1:
            res.append(tuple(edges))
            return
        rec(j + 1, edges, used)
        for i in range(j):
            for k in range(j + 1, n):
                prs = [(i, j), (j, k), (i, k)]
                if any(p in used for p in prs):
                    continue
                rec(j + 1, edges + [(i, j, k)], used | set(prs))

    rec(1, [], frozenset())
    return res


@pytest.mark.parametrize("n", [3, 4, 5, 6, 7])
def test_every_realizable_pattern_satisfies_constraints(n):
    """Soundness of K30/K31/cores: all patterns with realize_exact == True (census n<=7) pass; and
    the constraints are not vacuous (some non-realizable patterns are cut)."""
    n_real = n_cut = 0
    for edges in _all_patterns(n):
        viol = C.constraint_violations(n, edges, cores=CORES)
        r = R.realize_exact(n, list(edges))
        if r[0]:
            n_real += 1
            assert not viol, (edges, viol[:2])
        elif viol:
            n_cut += 1
    assert n_real > 0
    if n >= 5:
        assert n_cut > 0


def test_random_n8_realizable_patterns_satisfy_constraints():
    rng = random.Random(1)
    pats = _all_patterns(8)
    rng.shuffle(pats)
    seen = 0
    for edges in pats[:3000]:
        if R.realize_exact(8, list(edges))[0]:
            seen += 1
            assert not C.constraint_violations(8, edges, cores=CORES), edges
    assert seen > 50


def test_clause_generator_agrees_with_checker():
    """CP-SAT model (monotone+medial+cores) accepts a pattern iff the python checker does (n=7)."""
    n = 7
    mod = C.build_model(n, symmetry=False, monotone=True, medial=True, cores=CORES)
    rng = random.Random(2)
    pats = _all_patterns(n)
    rng.shuffle(pats)
    for edges in pats[:150]:
        m2 = mod.model.Clone()
        es = set(edges)
        # clone variables are addressed by index
        for t in mod.tri:
            m2.Add(m2.GetBoolVarFromProtoIndex(mod.e[t].Index()) == (1 if t in es else 0))
        s = C.cp_model.CpSolver()
        ok = s.Solve(m2) in (C.cp_model.OPTIMAL, C.cp_model.FEASIBLE)
        assert ok == (not C.constraint_violations(n, edges, cores=CORES)), edges


def test_record_patterns_satisfy_constraints():
    d = json.load(open(REPO / "data" / "small_records.json"))["sets"]
    assert len(d) == 7
    for key, rec in d.items():
        lo, hi, mid = map_of_set(rec["set"])
        edges = edges_of_map(mid)
        assert not C.constraint_violations(len(rec["set"]), edges, cores=CORES), key


@pytest.mark.parametrize("n,expect", [(8, 5), (9, 6), (10, 6), (11, 7), (12, 7)])
def test_min_alpha_with_all_constraints_unchanged(n, expect):
    """Realizable sets attain the table values, so the constrained minimum must still equal them."""
    a, edges, st = C.solve_min_alpha(n, forbid_f7=True, time_limit=300, monotone=True, medial=True,
                                     cores=[c for c in CORES if len(c["edges"]) <= 4], use_hy=True)
    assert st["optimal"] and a == expect
    assert not C.constraint_violations(n, edges, monotone=True, medial=True,
                                       cores=[c for c in CORES if len(c["edges"]) <= 4])


def test_solve_realizable_sat_and_unsat():
    st, info = C.solve_realizable(10, 6, monotone=True, medial=True, time_limit=60, workers=2)
    assert st == "SAT"
    from e757.core import alpha as h_of
    assert h_of(info["set"]) == 6 and len(info["set"]) == 10
    # f(7) = 5 and f(8) = 5: no realizable pattern with alpha <= 4
    for n in (7, 8):
        st, info = C.solve_realizable(n, 4, monotone=True, medial=True, time_limit=60, workers=2)
        assert st == "UNSAT", (n, st)
