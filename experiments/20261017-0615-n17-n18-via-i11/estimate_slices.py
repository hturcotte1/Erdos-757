import subprocess,random,time,re,sys
n,m,t,d=sys.argv[1:5]; N=int(sys.argv[5]); tl=float(sys.argv[6])
o=subprocess.run(['./conn_dfs3s',n,m,t,d,'0','0','-1','0'],capture_output=True,text=True).stdout.strip().splitlines()[-1]
K=int(re.search(r'cnt=(\d+)',o).group(1)); base=int(re.search(r'nodes=(\d+)',o).group(1)); print('slices',K,'base nodes',base,flush=True)
random.seed(1); res=[]; t0=time.time()
for I in random.sample(range(K),min(N,K)):
    if time.time()-t0>tl: break
    t=time.time()
    o=subprocess.run(['nice','-n','10','./conn_dfs3s',n,m,t if False else sys.argv[3],d,'0','0',str(K),str(I)],capture_output=True,text=True).stdout.strip().splitlines()[-1]
    nodes=int(re.search(r'nodes=(\d+)',o).group(1))-base; found=int(re.search(r'found=(\d+)',o).group(1)); res.append((nodes,found,time.time()-t))
import statistics
mn=statistics.mean(r[0] for r in res); sd=statistics.stdev(r[0] for r in res)
print('samples',len(res),'mean nodes/slice',mn,'stderr',sd/len(res)**.5,'est total nodes',mn*K,'est found',statistics.mean(r[1] for r in res)*K,'mean secs/slice',statistics.mean(r[2] for r in res))
