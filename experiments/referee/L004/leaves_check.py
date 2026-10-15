"""Referee L004, check L: per-prefix reflection consistency of the stored census (data only, own code).
For every prefix c:  leaves(c) [labelled patterns found below c, from the .done file]
                  == sol(c)    [canonical patterns output for c]
                   + #{P in census : P != refl P, prefix(refl P) == c}.
(Non-canonical leaves are not stored; if the search is complete they are exactly the mirrors of census patterns.)
A prefix whose search missed a non-canonical pattern Q (with refl Q found elsewhere), or a canonical P whose mirror was
counted elsewhere, violates its equation. Orbits missed entirely are not detected by this check."""
import gzip, json, os, collections
R = '/home/user/Erdos-757/experiments/20261014-1005-census-dfs/n14/results'
N = 14
pl = open(os.path.join(R, 'n14_m12_prefixes.txt')).read().split(); pidx = {p: q for q, p in enumerate(pl)}
expect = collections.Counter(); sol = collections.Counter(); sym = 0; orphan = 0
for q in range(len(pl)):
    for l in gzip.open(os.path.join(R, 'n14_m12_prefix_%05d.jsonl.gz' % q), 'rt'):
        es = sorted(tuple(e) for e in json.loads(l))
        sol[q] += 1
        r = sorted((N - 1 - k, N - 1 - j, N - 1 - i) for i, j, k in es)
        if r == es: sym += 1; continue
        bym = {e[1]: (e[0], e[2]) for e in r}
        c = ','.join('%d-%d' % bym[lv] for lv in (1, 2, 3))
        if c not in pidx: orphan += 1; continue
        expect[pidx[c]] += 1
bad = 0
for q in range(len(pl)):
    d = json.load(open(os.path.join(R, 'n14_m12_prefix_%05d.done' % q)))
    if int(d['leaves']) != sol[q] + expect[q]: bad += 1
print('prefixes', len(pl), 'symmetric', sym, 'mirrors in non-census cubes', orphan, 'prefixes violating the equation', bad)
