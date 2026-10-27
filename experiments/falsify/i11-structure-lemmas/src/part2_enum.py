import sys, json, itertools, collections, time
sys.path.insert(0,'src')
import networkx as nx
from hg import *

def gen_subcubic(maxm):
    """all connected simple graphs with max degree <=3 on 1..maxm vertices, up to isomorphism."""
    levels={1:[nx.empty_graph(1)]}
    for m in range(2,maxm+1):
        buckets=collections.defaultdict(list)
        cnt=0
        for G in levels[m-1]:
            avail=[v for v in G if G.degree(v)<3]
            for k in (1,2,3):
                for S in itertools.combinations(avail,k):
                    H=G.copy(); H.add_node(m-1)
                    for s in S: H.add_edge(m-1,s)
                    key=nx.weisfeiler_lehman_graph_hash(H,iterations=3)
                    key=(key,H.number_of_edges(),tuple(sorted(d for _,d in H.degree())))
                    b=buckets[key]
                    for X in b:
                        if nx.is_isomorphic(X,H): break
                    else:
                        b.append(H); cnt+=1
        levels[m]=[X for b in buckets.values() for X in b]
        print('m',m,len(levels[m]),flush=True)
    return levels

def dual_hypergraph(G):
    """H from G: vertex per G-edge, plus pendant vertices. returns n, edges"""
    nodes=list(G.nodes()); idx={v:i for i,v in enumerate(nodes)}
    vid={}; nxt=0
    for (a,b) in G.edges():
        vid[frozenset((a,b))]=nxt; nxt+=1
    edges=[]
    for v in nodes:
        t=[vid[frozenset((v,u))] for u in G[v]]
        while len(t)<3:
            t.append(nxt); nxt+=1
        edges.append(tuple(sorted(t)))
    return nxt,edges

if __name__=='__main__':
    maxm=int(sys.argv[1])
    t0=time.time()
    import pickle, os
    if os.path.exists('levels_cache_%d.pkl'%maxm): levels=pickle.load(open('levels_cache_%d.pkl'%maxm,'rb'))
    else:
        levels=gen_subcubic(maxm); pickle.dump(levels,open('levels_cache_%d.pkl'%maxm,'wb'))
    print('gen time',time.time()-t0)
    rows=[]
    minslack={}   # (n,m)->min slack
    viol=[]; mism_tau=0; mism_stated=collections.Counter(); nu_viol=0
    nC=0; nCfast=0; ntot=0; minratio=None
    for m,L in levels.items():
        for G in L:
            e=G.number_of_edges()
            n,es=dual_hypergraph(G)
            nu=len(nx.max_weight_matching(G,maxcardinality=True))
            t=tau(n,es)
            ntot+=1
            if t!=m-nu: mism_tau+=1
            # stated formula: tau = m - nu + #edges all of whose vertices have degree 1
            d=degrees(n,es)
            corr=sum(1 for E in es if all(d[v]==1 for v in E))
            if t!=m-nu+corr: mism_stated[m]+=1
            s=slack(n,es,t)
            assert s==11*nu-3*e or m==0
            if nu*11<3*e: nu_viol+=1; viol.append((n,m,t,s))
            if n<=14:
                ok=in_C(n,es,brute=True)
                assert ok,(n,m,es)
                nC+=1
            assert classC_fast(n,es),(n,m,es)
            nCfast+=1
            key=(n,m)
            if key not in minslack or s<minslack[key][0]: minslack[key]=(s,e,nu)
            r=nu/e if e else None
    out={'maxm':maxm,'total_graphs':ntot,'checked_in_C_bruteforce_n_le_14':nC,'checked_in_C_hall_C_all':nCfast,'tau_neq_m_minus_nu':mism_tau,
         'stated_formula_mismatch_by_m':dict(mism_stated),'nu_lt_3e_over_11':nu_viol,'violations':viol,
         'counts_by_m':{m:len(L) for m,L in levels.items()},
         'minslack_by_nm':{f'{n},{m}':v for (n,m),v in sorted(minslack.items())}}
    json.dump(out,open('part2_enum_results.json','w'),indent=1)
    # table
    n14={k:v for k,v in minslack.items() if k[0]<=14}
    print('min slack over n<=14:',min(v[0] for v in n14.values()))
    print('min slack over all:',min(v[0] for v in minslack.values()))
    print('total',ntot,'stated mismatch',dict(mism_stated),'nu viol',nu_viol)
