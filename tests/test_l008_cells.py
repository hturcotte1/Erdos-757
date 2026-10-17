"""Regression test for the cheap load-bearing computations of certificate L008 (f(16) = 10; K52).

Compiles the falsifier's connected-linear-3-graph enumerator conn_dfs3.c with gcc -O2 and checks
  * cells (15,9,6) and (16,8,6) are empty (2,056,435 and 19,103 nodes),
  * the connected (12,10,5), max-degree-3 labelled count is 145,033 (about 50 s),
and checks the witness A_base + {-323, 5000} is a (4,5)-set with h = 10, and that e757.fn_bounds marks n = 16 closed.
Skipped cleanly without gcc.  The 186M-node cell (15,10,6) is deliberately not run.
"""
import re
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

from e757 import core
from e757 import fn_bounds as B

REPO = Path(__file__).resolve().parent.parent
SRC = REPO / "experiments" / "20261017-0300-n16-via-i11" / "conn_dfs3.c"
A_BASE = [0, 136, 200, 243, 246, 249, 272, 286, 298, 323, 400, 528, 596, 1056]


@pytest.fixture(scope="module")
def conn_dfs3(tmp_path_factory):
    if shutil.which("gcc") is None:
        pytest.skip("gcc not available")
    exe = tmp_path_factory.mktemp("l008") / "conn_dfs3"
    subprocess.run(["gcc", "-O2", "-o", str(exe), str(SRC)], check=True)
    return exe


def run_cell(exe, n, m, tau0, maxdeg, timeout):
    out = subprocess.run(["nice", "-n", "5", str(exe), str(n), str(m), str(tau0), str(maxdeg), "0", "0"],
                         capture_output=True, text=True, timeout=timeout, check=True).stdout
    done = [l for l in out.splitlines() if l.startswith("DONE")]
    assert len(done) == 1
    d = dict(re.findall(r"(\w+)=(\d+)", done[0]))
    assert out.count("FOUND:") == int(d["found"])
    return int(d["nodes"]), int(d["found"])


def test_cell_15_9_6_empty(conn_dfs3):
    assert run_cell(conn_dfs3, 15, 9, 6, 3, 60) == (2056435, 0)


def test_cell_16_8_6_empty(conn_dfs3):
    assert run_cell(conn_dfs3, 16, 8, 6, 3, 60) == (19103, 0)


def test_connected_12_10_5_deg3_count(conn_dfs3):
    nodes, found = run_cell(conn_dfs3, 12, 10, 5, 3, 85)
    assert found == 145033 and nodes == 56801671


def test_witness_n16_h10():
    A = sorted(A_BASE + [-323, 5000])
    assert len(A) == 16 and core.is_45_set(A) and core.alpha(A) == 10


def test_f16_closed_in_fn_bounds():
    assert B.f_lower(16) == 10 and B.fn_bounds(20)[16] == (10, 10)
    assert B.is_closed(16) and not B.is_closed(18)
    assert B.fn_bounds(20)[18][0] == 10 and B.fn_bounds(20)[18][1] == 11  # f(18), f(20) still open
    assert B.beat_feasibility(16) == (True, 9, 7, 13)  # HY-only feasibility unchanged (backwards compatible)
    out = subprocess.run([sys.executable, "-m", "e757.fn_bounds"], cwd=REPO, capture_output=True, text=True,
                         check=True).stdout
    line16 = [l for l in out.splitlines() if l.startswith("n=16")][0]
    assert line16.startswith("n=16: CLOSED")
    line18 = [l for l in out.splitlines() if l.startswith("n=18")][0]
    assert line18.startswith("n=18: possible")
    assert "16: 10" in out.splitlines()[0]
