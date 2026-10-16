"""Post-processing of a finished prefix-split enumeration (n, m=n-2, alpha<=T).  Resumable at every stage.
  python3 postprocess.py N T M RESULTS_DIR TAG [P]
Stages (markers in RESULTS_DIR/post/):
 1 filter : stream all <TAG>_prefix_*.jsonl.gz through ./filter (C: K30, K31, cores, reflection canon) ->
            post/filtered.txt.gz  (lines: k30 k31 c4 call edges; c4 = no core with <=4 edges, call = no core at all)
 2 realize: O' patterns (k30&k31&c4) in batches of 4000, Pool(P): exact realization (fastreal.realize_fast for rigid
            patterns, e757.realizability.realize_exact fallback) -> post/real_<batch>.json.gz (+ .done)
 3 summary: affine classes (translate/gcd/reflection), reasons histogram, known sets, record-beating check,
            judge spot check of 50 random realized sets -> post/summary.json, post/judge_spotcheck.txt
Time model from (12,10): filter 0.19 ms per raw solution (single process); realization ~2 ms per O' pattern at n=12
(about 2-4 ms at n=14) / P."""
import sys, os, gzip, json, math, glob, random, subprocess, time
from multiprocessing import Pool
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, ROOT); sys.path.insert(0, HERE)
N, T, M = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
RES, TAG = os.path.abspath(sys.argv[4]), sys.argv[5]
P = int(sys.argv[6]) if len(sys.argv) > 6 else 3
POST = os.path.join(RES, "post"); os.makedirs(POST, exist_ok=True)
BATCH = 4000


def canon(edges):
    t = tuple(sorted(tuple(e) for e in edges))
    r = tuple(sorted((N - 1 - k, N - 1 - j, N - 1 - i) for i, j, k in t))
    return min(t, r)


def normalize(vals):
    v = sorted(vals); lo = v[0]; v = [x - lo for x in v]
    g = 0
    for x in v: g = math.gcd(g, x)
    v = [x // g for x in v]
    return tuple(min(v, sorted(v[-1] - x for x in v)))


def stage_filter():
    out = os.path.join(POST, "filtered.txt.gz")
    if os.path.exists(out + ".done"): return
    subprocess.run(["gcc", "-O2", "-o", os.path.join(POST, "filter"), os.path.join(HERE, "filter.c")], check=True)
    cores = os.path.join(POST, "cores.txt")
    subprocess.run([sys.executable, os.path.join(HERE, "dump_cores.py"), cores, str(N)], check=True, cwd=ROOT)
    files = sorted(glob.glob(os.path.join(RES, TAG + "_prefix_*.jsonl.gz")))
    assert files, "no prefix files"
    # convert jsonl -> SOL lines on the fly into the filter's stdin
    flt = subprocess.Popen([os.path.join(POST, "filter"), cores], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                           stderr=open(os.path.join(POST, "filter.stderr"), "w"), text=True)
    gz = subprocess.Popen(["gzip"], stdin=flt.stdout, stdout=open(out, "wb"))
    for f in files:
        with gzip.open(f, "rt") as g:
            for line in g:
                flt.stdin.write("SOL 0 " + " ".join("%d,%d,%d" % tuple(e) for e in json.loads(line)) + "\n")
    flt.stdin.close(); flt.wait(); gz.wait()
    assert flt.returncode == 0
    open(out + ".done", "w").write(open(os.path.join(POST, "filter.stderr")).read())


def real_batch(args):
    bi, pats = args
    from e757.core import alpha, is_45_set, ap_edges
    from e757.realizability import realize_exact, _rref, _x_rows
    from fastreal import realize_fast
    reasons, real, fb = {}, [], 0
    for t, in_call in pats:
        fr = realize_fast(N, list(t))
        if fr is None:
            fb += 1; r = realize_exact(N, list(t))
        else:
            r = (fr[0] == "ok", fr[1])
        if not r[0]:
            reasons[r[1]] = reasons.get(r[1], 0) + 1
            if not in_call: reasons["(excluded by long core) " + r[1]] = reasons.get("(excluded by long core) " + r[1], 0) + 1
            continue
        vals = sorted(r[1]); h = alpha(vals, ap_edges(vals)); ok45 = is_45_set(vals)
        R, piv = _rref(_x_rows(N, list(t)), N)
        real.append({"edges": [list(e) for e in t], "set": vals, "h": h, "is_45": ok45, "rigid": (N - len(piv)) == 2, "in_call": in_call})
    path = os.path.join(POST, "real_%05d.json.gz" % bi)
    with gzip.open(path + ".part", "wt") as g: json.dump({"reasons": reasons, "real": real, "fallback": fb, "n": len(pats)}, g)
    os.replace(path + ".part", path)
    open(path + ".done", "w").write("1")
    return bi


def stage_realize():
    counts = {"canon": 0, "k30": 0, "k31": 0, "c4": 0, "call": 0}
    batches, cur = [], []
    for line in gzip.open(os.path.join(POST, "filtered.txt.gz"), "rt"):
        f = line.split(); fl = list(map(int, f[:4]))
        counts["canon"] += 1; counts["k30"] += fl[0]
        if fl[0] and fl[1]:
            counts["k31"] += 1
            if fl[2]:
                counts["c4"] += 1; counts["call"] += fl[3]
                cur.append((tuple(tuple(map(int, t.split(","))) for t in f[4:]), fl[3]))
                if len(cur) == BATCH: batches.append(cur); cur = []
    if cur: batches.append(cur)
    json.dump(counts, open(os.path.join(POST, "filter_counts.json"), "w"))
    todo = [(i, b) for i, b in enumerate(batches) if not os.path.exists(os.path.join(POST, "real_%05d.json.gz.done" % i))]
    print("batches", len(batches), "todo", len(todo), flush=True)
    with Pool(P) as pool:
        for bi in pool.imap_unordered(real_batch, todo): print("batch", bi, "done", flush=True)
    return counts, len(batches)


def stage_summary(counts, nb):
    from e757 import core as _core
    from e757.saturated import map_of_set, edges_of_map
    from e757.core import alpha
    reasons, realizable, fb, tested = {}, [], 0, 0
    for i in range(nb):
        d = json.load(gzip.open(os.path.join(POST, "real_%05d.json.gz" % i), "rt"))
        for k, v in d["reasons"].items(): reasons[k] = reasons.get(k, 0) + v
        realizable += d["real"]; fb += d["fallback"]; tested += d["n"]
    classes = {}
    for k, r in enumerate(realizable): classes.setdefault(normalize(r["set"]), []).append(k)
    known = {}
    data = json.load(open(os.path.join(ROOT, "data/small_records.json")))["sets"]
    cands = {("record_" + k): v["set"] for k, v in data.items() if len(v["set"]) == N}
    cands.update({"core.KNOWN: " + k: v for k, v in _core.KNOWN.items() if len(v) == N})
    cset = set(canon(r["edges"]) for r in realizable)
    for name, A in cands.items():
        lo, hi, mid = map_of_set(A)
        known[name] = {"pattern_in_realizable": canon(edges_of_map(mid)) in cset, "affine_class_in_realized": normalize(A) in classes, "h": alpha(sorted(A))}
    # judge spot check
    random.seed(757); tmp = os.path.join(POST, "judge_tmp"); os.makedirs(tmp, exist_ok=True)
    for k, r in enumerate(random.sample(realizable, min(50, len(realizable)))):
        json.dump({"id": "cs%02d" % k, "type": "construction", "set": r["set"], "claimed_h": T, "notes": "census spot check"}, open(os.path.join(tmp, "cs%02d.json" % k), "w"))
    jr = subprocess.run([sys.executable, os.path.join(ROOT, "judge/judge.py")] + sorted(glob.glob(os.path.join(tmp, "*.json"))), capture_output=True, text=True).stdout
    open(os.path.join(POST, "judge_spotcheck.txt"), "w").write(jr)
    out = {"N": N, "T": T, "M": M, "filter_counts": counts, "n_tested": tested, "n_realizable": len(realizable),
           "n_rigid": sum(r["rigid"] for r in realizable), "n_affine_classes": len(classes), "unrealizable_reasons": reasons,
           "all_h_eq_T": all(r["h"] == T for r in realizable), "all_45": all(r["is_45"] for r in realizable),
           "realizable_all_in_full_core_set": all(r["in_call"] for r in realizable),
           "record_beating": [r["set"] for r in realizable if 7 * r["h"] < 4 * N], "known_sets": known,
           "n_fallback_to_realize_exact": fb, "judge_pass_count": jr.count("PASS"), "judge_lines": len(jr.strip().splitlines())}
    json.dump(out, open(os.path.join(POST, "summary.json"), "w"), indent=1)
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    t0 = time.time()
    tot = os.path.join(RES, TAG + "_TOTAL.json")
    assert os.path.exists(tot), "enumeration not finished (no %s)" % tot
    print("enumeration total:", open(tot).read(), flush=True)
    stage_filter(); print("filter done %.0fs" % (time.time() - t0), flush=True)
    counts, nb = stage_realize(); print("realize done %.0fs" % (time.time() - t0), flush=True)
    stage_summary(counts, nb)
