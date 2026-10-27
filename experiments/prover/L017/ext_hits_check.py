"""L017, consistency check of Theorem 4(iii) with the engine counters (Step 9.3): at the top-level cell (24,13,9,3) of L013
the d = 3 branch has only the 2 inputs 5 E1 + (8,5,3) (r = 6 components), and L013's log records hits_F7free = 6.
Theorem 4(iii) (Hall + Lemma U'') implies that no CONNECTED extension of such an input has tau >= 9; so all 6 hits must be
disconnected.  This script rebuilds the 2 inputs exactly as engine.recurse does (one representative per component type,
consecutive vertex blocks), runs L012's unchanged ext_d (args: 23 8 9 3 2), and reports the connectivity of every hit.
Usage: python3 ext_hits_check.py"""
import os, sys, subprocess, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hyp import read_cell, components, tau
HERE = os.path.dirname(os.path.abspath(__file__))
EXT = '/home/user/Erdos-757/experiments/prover/L012/bin/ext_d'
K = read_cell(os.path.join(HERE, 'out/L012/cells/cell_8_5_3_D3.txt')); E1 = read_cell(os.path.join(HERE, 'out/L012/cells/cell_3_1_1_D3.txt'))[0]
lines = []
for k in K:
    es = []; off = 0
    for _ in range(5):
        es += [tuple(v + off for v in e) for e in E1]; off += 3
    es += [tuple(v + off for v in e) for e in k]; off += 8
    assert off == 23
    lines.append('%d ' % len(es) + ' '.join('%d %d %d' % e for e in es))
out = subprocess.run([EXT, '23', '8', '9', '3', '2'], input='\n'.join(lines) + '\n', capture_output=True, text=True, timeout=600).stdout
print('ext_d SUMMARY (pruned run, as in L013):', [l for l in out.splitlines() if l.startswith('SUMMARY')])
out = subprocess.run([EXT, '23', '8', '9', '3', '2', 'noprune'], input='\n'.join(lines) + '\n', capture_output=True, text=True, timeout=600).stdout
print('ext_d SUMMARY (noprune: all hits with tau >= 9, no F7 pruning, no P3 test):', [l for l in out.splitlines() if l.startswith('SUMMARY')])
from hyp import contains_F7, p3_ok
allhits = [l for l in out.splitlines() if l.startswith('HIT')]
hits = [h for h in allhits if not contains_F7(24, [tuple(map(int, t.split(','))) for t in re.findall(r'\((\d+,\d+,\d+)\)', h)])]
print('noprune hits: %d, of which F7-free: %d' % (len(allhits), len(hits)))
for h in hits:
    es = [tuple(map(int, t.split(','))) for t in re.findall(r'\((\d+,\d+,\d+)\)', h)]
    nv = 1 + max(max(e) for e in es)
    nv = max(nv, 24)
    cs = components(range(nv), es)
    big = [c for c in cs if len(c) > 3]
    print('F7-free hit: %d edges, %d components, component sizes %s, tau %d' % (len(es), len(cs), sorted(len(c) for c in cs), tau(nv, es)))
conn = lambda h: len(components(range(24), [tuple(map(int, t.split(','))) for t in re.findall(r'\((\d+,\d+,\d+)\)', h)])) == 1
print('F7-free hits: %d, connected: %d; all noprune hits: %d, connected: %d (Theorem 4(iii) predicts 0 connected hits)'
      % (len(hits), sum(1 for h in hits if conn(h)), len(allhits), sum(1 for h in allhits if conn(h))))
