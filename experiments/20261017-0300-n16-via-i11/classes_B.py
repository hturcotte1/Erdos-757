import re,sys,json
sys.path.insert(0,'/home/user/Erdos-757'); sys.path.insert(0,'.')
import networkx as nx
from gutil import graph
from e757.cpsat_model import find_f7
nm=lambda a,b:a['t']==b['t']
buckets={}; reps=[]; tot=0; f7n=0
for l in open('G_B_conn15.txt'):
    t=list(map(int,l.split()))[1:]; es=[tuple(t[3*k:3*k+3]) for k in range(len(t)//3)]
    tot+=1
    G=graph(es); h=nx.weisfeiler_lehman_graph_hash(G,node_attr='t'); b=buckets.setdefault(h,[])
    if any(nx.is_isomorphic(G,H,node_match=nm) for H in b): continue
    b.append(G); reps.append((es,bool(find_f7(es))))
print('labelled',tot,'iso classes',len(reps),'F7-free classes',sum(1 for r in reps if not r[1]))
json.dump(reps,open('classes_B_reps.json','w'))
