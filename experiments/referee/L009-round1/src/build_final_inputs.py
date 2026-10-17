"""Referee L009: inputs of the final step at class level: one representative of each isomorphism class of the referee's
rebuilt connected (17,13,7) graphs in C (from out/x17.txt) and of the rebuilt connected (14,12,6) graphs in C (from out/x14.txt),
the latter plus the disjoint edge (14,15,16).  Also writes out/T17_reps.txt, out/T14_reps.txt."""
import re, subprocess
D = '/home/user/Erdos-757/experiments/referee/L009-round1/out/'
def reps(fn, n, tag):
    lines = [l for l in open(fn) if l.startswith(tag)]
    out = subprocess.run(['/home/user/Erdos-757/experiments/referee/L009-round1/bin/canon', str(n)], input=''.join(lines), capture_output=True, text=True).stdout.split('\n')
    seen = {}
    for o in out:
        if o:
            c, ln, a = o.split()
            seen.setdefault(c, lines[int(ln) - 1])
    return [re.findall(r'\(([\d,]+)\)', l) for l in seen.values()]
s17 = reps(D + 'x17.txt', 17, 'X tau=7 C=1 conn=1'); s14 = reps(D + 'x14.txt', 14, 'X tau=6 C=1 conn=1')
print(len(s17), 'classes (17,13,7);', len(s14), 'classes (14,12,6)')
with open(D + 'in18_classlevel.txt', 'w') as f:
    for es in s17: f.write('I: ' + ' '.join('(%s)' % e for e in es) + '\n')
    for es in s14: f.write('I: ' + ' '.join('(%s)' % e for e in es) + ' (14,15,16)\n')
for fn, S in (('T17_reps.txt', s17), ('T14_reps.txt', s14)):
    with open(D + fn, 'w') as f:
        for es in S: f.write('FOUND: ' + ' '.join('(%s)' % e for e in es) + '\n')
