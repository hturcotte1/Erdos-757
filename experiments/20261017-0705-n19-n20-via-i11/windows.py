"""Window cells (connected, class O) for n<=NMAX and decompositions of the deleted-vertex graph G into connected slack-0 / slack-1 cells."""
import json,sys
def cells(s,nmax):
    out=[]
    for n in range(3,nmax+1):
        for m in range(1,n-1):
            if n>2*m+1: continue
            v=3*n+2*m-s
            if v%11: continue
            t=v//11
            if 1<=t<=m and 17*t<=5*n+3*m: out.append((n,m,t))
    return out
def window(nmax):
    out=[]
    for n in range(3,nmax+1):
        for m in range(1,n-1):
            if n>2*m+1: continue
            lo=(3*n+2*m)//11+1; hi=min((5*n+3*m)//17,m)
            if lo<=hi: out.append((n,m,lo,hi,3*n+2*m-11*lo))
    return out
def parts(c,N,M):
    sol=[]
    def rec(rn,rm,st,ch):
        if rn==0 and rm==0: sol.append(list(ch)); return
        for i in range(st,len(c)):
            n,m,t=c[i]
            if n<=rn and m<=rm: rec(rn-n,rm-m,i,ch+[c[i]])
    rec(N,M,0,[]); return sol
res={}
w=window(18); res['window_cells_n<=18']=w
print('window cells (n,m,least violating tau,HY max tau,slack at that tau):'); [print(' ',x) for x in w if x[0]>=14]
c0=cells(0,17); print('slack-0 connected cells n<=17:',c0)
res['slack0_cells_n<=17']=c0
res['n17']=dict(H=(17,12,7),slack=3*17+24-77,G=(16,9,6),partitions=parts(c0,16,9))
res['n18']=dict(H=(18,16,8),slack=3*18+32-88,G=(17,13,7),partitions=parts(c0,17,13))
print(res['n17']); print(res['n18'])
json.dump(res,open('results_windows.json','w'),indent=1)
