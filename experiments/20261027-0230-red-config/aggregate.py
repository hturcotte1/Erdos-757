#!/usr/bin/env python3
"""Aggregate out/red_<n>_<m>.tsv (output of bin/redfree) into results.json and the gz lists of Red_k-free graphs.
Columns of the tsv: 1 n,2 m,3 tau,4 slack,5 maxdeg,6 redfree(1=no (Red) pair at all),7 best value,8 |Z*|,9 e(Z*),10 tau(E_Z*),11 Z* mask,12 T* mask,
13 degree histogram,14 min |Z| over all (Red) Z,15 mask of one such Z,16 min |Z| over R-connected (Red) Z (equals col 14),17 mask,
18 e(Z_min),19 tau(E_Z_min),20 degrees of the vertices of Z_min, then the graph ("C m a.b.c ...")."""
import glob, re, json, gzip, collections, os
HERE = os.path.dirname(os.path.abspath(__file__))
KS = [2, 3, 4, 5, 6, 7, 8]
res = {}; types = collections.Counter(); lists = {k: [] for k in (4, 5, 6)}
for f in sorted(glob.glob(os.path.join(HERE, 'out', 'red_*_*.tsv'))):
    n, m = map(int, re.findall(r'red_(\d+)_(\d+)', f)[0])
    cls = 0; rf = 0; kfree = collections.Counter(); slk = collections.defaultdict(list); hard = 0; bestmin = 10**9
    sl_all = []
    for l in open(f):
        t = l.rstrip('\n').split('\t'); cls += 1
        rf += int(t[5]); mz = int(t[13]); sl = int(t[3])
        sl_all.append(sl)
        for k in KS:
            if mz > k:
                kfree[k] += 1; slk[k].append(sl)
        for k in lists:
            if mz > k: lists[k].append(t[-1].strip())
        if int(t[2]) > 0 and mz < 99: types[(n >= 0, mz, int(t[17]), int(t[18]), t[19])] += 1
    res[f'{n},{m}'] = dict(n=n, m=m, classes=cls, redfree=rf, redk_free={k: kfree[k] for k in KS},
                           min_slack_redk_free={k: (min(slk[k]) if slk[k] else None) for k in KS},
                           slack_min=min(sl_all), slack_max=max(sl_all))
tot = collections.defaultdict(lambda: collections.Counter())
for key, r in res.items():
    tot[r['n']]['classes'] += r['classes']; tot[r['n']]['redfree'] += r['redfree']
    for k in KS: tot[r['n']][f'k{k}'] += r['redk_free'][k]
res['totals_by_n'] = {n: dict(c) for n, c in sorted(tot.items())}
res['types_of_minimal_Z'] = {f'|Z|={k[1]},e(Z)={k[2]},tau(E_Z)={k[3]},deg(Z)={k[4]}': v for k, v in sorted(types.items(), key=lambda kv: -kv[1])[:60]}
json.dump(res, open(os.path.join(HERE, 'results.json'), 'w'), indent=1)
for k, L in lists.items():
    with gzip.open(os.path.join(HERE, f'redk{k}_free_graphs.txt.gz'), 'wt') as g:
        g.write('# connected members of class C with max degree <= 3 and NO (Red) pair (Z,T) with |Z| <= %d (R-connected Z); canonical (nauty) edge lists "C m a.b.c ..."; vertex count = 1 + max label (graphs have no isolated vertices)\n' % k)
        for x in L: g.write(x + '\n')
print(json.dumps(res['totals_by_n'], indent=0))
