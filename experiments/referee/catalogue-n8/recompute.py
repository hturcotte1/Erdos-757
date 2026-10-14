"""Independent referee recomputation for experiments/20261014-0005-forbidden-n8 (NO e757 imports).

Method (all exact, Fractions / sympy):
  * A labeled configuration = list of edges (p, m, q): x_m = (x_p + x_q)/2, vertices are letters.
  * An order = permutation of the vertices; it is consistent with the labeling if every midpoint lies
    strictly between its two endpoints.  Rank-form pattern: edges (i,j,k) in ranks, sorted, canonical
    under reflection j -> n-1-j.
  * Verdict of a rank-form pattern:
      O  no strictly increasing solution of the AP equations (Fourier-Motzkin on the solution space,
         exact; certificate: integer combination of the equations that is a non-negative, non-zero
         combination of the gaps g_r = x_{r+1}-x_r).
      E  order-feasible, but some unlisted triple a<b<c has x_a+x_c-2x_b identically 0 on the solution
         space (certificate: coefficients y with sum_e y_e * eq_e = relation, via sympy).
      D  order-feasible, no forced extra AP, but some 4-set a<b<c<d has x_a+x_d-x_b-x_c identically 0
         (parallelogram = repeated difference), certificate as for E.
      R  otherwise; an explicit integer point is produced and verified exactly: strictly increasing,
         its set of 3-APs equals the pattern, every 4-subset has >= 5 distinct positive differences.
    Precedence O > E > D as in the deliverable.  Correctness of 'R': the strict-order region is a
    non-empty open subset of the solution space and the bad relations are finitely many proper
    hyperplanes of it, so a generic point avoids them; the script nevertheless exhibits one.
"""
import itertools, json, gzip, random, sys, os
from fractions import Fraction as F
from collections import Counter
import sympy

random.seed(12345)
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
OUT = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    OUT.append(s)


# ----------------------------------------------------------------------------- exact linear algebra
def rref(rows, ncols):
    R = [[F(x) for x in r] for r in rows]
    piv, r = [], 0
    for c in range(ncols):
        p = next((t for t in range(r, len(R)) if R[t][c] != 0), None)
        if p is None:
            continue
        R[r], R[p] = R[p], R[r]
        pv = R[r][c]
        R[r] = [x / pv for x in R[r]]
        for t in range(len(R)):
            if t != r and R[t][c] != 0:
                f = R[t][c]
                R[t] = [a - f * b for a, b in zip(R[t], R[r])]
        piv.append(c)
        r += 1
        if r == len(R):
            break
    return R[:r], piv


def nullspace(rows, ncols):
    R, piv = rref(rows, ncols) if rows else ([], [])
    free = [c for c in range(ncols) if c not in piv]
    basis = []
    for fc in free:
        v = [F(0)] * ncols
        v[fc] = F(1)
        for row, pc in zip(R, piv):
            v[pc] = -row[fc]
        basis.append(v)
    return basis


def dot(u, v):
    return sum(a * b for a, b in zip(u, v))


# ----------------------------------------------------------------------------- Fourier-Motzkin (strict, homogeneous)
def fm_point(ineqs, d):
    """ineqs: list of coefficient vectors c (len d) meaning c.t > 0.  Returns a rational t or None."""
    if any(all(x == 0 for x in c) for c in ineqs):
        return None
    if d == 0:
        return []
    pos = [c for c in ineqs if c[0] > 0]
    neg = [c for c in ineqs if c[0] < 0]
    zero = [c[1:] for c in ineqs if c[0] == 0]
    new = list(zero)
    for p in pos:
        for q in neg:
            new.append([p[0] * qq - q[0] * pp for pp, qq in zip(p[1:], q[1:])])
    rest = fm_point(new, d - 1)
    if rest is None:
        return None
    lows = [-dot(p[1:], rest) / p[0] for p in pos]          # t0 > low
    highs = [-dot(q[1:], rest) / q[0] for q in neg]         # t0 < high  (q0<0)
    lo = max(lows) if lows else None
    hi = min(highs) if highs else None
    if lo is None and hi is None:
        t0 = F(0)
    elif lo is None:
        t0 = hi - 1
    elif hi is None:
        t0 = lo + 1
    else:
        assert lo < hi, (lo, hi)
        t0 = (lo + hi) / 2
    return [t0] + rest


# ----------------------------------------------------------------------------- the oracle
def eq_rows(n, edges):
    rows = []
    for i, j, k in edges:
        r = [F(0)] * n
        r[i] += 1
        r[k] += 1
        r[j] -= 2
        rows.append(r)
    return rows


def gap_form(n, row):
    """Express a linear form sum row[v] x_v (with sum row = 0) in gaps g_r = x_{r+1}-x_r:
    coefficient of g_r is sum_{v>r} row[v]."""
    assert sum(row) == 0
    return [sum(row[v] for v in range(r + 1, n)) for r in range(n - 1)]


def farkas_certificate(n, edges):
    """Small integer y with sum_e y_e * eq_e = sum_r w_r g_r, w >= 0, w != 0 (proves no increasing point)."""
    rows = eq_rows(n, edges)
    gaps = [gap_form(n, r) for r in rows]
    m = len(edges)
    for B in (1, 2, 3, 4):
        for y in itertools.product(range(-B, B + 1), repeat=m):
            w = [sum(y[e] * gaps[e][r] for e in range(m)) for r in range(n - 1)]
            if all(x >= 0 for x in w) and any(x > 0 for x in w):
                return list(y), [int(x) for x in w]
    return None


def combination_certificate(n, edges, rel_vec):
    """Coefficients y (sympy Rationals) with sum_e y_e * eq_e == rel_vec, or None."""
    A = sympy.Matrix([[int(x) for x in r] for r in eq_rows(n, edges)]).T   # n x m
    b = sympy.Matrix([int(x) for x in rel_vec])
    try:
        sol, params = A.gauss_jordan_solve(b)
    except ValueError:
        return None
    sol = sol.subs({p: 0 for p in params})
    assert A * sol == b
    return list(sol)


def is_45(pts):
    for B in itertools.combinations(pts, 4):
        if len({abs(x - y) for x, y in itertools.combinations(B, 2)}) < 5:
            return False
    return True


def ap_set(pts):
    s = set(pts)
    pos = {x: i for i, x in enumerate(pts)}
    res = set()
    for x, y in itertools.combinations(pts, 2):
        if (x + y) % 2 == 0 and (x + y) // 2 in s and (x + y) // 2 not in (x, y):
            res.add(tuple(sorted((pos[x], pos[(x + y) // 2], pos[y]))))
    return res


def to_ints(x):
    import math
    den = 1
    for v in x:
        den = den * v.denominator // math.gcd(den, v.denominator)
    xs = [int(v * den) for v in x]
    m = min(xs)
    xs = [v - m for v in xs]
    g = 0
    for v in xs:
        g = math.gcd(g, v)
    return [v // max(g, 1) for v in xs]


def verdict(n, edges):
    """edges: rank-form (i,j,k).  Returns (letter, certificate)."""
    edges = sorted(tuple(e) for e in edges)
    rows = eq_rows(n, edges)
    N = nullspace(rows, n)                      # basis of solution space, x = sum t_j N_j
    d = len(N)
    ineqs = [[N[j][r + 1] - N[j][r] for j in range(d)] for r in range(n - 1)]
    t = fm_point(ineqs, d)
    if t is None:
        return "O", farkas_certificate(n, edges)
    listed = {frozenset(e) for e in edges}
    def vanishes(vec):
        return all(dot(vec, Nj) == 0 for Nj in N)
    for a, b, c in itertools.combinations(range(n), 3):
        if frozenset((a, b, c)) in listed:
            continue
        v = [F(0)] * n
        v[a] += 1; v[c] += 1; v[b] -= 2
        if vanishes(v):
            return "E", ((a, b, c), combination_certificate(n, edges, v))
    for a, b, c, dd in itertools.combinations(range(n), 4):
        v = [F(0)] * n
        v[a] += 1; v[dd] += 1; v[b] -= 1; v[c] -= 1
        if vanishes(v):
            return "D", ((a, b, c, dd), combination_certificate(n, edges, v))
    # realizable: exhibit a point
    base = [dot([Nj[v] for Nj in N], t) for v in range(n)]
    for trial in range(2000):
        if trial == 0:
            tt = t
        else:
            scale = F(1, 2 ** (1 + trial % 6))
            tt = [ti + scale * F(random.randint(-50, 50), 50) for ti in t]
        x = [sum(tt[j] * N[j][v] for j in range(d)) for v in range(n)]
        if any(x[r + 1] <= x[r] for r in range(n - 1)):
            continue
        pts = to_ints(x)
        if ap_set(pts) == {tuple(e) for e in edges} and is_45(pts):
            return "R", pts
    return "R?", None


# ----------------------------------------------------------------------------- orders of a labeling
def reflect(n, rf):
    return tuple(sorted((n - 1 - k, n - 1 - j, n - 1 - i) for i, j, k in rf))


def rank_form(perm, lab):
    """perm: dict vertex->rank; lab: list of (p, m, q).  None if inconsistent."""
    rf = []
    for p, m, q in lab:
        a, b, c = sorted((p, m, q), key=lambda v: perm[v])
        if b != m:
            return None
        rf.append((perm[a], perm[b], perm[c]))
    return tuple(sorted(rf))


def labeling_census(name, verts, lab, expect):
    n = len(verts)
    pats = {}
    for pr in itertools.permutations(range(n)):
        perm = dict(zip(verts, pr))
        rf = rank_form(perm, lab)
        if rf is None:
            continue
        rfc = min(rf, reflect(n, rf))
        if rfc not in pats:
            order = "".join(sorted(verts, key=lambda v: perm[v]))
            pats[rfc] = order
    res = {}
    for rfc, order in sorted(pats.items()):
        v, cert = verdict(n, rfc)
        res[rfc] = (v, cert, order)
    cnt = Counter(v for v, _, _ in res.values())
    say(f"\n== {name}: labeling {lab}  (vertices {''.join(verts)})")
    say(f"   distinct ordered patterns up to reflection: {len(res)}  verdicts {dict(cnt)}   expected {expect}")
    for rfc, (v, cert, order) in res.items():
        inv = {}
        say(f"   order {' '.join(order)}  rank-form {list(rfc)} : {v}  {fmt_cert(v, cert, order, rfc)}")
    ok = (len(res) == expect["total"]) and all(cnt.get(k, 0) == expect.get(k, 0) for k in "ROED")
    say(f"   MATCH: {ok}")
    return res, ok


def fmt_cert(v, cert, order, rfc):
    names = order
    if v == "O":
        if cert is None:
            return "(no small Farkas certificate found)"
        y, w = cert
        terms = " + ".join(f"({yi})*[{names[i]}+{names[k]}-2{names[j]}]" for yi, (i, j, k) in zip(y, rfc) if yi)
        gaps = " + ".join(f"{wi}*({names[r+1]}-{names[r]})" for r, wi in enumerate(w) if wi)
        return f"Farkas: {terms} = {gaps} > 0 but LHS = 0"
    if v in ("E", "D"):
        rel, y = cert
        if v == "E":
            a, b, c = rel
            relstr = f"x_{names[a]}+x_{names[c]}-2x_{names[b]} = 0 (unlisted AP {names[a]}{names[b]}{names[c]})"
        else:
            a, b, c, d = rel
            relstr = f"x_{names[a]}+x_{names[d]} = x_{names[b]}+x_{names[c]}  i.e. {names[b]}-{names[a]} = {names[d]}-{names[c]}"
        comb = " + ".join(f"({yi})*[{names[i]}+{names[k]}-2{names[j]}]" for yi, (i, j, k) in zip(y, rfc) if yi != 0)
        return f"forced: {relstr};  derivation: {comb}"
    if v == "R":
        return "realization " + ", ".join(f"{names[r]}={cert[r]}" for r in range(len(cert)))
    return str(cert)


def config_census(name, verts, edges, expect):
    """All vertex orders of an unlabeled configuration; rank forms up to reflection; verdict counts."""
    n = len(verts)
    pats = {}
    for pr in itertools.permutations(range(n)):
        perm = dict(zip(verts, pr))
        rf = []
        for e in edges:
            a, b, c = sorted(e, key=lambda v: perm[v])
            rf.append((perm[a], perm[b], perm[c]))
        rf = tuple(sorted(rf))
        rfc = min(rf, reflect(n, rf))
        pats.setdefault(rfc, None)
    cnt = Counter()
    res = {}
    for rfc in pats:
        v, cert = verdict(n, rfc)
        res[rfc] = v
        cnt[v] += 1
    say(f"\n== whole census {name}: {len(res)} ordered patterns, {dict(cnt)}   expected {expect}")
    ok = len(res) == expect["total"] and all(cnt.get(k, 0) == expect.get(k, 0) for k in "ROED")
    say(f"   MATCH: {ok}")
    return res, ok


def main():
    allok = True
    # configurations (vertex letters as in the README)
    TRI_E = [("a", "b", "c"), ("a", "d", "e"), ("b", "d", "f")]
    PASCH_E = [("a", "b", "c"), ("a", "d", "e"), ("b", "d", "f"), ("c", "e", "f")]
    C4_E = [("a", "b", "c"), ("a", "d", "e"), ("b", "f", "g"), ("d", "f", "h")]

    def lab(edges, mids):
        out = []
        for e, m in zip(edges, mids):
            p, q = [v for v in e if v != m]
            out.append((p, m, q))
        return out

    # ---- 3 forbidden + 3 realizable entries
    entries = [
        ("4.7 medial triangle (FORBIDDEN claimed)", "abcdef", lab(TRI_E, "cef"), {"total": 2, "O": 1, "D": 1}),
        ("8.15 medial 4-cycle (FORBIDDEN claimed)", "abcdefgh", lab(C4_E, "cegh"), {"total": 43, "O": 33, "D": 10}),
        ("10.6 Pasch K30 (FORBIDDEN claimed)", "abcdef", lab(PASCH_E, "adfc"), {"total": 1, "O": 1}),
        ("4.3 cyclic corner midpoints (REALIZABLE claimed)", "abcdef", lab(TRI_E, "adb"), {"total": 3, "R": 3}),
        ("4.6 one corner midpoint (REALIZABLE claimed)", "abcdef", lab(TRI_E, "aef"), {"total": 15, "R": 7, "O": 8}),
        ("10.5 Pasch (REALIZABLE claimed)", "abcdef", lab(PASCH_E, "adbc"), {"total": 3, "R": 1, "O": 2}),
    ]
    results = {}
    for name, verts, L, exp in entries:
        res, ok = labeling_census(name, list(verts), L, exp)
        results[name] = res
        allok &= ok

    # ---- whole censuses as in tests/test_forbidden_catalogue.py
    _, ok = config_census("TRIANGLE", "abcdef", TRI_E, {"total": 60, "R": 22, "O": 28, "D": 10}); allok &= ok
    _, ok = config_census("PASCH", "abcdef", PASCH_E, {"total": 15, "R": 1, "O": 13, "E": 1}); allok &= ok
    _, ok = config_census("TWO EDGES SHARING A VERTEX", "abcde", [("a", "b", "c"), ("a", "d", "e")],
                          {"total": 9, "R": 6, "O": 2, "D": 1}); allok &= ok
    _, ok = config_census("TWO DISJOINT EDGES", "abcdef", [("a", "b", "c"), ("d", "e", "f")],
                          {"total": 7, "R": 6, "O": 1}); allok &= ok

    # ---- Pasch realization {0,4,7,8,9,14}
    pts = [0, 4, 7, 8, 9, 14]
    aps = ap_set(pts)
    want = {(0, 1, 3), (0, 2, 5), (1, 4, 5), (2, 3, 4)}
    sid = max(len(S) for r in range(1, 7) for S in itertools.combinations(pts, r)
              if len({x + y for x, y in itertools.combinations_with_replacement(S, 2)}) == r * (r + 1) // 2)
    say(f"\n== Pasch realization {pts}: APs {sorted(aps)} == {sorted(want)}: {aps == want}; (4,5): {is_45(pts)}; h = {sid}")
    allok &= (aps == want and is_45(pts) and sid == 4)

    # ---- compare every order of the 6 labelings against catalogue.json.gz (data only, no e757)
    cat = json.load(gzip.open(os.path.join(REPO, "experiments/20261014-0005-forbidden-n8/catalogue.json.gz")))
    byrf = {}
    for c in cat["classes"]:
        for o in c["orders"]:
            rf = tuple(sorted(tuple(e) for e in o["rank_form"]))
            byrf[(c["n"], rf)] = o["verdict"]
    code = {"realizable": "R", "order-infeasible": "O", "forced extra AP": "E", "forced repeated difference": "D"}
    mism = 0
    tot = 0
    for name, res in results.items():
        for rfc, (v, _, _) in res.items():
            n = max(max(e) for e in rfc) + 1
            key = (n, rfc)
            if key not in byrf:
                key2 = (n, reflect(n, rfc))
                key = key2
            tot += 1
            if key not in byrf:
                say(f"   pattern {rfc} not found in catalogue"); mism += 1
            elif code[byrf[key]] != v:
                say(f"   MISMATCH {rfc}: mine {v}, catalogue {byrf[key]}"); mism += 1
    say(f"\n== per-order comparison with catalogue.json.gz: {tot} patterns, {mism} mismatches")
    allok &= mism == 0

    # ---- the 'forbidden in every order' injective labelings in the catalogue: list and medial check
    say("\n== injective labelings forbidden in every order (from catalogue.json.gz):")
    forb = []
    for c in cat["classes"]:
        if c["mids_injective"] and not any(o["verdict"] == "realizable" for o in c["orders"]):
            forb.append(c)
    hid_count = Counter(c["hid"] for c in forb)
    say(f"   count {len(forb)} by hid {dict(sorted(hid_count.items()))}")
    def has_medial_triangle(labeling):
        E = [(frozenset(e), m) for e, m in labeling]
        for (e1, m1), (e2, m2), (e3, m3) in itertools.combinations(E, 3):
            if len(e1 & e2) == 1 and len(e1 & e3) == 1 and len(e2 & e3) == 1 and len(e1 & e2 & e3) == 0:
                corners = (e1 & e2) | (e1 & e3) | (e2 & e3)
                if m1 not in corners and m2 not in corners and m3 not in corners:
                    return True
        return False
    for c in forb:
        say(f"   hid {c['hid']} n={c['n']} labeling {c['labeling']} orders {len(c['orders'])} "
            f"{dict(Counter(o['verdict'] for o in c['orders']))} medial-triangle: {has_medial_triangle(c['labeling'])}")

    # ---- total counts of the catalogue
    say(f"\n== catalogue: {len(cat['hypergraphs'])} configurations, {len(cat['classes'])} labelings, "
        f"{sum(c['mids_injective'] for c in cat['classes'])} injective")

    # ---- spot-check the n=8 core library (kind + minimality) with my oracle
    lib = json.load(open(os.path.join(REPO, "data/forbidden_ordered_n8.json")))
    cores = lib["cores"]
    say(f"\n== n=8 library: {len(cores)} cores, kinds {dict(Counter(c['kind'] for c in cores))}, "
        f"edge counts {dict(sorted(Counter(len(c['edges']) for c in cores).items()))}, "
        f"counts_by_n {lib['counts_by_n']}")
    sample = random.sample(cores, 40)
    bad = 0
    def forced(n, edges, kind, rel):
        rows = eq_rows(n, edges)
        if kind == "order":
            N = nullspace(rows, n)
            ineqs = [[Nj[r + 1] - Nj[r] for Nj in N] for r in range(n - 1)]
            return fm_point(ineqs, len(N)) is None
        v = [F(0)] * n
        if kind == "extra_ap":
            a, b, c = rel; v[a] += 1; v[c] += 1; v[b] -= 2
            if frozenset(rel) in {frozenset(e) for e in edges}:
                return False
        else:
            a, b, c, d = rel; v[a] += 1; v[d] += 1; v[b] -= 1; v[c] -= 1
        N = nullspace(rows, n)
        return all(dot(v, Nj) == 0 for Nj in N)
    for c in sample:
        n, kind, edges, rel = c["n"], c["kind"], [tuple(e) for e in c["edges"]], tuple(c.get("relation") or ())
        supp = {v for e in edges for v in e}
        ok = forced(n, edges, kind, rel) and supp == set(range(n))
        minimal = all(not forced(n, edges[:t] + edges[t + 1:], kind, rel) for t in range(len(edges)))
        linear = all(len(set(e1) & set(e2)) <= 1 for e1, e2 in itertools.combinations(edges, 2))
        if not (ok and minimal and linear):
            bad += 1
            say(f"   BAD core {c}: forced={ok} minimal={minimal} linear={linear}")
    say(f"   sampled {len(sample)} cores: {bad} failures (forced relation, minimality, linearity, full support)")
    allok &= bad == 0

    say(f"\nALL CHECKS MATCH: {allok}")
    with open(os.path.join(HERE, "recompute.out"), "w") as f:
        f.write("\n".join(OUT) + "\n")


if __name__ == "__main__":
    main()
