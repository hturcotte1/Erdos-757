from common import *
import time
d=json.load(open(ROOT+'/data/small_records.json'))['sets']
F=[2,3]
while len(F)<25: F.append(F[-1]+F[-2])
out={'fib_whole':{}, 'glue':{}}
for n in range(5,26):
    A=F[:n]; E=ap_edges(A); a=alpha(A,E)
    out['fib_whole'][n]=dict(is45=is_45_set(A),m=len(E),h=a,tau=n-a,slack=3*n+2*len(E)-11*(n-a))
    print('fib',n,out['fib_whole'][n],flush=True)
def glue(A,B,q=10**6+3,t=10**12):
    return sorted(list(A)+[q*b+t for b in B])
def rec(name,S):
    S=sorted(S); n=len(S); E=ap_edges(S); t0=time.time(); a=alpha(S,E)
    r=dict(n=n,m=len(E),h=a,tau=n-a,slack=3*n+2*len(E)-11*(n-a),is45=is_45_set(S),secs=round(time.time()-t0,1))
    out['glue'][name]=r; print(name,r,flush=True)
Ab=d['14']['set']
rec('Abase+Abase',glue(Ab,Ab))
rec('Abase+12',glue(Ab,d['12']['set']))
rec('Abase+12b',glue(Ab,d['12b']['set']))
rec('12+12b',glue(d['12']['set'],d['12b']['set']))
rec('12+12c+Abase',glue(glue(d['12']['set'],d['12c']['set'],q=10**5+7,t=10**11),Ab,q=10**9+9,t=10**20) if False else glue(glue(d['12']['set'],d['12c']['set']),[x*10**9+x for x in Ab],q=1,t=10**25))
json.dump(out,open(HERE+'/results_fib_glue.json','w'),indent=1)
