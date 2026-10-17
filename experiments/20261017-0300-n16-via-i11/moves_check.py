"""Completeness sanity test for the DFS output: the 47 iso classes of connected (15,11,tau>=6) maxdeg<=3 graphs must be closed under
single-incidence moves (replace a vertex x of an edge by y not in the edge) that keep linearity, connectivity, maxdeg<=3, 15 used vertices and tau>=6."""
import json,sys,itertools
sys.path.insert(0,'.')
import networkx as nx
from gutil import graph
reps=[r[0] for r in json.load(open('classes_B_reps.json'))]
nm=lambda a,b:a['t']==b['t']
buckets={}
for es in reps:
    G=graph([tuple(e) for e in es]); buckets.setdefault(nx.weisfeiler_lehman_graph_hash(G,node_attr='t'),[]).append(G)
def tau_ge(es,k):
    masks=[sum(1<<v for v in e) for e in es]
    def cover(unc,kk):
        if not unc: return True
        if kk==0: return False
        i=(unc&-unc).bit_length()-1; e=masks[i]
        for v in range(15):
            if e>>v&1:
                rest=[j for j in range(len(masks)) if (unc>>j&1) and not (masks[j]>>v&1)]
                if cover(sum(1<<j for j in rest),kk-1): return True
        return False
    return not cover((1<<len(masks))-1,k-1)
def connected(es):
    G=nx.Graph(); 
    for e in es: G.add_edges_from([(e[0],e[1]),(e[1],e[2])])
    return G.number_of_nodes()==15 and nx.is_connected(G)
tested=inclass=0; missing=[]
for es in reps:
    es=[tuple(e) for e in es]
    for ei,e in enumerate(es):
        for x in e:
            for y in range(15):
                if y in e: continue
                ne=tuple(sorted((set(e)-{x})|{y})); new=es[:ei]+[ne]+es[ei+1:]
                if len(set(new))<len(new): continue
                if any(len(set(a)&set(b))>=2 for a,b in itertools.combinations(new,2)): continue
                deg=[0]*15
                for f in new:
                    for v in f: deg[v]+=1
                if max(deg)>3 or not connected(new) or not tau_ge(new,6): continue
                tested+=1
                G=graph(new); h=nx.weisfeiler_lehman_graph_hash(G,node_attr='t')
                if any(nx.is_isomorphic(G,H,node_match=nm) for H in buckets.get(h,[])): inclass+=1
                else: missing.append(new)
print('valid neighbours tested',tested,'in DFS classes',inclass,'missing',len(missing)); json.dump(missing,open('moves_missing.json','w'))
