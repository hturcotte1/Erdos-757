"""Positive control: build G''+gadget for a PT-config (hit at slack 12) and verify by brute force that tau = tau''+4 and the slack drops by 9;
also test membership in C (linear, e(S)<=|S|-2 by Hall, F7-free) with own independent code (itertools)."""
import sys
sys.path.insert(0,'/home/user/Erdos-757/experiments/prover/e1hub-synthesis/checks')
from hyp import tau, is_linear
from itertools import combinations
def hall_ok(n,edges):
    # e(S)<=|S|-2 for all S, |S|>=2 : equivalently for all nonempty edge sets F, |V(F)|>=|F|+2.  check via subsets of edges (m small)
    m=len(edges)
    for r in range(1,m+1):
        for F in combinations(range(m),r):
            V=set()
            for i in F: V|=set(edges[i])
            if len(V)<r+2: return False
    return True
def has_F7(n,edges):
    es=set(map(frozenset,edges))
    for o in range(n):
        inc=[e for e in edges if o in e]
        for t in combinations(inc,3):
            ps=[tuple(sorted(set(e)-{o})) for e in t]  # pairs {p_i,q_i}
            for ch in range(8):
                p=[ps[i][(ch>>i)&1] for i in range(3)]; q=[ps[i][1-((ch>>i)&1)] for i in range(3)]
                if frozenset(p) in es and frozenset(q) in es and len(set(p))==3 and len(set(q))==3: return True
    return False
def build(n,edges,A,B,C):
    v,x,y,z,a,b,c=range(n,n+7)
    new=[(x,y,z),(v,x,a),(v,y,b),(v,z,c),(a,)+tuple(A),(b,)+tuple(B),(c,)+tuple(C)]
    return n+7,[tuple(sorted(e)) for e in edges]+[tuple(sorted(e)) for e in new]
line=sys.argv[1].split()
n=int(line[line.index('n')+1]); 
A=(int(line[line.index('A')+1]),int(line[line.index('A')+2])); B=(int(line[line.index('B')+1]),int(line[line.index('B')+2])); C=(int(line[line.index('C')+1]),int(line[line.index('C')+2]))
edges=[tuple(map(int,x.split(','))) for x in line[line.index('edges')+1:]]
t1=tau(n,edges); m1=len(edges)
N,E=build(n,edges,A,B,C); t2=tau(N,E)
print('G\'\': n',n,'m',m1,'tau',t1,'slack',3*n+2*m1-11*t1)
print('G\'\'+gadget: n',N,'m',len(E),'tau',t2,'slack',3*N+2*len(E)-11*t2,'tau rise',t2-t1)
print('linear',is_linear(E),'F7',has_F7(N,E),'Hall(e(S)<=|S|-2)', hall_ok(N,E))
