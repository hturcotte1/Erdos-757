from common import *
from collections import Counter
mn=10**9; rows=0; viol=0; hist=Counter(); eqs=Counter(); bysrc={}
for l in gzip.open(ROOT+'/experiments/20261014-0020-lp-fit/dataset.jsonl.gz','rt'):
    r=json.loads(l); rows+=1
    sl=3*r['n']+2*r['m']-11*r['tau']
    if sl<0: viol+=1
    mn=min(mn,sl)
    if sl<=0: eqs[(r['n'],r['m'],r['tau'],r['saturated'])]+=1
    k=r['n']
    bysrc.setdefault(k,[10**9,None]); 
    if sl<bysrc[k][0]: bysrc[k]=[sl,r['src']]
    if sl<=2 and r['n']>=13 and r['src'].startswith('rand'): hist[(r['n'],r['m'],r['tau'],sl)]+=1
out=dict(rows=rows,violations=viol,min_slack=mn,equality=[dict(n=k[0],m=k[1],tau=k[2],saturated=k[3],rows=v) for k,v in sorted(eqs.items())],
         min_slack_by_n={k:v for k,v in sorted(bysrc.items())},low_slack_random_n_ge13=[[list(k),v] for k,v in hist.items()])
json.dump(out,open(HERE+'/results_test4.json','w'),indent=1)
print(rows,viol,mn); print(out['equality']); print(out['min_slack_by_n'])
