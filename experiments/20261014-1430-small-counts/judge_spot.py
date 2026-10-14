"""Judge spot check: 20 random realized sets per n (pooled over all m with realized sets, seed 757), checked by the
frozen verifier (read-only use) exactly as the L002 pipeline does."""
import sys, os, json, gzip, glob, random, subprocess
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
F = {6: 4, 7: 5, 8: 5, 9: 6, 10: 6, 11: 7}
JUDGE = os.path.join(ROOT, "judge", "judge.py")
out = {}
for n in range(6, 12):
    pool = []
    for f in sorted(glob.glob(HERE + "/results/n%d_m*_real.json.gz" % n)):
        for r in json.load(gzip.open(f, "rt")): pool.append((f, r["set"]))
    random.seed(757); pick = random.sample(pool, 20)
    tmp = os.path.join(HERE, "results", "judge_tmp_n%d" % n); os.makedirs(tmp, exist_ok=True)
    for k, (f, s) in enumerate(pick):
        json.dump({"id": "sc%d_%02d" % (n, k), "type": "construction", "set": s, "claimed_h": F[n], "notes": "small-counts spot check"},
                  open(os.path.join(tmp, "sc%d_%02d.json" % (n, k)), "w"))
    jr = subprocess.run([sys.executable, JUDGE] + sorted(glob.glob(tmp + "/*.json")), capture_output=True, text=True).stdout
    out[n] = {"lines": len(jr.strip().splitlines()), "pass": jr.count("PASS NO-IMPROVEMENT"), "pool": len(pool)}
    open(os.path.join(HERE, "results", "judge_spot_n%d.txt" % n), "w").write(jr)
    print(n, out[n], flush=True)
json.dump(out, open(os.path.join(HERE, "results", "judge_spot.json"), "w"))
