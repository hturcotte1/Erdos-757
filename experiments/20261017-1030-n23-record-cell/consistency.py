import sys,json,gzip
sys.path.insert(0,'.')
import engine, dedupe_fast as DF
c14=engine.cell(14,12,6,4); c12=engine.cell(12,10,5,4)
k14={DF.canon_key(g) for g in c14}; k12={DF.canon_key(g) for g in c12}
tot=ok=0
for l in gzip.open('/home/user/Erdos-757/data/census_n14_m12_classes.jsonl.gz','rt'):
    r=json.loads(l); es=[tuple(e) for e in r['edges']]; tot+=1; ok+= DF.canon_key(es) in k14
print('census n=14: classes',tot,'isomorphic to one of the',len(k14),'engine classes (14,12,6,Delta=4):',ok)
recs=json.load(gzip.open('/home/user/Erdos-757/experiments/20261014-1005-census-dfs/results/realized_n12.json.gz','rt'))
tot=ok=0
for r in recs:
    es=[tuple(e) for e in r['edges']]; tot+=1; ok+= DF.canon_key(es) in k12
print('realizable n=12: classes',tot,'isomorphic to one of the',len(k12),'engine classes (12,10,5,4):',ok)
json.dump(dict(n14_total=2910,n14_found=None),open('/dev/null','w'))
