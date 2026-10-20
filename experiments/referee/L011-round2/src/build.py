"""Referee L011 r2: class-level inputs = disjoint unions of class representatives (my genbg + rf in-C lists, or all Delta<=3
classes with --all), components on consecutive vertex blocks; repeated cell types as multisets.  'I' = isolated point (vertex 0
block of size 1), 'AP' = single edge.  Output format "m a b c ...".  Usage: python3 -I build.py OUT [--all] TYPE TYPE ..."""
import sys, re
from itertools import combinations_with_replacement, product
def load(cell, allmode):
    n, m, t = cell
    fn = 'out/%s_%d_%d_%d%s.txt' % ('g' if allmode else 'gC', n, m, t, '_d3' if allmode else '')
    L = []
    for ln in open(fn):
        E = [tuple(map(int, x)) for x in re.findall(r'\((\d+),(\d+),(\d+)\)', ln)]
        if E: assert len(E) == m and max(max(e) for e in E) < n; L.append(E)
    return L
out = sys.argv[1]; args = sys.argv[2:]; allmode = '--all' in args; args = [a for a in args if a != '--all']
types = []
for a in args:
    if a == 'I': types.append(('I', None))
    elif a == 'AP': types.append(('AP', None))
    else: types.append(('C', tuple(map(int, a.split(',')))))
# group identical cells for multisets
groups = {}
for kind, cell in types:
    key = (kind, cell); groups[key] = groups.get(key, 0) + 1
choices = []
for (kind, cell), k in groups.items():
    if kind == 'I': choices.append([[('I', None)] * k])
    elif kind == 'AP': choices.append([[('AP', None)] * k])
    else:
        L = load(cell, allmode)
        choices.append([[('C', (cell, L[i])) for i in combo] for combo in combinations_with_replacement(range(len(L)), k)])
cnt = 0
with open(out, 'w') as f:
    for pick in product(*choices):
        comps = [c for grp in pick for c in grp]
        # order: I first, then APs, then cells (any fixed order is fine)
        comps.sort(key=lambda c: {'I': 0, 'AP': 1, 'C': 2}[c[0]])
        edges = []; base = 0
        for kind, data in comps:
            if kind == 'I': base += 1
            elif kind == 'AP': edges.append((base, base + 1, base + 2)); base += 3
            else:
                (n, m, t), E = data
                edges += [(a + base, b + base, c + base) for (a, b, c) in E]; base += n
        f.write('%d %s\n' % (len(edges), ' '.join('%d %d %d' % e for e in edges))); cnt += 1
print(out, 'inputs', cnt, 'vertices', base)
