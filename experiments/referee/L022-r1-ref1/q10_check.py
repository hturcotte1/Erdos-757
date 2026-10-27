# Referee check of L022 Theorem 5: Q10 = (10,7,4)#0 non-realizable (every labelling, even with extra APs),
# every proper edge subset realizable exactly; Q10 in C; tau = 4.
import sys, random, json
sys.path.insert(0, '.')
import rlib
from itertools import combinations

Q10 = [(0,1,2),(0,3,4),(1,5,7),(2,6,8),(3,7,9),(4,8,9),(5,6,9)]
n = 10
V = list(range(n))
out = {}
out['linear'] = rlib.is_linear(Q10)
out['F7free'] = rlib.is_F7_free(Q10)
out['P3'] = rlib.p3_ok(V, Q10)
out['tau'] = rlib.tau(Q10)
out['slack'] = rlib.slack(n, Q10)
out['degrees'] = sorted(rlib.degrees(V, Q10).values())
# structure claimed: v=9, pairs {3,7},{4,8},{5,6}; g12={0,3,4}, g13={1,7,5}, g23={2,8,6}; {0,1,2}
inc9 = [e for e in Q10 if 9 in e]
out['pairs_at_9'] = [sorted(set(e) - {9}) for e in inc9]

# exhaustive over ALL 3^7 labellings (including non-injective)
stat = {}
okl = []
for lab in rlib.labelings(Q10):
    st, basis, forced = rlib.analyse_labeling(n, lab)
    stat[st] = stat.get(st, 0) + 1
    if st == 'ok':
        okl.append(lab)
out['labelling_status_counts'] = stat
out['n_ok_labellings'] = len(okl)

# every proper edge subset (on the 10 vertices) realizable exactly, with explicit integer witness
rng = random.Random(7)
sub = {'checked': 0, 'exact_witness': 0, 'fail': []}
for k in range(0, 7):
    for S in combinations(range(7), k):
        E = [Q10[i] for i in S]
        if not E:
            sub['checked'] += 1; sub['exact_witness'] += 1
            continue
        r = rlib.realize(n, E, want_exact=True, rng=rng)
        sub['checked'] += 1
        if r['realizable'] and r['exact'] and r.get('point') is not None:
            pt = r['point']
            # independent re-check: brute force (4,5) and AP set equals E exactly
            A = set(frozenset(t) for t in rlib.ap_triples(pt))
            if A == set(frozenset(e) for e in E) and rlib.is_45_bruteforce(pt):
                sub['exact_witness'] += 1
            else:
                sub['fail'].append((S, 'witness mismatch'))
        else:
            sub['fail'].append((S, r.get('realizable'), r.get('exact')))
out['proper_subsets'] = sub
print(json.dumps(out, indent=1, default=str))
