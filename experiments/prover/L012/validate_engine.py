"""(L012) Validation of the recursion of engine.py against direct enumeration: with MD = 5 (so every cell with m >= 6 is built by the
vertex-removal recursion from smaller cells), recompute a set of cells with 6 <= m <= 10 that the main run (MD = 10) obtained by direct
enumeration (enum_conn + filt + canon), and compare the two sets of isomorphism classes (canonical forms)."""
import os, sys, subprocess, json
HERE = os.path.dirname(os.path.abspath(__file__))
os.environ['CELLDIR'] = os.path.join(HERE, 'out', 'cells_md5'); os.environ['ENGINELOG'] = os.path.join(HERE, 'out', 'engine_md5.log'); os.environ['MD'] = '5'
sys.path.insert(0, HERE)
import engine
targets = [(10, 7, 4, 4), (8, 6, 3, 3), (9, 5, 3, 3), (12, 6, 4, 3), (15, 7, 5, 3), (14, 8, 5, 3), (11, 7, 4, 3), (10, 8, 4, 3),
           (13, 9, 5, 3), (11, 8, 4, 3), (16, 10, 6, 3), (12, 7, 4, 2), (13, 8, 4, 2), (15, 9, 5, 2), (18, 10, 6, 2), (12, 10, 5, 4),
           (14, 9, 5, 3), (17, 10, 6, 3), (16, 9, 5, 2), (19, 10, 6, 2)]
def canonset(path, nv):
    L = [l.strip() for l in open(path) if l.startswith('FOUND:')]
    if not L: return set()
    return set(subprocess.run([os.path.join(HERE, 'bin', 'canon'), str(nv)], input='\n'.join(L) + '\n', capture_output=True, text=True).stdout.splitlines())
res = []
for key in targets:
    engine.cell(*key)
    a = canonset(os.path.join(HERE, 'out', 'cells_md5', 'cell_%d_%d_%d_D%d.txt' % key), key[0])
    b = canonset(os.path.join(HERE, 'out', 'cells', 'cell_%d_%d_%d_D%d.txt' % key), key[0])
    r = dict(cell=key, recursion_classes=len(a), direct_classes=len(b), equal=a == b); res.append(r); print(r, flush=True)
json.dump(res, open(os.path.join(HERE, 'validate_engine_output.json'), 'w'), indent=1)
print('ALL EQUAL' if all(r['equal'] for r in res) else 'SOME DIFFER')
