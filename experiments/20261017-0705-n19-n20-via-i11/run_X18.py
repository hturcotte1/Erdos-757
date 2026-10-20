"""Connected (18,12,7) (slack 1), maxdeg<=3: (a) maxdeg<=2 direct DFS; (b) has a degree-3 vertex w: X-w = (17,9,6) slack 3 = one of 7 partitions."""
from build import *
import itertools
from parts import parts
t0=time.time()
AP=[(0,1,2)]
P=parts(17,9,3); print(len(P),'partitions of (17,9) slack 3'); STATS['partitions_17_9_3']=[[c[:4] for c in p] for p in P]
cache={}
def cl(c):
    key=c[:3]
    if key not in cache: cache[key]=cell_classes(*key)
    return cache[key]
Gp=[]
for p in P:
    lists=[cl(c) for c in p]
    # multiset handling: identical cells -> combinations_with_replacement of class indices
    groups={}
    for c in p: groups.setdefault(c[:3],[]).append(c)
    gl=[]
    for key,cs in groups.items():
        k=len(cs); gl.append((key,list(itertools.combinations_with_replacement(range(len(cache[key])),k))))
    for combo in itertools.product(*[g[1] for g in gl]):
        parts_=[]
        for (key,_),idxs in zip(gl,combo):
            for i in idxs: parts_.append((key[0],cache[key][i]))
        es,n=union(parts_); assert n==17; Gp.append(es)
print('G prime candidates',len(Gp),flush=True); STATS['Gprime_17_9_6']=len(Gp)
X3=extend(Gp,17,7,'X18_deg3')
json.dump(X3,open('X18_deg3_classes.json','w'))
json.dump(STATS,open('stats_X18.json','w'),indent=1); print('secs',time.time()-t0)
