"""Referee recheck of Q8. Own plain-Python code; no e757, no falsifier code. sweep.c is my own C sweep."""
import itertools, subprocess, sys, json, re, random
def is45(A):
    A=list(A)
    if len(set(A))!=len(A): return False
    return all(len({abs(x-y) for x,y in itertools.combinations(q,2)})>=5 for q in itertools.combinations(A,4))
def apm(A):
    A=sorted(A); return [(1<<i)|(1<<j)|(1<<k) for i,j,k in itertools.combinations(range(len(A)),3) if A[i]+A[k]==2*A[j]]
def tau_brute(K,R):
    if not K: return 0
    Rl=[b for b in range(R.bit_length()) if R>>b&1]
    for k in range(1,len(Rl)+1):
        for c in itertools.combinations(Rl,k):
            M=sum(1<<b for b in c)
            if all(t&M for t in K): return k
    raise AssertionError
def state(E,S,D):
    assert not any(e&D==e for e in E)
    tr={e&~D for e in E if e&S==e}
    K=[t for t in tr if not any(u!=t and u&t==u for u in tr)]
    R=S&~D; e1=sum(bin(t).count('1')==1 for t in K); e2=sum(bin(t).count('1')==2 for t in K)
    tau=tau_brute(K,R); Rn=bin(R).count('1')
    return dict(tau=tau,e1=e1,e2=e2,R=Rn,Q8=(7*tau,3*Rn+2*e2+4*e1),D4=(21*tau,9*Rn+5*e2+12*e1))
def sweep(A,stride=0):
    E=apm(A); inp=f"{len(A)} {len(E)} {' '.join(map(str,E))}\n"
    out=subprocess.run(['./sweep',str(stride)],input=inp,capture_output=True,text=True).stdout
    return E,out
if __name__=='__main__':
    which=sys.argv[1]
    A12b=[0,178,198,218,227,235,272,276,287,317,356,436]
    Ab=[0,136,200,243,246,249,272,286,298,323,400,528,596,1056]
    if which=='step1':
        assert is45(A12b); E=apm(A12b); idx=sorted(A12b).index(287)
        r=state(E,(1<<12)-1,1<<idx); print('12b D={287}:',r)
        assert r['tau']==5 and r['R']==11 and r['e2']==1 and r['D4']==(105,104) and r['Q8']==(35,35)
        print('D4 violated 105>104; Q8 35<=35 holds. APs:',len(E))
    if which=='sweep':
        A=Ab if sys.argv[2]=='base' else A12b if sys.argv[2]=='12b' else json.loads(sys.argv[2])
        assert is45(A); stride=int(sys.argv[3]) if len(sys.argv)>3 else 0
        E,out=sweep(A,stride); lines=out.splitlines()
        print([l for l in lines if not l.startswith('DUMP')])
        # cross-check dumped states with Python brute force
        bad=0;cnt=0
        for l in lines:
            if l.startswith('DUMP'):
                d=dict(x.split('=') for x in l.split()[1:]); S,D=int(d['S']),int(d['D'])
                r=state(E,S,D); cnt+=1
                if (r['tau'],r['e1'],r['e2'],r['R'])!=(int(d['tau']),int(d['e1']),int(d['e2']),int(d['R'])): bad+=1
        print('python crosscheck of dumped states:',cnt,'checked, mismatches',bad)
