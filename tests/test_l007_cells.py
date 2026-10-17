"""Fast regression test for certificate L007 (window cells and tight cells).

Compiles the falsifier's connected-linear-3-graph enumerator conn_dfs2.c with gcc -O2 into a
temporary directory and checks the small cells cited in
results/proofs/L007-no-nonsaturated-extremal-14-point-sets.md:
  window cells (n,m,tau0) = (5,3,2),(8,4,3),(10,6,4),(11,5,4),(13,7,5): found = 0;
  tight cells (10,7,4) -> 637 labelled graphs, (13,8,5) -> 159 labelled graphs.
Slow cells ((12,9,5), the degree-3 (14,11,6) run) are deliberately excluded.
"""
import re
import shutil
import subprocess
from pathlib import Path

import pytest

SRC = (Path(__file__).resolve().parent.parent
       / "experiments" / "falsify" / "i11-inequality" / "conn_dfs2.c")
SUMMARY = re.compile(r"maxdeg=(\d+) n=(\d+) m=(\d+) tau0=(\d+) nodes=(\d+) found=(\d+)")


@pytest.fixture(scope="module")
def enum_bin(tmp_path_factory):
    gcc = shutil.which("gcc")
    if gcc is None:
        pytest.skip("gcc not available")
    if not SRC.exists():
        pytest.skip(f"missing {SRC}")
    out = tmp_path_factory.mktemp("l007") / "conn_dfs2"
    subprocess.run([gcc, "-O2", "-o", str(out), str(SRC)], check=True, timeout=60)
    return out


def run_cell(binary, n, m, tau0):
    p = subprocess.run(["nice", "-n", "5", str(binary), str(n), str(m), str(tau0)],
                       capture_output=True, text=True, timeout=30, check=True)
    hits = [ln for ln in p.stdout.splitlines() if SUMMARY.search(ln)]
    assert len(hits) == 1, p.stdout[-500:]
    mm = SUMMARY.search(hits[0])
    assert tuple(map(int, mm.groups()[1:4])) == (n, m, tau0)
    return int(mm.group(6))


@pytest.mark.parametrize("cell", [(5, 3, 2), (8, 4, 3), (10, 6, 4), (11, 5, 4), (13, 7, 5)])
def test_window_cells_empty(enum_bin, cell):
    assert run_cell(enum_bin, *cell) == 0


@pytest.mark.parametrize("cell,count", [((10, 7, 4), 637), ((13, 8, 5), 159)])
def test_tight_cells_counts(enum_bin, cell, count):
    assert run_cell(enum_bin, *cell) == count
