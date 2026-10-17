"""(L011) Like connected_filter.py (L009), but the vertex set is {0,...,N-1} given on the command line, so a vertex in no edge counts as
its own component (needed when an input contains an isolated vertex).  Reads SURVIVOR lines, writes the connected ones as FOUND
lines, and reports the multiset of component vertex counts of the disconnected ones, and the maximum degree of the connected ones.
Usage: connected_filter2.py SRC OUT N"""
import re, sys, collections
src, out, N = sys.argv[1], sys.argv[2], int(sys.argv[3])
conn = 0; disc = collections.Counter(); maxdeg = collections.Counter(); bad = 0
with open(out, 'w') as f:
    for l in open(src):
        if not l.startswith('SURVIVOR:'): continue
        es = [tuple(map(int, t.split(','))) for t in re.findall(r'\(([\d,]+)\)', l)]
        if max(max(e) for e in es) >= N: bad += 1
        parent = list(range(N))
        def find(x):
            while parent[x] != x: parent[x] = parent[parent[x]]; x = parent[x]
            return x
        for e in es:
            for v in e[1:]: parent[find(v)] = find(e[0])
        sizes = sorted(collections.Counter(find(v) for v in range(N)).values())
        if len(sizes) == 1:
            conn += 1; f.write('FOUND: ' + ' '.join('(%d,%d,%d)' % e for e in es) + '\n')
            d = collections.Counter(v for e in es for v in e); maxdeg[max(d.values())] += 1
        else: disc[tuple(sizes)] += 1
print(src, 'N =', N, 'survivors: connected', conn, '(max degree of connected:', dict(maxdeg), ') | disconnected by component vertex counts',
      dict(disc), '| labels >= N:', bad)
