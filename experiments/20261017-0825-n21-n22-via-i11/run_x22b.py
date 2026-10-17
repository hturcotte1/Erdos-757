"""(22,16,9): G=H-v=(21,13,8) slack 1: [3AP,(12,10,5)] [2AP,(15,11,6)] [AP,C10,(8,5,3)] [AP,(18,12,7)=none] [C10,(11,6,4)=none] [C13,(8,5,3)=none (F7)] [connected (21,13,8): maxdeg<=2 DFS or deg-3 rebuild from (20,10,7) slack 3]."""
import build
from build import *
import dedupe_fast as DF
def _dd(graphs,nv,tag):
    reps,st=DF.dedupe_fast(graphs,nv,tag); build.STATS[tag]=st; return reps
build.dedupe=_dd
from parts import parts
import itertools
t0=time.time()
cache={}
def cl(key):
    if key==(1,0,0): return [[]]   # isolated vertex
    if key not in cache: cache[key]=cell_classes(*key)
    return cache[key]
P=parts(20,10,3); print(len(P),'partitions of (20,10) slack 3'); STATS['partitions_20_10_3']=[[c[:4] for c in p] for p in P]
Gp=gprime_list(P,cl); print('G prime (20,10,7) candidates',len(Gp),flush=True); STATS['Gprime_20_10_7']=len(Gp)
X21=extend(Gp,20,8,'X21_deg3'); json.dump(X21,open('out/X21_classes.json','w'))
AP=[(0,1,2)]
c12=cl((12,10,5)); c10=cl((10,7,4)); c8=cl((8,5,3))
B15=[[tuple(e) for e in r[0]] for r in json.load(open('../20261017-0300-n16-via-i11/classes_B_reps.json'))]
c15=dedupe(B15,15,'cell_15_11_6_reused')
Gs=[[tuple(e) for e in g] for g in X21]; STATS['n_X21']=len(Gs)
for c in c12: es,n=union([(3,AP),(3,AP),(3,AP),(12,c)]); assert n==21; Gs.append(es)
for c in c15: es,n=union([(3,AP),(3,AP),(15,c)]); Gs.append(es)
for a in c10:
    for b in c8: es,n=union([(3,AP),(10,a),(8,b)]); Gs.append(es)
print('G (21,13,8) candidates',len(Gs),flush=True); STATS['G_21_13_8_candidates']=len(Gs)
inp='in_x22.txt'
with open(inp,'w') as f:
    for es in Gs: f.write("%d "%len(es)+" ".join("%d %d %d"%tuple(e) for e in es)+"\n")
subprocess.run('nice -n 10 ./ext_vertex2 21 9 3 < %s > out/hits_22_16_9.txt'%inp,shell=True,check=True)
last=open('out/hits_22_16_9.txt').read().strip().splitlines()[-1]; print(last); STATS['ext_main']=last
subprocess.run('nice -n 10 ./ext_vertex2 21 8 3 < %s | head -3000 > out/hits_22_16_9_control.txt'%inp,shell=True)
subprocess.run('nice -n 10 python3 post.py out/hits_22_16_9.txt 22 post_22_16_9.json > post_22_16_9.log 2>&1',shell=True); print(open('post_22_16_9.log').read())
subprocess.run('nice -n 10 python3 post.py out/hits_22_16_9_control.txt 22 post_22_16_9_control.json > post_22_16_9_control.log 2>&1',shell=True); print(open('post_22_16_9_control.log').read())
json.dump(STATS,open('stats_22_16_9.json','w'),indent=1); print('secs',time.time()-t0)
