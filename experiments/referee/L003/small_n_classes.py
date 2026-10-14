"""Referee L003: affine classes of extremal n-point (4,5)-sets for n <= 5 (illustration in a box; n<=3 by proof).
For every set {0 < a_1 < ... < a_{n-1} <= B} of integers: (4,5)? h? -> min h and #normal forms attaining it."""
import itertools, math
def is45(A):
    return all(len({abs(a-b) for a,b in itertools.combinations(q,2)}) >= 5 for q in itertools.combinations(A,4))
def sidon(B):
    d=set()
    for a,b in itertools.combinations(sorted(B),2):
        if b-a in d: return False
        d.add(b-a)
    return True
def h_of(A):
    for s in range(len(A),0,-1):
        if any(sidon(B) for B in itertools.combinations(A,s)): return s
def nf(A):
    lo=min(A); v=sorted(x-lo for x in A); g=0
    for x in v: g=math.gcd(g,x)
    v=[x//g for x in v] if g else v
    return tuple(min(v, sorted(v[-1]-x for x in v)))
for n, B in [(1,0),(2,30),(3,30),(4,30),(5,30)]:
    best=None; cls={}
    for rest in itertools.combinations(range(1,B+1), n-1):
        A=(0,)+rest
        if not is45(A): continue
        h=h_of(A)
        cls.setdefault(h,set()).add(nf(A))
    f=min(cls)
    print("n=%d box [0,%d]: min h = %d; normal forms with h=min: %d %s" % (n,B,f,len(cls[f]), sorted(cls[f])[:3]))
