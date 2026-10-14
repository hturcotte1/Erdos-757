"""Render catalogue.json (from catalogue.py) as Markdown tables, verifying every realization independently.
Usage: python3 gen_readme.py catalogue.json out.md"""
import json, sys
from collections import Counter, OrderedDict
from e757.core import ap_edges, is_45_set
import math, random
from fractions import Fraction
from e757.realizability import forbidden_core, realize_exact, order_feasible, _nullspace, _gap_rows

cat = json.load(open(sys.argv[1]))
OUT = sys.argv[2]
NAMES = {
    ((0, 1, 2),): "single edge", ((0, 1, 2), (0, 3, 4)): "two edges sharing a vertex",
    ((0, 1, 2), (0, 3, 4), (0, 5, 6)): "star of three edges (common vertex)",
    ((0, 1, 2), (0, 3, 4), (1, 5, 6)): "path of three edges",
    ((0, 1, 2), (0, 3, 4), (1, 3, 5)): "TRIANGLE (three edges pairwise meeting in three distinct vertices)",
    ((0, 1, 2), (0, 3, 4), (0, 5, 6), (1, 3, 7)): "triangle + pendant edge at a corner",
    ((0, 1, 2), (0, 3, 4), (0, 5, 6), (1, 3, 5)): "star of three edges + transversal edge (three triangles)",
    ((0, 1, 2), (0, 3, 4), (1, 5, 6), (2, 3, 7)): "triangle + pendant edge at an edge-private vertex",
    ((0, 1, 2), (0, 3, 4), (1, 5, 6), (3, 5, 7)): "4-cycle of edges (no triangle)",
    ((0, 1, 2), (0, 3, 4), (1, 5, 6), (2, 3, 5)): "two triangles sharing two edges",
    ((0, 1, 2), (0, 3, 4), (1, 3, 5), (2, 4, 5)): "PASCH (four edges on six vertices)",
}


def small_real(n, rf, trials=4000):
    """Search for a small integer realization (exact check by ap_edges / is_45_set); fallback realize_exact."""
    rf = [tuple(e) for e in rf]
    ok, c = order_feasible(n, rf)
    def prim(v):
        den = 1
        for a in v:
            den = den * a.denominator // math.gcd(den, a.denominator)
        w = [int(a * den) for a in v]
        g = 0
        for a in w:
            g = math.gcd(g, abs(a))
        return [a // g for a in w]
    g0 = prim(c["gaps"])
    basis = [prim(b) for b in _nullspace(_gap_rows(n, rf), n - 1)] if rf else []
    rnd = random.Random(1)
    best = None
    want = {frozenset(e) for e in rf}
    for tr in range(trials):
        t = rnd.randint(1, 6)
        g = [t * a for a in g0]
        for b in basis:
            r = rnd.randint(-3, 3)
            g = [x + r * y for x, y in zip(g, b)]
        if any(x <= 0 for x in g):
            continue
        d = 0
        for x in g:
            d = math.gcd(d, x)
        g = [x // d for x in g]
        vals = [0]
        for x in g:
            vals.append(vals[-1] + x)
        if best is not None and vals[-1] >= best[-1]:
            continue
        pos = {v: i for i, v in enumerate(vals)}
        got = {frozenset((pos[a], pos[b], pos[c])) for a, b, c in ap_edges(vals)}
        if got == want and is_45_set(vals):
            best = vals
    if best is None:
        r = realize_exact(n, rf)
        assert r[0]
        best = r[1]
    return best

L = lambda v: chr(97 + v)
KIND = {"realizable": "R", "order-infeasible": "O", "forced extra AP": "E", "forced repeated difference": "D"}


def lab_str(lab):
    return "; ".join(f"mid({L(e[0])},{L(e[2])})={L(m)}" if m == e[1] else
                     (f"mid({L(e[0])},{L(e[1])})={L(m)}" if m == e[2] else f"mid({L(e[1])},{L(e[2])})={L(m)}")
                     for e, m in lab)


def mid_str(e, m):
    o = [v for v in e if v != m]
    return f"mid({L(o[0])},{L(o[1])})={L(m)}"


def lab_str(lab):
    return "; ".join(mid_str(e, m) for e, m in lab)


def medial_triangle(lab):
    import itertools
    for (a, ma), (b, mb), (c, mc) in itertools.combinations(lab, 3):
        s = [set(a) & set(b), set(a) & set(c), set(b) & set(c)]
        if all(len(x) == 1 for x in s) and len(set.union(*s)) == 3:
            corners = set.union(*s)
            if not ({ma, mb, mc} & corners):
                return True
    return False


def medial_4cycle(lab):
    import itertools
    if len(lab) != 4:
        return False
    for p in itertools.permutations(lab):
        E = [set(x[0]) for x in p]
        ok = all(len(E[i] & E[(i + 1) % 4]) == 1 for i in range(4)) and not (E[0] & E[2]) and not (E[1] & E[3])
        if ok:
            corners = set.union(*[E[i] & E[(i + 1) % 4] for i in range(4)])
            if not ({x[1] for x in p} & corners):
                return True
    return False


def verify_realization(n, rf, vals):
    want = {frozenset(e) for e in rf}
    pos = {v: i for i, v in enumerate(vals)}
    got = {frozenset((pos[a], pos[b], pos[c])) for a, b, c in ap_edges(vals)}
    return vals == sorted(vals) and len(set(vals)) == n and got == want and is_45_set(vals)


def seq(order):
    return " ".join(L(v) for v in order)


def why(o):
    n = len(o["order"])
    rf = [tuple(e) for e in o["rank_form"]]
    inv = o["order"]
    nm = lambda r: L(inv[r])
    v = o["verdict"]
    if v == "order-infeasible":
        core = forbidden_core(n, rf, ("order",))
        return "O: no increasing point; minimal order-infeasible sub-pattern " + ", ".join(
            f"({nm(i)},{nm(j)},{nm(k)})" for i, j, k in core)
    if v == "forced extra AP":
        a, b, c = o["info"][1]
        return f"E: forces unlisted AP ({nm(a)},{nm(b)},{nm(c)})"
    if v == "forced repeated difference":
        (a, b), (c, d) = o["info"][1], o["info"][2]
        return f"D: forces x_{nm(b)}-x_{nm(a)} = x_{nm(d)}-x_{nm(c)}"
    return v


def main():
    lines = []
    large = []
    stats = []
    by_h = OrderedDict()
    for c in cat["classes"]:
        by_h.setdefault(c["hid"], []).append(c)
    for hid, cls in by_h.items():
        edges = cls[0]["edges"]
        n = cls[0]["n"]
        lines.append(f"### H{hid}: {NAMES[tuple(map(tuple, edges))]}  ({n} vertices, {len(edges)} edges)\n")
        lines.append("Edges: " + ", ".join("{" + ",".join(L(v) for v in e) + "}" for e in edges) +
                     f".  Labelings up to Aut(H): {len(cls)}.\n")
        lines.append("| # | labeling (midpoints) | midpoint-injective | orders | R | O | E | D | verdict |")
        lines.append("|---|---|---|---|---|---|---|---|---|")
        details = []
        for t, c in enumerate(cls):
            cnt = Counter(KIND[o["verdict"]] for o in c["orders"])
            tot = len(c["orders"])
            R = cnt["R"]
            if R:
                verdict = f"REALIZABLE in {R} of {tot} orders"
            else:
                kinds = "/".join(k for k in "OED" if cnt[k])
                verdict = f"FORBIDDEN in every order ({kinds})"
            reason = ""
            if not c["mids_injective"]:
                reason = "two edges share a midpoint m: x_p+x_q = 2m = x_r+x_s, a parallelogram"
            elif R == 0:
                if medial_triangle(c["labeling"]):
                    reason = "contains a medial triangle (K31)"
                elif medial_4cycle(c["labeling"]):
                    reason = "medial 4-cycle: Varignon, x_c+x_h = x_e+x_g"
                elif all(o["verdict"] == "order-infeasible" and len(forbidden_core(n, [tuple(e) for e in o["rank_form"]], ("order",))) == 2
                         for o in c["orders"]):
                    reason = "every order violates monotone midpoints (K30)"
                else:
                    reason = "see orders"
            verdict += (" -- " + reason) if reason else ""
            lines.append(f"| {hid}.{t+1} | {lab_str(c['labeling'])} | {'yes' if c['mids_injective'] else 'no'} | {tot} | "
                         f"{R} | {cnt['O']} | {cnt['E']} | {cnt['D']} | {verdict} |")
            stats.append({"hid": hid, "idx": t + 1, "n": n, "labeling": lab_str(c["labeling"]), "orders": tot,
                          "R": R, "O": cnt["O"], "E": cnt["E"], "D": cnt["D"], "injective": c["mids_injective"]})
            # details
            d = [f"**{hid}.{t+1}** `{lab_str(c['labeling'])}`"]
            realized = [o for o in c["orders"] if o["verdict"] == "realizable"]
            full = n <= 6
            big = []   # details for the long file
            show = c["orders"] if full else (realized[:1] if realized else c["orders"][:3])
            for o in show:
                inv = o["order"]
                if o["verdict"] == "realizable":
                    vals = small_real(n, o["rank_form"])
                    assert verify_realization(n, o["rank_form"], vals), (hid, t)
                    d.append(f"- order `{seq(inv)}` : R  realization " + ", ".join(
                        f"{L(inv[r])}={vals[r]}" for r in range(n)))
                else:
                    d.append(f"- order `{seq(inv)}` : " + why(o))
            if not full:
                d.append(f"- ({tot} orders in total; first realizable shown{'' if realized else ', none realizable: first 3 orders shown'})")
            details.append("\n".join(d))
        lines.append("")
        if n <= 6:
            lines.extend(x + "\n" for x in details)
        else:
            large.append(f"### H{hid}: {NAMES[tuple(map(tuple, edges))]} ({n} vertices): orders\n")
            large.append("Edges: " + ", ".join("{" + ",".join(L(v) for v in e) + "}" for e in edges) + ".\n")
            large.extend(x + "\n" for x in details)
    open(OUT, "w").write("\n".join(lines))
    open(OUT.replace(".md", "_orders_7_8_vertices.md"), "w").write("\n".join(large))
    json.dump(stats, open(OUT + ".stats.json", "w"), indent=0)


main()
