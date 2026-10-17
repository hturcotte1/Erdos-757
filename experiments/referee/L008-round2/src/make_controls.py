"""Referee round 2 (L008): control 3-graphs for the F7 / P3 / tau detectors.  Writes controls/controls.txt with lines
'FOUND: (a,b,c) ...' and controls/expected.txt with the expected (F7, P3-ok) flags computed from first principles here."""
import itertools, json, random
def aps(A):
    A = sorted(A); idx = {x: i for i, x in enumerate(A)}; S = set(A); E = []
    for i, j in itertools.combinations(range(len(A)), 2):
        if (A[i] + A[j]) % 2 == 0 and (A[i] + A[j]) // 2 in S:
            E.append(tuple(sorted((i, idx[(A[i] + A[j]) // 2], j))))
    return E
F7 = [(0,1,2),(0,3,4),(0,5,6),(1,3,5),(2,4,6)]
FANO = [(0,1,2),(0,3,4),(0,5,6),(1,3,5),(1,4,6),(2,3,6),(2,4,5)]
# AG(2,3): points (x,y) in Z3^2 -> 3x+y ; lines
pts = [(x, y) for x in range(3) for y in range(3)]
lines = set()
for p, q in itertools.combinations(pts, 2):
    d = ((q[0]-p[0]) % 3, (q[1]-p[1]) % 3)
    L = tuple(sorted(3*((p[0]+t*d[0]) % 3) + (p[1]+t*d[1]) % 3 for t in range(3)))
    lines.add(L)
AG = sorted(lines)
PASCH = [(0,1,2),(0,3,4),(1,3,5),(2,4,5)]
Abase = [0,136,200,243,246,249,272,286,298,323,400,528,596,1056]
C16 = sorted(Abase + [-323, 5000])
S12a = [0,269,385,467,501,511,521,523,535,538,549,575]
FIB = [2,3,5,8,13,21,34,55,89,144,233,377,610,987,1597,2584]
ctrl = []
def add(name, E, nv): ctrl.append((name, [tuple(e) for e in E], nv))
add('F7', F7, 7)
perm = list(range(16)); random.Random(1).shuffle(perm)
add('F7_relabelled_in_16', [tuple(sorted(perm[v] for v in e)) for e in F7], 16)
for i in range(5): add('F7_minus_edge%d' % i, [e for k, e in enumerate(F7) if k != i], 7)
add('Fano', FANO, 7); add('Fano_minus_line', FANO[:-1], 7)
add('AG23', AG, 9)
ag_minus_pt = [L for L in AG if 8 not in L]; add('AG23_minus_point', ag_minus_pt, 8)
ag_minus_2 = [L for L in AG if 8 not in L and 7 not in L]; add('AG23_minus_two_points', ag_minus_2, 7)
add('Pasch', PASCH, 6)
add('Abase_pattern', aps(Abase), 14); add('C16_pattern', aps(C16), 16); add('S12a_pattern', aps(S12a), 12); add('FIB16_pattern', aps(FIB), 16)
# F7 plus a pendant structure, F7 embedded in a larger graph with shifted labels
add('F7_shifted_plus_edges', [tuple(v+5 for v in e) for e in F7] + [(0,1,5),(2,3,6),(4,13,14)], 15)
# 13 vertices 12 edges P3-violation: L(13) minus one edge
L13 = [tuple(sorted(((i) % 13, (i+1) % 13, (i+3) % 13))) for i in range(13)]
add('L13', L13, 13); add('L13_minus_edge', L13[1:], 13)
def p3ok(E, nv):
    for r in range(2, nv+1):
        for S in itertools.combinations(range(nv), r):
            s = set(S)
            if sum(1 for e in E if set(e) <= s) > r - 2: return False
    return True
def hasf7(E, nv):
    Es = set(tuple(sorted(e)) for e in E)
    for p in itertools.permutations(range(nv), 7):
        if all(tuple(sorted(p[v] for v in e)) in Es for e in F7): return True
    return False
with open('controls/controls.txt', 'w') as f, open('controls/expected.txt', 'w') as g:
    for name, E, nv in ctrl:
        f.write('FOUND: ' + ' '.join('(%d,%d,%d)' % e for e in E) + '\n')
        if nv <= 13:
            exp = (hasf7(E, nv), p3ok(E, nv))
        else:
            exp = ('?', '?')
        g.write('%s nv=%d m=%d F7=%s P3ok=%s\n' % (name, nv, len(E), exp[0], exp[1]))
print(len(ctrl), 'controls written')
