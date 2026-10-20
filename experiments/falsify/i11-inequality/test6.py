from common import *
import time
res={}
# Fibonacci prefixes {2,3,5,8,...}
F=[2,3]
while len(F)<25: F.append(F[-1]+F[-2])
for n in range(5,26):
    A=F[:n]; E=edges_idx(A)
    is45 = is_45_set(A) if n<=14 else None
    t0=time.time()
    j=run_c([line(n,E)])
    s=summarize(j,'fib%d'%n); s['n']=n; s['m']=len(E); s['is45']=is45; s['secs']=round(time.time()-t0,1)
    s.pop('slack1_to_5',None)
    s['full_set_tau_slack']=None
    res[n]=s
    print(n,len(E),'is45',is45,'viol',j['violations'],'min_slack',j['min_slack'],'eq',[(e['n'],e['m'],e['tau']) for e in s['equality_cases']][:8],s['secs'],flush=True)
json.dump(res,open(HERE+'/results_fib.json','w'),indent=1)
