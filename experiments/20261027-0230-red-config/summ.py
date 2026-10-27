import sys,glob,collections,re
rows=collections.defaultdict(lambda:[0,0,99,0,0,-999,99,99,0])
for f in sorted(glob.glob('out/red_*_*.tsv')):
    n,m=map(int,re.findall(r'red_(\d+)_(\d+)',f)[0])
    c=collections.Counter(); mx=0;mcx=0;bmin=999;bmax=-999
    cnt=0;rf=0
    for l in open(f):
        t=l.split('\t'); cnt+=1; rf+=int(t[5]); ms=int(t[13]); mc=int(t[15]); mx=max(mx,ms); mcx=max(mcx,mc); b=int(t[6]); bmin=min(bmin,b); bmax=max(bmax,b)
        c[ms]+=1
    print(n,m,cnt,rf,'max(min|Z|)=',mx,'max(min conn|Z|)=',mcx,'bestval range',bmin,bmax, dict(sorted(c.items())))
