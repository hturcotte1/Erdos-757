"""Hunt: realizable extremal 15-point sets (alpha<=9, m in 9..12) + exact one-point extension test.
usage (repo root, PYTHONPATH=.):
  python3 experiments/.../hunt.py dfs  <hours> [seed]   # produce abstract patterns -> pats/
  python3 experiments/.../hunt.py work <hours>          # realize + extension test -> data/ext15_sets.jsonl, results
"""
import sys, os, json, random, time, subprocess, itertools, math, glob, gzip
from e757 import ordered_dfs_split as S
HERE = os.path.dirname(os.path.abspath(__file__))
PATS = os.path.join(HERE, "pats"); DATA = os.path.join(HERE, "data")
N = 15

# ---------------------------------------------------------------- DFS producer
def children(m, pre, depth):
    """surviving nodes at level depth (choices at midpoints 1..depth) below the prefix string pre"""
    cmd = [S.BIN] + S._base_args(N, 9, m, False) + ["mode=prefixes", "depth=%d" % depth]
    if pre: cmd.append("pre=" + pre)
    out = subprocess.run(cmd, capture_output=True, text=True).stdout
    return [l.split()[1] for l in out.splitlines() if l.startswith("PRE ")]

def pre_edges(pre):
    E = []
    for j, tok in enumerate(pre.split(","), start=1):
        if tok != "x":
            i, k = map(int, tok.split("-")); E.append((i, j, k))
    return E

PD = 5

def dfs(hours, seed=1, D=8):
    from e757.realizability import order_feasible
    rnd = random.Random(seed)
    top = {m: S.list_prefixes(N, 9, m, 3) for m in (9, 10, 11, 12)}
    print({m: len(v) for m, v in top.items()}, flush=True)
    t_end = time.time() + hours * 3600
    CAP = {11: 300, 12: 100, 10: 400, 9: 400}
    TL = {11: 20, 12: 10, 10: 60, 9: 60}
    cyc = 0; cnt = 0; pool = {m: {} for m in top}; last_read = 0
    while time.time() < t_end:
        cyc += 1
        m = [12, 11, 12, 11, 12, 11, 12, 11, 9, 10][cyc % 10] if True else 12
        if cyc % 20 == 1 and os.path.exists(os.path.join(DATA, "attempts.jsonl")):
            pool = {mm: {} for mm in top}
            for l in open(os.path.join(DATA, "attempts.jsonl")):
                try: r = json.loads(l)
                except Exception: continue
                if r.get("prefix") and r["realizable"] > 0:
                    k5 = ",".join(r["prefix"].split(",")[:PD])
                    pool[r["m"]][k5] = pool[r["m"]].get(k5, 0) + r["realizable"]
        if pool[m] and rnd.random() < 0.7:
            ks = list(pool[m]); pre = rnd.choices(ks, weights=[pool[m][k] ** 0.5 for k in ks])[0]; d = PD
        else:
            pre = rnd.choice(top[m]); d = 3
        dd = max(d, rnd.choice([D - 1, D, D + 1]))
        while d < dd:
            ch = children(m, pre, d + 1)
            ch = [c for c in ch if not fast_infeasible(pre_edges(c))]
            if not ch: pre = None; break
            pre = rnd.choice(ch); d += 1
        if pre is None: continue
        cmd = ["nice", "-n", "5", S.BIN] + S._base_args(N, 9, m, True) + ["mode=enum", "pre=" + pre, "tl=%g" % TL[m]]
        p = subprocess.run(cmd, capture_output=True, text=True)
        sols = [l[4:] for l in p.stdout.splitlines() if l.startswith("SOL")]
        done = [l for l in p.stdout.splitlines() if l.startswith("DONE")][-1]
        st = dict(kv.split("=") for kv in done.split()[1:])
        tot = len(sols)
        if tot > CAP[m]: sols = rnd.sample(sols, CAP[m])
        if not sols: continue
        cnt += 1
        base = os.path.join(PATS, "r_m%d_%06d_s%d" % (m, cnt, seed))
        with open(base + ".tmp", "w") as f:
            f.write(json.dumps({"m": m, "prefix": pre, "tl": TL[m], "nodes": int(st["nodes"]),
                                "timed_out": int(st["timed_out"]), "found": tot, "kept": len(sols)}) + "\n")
            for x in sols: f.write(x + "\n")
        os.replace(base + ".tmp", base + ".pat")
        print(time.strftime("%H:%M:%S"), "m", m, "pre", pre, "found", tot, "kept", len(sols), "timed_out", st["timed_out"], flush=True)

# ---------------------------------------------------------------- analysis
def refl(edges):
    return sorted((N - 1 - k, N - 1 - j, N - 1 - i) for i, j, k in edges)

def canon(edges):
    a = sorted(tuple(e) for e in edges); b = refl(a)
    return tuple(min(a, b))

def prim(vals):
    v = sorted(vals); v = [x - v[0] for x in v]
    g = 0
    for x in v: g = math.gcd(g, x)
    return [x // g for x in v]

def sidon9(vals, edges):
    """edges: list of (i,j,k) rank triples. returns list of bitmasks of all 3-AP-free 9-subsets and alpha."""
    em = [(1 << i) | (1 << j) | (1 << k) for i, j, k in edges]
    # alpha via enumeration of independent sets by size
    best = 0; res = {}
    ind = [0]  # all independent sets bitmask, built incrementally by vertex
    sets = [0]
    for v in range(N):
        bv = 1 << v
        new = []
        mv = [e for e in em if e >> v & 1 and e < (1 << (v + 1))]  # edges whose max vertex is v
        for s in sets:
            c = s | bv
            if all(e & c != e for e in mv): new.append(c)
        sets += new
    cnt = {}
    for s in sets:
        k = bin(s).count("1"); cnt[k] = cnt.get(k, 0) + 1
    alpha = max(cnt)
    return alpha, [s for s in sets if bin(s).count("1") == alpha]

def diffs_ok(a, b, c, x):
    d = {abs(a - b), abs(a - c), abs(a - x), abs(b - c), abs(b - x), abs(c - x)}
    return len(d) >= 5

def extensions(V, smax):
    """V: 15 doubled-integers (even). candidates x forming 3-AP with two points. Returns list of (x, pairs_in_AP, admissible)."""
    Vs = set(V); cands = set()
    for a, b in itertools.combinations(V, 2):
        for x in ((a + b) // 2, 2 * a - b, 2 * b - a):
            if x not in Vs: cands.add(x)
    triples = list(itertools.combinations(V, 3))
    out = []
    for x in sorted(cands):
        if not all(diffs_ok(a, b, c, x) for a, b, c in triples): continue
        pairs = []
        for a, b in itertools.combinations(range(N), 2):
            va, vb = V[a], V[b]
            if 2 * x == va + vb or 2 * va == x + vb or 2 * vb == x + va: pairs.append((a, b))
        out.append((x, pairs))
    return out

def covers(smasks, maxsz):
    """abstract necessary condition: pair sets G (size<=maxsz) such that every max Sidon set contains a pair of G.
    returns (min size or None, number of minimal covers found up to cap, list of up to 50 covers)"""
    pm = {}
    for a, b in itertools.combinations(range(N), 2):
        pb = (1 << a) | (1 << b)
        pm[(a, b)] = sum(1 << t for t, s in enumerate(smasks) if s & pb == pb)
    full = (1 << len(smasks)) - 1
    found = set()
    def rec(cov, G, d):
        if cov == full:
            found.add(frozenset(G)); return
        if d == 0: return
        t = next(t for t in range(len(smasks)) if not cov >> t & 1)
        s = smasks[t]; vs = [v for v in range(N) if s >> v & 1]
        for a, b in itertools.combinations(vs, 2):
            if (a, b) in G: continue
            rec(cov | pm[(a, b)], G + [(a, b)], d - 1)
    rec(0, [], maxsz)
    # minimal ones
    fl = sorted(found, key=len); mins = []
    for g in fl:
        if not any(h < g for h in mins): mins.append(g)
    return (min((len(g) for g in mins), default=None), len(mins), [sorted(g) for g in mins[:50]])

def cover_ext(m, E, covs):
    """abstract one-point extensions: for each minimal cover G and each rank position of x, build the 16-point pattern,
    prefilter (linear, midpoint-injective), then exact realization. Returns (n_patterns, n_prefiltered, n_realizable, list of sets)."""
    from e757.realizability import realize_exact
    from e757.core import is_45_set, alpha
    tested = real = 0; sets = []; npat = 0
    for G in covs:
        for r in range(16):
            sh = lambda i: i if i < r else i + 1
            edges = [(sh(i), sh(j), sh(k)) for i, j, k in E]
            for a, b in G:
                a2, b2 = sh(a), sh(b)
                if r < a2: edges.append((r, a2, b2))
                elif r < b2: edges.append((a2, r, b2))
                else: edges.append((a2, b2, r))
            npat += 1
            if len({e[1] for e in edges}) < len(edges): continue
            if any(len(set(e) & set(f)) > 1 for e, f in itertools.combinations(edges, 2)): continue
            tested += 1
            res = realize_exact(16, sorted(edges))
            if res[0]:
                real += 1; V = prim(res[1])
                sets.append({"G": [list(p) for p in G], "pos": r, "set": V, "h": alpha(V), "is45": bool(is_45_set(V))})
    return npat, tested, real, sets

nrec_extra = []

def analyse(m, edges, vals):
    from e757.core import ap_edges, is_45_set
    V = prim(vals)
    assert is_45_set(V)
    idx = {x: i for i, x in enumerate(V)}
    E = sorted((idx[a], idx[b], idx[c]) for a, b, c in ap_edges(V))
    assert E == sorted(tuple(e) for e in edges), "AP set mismatch"
    alpha, smasks = sidon9(V, E)
    assert alpha == 9
    deg = [sum(1 for e in E if v in e) for v in range(N)]
    inter = (1 << N) - 1
    for s in smasks: inter &= s
    universal = [v for v in range(N) if inter >> v & 1]
    V2 = [2 * x for x in V]
    ext = extensions(V2, smasks)
    best = None; nrec = 0; minh = 10; recs = []
    degs_best = None
    for x, pairs in ext:
        # h(B+x)=9 iff every max Sidon 9-set of B contains a pair forming an AP with x
        ok = all(any((s >> a & 1) and (s >> b & 1) for a, b in pairs) for s in smasks)
        if ok:
            nrec += 1; recs.append((x, pairs)); minh = 9
        else:
            if best is None or len(pairs) > best: best = len(pairs)
    cm = covers(smasks, 14 - m)
    r = {"m": m, "deg_seq": sorted(deg, reverse=True), "n_max_sidon": len(smasks), "universal": universal,
         "n_ext_admissible": len(ext), "min_h_ext": minh if ext else None,
         "ext_degx_dist": dict(sorted(__import__("collections").Counter(len(p) for _, p in ext).items())),
         "cover_min": cm[0], "n_min_covers": cm[1], "covers": cm[2], "n_record_ext": nrec}
    if cm[0] is not None:
        npat, tested, real, sets = cover_ext(m, E, [[tuple(p) for p in g] for g in cm[2]])
        r["cover_ext"] = {"patterns": npat, "prefiltered": tested, "realizable": real, "sets": sets[:5]}
        for q in sets:
            if q["h"] <= 9 and q["is45"]:
                nrec_extra.append(q)
    return r, V, E, recs

def fast_infeasible(edges):
    """float LP prefilter (heuristic): True if no g >= 1 with E g = 0 (gap system); only used to skip hopeless patterns."""
    import numpy as np
    from scipy.optimize import linprog
    from e757.realizability import _gap_rows
    if not edges: return False
    A = np.array(_gap_rows(N, edges), dtype=float)
    r = linprog(np.zeros(N - 1), A_eq=A, b_eq=np.zeros(len(edges)), bounds=[(1, None)] * (N - 1), method="highs")
    return r.status == 2

def work(hours):
    from e757.realizability import realize_exact
    t_end = time.time() + hours * 3600
    seen = set()
    donef = set(os.path.basename(f) for f in glob.glob(os.path.join(DATA, "done_*.flag")))
    out = open(os.path.join(DATA, "ext15_sets.jsonl"), "a")
    stats = open(os.path.join(DATA, "attempts.jsonl"), "a")
    if os.path.exists(os.path.join(DATA, "seen.txt")):
        seen = set(open(os.path.join(DATA, "seen.txt")).read().split())
    seenf = open(os.path.join(DATA, "seen.txt"), "a")
    idle = 0
    while time.time() < t_end:
        files = sorted(glob.glob(os.path.join(PATS, "*.pat")))
        files = [f for f in files if os.path.basename(f) + ".done" not in donef]
        if not files:
            if idle > 3 and not os.path.exists(os.path.join(HERE, "dfs_alive")): break
            idle += 1; time.sleep(20); continue
        idle = 0
        f = files[0]
        lines = open(f).read().splitlines()
        hdr = json.loads(lines[0])
        m = hdr["m"]
        npat = nreal = 0; reasons = {}
        for l in lines[1:]:
            e = [tuple(map(int, t.split(","))) for t in l.split()[1:]]
            c = canon(e); key = json.dumps(c, separators=(",", ":"))
            if key in seen: continue
            seen.add(key); seenf.write(key + "\n"); seenf.flush()
            npat += 1
            if fast_infeasible(e):
                reasons["order-infeasible(fast-LP)"] = reasons.get("order-infeasible(fast-LP)", 0) + 1; continue
            r = realize_exact(N, e)
            if not r[0]:
                reasons[r[1]] = reasons.get(r[1], 0) + 1; continue
            nreal += 1
            rec, V, E, recs = analyse(m, e, r[1])
            rec["set"] = V; rec["edges"] = E; rec["src"] = os.path.basename(f)
            out.write(json.dumps(rec) + "\n"); out.flush()
            if rec["n_record_ext"] or nrec_extra:
                cand = sorted(set(V2 for V2 in [x for x in []]))
                Cs = [prim([2 * v for v in V] + [x]) for x, pairs in recs] + [q["set"] for q in nrec_extra]
                for C in Cs:
                    pairs = None
                    json.dump({"set": C, "base": V, "pairs": pairs}, open(os.path.join(HERE, "RECORD_CANDIDATE.json"), "w"))
                    print("RECORD CANDIDATE", C, flush=True)
                    pr = subprocess.run(["python3", "scripts/new_claim.py", "--slug", "ext15-record", "--set", ",".join(map(str, C)),
                                         "--notes", "one-point extension of an extremal 15-point set"], capture_output=True, text=True)
                    print(pr.stdout, pr.stderr, flush=True)
                open(os.path.join(HERE, "STOP"), "w").write("record\n")
                return
        stats.write(json.dumps({"file": os.path.basename(f), "m": m, "found": hdr["found"], "new": npat, "realizable": nreal, "fail": reasons, "prefix": hdr.get("prefix"),
                                "timed_out": hdr["timed_out"]}) + "\n"); stats.flush()
        donef.add(os.path.basename(f) + ".done")
        open(os.path.join(DATA, "done_" + os.path.basename(f) + ".flag"), "w").write("")
        print(time.strftime("%H:%M:%S"), os.path.basename(f), "new", npat, "real", nreal, flush=True)

if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "dfs":
        open(os.path.join(HERE, "dfs_alive"), "w").write("1")
        try: dfs(float(sys.argv[2]), int(sys.argv[3]) if len(sys.argv) > 3 else 1, int(sys.argv[4]) if len(sys.argv) > 4 else 8)
        finally: os.remove(os.path.join(HERE, "dfs_alive"))
    elif cmd == "work": work(float(sys.argv[2]))
