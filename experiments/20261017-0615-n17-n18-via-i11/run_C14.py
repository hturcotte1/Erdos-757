from build import *
t0=time.time()
AP=[(0,1,2)]
c10_8=cell_classes(10,8,4); c13_9=cell_classes(13,9,5)
Gp=[]
for c in c10_8: es,n=union([(3,AP),(10,c)]); assert n==13; Gp.append(es)
for c in c13_9: Gp.append(c)
print('G prime (13,9,5) candidates',len(Gp))
C14=extend(Gp,13,6,'C14')
STATS['C14_final_classes']=len(C14)
json.dump(C14,open('C14_classes.json','w')); json.dump(STATS,open('stats_C14.json','w'),indent=1)
# consistency: realizable 2,910 classes with maxdeg<=3 must all be among them
import gzip
nmatch=tot=0
buckets={}
for es in C14:
    G=graph(es); buckets.setdefault(nx.weisfeiler_lehman_graph_hash(G,node_attr='t'),[]).append(G)
for l in gzip.open('/home/user/Erdos-757/data/census_n14_m12_classes.jsonl.gz','rt'):
    r=json.loads(l); es=[tuple(e) for e in r['edges']]
    d={}
    for e in es:
        for v in e: d[v]=d.get(v,0)+1
    if max(d.values())>3: continue
    tot+=1; G=graph(es); h=nx.weisfeiler_lehman_graph_hash(G,node_attr='t')
    nmatch+=any(nx.is_isomorphic(G,H,node_match=nm) for H in buckets.get(h,[]))
print('realizable census classes with maxdeg<=3:',tot,'found among C14:',nmatch)
STATS['census_consistency']=dict(realizable_maxdeg_le3=tot,found=nmatch)
json.dump(STATS,open('stats_C14.json','w'),indent=1)
print('secs',time.time()-t0)
