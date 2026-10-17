from build import *
AP=[(0,1,2)]
c10=cell_classes(10,7,4)
Gs=[]
for c in c10: es,n=union([(10,c),(3,AP),(3,AP),(3,AP)]); assert n==19; Gs.append(es)
# other partitions: [AP,AP,C13(8,5)] (all F7), [AP,(16,9,6)] (empty), [(19,10,7)] direct DFS (see D_19_10_7.txt)
inp='in_20_13_8.txt'; out='hits_20_13_8.txt'
with open(inp,'w') as f:
    for es in Gs: f.write("%d "%len(es)+" ".join("%d %d %d"%tuple(e) for e in es)+"\n")
for T,tag in ((8,'main'),(7,'control')):
    subprocess.run('nice -n 10 ./ext_vertex2 19 %d 3 < %s > %s'%(T,inp,out+'.'+tag),shell=True,check=True)
    print(T,open(out+'.'+tag).read().strip().splitlines()[-1])
