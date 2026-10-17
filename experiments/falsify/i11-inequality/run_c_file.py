from common import *
import sys,time
f=sys.argv[1]; tag=sys.argv[2]; t0=time.time()
p=subprocess.run(['nice','-n','5',HERE+'/subsets'],stdin=open(f),capture_output=True,text=True)
out=p.stdout
viol=[l for l in out.splitlines() if l.startswith('VIOLATION')]
j=json.loads("\n".join(l for l in out.splitlines() if not l.startswith('VIOLATION')))
j['violation_lines']=viol
s=summarize(j,tag); s['secs']=time.time()-t0
json.dump(s,open(HERE+'/results_%s.json'%tag,'w'),indent=1)
print(tag,s['inputs'],s['subsets'],'viol',s['violations'],'min',s['min_slack'],[(e['n'],e['m'],e['tau'],e['count']) for e in s['equality_cases']],round(s['secs']),viol[:3])
