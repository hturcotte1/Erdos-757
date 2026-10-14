from common import *
import random
from multiprocessing import Pool
rows=[json.loads(l) for l in open('/home/user/Erdos-757/experiments/20261014-0610-extremal-census/results/n12_m10_solutions.jsonl')]
random.seed(757); idx=random.sample(range(len(rows)),300)
def work(ch):
    res=run_cases([mk(i,12,rows[i],0,0) for i in ch],vcap=20)
    H=Counter(); V=[]; st=0
    for i,r in res.items():
        st+=r['states']
        for a,b in r['hist']['Q'].items(): H[a]+=b
        if r['violQ'] or r['violAct']: V.append((i,r['violQ'],r['viol'][:2]))
    return H,V,st
if __name__=='__main__':
    ch=[idx[i::8] for i in range(8)]
    with Pool(3) as p: out=p.map(work,ch)
    H=Counter();V=[];S=0
    for h,v,s in out: H.update(h);V+=v;S+=s
    print('hyps',len(idx),'states',S,'hyps with viol',len(V),'min',min(H),'eq',H[0])
    json.dump(dict(idx=idx,states=S,viol=V,hist=sorted(H.items())),open('step1b_results.json','w'))
