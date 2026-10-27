"""(L023) Falsification test of Proposition 6 on real (4,5)-sets: no judged claim set (results/claims/C*.json) and none of the explicit
realizable 21-point sets of (U4) (sets_21_19_9_realizable.json) contains Q8 among its APs."""
import sys, json, glob, itertools
sys.path.insert(0, '/home/user/Erdos-757')
from e757.core import ap_edges, is_45_set
from fractions import Fraction
def contains_q8(E, n):
    inc = [[] for _ in range(n)]
    for e in E:
        for v in e: inc[v].append(frozenset(e))
    for a in range(n):
        for ea in itertools.combinations(inc[a], 3):
            La = set().union(*ea) - {a}
            if len(La) != 6: continue
            for b in range(n):
                if b == a or b in La or len(inc[b]) < 3: continue
                for eb in itertools.combinations(inc[b], 3):
                    if set().union(*eb) - {b} == La: return True
    return False
def check(name, S):
    A = sorted(Fraction(str(x)) for x in S); idx = {x: i for i, x in enumerate(A)}
    E = [tuple(sorted(idx[v] for v in e)) for e in ap_edges(A)]
    return contains_q8(E, len(A)), len(A), len(E)
tot = hits = 0
for f in sorted(glob.glob('/home/user/Erdos-757/results/claims/C*.json')):
    c = json.load(open(f)); r = check(f, c['set']); tot += 1; hits += r[0]
    print('%s n=%d APs=%d contains Q8: %s' % (f.split('/')[-1], r[1], r[2], r[0]), flush=True)
for c in json.load(open('/home/user/Erdos-757/experiments/20261027-0400-realize-21-18-9/sets_21_19_9_realizable.json')):
    r = check('cls%d' % c['cls'], c['set']); tot += 1; hits += r[0]
print('SUMMARY sets %d containing Q8 %d' % (tot, hits))
