"""(L013, prover) Text summary of ext_validate_output.json (top-level branches) and ext_validate_sub_output.json (load-bearing sub-cells)."""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
def summ(fn):
    R = json.load(open(os.path.join(HERE, fn))); parts = []; ns = nw = bfh = ident = 0; allconn0 = True
    for r in R:
        n, m, t, D, d, tp = r['branch']
        v = r['verdicts']; tot = r['noprune_hits']
        desc = ', '.join('%s %s' % (format(c, ','), {'disconnected': 'disconnected', 'F7': 'connected, containing $F_7$', 'P3': 'connected, $F_7$-free, violating (P3)', 'IN_C': 'IN C'}.get(k, k)) for k, c in sorted(v.items(), key=lambda x: -x[1])) if tot else ''
        parts.append('(%d,%d,%d,%d) $d=%d$: %s input%s, %s extension%s with $\\tau\\ge%d$%s' % (n, m, t, D, d, format(r['inputs'], ','), '' if r['inputs'] == 1 else 's', format(tot, ','), '' if tot == 1 else 's', t, ' (%s)' % desc if tot else ''))
        ns += r['sampled_inputs']; nw += r.get('sampled_with_hits', 0); bfh += r['brute_force_hits_on_sample']; ident += r['sample_inputs_identical']
        allconn0 = allconn0 and r['connected_in_C_tau_t'] == 0
    return parts, ns, nw, bfh, ident, allconn0, len(R)
which = sys.argv[1]
parts, ns, nw, bfh, ident, ok, nb = summ('ext_validate_output.json' if which == 'top' else 'ext_validate_sub_output.json')
print('; '.join(parts) + '.')
print('BRANCHES=%d SAMPLED=%d WITHHITS=%d BFHITS=%d IDENTICAL=%d ALLZERO=%s' % (nb, ns, nw, bfh, ident, ok))
