import subprocess,random,time,re,sys
random.seed(1); K=21698; N=int(sys.argv[1]); tot=0; res=[]
for I in random.sample(range(K),N):
    t=time.time()
    o=subprocess.run(['nice','-n','5','./conn_dfs3s','15','11','6','3','0','0',str(K),str(I)],capture_output=True,text=True,timeout=1200).stdout.strip().splitlines()[-1]
    nodes=int(re.search(r'nodes=(\d+)',o).group(1)); found=int(re.search(r'found=(\d+)',o).group(1))
    res.append((I,nodes,found,time.time()-t)); print(res[-1],flush=True)
import statistics
print('mean nodes/slice',statistics.mean(r[1] for r in res),'est total',statistics.mean(r[1] for r in res)*K,'mean found',statistics.mean(r[2] for r in res))
