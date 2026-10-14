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
