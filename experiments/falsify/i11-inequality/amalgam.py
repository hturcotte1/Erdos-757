"""Amalgams: A and q*B+t (or reflected) identified at ONE point (a in A, b in B). q generic large prime-ish.
Checks (4,5) exactly, then computes n, m, tau exactly and I11 slack."""
from common import *
import time, itertools, sys
d=json.load(open(ROOT+'/data/small_records.json'))['sets']
pairs=[('14','14'),('14','12'),('12','12b'),('12','12c'),('14','11'),('14','10'),('12b','12c'),('14','8')]
q=100003
res=[];best=None;nviol=0;ntot=0;n45=0
t0=time.time()
for ka,kb in pairs:
    A=sorted(d[ka]['set']); B0=sorted(d[kb]['set'])
    for refl in (False,True):
        B=[-x for x in B0] if refl else B0[:]
        B=sorted(B)
        for a in A:
            for b in B:
                C=sorted(set(A)|{a+q*(x-b) for x in B})
                ntot+=1
                if len(C)!=len(A)+len(B)-1: continue
                if not is_45_set(C): continue
                n45+=1
                E=ap_edges(C); h=alpha(C,E); n=len(C); m=len(E); tau=n-h
                sl=3*n+2*m-11*tau
                if sl<0: nviol+=1; print('VIOLATION',ka,kb,refl,a,b,n,m,tau,sl)
                if best is None or sl<best[0]: best=(sl,ka,kb,refl,a,b,n,m,tau)
    print(ka,kb,'done total',ntot,'is45',n45,'viol',nviol,'best',best,round(time.time()-t0),flush=True)
json.dump(dict(tested=ntot,is45=n45,violations=nviol,best=best,q=q),open(HERE+'/results_amalgam.json','w'))
