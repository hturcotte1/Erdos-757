# Independent recomputation of Step 1 (window cells) and Step 4.3 (slack-0 cells), exact integers.
from math import ceil
def lo(n,m): return (3*n+2*m)//11+1          # least tau with 3n+2m-11tau<0
def hy(n,m): return (5*n+3*m)//17            # largest tau allowed by 17tau<=5n+3m
win=[]; s0=[]
for n in range(3,17):
    for m in range(0,n-1):                   # m<=n-2 (P3)
        if n>2*m+1: continue                 # connected: n<=2m+1
        if lo(n,m)<=min(hy(n,m),m): win.append((n,m,lo(n,m),hy(n,m)))
        if (3*n+2*m)%11==0:
            t=(3*n+2*m)//11
            s0.append((n,m,t, t<=m, 17*t<=5*n+3*m))
print("window cells (n,m,lo,hy):",win)
print("slack-0 connected cells n<=13 (n,m,tau,tau<=m,HY ok):",[c for c in s0 if c[0]<=13])
# Step 4.4: 13 = sum of component sizes from {3,10,13}
sols=[(a,b,c) for a in range(5) for b in range(2) for c in range(2) if 3*a+10*b+13*c==13]
print("13=3a+10b+13c:",sols)
# Step 3: per-vertex bound
for d in range(0,12):
    ok = 11*5 <= 3*13+2*(11-d)
    print(d, ok, end="; ")
print()
# Step 8.3: HY at n=14,tau=6
print("m>=", [m for m in range(0,13) if 17*6<=5*14+3*m][:1])
