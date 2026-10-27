"""Exact search for tight K = v + A + (3,1,1) with 4 pairs, A a tight connected comp, E = {x0,x1,x2} the extra edge.
cross pairs (x_i,a_i), inner pairs (b,b') in A.  Tightness <=> every maximum independent set of A u E contains one of the pairs.
Maximum independent sets of E: E minus one vertex.  Exhaustive over c = number of cross pairs in {2,3}  (c=1 is excluded by the class-C count k<=sum(def)-1; c=0 leaves E isolated)."""
import sys, json, itertools, time
sys.path.insert(0,'src')
import numpy as np
from part3a import *

def bitsets(A):
    M=A.mis; N=len(M)
    Bv=[]
    for a in range(A.n):
        col=((M>>a)&1).astype(np.uint8)
        Bv.append(int.from_bytes(np.packbits(col,bitorder='little').tobytes(),'little'))
    return Bv,N

def build(A,cross,inner):
    nA=A.n; edges=[tuple(e) for e in A.edges]
    X=[nA,nA+1,nA+2]; v=nA+3
    edges.append(tuple(X))
    for i,a in enumerate(cross): edges.append(tuple(sorted((X[i],a,v))))
    for (b,b2) in inner: edges.append(tuple(sorted((b,b2,v))))
    return nA+4,edges

def search(A,tl=1e9):
    t0=time.time()
    Bv,N=bitsets(A); full=(1<<N)-1
    nA=A.n
    inedge=A.pairs_in_edge
    pairs=[(b,b2) for b in range(nA) for b2 in range(b+1,nA) if (b,b2) not in inedge]
    Bp={p:Bv[p[0]]&Bv[p[1]] for p in pairs}
    # MIS as vertex lists
    M=A.mis
    mis_vs=[[v for v in range(nA) if (int(m)>>v)&1] for m in M]
    sols=[]   # (cross list, inner list)
    # c=2
    for a1 in range(nA):
        for a2 in range(nA):
            if a2==a1: continue
            U=full & ~(Bv[a1]&Bv[a2])
            if U==0: continue
            i0=(U&-U).bit_length()-1
            I0=mis_vs[i0]
            for p1 in itertools.combinations(I0,2):
                if p1 in inedge or a1 in p1 or a2 in p1: continue
                rem=U & ~Bp[p1]
                if rem==0:
                    # 3 pairs suffice (2 cross + 1 inner): any 4th inner pair disjoint
                    for p2 in pairs:
                        if set(p2)&{a1,a2,p1[0],p1[1]}: continue
                        sols.append(([a1,a2],[p1,p2]))
                    continue
                i1=(rem&-rem).bit_length()-1
                I1=mis_vs[i1]
                for p2 in itertools.combinations(I1,2):
                    if p2 in inedge or set(p2)&{a1,a2,p1[0],p1[1]}: continue
                    if rem & ~Bp[p2]==0:
                        sols.append(([a1,a2],[p1,p2]))
    # c=3
    for a1,a2,a3 in itertools.permutations(range(nA),3):
        F=0
        for (s,s2) in ((a2,a3),(a1,a3),(a1,a2)):
            F|= full & ~Bv[s] & ~Bv[s2]
        if F==0: continue
        i0=(F&-F).bit_length()-1
        for p in itertools.combinations(mis_vs[i0],2):
            if p in inedge or set(p)&{a1,a2,a3}: continue
            if F & ~Bp[p]==0: sols.append(([a1,a2,a3],[p]))
    return sols,N,round(time.time()-t0,1)

def inc(n,edges):
    B=nx.Graph()
    for v in range(n): B.add_node(('v',v),t=0)
    for i,e in enumerate(edges):
        B.add_node(('e',i),t=1)
        for w in e: B.add_edge(('v',w),('e',i))
    return B
def iso(B1,B2): return nx.is_isomorphic(B1,B2,node_match=lambda a,b:a['t']==b['t'])

def run(A,cap=200000):
    sols,N,secs=search(A)
    found=[]; stats={'raw_solutions':len(sols),'MIS':N,'secs':secs,'notC':0,'tight':0}
    seen_keys=set()
    import random
    random.seed(1)
    sample=sols if len(sols)<=cap else random.sample(sols,cap)
    for cross,inner in sample:
        n,edges=build(A,cross,inner)
        if not classC_fast(n,edges): stats['notC']+=1; continue
        t=tau(n,edges); s=slack(n,edges,t)
        if s!=0: stats['slack_%d'%s]=stats.get('slack_%d'%s,0)+1; continue
        stats['tight']+=1
        B=inc(n,edges)
        k=(len(edges),tuple(sorted(degrees(n,edges))))
        for (k2,B2,_) in found:
            if k2==k and iso(B,B2): break
        else: found.append((k,B,edges))
    stats['distinct_classes']=len(found); stats['sampled']=len(sample)
    return stats,[f[2] for f in found]

if __name__=='__main__':
    lib=load_library()
    for i,g in enumerate(json.load(open('part3a_results_n18.json'))['graphs']):
        lib.append(Comp('gen%d_%d#%d'%(g['n'],i,i),g['n'],[tuple(e) for e in g['edges']]))
    for i,g in enumerate(json.load(open('counterexample_conjecture_T_n21.json'))['graphs']):
        lib.append(Comp('K21_%d'%i,21,[tuple(e) for e in g['edges']]))
    names=sys.argv[1].split(',')
    out={}
    for nm in names:
        comps=[c for c in lib if c.name.startswith(nm)]
        for A in comps:
            st,gs=run(A)
            print(A.name,A.n,st,flush=True)
            out[A.name]={'stats':st,'graphs':gs}
    json.dump(out,open('e3plus_%s.json'%sys.argv[2],'w'))
