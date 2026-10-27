import glob,re,collections,json
H=collections.defaultdict(lambda: collections.Counter())  # (slack,d3)->nU2->count
tot=collections.Counter(); mism=0; hits=0; cells=collections.defaultdict(lambda:[0,0])
mx={}
for f in glob.glob('out/*.txt'):
    txt=open(f).read()
    if not txt.rstrip().endswith('DONE'): continue
    for l in txt.splitlines():
        if l.startswith('HIST'):
            _,_,s,_,d,_,u,_,c=l.split(); H[(int(s),int(d))][int(u)]+=int(c)
        elif l.startswith('TAUMISMATCH'): mism+=1
        elif l.startswith('HIT'): hits+=1
print('mismatch',mism,'hits',hits)
for s in sorted({k[0] for k in H}):
    row=[]
    for d in (1,0):
        c=H[(s,d)]
        if c: row.append('D<=3' if d else 'D>=4'); row.append('graphs=%d maxU2=%d dist=%s'%(sum(c.values()),max(c),dict(sorted(c.items()))))
    print('slack',s,' | '.join(map(str,row)))
