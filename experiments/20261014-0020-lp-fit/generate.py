"""Build dataset.jsonl.gz: feature rows of realizable AP hypergraphs (each row carries its integer point set).
Usage: python3 generate.py [--per-n 500] [--n20-seconds 600] [--subsets 200] [--seed 757] [--out dataset.jsonl.gz]
All quantities exact (ints). Floats are not used."""
import argparse, gzip, json, math, os, random, sys, time, itertools
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from e757.saturated import alpha_of_edges
from e757.anneal import random_linear_map, evaluate
from e757.saturated import to_integers


def normalize(S):
    S = sorted(S)
    t = [x - S[0] for x in S]
    g = 0
    for x in t:
        g = math.gcd(g, x)
    t = [x // g for x in t]
    r = [t[-1] - x for x in reversed(t)]
    return tuple(min(t, r))


def features(S):
    """S: sorted list of ints. Returns feature dict (exact)."""
    n = len(S)
    pos = {x: i for i, x in enumerate(S)}
    edges = []
    for i in range(n):
        for k in range(i + 2, n):
            s = S[i] + S[k]
            if s % 2 == 0 and (s // 2) in pos:
                edges.append((i, pos[s // 2], k))
    m = len({e[1] for e in edges})
    deg = [0] * n
    role_m = [0] * n
    role_e = [0] * n
    for (i, j, k) in edges:
        for v in (i, j, k):
            deg[v] += 1
        role_m[j] += 1
        role_e[i] += 1
        role_e[k] += 1
    alpha = alpha_of_edges(n, edges) if edges else n
    tau = n - alpha
    par = list(range(n))
    def find(x):
        while par[x] != x:
            par[x] = par[par[x]]
            x = par[x]
        return x
    for (i, j, k) in edges:
        par[find(i)] = find(j)
        par[find(k)] = find(j)
    comps = len({find(v) for v in range(n)})
    return {
        "n": n, "m": m, "e": len(edges), "tau": tau, "alpha": alpha, "non_mid": n - m,
        "d0": sum(1 for d in deg if d == 0), "d1": sum(1 for d in deg if d == 1), "d2": sum(1 for d in deg if d == 2),
        "d3": sum(1 for d in deg if d == 3), "d4p": sum(1 for d in deg if d >= 4),
        "mid_end2": sum(1 for v in range(n) if role_m[v] >= 1 and role_e[v] >= 2),
        "edges_mid_deg1": sum(1 for (i, j, k) in edges if deg[j] == 1),
        "parent_only": sum(1 for v in range(n) if role_e[v] >= 1 and role_m[v] == 0),
        "slack": 5 * n + 3 * m - 17 * tau, "D": 17 * alpha - 9 * n, "maxdeg": max(deg) if deg else 0,
        "comps": comps, "saturated": (m == n - 2), "edges_list": edges,
    }


class Writer:
    def __init__(self, path):
        self.f = gzip.open(path, "wt")
        self.seen = set()
        self.count = 0
        self.by_src = {}

    def add(self, S, src, extra=None):
        key = normalize(S)
        if key in self.seen:
            return False
        self.seen.add(key)
        row = features(sorted(S))
        row["set"] = sorted(S)
        row["src"] = src
        if extra:
            row.update(extra)
        self.f.write(json.dumps(row) + "\n")
        self.count += 1
        self.by_src[src] = self.by_src.get(src, 0) + 1
        return True

    def close(self):
        self.f.close()


def all_subsets(w, S, src, minsize=6):
    n = len(S)
    for r in range(minsize, n + 1):
        for c in itertools.combinations(S, r):
            w.add(list(c), src)


def random_set(n, rng):
    """one attempt: random saturated linear midpoint map -> exact solve -> exact (4,5) check. Returns ints or None."""
    m = random_linear_map(n, rng)
    ev = evaluate(m)
    if ev["is45"]:
        return sorted(to_integers(ev["vals"]))
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--per-n", type=int, default=500)
    ap.add_argument("--ns", type=int, nargs="*", default=[10, 12, 14, 16, 18])
    ap.add_argument("--n20-seconds", type=int, default=600)
    ap.add_argument("--subsets", type=int, default=200)
    ap.add_argument("--seed", type=int, default=757)
    ap.add_argument("--out", default="dataset.jsonl.gz")
    ap.add_argument("--skip-records", action="store_true")
    a = ap.parse_args()
    here = os.path.dirname(os.path.abspath(__file__))
    root = os.path.abspath(os.path.join(here, "..", ".."))
    w = Writer(os.path.join(here, a.out))
    rng = random.Random(a.seed)
    t0 = time.time()
    log = lambda s: print(f"[{time.time()-t0:7.1f}s] {s}", flush=True)
    A_base = [0, 136, 200, 243, 246, 249, 272, 286, 298, 323, 400, 528, 596, 1056]
    rec = json.load(open(os.path.join(root, "data", "small_records.json")))["sets"]
    # (a) all induced subsets of records
    srcs = [("A_base", A_base)] + [(f"rec{k}", v["set"]) for k, v in rec.items()]
    for name, S in srcs:
        S = sorted(S)
        if len(S) <= 14:
            all_subsets(w, S, "sub_" + name)
        log(f"{name} n={len(S)} rows so far {w.count}")
    # (b) random saturated sets
    stats = {}
    def run_n(n, quota=None, seconds=None):
        got = tries = 0
        t1 = time.time()
        while (quota is None or got < quota) and (seconds is None or time.time() - t1 < seconds):
            tries += 1
            S = random_set(n, rng)
            if S is None:
                continue
            if not w.add(S, f"rand{n}"):
                continue
            got += 1
            idx = list(range(n))
            seen_sub = 0
            for _ in range(a.subsets):
                r = rng.randint(6, n - 1)
                sub = sorted(rng.sample(S, r))
                if w.add(sub, f"randsub{n}"):
                    seen_sub += 1
            if got % 50 == 0:
                log(f"n={n} sets {got} tries {tries} rows {w.count}")
        stats[n] = (got, tries)
    for n in a.ns:
        run_n(n, quota=a.per_n)
    if a.n20_seconds:
        run_n(20, seconds=a.n20_seconds)
    w.close()
    json.dump({"rows": w.count, "by_src": w.by_src, "random_stats(got,tries)": stats, "seed": a.seed, "seconds": time.time() - t0},
              open(os.path.join(here, "generate_stats.json"), "w"), indent=1)
    log(f"done rows={w.count} {stats}")


if __name__ == "__main__":
    main()
