# Referee check of Step 7 / C7 and the sanity rows, from the definitions only (no e757, no judge import).
from itertools import combinations
from fractions import Fraction
def is45(A):
    return all(len({abs(a-b) for a,b in combinations(Q,2)})>=5 for Q in combinations(A,4))
def aps(A):
    S=set(A); A=sorted(A)
    return [(x,y,z) for x,z in combinations(A,2) for y in [Fraction(x+z,2)] if y in S and x<y<z]
def is_sidon(S):
    sums=[a+b for i,a in enumerate(S) for b in S[i:]]   # x<=y, includes 2x
    return len(sums)==len(set(sums))
def h_brute(A):
    A=sorted(A); n=len(A); best=0
    for mask in range(1<<n):
        k=bin(mask).count('1')
        if k<=best: continue
        S=[A[i] for i in range(n) if mask>>i&1]
        if is_sidon(S): best=k
    return best
def tau_of(n,E):
    for k in range(n+1):
        for T in combinations(range(n),k):
            t=set(T)
            if all(t & set(e) for e in E): return k
W=[0,323,523,566,569,572,595,609,621,646,723,851,919,1379]
fib=[1,1]
while len(fib)<16: fib.append(fib[-1]+fib[-2])
FIB=fib[2:16]          # F3..F16
AB=[0,136,200,243,246,249,272,286,298,323,400,528,596,1056]
for name,A in [('W',W),('Fib F3..F16',FIB),('A_base',AB)]:
    A=sorted(A); idx={x:i for i,x in enumerate(A)}
    P=aps(A); E=[(idx[x],idx[int(y)],idx[z]) for x,y,z in P]
    h=h_brute(A); t=tau_of(len(A),E)
    print(f'{name}: n={len(A)} distinct={len(set(A))==len(A)} (4,5)={is45(A)} m={len(P)} h_brute={h} n-tau={len(A)-t} tau={t} I11 slack={3*len(A)+2*len(P)-11*t}')
    if name=='W': print('  APs:',[(x,int(y),z) for x,y,z in P])
print('W-323 == (A_base \\ {136}) U {-323}:', sorted(x-323 for x in W)==sorted([x for x in AB if x!=136]+[-323]))
print('Fib:',FIB)
