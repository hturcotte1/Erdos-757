import sys, json, time
sys.path.insert(0,'src')
from part3m import *
lib=load_library()
for i,g in enumerate(json.load(open('part3a_results_n18.json'))['graphs']):
    lib.append(Comp('gen%d_%d#%d'%(g['n'],i,i),g['n'],[tuple(e) for e in g['edges']]))
v=json.load(open('counterexample_conjecture_T_n21.json'))['graphs']
for i,g in enumerate(v): lib.append(Comp('K21_%d'%i,21,[tuple(e) for e in g['edges']]))
by={c.name:c for c in lib}
tasks=[('K21_%d'%i,'e3#0') for i in range(5)]
tasks+=[(a,b) for a in by if a.startswith('t14') for b in by if b.startswith('t10')]
t0=time.time(); hits=[]; done=0; trunc=[]
tl=float(sys.argv[1])
for a,b in tasks:
    if time.time()-t0>tl: break
    comps=[by[a],by[b]]
    try:
        covs,nodes=minimal_covers(comps,4,max_nodes=3_000_000)
    except RuntimeError:
        trunc.append((a,b)); print('TRUNC',a,b,flush=True); continue
    done+=1
    print(a,b,len(covs),round(time.time()-t0),flush=True)
    if covs: hits.append({'W':[a,b],'k':4,'covers':covs})
json.dump({'k':4,'done':done,'trunc':trunc,'tasks':len(tasks),'hits':hits},open('part3m_n25.json','w'))
print('done',done,'of',len(tasks))
