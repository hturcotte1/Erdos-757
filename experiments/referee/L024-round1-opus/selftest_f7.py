import random
from itertools import combinations, permutations
from rlib import has_F7
def f7_brute(n,E):
    Es=set(tuple(sorted(e)) for e in E)
    F7=[(0,1,2),(0,3,4),(0,5,6),(1,3,5),(2,4,6)]
    for S in combinations(range(n),7):
        for p in permutations(S):
            if all(tuple(sorted(p[x] for x in e)) in Es for e in F7):
                return True
    return False
random.seed(7)
F7=[(0,1,2),(0,3,4),(0,5,6),(1,3,5),(2,4,6)]
bad=0;pos=0;tot=0
for it in range(60):
    n=8
    p=list(range(n)); random.shuffle(p)
    E=set(tuple(sorted(p[x] for x in e)) for e in F7)
    if it%2==1:
        E.discard(random.choice(sorted(E)))
    for _ in range(random.randint(0,3)):
        E.add(tuple(sorted(random.sample(range(n),3))))
    E=sorted(E)
    b=f7_brute(n,E); pos+=b; tot+=1
    if b!=has_F7(n,E): bad+=1; print('mismatch',E)
print('planted tests',tot,'positives',pos,'mismatches',bad)
