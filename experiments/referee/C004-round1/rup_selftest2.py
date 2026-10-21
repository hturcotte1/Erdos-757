"""For every corrupted proof the RUP checker ACCEPTS, check that the corrupted lemma is semantically implied
(cnf AND NOT lemma is UNSAT); an accepted non-implied lemma would expose an unsound checker."""
import random, sys, itertools
sys.path.insert(0, '/home/user/Erdos-757/experiments/referee/C004-round1')
import reflib as R  # noqa: E402
from pysat.solvers import Solver  # noqa: E402
rng = random.Random(2)
def php(p):
    var = lambda i, j: i * p + j + 1
    cl = [[var(i, j) for j in range(p)] for i in range(p + 1)]
    for j in range(p):
        for a, b in itertools.combinations(range(p + 1), 2):
            cl.append([-var(a, j), -var(b, j)])
    return cl, (p + 1) * p
insts = [php(p) for p in (4, 5, 6)]
for trial in range(150):
    nv = rng.randint(10, 16); cnf = [[rng.choice([1, -1]) * v for v in rng.sample(range(1, nv + 1), 3)] for _ in range(int(6.5 * nv))]
    insts.append((cnf, nv))
acc_bad = 0; acc = 0; rej = 0; tot = 0
for cnf, nv in insts:
    with Solver(name='glucose4', bootstrap_with=cnf, with_proof=True) as s:
        if s.solve():
            continue
        pr = s.get_proof()
    adds = [i for i, l in enumerate(pr) if l.strip() and not l.startswith('d') and l.strip() != '0']
    if not adds:
        continue
    for rep in range(3):
        i = rng.choice(adds); lits = [int(x) for x in pr[i].split()[:-1]]
        sub = rng.sample(lits, max(1, len(lits) // 2))
        pr2 = list(pr); pr2[i] = ' '.join(map(str, sub)) + ' 0'
        ok2, nl2, e2 = R.rup_check(cnf, pr2, nv)
        tot += 1
        if ok2:
            acc += 1
            # semantic implication of the corrupted lemma by the original formula
            with Solver(name='minisat22', bootstrap_with=cnf + [[-x] for x in sub]) as s2:
                if s2.solve():
                    acc_bad += 1
        else:
            rej += 1
print('corrupted proofs:', tot, 'rejected:', rej, 'accepted:', acc, 'accepted with a NON-implied lemma (must be 0):', acc_bad)
