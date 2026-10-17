"""Read SURVIVOR lines (from filter_hits) and split them into connected / disconnected hypergraphs; write the connected ones as
FOUND lines and report counts (and, for the disconnected ones, their component sizes)."""
import re, sys, collections
def comps(es):
    parent = {}
    def find(x):
        while parent.setdefault(x, x) != x: x = parent[x]
        return x
    for e in es:
        for v in e[1:]: parent[find(v)] = find(e[0])
    c = collections.Counter(find(v) for e in es for v in e)
    sizes = collections.Counter()
    for e in es: sizes[find(e[0])] += 0
    return sorted(len({v for e in es for v in e if find(v) == r}) for r in c)
src, out = sys.argv[1], sys.argv[2]
conn = 0; disc = collections.Counter()
with open(out, 'w') as f:
    for l in open(src):
        if not l.startswith('SURVIVOR:'): continue
        es = [tuple(map(int, t.split(','))) for t in re.findall(r'\(([\d,]+)\)', l)]
        cs = comps(es)
        if len(cs) == 1: conn += 1; f.write('FOUND: ' + ' '.join('(%d,%d,%d)' % e for e in es) + '\n')
        else: disc[tuple(cs)] += 1
print(src, 'survivors: connected', conn, '| disconnected by component vertex counts', dict(disc))
