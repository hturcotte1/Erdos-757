import sys,json
sys.path.insert(0,'/home/user/Erdos-757')
from e757.cpsat_model import load_cores
cores=load_cores('data/forbidden_ordered_n7.json','data/forbidden_ordered_n8.json')
out=['12']
for c in cores:
    v=c['n']
    for refl in (False,True):
        if refl:
            ed=[(v-1-k,v-1-j,v-1-i) for i,j,k in c['edges']]
            rel=None if c['relation'] is None else sorted(v-1-x for x in c['relation'])
        else:
            ed=[tuple(x) for x in c['edges']]; rel=c['relation']
        kind=1 if c['kind']=='extra_ap' else 0
        s=f"{kind} {v} {len(ed)} "+" ".join(f"{a} {b} {cc}" for a,b,cc in ed)
        if kind: s+=" "+" ".join(map(str,rel))
        out.append(s)
open(sys.argv[1],'w').write("\n".join(out)+"\n")
