"""S7: sanity test of the only lemma the abstract cases use (K3+K4: in a (4,5)-set, Sidon == 3-AP-free, so
h = alpha of the 3-AP hypergraph) on generic gluings A_base u (q*B + t), n = 26, where h_brute is infeasible.
h_def: SAT with ALL sum-collision clauses (definition). alpha: SAT with ONLY the 3-AP clauses."""
import json, sys, time
from fractions import Fraction as F
sys.path.insert(0, '.')
from pysat.solvers import Solver
from pysat.card import CardEnc, EncType
from r3lib import A_BASE, is45_np, h_sat, ap_triples, is_sidon

t0 = time.time()


def alpha_ap(vals):
    vals = [F(v) for v in vals]
    idx = {v: i for i, v in enumerate(vals)}
    cl = [[-(idx[u] + 1), -(idx[m] + 1), -(idx[w] + 1)] for u, m, w in ap_triples(vals)]
    n = len(vals); k = 1; best = None
    while True:
        enc = CardEnc.atleast(lits=list(range(1, n + 1)), bound=k, top_id=n, encoding=EncType.seqcounter)
        with Solver(name='glucose4', bootstrap_with=cl + enc.clauses) as s:
            if not s.solve():
                return k - 1
        k += 1


D = json.load(open('/home/user/Erdos-757/data/small_records.json'))['sets']
A = [F(a) for a in A_BASE]
for key, q, t in (('12', F(1000003, 7919), F(10 ** 7)), ('12b', F(-104729, 1009), F(3 * 10 ** 6)), ('14', F(7, 3) + F(1, 999983), F(5 * 10 ** 5))):
    Bk = [F(v) for v in D[key]['set']]
    C = A + [q * b + t for b in Bk]
    assert len(set(C)) == len(C)
    ok = is45_np(C)
    hd, W = h_sat(C, start=12)
    al = alpha_ap(C)
    print('glue A_base u (q*%s + t): n=%d (4,5) %s | h_def(SAT, all sum collisions) %d | alpha(3-AP only) %d | h(A)+h(B) = %d | witness Sidon %s'
          % (key, len(C), ok, hd, al, 8 + D[key]['h'], is_sidon(W)))
print('time %.1fs' % (time.time() - t0))
