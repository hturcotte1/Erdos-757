import sys, itertools
sys.path.insert(0,'/home/user/Erdos-757')
from e757.core import is_45_set, alpha, ap_edges
fib=[1,1]
for i in range(30): fib.append(fib[-1]+fib[-2])
# f(i) with f(0)=f(1)=1 ; set f(2..n+1)
for n in range(4,16):
    A=fib[2:n+2]
    ok=is_45_set(A) if n<=14 else None
    h=alpha(A); tau=n-h
    print(n,A[:4],ok,'h',h,'tau',tau,'GL tau formula',2*(n-1)//5,'3n/5+1',3*n/5+1, 'edges',len(ap_edges(A)))
# is {1,2,3,5} a (4,5)-set
print(is_45_set([1,2,3,5]), is_45_set([2,3,5,8]))
# F7, F8, F9 HY
import itertools
def tau(V,E):
    for k in range(len(V)+1):
        for T in itertools.combinations(V,k):
            if all(set(T)&set(e) for e in E): return k
F7=[(0,1,2),(0,3,4),(0,5,6),(1,3,5),(2,4,6)]
AG=[tuple(sorted(l)) for l in []]
pts=[(x,y) for x in range(3) for y in range(3)]
lines=set()
for p,q in itertools.combinations(pts,2):
    l=frozenset(r for r in pts if ((r[0]-p[0])*(q[1]-p[1])-(r[1]-p[1])*(q[0]-p[0]))%3==0)
    lines.add(l)
lines=[sorted(l) for l in lines]; print(len(lines))
def sub(del_):
    V=[p for p in pts if p not in del_]; E=[tuple(l) for l in lines if not set(l)&set(del_)]
    return V,E
for d in [[],[pts[0]]]:
    V,E=sub(d); t=tau(V,E); n,m=len(V),len(E); print(n,m,t,'17t',17*t,'5n+3m',5*n+3*m,'4t',4*t,'n+m',n+m)
V=list(range(7)); t=tau(V,F7); print('F7',t,17*t,5*7+15, 4*t, 12)
