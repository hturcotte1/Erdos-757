import sys, json, gzip, subprocess, os, itertools
sys.path.insert(0,'/home/user/Erdos-757')
from e757.core import ap_edges, is_45_set, alpha
HERE=os.path.dirname(os.path.abspath(__file__))
ROOT='/home/user/Erdos-757'

def edges_idx(A):
    A=sorted(A); idx={x:i for i,x in enumerate(A)}
    return [(idx[a],idx[b],idx[c]) for a,b,c in ap_edges(A)]

def line(n,edges):
    return "%d %d %s\n"%(n,len(edges)," ".join("%d %d %d"%tuple(e) for e in edges))

def run_c(lines_iter, nice=5):
    p=subprocess.Popen(['nice','-n',str(nice),os.path.join(HERE,'subsets')],stdin=subprocess.PIPE,stdout=subprocess.PIPE,text=True)
    out,_=p.communicate("".join(lines_iter))
    # parse
    viol=[l for l in out.splitlines() if l.startswith('VIOLATION')]
    j=json.loads("\n".join(l for l in out.splitlines() if not l.startswith('VIOLATION')))
    j['violation_lines']=viol
    return j

def summarize(j, tag=''):
    hist=j['hist']  # [s,m,tau,count,witline,witmask,slack]
    mn=j['min_slack']
    eq=[h for h in hist if h[6]==0]
    low=sorted(set(h[6] for h in hist))[:6]
    return dict(tag=tag,inputs=j['inputs'],subsets=j['subsets'],violations=j['violations'],min_slack=mn,
                slack_values_lowest=low,
                equality_cases=[dict(n=h[0],m=h[1],tau=h[2],count=h[3],first_input=h[4],first_mask=h[5]) for h in eq],
                slack1_to_5=[dict(n=h[0],m=h[1],tau=h[2],slack=h[6],count=h[3]) for h in hist if 0<h[6]<=3])
