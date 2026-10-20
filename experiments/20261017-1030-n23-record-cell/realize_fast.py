import numpy as np,sys,itertools
from realize_sat import assignments, exact
from fractions import Fraction as F
def batch_solve(edges,n,A):
    B=len(A); out=[]; 
    Xs=np.full((B,n),np.nan)
    # group by unmatched pair (affects which vertices are unknown)
    groups={}
    for bi,(asg,un) in enumerate(A): groups.setdefault(un,[]).append(bi)
    for un,bis in groups.items():
        u,v=un; idx=[w for w in range(n) if w not in (u,v)]; pos={w:i for i,w in enumerate(idx)}; m=len(idx)
        Mat=np.zeros((len(bis),m,m)); rhs=np.zeros((len(bis),m))
        for t,bi in enumerate(bis):
            asg=A[bi][0]
            for e,mid in zip(edges,asg):
                r=pos[mid]; Mat[t,r,r]+=2
                for w in e:
                    if w==mid: continue
                    if w==u: pass
                    elif w==v: rhs[t,r]+=1
                    else: Mat[t,r,pos[w]]-=1
        det=np.linalg.det(Mat); ok=np.abs(det)>1e-9
        sol=np.full((len(bis),m),np.nan)
        if ok.any(): sol[ok]=np.linalg.solve(Mat[ok],rhs[ok][...,None])[...,0]
        for t,bi in enumerate(bis):
            if not ok[t]: continue
            X=np.zeros(n); X[v]=1.0
            for w,i in pos.items(): X[w]=sol[t,i]
            Xs[bi]=X
    return Xs
def realize_fast(edges,n,tol=1e-8,chunk=800):
    edges=[tuple(e) for e in edges]; m=len(edges)
    A=assignments(edges,n); stats=dict(assignments=len(A),solvable=0,distinct=0,noextra=0,exact_ok=0)
    Xs=batch_solve(edges,n,A); good=[]
    iu=np.triu_indices(n,1)
    for s in range(0,len(A),chunk):
        X=Xs[s:s+chunk]; ok=~np.isnan(X).any(axis=1); stats['solvable']+=int(ok.sum())
        Xs_=np.sort(X,axis=1); gaps=np.diff(Xs_,axis=1).min(axis=1)
        dist=ok&(gaps>tol); stats['distinct']+=int(dist.sum())
        idx=np.nonzero(dist)[0]
        if len(idx)==0: continue
        Y=X[idx]                                  # (b,n)
        S=Y[:,:,None]+Y[:,None,:]                 # (b,n,n)
        cnt=np.zeros(len(idx),dtype=int)
        for j in range(n):
            T=np.abs(S-2*Y[:,j][:,None,None])<tol   # pairs (a,c) with x_a+x_c=2x_j
            T[:,j,:]=False; T[:,:,j]=False
            cnt+=T.sum(axis=(1,2))//2
        sel=idx[cnt==m]; stats['noextra']+=len(sel)
        good+= [s+int(i) for i in sel]
    found=[]
    for bi in good:
        asg,un=A[bi]; Xe=exact(edges,n,asg,un)
        if Xe is None or len(set(Xe))<n: continue
        from math import lcm
        L=1
        for x in Xe: L=lcm(L,x.denominator)
        found.append(sorted(int(x*L) for x in Xe)); stats['exact_ok']+=1
    return found,stats
if __name__=="__main__":
    import re,time
    sys.path.insert(0,'/home/user/Erdos-757')
    from e757.core import ap_edges
    Ab=[0,136,200,243,246,249,272,286,298,323,400,528,596,1056]; idx={x:i for i,x in enumerate(Ab)}
    E=[(idx[a],idx[b],idx[c]) for a,b,c in ap_edges(Ab)]
    t=time.time(); f,s=realize_fast(E,14); print('A_base',s,time.time()-t)
    l=open('/tmp/h6.txt').readlines()[0]
    es=[tuple(map(int,t.split(','))) for t in re.findall(r'\(([\d,]+)\)',l)]
    t=time.time(); f,s=realize_fast(es,23); print('cand0',s,time.time()-t)
