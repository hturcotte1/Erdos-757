"""Heuristic independent check of the (15,11,6,maxdeg3) enumeration: random local search (incidence moves, accept if tau stays >= current or random walk) 
for connected linear 11-edge graphs on 15 vertices with maxdeg<=3 and tau>=6; every graph found must be isomorphic to one of the 49 DFS classes."""
import random,json,sys,itertools,time
sys.path.insert(0,'.')
import networkx as nx
from gutil import graph
nm=lambda a,b:a['t']==b['t']
reps=[r[0] for r in json.load(open('classes_B_reps.json'))]
buckets={}
for es in reps:
    G=graph([tuple(e) for e in es]); buckets.setdefault(nx.weisfeiler_lehman_graph_hash(G,node_attr='t'),[]).append(G)
def tau(masks):
    def cover(unc,k):
        if not unc: return True
        if k==0: return False
        i=(unc&-unc).bit_length()-1; e=masks[i]
        while e:
            v=(e&-e); e^=v
            rest=0
            for j in range(len(masks)):
                if (unc>>j&1) and not (masks[j]&v): rest|=1<<j
            if cover(rest,k-1): return True
        return False
    for k in range(0,12):
        if cover((1<<len(masks))-1,k): return k
def valid(es):
    if len({tuple(sorted(e)) for e in es})<len(es): return False
    for a,b in itertools.combinations(es,2):
        if len(set(a)&set(b))>=2: return False
    deg=[0]*15
    for e in es:
        for v in e: deg[v]+=1
    return max(deg)<=3
random.seed(int(sys.argv[1])); T=float(sys.argv[2]); t0=time.time()
found=0; seen=set(); newclasses=0; tested=0
while time.time()-t0<T:
    # random start
    while True:
        es=[]; deg=[0]*15
        for _ in range(11):
            for _try in range(50):
                e=tuple(sorted(random.sample(range(15),3)))
                if all(deg[v]<3 for v in e) and all(len(set(e)&set(f))<2 for f in es): es.append(e); 
                else: continue
                for v in e: deg[v]+=1
                break
        if len(es)==11: break
    cur=tau([sum(1<<v for v in e) for e in es])
    for step in range(3000):
        if time.time()-t0>T: break
        i=random.randrange(11); x=random.choice(es[i]); y=random.randrange(15)
        if y in es[i]: continue
        ne=tuple(sorted((set(es[i])-{x})|{y})); new=es[:i]+[ne]+es[i+1:]
        if not valid(new): continue
        t=tau([sum(1<<v for v in e) for e in new])
        if t>=cur or random.random()<0.05: es,cur=new,t
        if cur>=6:
            G=nx.Graph()
            for e in es: G.add_edges_from([(e[0],e[1]),(e[1],e[2])])
            if G.number_of_nodes()==15 and nx.is_connected(G):
                tested+=1
                Gi=graph(es); h=nx.weisfeiler_lehman_graph_hash(Gi,node_attr='t')
                key=(h,)
                ok=any(nx.is_isomorphic(Gi,H,node_match=nm) for H in buckets.get(h,[]))
                if not ok: print('NOT IN DFS CLASSES',es,flush=True); newclasses+=1
                seen.add(h)
print('tau>=6 connected hits tested',tested,'distinct WL hashes seen',len(seen),'not in DFS classes',newclasses)
