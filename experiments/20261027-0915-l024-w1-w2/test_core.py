"""Validate classes()/claimB_brute()/witness_U()/union_all_U() of w1.py against (i) the definition (all tuples of minimum transversals)
and (ii) the Claim-B configurations of pattern (a) (experiments/prover/L024/pattern_a3_poor_results.json: g + three pairs, 359 configs)."""
import sys, json, itertools, random, time
sys.argv = ['x']
sys.path.insert(0, '/home/user/Erdos-757/experiments/20261027-0915-l024-w1-w2')
from w1 import *
pieces = load_pieces(); by = {P['name']: P for P in pieces}
random.seed(7)
def add_clause(S, vs):
    m = 0
    for x in vs: m |= 1 << x
    row = [0] * S.k
    for x in vs: row[S.piece_of[x]] |= S.hitbits[S.piece_of[x]][x]
    S.chit.append(row); S.cmask.append(m)
    return len(S.chit) - 1
def defn(S, masks):
    """returns (exists_cover, union of all U covering, some covering exists?)"""
    exists = False; uni = 0
    for Ts in itertools.product(*S.MT):
        U = 0
        for T in Ts: U |= T
        if all(U & m for m in masks): exists = True; uni |= U
    return exists, uni
# (i) random clause sets on real pieces
bad = 0; cnt = 0
for names in [('(3,1,1)#0', '(8,5,3)#0', '(10,7,4)#1'), ('(8,5,3)#1', '(3,1,1)#0', '(3,1,1)#0'), ('(15,11,6)#0', '(8,5,3)#0')]:
    S = Setup([by[n] for n in names], need2=False)
    base = len(S.chit)
    for trial in range(300):
        nc = random.choice([1, 2, 3, 4])
        cl = []
        for _ in range(nc):
            sz = random.choice([1, 2, 3])
            cl.append(add_clause(S, random.sample(range(S.N), sz)))
        masks = [S.cmask[c] for c in cl]
        ex, uni = defn(S, masks)
        ok, U2 = S.union_all_U(cl)
        w = S.witness_U(cl)
        cnt += 1
        if ok != ex or (ok and U2 != uni) or ((w is not None) != ex) or (w is not None and not all(w & m for m in masks)) or S.claimB_brute(cl) == ex:
            bad += 1; print('CORE MISMATCH', names, masks, ex, ok, w)
print('random clause tests', cnt, 'bad', bad)
# (ii) pattern (a) positives
D = json.load(open('/home/user/Erdos-757/experiments/prover/L024/pattern_a3_poor_results.json'))
pos = 0; badp = 0
for c in D['configs']:
    names = c['types']; gt = c['g']; pairs = c['pairs']
    S = Setup([by[n] for n in names], need2=False)
    cl = [add_clause(S, gt)] + [add_clause(S, p) for p in pairs]
    pos += 1
    if not S.claimB_brute(cl): badp += 1
    # a negative control: drop the requirement by replacing one pair with its first vertex only -> must stay uncovered or covered, compare to definition
    masks = [S.cmask[x] for x in cl]
    ex, uni = defn(S, masks)
    if ex: badp += 1
print('pattern (a) positives', pos, 'not-Claim-B (should be 0)', badp)
