"""(L016) helper: prints the run-F numbers (from the INFO lines of out/cellsF) in the form used by the certificate."""
import json, os, sys
D = sys.argv[1] if len(sys.argv) > 1 else 'out/cellsF'
def info(k):
    n, m, t, Dd = k; p = os.path.join(D, 'cell_%d_%d_%d_D%d.txt' % k)
    if not os.path.exists(p): return None, None
    L = open(p).read().splitlines(); nf = sum(1 for l in L if l.startswith('FOUND:'))
    return nf, json.loads([l for l in L if l.startswith('INFO ')][0][5:])
for k in [(24,16,9,3), (25,19,10,3), (26,22,11,3), (27,25,12,3)]:
    nf, inf = info(k)
    if inf is None: print(k, 'MISSING'); continue
    print('KEY', k, 'classes', nf, 'secs', inf.get('secs'), 'connected_hits', inf.get('connected_hits'))
    for b in inf['branches']:
        e = b.get('ext', {})
        print('  d=%d tp=%d Sp=%d decs=%d inputs=%d | graphs=%s bad_tau=%s tg_too_small=%s searched=%s max_min_covers=%s nodes=%s hits_F7free=%s hits_in_C=%s | HITlines=%s'
              % (b['d'], b['tp'], b['Sp'], b['decompositions'], b['inputs'], e.get('graphs'), e.get('bad_tau'), e.get('tg_too_small'), e.get('searched'),
                 e.get('max_min_covers'), e.get('nodes'), e.get('hits_F7free'), e.get('hits_in_C'), b.get('hits_in_C')))
