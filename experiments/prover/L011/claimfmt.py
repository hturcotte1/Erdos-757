"""(L011) Write the 22-point witness in the claim format of the frozen verifier (a check only; not a record claim, not in results/claims)."""
import json
w = json.load(open('witness_22.json'))
json.dump({'id': 'W22-f22-witness', 'type': 'construction', 'set': w['set'], 'claimed_h': 13, 'witness_sidon_subset': w['sidon13'],
           'notes': 'L011 witness for f(22) <= 13 (not a record claim): B12 union (5000 + 15*B10)'}, open('witness_check/W22-f22-witness.json', 'w'))
print('written witness_check/W22-f22-witness.json')
