import gzip, itertools, sys, collections
def tau(edges, n):
    for k in range(0, n+1):
        for T in itertools.combinations(range(n), k):
            s=set(T)
            if all(s & set(e) for e in edges): return k
cnt=collections.Counter(); small=[]
for line in gzip.open(sys.argv[1],'rt'):
    if line.startswith('#') or not line.strip(): continue
    parts=line.split(); m=int(parts[0]); E=[tuple(map(int,p.split('.'))) for p in parts[1:]]
    n=1+max(max(e) for e in E)
    if True:
        t=tau(E,n); sl=3*n+2*m-11*t
    else:
        t=None; sl=None
    cnt[(n, None if sl is None else (sl<=5))]+=1
    if sl is not None and sl<=5: small.append((n,m,t,sl))
print(sorted(cnt.items(), key=lambda x:(x[0][0],str(x[0][1]))))
print('low-slack (<=5) Red5-free with n<=10:', small)
