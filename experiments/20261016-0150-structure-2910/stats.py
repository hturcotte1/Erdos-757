"""Structural census of the 2,910 saturated extremal 14-point (4,5)-set classes (K45).
Run: nice -n 15 python3 experiments/20261016-0150-structure-2910/stats.py
All decisions are exact integer computations (bitmasks, gcd, set comparisons)."""
import gzip, json, itertools, os, sys, time
from math import gcd
from collections import Counter
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, ROOT)
from e757.core import ap_edges, is_45_set

N = 14
FULL = (1 << N) - 1
POP = np.array([bin(i).count("1") for i in range(1 << N)], dtype=np.int8)
IDX = np.arange(1 << N)


def components(verts, adj_edges):
    """number of connected components on `verts` using edge vertex-sets adj_edges"""
    verts = set(verts)
    parent = {v: v for v in verts}
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    for e in adj_edges:
        e = [v for v in e if v in verts]
        for a in e[1:]:
            ra, rb = find(e[0]), find(a)
            if ra != rb:
                parent[ra] = rb
    return len({find(v) for v in verts})


def two_colour_sizes(n_verts, pairs):
    """pairs form a graph on n_verts vertices; return (connected?, sorted class sizes) of the 2-colouring
    of the (assumed tree) graph; None if not bipartite."""
    adj = {v: [] for v in n_verts}
    for a, b in pairs:
        adj[a].append(b); adj[b].append(a)
    start = min(n_verts)
    col = {start: 0}
    stack = [start]
    while stack:
        u = stack.pop()
        for w in adj[u]:
            if w not in col:
                col[w] = 1 - col[u]; stack.append(w)
            elif col[w] == col[u]:
                return None
    if len(col) != len(n_verts):
        return ("disconnected", len(col))
    c1 = sum(col.values())
    return tuple(sorted((c1, len(n_verts) - c1)))


def analyse(rec):
    A = rec["set"]; E = [tuple(e) for e in rec["edges"]]
    assert len(A) == N and A == sorted(A) and len(E) == 12
    row = {}
    # consistency with the point set
    pos = {x: i for i, x in enumerate(A)}
    E2 = sorted((pos[a], pos[b], pos[c]) for a, b, c in ap_edges(A))
    row["edges_match_set"] = (E2 == sorted(E))
    row["is45"] = is_45_set(A)
    # degrees
    deg = [0] * N
    for e in E:
        for v in e:
            deg[v] += 1
    row["deg_seq"] = sorted(deg, reverse=True)
    row["max_deg"] = max(deg)
    row["n_deg1"] = deg.count(1)
    # independent sets by bitmask
    bad = np.zeros(1 << N, dtype=bool)
    for e in E:
        m = sum(1 << v for v in e)
        bad |= (IDX & m) == m
    indep = ~bad
    g = np.where(indep, POP, 0).astype(np.int8)
    for b in range(N):
        bit = 1 << b
        sel = IDX[(IDX & bit) != 0]
        g[sel] = np.maximum(g[sel], g[sel ^ bit])
    alpha = int(g[FULL])
    row["alpha"] = alpha
    row["alpha_plus1_count"] = int(np.count_nonzero(indep & (POP == alpha + 1)))
    ms = IDX[indep & (POP == alpha)]
    row["n_max_sidon"] = int(len(ms))
    # minimum transversals = complements of maximum independent sets (tau = 14-alpha)
    tau = N - alpha
    tv = ~bad  # placeholder to keep names clear
    trans_count = 0
    for s in ms:
        T = FULL ^ int(s)
        assert all(T & sum(1 << v for v in e) for e in E)
        trans_count += 1
    # independent check: count transversals of size tau directly (any set hitting all edges)
    emasks = [sum(1 << v for v in e) for e in E]
    hit = np.ones(1 << N, dtype=bool)
    for m in emasks:
        hit &= (IDX & m) != 0
    row["tau"] = tau
    row["n_min_transversals"] = int(np.count_nonzero(hit & (POP == tau)))
    row["no_transversal_smaller"] = (int(np.count_nonzero(hit & (POP < tau))) == 0)
    # universal vertices
    inter = FULL
    for s in ms:
        inter &= int(s)
    row["universal_vertices"] = bin(inter).count("1")
    # vertices in all min transversals / none
    # reflection
    refl = sorted((N - 1 - c, N - 1 - b, N - 1 - a) for a, b, c in E)
    row["symmetric"] = (refl == sorted(E))
    row["canon"] = min(tuple(sorted(E)), tuple(refl))
    # cut vertices
    weak = strong = 0
    for v in range(N):
        rest = [u for u in range(N) if u != v]
        shr = [tuple(u for u in e if u != v) for e in E]
        if components(rest, shr) > 1:
            weak += 1
        keep = [e for e in E if v not in e]
        if components(rest, keep) > 1:
            strong += 1
    row["cut_vertices_weak"] = weak      # edges shrunk to e\{v}
    row["cut_vertices_strong"] = strong  # edges through v deleted
    row["connected"] = components(range(N), E) == 1
    # sub-hypergraph alphas
    c13 = Counter(int(g[FULL ^ (1 << p)]) for p in range(N))
    row["h13_values"] = dict(c13)
    pairs7 = 0; pairs_vals = Counter()
    for p, q in itertools.combinations(range(N), 2):
        a = int(g[FULL ^ (1 << p) ^ (1 << q)])
        pairs_vals[a] += 1
        if a == 7:
            pairs7 += 1
    row["n_pairs_h12_eq7"] = pairs7
    row["h12_values"] = dict(pairs_vals)
    # G_L, G_R
    l = {}; r = {}
    for a, b, c in E:
        l[b] = a; r[b] = c
    row["saturated"] = sorted(l) == list(range(1, N - 1))
    GL = two_colour_sizes(set(range(0, N - 1)), [(l[j], j) for j in l])
    GR = two_colour_sizes(set(range(1, N)), [(j, r[j]) for j in r])
    row["GL_sizes"] = list(GL) if GL and GL[0] != "disconnected" else GL
    row["GR_sizes"] = list(GR) if GR and GR[0] != "disconnected" else GR
    # span
    g0 = 0
    for x in A:
        g0 = gcd(g0, x - A[0])
    row["gcd"] = g0
    row["max_coord"] = (A[-1] - A[0]) // g0
    gaps = tuple((A[i + 1] - A[i]) // g0 for i in range(N - 1))
    row["gaps"] = gaps
    row["set"] = A
    return row


def dist(rows, key):
    return dict(sorted(Counter(json.dumps(r[key]) if isinstance(r[key], (list, dict)) else r[key] for r in rows).items(), key=lambda kv: str(kv[0])))


def main():
    t0 = time.time()
    path = os.path.join(ROOT, "data", "census_n14_m12_classes.jsonl.gz")
    recs = [json.loads(s) for s in gzip.open(path, "rt")]
    rows = [analyse(r) for r in recs]
    S = {"n_classes": len(rows)}
    for key in ["edges_match_set", "is45", "alpha", "alpha_plus1_count", "tau", "no_transversal_smaller",
                "max_deg", "n_deg1", "n_max_sidon", "n_min_transversals", "universal_vertices",
                "symmetric", "cut_vertices_weak", "cut_vertices_strong", "connected", "saturated",
                "n_pairs_h12_eq7", "GL_sizes", "GR_sizes", "gcd", "h13_values", "h12_values"]:
        S[key] = dist(rows, key)
    S["deg_seq"] = dist(rows, "deg_seq")
    S["distinct_canon_patterns"] = len({r["canon"] for r in rows})
    S["classes_with_h12_eq7_subset"] = sum(1 for r in rows if r["n_pairs_h12_eq7"] > 0)
    mc = [r["max_coord"] for r in rows]
    S["max_coord_min"] = min(mc); S["max_coord_max"] = max(mc)
    S["max_coord_median"] = sorted(mc)[len(mc) // 2]
    S["n_distinct_gap_seqs"] = len({r["gaps"] for r in rows})
    S["n_distinct_gap_seqs_mod_reversal"] = len({min(r["gaps"], r["gaps"][::-1]) for r in rows})
    S["n_max_sidon_min"] = min(r["n_max_sidon"] for r in rows)
    S["n_max_sidon_max"] = max(r["n_max_sidon"] for r in rows)
    ab = [i for i, r in enumerate(rows) if r["set"] == [0, 136, 200, 243, 246, 249, 272, 286, 298, 323, 400, 528, 596, 1056]]
    S["A_base_row_index"] = ab[0] if ab else None
    if ab:
        S["A_base_row"] = {k: v for k, v in rows[ab[0]].items() if k not in ("canon", "gaps")}
    for r in rows:
        r["canon"] = list(r["canon"]); r["gaps"] = list(r["gaps"])
    S["runtime_s"] = round(time.time() - t0, 1)
    with open(os.path.join(HERE, "results.json"), "w") as f:
        json.dump({"summary": S, "rows": rows}, f)
    print(json.dumps(S, indent=1))


if __name__ == "__main__":
    main()
