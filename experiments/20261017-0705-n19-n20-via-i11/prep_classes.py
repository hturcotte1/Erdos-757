"""Take all labelled connected (12,10,5) maxdeg<=3 graphs (conn_dfs3 output), keep one per isomorphism class among those that are
F7-free and satisfy e(S)<=|S|-2 for all S (both inherited by G=R12+AP subset of H in class O).  Write G = R12 + AP(12,13,14) as ext input lines."""
import re,sys,json
sys.path.insert(0,'/home/user/Erdos-757'); sys.path.insert(0,'/home/user/Erdos-757/experiments/falsify/i11-inequality')
import networkx as nx
from e757.cpsat_model import find_f7
def graph(es):
    G=nx.Graph()
    for i,e in enumerate(es):
        G.add_node(('e',i),t=1)
        for v in e: G.add_node(('v',v),t=0); G.add_edge(('e',i),('v',v))
    return G
def sub_ok(es,n):
    masks=[sum(1<<v for v in e) for e in es]
    for S in range(1,1<<n):
        c=0
        for mk in masks:
            if mk&S==mk: c+=1
        if c and c>bin(S).count('1')-2: return False
    return True
src,out,NV,NAP=sys.argv[1],sys.argv[2],int(sys.argv[3]),int(sys.argv[4])
tot=f7=sub=0; buckets={}; reps=[]
for l in open(src):
    if not l.startswith('FOUND'): continue
    es=[tuple(map(int,t.split(','))) for t in re.findall(r'\(([\d,]+)\)',l)]
    tot+=1
    if find_f7(es): f7+=1; continue
    G=graph(es); h=nx.weisfeiler_lehman_graph_hash(G,node_attr='t'); b=buckets.setdefault(h,[])
    if any(nx.is_isomorphic(G,H,node_match=lambda a,b:a['t']==b['t']) for H in b): continue
    b.append(G)
    if not sub_ok(es,NV): sub+=1; continue
    reps.append(es)
with open(out,'w') as f:
    for es in reps:
        es2=es+[(NV+3*k,NV+3*k+1,NV+3*k+2) for k in range(NAP)]
        f.write("%d "%len(es2)+" ".join("%d %d %d"%e for e in es2)+"\n")
json.dump(dict(labelled_found=tot,with_F7=f7,iso_classes_F7free=sum(len(b) for b in buckets.values()),killed_by_eS=sub,kept=len(reps)),open(out+'.summary.json','w'))
print(tot,f7,sum(len(b) for b in buckets.values()),sub,len(reps))
