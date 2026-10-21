"""Optional: obtain a DRUP proof of 'no Sidon subset of size >= 39' from Glucose4 (pysat) on the own
CNF (sat_check.build) and check every lemma by reverse unit propagation with an own 2-watched-literal
checker (deletions ignored, which is sound). Usage: python3 drup_check.py <claim.json> <k>"""
import sys, time
sys.path.insert(0, '.')
from common import load_claim
from sat_check import build
from pysat.solvers import Solver

class RUP:
    def __init__(self):
        self.cls = []; self.watch = {}; self.units = []
    def add(self, c):
        c = list(dict.fromkeys(c))
        if any(-l in c for l in c):
            return                     # tautology: never needed
        if len(c) == 1:
            self.units.append(c[0]); return
        i = len(self.cls); self.cls.append(c)
        self.watch.setdefault(c[0], []).append(i); self.watch.setdefault(c[1], []).append(i)
    def implied(self, c):
        """True iff F & not(c) yields a conflict by unit propagation."""
        val = {}
        q = []
        def setlit(l):                 # make literal l true
            v = val.get(abs(l))
            if v is not None:
                return v == (l > 0)
            val[abs(l)] = (l > 0); q.append(-l)   # -l became false
            return True
        for l in c:
            if not setlit(-l):
                return True
        for u in self.units:
            if not setlit(u):
                return True
        def isfalse(l):
            v = val.get(abs(l)); return v is not None and v != (l > 0)
        def istrue(l):
            v = val.get(abs(l)); return v is not None and v == (l > 0)
        h = 0
        while h < len(q):
            fl = q[h]; h += 1          # literal fl is false
            ws = self.watch.get(fl, [])
            j = 0
            while j < len(ws):
                ci = ws[j]; cl = self.cls[ci]
                if cl[0] == fl:
                    cl[0], cl[1] = cl[1], cl[0]
                other = cl[0]
                if istrue(other):
                    j += 1; continue
                moved = False
                for k in range(2, len(cl)):
                    if not isfalse(cl[k]):
                        cl[1], cl[k] = cl[k], cl[1]
                        self.watch.setdefault(cl[1], []).append(ci)
                        ws[j] = ws[-1]; ws.pop(); moved = True; break
                if moved:
                    continue
                if isfalse(other):
                    return True        # conflict
                if not setlit(other):
                    return True
                j += 1
        return False

if __name__ == '__main__':
    raw, pts = load_claim(sys.argv[1]); A = sorted(pts); k = int(sys.argv[2])
    cnf, nF, top = build(A, k)
    t = time.time()
    with Solver(name='glucose4', bootstrap_with=cnf, with_proof=True) as s:
        res = s.solve(); proof = s.get_proof() if not res else None
    print('glucose4 k=%d -> %s in %.2fs; proof lines %s' % (k, 'SAT' if res else 'UNSAT', time.time() - t, None if proof is None else len(proof)))
    if res:
        sys.exit(1)
    chk = RUP()
    for c in cnf:
        chk.add(c)
    t = time.time(); nl = 0; empty = False
    for line in proof:
        toks = line.split()
        if not toks:
            continue
        if toks[0] == 'd':
            continue                   # deletions ignored (sound)
        lits = [int(x) for x in toks]
        assert lits[-1] == 0
        lits = lits[:-1]
        if not chk.implied(lits):
            print('LEMMA NOT RUP:', line); sys.exit(2)
        nl += 1
        if not lits:
            empty = True; break
        chk.add(lits)
    if not empty:
        empty = chk.implied([])
    print('checked %d lemmas by RUP in %.1fs; empty clause derived: %s' % (nl, time.time() - t, empty))
