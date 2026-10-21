"""(L016) python3 compare_branches16.py REFDIR key=DIR [key=DIR ...]: for every given recursion key, compare the branch data recorded in
the INFO line of DIR/cell_<key>.txt with the reference REFDIR/cell_<key>.txt: (d, t', S', number of decompositions, inputs, the
per-decomposition input counts, all ext_d counters, number of HIT lines) and the number of connected survivors.  (The worker's chunked
driver records the filt summaries in 'filt' instead of 'filt_chunks'; these are not compared.)"""
import sys, os, json
ref = sys.argv[1]; same = diff = 0
def info(p):
    return json.loads([l for l in open(p) if l.startswith('INFO ')][0][5:])
for arg in sys.argv[2:]:
    key, d = arg.split('=')
    n, m, t, D = key.split(','); fn = 'cell_%s_%s_%s_D%s.txt' % (n, m, t, D)
    a, b = info(os.path.join(d, fn)), info(os.path.join(ref, fn))
    if not a['route'].startswith('recurse'):
        ok = all(a.get(k) == b.get(k) for k in ('enum', 'labelled', 'in_C_tau_exact', 'filt'))
        same += ok; diff += (not ok)
        print('%s %s (direct): %s, labelled %s, in C with tau=t %s' % ('IDENTICAL' if ok else 'DIFFERENT', key, a.get('enum'), a.get('labelled'), a.get('in_C_tau_exact')))
        continue
    def brs(x): return [(br['d'], br['tp'], br['Sp'], br['decompositions'], br['inputs'], [s for _, s in br['dec']], br.get('ext'), br.get('hits_in_C')) for br in x['branches']]
    ok = brs(a) == brs(b) and a.get('connected_hits') == b.get('connected_hits')
    same += ok; diff += (not ok)
    print('%s %s: branches %d, inputs %s, nodes %s, hits_in_C %s, connected %s' % ('IDENTICAL' if ok else 'DIFFERENT', key, len(a['branches']),
          [br['inputs'] for br in a['branches']], [br.get('ext', {}).get('nodes') for br in a['branches']], [br.get('hits_in_C') for br in a['branches']], a.get('connected_hits')))
    if not ok: print('   mine  ', brs(a), a.get('connected_hits')); print('   theirs', brs(b), b.get('connected_hits'))
print('SUMMARY keys compared (direct: enum line, labelled, in-C counts, filt summary; recursion: branch data) %d, identical branch data %d, different %d' % (same + diff, same, diff))
