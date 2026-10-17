import subprocess, sys, itertools
sys.path.insert(0, 'src'); from h2g6 import to_g6
def run(nv, edges, t, D):
    g = to_g6(nv, edges)
    out = subprocess.run(['./bin/hfilt', str(nv), str(len(edges)), str(t), str(D), 'print'], input=g + '\n', capture_output=True, text=True).stdout
    return out.strip().splitlines()[-1]
F7 = [(0,1,2),(0,3,4),(0,5,6),(1,3,5),(2,4,6)]
fano = [(0,1,2),(0,3,4),(0,5,6),(1,3,5),(1,4,6),(2,3,6),(2,4,5)]
pts = [(x, y) for x in range(3) for y in range(3)]
lines = set()
for p in pts:
    for d in [(0,1),(1,0),(1,1),(1,2)]:
        lines.add(tuple(sorted(3*((p[0]+k*d[0])%3)+((p[1]+k*d[1])%3) for k in range(3))))
lines = sorted(lines)
# AG(2,3) minus points 7 and 8 -> relabel
rem = [l for l in lines if 7 not in l and 8 not in l]
abase = [0,136,200,243,246,249,272,286,298,323,400,528,596,1056]
ap = [(i,j,k) for i,j,k in itertools.combinations(range(14),3) if abase[i]+abase[k]==2*abase[j]]
grid = [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8)]
# relabelled F7 plus pendant edge
F7r = [(6,5,4),(6,3,2),(6,1,0),(5,3,1),(4,2,0),(0,7,8)]
# minus a parallel class (direction (1,0) lines: those with constant y)
par = [l for l in lines if len(set(v % 3 for v in l)) == 1]
agpc = [l for l in lines if l not in par]
tests = [('F7', 7, F7, 3, 3), ('AG23 minus 2 points', 9 - 2, rem, 3, 4), ('Fano', 7, fano, 1, 3), ('A_base t=6', 14, ap, 6, 4),
         ('A_base t=5 (tau>t)', 14, ap, 5, 4), ('A_base D=3', 14, ap, 6, 3), ('A_base t=7', 14, ap, 7, 4), ('grid', 9, grid, 3, 2),
         ('two disjoint edges', 6, [(0,1,2),(3,4,5)], 1, 1), ('nonlinear', 5, [(0,1,2),(0,1,3),(2,3,4)], 1, 3),
         ('F7r+pendant', 9, F7r, 1, 3), ('AG23 minus parallel class', 9, agpc, 1, 4),
         ('Fano + path (m <= n-2 overall)', 13, fano + [(6,7,8),(8,9,10),(10,11,12)], 1, 4)]
print('AP edges of A_base:', len(ap))
for name, nv, es, t, D in tests:
    print(name, '->', run(nv, es, t, D))
