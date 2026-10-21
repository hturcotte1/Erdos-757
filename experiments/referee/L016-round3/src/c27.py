# Referee L016 round 3: exact check of C27 (Theorem 2). Own code: ints only; (4,5) property by brute force over all 4-subsets;
# weak Sidon; 3-APs; h by (i) CP-SAT on the direct Sidon definition (pairs with equal sums), (ii) own exact branch-and-bound for the
# largest 3-AP-free subset, (iii) brute force over all subsets for A_base and B13.
import itertools, sys
from ortools.sat.python import cp_model
Abase = [0,136,200,243,246,249,272,286,298,323,400,528,596,1056]
B13 = [x for x in Abase if x != 1056]
C27 = sorted(Abase + [10**9 + 7919 * b for b in B13])
claimed = [0,136,200,243,246,249,272,286,298,323,400,528,596,1056,1000000000,1001076984,1001583800,1001924317,1001948074,1001971831,1002153968,1002264834,1002359862,1002557837,1003167600,1004181232,1004719724]
assert C27 == claimed, "C27 differs from the certificate's explicit list"
def is45(A):
    bad = 0
    for q in itertools.combinations(A, 4):
        if len({abs(x - y) for x, y in itertools.combinations(q, 2)}) < 5: bad += 1
    return bad
def weak_sidon(A):
    sums = {}
    for x, y in itertools.combinations(A, 2): sums.setdefault(x + y, []).append((x, y))
    return all(len(v) == 1 for v in sums.values())
def aps(A):
    S = set(A); return [(a, (a + c) // 2, c) for a, c in itertools.combinations(A, 2) if (a + c) % 2 == 0 and (a + c) // 2 in S and a < (a + c) // 2 < c]
def h_cpsat_sidon(A):
    # maximise |S| s.t. S is Sidon: for every value s, at most one "pair" {a,b} (a<=b) with a+b=s is fully inside S
    n = len(A); M = cp_model.CpModel(); x = [M.NewBoolVar('x%d' % i) for i in range(n)]
    pairs = {}
    for i in range(n):
        for j in range(i, n): pairs.setdefault(A[i] + A[j], []).append((i, j))
    for s, L in pairs.items():
        for (i, j), (k, l) in itertools.combinations(L, 2):
            idx = {i, j, k, l}
            M.Add(sum(x[v] for v in idx) <= len(idx) - 1)
    M.Maximize(sum(x)); solver = cp_model.CpSolver(); solver.parameters.num_workers = 1; solver.parameters.max_time_in_seconds = 600
    st = solver.Solve(M); assert st == cp_model.OPTIMAL, solver.StatusName(st)
    return int(solver.ObjectiveValue()), [A[i] for i in range(n) if solver.Value(x[i])]
def h_bb(A):
    # exact largest 3-AP-free subset by branch and bound on bitmasks
    n = len(A); E = [sum(1 << A.index(v) for v in e) for e in aps(A)]
    inc = [[e for e in E if e >> i & 1] for i in range(n)]
    best = [0]
    def rec(i, S, cnt):
        if cnt + (n - i) <= best[0]: return
        if i == n: best[0] = max(best[0], cnt); return
        # try to include i
        S2 = S | (1 << i)
        if all((e & S2) != e for e in inc[i]): rec(i + 1, S2, cnt + 1)
        rec(i + 1, S, cnt)
    rec(0, 0, 0); return best[0]
def h_brute(A):
    n = len(A); E = [sum(1 << A.index(v) for v in e) for e in aps(A)]; best = 0
    for S in range(1 << n):
        c = bin(S).count('1')
        if c > best and all((e & S) != e for e in E): best = c
    return best
def tau_bb(A):
    n = len(A); E = [sum(1 << A.index(v) for v in e) for e in aps(A)]
    def cov(S, b):
        for e in E:
            if not (e & S):
                if b == 0: return False
                return any(cov(S | (1 << v), b - 1) for v in range(n) if e >> v & 1)
        return True
    k = 0
    while not cov(0, k): k += 1
    return k
for name, A in [('A_base', Abase), ('B13', B13), ('C27', C27)]:
    n = len(A); assert len(set(A)) == n
    bad = is45(A); ws = weak_sidon(A); P = aps(A)
    print('%s: n=%d distinct, 4-subsets=%d, 4-subsets with <5 distances=%d -> (4,5)-set=%s, weak Sidon=%s, 3-APs=%d' % (name, n, len(list(itertools.combinations(range(n), 4))), bad, bad == 0, ws, len(P)))
    hs, wit = h_cpsat_sidon(A); hb = h_bb(A)
    print('   h by CP-SAT (direct Sidon definition) = %d, witness %s; h by own branch-and-bound (3-AP-free) = %d' % (hs, wit, hb))
    # verify the witness is Sidon directly
    diffs = [abs(x - y) for x, y in itertools.combinations(wit, 2)]; assert len(diffs) == len(set(diffs)); assert len(wit) == hs
    if n <= 14: print('   h by brute force over all 2^%d subsets = %d' % (n, h_brute(A)))
    print('   tau of the AP hypergraph = %d (n - h = %d); I11 slack 3n+2m-11tau = %d' % (tau_bb(A), n - hs, 3 * n + 2 * len(P) - 11 * tau_bb(A)))
    if name == 'C27':
        cross = [e for e in P if (e[0] < 10**8) != (e[2] < 10**8)]
        print('   3-APs using both parts: %d; APs inside A_base part: %d, inside the scaled part: %d' % (len(cross), sum(1 for e in P if e[2] < 10**8), sum(1 for e in P if e[0] >= 10**8)))
        print('   4n/7 record threshold: h <= ceil(4*27/7)-1 = %d; h(C27)=%d' % (-(-108 // 7) - 1, hs))
