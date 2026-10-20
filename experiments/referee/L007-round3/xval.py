# Cross-validate the proof's enumerators (conn_dfs2_all = falsifier, enum_conn = prover) against the referee's
# level-wise generator: for each cell (N,M,T0,D) the set of isomorphism classes (referee canonical form) of their
# outputs must equal the referee's class set.  Cells chosen with n in 10..14 where brute force is out of reach.
import subprocess, sys, re, time
def classes_from(text, tag):
    lines=[l for l in text.splitlines() if l.startswith(tag)]
    out=subprocess.run(['./canonfile'],input='\n'.join(lines)+'\n',capture_output=True,text=True,check=True).stdout
    return set(out.splitlines()), len(lines)
def run(cmd): return subprocess.run(['nice','-n','5']+cmd,capture_output=True,text=True,check=True,timeout=550).stdout
cells=[tuple(map(int,c.split())) for c in sys.argv[1:]]
bad=0
for (N,M,T0,D) in cells:
    t0=time.time()
    mine,_=classes_from(run(['./levelgen',str(N),str(M),str(T0),str(D),'0','1']),'CLASS')
    a,na=classes_from(run(['rerun/conn_dfs2_all',str(N),str(M),str(T0),str(D)]),'FOUND')
    b,nb=classes_from(run(['rerun/enum_conn',str(N),str(M),str(T0),str(D),'1']),'FOUND')
    ok = (mine==a==b)
    bad += not ok
    print(f'({N},{M},tau>={T0},D<={D}): referee classes={len(mine)}  conn_dfs2_all outputs={na} classes={len(a)}  enum_conn outputs={nb} classes={len(b)}  {"OK" if ok else "MISMATCH"}  [{time.time()-t0:.1f}s]', flush=True)
print('mismatching cells:',bad)
