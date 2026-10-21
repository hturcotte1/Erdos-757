"""(i) Replay genuine proofs on SATISFIABLE formulas (an UNSAT formula minus one clause): the empty clause must
never be derived.  (ii) Compare reflib.rup_check (2-watched literals) with a naive full-scan RUP checker on
corrupted proofs: outcomes must agree exactly (ok flag and the index of the first failing lemma)."""
import random, sys, itertools
sys.path.insert(0, '/home/user/Erdos-757/experiments/referee/C004-round1')
import reflib as R  # noqa: E402
from pysat.solvers import Solver  # noqa: E402

def naive_rup(clauses, proof):
    db = [list(c) for c in clauses]
    nl = 0
    def up_conflict(assumed):
        val = {}
        for x in assumed:
            if val.get(abs(x), x > 0) != (x > 0):
                return True
            val[abs(x)] = x > 0
        changed = True
        while changed:
            changed = False
            for c in db:
                unassigned = []; sat = False
                for l in c:
                    v = val.get(abs(l))
                    if v is None: unassigned.append(l)
                    elif v == (l > 0): sat = True; break
                if sat: continue
                if not unassigned: return True
                if len(unassigned) == 1:
                    l = unassigned[0]; val[abs(l)] = l > 0; changed = True
        return False
    for line in proof:
        line = line.strip()
        if not line or line.startswith('d') or line.startswith('c'):
            continue
        lits = [int(t) for t in line.split()][:-1]
        nl += 1
        if not up_conflict([-x for x in lits]):
            return False, nl, False
        if not lits:
            return True, nl, True
        db.append(lits)
    return True, nl, up_conflict([])

rng = random.Random(3)
insts = []
for trial in range(120):
    nv = rng.randint(8, 14)
    insts.append(([[rng.choice([1, -1]) * v for v in rng.sample(range(1, nv + 1), 3)] for _ in range(int(6.5 * nv))], nv))
replay_tests = 0; replay_bad = 0; cmp_tests = 0; cmp_bad = 0
for cnf, nv in insts:
    with Solver(name='glucose4', bootstrap_with=cnf, with_proof=True) as s:
        if s.solve():
            continue
        pr = s.get_proof()
    # (i) satisfiable sub-formula
    for rep in range(4):
        j = rng.randrange(len(cnf)); F = cnf[:j] + cnf[j + 1:]
        with Solver(name='minisat22', bootstrap_with=F) as s2:
            if not s2.solve():
                continue
        ok, nl, empty = R.rup_check(F, pr, nv)
        replay_tests += 1
        replay_bad += (ok and empty)
    # (ii) corrupted proofs: my checker vs naive checker
    adds = [i for i, l in enumerate(pr) if l.strip() and not l.startswith('d') and l.strip() != '0']
    for rep in range(3):
        pr2 = list(pr)
        if adds:
            i = rng.choice(adds); lits = [int(x) for x in pr[i].split()[:-1]]
            mode = rng.randrange(3)
            if mode == 0: sub = rng.sample(lits, max(1, len(lits) // 2))
            elif mode == 1: sub = [-lits[0]] + lits[1:]
            else: sub = [rng.choice([1, -1]) * rng.randint(1, nv)]
            pr2[i] = ' '.join(map(str, sub)) + ' 0'
        a = R.rup_check(cnf, pr2, nv); b = naive_rup(cnf, pr2)
        cmp_tests += 1
        if (a[0], a[1] if not a[0] else None) != (b[0], b[1] if not b[0] else None):
            cmp_bad += 1
            print('MISMATCH', a, b)
print('replays of genuine proofs on satisfiable formulas:', replay_tests, 'empty clause derived (must be 0):', replay_bad)
print('corrupted proofs compared with the naive checker:', cmp_tests, 'disagreements (must be 0):', cmp_bad)
# the main certificate through the naive checker too
c = R.load_claim('/home/user/Erdos-757/results/claims/C004-lemmaE-SK5-E1.json')
A = sorted(R.as_int_list(c['set'])); forb, _ = R.forbidden_sets(A)
cnf, top = R.sidon_cnf(len(A), forb, 34)
proof = open('/home/user/Erdos-757/experiments/referee/C004-round1/k34.drup').read().splitlines()
print('main k>=34 certificate through the naive full-scan RUP checker:', naive_rup(cnf, proof))
