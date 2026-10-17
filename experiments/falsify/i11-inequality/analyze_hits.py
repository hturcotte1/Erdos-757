import re,sys,itertools
sys.path.insert(0,'/home/user/Erdos-757')
from e757.cpsat_model import find_f7
from e757.saturated import alpha_of_edges
hits=[]
for l in open('ext_vertex_hits.txt'):
    if l.startswith('HIT:'):
        hits.append([tuple(map(int,t.split(','))) for t in re.findall(r'\(([\d,]+)\)',l)])
print(len(hits))
def e_sub_ok(es,n):
    # check e(S)<=|S|-2 for all S (necessary for class O): equivalently no S with e(S) >= |S|-1 ; brute force 2^14
    masks=[sum(1<<v for v in e) for e in es]
    for S in range(1,1<<n):
        c=sum(1 for mk in masks if mk&S==mk)
        if c>bin(S).count('1')-2 and c>0: return False
    return True
nf7=0; nsub=0; both=[]
for es in hits:
    if find_f7(es): continue
    nf7+=1
    if e_sub_ok(es,14): nsub+=1; both.append(es)
print('F7-free',nf7,'F7-free and e(S)<=|S|-2 for all S',nsub)
import json; json.dump(both,open('hits_f7free_sub.json','w'))
