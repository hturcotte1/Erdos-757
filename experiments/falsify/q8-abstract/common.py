import sys, os, json, random, subprocess
from collections import Counter
sys.path.insert(0,'/home/user/Erdos-757'); sys.path.insert(0,'/home/user/Erdos-757/experiments/falsify/q8-omega-inequality')
from q8lib import run_cases
def mask(e): return sum(1<<v for v in e)
def mk(hid,n,edges,mode,param,seed=0): return (hid,n,[mask(e) for e in edges],mode,param,seed)
def agg(res, hist_acc, viol_acc, eq_acc=None):
    for i,r in res.items():
        for k,v in r['hist']['Q'].items(): hist_acc[k]+=v
        if r['violQ'] or r['violAct']: viol_acc.append(i)
