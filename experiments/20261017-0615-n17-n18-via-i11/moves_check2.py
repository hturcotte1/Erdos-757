"""Single-incidence-move closure of a class list inside {connected, linear, maxdeg<=3, F7-free, e(S)-ok, n vertices, tau>=T} (sanity test of completeness)."""
import json,sys,itertools
sys.path.insert(0,'/home/user/Erdos-757'); sys.path.insert(0,'.')
import networkx as nx
from gutil import graph
from e757.cpsat_model import find_f7
from post import sub_ok
f,n,T=sys.argv[1],int(sys.argv[2]),int(sys.argv[3])
reps=[[tuple(e) for e in g] for g in json.load(open(f))]
nm=lambda a,b:a['t']==b['t']
bk={}
for es in reps: bk.setdefault(nx.weisfeiler_lehman_graph_hash(graph(es),node_attr='t'),[]).append(graph(es))
def tau_ge(es,k):
    masks=[sum(1<<v for v in e) for e in es]
    def cover(unc,kk):
        if not unc: return True
        if kk==0: return False
        i=(unc&-unc).bit_length()-1; e=masks[i]
        for v in range(n):
            if e>>v&1:
                rest=sum(1<<j for j in range(len(masks)) if (unc>>j&1) and not (masks[j]>>v&1))
                if cover(rest,kk-1): return True
        return False
    return not cover((1<<len(masks))-1,k-1)
tested=ok=0; missing=[]
for es in reps:
    for ei,e in enumerate(es):
        for x in e:
            for y in range(n):
                if y in e: continue
                ne=tuple(sorted((set(e)-{x})|{y})); new=es[:ei]+[ne]+es[ei+1:]
                if len(set(new))<len(new) or any(len(set(a)&set(b))>=2 for a,b in itertools.combinations(new,2)): continue
                deg=[0]*n
                for g in new:
                    for v in g: deg[v]+=1
                if max(deg)>3 or min(deg)==0: continue
                G=nx.Graph()
                for g in new: G.add_edges_from([(g[0],g[1]),(g[1],g[2])])
                if not nx.is_connected(G): continue
                if find_f7(new) or not tau_ge(new,T) or not sub_ok(new,n): continue
                tested+=1
                Gi=graph(new); h=nx.weisfeiler_lehman_graph_hash(Gi,node_attr='t')
                if any(nx.is_isomorphic(Gi,H,node_match=nm) for H in bk.get(h,[])): ok+=1
                else: missing.append(new)
print(f,'valid neighbours',tested,'in classes',ok,'missing',len(missing)); json.dump(missing,open(f+'.moves_missing.json','w'))
