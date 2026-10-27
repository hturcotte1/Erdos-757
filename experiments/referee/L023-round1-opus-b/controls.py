"""Controls for realize_own.decide (own code): realizable sets must be found realizable, with an explicit (4,5) witness;
the 11 classes of the refereed list cell(14,12,6,4) (L012 tarball, extracted into ref/): verdict per class and Q8 containment."""
import json, sys, os, re, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from realize_own import decide, is45
from q8lib import q8_copies
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = '/home/user/Erdos-757'
def aps(A):
    A = sorted(A); S = set(A); idx = {x: i for i, x in enumerate(A)}; out = []
    for i in range(len(A)):
        for j in range(i + 1, len(A)):
            if (A[i] + A[j]) % 2 == 0 and (A[i] + A[j]) // 2 in S:
                out.append((i, idx[(A[i] + A[j]) // 2], j))
    return out
sets = {
 'A_base': [0,136,200,243,246,249,272,286,298,323,400,528,596,1056],
 'B12': [0,269,385,467,501,511,521,523,535,538,549,575],
}
for f in ('C006-tight-21pt-h12.json', 'C007-c25-witness-f25.json', 'C008-f19-h11.json'):
    sets[f.split('-')[0]] = json.load(open(ROOT + '/results/claims/' + f))['set']
for name, A in sets.items():
    E = aps(A); n = len(A)
    t0 = time.time(); st, sols = decide(E, n, prune=True, stop_at_first=True)
    print('SET %s n=%d APs=%d is45=%s -> %s witness_is45=%s Q8copies=%d %s %.1fs' % (name, n, len(E), is45(A), 'REALIZABLE' if sols else 'NOT-REALIZABLE',
          (sols[0][1] is not None) if sols else '-', len(q8_copies(E)), json.dumps(st), time.time() - t0), flush=True)
L = [l for l in open(HERE + '/ref/L012/cells/cell_14_12_6_D4.txt') if l.startswith('FOUND')]
for i, l in enumerate(L):
    E = [tuple(map(int, t.split(','))) for t in re.findall(r'\((\d+,\d+,\d+)\)', l)]
    st, sols = decide(E, 14, prune=True, stop_at_first=True)
    print('cell(14,12,6,4) class %d: %s witness_is45=%s Q8copies=%d %s' % (i, 'REALIZABLE' if sols else 'NOT-REALIZABLE', (sols[0][1] is not None) if sols else '-', len(q8_copies(E)), json.dumps(st)), flush=True)
