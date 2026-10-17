"""(21,17,9): G=H-v=(20,14,8) slack 0: [AP,AP,C14] [AP,C17] [C10,C10] [connected (20,14,8) -> rebuilt via deg-3 vertex from (19,11,7) slack 2]."""
from build import *
from parts import parts
import itertools
t0=time.time()
cache={}
def cl(key):
    if key not in cache: cache[key]=cell_classes(*key)
    return cache[key]
P=parts(19,11,2); print([[c[:4] for c in p] for p in P]); STATS['partitions_19_11_2']=[[c[:4] for c in p] for p in P]
Gp=gprime_list(P,cl); print('G prime (19,11,7) candidates',len(Gp),flush=True); STATS['Gprime_19_11_7']=len(Gp)
X20=extend(Gp,19,8,'X20_deg3'); json.dump(X20,open('out/X20_classes.json','w'))
C14=json.load(open('../20261017-0615-n17-n18-via-i11/C14_classes.json')); C17=json.load(open('../20261017-0615-n17-n18-via-i11/G17_classes.json'))
AP=[(0,1,2)]; c10=cl((10,7,4))
Gs=[[tuple(e) for e in g] for g in X20]; STATS['n_X20']=len(Gs)
for c in C14: es,n=union([(14,[tuple(e) for e in c]),(3,AP),(3,AP)]); assert n==20; Gs.append(es)
for c in C17: es,n=union([(17,[tuple(e) for e in c]),(3,AP)]); Gs.append(es)
for a,b in itertools.combinations_with_replacement(range(len(c10)),2): es,n=union([(10,c10[a]),(10,c10[b])]); Gs.append(es)
print('G (20,14,8) candidates',len(Gs),flush=True); STATS['G_20_14_8_candidates']=len(Gs)
inp='in_x17.txt'
with open(inp,'w') as f:
    for es in Gs: f.write("%d "%len(es)+" ".join("%d %d %d"%tuple(e) for e in es)+"\n")
subprocess.run('nice -n 10 ./ext_vertex2 20 9 3 < %s > out/hits_21_17_9.txt'%inp,shell=True,check=True)
last=open('out/hits_21_17_9.txt').read().strip().splitlines()[-1]; print(last); STATS['ext_main']=last
subprocess.run('nice -n 10 ./ext_vertex2 20 8 3 < %s | head -3000 > out/hits_21_17_9_control.txt'%inp,shell=True)
subprocess.run('nice -n 10 python3 post.py out/hits_21_17_9.txt 21 post_21_17_9.json > post_21_17_9.log 2>&1',shell=True); print(open('post_21_17_9.log').read())
subprocess.run('nice -n 10 python3 post.py out/hits_21_17_9_control.txt 21 post_21_17_9_control.json > post_21_17_9_control.log 2>&1',shell=True); print(open('post_21_17_9_control.log').read())
json.dump(STATS,open('stats_21_17_9.json','w'),indent=1); print('secs',time.time()-t0)
