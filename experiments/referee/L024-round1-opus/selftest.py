import random, sys
from itertools import combinations, permutations
from rlib import *

def f7_brute(n,E):
    Es=set(tuple(sorted(e)) for e in E)
    F7=[(0,1,2),(0,3,4),(0,5,6),(1,3,5),(2,4,6)]
    for S in combinations(range(n),7):
        for p in permutations(S):
            if all(tuple(sorted(p[x] for x in e)) in Es for e in F7):
                return True
    return False

random.seed(12345)
bad=0; cnt=0; f7cnt=0; f7pos=0
for it in range(3000):
    n=random.randint(4,10)
    m=random.randint(1,min(9,n))
    E=set()
    tries=0
    while len(E)<m and tries<200:
        tries+=1
        E.add(tuple(sorted(random.sample(range(n),3))))
    E=sorted(E)
    if p3_ok(n,E)!=p3_brute(n,E): bad+=1; print('P3 mismatch',n,E)
    t1,mts=min_transversals(n,E)
    if tau_bb(n,E)!=t1: bad+=1; print('tau mismatch',n,E)
    # brute minimum transversals check
    emasks=[sum(1<<x for x in e) for e in E]
    allT=[sum(1<<x for x in S) for S in combinations(range(n),t1) if all(sum(1<<x for x in S)&em for em in emasks)]
    if sorted(allT)!=sorted(mts): bad+=1; print('mt mismatch')
    if it<400 and n<=8:
        f7cnt+=1
        b=f7_brute(n,E)
        f7pos+=b
        if has_F7(n,E)!=b: bad+=1; print('F7 mismatch',n,E)
    cnt+=1
# F7 itself and with relabelings
F7=[(0,1,2),(0,3,4),(0,5,6),(1,3,5),(2,4,6)]
for it in range(200):
    p=list(range(9)); random.shuffle(p)
    E=[tuple(sorted(p[x] for x in e)) for e in F7]
    if not has_F7(9,E): bad+=1; print('F7 missed')
print('selftest graphs',cnt,'F7 brute tested',f7cnt,'F7 positives',f7pos,'mismatches',bad)
