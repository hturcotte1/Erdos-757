import json,random,sys
from feed import stream
random.seed(5)
sel=json.load(open('selected_all.json'))
Mout=[];Rout=[]
def conv(l):
    t=l.split(); n,m=int(t[0]),int(t[1]); e=[tuple(map(int,x)) for x in zip(*[iter(t[3:])]*3)]
    return n,m,e
def fmt(n,e): return '%d %d %s'%(n,len(e),' '.join('%d,%d,%d'%x for x in e))
Mres=[];Rres=[];cm=cr=0
for o in sel:
    n,m,t,s=o['n'],o['m'],o['tau'],o['slack']
    if s>12 or s<0: continue
    sat=(m==n-2)
    if not sat and n>16: continue
    for l in stream(o['path']):
        nn,mm,e=conv(l)
        if sat and 8<=nn:
            cm+=1
            if len(Mres)<20000: Mres.append(fmt(nn,e))
            elif random.random()<20000/cm: Mres[random.randrange(20000)]=fmt(nn,e)
        if nn<=16 and s<=9:
            cr+=1
            if len(Rres)<20000: Rres.append(fmt(nn,e))
            elif random.random()<20000/cr: Rres[random.randrange(20000)]=fmt(nn,e)
Rres.append('3 1 0,1,2')
open('M_list.txt','w').write('\n'.join(Mres)+'\n'); open('R_list.txt','w').write('\n'.join(Rres)+'\n')
print(len(Mres),cm,len(Rres),cr)
