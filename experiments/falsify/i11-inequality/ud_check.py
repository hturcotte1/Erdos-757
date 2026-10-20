import re,sys,glob,json
sys.path.insert(0,'/home/user/Erdos-757')
from e757.cpsat_model import find_f7
res={}
for f in sorted(glob.glob('ud_*.txt'))+['conn2_all_14_11_6_deg3.txt']:
    c=0;nf=0;first=None
    for l in open(f):
        if l.startswith('FOUND') and l.endswith(')\n'):
            es=[tuple(map(int,t.split(','))) for t in re.findall(r'\(([\d,]+)\)',l)]
            c+=1
            if not find_f7(es):
                nf+=1; first=first or es
    last=[l for l in open(f) if l.startswith('maxdeg')]
    res[f]=dict(found_labelled=c,f7_free=nf,example_f7_free=first,done=bool(last))
    print(f,res[f]['found_labelled'],'F7-free:',nf,'finished' if last else 'RUNNING')
json.dump(res,open('results_ud_check.json','w'),indent=1)
