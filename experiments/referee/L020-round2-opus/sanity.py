"""Sanity checks of the own routines: in_C on K29 (True), on F7 (False), on a P3-violating graph (False)."""
import json
from hgr2 import HG, in_C, has_F7, p3_hall, is_linear
d = json.load(open('/home/user/Erdos-757/experiments/prover/L020/K29_classes.json'))
E = [tuple(sorted(e)) for e in d[0]['edges']]; V = sorted(set(u for e in E for u in e))
print('K29 in C:', in_C(V, E), '| tau', HG(V, E).tau())
F7 = [(0,1,2),(0,3,4),(0,5,6),(1,3,5),(2,4,6)]
print('F7: linear', is_linear(F7), 'has_F7', has_F7(F7), 'in_C', in_C(range(7), F7))
# P3 violation: 4 edges on 5 vertices? impossible linear; use AG(2,3) minus a point-type dense piece: Fano-free dense linear graph
P = [(0,1,2),(0,3,4),(1,3,5),(2,4,5)]   # Pasch: 4 edges on 6 vertices, e = |S|-2 ok; add (0,5,6)? keep as positive control
print('Pasch (6 vertices, 4 edges) p3:', p3_hall(range(6), P))
Q = P + [(2,3,6),(1,4,6),(0,5,6)]  # 7 edges on 7 vertices: violates e(S) <= |S|-2
print('7 edges on 7 vertices p3:', p3_hall(range(7), Q))
