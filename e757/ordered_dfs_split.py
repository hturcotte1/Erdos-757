"""Prefix-split driver for the C DFS (e757/c/ordered_dfs): enumerates the surviving prefixes (choices at midpoints
1..depth, same rules as the DFS: linearity, injectivity, K30, F7, alpha look-ahead, budget) with
`mode=prefixes depth=k`, then runs `pre=<prefix>` below each prefix as a separate process (P at a time,
niced), streaming solutions to <outdir>/<tag>_prefix_<id>.jsonl.gz and writing <tag>_prefix_<id>.done (JSON of the
DONE stats).  Resumable: prefixes with a .done marker are skipped; unfinished ones restart from scratch (output is
written to a .part file and renamed on completion).  The prefix list is frozen in <outdir>/<tag>_prefixes.txt.

CLI:  python3 -m e757.ordered_dfs_split n T m depth P outdir [--refl] [--nice 10] [--tag NAME]
Union over prefixes of the solutions == the unsplit solution set (tests/test_census_counts.py)."""
import gzip
import json
import os
import subprocess
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor

from e757 import ordered_dfs_c

BIN = ordered_dfs_c.BIN


def _base_args(n, T, m, refl):
    return ["n=%d" % n, "T=%d" % T, "m_min=%d" % m, "m_exact=%d" % m, "f7=1", "progress=0", "refl=%d" % int(refl)]


def list_prefixes(n, T, m, depth):
    out = subprocess.run([BIN] + _base_args(n, T, m, False) + ["mode=prefixes", "depth=%d" % depth],
                         capture_output=True, text=True, check=True).stdout
    return [l.split()[1] for l in out.splitlines() if l.startswith("PRE ")]


def parse_sol(line):
    return [[int(x) for x in t.split(",")] for t in line.split()[2:]]


def run_prefix(n, T, m, prefix, path, refl=False, nice=10, binary=None):
    """Run the DFS below one prefix; stream to path (.jsonl.gz) atomically; returns the stats dict."""
    cmd = ([] if not nice else ["nice", "-n", str(nice)]) + [binary or BIN] + _base_args(n, T, m, refl) + \
        ["mode=enum", "pre=" + prefix]
    t0 = time.time()
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, text=True)
    stats, cnt = {}, 0
    with gzip.open(path + ".part", "wt") as g:
        for line in p.stdout:
            if line.startswith("SOL"):
                g.write(json.dumps(parse_sol(line), separators=(",", ":")) + "\n")
                cnt += 1
            elif line.startswith("DONE"):
                stats = dict(kv.split("=") for kv in line.split()[1:])
    rc = p.wait()
    if rc != 0 or not stats or int(stats.get("timed_out", 1)) != 0 or int(stats["solutions"]) != cnt:
        raise RuntimeError("prefix %s failed rc=%s stats=%s count=%d" % (prefix, rc, stats, cnt))
    os.replace(path + ".part", path)
    stats["wall"] = round(time.time() - t0, 2)
    stats["prefix"] = prefix
    return stats


def run_split(n, T, m, depth, P, outdir, refl=False, nice=10, tag=None, log=print):
    tag = tag or "n%d_m%d" % (n, m)
    os.makedirs(outdir, exist_ok=True)
    pl = os.path.join(outdir, tag + "_prefixes.txt")
    if os.path.exists(pl):
        prefixes = open(pl).read().split()
    else:
        prefixes = list_prefixes(n, T, m, depth)
        open(pl, "w").write("\n".join(prefixes) + "\n")
    log("prefixes: %d (depth %d)" % (len(prefixes), depth))
    lock = threading.Lock()
    state = {"done": 0, "skipped": 0, "sols": 0, "nodes": 0, "t0": time.time()}

    def job(idx):
        base = os.path.join(outdir, "%s_prefix_%05d" % (tag, idx))
        if os.path.exists(base + ".done"):
            st = json.load(open(base + ".done"))
            with lock:
                state["skipped"] += 1
            return st
        st = run_prefix(n, T, m, prefixes[idx], base + ".jsonl.gz", refl=refl, nice=nice)
        json.dump(st, open(base + ".done", "w"))
        with lock:
            state["done"] += 1
            state["sols"] += int(st["solutions"])
            state["nodes"] += int(st["nodes"])
            if state["done"] % 10 == 0 or state["done"] + state["skipped"] == len(prefixes):
                log("done %d/%d (skipped %d) sols+=%d nodes+=%.3g elapsed %.0fs" % (
                    state["done"] + state["skipped"], len(prefixes), state["skipped"], state["sols"],
                    state["nodes"], time.time() - state["t0"]))
        return st

    with ThreadPoolExecutor(max_workers=P) as ex:
        stats = list(ex.map(job, range(len(prefixes))))
    tot = {"prefixes": len(prefixes), "solutions": sum(int(s["solutions"]) for s in stats),
           "nodes": sum(int(s["nodes"]) for s in stats), "refl": bool(refl),
           "cpu_seconds": round(sum(float(s.get("time", 0)) for s in stats), 1)}
    json.dump(tot, open(os.path.join(outdir, tag + "_TOTAL.json"), "w"))
    log("TOTAL " + json.dumps(tot))
    return tot


def iter_solutions(outdir, tag):
    """Yield edge lists from all finished prefix files."""
    import glob
    for f in sorted(glob.glob(os.path.join(outdir, tag + "_prefix_*.jsonl.gz"))):
        with gzip.open(f, "rt") as g:
            for line in g:
                yield json.loads(line)


if __name__ == "__main__":
    a = sys.argv[1:]
    refl = "--refl" in a
    nice = 10
    tag = None
    if "--nice" in a:
        i = a.index("--nice"); nice = int(a[i + 1]); del a[i:i + 2]
    if "--tag" in a:
        i = a.index("--tag"); tag = a[i + 1]; del a[i:i + 2]
    a = [x for x in a if x != "--refl"]
    n, T, m, depth, P = map(int, a[:5])
    run_split(n, T, m, depth, P, a[5], refl=refl, nice=nice, tag=tag, log=lambda s: print(s, flush=True))
