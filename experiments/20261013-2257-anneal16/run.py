#!/usr/bin/env python3
"""Parallel driver for e757.anneal (Track U1).

  python3 experiments/20261013-2257-anneal16/run.py --seconds 21600 --configs 16:0,16:1,16:0,18:0 --seed0 1000

--configs  comma list of n:nfree, one worker process each (target h = ceil(4n/7)-1: 9 for n=16, 10 for n=18)
Writes logs/worker_<k>.log, logs/ckpt_<k>.json (each worker), and best.json (merged, every --every seconds).
Any (4,5)-set with h/n < 4/7 is passed through scripts/new_claim.py immediately.
"""
import argparse, json, math, multiprocessing as mp, os, subprocess, sys, time
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent
sys.path.insert(0, str(REPO))
from e757.anneal import Runner  # noqa: E402


def worker(k, n, nfree, seed, seconds, w, t_start):
    d = json.load(open(REPO / "data" / "small_records.json"))["sets"]
    seeds = [(name, d[name]["set"]) for name in ("14", "12", "12b", "12c", "11", "10") if len(d[name]["set"]) <= n]
    logf = open(HERE / "logs" / f"worker_{k}.log", "a", buffering=1)

    def log(msg):
        logf.write(f"{time.strftime('%H:%M:%S')} [w{k} n={n} nf={nfree} seed={seed}] {msg}\n")

    target = math.ceil(4 * n / 7) - 1
    r = Runner(n, target, seed, nfree=nfree, w=w, seeds_from=seeds, log=log, ckpt=HERE / "logs" / f"ckpt_{k}.json")

    def on_hit(m, h, ints):
        sf = HERE / "logs" / f"hit_{k}_{seed}_{len(r.hits)}.json"
        sf.write_text(json.dumps(ints))
        out = subprocess.run([sys.executable, str(REPO / "scripts" / "new_claim.py"), "--slug", f"anneal{n}-{seed}",
                              "--set-file", str(sf), "--notes", "found by e757.anneal (Track U1)"],
                             capture_output=True, text=True, cwd=REPO)
        log("JUDGE: " + out.stdout.strip().replace("\n", " | ") + out.stderr.strip())
    r.on_hit = on_hit
    log(f"start target h<={target}")
    while True:
        left = seconds - (time.time() - t_start)
        if left <= 0:
            break
        r.run(seconds=min(left, 300))
        log(f"stats {r.stats} valid_alpha {r.valid_alpha} coll0_alpha {sorted(r.coll0_alpha.items())} "
            f"best_cost {r.best_cost and (round(r.best_cost['cost'], 3), r.best_cost['n_indep_target_plus_1'])}")
    r.dump()


def merge(nworkers):
    allr = []
    for k in range(nworkers):
        p = HERE / "logs" / f"ckpt_{k}.json"
        if p.exists():
            try:
                allr.append(json.loads(p.read_text()))
            except Exception:
                pass
    best = None
    for r in allr:
        b = r.get("best")
        if b and (best is None or b["h"] / b["n"] < best["h"] / best["n"]):
            best = b
    out = {"updated_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
           "best_valid_by_ratio": best,
           "workers": [{"n": r["n"], "nfree": r["nfree"], "seed": r["seed"], "stats": r["stats"],
                        "valid_alpha_distribution": r["valid_alpha_distribution"],
                        "coll0_alpha_distribution": r.get("coll0_alpha_distribution"),
                        "best_valid_h": r["best"] and r["best"]["h"],
                        "best_cost": r.get("best_cost") and {k: v for k, v in r["best_cost"].items() if k != "map"},
                        "hits": r["hits"]} for r in allr]}
    tmp = HERE / "best.json.tmp"
    tmp.write_text(json.dumps(out, indent=1))
    os.replace(tmp, HERE / "best.json")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--seconds", type=float, default=21600)
    ap.add_argument("--configs", default="16:0,16:1,16:0,18:0")
    ap.add_argument("--seed0", type=int, default=1000)
    ap.add_argument("--every", type=float, default=180)
    ap.add_argument("--w", type=float, default=1.0)
    ap.add_argument("--k0", type=int, default=0, help="worker index offset (to restart one crashed worker in place)")
    ap.add_argument("--no-merge", action="store_true", help="restarted single workers: leave best.json to the main driver")
    a = ap.parse_args()
    (HERE / "logs").mkdir(exist_ok=True)
    t0 = time.time()
    cfgs = [tuple(map(int, c.split(":"))) for c in a.configs.split(",")]
    procs = [mp.Process(target=worker, args=(a.k0 + k, n, nf, a.seed0 + k, a.seconds, a.w, t0)) for k, (n, nf) in enumerate(cfgs)]
    for p in procs:
        p.start()
    while any(p.is_alive() for p in procs):
        time.sleep(a.every)
        merge(len(cfgs)) if not a.no_merge else None
    merge(len(cfgs)) if not a.no_merge else None
