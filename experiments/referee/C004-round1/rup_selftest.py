"""Soundness/completeness self-test of reflib.rup_check, plus the structure of the new AP in C004."""
import random, sys, itertools
sys.path.insert(0, '/home/user/Erdos-757/experiments/referee/C004-round1')
import reflib as R  # noqa: E402
from pysat.solvers import Solver  # noqa: E402
rng = random.Random(1)
# (a) satisfiable random 3-CNFs + random fake proofs ending with the empty clause: must never be accepted
acc = 0; tests = 0
for trial in range(300):
    nv = rng.randint(5, 12); m = rng.randint(nv, 3 * nv)
    cnf = [[rng.choice([1, -1]) * v for v in rng.sample(range(1, nv + 1), 3)] for _ in range(m)]
    with Solver(name='minisat22', bootstrap_with=cnf) as s:
        if not s.solve():
            continue
    fake = [' '.join(str(rng.choice([1, -1]) * v) for v in rng.sample(range(1, nv + 1), rng.randint(1, 3))) + ' 0'
            for _ in range(rng.randint(1, 30))] + ['0']
    ok, nl, empty = R.rup_check(cnf, fake, nv)
    tests += 1
    if ok and empty:
        acc += 1
print('satisfiable formulas with fake proofs:', tests, 'accepted (must be 0):', acc)
# (b) genuine proofs of unsatisfiable formulas (pigeonhole PHP(p+1,p) and random unsat 3-CNF) must be accepted;
#     single-literal corruptions are reported (rejection expected in most cases)
def php(p):
    var = lambda i, j: i * p + j + 1
    cl = [[var(i, j) for j in range(p)] for i in range(p + 1)]
    for j in range(p):
        for a, b in itertools.combinations(range(p + 1), 2):
            cl.append([-var(a, j), -var(b, j)])
    return cl, (p + 1) * p
good = 0; total = 0; corrupt_rej = 0; corrupt_tot = 0
insts = [php(p) for p in (3, 4, 5, 6)]
for trial in range(60):
    nv = 12; cnf = [[rng.choice([1, -1]) * v for v in rng.sample(range(1, nv + 1), 3)] for _ in range(80)]
    insts.append((cnf, nv))
for cnf, nv in insts:
    with Solver(name='glucose4', bootstrap_with=cnf, with_proof=True) as s:
        if s.solve():
            continue
        pr = s.get_proof()
    total += 1
    ok, nl, empty = R.rup_check(cnf, pr, nv)
    good += ok and empty
    adds = [i for i, l in enumerate(pr) if l.strip() and not l.startswith('d') and l.strip() != '0']
    if adds:
        i = rng.choice(adds); lits = pr[i].split()[:-1]
        # corruption: drop all but the first literal of a lemma (a stronger, usually non-implied clause)
        pr2 = list(pr); pr2[i] = lits[0] + ' 0'
        ok2, _, e2 = R.rup_check(cnf, pr2, nv)
        corrupt_tot += 1; corrupt_rej += (not (ok2 and e2))
print('unsat instances with genuine glucose4 proofs:', total, 'accepted:', good)
print('corrupted proofs (one lemma truncated to a unit):', corrupt_tot, 'rejected:', corrupt_rej, '(not all must be rejected: a truncated lemma can still be RUP)')
# (c) the new AP(s) in C004
A = sorted(R.as_int_list(R.load_claim('/home/user/Erdos-757/results/claims/C004-lemmaE-SK5-E1.json')['set']))
aps = R.ap_triples(A)
newpts = {0, len(A) - 1}
print('APs meeting the two new points (indices 0 and 57):', [(A[i], A[j], A[k]) for i, j, k in aps if {i, k} & newpts or j in newpts])
print('a =', A[1], ' 2a == max:', 2 * A[1] == A[-1])
