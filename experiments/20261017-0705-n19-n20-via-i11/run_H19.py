from build import *
import itertools
t0=time.time()
AP=[(0,1,2)]
X18=json.load(open('X18_deg3_classes.json'))
c12=cell_classes(12,10,5); c10=cell_classes(10,7,4); c8=cell_classes(8,5,3)
# (15,11,6): reuse the 49 classes of experiments/20261017-0300-n16-via-i11 (conn_dfs3 maxdeg 3, verified there), re-filter F7/e(S)
B15=[[tuple(e) for e in r[0]] for r in json.load(open('../20261017-0300-n16-via-i11/classes_B_reps.json'))]
c15=dedupe(B15,15,'cell_15_11_6_reused')
Gs=[[tuple(e) for e in g] for g in X18]; STATS['H19_input_X18']=len(Gs)
for c in c12: es,n=union([(3,AP),(3,AP),(12,c)]); assert n==18; Gs.append(es)
for c in c15: es,n=union([(3,AP),(15,c)]); Gs.append(es)
for a in c10:
    for b in c8: es,n=union([(10,a),(8,b)]); Gs.append(es)
print('G (18,12,7) candidates',len(Gs),flush=True); STATS['H19_G_candidates']=len(Gs)
inp='in_H19.txt'
with open(inp,'w') as f:
    for es in Gs: f.write("%d "%len(es)+" ".join("%d %d %d"%tuple(e) for e in es)+"\n")
for T,tag in ((8,'main'),(7,'control')):
    subprocess.run('nice -n 10 ./ext_vertex2 18 %d 3 < %s > hits_H19.%s.txt'%(T,inp,tag),shell=True,check=True)
    last=open('hits_H19.%s.txt'%tag).read().strip().splitlines()[-1]; print(T,last); STATS['H19_ext_'+tag]=last
subprocess.run('nice -n 10 python3 post.py hits_H19.main.txt 19 post_H19.json > post_H19.log 2>&1',shell=True)
print(open('post_H19.log').read()); STATS['H19_post']=json.load(open('post_H19.json'))['summary']
json.dump(STATS,open('stats_H19.json','w'),indent=1)
