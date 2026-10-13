#!/usr/bin/env python3
"""
FROZEN JUDGE for Erdos Problem #757 constructions. Do not edit.
(Protected by a hook and a deny rule; its SHA-256 is pinned in judge/judge.sha256 and checked by
scripts/status.py, scripts/preflight.sh and the tests.)

Independent of the e757 package. It checks the definitions with exact rational arithmetic:

  * (4,5)-set: every 4 distinct points determine >= 5 distinct absolute differences.
  * h(A): the largest Sidon subset, where S is Sidon iff all positive differences
          y - x (x < y in S) are distinct (equivalently: all sums x + y, x <= y, are distinct).
          Computed by branch and bound on 3-APs. This is valid because a (4,5)-set is weak Sidon,
          which the judge also checks. For n <= 30 it is cross-checked by a second search that
          uses only the definition of a Sidon set.

Usage (from anywhere):
  python3 judge/judge.py results/claims/C001-foo.json [more.json ...]
  python3 judge/judge.py --all            # every results/claims/*.json

Claim file format (JSON). The file name must be <id>.json:
  {"id": "C001-short-name",
   "type": "construction",
   "set": [0, 136, 200, ...],          # integers, or strings like "3/7" for exact rationals
   "claimed_h": 8,                     # optional: the largest Sidon subset size the author claims
   "witness_sidon_subset": [...],      # optional: a Sidon subset of the set
   "notes": "how it was found"}

Output, one verdict line per claim:
  JUDGE: PASS NEW-RECORD <id> n=.. h=.. ratio=..      (h/n < 4/7: beats the published upper bound)
  JUDGE: PASS NO-IMPROVEMENT <id> n=.. h=.. ratio=..
  JUDGE: FAIL <id> <reason>
Exit status 0 iff every claim passes.
"""
import itertools
import json
import sys
from fractions import Fraction
from pathlib import Path

RECORD = Fraction(4, 7)
MAX_N = 120
REPO = Path(__file__).resolve().parent.parent


def parse_set(raw):
    vals = [Fraction(str(x)) for x in raw]
    if len(set(vals)) != len(vals):
        raise ValueError("set has repeated elements")
    return sorted(vals)


def is_45(A):
    for q in itertools.combinations(A, 4):
        d = {abs(x - y) for x, y in itertools.combinations(q, 2)}
        if len(d) < 5:
            return False, [str(x) for x in q]
    return True, None


def is_sidon(S):
    diffs = [y - x for x, y in itertools.combinations(sorted(S), 2)]
    return len(diffs) == len(set(diffs))


def is_weak_sidon(A):
    sums = [x + y for x, y in itertools.combinations(A, 2)]
    return len(sums) == len(set(sums))


def max_sidon(A):
    """Exact largest Sidon subset by depth-first search on pair differences (definition only)."""
    n = len(A)
    diff_ids = {}
    pid = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            d = A[j] - A[i]
            if d not in diff_ids:
                diff_ids[d] = len(diff_ids)
            pid[i][j] = pid[j][i] = diff_ids[d]
    best = [0]
    chosen = []

    def rec(i, used):
        if len(chosen) + (n - i) <= best[0]:
            return
        if i == n:
            best[0] = len(chosen)
            return
        mask = 0
        ok = True
        for c in chosen:
            bit = 1 << pid[c][i]
            if used & bit or mask & bit:
                ok = False
                break
            mask |= bit
        if ok:
            chosen.append(i)
            rec(i + 1, used | mask)
            chosen.pop()
        rec(i + 1, used)

    rec(0, 0)
    return best[0]


def max_sidon_via_aps(A):
    """Exact largest Sidon subset for a WEAK SIDON set A.

    Elementary fact used (Ma-Tang Lemma 2.3, three-line proof): if all sums x+y with
    x<y in A are distinct, then a subset S is Sidon iff S contains no 3-term AP.
    (A failing Sidon relation u+v=x+y inside S cannot use 4 distinct elements, since A
    is weak Sidon, and with 3 distinct elements it must be a+c=2b.)
    So h(A) is the independence number of the 3-uniform hypergraph of 3-APs in A,
    computed per connected component by branch and bound with a packing bound."""
    n = len(A)
    idx = {x: i for i, x in enumerate(A)}
    edges = []
    for i in range(n):
        for k in range(i + 2, n):
            j = idx.get((A[i] + A[k]) / 2)
            if j is not None:
                edges.append((i, j, k))
    parent = list(range(n))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for i, j, k in edges:
        parent[find(i)] = find(j)
        parent[find(k)] = find(j)
    comps = {}
    for v in range(n):
        comps.setdefault(find(v), []).append(v)
    total = 0
    for verts in comps.values():
        vs = set(verts)
        cedges = [e for e in edges if e[0] in vs]
        total += _alpha_component(verts, cedges)
    return total


def _alpha_component(verts, edges):
    if not edges:
        return len(verts)
    deg = {v: 0 for v in verts}
    for e in edges:
        for v in e:
            deg[v] += 1
    order = sorted(verts, key=lambda v: -deg[v])  # branch on high-degree vertices first
    pos = {v: i for i, v in enumerate(order)}
    n = len(order)
    emask = []
    by_last = [[] for _ in range(n)]
    for e in edges:
        ps = sorted(pos[v] for v in e)
        m = (1 << ps[0]) | (1 << ps[1]) | (1 << ps[2])
        emask.append(m)
        by_last[ps[2]].append(m)
    full = (1 << n) - 1
    best = [0]

    def bound(chosen, i, size):
        und = full ^ ((1 << i) - 1)
        avail = chosen | und
        used = 0
        loss = 0
        for e in emask:
            if e & avail == e:
                u = e & und
                if not (u & used):
                    used |= u
                    loss += 1
        return size + (n - i) - loss

    def rec(i, chosen, size):
        if size + (n - i) <= best[0]:
            return
        if i == n:
            best[0] = size
            return
        if bound(chosen, i, size) <= best[0]:
            return
        c2 = chosen | (1 << i)
        if all(e & c2 != e for e in by_last[i]):
            rec(i + 1, c2, size + 1)
        rec(i + 1, chosen, size)

    rec(0, 0, 0)
    return best[0]


def judge_struct(path):
    """Structured verdict: dict(ok, tag, id, n, h, ratio, line)."""
    path = Path(path)
    out = {"ok": False, "tag": "FAIL", "id": path.stem, "n": None, "h": None, "ratio": None}

    def fail(msg):
        out["line"] = f"JUDGE: FAIL {out['id']} {msg}"
        return out

    try:
        claim = json.loads(path.read_text())
        cid = str(claim.get("id", path.stem))
        out["id"] = cid
        if cid != path.stem:
            return fail(f"the claim id must equal the file name (file is {path.name})")
        if claim.get("type") != "construction":
            return fail("type is not 'construction' (the judge only checks constructions)")
        A = parse_set(claim["set"])
        n = len(A)
        out["n"] = n
        if n < 4 or n > MAX_N:
            return fail(f"n={n} outside supported range 4..{MAX_N}")
        ok, bad = is_45(A)
        if not ok:
            return fail(f"not a (4,5)-set; quadruple {bad} has fewer than 5 distinct distances")
        if not is_weak_sidon(A):
            return fail("not weak Sidon (impossible for a genuine (4,5)-set)")
        h = max_sidon_via_aps(A)
        if n <= 30:  # independent cross-check straight from the Sidon definition
            h2 = max_sidon(A)
            if h2 != h:
                return fail(f"internal disagreement h_ap={h} h_direct={h2} (report this)")
        w = claim.get("witness_sidon_subset")
        if w is not None:
            W = parse_set(w)
            if not set(W) <= set(A) or not is_sidon(W):
                return fail("witness_sidon_subset is not a Sidon subset of the set")
            if len(W) != h:
                return fail(f"witness has size {len(W)} but the largest Sidon subset has size {h}")
        if "claimed_h" in claim and int(claim["claimed_h"]) != h:
            return fail(f"claimed_h={claim['claimed_h']} but the exact largest Sidon subset has size {h}")
        r = Fraction(h, n)
        tag = "NEW-RECORD" if r < RECORD else "NO-IMPROVEMENT"
        out.update(ok=True, tag=tag, h=h, ratio=r)
        out["line"] = (f"JUDGE: PASS {tag} {cid} n={n} h={h} ratio={r} ({float(r):.6f})"
                       f" vs 4/7={float(RECORD):.6f}")
        return out
    except Exception as e:  # noqa: BLE001
        return fail(f"could not be checked: {e}")


def judge(path):
    """Backward-compatible wrapper: returns (ok, verdict_line)."""
    s = judge_struct(path)
    return s["ok"], s["line"]


def main(argv):
    if not argv:
        print(__doc__)
        return 2
    paths = argv
    if argv == ["--all"]:
        paths = sorted(str(p) for p in (REPO / "results" / "claims").glob("*.json"))
        if not paths:
            print("JUDGE: no claim files in results/claims/")
            return 0
    all_ok = True
    for p in paths:
        ok, line = judge(p)
        print(line)
        all_ok &= ok
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
