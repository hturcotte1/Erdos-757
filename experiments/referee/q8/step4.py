import json, subprocess
from check import is45, apm, sweep
recs=json.load(open('../../../data/small_records.json'))['sets']
for k,v in recs.items():
    A=v['set']; assert is45(A)
    E,out=sweep(A); print(k,len(A),[l for l in out.splitlines() if l.startswith('RESULT')][0],flush=True)
A=[0,269,385,467,501,511,521,523,535,538,549,575]; assert is45(A)
E,out=sweep(A); print('0..575',[l for l in out.splitlines() if l.startswith('RESULT')][0])
F='../../falsify/q8-omega-inequality/'
rs=json.load(open(F+'random_sets.json')); ad=json.load(open(F+'adv_sets.json'))
for name,A in (('adv16#46',ad['16'][46]),('random16#298',rs['16'][298])):
    import time;t=time.time(); E,out=sweep(A); print(name,[l for l in out.splitlines() if l.startswith('RESULT')][0],round(time.time()-t),'s',flush=True)
