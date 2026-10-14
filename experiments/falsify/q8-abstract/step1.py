from common import *
from multiprocessing import Pool
rows=[json.loads(l) for l in open('/home/user/Erdos-757/experiments/20261014-0610-extremal-census/results/n12_m10_solutions.jsonl')]
print(len(rows),'solutions')
def work(chunk):
    cases=[mk(i,12,e,1,2) for i,e in chunk]
    res=run_cases(cases,vcap=20)
    H=Counter(); V=[]; empt=Counter(); states=0
    for i,r in res.items():
        for k,v in r['hist']['Q'].items(): H[k]+=v
        states+=r['states']
        if r['violQ'] or r['violAct']: V.append((i,r['viol']))
    return H,V,states
if __name__=='__main__':
    idx=list(enumerate(rows)); chunks=[idx[i:i+500] for i in range(0,len(idx),500)]
    with Pool(4) as p: out=p.map(work,chunks)
    H=Counter();V=[];S=0
    for h,v,s in out: H.update(h);V+=v;S+=s
    print('states',S,'violations',len(V)); print('min slack',min(H)); print(sorted(H.items())[:8])
    json.dump({'n_hyp':len(rows),'states':S,'viol':V[:20],'hist':sorted(H.items())},open('step1_results.json','w'))
