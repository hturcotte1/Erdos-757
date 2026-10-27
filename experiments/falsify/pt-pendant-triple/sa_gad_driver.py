"""Targeted gadget SA: for each N=29..40 and each cell (N,m,tau) with slack -1 (and slack 0,1 as controls) run ./ptsa gad with m fixed."""
import subprocess,sys,os
iters=int(sys.argv[1]); seeds=[int(x) for x in sys.argv[2].split(',')]; Ns=range(int(sys.argv[3]),int(sys.argv[4])+1)
slacks=[int(x) for x in sys.argv[5].split(',')]
for N in Ns:
  for sl in slacks:
    for tau in range(8,20):
        num=11*tau+sl-3*N
        if num%2: continue
        m=num//2
        if m<max(9,N//2) or m>N-2: continue
        for sd in seeds:
            f='sa/gad_N%d_m%d_t%d_s%d_seed%d.txt'%(N,m,tau,sl,sd)
            if os.path.exists(f) and 'BEST' in open(f).read(): continue
            p=subprocess.run(['nice','-n','10','./ptsa','gad',str(N),str(iters),str(sd+1000*N+m),'2.5','0.3','1.0',str(m),str(m)],capture_output=True,text=True,timeout=7200)
            open(f,'w').write(p.stdout+p.stderr)
            line=[l for l in p.stdout.splitlines() if l.startswith('GAD')]
            print(N,m,tau,'target slack',sl,line[0][:90] if line else 'none',flush=True)
