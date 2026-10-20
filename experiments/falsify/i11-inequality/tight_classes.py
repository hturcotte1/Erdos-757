import re,sys,json
sys.path.insert(0,'/home/user/Erdos-757')
from isocheck import parse,graph
import networkx as nx
from e757.cpsat_model import find_f7
def reps(lst):
    buckets={};out=[]
    for es in lst:
        G=graph(es);h=nx.weisfeiler_lehman_graph_hash(G,node_attr='t');b=buckets.setdefault(h,[])
        if not any(nx.is_isomorphic(G,H,node_match=lambda a,b:a['t']==b['t']) for H in b): b.append(G); out.append(es)
    return out
def sub_ok(es,n):
    masks=[sum(1<<v for v in e) for e in es]
    return all(sum(1 for mk in masks if mk&S==mk)<=bin(S).count('1')-2 for S in range(1,1<<n) if any(mk&S==mk for mk in masks))
res={}
for name,f,n in (('C10 (10,7,4)','conn_all_10_7_4.txt',10),('C13 (13,8,5)','conn_all_13_8_5.txt',13)):
    r=reps(parse(open(f).read()))
    res[name]=[dict(edges=es,f7_free=not find_f7(es),e_sub_ok=sub_ok(es,n)) for es in r]
    print(name,'iso classes',len(r),'F7-free',sum(x['f7_free'] for x in res[name]),'F7-free and e(S)<=|S|-2',sum(x['f7_free'] and x['e_sub_ok'] for x in res[name]))
json.dump(res,open('results_tight_classes.json','w'),indent=1)
