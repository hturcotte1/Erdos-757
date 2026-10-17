"""Tests of the F7 detectors: (1) Lemma F (degree pattern 3,2^6 on a 7-vertex union) agrees with the definitional
test on ALL labelled linear 5-edge 3-graphs on [7]; (2) positive/negative controls; (3) prover's f7check.has_f7
agrees with ref_f7 on the same controls."""
import itertools, sys, importlib.util
sys.path.insert(0, '/home/user/Erdos-757/experiments/referee/L007-round1')
from ref_f7 import *
spec = importlib.util.spec_from_file_location('pf7', '/home/user/Erdos-757/experiments/prover/L007/indep/f7check.py')
pf7 = importlib.util.module_from_spec(spec); spec.loader.exec_module(pf7)
T = list(itertools.combinations(range(7), 3))
nlin = nF7 = agree = 0
for five in itertools.combinations(T, 5):
    if not is_linear(five): continue
    if len(set().union(*five)) != 7: continue
    nlin += 1
    a = has_f7(five)
    deg = {}
    for e in five:
        for v in e: deg[v] = deg.get(v, 0) + 1
    b = sorted(deg.values()) == [2,2,2,2,2,2,3]
    c = pf7.has_f7(list(five))
    nF7 += a
    agree += (a == b == c)
print('linear spanning 5-edge 3-graphs on [7]:', nlin, ' F7 copies (definitional):', nF7, ' all three tests agree:', agree == nlin)
# controls
fano = [(0,1,2),(0,3,4),(0,5,6),(1,3,5),(1,4,6),(2,3,6),(2,4,5)]
AG = [tuple(sorted((3*x+y) for (x,y) in L)) for L in [
      [(0,0),(0,1),(0,2)],[(1,0),(1,1),(1,2)],[(2,0),(2,1),(2,2)],[(0,0),(1,0),(2,0)],[(0,1),(1,1),(2,1)],[(0,2),(1,2),(2,2)],
      [(0,0),(1,1),(2,2)],[(0,1),(1,2),(2,0)],[(0,2),(1,0),(2,1)],[(0,0),(1,2),(2,1)],[(0,1),(1,0),(2,2)],[(0,2),(1,1),(2,0)]]]
assert is_linear(AG) and len(AG) == 12
AGm1 = [e for e in AG if 8 not in e]
AGm2 = [e for e in AG if 8 not in e and 7 not in e]
D14 = [(0,1,2),(3,5,6),(0,3,13),(1,5,13),(2,6,13),(4,7,8),(4,9,10),(7,9,11),(8,9,12),(10,11,12),(2,3,4)]
ctrl = dict(F7=(F7, True), fano=(fano, False), AG23=(AG, True), AG_minus_1=(AGm1, True), AG_minus_2=(AGm2, True), D14=(D14, True),
            fano_minus_2_lines=([e for e in fano if e not in [(0,1,2),(0,3,4)]], False),
            F7_minus_edge=(F7[:4], False), L13=([tuple(sorted(((i)%13,(i+1)%13,(i+3)%13))) for i in range(13)], False))
for k, (es, want) in ctrl.items():
    a = has_f7(es); c = pf7.has_f7(es)
    print(k, 'linear', is_linear(es), 'ref_f7', a, 'prover', c, 'expected', want, 'OK' if a == want == c else 'FAIL')
print('D14 F7 copies:', f7_copies(D14))
