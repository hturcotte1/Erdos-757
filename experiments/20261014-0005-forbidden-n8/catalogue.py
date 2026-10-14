"""Catalogue of midpoint labelings x orders for small connected linear 3-uniform configurations.

For every connected linear 3-graph H with 1..4 edges on <= 8 vertices (up to isomorphism), every
midpoint labeling (one midpoint per edge, up to Aut(H)), every vertex order consistent with the
labeling (midpoint strictly between its endpoints; orders identified up to reflection and up to
Aut(H), i.e. distinct rank-form patterns), the verdict of e757.realizability.realize_exact.
Usage: python3 catalogue.py out.json
"""
import itertools, json, sys, time
from collections import Counter, defaultdict
import networkx as nx
from networkx.algorithms.isomorphism import GraphMatcher

from e757.realizability import realize_exact

OUT = sys.argv[1] if len(sys.argv) > 1 else "catalogue.json"
VMAX, EMAX = 8, 4


def inc_graph(edges):
    G = nx.Graph()
    for t, e in enumerate(edges):
        G.add_node(("e", t), k=1)
        for v in e:
            G.add_node(("v", v), k=0)
            G.add_edge(("e", t), ("v", v))
    return G


def iso(e1, e2):
    return GraphMatcher(inc_graph(e1), inc_graph(e2), node_match=lambda a, b: a["k"] == b["k"]).is_isomorphic()


def gen_hypergraphs():
    levels = {1: [((0, 1, 2),)]}
    for ne in range(2, EMAX + 1):
        found = []
        for edges in levels[ne - 1]:
            nv = max(v for e in edges for v in e) + 1
            for r in (1, 2, 3):          # new edge uses r old vertices and 3-r new ones
                if nv + 3 - r > VMAX:
                    continue
                for old in itertools.combinations(range(nv), r):
                    new = tuple(old) + tuple(range(nv, nv + 3 - r))
                    if any(len(set(new) & set(e)) > 1 for e in edges):
                        continue
                    cand = tuple(edges) + (new,)
                    if not any(len(c) == len(cand) and iso(c, cand) for c in found):
                        found.append(cand)
        levels[ne] = found
    return [e for ne in levels for e in levels[ne]]


def automorphisms(edges):
    es = {frozenset(e) for e in edges}
    GM = GraphMatcher(inc_graph(edges), inc_graph(edges), node_match=lambda a, b: a["k"] == b["k"])
    auts = []
    for m in GM.isomorphisms_iter():
        auts.append({v[1]: w[1] for v, w in m.items() if v[0] == "v"})
    return auts


def reflect(n, edges):
    return tuple(sorted((n - 1 - k, n - 1 - j, n - 1 - i) for i, j, k in edges))


def main():
    t0 = time.time()
    hgs = gen_hypergraphs()
    print(len(hgs), "hypergraphs", flush=True)
    cache = {}
    out = []
    for hid, edges in enumerate(hgs):
        nv = max(v for e in edges for v in e) + 1
        auts = automorphisms(edges)
        # group: labeling-class -> {rankform -> perm representative}
        classes = defaultdict(dict)
        for perm in itertools.permutations(range(nv)):   # perm[v] = rank of vertex v
            rf = []
            mids = {}
            for e in edges:
                a, b, c = sorted(e, key=lambda v: perm[v])
                rf.append((perm[a], perm[b], perm[c]))
                mids[frozenset(e)] = b
            rf = tuple(sorted(rf))
            rfc = min(rf, reflect(nv, rf))
            # canonical labeling under Aut(H)
            best = None
            for au in auts:
                lab = tuple(sorted((tuple(sorted(au[v] for v in e)), au[mids[frozenset(e)]]) for e in edges))
                if best is None or lab < best:
                    best = lab
            d = classes[best]
            if rfc not in d:
                d[rfc] = perm
        for lab, pats in sorted(classes.items()):
            rec = {"hid": hid, "n": nv, "edges": [list(e) for e in edges], "labeling": [[list(e), m] for e, m in lab],
                   "mids_injective": len({m for _, m in lab}) == len(lab), "orders": []}
            for rfc, perm in sorted(pats.items()):
                inv = sorted(range(nv), key=lambda v: perm[v])   # inv[rank] = vertex
                if rfc not in cache:
                    if rec["mids_injective"] or True:
                        cache[rfc] = realize_exact(nv, list(rfc))
                res = cache[rfc]
                if res[0]:
                    kind, info = "realizable", res[1]
                else:
                    kind = res[1]
                    info = res[2] if len(res) > 2 else None
                    if isinstance(info, dict):
                        info = None
                    else:
                        info = list(info) if info is not None else None
                rec["orders"].append({"order": inv, "rank_form": [list(e) for e in rfc], "verdict": kind,
                                      "info": json.loads(json.dumps(info, default=list))})
            out.append(rec)
        print(hid, edges, "classes", len(classes), "patterns", sum(len(v) for v in classes.values()),
              f"{time.time()-t0:.0f}s", flush=True)
    json.dump({"hypergraphs": [list(map(list, h)) for h in hgs], "classes": out}, open(OUT, "w"), indent=0)


main()
