"""(L013, prover) Summarise crosscheck_direct.jsonl (C6) as text lines for the certificate."""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
rows = [json.loads(l) for l in open(os.path.join(HERE, 'crosscheck_direct.jsonl')) if l.strip()]
seen = set(); out = []
for r in rows:
    if 'status' in r: out.append('- (%s): %s' % (','.join(str(r['cell']).split()), r['status'])); continue
    k = tuple(r['cell'])
    if k in seen: continue
    seen.add(k); e = r['direct_enum'].split()
    calls = [x for x in e if x.startswith('calls=')][0][6:]; found = [x for x in e if x.startswith('found=')][0][6:]
    out.append('- (%d,%d,%d,%d): recursion %d classes, direct %d classes, %s (enum_conn calls=%s, labelled graphs found=%s, in C with tau=t: %d; %.1f s)'
               % (k + (r['main_classes'], r['direct_classes'], 'EQUAL' if r['equal'] else 'DIFFERENT', format(int(calls), ','), format(int(found), ','), r['direct_in_C'], r['direct_secs'])))
print('\n'.join(out))
neq = sum(1 for r in rows if 'equal' in r and r['equal'])
unfinished = ['(%s)' % ','.join(r['cell'].split()) for r in rows if 'status' in r]
print('%d completed comparisons, %d of them EQUAL, %d with n >= 22, %d non-empty (%s); %d further runs did not finish (%s) and are not used' % (len(seen), neq, sum(1 for k in seen if k[0] >= 22),
      sum(1 for r in rows if r.get('main_classes', 0) > 0), ', '.join('(%d,%d,%d,%d)' % tuple(r['cell']) for r in rows if r.get('main_classes', 0) > 0), len(unfinished), ', '.join(unfinished)))
