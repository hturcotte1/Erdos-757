"""Build extension inputs (lines "m a b c ...") as disjoint unions of labelled components, written for certificate L009.
Usage: combine.py OUT NAME1:FILE1[:TAG] NAME2:FILE2[:TAG] ...   where each argument is a component slot:
  'AP'               a single edge (one fixed labelled copy);
  'ISO'              an isolated vertex;
  'FILE[:TAG]'       every hypergraph on the lines of FILE starting with TAG: (default FOUND), all labelled copies.
The output is the Cartesian product over the slots (components placed on consecutive vertex blocks in slot order)."""
import re, sys, itertools
def load(spec):
    if spec == 'AP': return [[(0, 1, 2)]], 3
    if spec == 'ISO': return [[]], 1          # an isolated vertex (one vertex, no edge)
    f, tag = (spec.split(':') + ['FOUND'])[:2]
    L = []
    for l in open(f):
        if l.startswith(tag + ':'):
            L.append([tuple(map(int, t.split(','))) for t in re.findall(r'\(([\d,]+)\)', l)])
    nv = max(max(max(e) for e in es) for es in L) + 1
    assert all(set().union(*es) == set(range(nv)) for es in L), spec
    return L, nv
out = sys.argv[1]; slots = [load(s) for s in sys.argv[2:]]
cnt = 0
with open(out, 'w') as f:
    for combo in itertools.product(*[s[0] for s in slots]):
        es = []; off = 0
        for (L, nv), comp in zip(slots, combo):
            es += [tuple(v + off for v in e) for e in comp]; off += nv
        f.write('%d ' % len(es) + ' '.join('%d %d %d' % e for e in es) + '\n'); cnt += 1
print(out, 'graphs:', cnt, 'vertices:', off, 'slot sizes:', [len(s[0]) for s in slots])
