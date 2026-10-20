from build import *
import itertools
t0=time.time()
AP=[(0,1,2)]
c6_3=cell_classes(6,3,2); c8_5=cell_classes(8,5,3); c10_7=cell_classes(10,7,4); c10_8=cell_classes(10,8,4); c13_9=cell_classes(13,9,5); c16_10=cell_classes(16,10,6)
Gp=[]
for c in c10_8: es,n=union([(3,AP),(3,AP),(10,c)]); assert n==16; Gp.append(es)
for c in c13_9: es,n=union([(3,AP),(13,c)]); Gp.append(es)
for a in c10_7:
    for b in c6_3: es,n=union([(10,a),(6,b)]); Gp.append(es)
for a,b in itertools.combinations_with_replacement(range(len(c8_5)),2):
    es,n=union([(8,c8_5[a]),(8,c8_5[b])]); Gp.append(es)
Gp+=c16_10
print('G prime (16,10,6) candidates',len(Gp),flush=True)
STATS['Gprime_candidates']=len(Gp)
G17=extend(Gp,16,7,'G17')
STATS['G17_final_classes']=len(G17)
json.dump(G17,open('G17_classes.json','w')); json.dump(STATS,open('stats_G17.json','w'),indent=1)
print('secs',time.time()-t0)
