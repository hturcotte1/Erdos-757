import json, glob, re, collections, os, gzip
R = {}
# ---- growth ----
g = collections.defaultdict(lambda: dict(tried=0, ok=0, minslack=10**9, cells={}))
for K in (1, 4, 10):
    for l in open('out/grow_K%d.txt' % K):
        m = re.match(r'GROW n=(\d+) m=(\d+) K=(\d+) tried=(\d+) ok=(\d+) minslack=(-?\d+)', l)
        if not m: continue
        n, mm, k, t, ok, ms = map(int, m.groups())
        d = g[(n, k)]; d['tried'] += t; d['ok'] += ok; d['minslack'] = min(d['minslack'], ms); d['cells'][mm] = ms
R['growth'] = {'%d_K%d' % k: dict(tried=v['tried'], ok=v['ok'], minslack=v['minslack'], min_slack_by_m=v['cells']) for k, v in sorted(g.items())}
R['growth_samples_K1_total'] = sum(v['ok'] for k, v in g.items() if k[1] == 1)
# ---- gluing ----
gd = json.load(open('out/glue_main.json'))
R['glue'] = dict(total_generated=gd['total'], per_n={n: dict(generated=v['generated'], in_C=v['inC'], min_slack_any=v['minslack']) for n, v in gd['per_n'].items() if 20 <= int(n) <= 52},
                 min_connected_slack_by_n={n: v[0]['slack'] for n, v in sorted(gd['best'].items(), key=lambda kv: int(kv[0]))}, n_slack_le1_connected=gd['n_low'])
R['glue_exhaustive'] = json.load(open('out/glue_exh.json'))
# ---- extension ----
cells = {}
for l in open('out/ext_out.txt'):
    p = l.split()
    if p and p[0] == 'CELL': cells[(int(p[1]), int(p[2]))] = int(p[4])
    if p and p[0] == 'EXTEND': R['extend_summary'] = l.strip()
mn = collections.defaultdict(lambda: 999)
for (n, m), s in cells.items(): mn[n] = min(mn[n], s)
R['extend_min_slack_by_n'] = dict(sorted(mn.items()))
# ---- beam ----
R['beam'] = {}
for f in sorted(glob.glob('out/beam_*_stats.json')):
    d = json.load(open(f)); R['beam'][os.path.basename(f)[5:-11]] = {n: dict(pool_connected=v['pool'], min_connected_slack=v['minslack']) for n, v in d.items() if int(n) >= 14}
# ---- SA ----
R['sa_cells'] = []
for l in open('out/sa_cellsA.log'):
    p = l.split()
    if len(p) >= 9 and p[2] == 'lo': R['sa_cells'].append(dict(n=int(p[0]), m=int(p[1]), lo=int(p[3]), best_slack=int(p[5]), tau=int(p[7]), evals=int(p[9])))
R['sa_polish'] = [eval(l) for l in open('out/sa2_polA.log') if l.startswith('{')]
R['subsa'] = [x for f in glob.glob('out/subsa_*.json') for x in json.load(open(f))]
for f in glob.glob('out/real_*.json'): R.setdefault('real', {})[os.path.basename(f)] = json.load(open(f))
json.dump(R, open('results.json', 'w'), indent=1, default=str)
print('written results.json')
