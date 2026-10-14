import sys,glob
sys.path.insert(0,'/home/user/Erdos-757')
from e757.cpsat_model import load_cores, constraint_violations
CORES=load_cores(*sorted(glob.glob('/home/user/Erdos-757/data/forbidden_ordered_n*.json')))
def _prep():
    out=[]
    for c in CORES:
        v=c['n']
        for refl in (False,True):
            if refl:
                ed=[(v-1-k,v-1-j,v-1-i) for i,j,k in c['edges']]
                rel=None if c['relation'] is None else tuple(sorted(v-1-x for x in c['relation']))
            else:
                ed=[tuple(x) for x in c['edges']]; rel=None if c['relation'] is None else tuple(c['relation'])
            by=[[] for _ in range(v)]
            for e in ed: by[max(e)].append(e)
            out.append((v,by,c['kind'],rel))
    return out
PREP=_prep()
def has_core(n,E):
    Es=set(map(tuple,E))
    for v,by,kind,rel in PREP:
        if v>n: continue
        emb=[]
        def rec(pos,start):
            if pos==v:
                if kind=='extra_ap' and tuple(emb[x] for x in rel) in Es: return False
                return True
            for x in range(start,n-(v-pos)+1):
                emb.append(x)
                if all(tuple(emb[y] for y in e) in Es for e in by[pos]):
                    if rec(pos+1,x+1): emb.pop(); return True
                emb.pop()
            return False
        if rec(0,0): return True
    return False
if __name__=='__main__':
    import json
    rows=[json.loads(l) for l in open('/home/user/Erdos-757/experiments/20261014-0610-extremal-census/results/n12_m10_solutions.jsonl')]
    for i in range(60):
        a=has_core(12,rows[i]); b=bool(constraint_violations(12,[tuple(x) for x in rows[i]],False,False,CORES))
        assert a==b,(i,a,b)
    print('ok')
