import sys, json, gzip, collections
sys.path.insert(0,'src')
from hg import *
R='cells12/cells/'
def cell(name):
    return parse_cell(R+name)
sets={}
sets['tight(3,1,1)']=cell('cell_3_1_1_D4.txt')
sets['tight(10,7,4)D4']=cell('cell_10_7_4_D4.txt')
sets['tight(14,12,6)D4']=cell('cell_14_12_6_D4.txt')
sets['tight(17,13,7)D3']=cell('cell_17_13_7_D3.txt')
# census
cen=[]
for line in gzip.open('../../../data/census_n14_m12_classes.jsonl.gz','rt'):
    d=json.loads(line); cen.append([tuple(e) for e in d['edges']])
sets['census2910']=cen
Ab=[0,136,200,243,246,249,272,286,298,323,400,528,596,1056]
ed=[]
for i in range(14):
    for k in range(i+1,14):
        s=Ab[i]+Ab[k]
        if s%2==0 and (s//2) in Ab:
            ed.append((i,Ab.index(s//2),k) if False else tuple(sorted((i,Ab.index(s//2),k))))
sets['A_base']=[ed]
# slack-1 cells
sets['slack1(8,5,3)D4']=cell('cell_8_5_3_D4.txt')
sets['slack1(12,10,5)D4']=cell('cell_12_10_5_D4.txt')
sets['slack1(15,11,6)D4']=cell('cell_15_11_6_D4.txt')
sets['slack1(19,16,8)D4']=cell('cell_19_16_8_D4.txt')
sets['slack1(22,17,9)D4']=cell('cell_22_17_9_D4.txt')
sets['slack1(26,22,11)D3']=parse_cell('cells16/cells_new/runF/cell_26_22_11_D3.txt')
res={}
univ_examples=[]
for name,L in sets.items():
    cnt=0; viol=0; nuniv_dist=collections.Counter(); univ_deg=collections.Counter(); univ_graphs=0
    sl=collections.Counter(); conn=0; inC=0
    maxdeg=collections.Counter()
    for es in L:
        n=nverts(es); t=tau(n,es); s=slack(n,es,t); sl[s]+=1
        conn+=is_connected(n,es)
        inC+= (in_C(n,es,brute=(n<=22)))
        d=degrees(n,es); maxdeg[max(d)]+=1
        u=[]
        for x in range(n):
            tx=tau(n,es,((1<<n)-1)&~(1<<x))
            assert tx in (t-1,t)
            if tx==t: u.append(x)
        nuniv_dist[len(u)]+=1
        for x in u: univ_deg[d[x]]+=1
        if u:
            univ_graphs+=1
            if len(univ_examples)<50: univ_examples.append({'cell':name,'n':n,'edges':es,'universal':u,'deg':[d[x] for x in u]})
        cnt+=1
    res[name]={'count':cnt,'slack_counter':{str(k):v for k,v in sl.items()},'connected':conn,'inC_checked':inC,
      'maxdeg_dist':dict(maxdeg),'num_universal_vertices_per_graph':{str(k):v for k,v in sorted(nuniv_dist.items())},
      'degree_of_universal_vertices':{str(k):v for k,v in sorted(univ_deg.items())},'graphs_with_universal':univ_graphs}
    print(name,res[name],flush=True)
json.dump(res,open('part1_results.json','w'),indent=1)
json.dump(univ_examples,open('part1_universal_examples.json','w'))
