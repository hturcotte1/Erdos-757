"""Run ptan over selected cells with slack in [lo,hi]; log to out/. usage: run_cells.py lo hi"""
import json,subprocess,sys,os,time
from feed import stream
lo,hi=int(sys.argv[1]),int(sys.argv[2])
os.makedirs('out',exist_ok=True)
sel=[o for o in json.load(open(sys.argv[3] if len(sys.argv)>3 else 'selected.json')) if lo<=o['slack']<=hi]
sel.sort(key=lambda o:(o['slack'],o['n']))
for o in sel:
    tag='cell_%d_%d_%d_D%d_s%d'%(o['n'],o['m'],o['tau'],o['D'],o['slack'])
    outp='out/'+tag+'.txt'
    if os.path.exists(outp) and os.path.getsize(outp)>0 and open(outp).read().rstrip().endswith('DONE'): continue
    t=time.time()
    p=subprocess.Popen(['nice','-n','10','./ptan','5'],stdin=subprocess.PIPE,stdout=open(outp,'w'),text=True)
    k=0
    for l in stream(o['path']):
        p.stdin.write(l+'\n'); k+=1
    p.stdin.close(); p.wait()
    open(outp,'a').write('GRAPHS %d\nSRC %s\nDONE\n'%(k,o['path']))
    print(tag,k,'graphs',round(time.time()-t,1),'s',flush=True)
