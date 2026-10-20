"""Decompose G' = (16,10,6) (slack 2) into connected components: slack-s cells (s=0,1,2), sum of slacks 2, total (16,10)."""
import json,itertools
def cells(s,nmax):
    out=[]
    for n in range(3,nmax+1):
        for m in range(1,n-1):
            if n>2*m+1: continue
            v=3*n+2*m-s
            if v%11: continue
            t=v//11
            if 1<=t<=m and 17*t<=5*n+3*m: out.append((n,m,t,s))
    return out
C=[c for s in (0,1,2) for c in cells(s,16)]
print({s:[c[:3] for c in cells(s,16)] for s in (0,1,2)})
def parts(N,M,S):
    sol=[]
    def rec(rn,rm,rs,st,ch):
        if rn==0 and rm==0 and rs==0: sol.append(list(ch)); return
        for i in range(st,len(C)):
            n,m,t,s=C[i]
            if n<=rn and m<=rm and s<=rs: rec(rn-n,rm-m,rs-s,i,ch+[C[i]])
    rec(N,M,S,0,[]); return sol
P=parts(16,10,2)
for p in P: print(p)
json.dump(P,open('results_parts_16_10_2.json','w'))
