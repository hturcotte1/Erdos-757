#!/usr/bin/env python3
"""Save a candidate (4,5)-set as a claim and judge it.

Usage:
  python3 scripts/new_claim.py --slug anneal16 --set "0,136,200,..." --notes "found by ..."
  python3 scripts/new_claim.py --slug x --set-file experiments/.../best.json   (a JSON list)

Writes results/claims/C###-<slug>.json only if the judge passes, adding claimed_h and a witness
Sidon subset. Prints the JUDGE line. Exit code 0 on pass.
"""
import argparse
import importlib.util
import itertools
import json
import re
import sys
from fractions import Fraction
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
CLAIMS = REPO / "results" / "claims"


def load_judge():
    spec = importlib.util.spec_from_file_location("frozen_judge", REPO / "judge" / "judge.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def witness(vals, h):
    """Find one maximum Sidon subset (3-AP-free subset of a weak Sidon set) by search."""
    A = sorted(vals)
    n = len(A)
    idx = {x: i for i, x in enumerate(A)}
    edges = [(i, idx[(A[i] + A[k]) / 2], k) for i in range(n) for k in range(i + 2, n)
             if (A[i] + A[k]) / 2 in idx]
    by_last = [[] for _ in range(n)]
    for e in edges:
        by_last[max(e)].append(sum(1 << v for v in e))
    found = []

    def rec(i, chosen, size):
        if found or size + (n - i) < h:
            return
        if size == h:
            found.append(chosen)
            return
        if i == n:
            return
        c2 = chosen | (1 << i)
        if all(m & c2 != m for m in by_last[i]):
            rec(i + 1, c2, size + 1)
        rec(i + 1, chosen, size)

    rec(0, 0, 0)
    return [A[i] for i in range(n) if found and (found[0] >> i) & 1]


def fmt(x):
    x = Fraction(x)
    return int(x) if x.denominator == 1 else f"{x.numerator}/{x.denominator}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--slug", required=True)
    ap.add_argument("--set", help="comma-separated values (ints or p/q)")
    ap.add_argument("--set-file", help="JSON file with a list of values")
    ap.add_argument("--notes", default="")
    a = ap.parse_args()
    if a.set_file:
        raw = json.loads(Path(a.set_file).read_text())
    elif a.set:
        raw = [s.strip() for s in a.set.split(",") if s.strip()]
    else:
        sys.exit("give --set or --set-file")
    vals = sorted(Fraction(str(x)) for x in raw)
    slug = re.sub(r"[^A-Za-z0-9-]+", "-", a.slug).strip("-")[:40] or "set"
    CLAIMS.mkdir(parents=True, exist_ok=True)
    nums = [int(m.group(1)) for p in CLAIMS.glob("C*.json") if (m := re.match(r"C(\d+)-", p.name))]
    cid = f"C{(max(nums) + 1) if nums else 1:03d}-{slug}"
    path = CLAIMS / f"{cid}.json"
    claim = {"id": cid, "type": "construction", "set": [fmt(x) for x in vals], "notes": a.notes}
    path.write_text(json.dumps(claim, indent=1))
    J = load_judge()
    s = J.judge_struct(path)
    if not s["ok"]:
        path.unlink()
        print(s["line"])
        print("(not saved)")
        sys.exit(1)
    claim["claimed_h"] = s["h"]
    claim["witness_sidon_subset"] = [fmt(x) for x in witness(vals, s["h"])]
    path.write_text(json.dumps(claim, indent=1))
    s2 = J.judge_struct(path)
    print(s2["line"])
    print(f"saved: {path.relative_to(REPO)}")
    sys.exit(0 if s2["ok"] else 1)


if __name__ == "__main__":
    main()
