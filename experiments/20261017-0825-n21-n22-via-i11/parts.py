"""Generic: connected cells with slack s (m<=n-2, n<=2m+1, HY, tau<=m) and partitions of (N,M) into cells with slacks summing to S."""
import json,sys
def cells(s,nmax):
    out=[]
    for n in range(3,nmax+1):
        for m in range(1,n-1):
            if n>2*m+1: continue
            v=3*n+2*m-s
            if v%11: continue
            t=v//11
            if 1<=t<=m and 17*t<=5*n+3*m: out.append((n,m,t,s))
    if s==3: out.append((1,0,0,3))   # isolated vertex: slack 3
    return out
def parts(N,M,S,nmax=None):
    nmax=nmax or N
    C=[c for s in range(S+1) for c in cells(s,nmax)]
    sol=[]
    def rec(rn,rm,rs,st,ch):
        if rn==0 and rm==0 and rs==0: sol.append(list(ch)); return
        for i in range(st,len(C)):
            n,m,t,s=C[i]
            if n<=rn and m<=rm and s<=rs: rec(rn-n,rm-m,rs-s,i,ch+[C[i]])
    rec(N,M,S,0,[]); return sol
if __name__=="__main__":
    N,M,S=map(int,sys.argv[1:4])
    print('slack-0 cells',[c[:3] for c in cells(0,N)])
    for p in parts(N,M,S): print([c[:4] for c in p])
