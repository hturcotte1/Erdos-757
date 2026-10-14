"""Cross-engine counts of the extremal census: the number of members of O(n) (linear, midpoint-injective, K30,
F7-free) with exactly m edges and alpha <= T, counted by (1) the C DFS, (2) the Python DFS and (3) CP-SAT native
enumeration (e757.cpsat_model.enumerate_native without K31/cores), must agree.
Small instances always run; the (9,7,6) and (10,8,6) instances (CP-SAT 1-15 min) run when E757_SLOW=1.
Known values: (7,5,5)=10, (8,6,5)=260, (8,6,6)=286, (9,7,6)=8570, (10,8,6)=79488.
Also the 12-point census: experiments/20261014-1005-census-dfs/results/n12_m10_all.jsonl.gz has 2,226,490 lines."""
import os
import tempfile

import pytest

from e757.cpsat_model import enumerate_native
from e757.ordered_dfs import enumerate_solutions
from e757.ordered_dfs_c import available, run as run_c

SLOW = os.environ.get("E757_SLOW") == "1"
CASES = [(7, 5, 5, 10), (8, 6, 5, 260), (8, 6, 6, 286)]
if SLOW:
    CASES += [(9, 7, 6, 8570), (10, 8, 6, 79488)]


def count_dfs_py(n, m, T):
    sols = []
    enumerate_solutions(n, T, m_min=m, m_exact=m, forbid_f7=True, callback=lambda e, a: sols.append(tuple(sorted(e))))
    assert len(sols) == len(set(sols))
    return set(sols)


def count_dfs_c(n, m, T):
    sols, stats = run_c(n=n, T=T, m_min=m, m_exact=m, f7=1, mode="enum", progress=0)
    assert int(stats["timed_out"]) == 0
    return {tuple(sorted(e)) for a, e in sols}


def count_cpsat(n, m, T):
    with tempfile.TemporaryDirectory() as d:
        path = os.path.join(d, "s.jsonl")
        cnt, status = enumerate_native(n, T, m, path, monotone=True, medial=False, core_max_edges=None,
                                       time_limit=3000)
        assert status == "EXHAUSTED"
        import json
        sols = {tuple(sorted(tuple(e) for e in json.loads(l))) for l in open(path)}
        assert len(sols) == cnt
        return sols


@pytest.mark.parametrize("n,m,T,expected", CASES)
def test_census_counts_agree(n, m, T, expected):
    c = count_dfs_c(n, m, T)
    cp = count_cpsat(n, m, T)
    assert len(c) == len(cp) == expected
    assert c == cp
    if n <= 9:
        assert count_dfs_py(n, m, T) == c


@pytest.mark.skipif(not available(), reason="C binary unavailable")
def test_c_binary_runs():
    assert len(count_dfs_c(7, 5, 5)) == 10
