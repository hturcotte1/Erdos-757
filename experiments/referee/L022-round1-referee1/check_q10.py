# Referee check: Q10 = (10,7,4)#0 is non-realizable (even as a sub-hypergraph of the AP
# hypergraph of a (4,5)-set), and each of its 7 one-edge deletions is realizable exactly.
import random, json, sys
from rlib import tau, slack, is_linear, contains_F7, P3_ok, verts, degree, is_45_bruteforce
from realize import decide, ap_edges_of_points

Q10 = [(0, 1, 2), (0, 3, 4), (1, 5, 7), (2, 6, 8), (3, 7, 9), (4, 8, 9), (5, 6, 9)]
V = list(range(10))
print('Q10 edges', Q10)
print('degrees', [degree(Q10, x) for x in V])
print('tau', tau(Q10, V), 'slack', slack(Q10, V), 'linear', is_linear(Q10),
      'F7', contains_F7(Q10), 'P3', P3_ok(Q10, V))
ok, info = decide(Q10, 10, random.Random(7))
print('Q10 realizable (sub-hypergraph, any extra APs allowed):', ok, info.get('labellings_tried'), info.get('stats'))
# one-edge deletions
allok = True
for i in range(7):
    E = Q10[:i] + Q10[i + 1:]
    ok2, inf2 = decide(E, 10, random.Random(100 + i), want_exact=True)
    if ok2:
        pt = inf2['point']
        b = is_45_bruteforce(pt)
        exact = ap_edges_of_points(pt) == set(tuple(sorted(e)) for e in E)
        print('  delete', Q10[i], '-> exact realization', pt, 'bruteforce(4,5)', b, 'AP set == edges', exact)
        allok = allok and b and exact
    else:
        print('  delete', Q10[i], '-> NOT realizable', inf2)
        allok = False
print('all 7 one-edge deletions exactly realizable:', allok)
