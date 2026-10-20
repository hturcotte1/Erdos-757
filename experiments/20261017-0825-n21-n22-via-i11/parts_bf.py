"""Independent brute force: all multisets of component types (n_i,m_i,tau_i) (connected cells incl. the isolated vertex (1,0,0)) with slack in [0,k],
HY-feasible, summing to (N,M,Tau).  Compared with parts.py (which sums slacks instead of tau)."""
import itertools,sys,json
from parts import parts
def universe(nmax,k):
    U=[(1,0,0)]
    for n in range(3,nmax+1):
        for m in range(1,n-1):
            if n>2*m+1: continue
            for t in range(1,m+1):
                if 17*t>5*n+3*m: continue
                s=3*n+2*m-11*t
                if 0<=s<=k: U.append((n,m,t))
    return [u for u in U if (3*u[0]+2*u[1]-11*u[2])<=k]
def bf(N,M,T,k):
    U=universe(N,k); sol=[]
    def rec(rn,rm,rt,st,ch):
        if rn==0 and rm==0 and rt==0: sol.append(tuple(sorted(ch))); return
        for i in range(st,len(U)):
            n,m,t=U[i]
            if n<=rn and m<=rm and t<=rt: rec(rn-n,rm-m,rt-t,i,ch+[U[i]])
    rec(N,M,T,0,[]); return sorted(sol)
def check(N,M,T,k):
    a=bf(N,M,T,k); b=sorted(tuple(sorted(c[:3] for c in p)) for p in parts(N,M,k))
    ok = a==b
    print((N,M,T,k),'brute force',len(a),'parts.py',len(b),'EQUAL' if ok else 'DIFFERENT'); 
    if not ok: print(' only bf:',[x for x in a if x not in b]); print(' only parts:',[x for x in b if x not in a])
    return dict(N=N,M=M,T=T,k=k,bf=len(a),parts=len(b),equal=ok,lists=[list(x) for x in a])
if __name__=="__main__":
    res=[check(*map(int,a.split(','))) for a in sys.argv[1:]]
    json.dump(res,open('results_parts_check.json','w'),indent=1)
