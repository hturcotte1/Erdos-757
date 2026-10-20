"""Programmatic check of Claim A: for every connected cell (n,m) with 3<=n<=NMAX, 1<=m<=n-2, n<=2m+1 where the Henning-Yeo window
lo=floor((3n+2m)/11)+1 <= min(floor((5n+3m)/17), m) is non-empty, run conn_dfs2 n m lo and record found (must be 0)."""
import subprocess,re,json,sys
NMAX=int(sys.argv[1]); res=[]
for n in range(3,NMAX+1):
    for m in range(1,n-1):
        if n>2*m+1: continue
        lo=(3*n+2*m)//11+1; hi=min((5*n+3*m)//17,m)
        if lo>hi: continue
        o=subprocess.run(['./conn_dfs2',str(n),str(m),str(lo)],capture_output=True,text=True).stdout.strip().splitlines()[-1]
        f=int(re.search(r'found=(\d+)',o).group(1)); nodes=int(re.search(r'nodes=(\d+)',o).group(1))
        res.append(dict(n=n,m=m,tau0=lo,hy_hi=hi,found=f,nodes=nodes)); print(res[-1],flush=True)
json.dump(res,open('results_verify_cells_n%d.json'%NMAX,'w'),indent=1)
