import sys, json, random, collections, time
sys.path.insert(0,'src')
import networkx as nx
from hg import *
from part2_enum import dual_hypergraph
random.seed(int(sys.argv[2]) if len(sys.argv)>2 else 1)
NTARGET=int(sys.argv[1])

def rand_subcubic(m,eT=None):
    G=nx.empty_graph(m)
    deg=[0]*m
    for i in range(1,m):
        cand=[v for v in range(i) if deg[v]<3]
        v=random.choice(cand); G.add_edge(i,v); deg[i]+=1; deg[v]+=1
    emax=(3*m)//2
    if eT is None: eT=random.randint(m-1,emax)
    tries=0
    while G.number_of_edges()<eT and tries<50*m:
        tries+=1
        a,b=random.sample(range(m),2)
        if deg[a]<3 and deg[b]<3 and not G.has_edge(a,b):
            G.add_edge(a,b); deg[a]+=1; deg[b]+=1
    return G

def evalG(G,check_C=True):
    m=G.number_of_nodes(); e=G.number_of_edges()
    n,es=dual_hypergraph(G)
    nu=len(nx.max_weight_matching(G,maxcardinality=True))
    t=tau(n,es)
    assert t==m-nu,(n,m,t,nu)
    s=3*n+2*m-11*t
    assert s==11*nu-3*e
    if check_C: assert classC_fast(n,es)
    return n,m,e,nu,t,s,es

stats=collections.defaultdict(lambda:[10**9,0])   # n -> [min slack, count]
minrat=10**9; worst=None; cnt=0; t0=time.time()
byn=collections.Counter()
while cnt<NTARGET:
    m=random.randint(6,26)
    G=rand_subcubic(m)
    n=3*m-G.number_of_edges()
    if n<15 or n>40: continue
    if not nx.is_connected(G): continue
    r=evalG(G,check_C=True)
    cnt+=1; byn[r[0]]+=1
    st=stats[r[0]]; st[1]+=1
    if r[5]<st[0]: st[0]=r[5]
    if cnt%20000==0: print(cnt,time.time()-t0,flush=True)
res={'random_samples':cnt,'by_n_count':dict(sorted(byn.items())),'min_slack_by_n':{n:v[0] for n,v in sorted(stats.items())},
     'global_min_slack':min(v[0] for v in stats.values())}
# hill climbing to minimise slack = 11 nu - 3 e
hc={}
for m in range(8,27):
    best=None
    for rep in range(6):
        G=rand_subcubic(m)
        cur=11*len(nx.max_weight_matching(G,maxcardinality=True))-3*G.number_of_edges()
        for step in range(400):
            H=G.copy()
            es=list(H.edges())
            if random.random()<0.5 and es:
                H.remove_edge(*random.choice(es))
            a,b=random.sample(range(m),2)
            if H.degree(a)<3 and H.degree(b)<3 and not H.has_edge(a,b): H.add_edge(a,b)
            if not nx.is_connected(H): continue
            val=11*len(nx.max_weight_matching(H,maxcardinality=True))-3*H.number_of_edges()
            # normalise by size? minimise raw slack (can only shrink by structure)
            if val<=cur: G,cur=H,val
        n_,m_,e_,nu_,t_,s_,es_=evalG(G,check_C=(3*m-G.number_of_edges())<=40)
        if best is None or s_<best[0]: best=(s_,n_,m_,e_,nu_)
    hc[m]=best
res['hillclimb_min_slack_by_m']={m:v for m,v in hc.items()}
res['hillclimb_global_min']=min(v[0] for v in hc.values())
json.dump(res,open('part2_random_results.json','w'),indent=1)
print(json.dumps(res)[:3000])
