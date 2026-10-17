from build import *
t0=time.time()
G17=json.load(open('G17_classes.json')); C14=json.load(open('C14_classes.json'))
Gs=[[tuple(e) for e in g] for g in G17]
nconn=len(Gs)
for c in C14:
    es,n=union([(14,[tuple(e) for e in c]),(3,[(0,1,2)])]); assert n==17; Gs.append(es)
print('G (17,13,7) candidates: from G17',nconn,'+ C14+AP',len(C14),flush=True)
STATS['H18_inputs']=dict(G17_classes=nconn,C14_plus_AP=len(C14))
# extension, but keep ALL hits (not only F7-free) for the F7/e(S)/orderability accounting
inp='in_H18.txt'
with open(inp,'w') as f:
    for es in Gs: f.write("%d "%len(es)+" ".join("%d %d %d"%tuple(e) for e in es)+"\n")
subprocess.run('nice -n 10 ./ext_vertex2 17 8 3 < in_H18.txt > hits_H18.txt',shell=True,check=True)
last=open('hits_H18.txt').read().strip().splitlines()[-1]; print(last)
STATS['H18_ext']=last
subprocess.run('nice -n 10 python3 post.py hits_H18.txt 18 post_H18.json > post_H18.log 2>&1',shell=True)
print(open('post_H18.log').read())
STATS['H18_post']=json.load(open('post_H18.json'))['summary']
json.dump(STATS,open('stats_H18.json','w'),indent=1)
