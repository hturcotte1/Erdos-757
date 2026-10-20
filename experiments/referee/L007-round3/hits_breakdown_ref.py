# Referee check of the C4 breakdown: which input graph each of the 3,186 hits comes from (G = hit minus vertex 13),
# the F7 status of the (10,7,4) class of that input, and whether every F7 copy uses vertex 13 (H-13 F7-free).
import re, subprocess, collections, sys
sys.path.insert(0,'.')
from reff7 import contains
def parse(path,tag):
    return [[tuple(sorted(map(int,t.split(',')))) for t in re.findall(r'\(([\d,]+)\)',l)] for l in open(path) if l.startswith(tag)]
def canon_lines(graphs):
    txt='\n'.join(' '.join(f'({a},{b},{c})' for a,b,c in g) for g in graphs)+'\n'
    return subprocess.run(['./canonfile'],input=txt,capture_output=True,text=True,check=True).stdout.splitlines()
H=parse('../../prover/L007/indep/ext_indep_hits.txt','HIT:')
G=[[e for e in h if 13 not in e] for h in H]
kind=['13_8_5' if (10,11,12) not in g else '10_7_4' for g in G]
# for 10_7_4 inputs: class of the 10-vertex part, F7 status of that class
C10=[[e for e in g if e!=(10,11,12)] for g,k in zip(G,kind) if k=='10_7_4']
f7_10=[contains(c) for c in C10]
uses13=[not contains(g) for g,k in zip(G,kind) if k=='10_7_4']   # G=H-13 F7-free <=> every F7 of H uses 13
cnt=collections.Counter(kind)
print('hits',len(H),'from (13,8,5):',cnt['13_8_5'],'from (10,7,4)+edge:',cnt['10_7_4'])
print('  (10,7,4) part contains F7:',sum(f7_10),' F7-free:',len(f7_10)-sum(f7_10))
print('  among hits over F7-free (10,7,4) parts, every F7 uses vertex 13:',all(u for u,f in zip(uses13,f7_10) if not f),
      '(count',sum(1 for u,f in zip(uses13,f7_10) if not f and u),')')
# labelled outputs per (10,7,4) class in conn_all_10_7_4 and which class has F7
L=parse('rerun/out/conn_all_10_7_4.txt','FOUND:')
cl=canon_lines(L); per=collections.Counter(cl); f7cls={c:contains(g) for c,g in zip(cl,L)}
print('  (10,7,4) labelled outputs per class:',sorted((v,f7cls[k]) for k,v in per.items()))
