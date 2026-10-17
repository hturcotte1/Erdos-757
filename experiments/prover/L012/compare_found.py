"""Compare FOUND lists (union of the files in each group, groups separated by '--') as sets of labelled edge sets."""
import re, sys, gzip
def P(f):
    op = gzip.open if f.endswith('.gz') else open
    return [frozenset(tuple(sorted(map(int, t.split(',')))) for t in re.findall(r'\(([\d,]+)\)', l)) for l in op(f, 'rt') if l.startswith('FOUND:')]
groups = [[]]
for a in sys.argv[1:]:
    if a == '--': groups.append([])
    else: groups[-1].append(a)
sets = []
for g in groups:
    L = [x for f in g for x in P(f)]
    sets.append(set(L)); print(' + '.join(g), ': lines', len(L), 'distinct', len(set(L)))
print('all groups identical:', all(s == sets[0] for s in sets))
