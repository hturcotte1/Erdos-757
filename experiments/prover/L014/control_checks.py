"""(L014) Non-vacuity controls (f).
(1) A_base: its AP hypergraph recomputed from the point set (vertex i = i-th smallest point; edges = 3-term APs a+c = 2b), compared with
    ../L012/abase_pattern.txt, checked by pyverify (in C, tau = 6, connected, max degree 4) and located in out/cells/cell_14_12_6_D4.txt
    (canonical form by bin/canon 14).
(2) cell(23,21,10,4) of this run against L012 Theorem 3(a): the 699 classes of ../L012/route4_classes.txt.gz, as sets of FOUND lines
    and again as sets of canonical forms recomputed by bin/canon 23 from both files; branch data of the d = 3 branch."""
import os, sys, json, gzip, re, subprocess, itertools
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import pyverify as pv
def found(fn, opener=open):
    reps, info = [], None
    with opener(fn, 'rt') as f:
        for l in f:
            if l.startswith('FOUND:'): reps.append(l.rstrip('\n'))
            elif l.startswith('INFO '): info = json.loads(l[5:])
    return reps, info
def canon(lines, nv):
    r = subprocess.run([os.path.join(HERE, 'bin', 'canon'), str(nv)], input='\n'.join(lines) + '\n', capture_output=True, text=True, check=True)
    out = r.stdout.splitlines(); assert len(out) == len(lines); return out
A = [0, 136, 200, 243, 246, 249, 272, 286, 298, 323, 400, 528, 596, 1056]
idx = {a: i for i, a in enumerate(A)}
E = sorted((idx[a], idx[b], idx[c]) for a, b, c in itertools.combinations(A, 3) if a + c == 2 * b)
line = 'FOUND: ' + ' '.join('(%d,%d,%d)' % e for e in E)
ref = open(os.path.join(HERE, '..', 'L012', 'abase_pattern.txt')).read().strip()
print('(1) A_base: %d three-term APs; equal to L012 abase_pattern.txt: %s; linear %s, F7 %s, (P3) %s, tau %d, connected %s, max degree %d'
      % (len(E), line == ref, pv.linear(E), pv.has_f7(E), pv.p3(E), pv.tau(E), pv.connected(E, range(14)), pv.maxdeg(E)))
c14, _ = found(os.path.join(HERE, 'out', 'cells', 'cell_14_12_6_D4.txt'))
cf = canon([line], 14)[0]; c14c = canon(c14, 14)
print('    cell(14,12,6,4) of this run: %d classes; canonical form of A_base among them: %s (class index %s)' % (len(c14), cf in c14c, c14c.index(cf) if cf in c14c else None))
mine, info = found(os.path.join(HERE, 'out', 'cells', 'cell_23_21_10_D4.txt'))
l12, _ = found(os.path.join(HERE, '..', 'L012', 'route4_classes.txt.gz'), gzip.open)
print('(2) cell(23,21,10,4) of this run: %d classes; L012 route4_classes.txt.gz: %d classes; FOUND-line sets equal: %s' % (len(mine), len(l12), set(mine) == set(l12)))
a, b = set(canon(mine, 23)), set(canon(l12, 23))
print('    recomputed canonical forms: %d and %d distinct, sets equal: %s' % (len(a), len(b), a == b))
for br in info['branches']:
    print('    branch d=%d tp=%d S\'=%d decompositions=%d inputs=%d ext=%s hits_in_C=%s' % (br['d'], br['tp'], br['Sp'], br['decompositions'], br['inputs'], br.get('ext'), br.get('hits_in_C')))
print('    connected_hits', info.get('connected_hits'))
degs = []
for l in mine:
    es = [tuple(map(int, t.split(','))) for t in re.findall(r'\((\d+,\d+,\d+)\)', l)]
    degs.append(pv.maxdeg(es))
print('    maximum degrees of the classes:', {d: degs.count(d) for d in sorted(set(degs))})
