"""Union over all processed data of tau_max(s,m) for induced subsets; then exact frontier LP (Fractions)."""
from common import *
import test23_gens as G
from fractions import Fraction as F
import sys
S='/tmp/claude-0/-home-user-Erdos-757/32619e2f-2987-5d2f-a1f8-a110778bce61/scratchpad/'
srcs={'abs12':G.gen_abs12,'abs14':G.gen_abs14,'n14':G.gen_n14,'n12':G.gen_n12,'small':G.gen_small}
tmax={}
for name,g in srcs.items():
    j=run_c(g())
    for s,m,t,c,wl,wm,sl in j['hist']:
        k=(s,m)
        if t>tmax.get(k,(-1,))[0]: tmax[k]=(t,name)
    print(name,'done',flush=True)
# ext14 file (15-point sets)
p=subprocess.run(['nice','-n','5',HERE+'/subsets'],stdin=open(S+'ext14.txt'),capture_output=True,text=True)
j=json.loads("\n".join(l for l in p.stdout.splitlines() if not l.startswith('VIOLATION')))
for s,m,t,c,wl,wm,sl in j['hist']:
    k=(s,m)
    if t>tmax.get(k,(-1,))[0]: tmax[k]=(t,'ext14')
json.dump({"%d,%d"%k:v for k,v in sorted(tmax.items())},open(HERE+'/results_tau_max_union.json','w'),indent=0)
print(len(tmax),'cells')
