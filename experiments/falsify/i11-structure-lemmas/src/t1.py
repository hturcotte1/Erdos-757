import sys; sys.path.insert(0,'src')
from hg import *
import random, itertools
random.seed(2)
bad=0;tot=0;pos=0;f7c=0
for it in range(40000):
    n=random.randint(6,11); m=random.randint(n-3,n+1)
    # greedy random linear
    E=[]; used=set()
    tries=0
    while len(E)<m and tries<200:
        tries+=1
        t=tuple(sorted(random.sample(range(n),3)))
        ps=list(itertools.combinations(t,2))
        if any(p in used for p in ps): continue
        used.update(ps); E.append(t)
    tot+=1
    f7=has_F7(n,E); 
    a=(not f7) and eS_ok(n,E)
    b=classC_fast(n,E)
    pos+=a; f7c+=f7
    if a!=b: bad+=1
    assert f7==has_F7_fast(n,E)
print(tot,pos,f7c,bad)
