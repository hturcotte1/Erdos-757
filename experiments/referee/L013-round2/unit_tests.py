import subprocess, itertools
A = [0,136,200,243,246,249,272,286,298,323,400,528,596,1056]
idx = {a: i for i, a in enumerate(A)}
aps = sorted(tuple(sorted((idx[a], idx[(a + c) // 2], idx[c]))) for a, c in itertools.combinations(A, 2) if (a + c) % 2 == 0 and (a + c) // 2 in idx)
tests = {
 'F7 (expect F7=1)': (7, [(0,1,2),(0,3,4),(0,5,6),(1,3,5),(2,4,6)]),
 'F7 relabelled + pendant (expect F7=1)': (9, [(6,5,4),(6,3,2),(6,1,0),(5,3,1),(4,2,0),(0,7,8)]),
 'Fano (expect P3=0)': (7, [(0,1,2),(0,3,4),(0,5,6),(1,3,5),(1,4,6),(2,3,6),(2,4,5)]),
 'A_base (expect in C, tau=6, 12 edges)': (14, aps),
 'grid 3x3 lines rows+cols (expect P3=1, F7=0)': (9, [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8)]),
 'AG(2,3) minus parallel class (9 lines, expect P3=0)': (9, [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(1,5,6),(2,3,7)]),
 'two disjoint edges (expect connected=0)': (6, [(0,1,2),(3,4,5)]),
 'nonlinear (expect linear=0)': (5, [(0,1,2),(0,1,3)]),
 'P3 tight: 4 edges on 6 vertices? K4-like (0,1,2),(0,3,4),(1,3,5),(2,4,5) (expect P3=1? e=4 n=6 -> 4<=4)': (6, [(0,1,2),(0,3,4),(1,3,5),(2,4,5)]),
 '5 edges on 6 vertices (expect P3=0, nonlinear maybe)': (6, [(0,1,2),(0,3,4),(1,3,5),(2,4,5),(0,5,1)]),
}
for name, (n, es) in tests.items():
    inp = 'X: ' + ' '.join('(%d,%d,%d)' % e for e in es) + '\n'
    out = subprocess.run(['./bin/refx', 'check', str(n), 'brute'], input=inp, capture_output=True, text=True).stdout.strip()
    print(name, '->', out)
