"""C6 (L019): for given graphs (cell file, indices), list every fold at every degree-2 vertex and why it leaves C."""
import sys, itertools, collections
from hg import *
from check_folding import fold

path = sys.argv[1]; idxs = list(map(int, sys.argv[2].split(',')))
cells = read_cell(path)
for gi in idxs:
    n, m, t, E = cells[gi]; d = degrees(n, E)
    print('graph', gi, (n, m, t), 'Delta', max(d), 'degrees', d, 'edges', E)
    inE = set()
    for e in E:
        for a, b in itertools.permutations(e, 2): inE.add((a, b))
    for x in range(n):
        if d[x] != 2: continue
        e1, e2 = [e for e in E if x in e]
        out = []
        for u in [y for y in e1 if y != x]:
            for w in [y for y in e2 if y != x]:
                if (u, w) in inE: out.append('%d~%d:adj' % (u, w)); continue
                n2, E2 = fold(n, E, x, u, w)
                lin = linear(E2); f7 = has_f7(E2) if lin else False; pp = p3(E2)
                r = ('N' if not lin else '') + ('F' if f7 else '') + ('P' if not pp else '')
                if not pp:
                    r += '(tight %s)' % tight_set_exists(n, E, x, u, w)
                out.append('%d~%d:%s' % (u, w, r or 'inC'))
        print('  x=%d edges %s %s:' % (x, e1, e2), ' '.join(out))
