from common import *
import glob, random
def gen_n14():
    for l in gzip.open(ROOT+'/data/census_n14_m12_classes.jsonl.gz','rt'):
        r=json.loads(l); yield line(r['n'],r['edges'])
def gen_n12(sample=None):
    recs=json.load(gzip.open(ROOT+'/experiments/20261014-1005-census-dfs/results/realized_n12.json.gz','rt'))
    if sample: random.seed(757); recs=random.sample(recs,sample)
    for r in recs: yield line(12,r['edges'])
def gen_small():
    # all realizable classes n=6..11 for every m stored (small-counts)
    for f in sorted(glob.glob(ROOT+'/experiments/20261014-1430-small-counts/results/n*_m*_real.json.gz')+glob.glob(ROOT+'/experiments/20261014-1430-small-counts/results/n*_sample_real.json.gz')):
        n=int(os.path.basename(f).split('_')[0][1:])
        for r in json.load(gzip.open(f,'rt')):
            yield line(n,r['edges'])
def gen_abs12():
    seen=set()
    for l in gzip.open(ROOT+'/experiments/20261014-1005-census-dfs/results/n12_m10_all.jsonl.gz','rt'):
        yield line(12,json.loads(l))
def gen_abs14():
    for l in gzip.open(ROOT+'/experiments/20261014-1005-census-dfs/n14/results/post/filtered.txt.gz','rt'):
        t=l.split()[4:]
        E=[tuple(map(int,x.split(','))) for x in t]
        yield line(14,E)
