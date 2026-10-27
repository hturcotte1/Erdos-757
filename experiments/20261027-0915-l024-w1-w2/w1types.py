import sys, itertools
sys.path.insert(0,'/home/user/Erdos-757/experiments/prover/L024')
from hyp24 import load_pieces
RICH = {'(10,7,4)#0','(10,7,4)#3','(15,11,6)#4','(15,11,6)#5','(15,11,6)#14','(15,11,6)#15','(15,11,6)#16','(15,11,6)#17',
        '(17,13,7)#0','(17,13,7)#1','(17,13,7)#2','(17,13,7)#3','(17,13,7)#4','(17,13,7)#5'}
def nonrich(pieces):
    return [P for P in pieces if P['name'] not in RICH]
def types(k, pieces, nmin=25):
    nr = nonrich(pieces)
    out = []
    for combo in itertools.combinations_with_replacement(range(len(nr)), k):
        Ps = [nr[i] for i in combo]
        n = sum(P['n'] for P in Ps); W = sum(P['W'] for P in Ps)
        if n < nmin: continue
        if W < 35*k - 96: continue
        out.append(tuple(P['name'] for P in Ps))
    return out
if __name__ == '__main__':
    pcs = load_pieces()
    print(len(nonrich(pcs)), [P['name'] for P in nonrich(pcs)])
    for k in (2,3,4):
        t = types(k, pcs); print(k, len(t))
        if k==2: print(t[:5], len(types(2,pcs,nmin=0)))
        from collections import Counter
        print(Counter(tuple(sorted(x.split('#')[0] for x in tt)) for tt in t).most_common(12))
