import re,sys,json,gzip,random
sys.path.insert(0,'/home/user/Erdos-757'); sys.path.insert(0,'.')
import networkx as nx
from gutil import graph
# the 150 classes = F7-free iso classes (before e(S) filter); rebuild from R12_labelled.txt
from e757.cpsat_model import find_f7
nm=lambda a,b:a['t']==b['t']
buckets={}
for l in open('R12_labelled.txt'):
    if not l.startswith('FOUND'): continue
    es=[tuple(map(int,t.split(','))) for t in re.findall(r'\(([\d,]+)\)',l)]
    if find_f7(es): continue
    G=graph(es); h=nx.weisfeiler_lehman_graph_hash(G,node_attr='t'); b=buckets.setdefault(h,[])
    if not any(nx.is_isomorphic(G,H,node_match=nm) for H in b): b.append(G)
print('classes',sum(len(b) for b in buckets.values()))
def member(es):
    G=graph(es); h=nx.weisfeiler_lehman_graph_hash(G,node_attr='t')
    return any(nx.is_isomorphic(G,H,node_match=nm) for H in buckets.get(h,[]))
def maxdeg(es):
    d={}
    for e in es:
        for v in e: d[v]=d.get(v,0)+1
    return max(d.values())
R='/home/user/Erdos-757/experiments/20261014-1005-census-dfs/results/'
recs=json.load(gzip.open(R+'realized_n12.json.gz','rt'))
tot=ok=0
for r in recs:
    es=[tuple(e) for e in r['edges']]
    if maxdeg(es)<=3:
        tot+=1; ok+=member(es)
print('realizable classes with maxdeg<=3:',tot,'isomorphic to a DFS class:',ok)
random.seed(3); lines=[]
for i,l in enumerate(gzip.open(R+'n12_m10_all.jsonl.gz','rt')):
    if random.random()<0.01: lines.append(json.loads(l))
tot=ok=0
for es in lines[:20000]:
    es=[tuple(e) for e in es]
    if maxdeg(es)<=3:
        tot+=1; ok+=member(es)
print('sampled abstract patterns with maxdeg<=3:',tot,'ok',ok)
