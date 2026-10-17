"""Connected cells (n,m,tau) with m<=n-2, n<=2m+1, 1<=tau<=m, HY 17tau<=5n+3m and slack 3n+2m-11tau = s, n<=15; and the partitions of n=15 into
one slack-1 component plus slack-0 components (sizes taken from the cells), requiring total edges 11."""
import itertools, json
def cells(s,nmax=15):
    out=[]
    for n in range(3,nmax+1):
        for m in range(1,n-1):
            if n>2*m+1: continue
            v=3*n+2*m-s
            if v%11: continue
            t=v//11
            if 1<=t<=m and 17*t<=5*n+3*m: out.append((n,m,t))
    return out
c0,c1=cells(0),cells(1)
print('slack0',c0); print('slack1',c1)
sol=[]
def rec(rem_n,rem_m,start,chosen):
    if rem_n==0 and rem_m==0: sol.append(list(chosen)); return
    for i in range(start,len(c0)):
        n,m,t=c0[i]
        if n<=rem_n and m<=rem_m: rec(rem_n-n,rem_m-m,i,chosen+[c0[i]])
for c in c1:
    rec(15-c[0],11-c[1],0,[c])  # slack-1 comp + multiset of slack-0 comps
    # note: recursion enumerates multisets of slack-0 comps
print('partitions of (15,11):',sol)
json.dump(dict(slack0=c0,slack1=c1,partitions=sol),open('results_slack_cells.json','w'),indent=1)
