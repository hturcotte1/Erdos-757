"""Referee L004, check T1: bookkeeping of the prefix-split census and per-pattern invariants (own code only).
usage: python3 check_book.py RESULTS_DIR OUT_KEYS.gz
 - prefixes file has 2537 entries; every index has .done + .jsonl.gz, no .part
 - .done: prefix field == prefixes[idx], timed_out == 0, solutions == #lines of the jsonl.gz (full gzip read)
 - totals equal n14_m12_TOTAL.json
 - every solution: its edges at midpoints 1..3 equal the prefix edges
 - every solution through ./pchk 14: saturated, linear, K30, F7-free, alpha <= 8, canonical (P <= refl P)
 - all canonical keys distinct; writes sorted keys (one per line: key) to OUT_KEYS.gz, with prefix idx
"""
import gzip, json, os, subprocess, sys, collections

RES, OUT = sys.argv[1], sys.argv[2]
HERE = os.path.dirname(os.path.abspath(__file__))
TAG = "n14_m12"
pref = open(os.path.join(RES, TAG + "_prefixes.txt")).read().split()
print("prefixes in file:", len(pref), "distinct:", len(set(pref)))
problems = collections.Counter()
tot_s = tot_n = 0; tot_t = 0.0
names = set(os.listdir(RES))
assert not any(x.endswith(".part") for x in names), "part files present"

p = subprocess.Popen([os.path.join(HERE, "pchk"), "14"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
import threading
outlines = []
def reader():
    for l in p.stdout: outlines.append(l)
th = threading.Thread(target=reader); th.start()

per_prefix = []
for idx, pr in enumerate(pref):
    base = os.path.join(RES, "%s_prefix_%05d" % (TAG, idx))
    if not os.path.exists(base + ".done") or not os.path.exists(base + ".jsonl.gz"):
        problems["missing"] += 1; continue
    d = json.load(open(base + ".done"))
    if d.get("prefix") != pr: problems["prefix_field_mismatch"] += 1
    if int(d["timed_out"]) != 0: problems["timed_out"] += 1
    pe = []
    for tok in pr.split(","):
        a, b = tok.split("-"); pe.append((int(a), int(b)))
    cnt = 0
    with gzip.open(base + ".jsonl.gz", "rt") as g:
        for line in g:
            es = json.loads(line); cnt += 1
            bym = {e[1]: (e[0], e[2]) for e in es}
            for lvl in (1, 2, 3):
                if bym.get(lvl) != pe[lvl - 1]: problems["solution_not_in_prefix"] += 1; break
            p.stdin.write("%d %s\n" % (idx, " ".join("%d,%d,%d" % tuple(e) for e in es)))
    if cnt != int(d["solutions"]): problems["count_mismatch"] += 1
    per_prefix.append(cnt)
    tot_s += cnt; tot_n += int(d["nodes"]); tot_t += float(d["time"])
p.stdin.close(); p.wait(); th.join()
T = json.load(open(os.path.join(RES, TAG + "_TOTAL.json")))
print("sum solutions", tot_s, "sum nodes", tot_n, "sum time %.1f" % tot_t, "TOTAL file", T)
if tot_s != T["solutions"] or tot_n != T["nodes"]: problems["total_mismatch"] += 1
flags = collections.Counter(); keys = []; own = set(); sym = 0
alph = collections.Counter()
for l in outlines:
    f = l.split()
    idx, sat, lin, k30, f7, al, canon, sy, key, ownk = f[0], *map(int, f[1:8]), f[8], f[9]
    alph[al] += 1
    if not (sat and lin and k30 and f7 == 0 and al <= 8 and canon): flags[(sat, lin, k30, f7, al <= 8, canon)] += 1
    sym += sy
    keys.append((key, idx)); own.add(ownk)
print("patterns checked", len(outlines), "alpha histogram", dict(alph), "symmetric", sym)
print("flag failures", dict(flags))
ks = [k for k, _ in keys]
print("distinct canonical keys", len(set(ks)), "of", len(ks), "; distinct labelled", len(own))
if len(set(ks)) != len(ks): problems["duplicate_keys"] += 1
with gzip.open(OUT, "wt") as g:
    for k, idx in sorted(keys): g.write("%s %s\n" % (k, idx))
print("per-prefix: zero-solution prefixes", sum(1 for c in per_prefix if c == 0), "max", max(per_prefix))
print("PROBLEMS", dict(problems))
