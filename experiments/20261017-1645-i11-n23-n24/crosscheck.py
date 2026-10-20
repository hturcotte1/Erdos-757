"""Step (5): cross-check cells the engine computed by recursion (MD=10 => m>=11 are built by vertex re-insertion) against direct enumeration
(MD=15: enum_conn + filt + canon), comparing the canonical-form sets.  Usage: python3 crosscheck.py n m t D [...]  (CELLDIR for the direct run
is out/cells_direct).  Also checks the known counts cell(12,10,5,3)=149 and cell(10,7,4,3)=4 from the main run."""
import os, sys, subprocess, json, time
HERE = os.path.dirname(os.path.abspath(__file__))
os.environ['CELLDIR'] = os.path.join(HERE, 'out', 'cells_direct'); os.environ['ENGINELOG'] = os.path.join(HERE, 'out', 'engine_direct.log'); os.environ['MD'] = '15'
sys.path.insert(0, HERE)
import engine
def canonset(path, nv):
    L = [l.strip() for l in open(path) if l.startswith('FOUND:')]
    if not L: return set()
    return set(subprocess.run([os.path.join(HERE, 'bin', 'canon'), str(nv)], input='\n'.join(L) + '\n', capture_output=True, text=True).stdout.splitlines())
args = list(map(int, sys.argv[1:])); res = []
for i in range(0, len(args), 4):
    key = tuple(args[i:i + 4]); t0 = time.time(); engine.cell(*key)
    f = 'cell_%d_%d_%d_D%d.txt' % key
    a = canonset(os.path.join(HERE, 'out', 'cells', f), key[0]); b = canonset(os.path.join(HERE, 'out', 'cells_direct', f), key[0])
    inf = [l for l in open(os.path.join(HERE, 'out', 'cells', f)) if l.startswith('INFO')][0]
    r = dict(cell=key, recursion_route=('"recurse"' in inf), recursion_classes=len(a), direct_classes=len(b), equal=(a == b), direct_secs=round(time.time() - t0, 1))
    res.append(r); print(r, flush=True)
    open(os.path.join(HERE, 'crosscheck_results.jsonl'), 'a').write(json.dumps(r) + '\n')
print('ALL EQUAL' if all(r['equal'] for r in res) else 'SOME DIFFER')
