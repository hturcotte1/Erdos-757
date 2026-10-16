"""Referee L002: compare (a) my brute force (mydfs allm=1, pairwise constraints only, exact alpha at leaves),
(b) my pruned CSP search (mydfs prune=1), (c) the census binary (ordered_dfs at commit ea6c3d9, f7=1, mode=count)
on every (n, m, T) cell for n = 5..NMAX."""
import subprocess, sys, re, collections
NMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 10
CENSUS = "census_src/ordered_dfs_census"
def census(n, m, T):
    out = subprocess.run([CENSUS, f"n={n}", f"T={T}", f"m_min={m}", f"m_exact={m}", "f7=1", "mode=count", "progress=0"],
                         capture_output=True, text=True, timeout=3000).stdout
    d = re.search(r"DONE nodes=(\d+) leaves=(\d+) solutions=(\d+) timed_out=(\d)", out)
    assert d and d.group(4) == "0", out[-300:]
    return int(d.group(3))
def mine(n, m, T):
    out = subprocess.run(["./mydfs", f"n={n}", f"m={m}", f"T={T}", "prune=1"], capture_output=True, text=True, timeout=3000).stdout
    return int(re.search(r"sols=(\d+)", out).group(1))
bad = 0; cells = 0
NMIN = int(sys.argv[2]) if len(sys.argv) > 2 else 5
for n in range(NMIN, NMAX + 1):
    hist = collections.defaultdict(int)
    for line in open(f"brute_n{n}.txt"):
        g = re.match(r"H n=\d+ m=(\d+) alpha=(\d+) count=(\d+)", line)
        if g: hist[(int(g.group(1)), int(g.group(2)))] = int(g.group(3))
    for m in range(0, n - 1):
        alphas = [a for (mm, a) in hist if mm == m]
        lo = (min(alphas) - 1) if alphas else 0
        hi = max(alphas) if alphas else n
        for T in range(max(lo, 0), hi + 1):
            b = sum(c for (mm, a), c in hist.items() if mm == m and a <= T)
            c = census(n, m, T); p = mine(n, m, T); cells += 1
            flag = "" if b == c == p else "  <-- MISMATCH"
            if flag: bad += 1
            print(f"n={n} m={m} T={T}: brute={b} census={c} mine_pruned={p}{flag}", flush=True)
print(f"cells={cells} mismatches={bad}")
