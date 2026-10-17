"""Exact realization of a saturated candidate H (n vertices, n-2 edges): enumerate injective midpoint assignments (edge -> one of its vertices, all distinct; the 2 unmatched
vertices are the extremes, x=0 and x=1), solve the rigid linear system x_j=(x_i+x_k)/2 (numpy prefilter, then exact Fractions), require: distinct values,
AP set of the solution == edge set of H, and the (4,5) property.  Returns the list of realizations (integer sets)."""
import sys,itertools,numpy as np
from fractions import Fraction as F
def assignments(edges,n,limit=None):
    m=len(edges); order=sorted(range(m),key=lambda e:0)
    inc=[[] for _ in range(n)]
    for ei,e in enumerate(edges):
        for v in e: inc[v].append(ei)
    res=[]; used=[False]*n; asg=[None]*m
    def rec(k):
        if limit and len(res)>=limit: return
        if k==m:
            un=[v for v in range(n) if not used[v]]
            res.append((tuple(asg),tuple(un))); return
        for v in edges[k]:
            if not used[v]:
                used[v]=True; asg[k]=v; rec(k+1); used[v]=False
    rec(0); return res
def solve_float(edges,n,asg,un):
    u,v=un; idx=[w for w in range(n) if w not in (u,v)]; pos={w:i for i,w in enumerate(idx)}
    m=len(idx); A=np.zeros((m,m)); b=np.zeros(m)
    for e,mid in zip(edges,asg):
        i,k=[w for w in e if w!=mid]; r=pos[mid]; A[r,r]+=2
        for w in (i,k):
            if w==u: pass
            elif w==v: b[r]+=1
            else: A[r,pos[w]]-=1
    try: x=np.linalg.solve(A,b)
    except np.linalg.LinAlgError: return None
    X=np.zeros(n); X[v]=1.0
    for w,i in pos.items(): X[w]=x[i]
    return X
def aps_of(X,n,tol=1e-9):
    order=np.argsort(X); xs=X[order]; out=set()
    for a in range(n):
        for c in range(a+2,n):
            t=(xs[a]+xs[c])/2
            j=np.searchsorted(xs,t-tol)
            if j<n and abs(xs[j]-t)<tol and a<j<c: out.add(tuple(sorted((int(order[a]),int(order[j]),int(order[c])))))
    return out
def exact(edges,n,asg,un):
    u,v=un; idx=[w for w in range(n) if w not in (u,v)]; pos={w:i for i,w in enumerate(idx)}; m=len(idx)
    M=[[F(0)]*(m+1) for _ in range(m)]
    for e,mid in zip(edges,asg):
        i,k=[w for w in e if w!=mid]; r=pos[mid]; M[r][r]+=2
        for w in (i,k):
            if w==v: M[r][m]+=1
            elif w!=u: M[r][pos[w]]-=1
    for c in range(m):
        p=next((r for r in range(c,m) if M[r][c]!=0),None)
        if p is None: return None
        M[c],M[p]=M[p],M[c]; inv=1/M[c][c]; M[c]=[x*inv for x in M[c]]
        for r in range(m):
            if r!=c and M[r][c]!=0:
                f=M[r][c]; M[r]=[a-f*b for a,b in zip(M[r],M[c])]
    X=[F(0)]*n; X[v]=F(1)
    for w,i in pos.items(): X[w]=M[i][m]
    return X
def realize(edges,n,limit=None,verbose=False):
    edges=[tuple(e) for e in edges]; E=set(tuple(sorted(e)) for e in edges); found=[]
    A=assignments(edges,n,limit); stats=dict(assignments=len(A),solvable=0,distinct=0,ap_equal=0,exact_ok=0)
    for asg,un in A:
        X=solve_float(edges,n,asg,un)
        if X is None: continue
        stats['solvable']+=1
        if len(set(np.round(X,9)))<n: continue
        stats['distinct']+=1
        if aps_of(X,n)!=E: continue
        stats['ap_equal']+=1
        Xe=exact(edges,n,asg,un)
        if Xe is None or len(set(Xe))<n: continue
        from math import lcm
        L=1
        for x in Xe: L=lcm(L,x.denominator)
        S=sorted(int(x*L) for x in Xe)
        found.append((S,asg,un)); stats['exact_ok']+=1
    return found,stats
if __name__=="__main__":
    import re
    l=open(sys.argv[1]).readlines()[int(sys.argv[2])]
    es=[tuple(map(int,t.split(','))) for t in re.findall(r'\(([\d,]+)\)',l)]
    n=max(max(e) for e in es)+1
    f,s=realize(es,n); print(s,len(f))
