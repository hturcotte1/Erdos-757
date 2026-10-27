"""independent verification of the new tight graphs (n=17 Delta=4 and n=21): pure python F7 / linear / e(S) brute force, CP-SAT tau, connectivity, degrees"""
import sys, json, itertools
sys.path.insert(0,'src')
from hg import *
from ortools.sat.python import cp_model
def tau_cpsat(n,edges):
    m=cp_model.CpModel(); x=[m.NewBoolVar('x%d'%i) for i in range(n)]
    for e in edges: m.Add(sum(x[v] for v in e)>=1)
    m.Minimize(sum(x)); s=cp_model.CpSolver(); s.parameters.num_workers=1
    r=s.Solve(m); assert r==cp_model.OPTIMAL
    return int(s.ObjectiveValue())
d=json.load(open('part3m_post_%s.json'%sys.argv[1]))
out=[]
for g in d['graphs']:
    n=g['n']; es=[tuple(e) for e in g['edges']]
    rec={'n':n,'m':len(es),'connected':is_connected(n,es),'linear':linear(es),'F7_free_python':not has_F7(n,es),
         'eS_ok_bruteforce':eS_ok(n,es),'tau_dp':tau(n,es),'tau_cpsat':tau_cpsat(n,es),'maxdeg':max(degrees(n,es)),'degseq':sorted(degrees(n,es))}
    rec['slack']=3*n+2*len(es)-11*rec['tau_cpsat']
    rec['edges']=es
    out.append(rec)
    print({k:v for k,v in rec.items() if k!='edges'},flush=True)
json.dump(out,open('verified_new_tight_%s.json'%sys.argv[1],'w'))
