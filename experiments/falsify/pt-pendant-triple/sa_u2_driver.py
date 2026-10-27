import subprocess,sys,os
iters=int(sys.argv[1]); seeds=[int(x) for x in sys.argv[2].split(',')]; Ns=[int(x) for x in sys.argv[3].split(',')]
os.makedirs('sa',exist_ok=True)
for N in Ns:
    for sd in seeds:
        f='sa/u2_N%d_seed%d.txt'%(N,sd)
        if os.path.exists(f) and 'FINAL' in open(f).read(): continue
        mmin=N//2+2; mmax=N-2
        p=subprocess.run(['nice','-n','10','./ptsa','u2',str(N),str(iters),str(sd*100+N),'8',str(mmin),str(mmax),'2.0','0.3'],capture_output=True,text=True,timeout=7200)
        open(f,'w').write(p.stdout+p.stderr)
        print(N,sd,[l[:150] for l in p.stdout.splitlines() if l.startswith('U2')],flush=True)
