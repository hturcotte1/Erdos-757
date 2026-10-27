import sys, json, subprocess, numpy as np
sys.path.insert(0,'src')
from hg import *
from ortools.sat.python import cp_model
fn=sys.argv[1]; n=int(sys.argv[2]); t=int(sys.argv[3])
gs=json.load(open(fn))['graphs']
def tau_cpsat(n,edges):
    m=cp_model.CpModel(); x=[m.NewBoolVar('x%d'%i) for i in range(n)]
    for e in edges: m.Add(sum(x[v] for v in e)>=1)
    m.Minimize(sum(x)); s=cp_model.CpSolver(); s.parameters.num_workers=1
    assert s.Solve(m)==cp_model.OPTIMAL
    return int(s.ObjectiveValue())
def eS_ok_chunked(n,edges):
    masks=[(1<<a)|(1<<b)|(1<<c) for a,b,c in edges]
    N=1<<n; CH=1<<22
    for st in range(0,N,CH):
        S=np.arange(st,min(N,st+CH),dtype=np.int64)
        cnt=np.zeros(len(S),dtype=np.int16); pc=np.zeros(len(S),dtype=np.int16)
        for mk in masks: cnt+=((S&mk)==mk)
        for i in range(n): pc+=((S>>i)&1).astype(np.int16)
        if ((pc>=2)&(cnt>pc-2)).any(): return False
    return True
B='/home/user/Erdos-757/experiments/prover/L012/bin/'
lines=['FOUND: '+' '.join('(%d,%d,%d)'%tuple(g['edges'][i]) for i in range(len(g['edges']))) for g in gs]
out=subprocess.run([B+'filt','FOUND',str(n),'tau',str(t)],input='\n'.join(lines)+'\n',capture_output=True,text=True).stdout
print(out.strip().splitlines()[-1])
res=[]
for g in gs:
    es=[tuple(e) for e in g['edges']]
    r={'n':n,'m':len(es),'connected':is_connected(n,es),'linear':linear(es),'F7free_py':not has_F7(n,es),'eS_ok_bruteforce':eS_ok_chunked(n,es),'tau_cpsat':tau_cpsat(n,es),'maxdeg':max(degrees(n,es))}
    r['slack']=3*n+2*len(es)-11*r['tau_cpsat']; r['edges']=es
    print({k:v for k,v in r.items() if k!='edges'},flush=True); res.append(r)
json.dump({'filt_summary':out.strip().splitlines()[-1],'graphs':res},open('verified_'+fn,'w'))
