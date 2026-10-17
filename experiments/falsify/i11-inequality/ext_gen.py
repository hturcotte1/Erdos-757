"""Generate all (4,5) single-point extensions (new point x lies in a new 3-AP with two old points) of census classes,
write them as C-input lines (n E triples) to a file, one set per line, plus a sidecar json of sets.  Exact integers
(set scaled by 4 so every candidate is an integer)."""
import sys, json, gzip, itertools, random
from multiprocessing import Pool
sys.path.insert(0,'/home/user/Erdos-757/experiments/falsify/i11-inequality')
from common import *
def ndist(q): return len({abs(u-v) for u,v in itertools.combinations(q,2)})
def ext(A0):
    A=sorted(4*a for a in A0); S=set(A); out=[]
    cand=set()
    for a,b in itertools.combinations(A,2):
        s=a+b; cand.add(s//2); cand.add(2*a-b); cand.add(2*b-a)
    cand-=S
    tr=list(itertools.combinations(A,3))
    for x in sorted(cand):
        if all(ndist((x,)+q)>=5 for q in tr): out.append(sorted(A+[x]))
    return out
def work(A0):
    res=[]
    for B in ext(A0):
        E=edges_idx(B); res.append(line(len(B),E))
    return res
if __name__=="__main__":
    which=sys.argv[1]; outf=sys.argv[2]; nproc=int(sys.argv[3])
    if which=='n14':
        sets=[json.loads(l)['set'] for l in gzip.open(ROOT+'/data/census_n14_m12_classes.jsonl.gz','rt')]
    else:
        recs=json.load(gzip.open(ROOT+'/experiments/20261014-1005-census-dfs/results/realized_n12.json.gz','rt'))
        random.seed(757); random.shuffle(recs); sets=[r['set'] for r in recs[:int(which[4:])]]
    cnt=0
    with open(outf,'w') as f, Pool(nproc) as p:
        for res in p.imap_unordered(work,sets,chunksize=8):
            for l in res: f.write(l); cnt+=1
    print(which,'sets generated',cnt)
