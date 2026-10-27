"""Finish cell(26,18,10,3): the python driver process (run1.py) died (its parent run_list2.sh was killed by the operator at ~06:50 UTC, which
took the python process down at the end of the ext_d phase) AFTER all pipelines of both chunks had completed (extsum/filtsum/keys files complete).
This script redoes ONLY stream.recurse's post-processing (counter sums and the same assertions, keys_to_reps, engine.save) from those files."""
import os, sys, math, itertools, json, time
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, 'src'))
os.environ.update(CELLDIR=os.path.join(HERE,'out','cells'), ENGINELOG=os.path.join(HERE,'out','engine.log'), WORKDIR=os.path.join(HERE,'out','work'))
import engine, stream
n,m,t,D = 26,18,10,3; d=3; tp=9; Sp = 3*(n-1)+2*(m-d)-11*tp; assert Sp == 6
decs = engine.decompositions(n-1, m-d, Sp); dec_info=[]; total=0
for dec in decs:
    groups={}
    for c in dec: groups[c]=groups.get(c,0)+1
    size=1
    for typ,k in sorted(groups.items()):
        c=len(engine.cell(typ[0],typ[1],typ[2],d)); size*=math.comb(c+k-1,k)
    dec_info.append([list(dec),size]); total+=size
bases=[os.path.join(HERE,'out','work','rec_26_18_10_D3_d3_tp9_c%d'%i) for i in (0,1)]
assert sum(1 for b in bases for _ in open(b+'.in')) == total, 'input count mismatch'
tot={}; nh=0; nconn=0; fl=[]
for b in bases:
    es=[l for l in stream.rd(b+'.extsum').splitlines() if l.startswith('SUMMARY')]; assert len(es)==1
    for kv in es[0].split()[1:]:
        k,v=kv.split('='); tot[k]=tot.get(k,0)+int(v) if k!='max_min_covers' else max(tot.get(k,0),int(v))
    fs=stream.rd(b+'.filtsum').splitlines()[-1]; fkv=stream.summary_kv(fs); nh+=int(fkv['total']); nconn+=int(fkv['survivors_connected']); fl.append(fs)
assert tot.get('bad_tau',0)==0
assert tot.get('graphs')==total and tot.get('searched',0)+tot.get('tg_too_small',0)+tot.get('bad_tau',0)==total
assert nh==tot.get('hits_in_C',0)
br=dict(d=d,tp=tp,Sp=Sp,decompositions=len(decs),inputs=total,dec=dec_info,ext=tot,hits_in_C=nh,filt_chunks=fl)
reps=stream.keys_to_reps([b+'.keys' for b in bases])
info=dict(route='recurse',driver='stream',branches=[br],connected_hits=nconn,secs=round(time.time()-time.mktime(time.strptime('2026-10-27 05:48:21','%Y-%m-%d %H:%M:%S')),1),
          note='post-processing finished by finish_26_18.py after run1.py died; secs approximate (START 05:48:21 UTC to now)')
engine.save((n,m,t,D),reps,info); engine.log('CELL',(n,m,t,D),'classes',len(reps),'(finish_26_18.py)')
row=['(26,18,10,3)',len(reps),total,tot['nodes'],info['secs'],tot['bad_tau'],nh,'recurse(finished by hand)',time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime())]
open(os.path.join(HERE,'progress.tsv'),'a').write('\t'.join(map(str,row))+'\n')
print(row)
