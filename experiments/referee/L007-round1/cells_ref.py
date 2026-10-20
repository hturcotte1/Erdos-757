# Referee recomputation of the window cells (Step 1) and slack-0 cells (Step 4.3), integer arithmetic only.
import math
def lo(n,m): return (3*n+2*m)//11 + 1          # least tau with 11 tau > 3n+2m
def hy(n,m): return (5*n+3*m)//17               # largest tau allowed by 17 tau <= 5n+3m
print("connected cells: n>=3, ceil((n-1)/2) <= m <= n-2")
win=[]
for n in range(3,17):
    row=[]
    for m in range(-(-(n-1)//2), n-1):
        L,Hh=lo(n,m),hy(n,m)
        w = L <= min(Hh,m)
        row.append(f"{m}:({L},{Hh}){'W' if w else ''}")
        if w: win.append((n,m,L,min(Hh,m)))
    print(n, " ".join(row))
print("window cells (n,m,lo,min(hy,m)):", win)
# brute check: for each connected cell, list all tau values with s<0 and tau<=min(hy,m)
for (n,m,L,U) in win:
    assert all(11*t > 3*n+2*m and 17*t <= 5*n+3*m and t<=m for t in range(L,U+1))
# slack-0 connected cells, by brute force over tau (no modular shortcut)
s0=[]
for n in range(3,14):
    for m in range(-(-(n-1)//2), n-1):
        if (3*n+2*m)%11==0: s0.append((n,m,(3*n+2*m)//11))
print("slack-0 connected cells n<=13:", s0)
# also check HY and tau<=m for these
for (n,m,t) in s0: print((n,m,t), "tau<=m", t<=m, "HY", 17*t, "<=", 5*n+3*m, 17*t<=5*n+3*m)
# partitions of 13 into component sizes from {3,10,13} (sizes of slack-0 connected cells)
sizes=sorted(set(c[0] for c in s0))
sols=[]
def rec(rem, start, acc):
    if rem==0: sols.append(tuple(acc)); return
    for i in range(start,len(sizes)):
        if sizes[i]<=rem: rec(rem-sizes[i], i, acc+[sizes[i]])
rec(13,0,[])
print("component-size multisets summing to 13:", sols)
# Step 8.3: tau=6, n=14 -> m>=11 by HY
print("n=14,tau=6: min m with 102<=70+3m:", min(m for m in range(0,13) if 17*6<=5*14+3*m))
# Step 3: Lemma A at n=13 with tau(H-v)>=5, m=11-d
for d in range(0,6): print("d",d,"11*5<=39+2*(11-d)?", 55<=39+2*(11-d))
