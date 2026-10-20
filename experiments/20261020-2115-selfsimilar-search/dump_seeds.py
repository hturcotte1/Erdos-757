#!/usr/bin/env python3
"""Dump seed sets (normalised: min 0, gcd 1, canonical under reflection, deduped) to seeds_<tag>.txt
lines: 'id n x0 .. x_{n-1}'; metadata in seeds_meta.json (id -> description)."""
import json, gzip, sys, math
R='/home/user/Erdos-757/'
def norm(s):
    s=sorted(s); m=s[0]; s=[x-m for x in s]; g=0
    for x in s: g=math.gcd(g,x)
    s=[x//g for x in s]
    t=sorted(s[-1]-x for x in s)
    return tuple(min(tuple(s),tuple(t)))
groups={}  # tag -> {normset: desc}
def add(tag,s,desc):
    groups.setdefault(tag,{}).setdefault(norm(s),desc)
sr=json.load(open(R+'data/small_records.json'))['sets']
for k,v in sr.items():
    if v['n']>=11: add(f"n{v['n']}",v['set'],f"small_records:{k}")
add('n11',[0,49,75,83,98,101,117,119,121,159,269],'reader O')
d12=json.load(gzip.open(R+'experiments/20261014-1005-census-dfs/results/realized_n12.json.gz'))
for i,r in enumerate(d12): add('n12',r['set'],f"n12class:{i}")
for i,l in enumerate(gzip.open(R+'data/census_n14_m12_classes.jsonl.gz')):
    r=json.loads(l); add('n14',r['set'],f"n14class:{i}")
for i,l in enumerate(gzip.open(R+'data/ext15_sets.jsonl.gz')):
    r=json.loads(l); add('n15',r['set'],f"ext15:{i}")
# derived: delete one point
for tag_src,tag_dst in (('n14','n13'),('n12','n11')):
    for s,desc in list(groups[tag_src].items()):
        for j in range(len(s)):
            t=list(s[:j])+list(s[j+1:]); add(tag_dst,t,f"{desc}-del{j}")
meta={}
for tag,g in groups.items():
    with open(f'seeds_{tag}.txt','w') as f:
        for i,(s,desc) in enumerate(sorted(g.items())):
            sid=f"{tag}_{i}"; meta[sid]=desc
            f.write(f"{i} {len(s)} "+" ".join(map(str,s))+"\n")
    print(tag,len(g))
json.dump(meta,open('seeds_meta.json','w'))
