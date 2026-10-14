import pickle, json, os
from collections import Counter
d = pickle.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'stats.pkl'), 'rb'))
R12, U12, R14 = d['R12'], d['U12'], d['R14']
keys = list(R12[0].keys())
out = []
inv = []
def fmt(c, tot):
    return ', '.join('%s:%d' % (k, c[k]) for k in sorted(c, key=str))
out.append('Counts: R12=%d realizable, U12=%d unrealizable (K31+core<=4 class), R14=%d realizable 14-point sets (partial census)\n' % (len(R12), len(U12), len(R14)))
for k in keys:
    cR, cU, c14 = (Counter(x[k] for x in L) for L in (R12, U12, R14))
    big = len(set(cR) | set(cU) | set(c14)) > 40
    out.append('### %s' % k)
    if big:
        out.append('(%d distinct values in R12, %d in U12, %d in R14; showing top 8 for R12 and fraction)' % (len(cR), len(cU), len(c14)))
        for name, c in (('R12', cR), ('U12', cU), ('R14', c14)):
            out.append('- %s top: %s' % (name, '; '.join('%s x%d' % (v, n) for v, n in c.most_common(8))))
        out.append('- R12 values not seen in U12: %d; U12 values not in R12: %d' % (len(set(cR) - set(cU)), len(set(cU) - set(cR))))
        continue
    vals = sorted(set(cR) | set(cU) | set(c14), key=str)
    out.append('| value | R12 | U12 | R14 |\n|---|---|---|---|')
    for v in vals:
        out.append('| %s | %d | %d | %d |' % (v, cR[v], cU[v], c14[v]))
    # candidate invariant: value set seen in realizable (n=12 and n=14)
    if k in ('degseq', 'roles', 'spans'): continue
    S12 = set(cR); S14 = set(c14); S = S12 | S14
    viol = sum(cU[v] for v in cU if v not in S)
    viol12 = sum(cU[v] for v in cU if v not in S12)
    inv.append(dict(stat=k, allowed_R12=sorted(S12, key=str), allowed_R14=sorted(S14, key=str), U12_excluded_by_union=viol,
                    U12_excluded_by_R12_only=viol12, R12_values_not_in_R14=sorted(S12 - S14, key=str),
                    R14_values_not_in_R12=sorted(S14 - S12, key=str)))
    if viol:
        out.append('**candidate invariant: %s in %s excludes %d of %d unrealizable**' % (k, sorted(S, key=str), viol, len(U12)))
open('tables.md', 'w').write('\n'.join(out))
json.dump(inv, open('invariants_scan.json', 'w'), indent=1, default=str)
print('\n'.join(l for l in out if 'candidate' in l or l.startswith('Counts')))
