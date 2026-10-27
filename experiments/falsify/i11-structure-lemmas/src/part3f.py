"""Phase F: from minimal covers with k<4 pairs, add 4-k filler pairs touching extra tight components R; test K in class C exactly."""
import sys, json, itertools, collections, time, os
sys.path.insert(0,'src')
from part3a import *
from part3m import comp_multisets, deff

def main(jsonfile,nmax,tlimit):
    d=json.load(open(jsonfile)); k=d['k']
    lib=load_library()
    if os.path.exists('part3a_results.json'):
        for i,g in enumerate(json.load(open('part3a_results.json'))['graphs']):
            lib.append(Comp('gen%d_%d#%d'%(g['n'],i,i),g['n'],[tuple(e) for e in g['edges']]))
    byname={c.name:c for c in lib}
    t0=time.time()
    tight=[]; tried=0; inC=0
    seen=[]
    for hit in d['hits']:
        W=[byname[nm] for nm in hit['W']]
        nW=sum(c.n for c in W)
        for covs in hit['covers']:
            nf=4-k
            for r in range(0,2*nf+1):
                for Ridx in (comp_multisets(lib,r,nmax-1-nW) if r>0 else [()]):
                    R=[lib[i] for i in Ridx]
                    comps=W+R
                    off=[];o=0
                    for c in comps: off.append(o); o+=c.n
                    NQ=o
                    # vertex info
                    comp_of=[];local=[]
                    for ci,c in enumerate(comps):
                        for x in range(c.n): comp_of.append(ci); local.append(x)
                    used={x for p in covs for x in p}
                    cand=[(u,w) for u in range(NQ) for w in range(u+1,NQ) if u not in used and w not in used
                          and not (comp_of[u]==comp_of[w] and (local[u],local[w]) in comps[comp_of[u]].pairs_in_edge)]
                    nW_c=len(W)
                    # choose nf filler pairs, disjoint, touching all R comps
                    for extra in itertools.combinations(cand,nf):
                        vs=[x for p in extra for x in p]
                        if len(set(vs))<len(vs): continue
                        touched={comp_of[x] for x in vs}
                        if any((nW_c+j) not in touched for j in range(len(R))): continue
                        prs=[tuple(p) for p in covs]+list(extra)
                        nn,edges=build_K(comps,off,NQ,prs)
                        tried+=1
                        if not is_connected(nn,edges): continue
                        if not classC_fast(nn,edges): continue
                        inC+=1
                        t=tau(nn,edges); s=slack(nn,edges,t)
                        rec={'n':nn,'m':len(edges),'tau':t,'slack':s,'W':hit['W'],'R':[c.name for c in R],'edges':edges}
                        if s==0:
                            tight.append(rec)
                    if time.time()-t0>tlimit:
                        print('TIME LIMIT',flush=True); return tight,tried,inC
    return tight,tried,inC

if __name__=='__main__':
    tight,tried,inC=main(sys.argv[1],int(sys.argv[2]),float(sys.argv[3]))
    print('tried',tried,'in C',inC,'tight',len(tight))
    c=collections.Counter((t['n'],t['m'],t['tau']) for t in tight)
    print(c)
    json.dump({'tried':tried,'inC':inC,'tight':tight},open('part3f_out.json','w'))
