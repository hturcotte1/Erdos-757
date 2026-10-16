"""Compare enum.c (prune=0 and prune=1, all NONE budgets) with brute.py output for n=5..9, every (m,T)."""
import subprocess, re, sys
bad = 0; cells = 0
for n in range(5, 10):
    ref = {}
    for line in open(f"brute_n{n}.txt"):
        d = dict(kv.split("=") for kv in line.split())
        ref[(int(d["m"]), int(d["T"]))] = (int(d["f7free"]), int(d["f7"]))
    for T in range(1, n + 1):
        for prune in (0, 1):
            r = subprocess.run(["./enum", str(n), str(T), str(n - 2), str(prune), "0"], capture_output=True, text=True)
            got = {}
            for line in r.stderr.splitlines():
                mm = re.match(r"COUNT m=(\d+) alpha<=T: f7free=(\d+) f7=(\d+)", line)
                if mm: got[int(mm.group(1))] = (int(mm.group(2)), int(mm.group(3)))
            exp = {m: v for (m, TT), v in ref.items() if TT == T}
            for m in set(exp) | set(got):
                cells += 1
                if exp.get(m, (0, 0)) != got.get(m, (0, 0)):
                    bad += 1; print("MISMATCH", n, T, prune, m, exp.get(m), got.get(m))
print("cells", cells, "mismatches", bad)
