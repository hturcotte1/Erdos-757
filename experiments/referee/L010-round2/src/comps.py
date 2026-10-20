"""Component structure (vertex count, edges, tau) of 3-graphs on NV vertices; lines '... (a,b,c) ...' or '-n' format."""
import sys, re, collections, itertools
NV = int(sys.argv[1]); fmt = sys.argv[2] if len(sys.argv) > 2 else 'paren'
def tau(es):
    vs = sorted({v for e in es for v in e})
    for k in range(0, len(vs) + 1):
        for S in itertools.combinations(vs, k):
            s = set(S)
            if all(s & set(e) for e in es): return k
cnt = collections.Counter()
for l in sys.stdin:
    l = l.split('|')[0]
    if fmt == 'paren': es = [tuple(map(int, t.split(','))) for t in re.findall(r'\(([\d,]+)\)', l)]
    else:
        a = list(map(int, l.split())); es = [tuple(a[1+3*i:4+3*i]) for i in range(a[0])]
    if not es: continue
    par = list(range(NV))
    def f(x):
        while par[x] != x: par[x] = par[par[x]]; x = par[x]
        return x
    for e in es: par[f(e[1])] = f(e[0]); par[f(e[2])] = f(e[0])
    comp = collections.defaultdict(list)
    for e in es: comp[f(e[0])].append(e)
    iso = sum(1 for v in range(NV) if f(v) == v and v not in {u for e in es for u in e})
    typ = sorted((len({v for e in c for v in e}), len(c), tau(c)) for c in comp.values()) + [(1, 0, 0)] * iso
    cnt[tuple(sorted(typ))] += 1
for k, v in sorted(cnt.items(), key=lambda x: -x[1]): print(v, k)
