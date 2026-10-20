"""Abstract class search: for each (n,m) in the Henning-Yeo window where I11 could fail, decide with CP-SAT whether an
ordered midpoint hypergraph (linear, injective midpoints, F7-free; class O, NO K30/K31/cores) with exactly m edges and
alpha <= n - tau0 exists, tau0 = floor((3n+2m)/11)+1 = least violating tau.  UNSAT in O => I11 holds on O (hence on O' and on realizable sets)."""
import sys, json, time, os
sys.path.insert(0,'/home/user/Erdos-757')
from e757.cpsat_model import feasible_alpha_le
from e757.saturated import alpha_of_edges
HERE=os.path.dirname(os.path.abspath(__file__))
nmin,nmax,tl,workers=int(sys.argv[1]),int(sys.argv[2]),int(sys.argv[3]),int(sys.argv[4])
mopt=sys.argv[5] if len(sys.argv)>5 else 'O'
out=HERE+'/results_cells_%s_%d_%d.jsonl'%(mopt,nmin,nmax)
for n in range(nmin,nmax+1):
    for m in range(1,n-1):
        lo=(3*n+2*m)//11+1; hi=min((5*n+3*m)//17,m)
        if lo>hi: continue
        T=n-lo
        t0=time.time()
        kw=dict(monotone=True,medial=True) if mopt=='Op' else {}
        r,edges,st=feasible_alpha_le(n,T,m_exact=m,forbid_f7=True,time_limit=tl,workers=workers,**kw)
        rec=dict(n=n,m=m,tau_violating=lo,hy_max_tau=hi,alpha_le=T,result=r,secs=round(time.time()-t0,1),cls=mopt)
        if r=='SAT':
            rec['edges']=edges; rec['alpha_check']=alpha_of_edges(n,edges)
        print(json.dumps(rec),flush=True)
        open(out,'a').write(json.dumps(rec)+'\n')
