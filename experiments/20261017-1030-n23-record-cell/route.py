import engine,sys,json,time,itertools
from engine import *
route=sys.argv[1]
t0=time.time()
if route=='4':   # H has a degree-4 vertex: G=H-v=(22,17,9) slack 1, maxdeg<=4, endpoints of the 4 new pairs have G-degree<=3
    N,M,S,D,d,ep=22,17,1,4,4,3
else:            # maxdeg(H)=3: G=(22,18,9) slack 3, maxdeg<=3, endpoints G-degree<=2
    N,M,S,D,d,ep=22,18,3,3,3,2
Gs,P=gprime(N,M,S,D)
log('ROUTE',route,'partitions',[[c[:4] for c in p] for p in P],'G candidates',len(Gs))
hits,last=run_ext(Gs,N,10,d,ep,'final_route'+route)
log('ROUTE',route,'final hits (tau>=10, F7-free, e(S) ok):',len(hits))
json.dump(dict(route=route,partitions=[[c[:4] for c in p] for p in P],G_candidates=len(Gs),ext=last,hits=hits,secs=time.time()-t0,log=engine.LOG),open('results_route%s.json'%route,'w'))
