"""Referee L007 r2: Step 7 witnesses from the definitions (exact integers).
(4,5): every 4-subset has >= 5 distinct absolute differences.  APs: triples x<y<z with x+z=2y.
h: (a) largest subset whose positive differences are all distinct, by brute force over all 2^n subsets;
   (b) CP-SAT maximum Sidon subset: for every a+b=c+d with {a,b}!={c,d} (a<=b, c<=d) forbid all of them chosen."""
import itertools, json
from ortools.sat.python import cp_model
def is45(A):
    return all(len({abs(x - y) for x, y in itertools.combinations(B, 2)}) >= 5 for B in itertools.combinations(A, 4))
def aps(A):
    S = set(A); return [(x, (x + z) // 2, z) for x, z in itertools.combinations(sorted(A), 2) if (x + z) % 2 == 0 and (x + z) // 2 in S]
def sidon(B):
    d = [y - x for x, y in itertools.combinations(sorted(B), 2)]
    return len(d) == len(set(d))
def h_brute(A):
    A = sorted(A); n = len(A); best = 0
    for mask in range(1 << n):
        k = bin(mask).count('1')
        if k <= best: continue
        if sidon([A[i] for i in range(n) if mask >> i & 1]): best = k
    return best
def h_cpsat(A):
    A = sorted(A); n = len(A); M = cp_model.CpModel(); x = [M.NewBoolVar('x%d' % i) for i in range(n)]
    sums = {}
    for i in range(n):
        for j in range(i, n):
            sums.setdefault(A[i] + A[j], []).append((i, j))
    for s, L in sums.items():
        for (i, j), (k, l) in itertools.combinations(L, 2):
            idx = sorted({i, j, k, l}); M.AddBoolOr([x[t].Not() for t in idx])
    M.Maximize(sum(x)); S = cp_model.CpSolver(); S.parameters.num_workers = 1
    r = S.Solve(M); assert r == cp_model.OPTIMAL
    return int(S.ObjectiveValue())
W = [0, 323, 523, 566, 569, 572, 595, 609, 621, 646, 723, 851, 919, 1379]
fib = [2, 3]
while len(fib) < 14: fib.append(fib[-1] + fib[-2])
Abase = [0, 136, 200, 243, 246, 249, 272, 286, 298, 323, 400, 528, 596, 1056]
out = {}
for name, A in [('W', W), ('Fib_F3_F16', fib), ('A_base', Abase)]:
    out[name] = dict(n=len(A), distinct=len(set(A)) == len(A), is45=is45(A), m=len(aps(A)), h_brute=h_brute(A), h_cpsat=h_cpsat(A))
    print(name, A, out[name], flush=True)
print('W APs:', aps(W))
Wm = sorted(set(x - 323 for x in W)); target = sorted((set(Abase) - {136}) | {-323})
print('W-323 == (A_base \\ {136}) U {-323}:', Wm == target)
json.dump(out, open('witness_check.json', 'w'), indent=1)
