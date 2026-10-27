#!/usr/bin/env python3
"""Independent referee verifier for claim C006 (results/claims/C006-tight-21pt-h12.json).

Does NOT import e757/ or judge/.  Exact integer / Fraction arithmetic throughout.
Methods for h(A) (largest Sidon subset), all from the DEFINITION
"S is Sidon iff all sums x+y (x<=y in S) are distinct":
  H1  numpy enumeration of all 2^n subsets against the 'violation sets'
      {i,j,k,l} (from A_i+A_j = A_k+A_l, {i,j} != {k,l} as multisets);
  H2  brute force over all C(n,13) and C(n,12) subsets, checking sums directly;
  H3  ILP: OR-tools CP-SAT and scipy/HiGHS milp on the violation-set constraints;
  H4  transversal number of the 3-AP hypergraph by brute force over C(n,8), C(n,9).
"""
import itertools, json, re, sys, time
from fractions import Fraction
from math import comb, floor, ceil

import numpy as np

CLAIM = "/home/user/Erdos-757/results/claims/C006-tight-21pt-h12.json"
EXPECTED = [0, 210, 396, 420, 444, 792, 888, 1374, 1566, 1581, 1596, 1758, 1935,
            1941, 2231, 2301, 2304, 2375, 2449, 2521, 2667]
T0 = time.time()
problems = []


def say(*a):
    print(*a, flush=True)


def check(cond, msg):
    say(("  OK   " if cond else "  FAIL ") + msg)
    if not cond:
        problems.append(msg)


# ---------------------------------------------------------------- 0. parsing
say("== 0. parsing / artifacts")
raw = open(CLAIM).read()
floats_seen = []
data = json.loads(raw, parse_float=lambda s: floats_seen.append(s) or Fraction(s))
check(not floats_seen, f"no float literals anywhere in the JSON (seen: {floats_seen})")
A_raw = data["set"]
check(all(type(x) is int for x in A_raw), "every element of 'set' is a JSON integer (type int, not bool/float/str)")
m_set = re.search(r'"set"\s*:\s*\[([^\]]*)\]', raw)
toks = [t.strip() for t in m_set.group(1).split(",")]
check(all(re.fullmatch(r"-?\d+", t) for t in toks), "raw tokens of 'set' are plain decimal integers")
check(A_raw == EXPECTED, "set equals the 21 integers quoted in the referee task")
n = len(A_raw)
check(n == 21, f"n = {n}")
check(len(set(A_raw)) == n, "all points distinct")
check(A_raw == sorted(A_raw), "listed in increasing order (not needed, informational)")
A = sorted(A_raw)
W = data.get("witness_sidon_subset")
claimed_h = data.get("claimed_h")
say(f"  claimed_h = {claimed_h}; witness size = {len(W) if W else None}")
check(type(claimed_h) is int and claimed_h == 12, "claimed_h is the integer 12")
idx = {x: i for i, x in enumerate(A)}

# ---------------------------------------------------------------- 1. (4,5)
say("== 1. (4,5) property, three formulations")
hist = {}
bad1 = bad2 = 0
for B in itertools.combinations(A, 4):
    D = {abs(x - y) for x, y in itertools.combinations(B, 2)}
    BB = {x - y for x in B for y in B}
    hist[len(D)] = hist.get(len(D), 0) + 1
    if len(D) < 5:
        bad1 += 1
    if len(BB) < 11:
        bad2 += 1
    assert len(BB) == 1 + 2 * len(D)
say(f"  4-subsets: {comb(n,4)}; histogram of #distinct distances: {dict(sorted(hist.items()))}")
check(bad1 == 0, "M1: every 4-subset has >= 5 distinct positive differences")
check(bad2 == 0, "M2: every 4-subset B has |B-B| >= 11 (and |B-B| = 1+2|D(B)| always)")
# M3 structural: weak Sidon (no 4 distinct a+b=c+d) and no two 3-APs sharing two points
sums = {}
for i, j in itertools.combinations(range(n), 2):
    sums.setdefault(A[i] + A[j], []).append((i, j))
weak_sidon = all(len(v) == 1 for v in sums.values())
APs = []
for i in range(n):
    for k in range(i + 2, n):
        s = A[i] + A[k]
        if s % 2 == 0 and (s // 2) in idx:
            j = idx[s // 2]
            assert i < j < k
            APs.append((i, j, k))
m = len(APs)
linear = all(len(set(e) & set(f)) <= 1 for e, f in itertools.combinations(APs, 2))
check(weak_sidon, "M3a: weak Sidon (all sums x+y, x<y, distinct)")
check(linear, "M3b: no two 3-APs share two points (AP hypergraph linear)")
check(hist.get(5, 0) == m * (n - 3), f"M3c: #4-sets with exactly 5 distances = m(n-3) = {m*(n-3)} (each contains exactly one AP)")

# ---------------------------------------------------------------- 2. Sidon / h
say("== 2. h(A): largest Sidon subset")


def is_sidon_sums(S):
    s = [x + y for x, y in itertools.combinations_with_replacement(S, 2)]
    return len(s) == len(set(s))


def is_sidon_diffs(S):
    d = [abs(x - y) for x, y in itertools.combinations(S, 2)]
    return len(d) == len(set(d))


check(W is not None and set(W) <= set(A) and len(set(W)) == len(W) == 12, "witness is a 12-subset of A")
check(is_sidon_sums(sorted(W)) and is_sidon_diffs(sorted(W)), "witness is Sidon (sums and differences forms)")
# violation sets from the Sidon definition (multiset pairs with equal sums)
psums = {}
for i, j in itertools.combinations_with_replacement(range(n), 2):
    psums.setdefault(A[i] + A[j], []).append((i, j))
viol = set()
for v in psums.values():
    for p, q in itertools.combinations(v, 2):
        viol.add(frozenset(p) | frozenset(q))
viol = sorted(viol, key=lambda s: sorted(s))
sizes = {}
for v in viol:
    sizes[len(v)] = sizes.get(len(v), 0) + 1
say(f"  violation sets from equal sums: {len(viol)}, by size {sizes}")
apsets = sorted(frozenset(e) for e in APs)
check(sorted(viol, key=sorted) == sorted(apsets, key=sorted),
      "violation sets are exactly the 3-AP triples (instance check of Ma-Tang Lemma 2.3)")

# H1: numpy over all 2^n subsets
N = 1 << n
masks = np.arange(N, dtype=np.int64)
ind = np.ones(N, dtype=bool)
for v in viol:
    vm = sum(1 << i for i in v)
    ind &= (masks & vm) != vm
pc = np.bitwise_count(masks.astype(np.uint64)).astype(np.int64)
h1 = int(pc[ind].max())
cnt_max = int(np.count_nonzero(ind & (pc == h1)))
say(f"  H1 (2^{n} enumeration): h = {h1}; #maximum Sidon subsets = {cnt_max}; #Sidon subsets total = {int(ind.sum())}")
check(h1 == 12, "H1: h = 12")

# H2: brute force over 13- and 12-subsets, direct sum check
t = time.time()
s13 = sum(1 for S in itertools.combinations(A, 13) if is_sidon_sums(S))
s12 = sum(1 for S in itertools.combinations(A, 12) if is_sidon_sums(S))
say(f"  H2: Sidon 13-subsets: {s13} of {comb(n,13)}; Sidon 12-subsets: {s12} of {comb(n,12)} ({time.time()-t:.1f}s)")
check(s13 == 0, "H2: no 13-subset is Sidon (so h <= 12, as Sidon is hereditary)")
check(s12 == cnt_max, "H2: #Sidon 12-subsets agrees with H1")

# H3: ILPs
from ortools.sat.python import cp_model
mdl = cp_model.CpModel()
x = [mdl.NewBoolVar(f"x{i}") for i in range(n)]
for v in viol:
    mdl.Add(sum(x[i] for i in v) <= len(v) - 1)
mdl.Maximize(sum(x))
sol = cp_model.CpSolver()
sol.parameters.num_workers = 1
sol.parameters.max_time_in_seconds = 120
st = sol.Solve(mdl)
cp_opt = int(round(sol.ObjectiveValue()))
say(f"  H3a CP-SAT: status={sol.StatusName(st)}, optimum={cp_opt}, bound={sol.BestObjectiveBound()}")
check(sol.StatusName(st) == "OPTIMAL" and cp_opt == 12, "H3a: CP-SAT proves max = 12")
mdl2 = cp_model.CpModel()
y = [mdl2.NewBoolVar(f"y{i}") for i in range(n)]
for v in viol:
    mdl2.Add(sum(y[i] for i in v) <= len(v) - 1)
mdl2.Add(sum(y) >= 13)
sol2 = cp_model.CpSolver()
sol2.parameters.num_workers = 1
st2 = sol2.Solve(mdl2)
say(f"  H3b CP-SAT feasibility of a Sidon 13-subset: {sol2.StatusName(st2)}")
check(sol2.StatusName(st2) == "INFEASIBLE", "H3b: Sidon 13-subset infeasible")
from scipy.optimize import milp, LinearConstraint, Bounds
Amat = np.zeros((len(viol), n))
ub = np.zeros(len(viol))
for r, v in enumerate(viol):
    for i in v:
        Amat[r, i] = 1
    ub[r] = len(v) - 1
res = milp(c=-np.ones(n), constraints=LinearConstraint(Amat, -np.inf, ub),
           integrality=np.ones(n), bounds=Bounds(0, 1))
say(f"  H3c scipy/HiGHS milp: status={res.status} ({res.message}), optimum={-res.fun}")
check(res.status == 0 and round(-res.fun) == 12, "H3c: HiGHS proves max = 12")
sel = [A[i] for i in range(n) if res.x[i] > 0.5]
check(is_sidon_sums(sel) and len(sel) == 12, f"H3c: HiGHS solution is a Sidon 12-set {sel}")

# ---------------------------------------------------------------- 3. AP hypergraph
say("== 3. AP hypergraph")
say("  APs (as values a<b<c, midpoint b): " + "; ".join(f"{A[i]},{A[j]},{A[k]}" for i, j, k in APs))
mids = [j for _, j, _ in APs]
check(m == 19, f"m = #3-APs = {m}")
check(len(set(mids)) == m, "midpoint map injective (distinct midpoints)")
check(0 not in mids and n - 1 not in mids, "min A and max A are not midpoints")
nonmid = [A[v] for v in range(n) if v not in mids]
say(f"  non-midpoints: {nonmid}  (saturated iff m = n-2: {m == n-2})")
deg = [sum(v in e for e in APs) for v in range(n)]
say(f"  degree by point: " + ", ".join(f"{A[v]}:{deg[v]}" for v in range(n)))
dseq = sorted(deg, reverse=True)
say(f"  degree sequence (sorted): {dseq}; sum = {sum(deg)} (= 3m = {3*m})")
check(max(deg) == 4, f"max degree = {max(deg)}")
check(linear, "linear")
# connectivity
par = list(range(n))


def fnd(a):
    while par[a] != a:
        par[a] = par[par[a]]
        a = par[a]
    return a


for e in APs:
    for v in e[1:]:
        par[fnd(v)] = fnd(e[0])
comps = len({fnd(v) for v in range(n)})
say(f"  connected components of H (isolated points count): {comps}; isolated: {[A[v] for v in range(n) if deg[v]==0]}")
# F7-freeness, two methods
F7 = [(0, 1, 2), (0, 3, 4), (0, 5, 6), (1, 3, 5), (2, 4, 6)]
Eset = set(apsets)
emb = 0


def bt(phi):
    global emb
    k = len(phi)
    if k == 7:
        emb += 1
        return
    for v in range(n):
        if v in phi:
            continue
        phi2 = phi + [v]
        ok = True
        for e in F7:
            if max(e) == k and frozenset(phi2[t] for t in e) not in Eset:
                ok = False
                break
        if ok:
            bt(phi2)


bt([])
check(emb == 0, f"F7-free (backtracking embedding count = {emb})")
cand = 0
iso = 0
F7s = {frozenset(e) for e in F7}
for es in itertools.combinations(APs, 5):
    U = sorted(set().union(*map(set, es)))
    if len(U) != 7:
        continue
    cand += 1
    es_s = {frozenset(e) for e in es}
    for perm in itertools.permutations(U):
        if {frozenset(perm[t] for t in e) for e in F7} == es_s:
            iso += 1
            break
check(iso == 0, f"F7-free (5-edge subsets on 7 points: {cand}, isomorphic to F7: {iso})")

# H4: transversal number
t = time.time()
emasks = [sum(1 << v for v in e) for e in APs]
tr8 = sum(1 for T in itertools.combinations(range(n), 8)
          if all(any(v in e for v in T) for e in APs))
tr9 = sum(1 for T in itertools.combinations(range(n), 9)
          if all(any(v in e for v in T) for e in APs))
say(f"  H4: transversals of size 8: {tr8}; size 9: {tr9} ({time.time()-t:.1f}s)")
check(tr8 == 0 and tr9 == cnt_max, "H4: tau = 9 and #minimum transversals = #maximum Sidon subsets")
compW = [A[i] for i in range(n) if A[i] not in set(W)]
check(all(any(A[v] in compW for v in e) for e in APs), f"complement of the witness {compW} is a transversal")
tau = 9
check(n - tau == h1, "h = n - tau (alpha = n - tau)")

# ---------------------------------------------------------------- 4. arithmetic
say("== 4. exact arithmetic")
check(Fraction(h1, n) == Fraction(4, 7), f"h/n = {Fraction(h1,n)} == 4/7 exactly (not < 4/7: no record)")
check(not (Fraction(h1, n) < Fraction(4, 7)), "h/n < 4/7 is FALSE")
lb_pub = Fraction(9 * n, 17)
lb_sharp = Fraction(9 * n + 6, 17)
say(f"  9n/17 = {lb_pub} = {float(lb_pub):.4f}; (9n+6)/17 = {lb_sharp} = {float(lb_sharp):.4f}")
check(ceil(lb_pub) == 12 and ceil(lb_sharp) == 12, "both forms give h >= 12 at n = 21")
taumax = Fraction(5 * n + 3 * (n - 2), 17)
say(f"  HY with m <= n-2: tau <= (8n-6)/17 = {taumax} = {float(taumax):.4f}, floor = {floor(taumax)}")
check(floor(taumax) == 9, "tau <= 9, h >= 12 for every 21-point (4,5)-set")
check(17 * tau <= 5 * n + 3 * m, f"HY on this set: 17*tau = {17*tau} <= 5n+3m = {5*n+3*m} (slack {5*n+3*m-17*tau})")
check(11 * tau <= 3 * n + 2 * m, f"I11 on this set: 11*tau = {11*tau} <= 3n+2m = {3*n+2*m} (slack {3*n+2*m-11*tau})")
say(f"  D = 17h - 9n = {17*h1 - 9*n}; D/n = {Fraction(17*h1-9*n, n)}")

# ---------------------------------------------------------------- 5. all subsets
say("== 5. every subset S of A (each is a (4,5)-set): alpha, e(S), HY, I11, class C")
g = np.where(ind, pc, 0).astype(np.int8)
for i in range(n):
    g = g.reshape(-1, 2, 1 << i)
    g[:, 1, :] = np.maximum(g[:, 1, :], g[:, 0, :])
    g = g.reshape(-1)
alpha = g.astype(np.int64)  # alpha[S] = max Sidon subset of S
e = np.zeros(N, dtype=np.int64)
for em in emasks:
    e += ((masks & em) == em)
tauS = pc - alpha
big = pc >= 2
check(bool(np.all(e[big] <= pc[big] - 2)), "e(S) <= |S|-2 for all S with |S| >= 2 (class C)")
check(bool(np.all(17 * tauS <= 5 * pc + 3 * e)), "HY 17 tau <= 5|S|+3e(S) on all 2^21 subsets")
check(bool(np.all(11 * tauS <= 3 * pc + 2 * e)), "I11 11 tau <= 3|S|+2e(S) on all 2^21 subsets")
check(int(alpha[N - 1]) == 12, "SOS-DP alpha(full) = 12")
fknown = {1: 1, 2: 2, 3: 2, 4: 3, 5: 4, 6: 4, 7: 5, 8: 5, 9: 6, 10: 6, 11: 7, 12: 7, 13: 8,
          14: 8, 15: 9, 16: 10, 17: 10, 18: 11, 20: 12}
row = []
for k in range(1, n + 1):
    sel_k = pc == k
    mn = int(alpha[sel_k].min())
    row.append((k, mn))
    if k in fknown:
        check(mn >= fknown[k], f"min h over {k}-subsets = {mn} >= f({k}) = {fknown[k]}")
    else:
        say(f"  min h over {k}-subsets = {mn} (f({k}) not pinned here)")
full = N - 1
two = [(int(alpha[full ^ (1 << i)])) for i in range(n)]
say(f"  h(A minus one point) for each point: {two}")
# 19-point subsets
m19 = min(int(alpha[full ^ (1 << i) ^ (1 << j)]) for i, j in itertools.combinations(range(n), 2))
say(f"  min h over 19-point subsets: {m19}")
# two-block partition certificate for tau >= 9
tf = tauS
comp = full ^ masks
hits = np.nonzero((tf + tf[comp] == 9) & (masks != 0) & (masks != full) & (masks < comp))[0]
say(f"  two-block partitions (U, V-U) with tau(U)+tau(V-U) = 9: {len(hits)}")
if len(hits):
    best = min(hits, key=lambda s: max(int(pc[s]), int(pc[full ^ s])))
    U = [A[i] for i in range(n) if best >> i & 1]
    V2 = [A[i] for i in range(n) if not best >> i & 1]
    say(f"    most balanced: U={U} (tau {int(tf[best])}), V-U={V2} (tau {int(tf[full^best])})")

say(f"== done in {time.time()-T0:.1f}s; problems: {len(problems)}")
for p in problems:
    say("  PROBLEM: " + p)
sys.exit(1 if problems else 0)
