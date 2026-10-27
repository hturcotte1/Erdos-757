# collect all slack<=1 graphs found anywhere (out/low_*.txt, beam low files), dedupe up to isomorphism (WL hash + networkx isomorphism),
# classify connected components, write low_graphs.jsonl.gz and a summary json.
import glob, gzip, json, collections, sys, re
import networkx as nx
from common import *
files = sorted(glob.glob('out/low_*.txt') + glob.glob('out/beam_*_low.txt'))
raw = []
for f in files:
    for l in open(f):
        l = l.strip()
        if not l or l.startswith('NEG'): continue
        t = l.split(' ')
        # formats: "slack n m tau TAG n m edges..." (TAG or fp hex)
        try:
            s, n, m, tau = int(t[0]), int(t[1]), int(t[2]), int(t[3]); gl = ' '.join(t[5:])
        except Exception: continue
        raw.append((s, n, m, tau, gl, f))
print('raw', len(raw))
def graph_edges(gl):
    t = gl.split(' '); n = int(t[0]); es = [tuple(int(x) for x in w.split(',')) for w in t[2:]]; return n, es
def inc_graph(n, es):
    G = nx.Graph()
    for v in range(n): G.add_node(('v', v), t='v')
    for i, e in enumerate(es):
        G.add_node(('e', i), t='e')
        for v in e: G.add_edge(('v', v), ('e', i))
    return G
buckets = collections.defaultdict(list); uniq = []
for s, n, m, tau, gl, f in raw:
    if n < 15: continue
    nn, es = graph_edges(gl); G = inc_graph(nn, es)
    h = (n, m, tau, nx.weisfeiler_lehman_graph_hash(G, node_attr='t', iterations=5)); dup = False
    for G2 in buckets[h]:
        if nx.is_isomorphic(G, G2, node_match=lambda a, b: a['t'] == b['t']): dup = True; break
    if dup: continue
    buckets[h].append(G); uniq.append((s, n, m, tau, nn, es, f, h[3]))
print('unique n>=15', len(uniq))
def comps(n, es):
    par = list(range(n))
    def f(x):
        while par[x] != x: par[x] = par[par[x]]; x = par[x]
        return x
    for e in es:
        for v in e[1:]: par[f(v)] = f(e[0])
    cs = collections.defaultdict(list)
    for e in es: cs[f(e[0])].append(e)
    iso = sum(1 for v in range(n) if all(v not in e for e in es))
    return list(cs.values()), iso
out = []; summ = collections.Counter(); pieces = collections.Counter()
for s, n, m, tau, nn, es, f, wl in uniq:
    cs, iso = comps(nn, es); cinfo = []
    lines = []
    for ce in cs:
        vs = sorted(set(v for e in ce for v in e)); mp = {v: i for i, v in enumerate(vs)}
        lines.append(line(len(vs), [tuple(mp[v] for v in e) for e in ce]))
    res = run_eval(lines) if lines else []
    cinfo = [(r[0], r[1], r[2], r[3]) for r in res]
    out.append(dict(slack=s, n=n, m=m, tau=tau, connected=(len(cs) == 1 and iso == 0), n_components=len(cs), isolated=iso, components=cinfo, src=f, wl_hash=wl, edges=[list(e) for e in es]))
    summ[(s, n if len(cs) == 1 and iso == 0 else None, 'conn' if (len(cs) == 1 and iso == 0) else 'disc')] += 1
with gzip.open('low_graphs.jsonl.gz', 'wt') as fo:
    for d in out: fo.write(json.dumps(d) + '\n')
conn = [d for d in out if d['connected']]
print('connected unique:', len(conn))
c = collections.Counter((d['slack'], d['n'], d['m'], d['tau']) for d in conn)
for k in sorted(c, key=lambda k: (k[1], k[0])): print(k, c[k])
json.dump(dict(raw=len(raw), unique=len(uniq), connected=len(conn), connected_cells={str(k): v for k, v in c.items()},
               disconnected_component_types=dict(collections.Counter(tuple(sorted(map(tuple, d['components']))) for d in out if not d['connected']).most_common(40)) if False else None), open('low_summary.json', 'w'), indent=1)
