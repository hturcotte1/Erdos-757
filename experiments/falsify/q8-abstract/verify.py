import sys, json, itertools
sys.path.insert(0,'/home/user/Erdos-757')
from e757.cpsat_model import constraint_violations, is_ordered_midpoint_hypergraph, find_f7, load_cores
import glob
def trace_info(n,edges,D):
    D=set(D); tr={frozenset(set(e)-D) for e in edges}
    K=[t for t in tr if not any(u<t for u in tr)]
    verts=sorted(set().union(*K)) if K else []
    for k in range(len(verts)+1):
        for c in itertools.combinations(verts,k):
            if all(set(c)&t for t in K): return K,k
def indep(edges,D): return not any(set(e)<=set(D) for e in edges)
def q8(n,edges,D,S=None):
    S=set(range(n)) if S is None else set(S)
    E=[e for e in edges if set(e)<=S]
    K,tau=trace_info(n,E,D)
    R=len(S-set(D)); e1=sum(len(t)==1 for t in K); e2=sum(len(t)==2 for t in K); e3=sum(len(t)==3 for t in K)
    return dict(tau=tau,R=R,e1=e1,e2=e2,e3=e3,lhs=7*tau,rhs=3*R+2*e2+4*e1,K=sorted(map(sorted,K)))
def classify(n,edges):
    cores=load_cores(*sorted(glob.glob('/home/user/Erdos-757/data/forbidden_ordered_n*.json')))
    e=[tuple(x) for x in edges]
    return dict(O=is_ordered_midpoint_hypergraph(n,e) and not find_f7(e,1),
      monotone=not constraint_violations(n,e,True,False,None),
      medial=not constraint_violations(n,e,False,True,None),
      cores=not constraint_violations(n,e,False,False,cores))
if __name__=='__main__':
    rows=[json.loads(l) for l in open('/home/user/Erdos-757/experiments/20261014-0610-extremal-census/results/n12_m10_solutions.jsonl')]
    e=rows[1110]; D=[i for i in range(12) if 260>>i&1]
    print(e,D,indep(e,D)); print(q8(12,e,D)); print(classify(12,e))
