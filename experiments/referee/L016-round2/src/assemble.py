"""assemble the review from the draft parts; placeholders filled from a json of strings"""
import sys, json
R = '/home/user/Erdos-757/experiments/referee/L016-round2/'
fill = json.load(open(sys.argv[1])); out = sys.argv[2]
head = open(R + 'review_draft.txt').read()
body = open(R + 'review_body.txt').read(); checks = open(R + 'review_checks.txt').read(); probs = open(R + 'review_problems.txt').read()
txt = head.replace('__REST__', body + '\n' + checks + '\n' + probs)
for k, v in fill.items(): txt = txt.replace(k, v)
left = [k for k in ['__TS__','__C25__','__C26__','__R14__','__R15__','__R16__','__R17__','__LIMITS__','__REST__'] if k in txt]
assert not left, left
open(out, 'w').write(txt)
print(out, len(txt.splitlines()), 'lines; first line:', txt.split('\n')[0])
