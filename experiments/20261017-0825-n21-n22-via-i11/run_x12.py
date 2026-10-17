"""(21,12,8): maxdeg 3 case with a degree-3 vertex: G=(20,9,7) slack 1."""
from build import *
from parts import parts
cache={}
def cl(key):
    if key not in cache: cache[key]=cell_classes(*key)
    return cache[key]
P=parts(20,9,1); print([[c[:4] for c in p] for p in P])
Gp=gprime_list(P,cl); print('G candidates',len(Gp)); STATS['G_20_9_7_candidates']=len(Gp); STATS['partitions']=[[c[:4] for c in p] for p in P]
inp='in_x12.txt'
with open(inp,'w') as f:
    for es in Gp: f.write("%d "%len(es)+" ".join("%d %d %d"%tuple(e) for e in es)+"\n")
subprocess.run('nice -n 10 ./ext_vertex2 20 8 3 < %s > out/hits_21_12_8.txt'%inp,shell=True,check=True)
last=open('out/hits_21_12_8.txt').read().strip().splitlines()[-1]; print(last); STATS['ext_main']=last
subprocess.run('nice -n 10 ./ext_vertex2 20 7 3 < %s | head -3000 > out/hits_21_12_8_control.txt'%inp,shell=True)
subprocess.run('nice -n 10 python3 post.py out/hits_21_12_8.txt 21 post_21_12_8.json > post_21_12_8.log 2>&1',shell=True)
print(open('post_21_12_8.log').read())
subprocess.run('nice -n 10 python3 post.py out/hits_21_12_8_control.txt 21 post_21_12_8_control.json > post_21_12_8_control.log 2>&1',shell=True)
print(open('post_21_12_8_control.log').read())
json.dump(STATS,open('stats_21_12_8.json','w'),indent=1)
