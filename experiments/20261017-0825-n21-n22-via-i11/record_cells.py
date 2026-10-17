"""For n=14..30: cells (n,m,tau) allowed by HY and I11 (slack>=0), m<=n-2, tau<=m, with h=n-tau <= ceil(4n/7)-1 (i.e. beating 4/7)."""
import json,math
res={}
for n in range(14,31):
    hmax=math.ceil(4*n/7)-1; tmin=n-hmax; cells=[]
    for m in range(1,n-1):
        for t in range(tmin,m+1):
            if 17*t<=5*n+3*m and 11*t<=3*n+2*m: cells.append((m,t,3*n+2*m-11*t))
    res[n]=dict(h_max=hmax,tau_min=tmin,cells=cells)
    print(n,'h<=%d (tau>=%d)'%(hmax,tmin),[(m,t,'s=%d'%s) for m,t,s in cells][:12])
json.dump(res,open('results_record_cells.json','w'),indent=1)
