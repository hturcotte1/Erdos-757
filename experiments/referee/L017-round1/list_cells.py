# Referee L017 round 1: inventory of the stored refereed cell lists (independent parser).
import os, re, sys, json, collections
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cells')
pat = re.compile(r'cell_(\d+)_(\d+)_(\d+)_D(\d+)\.txt$')
def parse(path):
    graphs = []
    info = []
    with open(path) as fh:
        for line in fh:
            if line.startswith('FOUND:'):
                edges = [tuple(int(x) for x in t.split(',')) for t in re.findall(r'\(([^)]*)\)', line)]
                graphs.append(edges)
            elif line.startswith('INFO'):
                info.append(line.strip())
    return graphs, info
inv = collections.defaultdict(list)
for dirpath, _, files in os.walk(ROOT):
    for f in files:
        mm = pat.search(f)
        if not mm: continue
        n, m, t, D = map(int, mm.groups())
        g, info = parse(os.path.join(dirpath, f))
        maxdegs = []
        for edges in g:
            deg = collections.Counter(v for e in edges for v in e)
            maxdegs.append(max(deg.values()) if deg else 0)
        n3 = sum(1 for d in maxdegs if d <= 3)
        inv[(n, m, t)].append((D, len(g), n3, os.path.relpath(os.path.join(dirpath, f), ROOT), len(info)))
out = {}
for key in sorted(inv):
    out['%d_%d_%d' % key] = inv[key]
json.dump(out, open(os.path.join(os.path.dirname(ROOT), 'cell_inventory.json'), 'w'), indent=0)
print(len(inv), 'distinct (n,m,t) keys')
