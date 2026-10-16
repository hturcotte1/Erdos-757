"""Referee L003 round 2: set-level comparison of my saturated classes (satcheck output) with the census realized sets
(read as DATA only) and, optionally, with the round-1 referee's output.  No imports from e757/ or judge/.
usage: python3 compare.py N F MYFILE[.gz] [--r1 ROUND1FILE[.gz]]
"""
import sys, os, json, gzip, glob, math
from fractions import Fraction

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
CENSUS = os.path.join(ROOT, "experiments", "20261014-1430-small-counts")


def opn(p):
    return gzip.open(p, "rt") if p.endswith(".gz") else open(p)


def canon(vals):
    """affine normal form: sort, translate to min 0, scale to a primitive integer vector, lexicographic min with reflection."""
    v = sorted(Fraction(x) for x in vals)
    lo = v[0]
    v = [x - lo for x in v]
    den = 1
    for x in v:
        den = den * x.denominator // math.gcd(den, x.denominator)
    w = [int(x * den) for x in v]
    g = 0
    for x in w:
        g = math.gcd(g, x)
    w = [x // g for x in w]
    r = sorted(w[-1] - x for x in w)
    return tuple(min(w, r))


def mine(path, n, f):
    out, hh = set(), {}
    for line in opn(path):
        if not line.startswith("S "):
            continue
        p = line.split()
        h = int(p[1]); vals = tuple(int(x) for x in p[2:])
        assert len(vals) == n
        assert canon(vals) == vals, "my output not in canonical form"
        hh[h] = hh.get(h, 0) + 1
        if h == f:
            assert vals not in out, "duplicate class in my output"
            out.add(vals)
    return out, hh


def census(n):
    sets, nrec = set(), 0
    if n <= 10:
        files = [os.path.join(CENSUS, "results", "n%d_m%d_real.json.gz" % (n, n - 2))]
        recs = []
        for fn in files:
            recs += json.load(gzip.open(fn, "rt"))
    else:
        files = sorted(glob.glob(os.path.join(CENSUS, "n11", "results", "post", "real_*.json.gz")))
        recs = []
        for fn in files:
            recs += json.load(gzip.open(fn, "rt"))["real"]
    for r in recs:
        nrec += 1
        assert len(r["set"]) == n and len(r["edges"]) == n - 2
        sets.add(canon(r["set"]))
    return sets, nrec, len(files)


def round1(path):
    s = set()
    for line in opn(path):
        if line.startswith("SET "):
            p = line.split("|")[0].split()
            if int(p[1]) == F:
                s.add(canon([int(x) for x in p[2:]]))
    return s


if __name__ == "__main__":
    N, F, MY = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
    my, hh = mine(MY, N, F)
    cs, nrec, nfiles = census(N)
    print("n=%d f=%d: my classes with h=f: %d (my class h-histogram %s); census records %d in %d files -> %d classes"
          % (N, F, len(my), dict(sorted(hh.items())), nrec, nfiles, len(cs)))
    print("  mine - census = %d, census - mine = %d" % (len(my - cs), len(cs - my)))
    if "--r1" in sys.argv:
        r1 = round1(sys.argv[sys.argv.index("--r1") + 1])
        print("  round-1 classes with h=f: %d; mine - r1 = %d, r1 - mine = %d" % (len(r1), len(my - r1), len(r1 - my)))
