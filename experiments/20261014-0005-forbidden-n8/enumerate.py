"""Exhaustive library of ordered midpoint patterns on n <= NMAX vertices and minimal forbidden cores.

Standing constraints (cheap combinatorial ones): each interior j is the midpoint of at most one
edge (i,j,k), i<j<k; linearity (two edges share <= 1 vertex).
Classification precedence: order-infeasible > forced extra AP > forced repeated difference > realizable.
Minimal cores: enumerated exhaustively as the patterns S with full support on n vertices such that
S forces a relation R (order-infeasibility, extra AP T not in S, or parallelogram relation on a 4-set)
and no S minus one edge forces R.  (Forced relations only involve vertices in supp(S), so every
minimal core appears at n = |supp|.)  Dedup: reflection j -> n-1-j.
Usage: python3 enumerate.py NMAX out.json [NMIN]   (NMIN: first n to enumerate; default 3)
"""
import itertools, json, sys, time
from collections import Counter

from e757.realizability import (order_feasible, forced_relations, is_forced, realize_exact)

NMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 7
OUT = sys.argv[2] if len(sys.argv) > 2 else "forbidden_ordered_n7.json"
NMIN = int(sys.argv[3]) if len(sys.argv) > 3 else 3


def patterns(n):
    """All linear midpoint-injective ordered patterns on n vertices (as sorted edge tuples)."""
    res = []
    def rec(j, edges, used):
        if j == n - 1:
            res.append(tuple(edges)); return
        rec(j + 1, edges, used)
        for i in range(j):
            for k in range(j + 1, n):
                prs = [(i, j), (j, k), (i, k)]
                if any(p in used for p in prs):
                    continue
                rec(j + 1, edges + [(i, j, k)], used | set(prs))
    rec(1, [], frozenset())
    return res


def reflect_edges(n, edges):
    return tuple(sorted((n - 1 - k, n - 1 - j, n - 1 - i) for i, j, k in edges))


def reflect_rel(n, rel):
    if rel[0] == "order":
        return rel
    return (rel[0], tuple(sorted(n - 1 - v for v in rel[1])))


def canon(n, edges, rel):
    a = (tuple(sorted(edges)), rel)
    b = (reflect_edges(n, edges), reflect_rel(n, rel))
    return min(a, b, key=repr)


def support(edges):
    return {v for e in edges for v in e}


def main():
    t0 = time.time()
    counts = {}
    cores = {}
    for n in range(NMIN, NMAX + 1):
        pats = patterns(n)
        cnt = Counter()
        feas = {}
        def feasible(edges):
            if edges not in feas:
                ok, _ = order_feasible(n, edges)
                assert ok is not None
                feas[edges] = ok
            return feas[edges]
        for edges in pats:
            if not feasible(edges):
                cnt["order-infeasible"] += 1
            else:
                fr = forced_relations(n, edges)
                if fr["extra_ap"]:
                    cnt["forced extra AP"] += 1
                elif fr["diff"]:
                    cnt["forced repeated difference"] += 1
                else:
                    cnt["realizable"] += 1
            # minimal cores (full support only)
            if support(edges) != set(range(n)) and edges:
                continue
            if not edges:
                continue
            subs = [tuple(e for e in edges if e != d) for d in edges]
            if not feasible(edges):
                if all(feasible(s) for s in subs):
                    cores[canon(n, edges, ("order",))] = n
                continue
            fr = forced_relations(n, edges)
            rels = [("extra_ap", t) for t in fr["extra_ap"]] + [("diff", q) for q in fr["diff"]]
            subfr = [forced_relations(n, s) for s in subs]
            for rel in rels:
                key = "extra_ap" if rel[0] == "extra_ap" else "diff"
                if all(rel[1] not in f[key] for f in subfr):
                    cores[canon(n, edges, rel)] = n
        counts[n] = dict(cnt, total=len(pats))
        print(n, counts[n], "cores so far", len(cores), f"{time.time()-t0:.1f}s", flush=True)
    core_list = []
    for (edges, rel), n in sorted(cores.items(), key=lambda kv: (kv[1], len(kv[0][0]), repr(kv[0]))):
        kind = rel[0]
        core_list.append({"n": n, "kind": kind, "edges": [list(e) for e in edges],
                          "relation": list(rel[1]) if kind != "order" else None})
    summary = Counter((c["n"], c["kind"]) for c in core_list)
    out = {"description": "Ordered linear midpoint-injective AP patterns, %d<=n<=%d: class counts and minimal forbidden cores "
                          "(edges (i,j,k): 2x_j=x_i+x_k, ranks 0..n-1; kind order = order-infeasible; "
                          "extra_ap relation (a,b,c): S forces an unlisted AP; diff relation (a,b,c,d): S forces "
                          "x_a+x_d=x_b+x_c). Dedup under reflection j->n-1-j." % (NMIN, NMAX),
           "counts_by_n": {str(k): v for k, v in counts.items()},
           "cores_by_n_kind": {f"{n}/{k}": v for (n, k), v in sorted(summary.items())},
           "n_cores": len(core_list), "cores": core_list}
    json.dump(out, open(OUT, "w"), indent=0)
    print("cores:", len(core_list), dict(summary))


main()
