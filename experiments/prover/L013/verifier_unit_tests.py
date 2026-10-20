"""(L013, prover) Unit tests of the pure-Python verifier of check_cells.py on positive and negative examples."""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from check_cells import verify, has_f7, p3, tau_exact, parse_edges
F7 = [(0,1,2),(0,3,4),(0,5,6),(1,3,5),(2,4,6)]
fano = [(0,1,2),(0,3,4),(0,5,6),(1,3,5),(1,4,6),(2,3,6),(2,4,5)]
ab = parse_edges(open(os.path.join(HERE, '..', 'L012', 'abase_pattern.txt')).read())
grid = [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8)]; ag_minus_class = grid + [(0,4,8),(1,5,6),(2,3,7)]
F7b = [(6,5,4),(6,3,2),(6,1,0),(5,3,1),(4,2,0),(0,7,8)]
tests = [('F7', verify(F7, 7, 5, 3, 3), 'F7'),
         ('Fano plane', verify(fano, 7, 7, 3, 3), 'P3'),
         ('A_base pattern (14,12,6), D=4', verify(ab, 14, 12, 6, 4), None),
         ('A_base pattern with t=5', verify(ab, 14, 12, 5, 4), 'tau'),
         ('A_base pattern with D=3', verify(ab, 14, 12, 6, 3), 'degree'),
         ('two disjoint edges', verify([(0,1,2),(3,4,5)], 6, 2, 2, 1), 'disconnected'),
         ('non-linear', verify([(0,1,2),(0,1,3),(2,3,4)], 5, 3, 2, 3), 'nonlinear'),
         ('F7 relabelled plus a pendant edge', verify(F7b, 9, 6, 3, 3), 'F7'),
         ('3x3 grid (6 lines)', verify(grid, 9, 6, 3, 3), None),
         ('AG(2,3) minus one parallel class', verify(ag_minus_class, 9, 9, tau_exact(ag_minus_class), 3), 'P3')]
bad = 0
for name, got, want in tests:
    ok = got == want; bad += not ok
    print('%-40s verdict %-14s expected %-14s %s' % (name, got, want, 'OK' if ok else 'FAIL'))
print('AG(2,3) minus a class contains F7:', has_f7(ag_minus_class), '(expected False: F7 needs all four parallel classes)')
print('failures:', bad)
