"""Validate drup_check on small instances: UNSAT at h+1 must be certified; also a corrupted proof must be rejected."""
import sys, json
sys.path.insert(0, '.')
from sat_check import build
from drup_check import RUP
from pysat.solvers import Solver
def certify(A, k, corrupt=False):
    cnf, _, _ = build(sorted(A), k)
    with Solver(name='glucose4', bootstrap_with=cnf, with_proof=True) as s:
        assert not s.solve(); proof = s.get_proof()
    chk = RUP()
    for c in cnf: chk.add(c)
    lines = [l for l in proof if l.split() and l.split()[0] != 'd']
    if corrupt:   # replace the proof by the bare empty clause: must fail unless F is UP-refutable
        lines = ['0']
    for line in lines:
        lits = [int(x) for x in line.split()][:-1]
        if not chk.implied(lits):
            return False, len(lines)
        if not lits: return True, len(lines)
        chk.add(lits)
    return chk.implied([]), len(lines)
Abase = [0, 136, 200, 243, 246, 249, 272, 286, 298, 323, 400, 528, 596, 1056]
O = [0, 49, 75, 83, 98, 101, 117, 119, 121, 159, 269]
I1 = sorted(set([269 * x for x in O] + [269 * 101 + 18 * x for x in O]))
t = 3 * (max(I1) - min(I1)) + 1000003
E1 = sorted(set([x + t for x in I1] + [0, 2 * t]))
for name, A, h in (('A_base', Abase, 8), ('O', O, 7), ('I_1', I1, 12), ('E1(S_1)', E1, 13)):
    ok, nl = certify(A, h + 1); bad, _ = certify(A, h + 1, corrupt=True)
    print(f'{name}: proof of no Sidon subset of size {h+1} verified by RUP: {ok} ({nl} lemmas); bare empty-clause proof accepted: {bad}')
