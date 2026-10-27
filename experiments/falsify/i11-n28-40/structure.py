# For the lowest-slack CONNECTED graphs (beam pools, gluing, vext) find hub sets H (|H|<=3) whose deletion leaves only tight components (slack<=1);
# report n,m,tau,slack and the component types.  This tells how the near-tight connected graphs are assembled.
import gzip, json, itertools, collections, glob, sys
from common import *
cands = {}
for f in glob.glob('out/beam_d5*_pools.jsonl.gz'):
    for l in gzip.open(f, 'rt'):
        d = json.loads(l)
        if d['n'] >= 17 and d['slack'] <= 3:
            t = d['line'].split(' '); n = int(t[0]); es = [tuple(int(x) for x in w.split(',')) for w in t[2:]]
            cands[(n, tuple(sorted(es)))] = (d['slack'], n, es)
gd = json.load(open('out/glue_main.json'))['best']
for n, L in gd.items():
    for x in L:
        if x['slack'] <= 3 and 17 <= int(n) <= 44: cands[(int(n), tuple(sorted(tuple(e) for e in x['edges'])))] = (x['slack'], int(n), [tuple(e) for e in x['edges']])
def conn(n, es):
    par = list(range(n))
    def f(x):
        while par[x] != x: par[x] = par[par[x]]; x = par[x]
        return x
    for e in es:
        for v in e[1:]: par[f(v)] = f(e[0])
    return len(set(v for e in es for v in e)) == n and len(set(f(v) for v in range(n))) == 1
cands = {k: v for k, v in cands.items() if conn(v[1], v[2])}
print('candidates (connected)', len(cands), flush=True)
def comps_after(n, es, H):
    es2 = [e for e in es if not (set(e) & H)]
    par = {}
    def f(x):
        par.setdefault(x, x)
        while par[x] != x: par[x] = par[par[x]]; x = par[x]
        return x
    for e in es2:
        for v in e[1:]: par[f(v)] = f(e[0])
    cs = collections.defaultdict(list)
    for e in es2: cs[f(e[0])].append(e)
    return list(cs.values())
rows = []
for key, (s, n, es) in sorted(cands.items(), key=lambda kv: (kv[1][0], kv[1][1]))[:400]:
    found = None
    for h in (1, 2, 3):
        lines = []; owner = []
        for H in itertools.combinations(range(n), h):
            cs = comps_after(n, es, set(H))
            if not cs: continue
            for ce in cs:
                vs = sorted(set(v for e in ce for v in e)); mp = {v: i for i, v in enumerate(vs)}
                lines.append(line(len(vs), [tuple(mp[v] for v in e) for e in ce])); owner.append(H)
        res = run_eval(lines)
        byH = collections.defaultdict(list)
        for H, r in zip(owner, res): byH[H].append(r)
        for H, rs in byH.items():
            if all(r[3] <= 1 for r in rs): found = (h, H, sorted((r[0], r[1], r[2], r[3]) for r in rs)); break
        if found: break
    rows.append(dict(slack=s, n=n, m=len(es), found=found))
c = collections.Counter()
for r in rows:
    k = (r['slack'], None if not r['found'] else (r['found'][0], tuple(r['found'][2])))
    c[k] += 1
for k, v in sorted(c.items(), key=lambda kv: (kv[0][0], str(kv[0][1]))): print(v, k)
json.dump(rows, open('out/structure.json', 'w'))
