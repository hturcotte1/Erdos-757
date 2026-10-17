"""Referee round 2 (L008): independent check of C16 = A_base + {-323, 5000} (no e757, no judge code).
(4,5): all 4-subsets have >= 5 distinct |differences| (exact ints).  h: (i) CP-SAT model directly on the Sidon definition
(for every pair of distinct pairs {a<=b},{c<=d} with a+b=c+d, not all distinct elements chosen), maximize; (ii) brute force over
all subsets of sizes 10 and 11 with the definition 'all sums x+y (x<=y) distinct'.  Also the 3-AP count and tau of the AP
hypergraph by brute force, and h/n vs 4/7 with Fractions."""
import itertools, json
from fractions import Fraction
from ortools.sat.python import cp_model
AB = [0, 136, 200, 243, 246, 249, 272, 286, 298, 323, 400, 528, 596, 1056]
C = sorted(AB + [-323, 5000]); n = len(C)
assert len(set(C)) == n == 16
bad = [q for q in itertools.combinations(C, 4) if len({abs(x - y) for x, y in itertools.combinations(q, 2)}) < 5]
print('distinct:', len(set(C)) == n, '| 4-subsets:', sum(1 for _ in itertools.combinations(C, 4)), '| violating 4-subsets:', len(bad))
def sidon(S):
    s = [x + y for i, x in enumerate(S) for y in S[i:]]; return len(s) == len(set(s))
# CP-SAT on the definition
m = cp_model.CpModel(); x = [m.NewBoolVar('x%d' % i) for i in range(n)]
pairs = [(i, j) for i in range(n) for j in range(i, n)]
bysum = {}
for (i, j) in pairs: bysum.setdefault(C[i] + C[j], []).append((i, j))
ncons = 0
for s, L in bysum.items():
    for (p, q) in itertools.combinations(L, 2):
        idx = sorted(set(p) | set(q)); m.AddBoolOr([x[k].Not() for k in idx]); ncons += 1
m.Maximize(sum(x)); sol = cp_model.CpSolver(); sol.parameters.num_workers = 1; st = sol.Solve(m)
hcp = int(sol.ObjectiveValue()); S = [C[i] for i in range(n) if sol.Value(x[i])]
print('CP-SAT: status', sol.StatusName(st), 'h =', hcp, 'witness', S, 'is Sidon:', sidon(S), '| constraints', ncons)
has10 = sum(1 for T in itertools.combinations(C, 10) if sidon(T)); has11 = sum(1 for T in itertools.combinations(C, 11) if sidon(T))
print('brute force: Sidon 10-subsets:', has10, '| Sidon 11-subsets:', has11)
aps = [(a, b, c) for a, b, c in itertools.combinations(C, 3) if a + c == 2 * b]
idx = {v: i for i, v in enumerate(C)}; E = [frozenset(idx[v] for v in t) for t in aps]
tau = next(k for k in range(n + 1) if any(all(e & set(T) for e in E) for T in itertools.combinations(range(n), k)))
print('3-APs:', len(aps), '| tau(AP hypergraph) =', tau, '| n - tau =', n - tau)
r = Fraction(hcp, n); print('h/n =', r, '| < 4/7 ?', r < Fraction(4, 7))
json.dump({"id": "L008r2-C16", "type": "construction", "set": C, "claimed_h": hcp, "notes": "referee round 2 scratch check (not a claim)"}, open('L008r2-C16.json', 'w'))
