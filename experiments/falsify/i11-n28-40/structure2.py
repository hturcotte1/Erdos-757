# hub decomposition of the connected slack<=1 graphs found at n>=15: smallest vertex set H (|H|<=4) whose deletion leaves only components of slack<=1
import glob, json, itertools, collections, sys
from common import *
import gzip
seen = {}
for l in gzip.open('low_graphs.jsonl.gz', 'rt'):
    d = json.loads(l)
    if d['connected'] and d['n'] >= 15: seen['%d_%d_%d_%d' % (d['n'], d['m'], d['slack'], len(seen))] = (d['slack'], d['n'], [tuple(e) for e in d['edges']])
print('unique fp', len(seen), flush=True)
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
rows = []; cnt = collections.Counter(); ex = {}
byn = collections.defaultdict(list)
for fp, (s, n, es) in seen.items(): byn[(n, len(es), s)].append(es)
for key in sorted(byn):
    sample = byn[key][:25]
    for es in sample:
        n = key[0]; found = None
        for h in (1, 2, 3, 4):
            lines = []; owner = []
            for H in itertools.combinations(range(n), h):
                for ce in comps_after(n, es, set(H)):
                    vs = sorted(set(v for e in ce for v in e)); mp = {v: i for i, v in enumerate(vs)}
                    lines.append(line(len(vs), [tuple(mp[v] for v in e) for e in ce])); owner.append(H)
            res = run_eval(lines) if lines else []
            byH = collections.defaultdict(list)
            for H, r in zip(owner, res): byH[H].append(r)
            for H, rs in byH.items():
                if all(r[3] <= 1 for r in rs): found = (h, [sum(1 for e in es if v in e) for v in H], sorted((r[0], r[1], r[2], r[3]) for r in rs)); break
            if found: break
        k = (key, None if not found else (found[0], tuple(found[1]), tuple(found[2])))
        cnt[k] += 1
for k, v in sorted(cnt.items(), key=lambda kv: (kv[0][0][0], kv[0][0][2])): print(v, 'x', 'n,m,slack=', k[0], 'hubs,hubdeg,components=', k[1])
json.dump([[list(k[0]), k[1], v] for k, v in cnt.items()], open('out/structure2.json', 'w'))
