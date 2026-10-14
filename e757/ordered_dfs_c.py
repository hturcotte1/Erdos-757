"""Python wrapper for the C port e757/c/ordered_dfs.c (text protocol, see the C file header).

    from e757.ordered_dfs_c import run
    sols, stats = run(n=16, T=9, m_min=13, f7=True, mode="enum", tl=60)
    # sols: list of (alpha, edges) with edges a tuple of (i, j, k); stats: dict of strings from the DONE line
"""
from __future__ import annotations

import os
import subprocess

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BIN = os.path.join(_ROOT, "e757", "c", "ordered_dfs")


def build():
    """Compile the binary with gcc (e757/c/build.sh); returns True on success."""
    try:
        subprocess.run(["bash", os.path.join(_ROOT, "e757", "c", "build.sh")], check=True,
                       capture_output=True, timeout=120)
    except Exception:  # noqa: BLE001
        return False
    return os.path.exists(BIN)


def available():
    return os.path.exists(BIN) or build()


def run(timeout=None, **kw):
    """Run the binary with key=value arguments (booleans become 0/1); parse SOL/DONE lines."""
    if not available():
        raise RuntimeError("cannot build e757/c/ordered_dfs")
    args = [BIN] + ["%s=%s" % (k, int(v) if isinstance(v, bool) else v) for k, v in kw.items()]
    out = subprocess.run(args, capture_output=True, text=True, timeout=timeout, check=True).stdout
    sols, stats = [], {}
    for line in out.splitlines():
        if line.startswith("SOL"):
            parts = line.split()
            sols.append((int(parts[1]), tuple(tuple(int(x) for x in p.split(",")) for p in parts[2:])))
        elif line.startswith("DONE") or line.startswith("EST "):
            stats.update(kv.split("=") for kv in line.split()[1:])
    return sols, stats
