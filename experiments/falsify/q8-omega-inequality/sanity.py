from q8lib import *
A12b=[0,178,198,218,227,235,272,276,287,317,356,436]
ms=masks_of(A12b); print(len(ms),'edges')
i=A12b.index(287)
# single D={287}, S=full: use mode 1 param 1 and look at D4 hist; also direct via python reference
import itertools
def ref(A,D):
    A=sorted(A); E=[set(e) for e in ap_edges(A)]
    tr=[frozenset(e-set(D)) for e in E]; tr=set(tr)
    K=[t for t in tr if not any(u<t for u in tr)]
    verts=sorted(set().union(*K))
    for k in range(len(verts)+1):
        for c in itertools.combinations(verts,k):
            if all(set(c)&t for t in K): tau=k;break
        else: continue
        break
    e1=sum(len(t)==1 for t in K); e2=sum(len(t)==2 for t in K)
    R=len(A)-len(D)
    return tau,e1,e2,R,21*tau,9*R+5*e2+12*e1, 7*tau, 3*R+2*e2+4*e1
if __name__=="__main__": print(ref(A12b,[287]))
if __name__=="__main__":
  r=run_cases([(1,12,ms,1,1,0),(2,12,ms,0,0,0)])
  for k,v in r.items(): print(k,{a:b for a,b in v.items() if a not in('hist','viol','eq')}, {h:min(x) for h,x in v['hist'].items()})
