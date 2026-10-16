import json,sys,time
from multiprocessing import Pool
from fastcores import has_core
rows=[json.loads(l) for l in open('/home/user/Erdos-757/experiments/20261014-0610-extremal-census/results/n12_m10_solutions.jsonl')]
def f(i): return i, not has_core(12,rows[i])
if __name__=='__main__':
    t=time.time()
    with Pool(4) as p: out=p.map(f,range(len(rows)),chunksize=50)
    ok=[i for i,o in out if o]
    print(len(rows),'time',time.time()-t,'pass full cores',len(ok))
    json.dump(ok,open('census_fullcore_pass.json','w'))
