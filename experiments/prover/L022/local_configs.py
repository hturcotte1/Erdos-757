"""Realizability (rexact.decide, all labellings) of the local configurations of patterns (b) and (f*) of L022 Theorem 2
with a single-edge side, and of their extensions by the edges of F1 at the attachment vertices.
Vertices: v=0; (b): x1,x2,x3 = 1,2,3; y1,y2,y3 = 4,5,6.  (f*): a,b,c,e = 1,2,3,4 in F1; d,f = 5,6; z = 7 (F2 = {d,f,z}).
usage: python3 local_configs.py"""
import sys
sys.path.insert(0, '/home/user/Erdos-757/experiments/20261027-0400-realize-21-18-9')
from rexact import decide
configs = {
 'b_E1_core': (7, [(0,1,4), (0,2,5), (0,3,6), (4,5,6)]),
 'b_E1_with_pendant_edges_at_x': (13, [(0,1,4), (0,2,5), (0,3,6), (4,5,6), (1,7,8), (2,9,10), (3,11,12)]),
 'b_E1_x_share_one_edge': (11, [(0,1,4), (0,2,5), (0,3,6), (4,5,6), (1,2,7), (3,8,9), (7,8,10)]),
 'f_E1_core': (8, [(0,1,2), (0,3,5), (0,4,6), (5,6,7)]),
 'F7': (7, [(0,1,2), (0,3,4), (0,5,6), (1,3,5), (2,4,6)]),
}
for name, (n, E) in configs.items():
    sols, st = decide(E, n, find_all=True, tlimit=600)
    labs = sorted({tuple(s[0]) for s in sols})
    print(name, 'n', n, 'm', len(E), 'realizable' if sols else 'NOT realizable', 'realizable labellings', len(sols),
          'prunes', st['prunes'], flush=True)
    if sols:
        print('   example labelling (a,mid,c):', sols[0][0])
