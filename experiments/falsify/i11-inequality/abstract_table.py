import json,os
base='/home/user/Erdos-757/experiments/20261014-0500-slack-landscape/'
out=[]
res={}
for c,f in (("O' (abstract ordered class, K30+K31+cores)","results_op.jsonl"),("realizable","results_real.jsonl")):
    st={}
    for l in open(base+f):
        r=json.loads(l); st[(r['n'],r['m'])]=r
    ns=sorted({n for n,m in st})
    out.append("\n### I11 slack 3n+2m-11*tau_max, class %s (range 'a..b' = unresolved cell, tau_max in a range)\n"%c)
    out.append("| n \\ m | "+" | ".join(str(m) for m in range(1,13))+" |"); out.append("|"+"---|"*13)
    cells={}
    for n in ns:
        row=[]
        for m in range(1,13):
            r=st.get((n,m))
            if r is None or m>n-2: row.append(""); continue
            if r['status']=='optimal':
                tau=n-r['alpha']; s=3*n+2*m-11*tau; row.append(str(s)); cells["%d,%d"%(n,m)]=dict(tau_max=tau,slack=s)
            elif r['status']=='range':
                lo=n-r['alpha']; hi=n-r['alpha_ge']
                s1=3*n+2*m-11*hi; s2=3*n+2*m-11*lo; row.append("%d..%d"%(s1,s2)); cells["%d,%d"%(n,m)]=dict(tau_range=[lo,hi],slack_range=[s1,s2])
            else: row.append("t/o")
        out.append("| %d | "%n+" | ".join(row)+" |")
    res[c]=cells
open('abstract_table.md','w').write("\n".join(out)+"\n")
json.dump(res,open('results_abstract_table.json','w'),indent=1)
print("\n".join(out))
neg=[(c,k,v) for c,cl in res.items() for k,v in cl.items() if ('slack' in v and v['slack']<0) or ('slack_range' in v and v['slack_range'][0]<0)]
print('negative-or-possibly-negative cells:',neg)
