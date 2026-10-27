#!/usr/bin/env python3
"""Aggregate out/summary_15_m.txt (redmin) and out/hits_15_m.tsv into results.json, tables.md and the saved graph lists."""
import glob, re, json, gzip, os, collections
HERE = os.path.dirname(os.path.abspath(__file__))
res = {}; hard = []; ge7 = []; ge6 = []; redfree = []
for f in sorted(glob.glob(os.path.join(HERE, 'out', 'summary_15_*.txt'))):
    m = int(re.findall(r'summary_15_(\d+)', f)[0]); s = open(f).read().strip()
    if 'hist=' not in s: continue
    d = dict(re.findall(r'(\w+)=(-?\d+)', s.split('hist=')[0])); d = {k: int(v) for k, v in d.items()}
    hist = collections.Counter(); 
    for tok in s.split('hist=')[1].split(','):
        if tok: a, b, c = map(int, tok.split(':')); hist[(a, b)] += c
    bysz = collections.Counter(); bysz_le5 = collections.Counter()
    for (ms, sl), c in hist.items():
        bysz[ms] += c
        if sl <= 5: bysz_le5[ms] += c
    d['n'] = 15; d['m'] = m
    d['dist_min_Z'] = {str(k): v for k, v in sorted(bysz.items())}
    d['dist_min_Z_slack_le5'] = {str(k): v for k, v in sorted(bysz_le5.items())}
    d['hist_minZ_slack'] = {f'{a},{b}': c for (a, b), c in sorted(hist.items())}
    d['min_slack_by_minZ'] = {str(a): min(b for (x, b) in hist if x == a) for a in sorted(set(a for a, _ in hist))}
    res[str(m)] = d
    h = os.path.join(HERE, 'out', f'hits_15_{m}.tsv')
    if os.path.exists(h):
        for l in open(h):
            t = l.rstrip('\n').split('\t'); n_, m_, tau, sl, ms = map(int, t[:5]); g = t[6]
            row = (m_, tau, sl, ms, g)
            if ms >= 6: ge6.append(row)
            if ms >= 7: ge7.append(row)
            if ms == 99: redfree.append(row)
res['total_classes'] = sum(r['cls'] for r in res.values() if isinstance(r, dict) and 'cls' in r)
res['total_redfree'] = sum(r['redfree'] for r in res.values() if isinstance(r, dict) and 'cls' in r)
res['max_minZ_overall'] = max(r['maxminsz'] for r in res.values() if isinstance(r, dict) and 'cls' in r)
res['n_minZ_ge6'] = len(ge6); res['n_minZ_ge7'] = len(ge7)
res['n_minZ_ge7_slack_le5'] = sum(1 for r in ge7 if r[2] <= 5)
res['n_minZ_ge6_slack_le5'] = sum(1 for r in ge6 if r[2] <= 5)
res['minZ_ge7_by_cell_slack'] = {f'm={a},slack={b},minZ={c}': v for (a, b, c), v in sorted(collections.Counter((r[0], r[2], r[3]) for r in ge7).items())}
json.dump(res, open(os.path.join(HERE, 'results.json'), 'w'), indent=1)
def dump(name, rows, hdr):
    with gzip.open(os.path.join(HERE, 'graphs', name), 'wt') as g:
        g.write(hdr + '\n')
        for r in rows: g.write(f'{r[0]}\t{r[1]}\t{r[2]}\t{r[3]}\t{r[4]}\n')
H = '# connected members of C, Delta<=3, n=15; columns: m tau slack minZ graph (canonical nauty edge list "C m a.b.c ..." ); minZ = smallest |Z| of a (Red) pair'
dump('n15_minZ_ge6.tsv.gz', ge6, H); dump('n15_minZ_ge7.tsv.gz', ge7, H)
dump('n15_minZ_ge6_slack_le5.tsv.gz', [r for r in ge6 if r[2] <= 5], H)
# table
with open(os.path.join(HERE, 'tables.md'), 'w') as t:
    t.write('Table: n=15 census cells (connected, Delta<=3, in C, up to isomorphism), smallest |Z| of a (Red) pair\n\n')
    t.write('| m | d | classes | Red-free | slack range | max min|Z| | min|Z|=2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | >=10 |\n|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|\n')
    for m in sorted(int(k) for k in res if k.isdigit()):
        r = res[str(m)]; dd = {int(k): v for k, v in r['dist_min_Z'].items()}
        t.write(f"| {m} | {15-m} | {r['cls']} | {r['redfree']} | {r['minslack']}..{r['maxslack']} | {r['maxminsz']} | " + ' | '.join(str(dd.get(k, 0)) for k in range(2, 10)) + f" | {sum(v for k, v in dd.items() if 10 <= k < 99)} |\n")
    t.write('\nSlack <= 5 classes by min|Z|:\n\n')
    for m in sorted(int(k) for k in res if k.isdigit()):
        t.write(f"* m={m}: {res[str(m)]['dist_min_Z_slack_le5']}\n")
    t.write('\nClasses with min|Z| >= 7 by (m, slack, min|Z|): ' + json.dumps(res['minZ_ge7_by_cell_slack']) + '\n')
print(json.dumps({k: v for k, v in res.items() if not isinstance(v, dict)}))
for m in sorted(int(k) for k in res if k.isdigit()): print(m, res[str(m)]['cls'], res[str(m)]['redfree'], res[str(m)]['maxminsz'], res[str(m)]['minslack'], res[str(m)]['dist_min_Z'])
