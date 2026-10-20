from common import *
import time
d=json.load(open(ROOT+'/data/small_records.json'))['sets']
sets={k:v['set'] for k,v in d.items()}
res={}
t0=time.time()
for k,A in sets.items():
    A=sorted(A); assert is_45_set(A)
    E=edges_idx(A)
    j=run_c([line(len(A),E)])
    res[k]=summarize(j,'small_records '+k)
    res[k]['n']=len(A); res[k]['edges']=E
    print(k,len(A),len(E),'min_slack',j['min_slack'],'viol',j['violations'],[ (e['n'],e['m'],e['tau']) for e in res[k]['equality_cases']])
# all together
allj=run_c([line(len(sorted(A)),edges_idx(A)) for A in sets.values()])
res['ALL']=summarize(allj,'all 7 small_records sets')
res['_secs']=time.time()-t0
json.dump(res,open(HERE+'/results_test1.json','w'),indent=1)
print('ALL',allj['min_slack'],allj['violations'],[(e['n'],e['m'],e['tau'],e['count']) for e in res['ALL']['equality_cases']])
