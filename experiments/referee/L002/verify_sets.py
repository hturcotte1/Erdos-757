"""Referee L002: independent Python verification (exact integers/Fractions; no e757, no judge import).
 - known 12-point sets: (4,5), m, h by CP-SAT ILP, canonical normal form in the census list (from realized file);
 - random sample of census sets: distinct, (4,5), AP pattern == stored edges, m == 10, h == 7 by CP-SAT ILP
   (with the witness re-checked by definition and optimality status OPTIMAL)."""
import gzip, json, random, itertools, sys
from fractions import Fraction
from math import gcd
from ortools.sat.python import cp_model

def is45(A):
    for q in itertools.combinations(A, 4):
        if len({abs(x - y) for x, y in itertools.combinations(q, 2)}) < 5: return False
    return True
def aps(A):
    A = sorted(A); pos = {v: i for i, v in enumerate(A)}; out = set()
    for i, k in itertools.combinations(range(len(A)), 2):
        s = A[i] + A[k]
        if s % 2 == 0 and s // 2 in pos: out.add((i, pos[s // 2], k))
    return out
def sidon(S):
    d = [y - x for x, y in itertools.combinations(sorted(S), 2)]
    return len(d) == len(set(d))
def h_ilp(A):
    A = sorted(A); n = len(A)
    md = cp_model.CpModel(); x = [md.NewBoolVar(f"x{i}") for i in range(n)]
    pairs = list(itertools.combinations(range(n), 2))
    for (a, b), (c, d) in itertools.combinations(pairs, 2):
        if A[b] - A[a] == A[d] - A[c]:
            S = sorted({a, b, c, d}); md.Add(sum(x[i] for i in S) <= len(S) - 1)
    md.Maximize(sum(x)); sv = cp_model.CpSolver(); sv.parameters.num_workers = 1
    st = sv.Solve(md); assert st == cp_model.OPTIMAL
    W = [A[i] for i in range(n) if sv.Value(x[i])]
    assert sidon(W)
    return len(W)
def canon(v):
    v = sorted(Fraction(t) for t in v); v = [t - v[0] for t in v]
    den = 1
    for t in v: den = den * t.denominator // gcd(den, t.denominator)
    v = [int(t * den) for t in v]; g = 0
    for t in v: g = gcd(g, t)
    v = [t // g for t in v]; r = sorted(v[-1] - t for t in v)
    return tuple(min(v, r))

census = json.load(gzip.open(sys.argv[1], "rt"))
cset = {canon(r["set"]): r for r in census}
print("census entries", len(census), "distinct classes", len(cset))
known = {"record_12": [0, 269, 385, 467, 501, 511, 521, 523, 535, 538, 549, 575],
         "record_12b / omega ex.1": [0, 178, 198, 218, 227, 235, 272, 276, 287, 317, 356, 436],
         "record_12c / omega ex.2": [-336, -168, -44, -24, -4, 0, 39, 44, 49, 80, 102, 160]}
for k, A in known.items():
    c = canon(A)
    print(k, "n", len(A), "(4,5)", is45(A), "m", len(aps(A)), "h_ilp", h_ilp(A), "class in census", c in cset)
print("known classes pairwise distinct:", len({canon(A) for A in known.values()}) == 3)
random.seed(int(sys.argv[3]) if len(sys.argv) > 3 else 757)
sample = random.sample(census, int(sys.argv[2]))
bad = 0
for r in sample:
    A = r["set"]
    ok = (len(set(A)) == 12 and is45(A) and aps(A) == set(map(tuple, r["edges"])) and len(aps(A)) == 10 and h_ilp(A) == 7)
    bad += not ok
print("sample", len(sample), "failures", bad)
