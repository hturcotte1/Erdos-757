"""Observation 7 spot check (own code): for each class of the given lists, does some degree-3 vertex v give
K - v = triangle (6,3,2) + X with X of the stated cell, with the triangle carrying P1 and c,e (pattern (f), F1 = T)?"""
import sys, json
sys.path.insert(0, '/home/user/Erdos-757/experiments/referee/L020-round1-opus')
import hg
from roles_check import read_cell
from t3_check import check_vertex


def theta_vertex(n, es, t):
    s = hg.slack(n, len(es), t)
    d = hg.degrees(n, es)
    for v in range(n):
        if d[v] != 3:
            continue
        st = {}
        fails, pat, cells, ny = check_vertex(n, es, t, s, v, st)
        if pat != 'f' or fails:
            continue
        if (6, 3, 2, 2) not in cells:
            continue
        # which component carries the inside pair?
        P = [tuple(x for x in e if x != v) for e in es if v in e]
        rest = [x for x in range(n) if x != v]
        comps = hg.components(rest, [e for e in es if v not in e])
        tri = [vs for vs, ce in comps if len(vs) == 6 and len(ce) == 3][0]
        inside = [p for p in P if p[0] in tri and p[1] in tri]
        if len(inside) == 1:
            return v, cells
    return None, None


for path in sys.argv[1:]:
    if path.endswith('.json'):
        L = [(c['n'], c['m'], c['tau'], [tuple(e) for e in c['edges']]) for c in json.load(open(path))]
    else:
        L = [g for g in read_cell(path) if max(hg.degrees(g[0], g[3])) <= 3]
    hit = 0
    xcells = {}
    for n, m, t, es in L:
        v, cells = theta_vertex(n, es, t)
        if v is not None:
            hit += 1
            x = [c for c in cells if c != (6, 3, 2, 2)][0]
            xcells[x] = xcells.get(x, 0) + 1
    print(path.split('/')[-1], 'classes', len(L), 'with a Theta-vertex (triangle carries P1 and c,e)', hit, 'X cells', xcells, flush=True)
