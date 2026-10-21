"""SAT decision of h(C004) from the Sidon definition: >= 33 SAT (model re-verified), >= 34 UNSAT with a DRUP proof
from Glucose4 checked by my own forward RUP checker (reflib.rup_check); MiniSat22 as a second solver.
The cardinality encoding (Sinz sequential counter) is my own and is first validated exhaustively on small sizes."""
import itertools
import json
import sys
import time

sys.path.insert(0, '/home/user/Erdos-757/experiments/referee/C004-round1')
import reflib as R  # noqa: E402
from pysat.solvers import Solver  # noqa: E402

out = {}
# ---- 1. exhaustive validation of the sequential counter: for n <= 7, every K, every assignment
t = time.time()
bad = 0
cases = 0
for nn in range(1, 8):
    xs = list(range(1, nn + 1))
    for K in range(0, nn + 1):
        cls, top = R.atmost_seqcounter(xs, K, nn)
        with Solver(name='minisat22', bootstrap_with=cls) as s:
            for bits in itertools.product([0, 1], repeat=nn):
                ass = [x if b else -x for x, b in zip(xs, bits)]
                res = s.solve(assumptions=ass)
                cases += 1
                if res != (sum(bits) <= K):
                    bad += 1
print(f'seq-counter exhaustive validation: {cases} (n,K,assignment) cases, {bad} mismatches ({time.time()-t:.1f}s)')
out['seqcounter_validation'] = {'cases': cases, 'mismatches': bad}

# ---- 2. the claim
c = R.load_claim('/home/user/Erdos-757/results/claims/C004-lemmaE-SK5-E1.json')
A = sorted(R.as_int_list(c['set']))
n = len(A)
forb, census = R.forbidden_sets(A)
print('n', n, 'forbidden census', census)

for k in (33, 34):
    cnf, top = R.sidon_cnf(n, forb, k)
    print(f'k={k}: vars={top} clauses={len(cnf)}')
    for name in ('minisat22', 'glucose4'):
        t = time.time()
        with Solver(name=name, bootstrap_with=cnf) as s:
            res = s.solve()
            dt = time.time() - t
            info = {'result': res, 'secs': round(dt, 2)}
            try:
                info['stats'] = s.accum_stats()
            except Exception:  # noqa: BLE001
                pass
            if res:
                model = s.get_model()
                chosen = [A[v] for v in range(n) if model[v] > 0]
                info['model_size'] = len(chosen)
                info['model_sidon_sums'] = R.is_sidon_sums(chosen)
                info['model_sidon_diffs'] = R.is_sidon_diffs(chosen)
                info['model_subset'] = set(chosen) <= set(A)
            print(f'  {name}: {info}')
            out[f'k{k}_{name}'] = info

# ---- 3. DRUP proof of UNSAT for k = 34 (Glucose4), checked by own forward RUP checker
cnf, top = R.sidon_cnf(n, forb, 34)
t = time.time()
with Solver(name='glucose4', bootstrap_with=cnf, with_proof=True) as s:
    res = s.solve()
    proof = s.get_proof() if not res else None
print(f'glucose4 with proof: result {res} ({time.time()-t:.1f}s); proof lines: {len(proof) if proof else None}')
out['k34_glucose4_proof_lines'] = len(proof) if proof else None
if proof is not None:
    with open('/home/user/Erdos-757/experiments/referee/C004-round1/k34.drup', 'w') as fh:
        fh.write('\n'.join(proof) + '\n')
    with open('/home/user/Erdos-757/experiments/referee/C004-round1/k34.cnf', 'w') as fh:
        fh.write(f'p cnf {top} {len(cnf)}\n')
        for cl in cnf:
            fh.write(' '.join(map(str, cl)) + ' 0\n')
    t = time.time()
    ok, nl, empty = R.rup_check(cnf, proof, top)
    print(f'own RUP check: all lemmas RUP = {ok}; lemmas checked = {nl}; empty clause derived = {empty} '
          f'({time.time()-t:.1f}s)')
    out['k34_rup_check'] = {'ok': ok, 'lemmas': nl, 'empty': empty}

# ---- 4. negative control for the RUP checker: a corrupted proof must be rejected
if proof is not None:
    lem = [p for p in proof if p.strip() and not p.startswith('d')]
    # a non-implied lemma: the unit clause 'x_1 true' is not implied by the k=34 CNF? use a clause that is false
    # in a known model of the k=33 CNF restricted... simplest: a lemma that contradicts a SAT model of the base clauses
    fake = ['1 0', '-1 0', '0']  # deriving both x1 and -x1 by RUP is impossible unless already refutable by UP
    ok2, nl2, _ = R.rup_check(cnf, fake, top)
    print('negative control (fake proof "1 0 / -1 0 / 0"): accepted =', ok2, 'at lemma', nl2)
    out['rup_negative_control_accepted'] = ok2
    # and the k = 33 (satisfiable) CNF must NOT be refuted by the k = 34 proof
    cnf33, top33 = R.sidon_cnf(n, forb, 33)
    ok3, nl3, e3 = R.rup_check(cnf33, proof, max(top, top33))
    print('negative control (k=34 proof replayed on the satisfiable k=33 CNF): ok =', ok3, 'empty =', e3,
          'stopped at lemma', nl3)
    out['rup_negative_control_k33'] = {'ok': ok3, 'empty': e3}
with open('/home/user/Erdos-757/experiments/referee/C004-round1/sat_c004.json', 'w') as fh:
    json.dump(out, fh, indent=1, default=str)
