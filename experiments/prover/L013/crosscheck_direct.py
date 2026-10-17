"""(L013, prover) Cross-check (b): recompute a cell by DIRECT enumeration (MD raised, fresh cell directory, so no sub-cell is used:
enum_conn n m t D -> filt (C, tau == t) -> nauty canonical forms) and compare it, as a set of canonical representatives, with the cell
file of the main run (computed by the recursion).  Usage: python3 crosscheck_direct.py MAINCELLDIR n m t D ; appends to crosscheck_direct.jsonl."""
import os, sys, json, time, re
HERE = os.path.dirname(os.path.abspath(__file__))
main_dir = sys.argv[1]; key = tuple(map(int, sys.argv[2:6]))
d = os.path.join(HERE, 'out', 'direct', 'cell_%d_%d_%d_D%d' % key); os.makedirs(d, exist_ok=True)
for f in os.listdir(d): os.remove(os.path.join(d, f))
os.environ['CELLDIR'] = d; os.environ['ENGINELOG'] = os.path.join(d, 'engine.log'); os.environ['MD'] = '99'
sys.path.insert(0, HERE)
import engine
assert engine.MD == 99
t0 = time.time(); reps = engine.cell(*key); secs = round(time.time() - t0, 1)
info = [json.loads(l[5:]) for l in open(os.path.join(d, 'cell_%d_%d_%d_D%d.txt' % key)) if l.startswith('INFO ')][0]
assert info['route'] == 'direct'
mainf = os.path.join(main_dir, 'cell_%d_%d_%d_D%d.txt' % key)
main_reps = [engine.parse_edges(l) for l in open(mainf) if l.startswith('FOUND:')]
main_info = [json.loads(l[5:]) for l in open(mainf) if l.startswith('INFO ')][0]
A = set(tuple(map(tuple, r)) for r in reps); Bm = set(tuple(map(tuple, r)) for r in main_reps)
rec = dict(cell=list(key), main_route=main_info['route'], main_classes=len(Bm), direct_classes=len(A), equal=(A == Bm),
           direct_enum=info['enum'], direct_labelled=info['labelled'], direct_in_C=info['in_C_tau_exact'], direct_secs=secs)
print(json.dumps(rec), flush=True)
open(os.path.join(HERE, 'crosscheck_direct.jsonl'), 'a').write(json.dumps(rec) + '\n')
